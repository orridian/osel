"""Load and validate local datasets, and compute dataset identity.

Supported formats:

- ``.jsonl``: one example object per non-blank line.
- ``.json``: either a list of example objects, or ``{"schema_version": "1", "examples": [...]}``.

Dataset identity
----------------
``identity = "sha256:" + sha256(canonical_json(sorted examples))`` where examples are sorted by
``id`` and serialized with sorted keys and no insignificant whitespace. Consequently:

- whitespace, key order, file format (JSON vs JSONL) and row order do **not** change identity;
- any change to an example's ``id``, ``input``, ``reference`` or ``metadata`` **does**.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from osel.errors import InvalidInputError
from osel.schema import SCHEMA_VERSION, Example, example_from_dict, validate_record


@dataclass(frozen=True)
class RowError:
    row: int  # 1-based line (JSONL) or list index + 1 (JSON)
    message: str

    def __str__(self) -> str:
        return f"row {self.row}: {self.message}"


@dataclass(frozen=True)
class Dataset:
    path: str
    examples: tuple[Example, ...]
    identity: str
    schema_version: str = SCHEMA_VERSION

    def __len__(self) -> int:
        return len(self.examples)

    def by_id(self) -> dict[str, Example]:
        return {e.id: e for e in self.examples}


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_identity(examples: tuple[Example, ...] | list[Example]) -> str:
    ordered = sorted(examples, key=lambda e: e.id)
    payload = canonical_json([e.to_dict() for e in ordered]).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _read_text(path: Path, encoding: str) -> str:
    if not path.exists():
        raise InvalidInputError(f"dataset not found: {path}")
    if path.is_dir():
        raise InvalidInputError(f"dataset path is a directory, expected a file: {path}")
    try:
        text = path.read_text(encoding=encoding)
    except UnicodeDecodeError as exc:
        raise InvalidInputError(
            f"cannot decode {path} as {encoding}: {exc.reason} at byte {exc.start}. "
            "Pass the correct --encoding."
        ) from exc
    except LookupError as exc:
        raise InvalidInputError(f"unknown encoding: {encoding}") from exc
    return text.removeprefix("﻿")


def _parse_records(path: Path, text: str) -> tuple[list[tuple[int, Any]], list[RowError]]:
    records: list[tuple[int, Any]] = []
    errors: list[RowError] = []
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        for lineno, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                records.append((lineno, json.loads(line)))
            except json.JSONDecodeError as exc:
                errors.append(RowError(lineno, f"invalid JSON: {exc.msg} (column {exc.colno})"))
        return records, errors
    if suffix == ".json":
        if not text.strip():
            return [], []
        try:
            doc = json.loads(text)
        except json.JSONDecodeError as exc:
            errors.append(RowError(exc.lineno, f"invalid JSON: {exc.msg} (column {exc.colno})"))
            return [], errors
        if isinstance(doc, dict):
            version = str(doc.get("schema_version", SCHEMA_VERSION))
            if version != SCHEMA_VERSION:
                errors.append(RowError(0, f"unsupported schema_version {version!r}"))
                return [], errors
            doc = doc.get("examples")
        if not isinstance(doc, list):
            errors.append(RowError(0, "expected a list of examples or an object with 'examples'"))
            return [], errors
        return [(i, rec) for i, rec in enumerate(doc, start=1)], errors
    raise InvalidInputError(f"unsupported dataset format {suffix!r}; use .jsonl or .json")


def validate_dataset(
    path: str | Path, encoding: str = "utf-8"
) -> tuple[Dataset | None, list[RowError]]:
    """Validate a dataset file. Returns (dataset, []) on success, (None, errors) otherwise.

    Raises InvalidInputError only for file-level problems (missing, undecodable, bad format).
    """
    p = Path(path)
    text = _read_text(p, encoding)
    records, errors = _parse_records(p, text)
    examples: list[Example] = []
    seen: dict[str, int] = {}
    for row, rec in records:
        problems = validate_record(rec)
        if problems:
            errors.extend(RowError(row, msg) for msg in problems)
            continue
        ex = example_from_dict(rec)
        if ex.id in seen:
            errors.append(RowError(row, f"duplicate id {ex.id!r} (first seen at row {seen[ex.id]})"))
            continue
        seen[ex.id] = row
        examples.append(ex)
    if not records and not errors:
        errors.append(RowError(0, "dataset is empty"))
    if errors:
        return None, errors
    ex_tuple = tuple(examples)
    return Dataset(path=str(path), examples=ex_tuple, identity=compute_identity(ex_tuple)), []


def load_dataset(path: str | Path, encoding: str = "utf-8") -> Dataset:
    """Load a dataset, raising InvalidInputError with row-level details if invalid."""
    dataset, errors = validate_dataset(path, encoding)
    if dataset is None:
        raise InvalidInputError(
            f"dataset {path} is invalid ({len(errors)} problem(s))", [str(e) for e in errors]
        )
    return dataset
