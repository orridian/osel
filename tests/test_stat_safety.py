"""P0 statistical-safety rules: uninformative intervals and comparison-time warnings.

A zero-width bootstrap interval says nothing about noise, so it must not count as evidence
for ``--require-ci`` unless enough examples moved the same way (sign test).
"""

from __future__ import annotations

import json
from pathlib import Path

from osel.compare import compare_runs, find_regressions
from osel.config import config_from_mapping
from osel.report import render_comparison
from osel.runner import run_evaluation


def _run(tmp_path: Path, name: str, outputs: dict[str, str], refs: dict[str, str], metrics=None):
    (tmp_path / "data.jsonl").write_text(
        "".join(json.dumps({"id": k, "input": k, "reference": v}) + "\n" for k, v in refs.items()),
        encoding="utf-8",
    )
    (tmp_path / f"{name}.jsonl").write_text(
        "".join(json.dumps({"id": k, "output": v}) + "\n" for k, v in outputs.items()),
        encoding="utf-8",
    )
    cfg = {"dataset": "data.jsonl", "predictions": f"{name}.jsonl", "metrics": metrics or ["exact_match"]}
    return run_evaluation(config_from_mapping(cfg, tmp_path))


def _ids(n: int) -> list[str]:
    return [f"k{i:03d}" for i in range(n)]


def _pair(tmp_path: Path, n: int, good: int, metrics=None):
    """Baseline right on all n examples; current right on the first `good`."""
    refs = {k: "a" for k in _ids(n)}
    base = _run(tmp_path, "b", dict(refs), refs, metrics)
    cur = _run(tmp_path, "c", {k: ("a" if i < good else "x") for i, k in enumerate(_ids(n))}, refs, metrics)
    return compare_runs(base, cur)


def test_single_example_interval_is_not_evidence(tmp_path: Path) -> None:
    cmp = _pair(tmp_path, 1, good=0)
    mc = cmp.metrics[0]
    assert mc.direction == "degraded"
    assert mc.paired_ci_low == mc.paired_ci_high == -1.0  # degenerate interval still reported
    assert mc.ci_excludes_zero is None
    assert mc.ci_note is not None and "only 1 paired example" in mc.ci_note
    assert find_regressions(cmp, require_ci=True) == []  # no statistical support claimed
    assert [r.metric for r in find_regressions(cmp)] == ["exact_match"]  # plain rule still fails


def test_few_identical_differences_are_not_evidence(tmp_path: Path) -> None:
    cmp = _pair(tmp_path, 5, good=0)  # 2 * 0.5**5 = 0.0625 > 0.05
    mc = cmp.metrics[0]
    assert mc.ci_excludes_zero is None and "too few" in (mc.ci_note or "")
    assert find_regressions(cmp, require_ci=True) == []


def test_enough_identical_differences_are_evidence(tmp_path: Path) -> None:
    cmp = _pair(tmp_path, 6, good=0)  # 2 * 0.5**6 = 0.03125 <= 0.05
    mc = cmp.metrics[0]
    assert mc.ci_excludes_zero is True and mc.ci_note is None
    assert [r.metric for r in find_regressions(cmp, require_ci=True)] == ["exact_match"]


def test_all_zero_differences_stay_informative(tmp_path: Path) -> None:
    cmp = _pair(tmp_path, 3, good=3)
    mc = cmp.metrics[0]
    assert mc.direction == "unchanged" and mc.ci_excludes_zero is False and mc.ci_note is None


def test_small_sample_warning_on_comparison(tmp_path: Path) -> None:
    cmp = _pair(tmp_path, 10, good=7)
    assert any("only 10 paired examples" in w for w in cmp.warnings)
    assert "warnings:" in render_comparison(cmp)
    assert cmp.to_dict()["warnings"] == cmp.warnings


def test_no_small_sample_warning_at_30(tmp_path: Path) -> None:
    cmp = _pair(tmp_path, 30, good=20)
    assert not any("paired examples" in w for w in cmp.warnings)


def test_multiple_metrics_warning(tmp_path: Path) -> None:
    cmp = _pair(tmp_path, 40, good=30, metrics=["exact_match", "contains", "token_f1"])
    multi = [w for w in cmp.warnings if "metrics compared" in w]
    assert len(multi) == 1
    assert "3 metrics compared" in multi[0] and "14%" in multi[0]  # 1 - 0.95**3 = 0.1426


def test_single_metric_has_no_multiplicity_warning(tmp_path: Path) -> None:
    cmp = _pair(tmp_path, 40, good=30)
    assert not any("metrics compared" in w for w in cmp.warnings)
