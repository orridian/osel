"""Launch-audit edge cases: statistics, regression rules, secrets, and odd system outputs.

Each test documents a behavior a user could rely on in CI.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from osel.cli import main
from osel.compare import compare_runs, find_regressions
from osel.config import config_from_mapping
from osel.record import REDACTED, is_secret_key, redact
from osel.runner import run_evaluation


def _setup(tmp_path: Path, n: int, refs: str | None = None) -> None:
    rows = [{"id": f"k{i:03d}", "input": i, "reference": refs or "a"} for i in range(n)]
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def _preds(tmp_path: Path, name: str, outputs: dict[str, object]) -> str:
    path = tmp_path / f"{name}.jsonl"
    path.write_text(
        "".join(json.dumps({"id": k, "output": v}) + "\n" for k, v in outputs.items()), encoding="utf-8"
    )
    return path.name


def _run(tmp_path: Path, preds: str, metrics: list | None = None, **extra):
    cfg = {"dataset": "data.jsonl", "predictions": preds, "metrics": metrics or ["exact_match"], **extra}
    return run_evaluation(config_from_mapping(cfg, tmp_path))


def _ids(n: int) -> list[str]:
    return [f"k{i:03d}" for i in range(n)]


# --- statistics edge cases ------------------------------------------------------------------


def test_identical_runs_give_zero_width_paired_interval(tmp_path: Path) -> None:
    _setup(tmp_path, 40)
    p = _preds(tmp_path, "p", {k: ("a" if i % 3 else "b") for i, k in enumerate(_ids(40))})
    mc = compare_runs(_run(tmp_path, p), _run(tmp_path, p)).metrics[0]
    assert (mc.paired_mean_diff, mc.paired_ci_low, mc.paired_ci_high) == (0.0, 0.0, 0.0)
    assert mc.ci_excludes_zero is False and mc.direction == "unchanged"


def test_tiny_sample_still_works_and_warns(tmp_path: Path) -> None:
    _setup(tmp_path, 2)
    rec = _run(tmp_path, _preds(tmp_path, "p", {"k000": "a", "k001": "b"}))
    agg = rec.aggregates["exact_match"]
    assert agg["mean"] == 0.5 and agg["small_sample"] is True
    assert 0.0 <= agg["ci_low"] <= agg["ci_high"] <= 1.0
    assert any("unreliable" in w for w in rec.warnings)


def test_large_difference_ci_excludes_zero(tmp_path: Path) -> None:
    _setup(tmp_path, 100)
    good = _run(tmp_path, _preds(tmp_path, "g", {k: "a" for k in _ids(100)}))
    bad_outputs = {k: ("a" if i < 20 else "x") for i, k in enumerate(_ids(100))}
    bad = _run(tmp_path, _preds(tmp_path, "b", bad_outputs))
    mc = compare_runs(good, bad).metrics[0]
    assert mc.paired_mean_diff == pytest.approx(-0.8)
    assert mc.ci_excludes_zero is True and mc.paired_ci_high < 0


def test_comparison_is_seed_deterministic(tmp_path: Path) -> None:
    _setup(tmp_path, 60)
    a = _run(tmp_path, _preds(tmp_path, "a", {k: ("a" if i % 2 else "x") for i, k in enumerate(_ids(60))}))
    b = _run(tmp_path, _preds(tmp_path, "b", {k: ("a" if i % 3 else "x") for i, k in enumerate(_ids(60))}))
    assert compare_runs(a, b).to_dict() == compare_runs(a, b).to_dict()
    m1, m2 = compare_runs(a, b, seed=1).metrics[0], compare_runs(a, b, seed=2).metrics[0]
    assert (m1.paired_ci_low, m1.paired_ci_high) != (m2.paired_ci_low, m2.paired_ci_high)
    assert m1.paired_mean_diff == m2.paired_mean_diff  # the point estimate never depends on the seed


def test_missing_values_pair_only_common_examples(tmp_path: Path) -> None:
    _setup(tmp_path, 10)
    full = _run(tmp_path, _preds(tmp_path, "f", {k: "a" for k in _ids(10)}))
    partial = _run(tmp_path, _preds(tmp_path, "p", {k: "a" for k in _ids(10)[:7]}))
    mc = compare_runs(full, partial).metrics[0]
    assert mc.paired_n == 7
    assert (mc.baseline_n_errors, mc.current_n_errors) == (0, 3)


def test_lower_is_better_regression_with_require_ci(tmp_path: Path) -> None:
    _setup(tmp_path, 50, refs="1")
    base = _run(tmp_path, _preds(tmp_path, "b", {k: "1" for k in _ids(50)}), metrics=["abs_error"])
    worse = _run(tmp_path, _preds(tmp_path, "w", {k: "3" for k in _ids(50)}), metrics=["abs_error"])
    cmp = compare_runs(base, worse)
    assert cmp.metrics[0].direction == "degraded"
    regs = find_regressions(cmp, require_ci=True)
    assert [r.metric for r in regs] == ["abs_error"]
    assert find_regressions(compare_runs(worse, base)) == []  # improvement is not a regression


# --- regression rules for failing examples (audit bug fix) ----------------------------------


def test_new_failures_are_regressions_even_if_mean_holds(tmp_path: Path) -> None:
    _setup(tmp_path, 10)
    base = _run(tmp_path, _preds(tmp_path, "b", {k: "a" for k in _ids(10)}))
    half = _run(tmp_path, _preds(tmp_path, "h", {k: "a" for k in _ids(10)[:5]}))
    cmp = compare_runs(base, half)
    assert cmp.metrics[0].delta == 0  # mean over scored examples is unchanged...
    regs = find_regressions(cmp)  # ...but 5 examples now fail
    assert len(regs) == 1 and "5 more example(s) failed" in regs[0].reason
    assert find_regressions(cmp, max_new_errors=5) == []


def test_all_failures_are_a_regression(tmp_path: Path) -> None:
    _setup(tmp_path, 4)
    base = _run(tmp_path, _preds(tmp_path, "b", {k: "a" for k in _ids(4)}))
    none = _run(tmp_path, _preds(tmp_path, "n", {}))
    regs = find_regressions(compare_runs(base, none))
    assert len(regs) == 1 and "no examples could be scored" in regs[0].reason


def test_fewer_failures_is_not_a_regression(tmp_path: Path) -> None:
    _setup(tmp_path, 6)
    half = _run(tmp_path, _preds(tmp_path, "h", {k: "a" for k in _ids(6)[:3]}))
    full = _run(tmp_path, _preds(tmp_path, "f", {k: "a" for k in _ids(6)}))
    assert find_regressions(compare_runs(half, full)) == []


def test_cli_max_new_errors(tmp_path: Path, capsys, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _setup(tmp_path, 6)
    for name, outputs in (("base", {k: "a" for k in _ids(6)}), ("cur", {k: "a" for k in _ids(6)[:5]})):
        cfg = {"dataset": "data.jsonl", "predictions": _preds(tmp_path, name, outputs),
               "metrics": ["exact_match"]}
        (tmp_path / f"{name}.json").write_text(json.dumps(cfg), encoding="utf-8")
        assert main(["eval", "run", f"{name}.json", "-o", f"{name}_run.json"]) == 0
    capsys.readouterr()
    assert main(["check", "--baseline", "base_run.json", "--current", "cur_run.json"]) == 1
    assert "failed examples 0 -> 1" in capsys.readouterr().out
    args = ["check", "--baseline", "base_run.json", "--current", "cur_run.json"]
    assert main([*args, "--max-new-errors", "1"]) == 0


# --- secrets ---------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "key", ["api_key", "apiKey", "OPENAI_API_KEY", "password", "clientSecret", "auth", "access_token",
            "Authorization", "private_key", "aws_secret_access_key", "session"],
)
def test_secret_keys_redacted(key: str) -> None:
    assert is_secret_key(key)


@pytest.mark.parametrize(
    "key", ["author", "max_tokens", "tokenizer", "authors", "description", "model", "temperature", "keyword"],
)
def test_ordinary_keys_kept(key: str) -> None:
    assert not is_secret_key(key)


def test_secret_looking_values_redacted_anywhere() -> None:
    data = {"notes": ["ghp_" + "a" * 30, "github_pat_" + "b" * 30, "AKIA" + "C" * 16, "harmless"]}
    assert redact(data) == {"notes": [REDACTED, REDACTED, REDACTED, "harmless"]}


def test_reports_never_contain_secrets(tmp_path: Path, capsys, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("MY_SERVICE_TOKEN", "envsecretvalue123")
    _setup(tmp_path, 3)
    cfg = {"dataset": "data.jsonl", "predictions": _preds(tmp_path, "p", {k: "a" for k in _ids(3)}),
           "metrics": ["exact_match"], "description": "sk-" + "z" * 24}
    (tmp_path / "c.json").write_text(json.dumps(cfg), encoding="utf-8")
    assert main(["eval", "run", "c.json", "-o", "r.json"]) == 0
    for args in (["report", "r.json", "--format", "json", "--full"], ["run", "show", "r.json", "--json"]):
        assert main(args) == 0
    text = capsys.readouterr().out + Path("r.json").read_text(encoding="utf-8")
    assert "zzzzzzzz" not in text and "envsecretvalue" not in text and "MY_SERVICE_TOKEN" not in text


# --- run store ordering (audit bug fix) ------------------------------------------------------


def test_latest_uses_creation_time_not_run_id(tmp_path: Path) -> None:
    from datetime import datetime, timezone

    from osel.record import RunStore

    _setup(tmp_path, 2)
    p = _preds(tmp_path, "p", {k: "a" for k in _ids(2)})
    store = RunStore(tmp_path / "store")
    # Same second, so the run_id prefix is identical; only microseconds differ.
    times = [datetime(2026, 1, 1, 12, 0, 0, us, tzinfo=timezone.utc) for us in (100, 200, 300)]
    names = []
    for i, when in enumerate(times):
        cfg = {"dataset": "data.jsonl", "predictions": p, "metrics": ["exact_match"], "name": f"run{i}"}
        rec = run_evaluation(config_from_mapping(cfg, tmp_path), created_at=when)
        store.save(rec)
        names.append(rec.run_id)
    assert len({n[:16] for n in names}) == 1  # identical second-resolution prefix
    assert store.load("latest").name == "run2"
    assert [store.load(str(f)).name for f in store.list()] == ["run0", "run1", "run2"]


# --- odd system outputs ----------------------------------------------------------------------


def test_unserializable_prediction_does_not_crash(tmp_path: Path) -> None:
    _setup(tmp_path, 2)
    (tmp_path / "weird_system.py").write_text("def predict(x):\n    return {x}\n", encoding="utf-8")
    cfg = {"dataset": "data.jsonl", "system": "weird_system:predict", "python_path": ["."],
           "metrics": ["exact_match"]}
    rec = run_evaluation(config_from_mapping(cfg, tmp_path))
    json.dumps(rec.to_dict())  # must be saveable
    assert rec.examples[0]["prediction"] == "{0}"
    assert any("not JSON-serializable" in w for w in rec.warnings)
