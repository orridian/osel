"""The claims made in examples/demos/*/README.md must stay true."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from osel.compare import compare_runs, find_regressions
from osel.config import load_config
from osel.errors import IncompatibleRunsError
from osel.runner import run_evaluation

DEMOS = Path(__file__).parent.parent / "examples" / "demos"


def test_demo1_reproducible_and_refuses_changed_data(examples_dir: Path, tmp_path: Path) -> None:
    cfg = examples_dir / "quickstart" / "config.yaml"
    r1, r2 = run_evaluation(load_config(cfg)), run_evaluation(load_config(cfg))
    assert r1.dataset["identity"] == r2.dataset["identity"]
    assert r1.aggregates == r2.aggregates
    assert all(m.direction == "unchanged" for m in compare_runs(r1, r2).metrics)

    changed = tmp_path / "qs"
    shutil.copytree(examples_dir / "quickstart", changed)
    data = changed / "data.jsonl"
    data.write_text(data.read_text(encoding="utf-8").replace('"Oslo"', '"Bergen"'), encoding="utf-8")
    r3 = run_evaluation(load_config(changed / "config.yaml"))
    assert r3.dataset["identity"].startswith("sha256:b11f789f")
    assert r1.dataset["identity"].startswith("sha256:d989320b")
    with pytest.raises(IncompatibleRunsError, match="not comparable"):
        compare_runs(r1, r3)


def test_demo2_regressions(examples_dir: Path) -> None:
    good = run_evaluation(load_config(examples_dir / "function-eval" / "config.yaml"))
    buggy = run_evaluation(load_config(examples_dir / "function-eval" / "config_buggy.yaml"))
    regs = find_regressions(compare_runs(good, buggy))
    assert sorted(r.metric for r in regs) == ["abs_error", "within_tolerance"]
    assert all("1 more example(s) failed" in r.reason for r in regs)


@pytest.mark.parametrize(
    ("scenario", "low", "high", "excludes_zero"),
    [("small", -0.075, 0.15, False), ("large", 0.015, 0.085, True)],
)
def test_demo3_uncertainty(scenario: str, low: float, high: float, excludes_zero: bool) -> None:
    folder = DEMOS / "03-uncertainty" / scenario
    base = run_evaluation(load_config(folder / "baseline.yaml"))
    cand = run_evaluation(load_config(folder / "candidate.yaml"))
    assert base.aggregates["exact_match"]["mean"] == pytest.approx(0.70)
    assert cand.aggregates["exact_match"]["mean"] == pytest.approx(0.75)
    mc = compare_runs(base, cand).metrics[0]
    assert mc.paired_ci_low == pytest.approx(low, abs=1e-9)
    assert mc.paired_ci_high == pytest.approx(high, abs=1e-9)
    assert mc.ci_excludes_zero is excludes_zero
