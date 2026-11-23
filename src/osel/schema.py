"""Dataset example schema (version 1).

An example is a JSON object with:

- ``id`` (required): non-empty string, unique within the dataset, stable across versions.
- ``input`` (required): any JSON value given to the system under evaluation.
- ``reference`` (optional): any JSON value; the expected/reference output.
- ``metadata`` (optional): JSON object with free-form annotations (e.g. tags, source).

Unknown top-level keys are rejected so that typos (e.g. ``refrence``) are caught early.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

SCHEMA_VERSION = "1"
REQUIRED_KEYS = ("id", "input")
OPTIONAL_KEYS = ("reference", "metadata")
ALLOWED_KEYS = frozenset(REQUIRED_KEYS + OPTIONAL_KEYS)


@dataclass(frozen=True)
class Example:
    id: str
    input: Any
    reference: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)
    has_reference: bool = False

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"id": self.id, "input": self.input}
        if self.has_reference:
            out["reference"] = self.reference
        if self.metadata:
            out["metadata"] = self.metadata
        return out


def validate_record(obj: Any) -> list[str]:
    """Return a list of problems with a single example record (empty if valid)."""
    if not isinstance(obj, dict):
        return [f"expected a JSON object, got {type(obj).__name__}"]
    problems: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in obj:
            problems.append(f"missing required field '{key}'")
    unknown = sorted(set(obj) - ALLOWED_KEYS)
    if unknown:
        problems.append(
            f"unknown field(s) {', '.join(repr(k) for k in unknown)}; "
            f"allowed: {', '.join(sorted(ALLOWED_KEYS))}"
        )
    if "id" in obj:
        ex_id = obj["id"]
        if not isinstance(ex_id, str) or not ex_id.strip():
            problems.append("field 'id' must be a non-empty string")
    if "metadata" in obj and not isinstance(obj["metadata"], dict):
        problems.append("field 'metadata' must be a JSON object")
    return problems


def example_from_dict(obj: dict[str, Any]) -> Example:
    """Build an Example from an already-validated record."""
    return Example(
        id=obj["id"],
        input=obj["input"],
        reference=obj.get("reference"),
        metadata=dict(obj.get("metadata") or {}),
        has_reference="reference" in obj,
    )
