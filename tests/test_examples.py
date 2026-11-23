"""Every shipped example runs and produces its documented result."""

from __future__ import annotations

from pathlib import Path

import pytest

from osel.config import load_config
from osel.runner import run_evaluation


@pytest.mark.parametrize(
    ("config", "expected"),
    [
        ("quickstart/config.yaml", {"exact_match": 0.8, "token_f1": 0.8}),
        ("quickstart/config_v2.yaml", {"exact_match": 0.6, "token_f1": 0.733333}),
        ("function-eval/config.yaml", {"abs_error": 0.0, "within_tolerance": 1.0}),
    ],
)
def test_example_results(examples_dir: Path, config: str, expected: dict[str, float]) -> None:
    rec = run_evaluation(load_config(examples_dir / config))
    for metric, value in expected.items():
        assert rec.aggregates[metric]["mean"] == pytest.approx(value, abs=1e-6)
        assert rec.aggregates[metric]["n_errors"] == 0
