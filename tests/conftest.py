from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
EXAMPLES = Path(__file__).parent.parent / "examples"


@pytest.fixture
def fixtures() -> Path:
    return FIXTURES


@pytest.fixture
def examples_dir() -> Path:
    return EXAMPLES


def write_jsonl(path: Path, rows: list[dict]) -> Path:
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return path


@pytest.fixture
def make_eval(tmp_path: Path):
    """Create a dataset + predictions + config in tmp_path; returns the config path."""

    def _make(
        refs: dict[str, str],
        preds: dict[str, str],
        name: str = "t",
        metrics: list | None = None,
        extra: dict | None = None,
    ) -> Path:
        write_jsonl(
            tmp_path / "data.jsonl", [{"id": k, "input": k, "reference": v} for k, v in refs.items()]
        )
        write_jsonl(
            tmp_path / f"pred_{name}.jsonl", [{"id": k, "output": v} for k, v in preds.items()]
        )
        cfg = {
            "name": name,
            "dataset": "data.jsonl",
            "predictions": f"pred_{name}.jsonl",
            "metrics": metrics or ["exact_match"],
            "seed": 0,
            **(extra or {}),
        }
        path = tmp_path / f"config_{name}.json"
        path.write_text(json.dumps(cfg), encoding="utf-8")
        return path

    return _make
