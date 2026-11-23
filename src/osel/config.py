"""Evaluation config (YAML or JSON).

Example::

    name: quickstart
    dataset: data.jsonl          # relative to the config file
    predictions: predictions.jsonl   # OR  system: "mypkg.module:predict"
    metrics: [exact_match, token_f1]
    seed: 0

Paths are resolved relative to the config file's directory.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from osel.errors import InvalidInputError

ALLOWED_KEYS = {
    "name",
    "description",
    "dataset",
    "encoding",
    "predictions",
    "system",
    "python_path",
    "metrics",
    "seed",
    "bootstrap_samples",
    "confidence",
    "record_predictions",
}


@dataclass
class EvalConfig:
    name: str
    dataset: Path
    metrics: list[str | dict[str, Any]]
    base_dir: Path
    encoding: str = "utf-8"
    predictions: Path | None = None
    system: str | None = None
    python_path: list[Path] = field(default_factory=list)
    seed: int = 0
    bootstrap_samples: int = 1000
    confidence: float = 0.95
    record_predictions: bool = True
    raw: dict[str, Any] = field(default_factory=dict)


def _parse_file(path: Path) -> Any:
    if not path.is_file():
        raise InvalidInputError(f"config not found: {path}")
    text = path.read_text(encoding="utf-8")
    try:
        if path.suffix.lower() == ".json":
            return json.loads(text)
        return yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise InvalidInputError(f"cannot parse config {path}: {exc}") from exc


def config_from_mapping(raw: Any, base_dir: Path) -> EvalConfig:
    if not isinstance(raw, dict):
        raise InvalidInputError("config must be a mapping (key: value pairs)")
    problems: list[str] = []
    unknown = sorted(set(raw) - ALLOWED_KEYS)
    if unknown:
        problems.append(f"unknown key(s): {', '.join(unknown)}")
    if not isinstance(raw.get("dataset"), str):
        problems.append("'dataset' (path string) is required")
    has_pred = raw.get("predictions") is not None
    has_sys = raw.get("system") is not None
    if has_pred == has_sys:
        problems.append("set exactly one of 'predictions' (file) or 'system' (module:function)")
    metrics = raw.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        problems.append("'metrics' must be a non-empty list")
    seed = raw.get("seed", 0)
    if not isinstance(seed, int) or isinstance(seed, bool):
        problems.append("'seed' must be an integer")
    samples = raw.get("bootstrap_samples", 1000)
    if not isinstance(samples, int) or isinstance(samples, bool) or samples < 1:
        problems.append("'bootstrap_samples' must be a positive integer")
    confidence = raw.get("confidence", 0.95)
    if not isinstance(confidence, (int, float)) or not 0 < float(confidence) < 1:
        problems.append("'confidence' must be between 0 and 1 (exclusive)")
    python_path = raw.get("python_path", [])
    if not isinstance(python_path, list) or not all(isinstance(p, str) for p in python_path):
        problems.append("'python_path' must be a list of path strings")
    if problems:
        raise InvalidInputError("invalid evaluation config", problems)

    def resolve(p: str) -> Path:
        path = Path(p)
        return path if path.is_absolute() else (base_dir / path)

    return EvalConfig(
        name=str(raw.get("name") or Path(raw["dataset"]).stem),
        dataset=resolve(raw["dataset"]),
        metrics=list(metrics),  # type: ignore[arg-type]
        base_dir=base_dir,
        encoding=str(raw.get("encoding", "utf-8")),
        predictions=resolve(raw["predictions"]) if has_pred else None,
        system=str(raw["system"]) if has_sys else None,
        python_path=[resolve(p) for p in python_path],
        seed=seed,
        bootstrap_samples=samples,
        confidence=float(confidence),
        record_predictions=bool(raw.get("record_predictions", True)),
        raw=dict(raw),
    )


def load_config(path: str | Path) -> EvalConfig:
    p = Path(path)
    return config_from_mapping(_parse_file(p), p.resolve().parent)
