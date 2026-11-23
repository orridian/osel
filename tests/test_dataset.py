from __future__ import annotations

from pathlib import Path

import pytest

from osel.dataset import compute_identity, load_dataset, validate_dataset
from osel.errors import InvalidInputError
from osel.schema import Example, example_from_dict, validate_record


def test_valid_jsonl_loads(fixtures: Path) -> None:
    ds = load_dataset(fixtures / "valid.jsonl")
    assert [e.id for e in ds.examples] == ["e1", "e2", "e3"]  # blank line skipped
    assert ds.examples[1].metadata == {"difficulty": "easy"}
    assert ds.identity.startswith("sha256:") and len(ds.identity) == 7 + 64


def test_invalid_fixture_reports_every_row(fixtures: Path) -> None:
    ds, errors = validate_dataset(fixtures / "invalid.jsonl")
    assert ds is None
    by_row: dict[int, list[str]] = {}
    for e in errors:
        by_row.setdefault(e.row, []).append(e.message)
    assert 1 not in by_row  # the valid row is fine
    assert any("non-empty string" in m for m in by_row[2])
    assert any("invalid JSON" in m for m in by_row[3])
    assert any("missing required field 'input'" in m for m in by_row[4])
    assert any("refrence" in m for m in by_row[5])
    assert any("JSON object" in m for m in by_row[6])
    assert any("duplicate id 'e1'" in m for m in by_row[7])
    assert any("metadata" in m for m in by_row[8])


def test_load_invalid_raises_with_details(fixtures: Path) -> None:
    with pytest.raises(InvalidInputError) as info:
        load_dataset(fixtures / "invalid.jsonl")
    assert info.value.exit_code == 2
    assert len(info.value.details) >= 7


def test_identity_ignores_order_format_and_whitespace(fixtures: Path) -> None:
    a = load_dataset(fixtures / "valid.jsonl")
    b = load_dataset(fixtures / "valid_reordered.json")
    assert a.identity == b.identity


def test_identity_detects_content_change() -> None:
    base = [Example("a", "x", "1", has_reference=True), Example("b", "y", "2", has_reference=True)]
    changed = [Example("a", "x", "1", has_reference=True), Example("b", "y", "3", has_reference=True)]
    meta = [Example("a", "x", "1", {"t": 1}, True), Example("b", "y", "2", has_reference=True)]
    ids = {compute_identity(base), compute_identity(changed), compute_identity(meta)}
    assert len(ids) == 3


def test_reference_none_differs_from_missing_reference() -> None:
    with_none = [example_from_dict({"id": "a", "input": 1, "reference": None})]
    without = [example_from_dict({"id": "a", "input": 1})]
    assert compute_identity(with_none) != compute_identity(without)


def test_round_trip_serialization() -> None:
    rec = {"id": "a", "input": {"q": [1, 2]}, "reference": None, "metadata": {"k": "v"}}
    assert validate_record(rec) == []
    assert example_from_dict(rec).to_dict() == rec


def test_empty_file(tmp_path: Path) -> None:
    (tmp_path / "empty.jsonl").write_text("\n\n", encoding="utf-8")
    ds, errors = validate_dataset(tmp_path / "empty.jsonl")
    assert ds is None and "empty" in errors[0].message


def test_missing_file_and_bad_extension(tmp_path: Path) -> None:
    with pytest.raises(InvalidInputError, match="not found"):
        load_dataset(tmp_path / "nope.jsonl")
    (tmp_path / "data.csv").write_text("id,input\n", encoding="utf-8")
    with pytest.raises(InvalidInputError, match="unsupported dataset format"):
        load_dataset(tmp_path / "data.csv")


def test_explicit_encoding_and_bom(tmp_path: Path) -> None:
    p = tmp_path / "latin.jsonl"
    p.write_bytes('{"id": "a", "input": "café"}\n'.encode("latin-1"))
    with pytest.raises(InvalidInputError, match="cannot decode"):
        load_dataset(p)
    assert load_dataset(p, encoding="latin-1").examples[0].input == "café"
    bom = tmp_path / "bom.jsonl"
    bom.write_bytes('﻿{"id": "a", "input": "x"}\n'.encode())
    assert len(load_dataset(bom)) == 1


def test_json_object_wrong_schema_version(tmp_path: Path) -> None:
    p = tmp_path / "d.json"
    p.write_text('{"schema_version": "99", "examples": []}', encoding="utf-8")
    ds, errors = validate_dataset(p)
    assert ds is None and "schema_version" in errors[0].message
