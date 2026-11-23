from __future__ import annotations

import copy

import pytest

from osel.compare import compare_runs, find_regressions
from osel.config import load_config
from osel.errors import IncompatibleRunsError
from osel.record import RunRecord
from osel.runner import run_evaluation

REFS = {f"k{i:02d}": f"v{i}" for i in range(40)}


def _run(make_eval, preds: dict[str, str], name: str, metrics=None) -> RunRecord:
    return run_evaluation(load_config(make_eval(REFS, preds, name=name, metrics=metrics)))


def _with_wrong(n: int) -> dict[str, str]:
    return {k: ("WRONG" if i < n else v) for i, (k, v) in enumerate(REFS.items())}


def test_equal_runs_unchanged(make_eval) -> None:
    a = _run(make_eval, REFS, "a")
    b = _run(make_eval, REFS, "b")
    cmp = compare_runs(a, b)
    assert cmp.compatible
    mc = cmp.metrics[0]
    assert mc.direction == "unchanged" and mc.delta == 0
    assert mc.paired_n == 40 and mc.paired_mean_diff == 0
    assert find_regressions(cmp) == []


def test_improved_and_degraded(make_eval) -> None:
    good, bad = _run(make_eval, _with_wrong(2), "good"), _run(make_eval, _with_wrong(20), "bad")
    worse = compare_runs(good, bad)
    assert worse.metrics[0].direction == "degraded"
    assert worse.metrics[0].ci_excludes_zero is True  # 18/40 flips is clearly not noise
    regs = find_regressions(worse)
    assert len(regs) == 1 and regs[0].metric == "exact_match"
    assert find_regressions(worse, tolerance=0.5) == []
    assert find_regressions(worse, per_metric={"exact_match": 0.5}) == []
    better = compare_runs(bad, good)
    assert better.metrics[0].direction == "improved"
    assert find_regressions(better) == []


def test_require_ci_ignores_noise(make_eval) -> None:
    a, b = _run(make_eval, _with_wrong(0), "a"), _run(make_eval, _with_wrong(1), "b")
    cmp = compare_runs(a, b)
    assert len(find_regressions(cmp)) == 1
    assert find_regressions(cmp, require_ci=True) == []  # one flip in 40: CI includes 0


def test_lower_is_better_direction(make_eval) -> None:
    refs = {"a": "1", "b": "2"}
    m = ["abs_error"]
    base = run_evaluation(load_config(make_eval(refs, {"a": "1", "b": "2"}, "x", metrics=m)))
    cur = run_evaluation(load_config(make_eval(refs, {"a": "1", "b": "5"}, "y", metrics=m)))
    mc = compare_runs(base, cur).metrics[0]
    assert mc.direction == "degraded" and mc.degradation() == 1.5


def test_changed_dataset_is_incompatible(make_eval) -> None:
    a = _run(make_eval, REFS, "a")
    b = copy.deepcopy(a)
    b.dataset["identity"] = "sha256:different"
    with pytest.raises(IncompatibleRunsError, match="not comparable") as info:
        compare_runs(a, b)
    assert any("dataset changed" in d for d in info.value.details)
    cmp = compare_runs(a, b, allow_incompatible=True)
    assert not cmp.compatible and cmp.metrics[0].paired_ci_low is None


def test_metric_version_change_is_incompatible(make_eval) -> None:
    a = _run(make_eval, REFS, "a")
    b = copy.deepcopy(a)
    b.metrics["exact_match"]["version"] = "2"
    with pytest.raises(IncompatibleRunsError):
        compare_runs(a, b)


def test_missing_metric_is_regression(make_eval) -> None:
    a = _run(make_eval, REFS, "a", metrics=["exact_match", "token_f1"])
    b = _run(make_eval, REFS, "b", metrics=["exact_match"])
    cmp = compare_runs(a, b)
    assert cmp.missing_in_current == ["token_f1"]
    regs = find_regressions(cmp)
    assert [r.metric for r in regs] == ["token_f1"]
