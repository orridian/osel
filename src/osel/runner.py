"""Evaluation runner: produce predictions, score them, aggregate, and build a RunRecord."""

from __future__ import annotations

import hashlib
import json
import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from osel import stats
from osel.config import EvalConfig
from osel.dataset import canonical_json, load_dataset
from osel.errors import InvalidInputError
from osel.metrics import Metric, check_score, import_object, resolve_metric
from osel.record import RunRecord, environment_metadata, redact

MAX_ERROR_CHARS = 500


def _error(stage: str, exc: BaseException, metric: str | None = None) -> dict[str, Any]:
    msg = str(exc)
    if len(msg) > MAX_ERROR_CHARS:
        msg = msg[:MAX_ERROR_CHARS] + "…"
    err = {"stage": stage, "type": type(exc).__name__, "message": msg}
    if metric:
        err["metric"] = metric
    return err


@contextmanager
def _extra_sys_path(paths: list[Path]) -> Iterator[None]:
    added = [str(p.resolve()) for p in paths]
    sys.path[:0] = added
    try:
        yield
    finally:
        for p in added:
            if p in sys.path:
                sys.path.remove(p)


def load_predictions(path: Path, encoding: str = "utf-8") -> dict[str, Any]:
    """Load a predictions JSONL file with ``{"id": ..., "output": ...}`` per line."""
    if not path.is_file():
        raise InvalidInputError(f"predictions file not found: {path}")
    preds: dict[str, Any] = {}
    problems: list[str] = []
    text = path.read_text(encoding=encoding).removeprefix("﻿")
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            problems.append(f"row {lineno}: invalid JSON: {exc.msg}")
            continue
        if not isinstance(obj, dict) or not isinstance(obj.get("id"), str) or "output" not in obj:
            problems.append(f"row {lineno}: expected an object with string 'id' and 'output'")
            continue
        if obj["id"] in preds:
            problems.append(f"row {lineno}: duplicate prediction for id {obj['id']!r}")
            continue
        preds[obj["id"]] = obj["output"]
    if problems:
        raise InvalidInputError(f"predictions file {path} is invalid", problems)
    return preds


def _json_safe(value: Any) -> tuple[Any, bool]:
    """Return (value, True) if JSON-serializable, else (repr(value), False)."""
    try:
        json.dumps(value)
    except (TypeError, ValueError):
        return repr(value)[:MAX_ERROR_CHARS], False
    return value, True


def _make_run_id(created: datetime, payload: str) -> str:
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:8]
    return f"{created.strftime('%Y%m%dT%H%M%SZ')}-{digest}"


def _aggregate(
    values: list[float], n_errors: int, metric: Metric, config: EvalConfig, salt: int
) -> dict[str, Any]:
    ci = stats.bootstrap_mean_ci(
        values,
        confidence=config.confidence,
        n_resamples=config.bootstrap_samples,
        seed=config.seed + salt,
    )
    return {
        "n": len(values),
        "n_errors": n_errors,
        "mean": stats.mean(values),
        "std": stats.sample_std(values),
        "min": min(values) if values else None,
        "max": max(values) if values else None,
        "ci_low": ci.low if ci else None,
        "ci_high": ci.high if ci else None,
        "higher_is_better": bool(metric.higher_is_better),
        "small_sample": len(values) < stats.SMALL_SAMPLE,
    }


def run_evaluation(config: EvalConfig, *, created_at: datetime | None = None) -> RunRecord:
    """Execute a configured evaluation and return its run record (not yet saved)."""
    dataset = load_dataset(config.dataset, config.encoding)
    warnings: list[str] = []

    with _extra_sys_path(config.python_path):
        metrics = [resolve_metric(spec) for spec in config.metrics]
        names = [m.name for m in metrics]
        dupes = sorted({n for n in names if names.count(n) > 1})
        if dupes:
            raise InvalidInputError(f"duplicate metric name(s): {', '.join(dupes)}")

        predict: Callable[[Any], Any] | None = None
        predictions: dict[str, Any] = {}
        if config.predictions is not None:
            predictions = load_predictions(config.predictions, config.encoding)
            extra = sorted(set(predictions) - {e.id for e in dataset.examples})
            if extra:
                warnings.append(
                    f"{len(extra)} prediction(s) have ids not in the dataset and were ignored"
                )
        else:
            assert config.system is not None
            obj = import_object(config.system)
            if not callable(obj):
                raise InvalidInputError(f"system {config.system!r} is not callable")
            predict = obj

        values: dict[str, list[float]] = {m.name: [] for m in metrics}
        errors: dict[str, int] = {m.name: 0 for m in metrics}
        results: list[dict[str, Any]] = []
        unserializable = 0
        for ex in dataset.examples:
            entry: dict[str, Any] = {"id": ex.id, "scores": {}, "errors": []}
            try:
                if predict is not None:
                    prediction = predict(ex.input)
                elif ex.id in predictions:
                    prediction = predictions[ex.id]
                else:
                    raise LookupError(f"no prediction for id {ex.id!r}")
            except Exception as exc:  # noqa: BLE001 - recorded per example, run continues
                entry["errors"].append(_error("predict", exc))
                for m in metrics:
                    errors[m.name] += 1
                results.append(entry)
                continue
            if config.record_predictions:
                stored, ok = _json_safe(prediction)
                entry["prediction"] = stored
                if not ok:
                    unserializable += 1
            for m in metrics:
                try:
                    score = check_score(m.score(prediction, ex))
                except Exception as exc:  # noqa: BLE001
                    entry["errors"].append(_error("score", exc, metric=m.name))
                    errors[m.name] += 1
                    continue
                entry["scores"][m.name] = score
                values[m.name].append(score)
            results.append(entry)

    if unserializable:
        warnings.append(
            f"{unserializable} prediction(s) were not JSON-serializable and were stored as repr() text"
        )
    for m in metrics:
        if errors[m.name]:
            warnings.append(f"metric {m.name!r}: {errors[m.name]} example(s) could not be scored")
        if 0 < len(values[m.name]) < stats.SMALL_SAMPLE:
            warnings.append(
                f"metric {m.name!r}: only {len(values[m.name])} scored examples; "
                "bootstrap intervals are unreliable below 30"
            )

    created = (created_at or datetime.now(timezone.utc)).astimezone(timezone.utc)
    raw_config = redact(config.raw)
    run_id = _make_run_id(
        created, canonical_json([raw_config, dataset.identity, created.isoformat()])
    )
    return RunRecord(
        run_id=run_id,
        created_at=created.isoformat().replace("+00:00", "Z"),
        name=config.name,
        osel_version=environment_metadata()["osel_version"],
        config=raw_config,
        dataset={
            "path": str(config.raw.get("dataset")),
            "identity": dataset.identity,
            "n_examples": len(dataset),
            "schema_version": dataset.schema_version,
        },
        metrics={
            m.name: {"version": str(m.version), "higher_is_better": bool(m.higher_is_better)}
            for m in metrics
        },
        environment=environment_metadata(config.base_dir),
        statistics={
            "method": "percentile bootstrap of the mean",
            "confidence": config.confidence,
            "bootstrap_samples": config.bootstrap_samples,
            "seed": config.seed,
        },
        aggregates={
            m.name: _aggregate(values[m.name], errors[m.name], m, config, salt=i)
            for i, m in enumerate(metrics)
        },
        examples=results,
        warnings=warnings,
    )
