"""Metric interface and built-in metrics.

A metric is any object with:

- ``name: str`` — unique within a run;
- ``version: str`` — bump whenever scoring behavior changes (runs with different versions
  are not comparable);
- ``higher_is_better: bool``;
- ``score(prediction, example) -> float`` — return a finite number, or raise
  :class:`osel.errors.MetricError` if the example cannot be scored.

Custom metrics are referenced in configs as ``"package.module:ClassOrObject"``.
"""

from __future__ import annotations

import importlib
import math
import re
from collections import Counter
from typing import Any, Protocol, runtime_checkable

from osel.errors import InvalidInputError, MetricError
from osel.schema import Example


@runtime_checkable
class Metric(Protocol):
    name: str
    version: str
    higher_is_better: bool

    def score(self, prediction: Any, example: Example) -> float: ...


def _require_reference(example: Example) -> Any:
    if not example.has_reference:
        raise MetricError(f"example {example.id!r} has no 'reference'")
    return example.reference


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


class ExactMatch:
    """1.0 if prediction equals reference, else 0.0.

    Strings are compared after stripping surrounding whitespace; with ``normalize=True``
    they are also lower-cased and internal whitespace is collapsed. Non-strings are
    compared by JSON value equality.
    """

    version = "1"
    higher_is_better = True

    def __init__(self, normalize: bool = False, name: str = "exact_match") -> None:
        self.normalize = normalize
        self.name = name

    def score(self, prediction: Any, example: Example) -> float:
        ref = _require_reference(example)
        if isinstance(prediction, str) and isinstance(ref, str):
            a, b = prediction.strip(), ref.strip()
            if self.normalize:
                a, b = _normalize(a), _normalize(b)
            return float(a == b)
        return float(prediction == ref)


class Contains:
    """1.0 if the reference string occurs in the prediction string (case-insensitive)."""

    version = "1"
    higher_is_better = True

    def __init__(self, name: str = "contains") -> None:
        self.name = name

    def score(self, prediction: Any, example: Example) -> float:
        ref = _require_reference(example)
        if not isinstance(ref, str):
            raise MetricError("contains requires a string reference")
        return float(_normalize(ref) in _normalize(str(prediction)))


class TokenF1:
    """Token-overlap F1 between prediction and reference (whitespace tokens, lower-cased).

    Both empty -> 1.0; exactly one empty -> 0.0.
    """

    version = "1"
    higher_is_better = True

    def __init__(self, name: str = "token_f1") -> None:
        self.name = name

    def score(self, prediction: Any, example: Example) -> float:
        ref = _require_reference(example)
        pred_tokens = _normalize(str(prediction)).split()
        ref_tokens = _normalize(str(ref)).split()
        if not pred_tokens and not ref_tokens:
            return 1.0
        if not pred_tokens or not ref_tokens:
            return 0.0
        common = Counter(pred_tokens) & Counter(ref_tokens)
        overlap = sum(common.values())
        if overlap == 0:
            return 0.0
        precision = overlap / len(pred_tokens)
        recall = overlap / len(ref_tokens)
        return 2 * precision * recall / (precision + recall)


class AbsError:
    """Absolute error |prediction - reference| for numeric outputs (lower is better)."""

    version = "1"
    higher_is_better = False

    def __init__(self, name: str = "abs_error") -> None:
        self.name = name

    def score(self, prediction: Any, example: Example) -> float:
        ref = _require_reference(example)
        try:
            return abs(float(prediction) - float(ref))
        except (TypeError, ValueError) as exc:
            raise MetricError(f"abs_error needs numeric values: {exc}") from exc


BUILTIN_METRICS: dict[str, type] = {
    "exact_match": ExactMatch,
    "contains": Contains,
    "token_f1": TokenF1,
    "abs_error": AbsError,
}


def import_object(ref: str) -> Any:
    """Import ``"package.module:attr"``."""
    module_name, sep, attr = ref.partition(":")
    if not sep or not module_name or not attr:
        raise InvalidInputError(f"expected 'module:attribute', got {ref!r}")
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise InvalidInputError(f"cannot import module {module_name!r}: {exc}") from exc
    obj: Any = module
    for part in attr.split("."):
        try:
            obj = getattr(obj, part)
        except AttributeError as exc:
            raise InvalidInputError(f"{module_name!r} has no attribute {attr!r}") from exc
    return obj


def resolve_metric(spec: str | dict[str, Any]) -> Metric:
    """Build a metric from a config entry.

    ``"exact_match"`` · ``"mypkg.metrics:MyMetric"`` ·
    ``{"use": "exact_match", "params": {"normalize": true}}``
    """
    params: dict[str, Any] = {}
    if isinstance(spec, str):
        use = spec
    elif isinstance(spec, dict):
        raw_use = spec.get("use")
        raw_params = spec.get("params") or {}
        unknown = set(spec) - {"use", "params"}
        if unknown:
            raise InvalidInputError(f"unknown metric option(s): {sorted(unknown)}")
        if not isinstance(raw_use, str):
            raise InvalidInputError("metric entry needs a string 'use' field")
        if not isinstance(raw_params, dict):
            raise InvalidInputError("metric 'params' must be a mapping")
        use, params = raw_use, raw_params
    else:
        raise InvalidInputError(f"invalid metric entry: {spec!r}")

    target: Any = BUILTIN_METRICS.get(use) or (import_object(use) if ":" in use else None)
    if target is None:
        raise InvalidInputError(
            f"unknown metric {use!r}; built-ins: {', '.join(sorted(BUILTIN_METRICS))}, "
            "or use 'module:Class'"
        )
    try:
        metric = target(**params) if isinstance(target, type) else target
    except TypeError as exc:
        raise InvalidInputError(f"invalid params for metric {use!r}: {exc}") from exc
    if params and not isinstance(target, type):
        raise InvalidInputError(f"metric {use!r} is an instance; 'params' are not allowed")
    for attr in ("name", "version", "higher_is_better"):
        if not hasattr(metric, attr):
            raise InvalidInputError(f"metric {use!r} is missing attribute {attr!r}")
    if not callable(getattr(metric, "score", None)):
        raise InvalidInputError(f"metric {use!r} has no callable score()")
    return metric  # type: ignore[no-any-return]


def check_score(value: Any) -> float:
    """Validate a metric's return value."""
    if isinstance(value, bool):
        return float(value)
    if not isinstance(value, (int, float)):
        raise MetricError(f"metric returned {type(value).__name__}, expected a number")
    f = float(value)
    if not math.isfinite(f):
        raise MetricError(f"metric returned non-finite value {f}")
    return f
