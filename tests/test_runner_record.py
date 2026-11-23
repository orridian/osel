from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from osel.config import load_config
from osel.errors import InvalidInputError
from osel.record import REDACTED, RunStore, load_run, redact, save_run
from osel.runner import run_evaluation

REFS = {"a": "x", "b": "y", "c": "z", "d": "w"}


def test_deterministic_fixture_known_result(make_eval) -> None:
    cfg = make_eval(REFS, {"a": "x", "b": "y", "c": "WRONG", "d": "w"})
    when = datetime(2026, 11, 11, tzinfo=timezone.utc)
    r1 = run_evaluation(load_config(cfg), created_at=when)
    r2 = run_evaluation(load_config(cfg), created_at=when)
    agg = r1.aggregates["exact_match"]
    assert agg["mean"] == 0.75 and agg["n"] == 4 and agg["n_errors"] == 0
    assert r1.run_id == r2.run_id
    assert r1.aggregates == r2.aggregates
    assert r1.created_at == "2026-11-11T00:00:00Z"


def test_missing_prediction_recorded_not_fatal(make_eval) -> None:
    cfg = make_eval(REFS, {"a": "x", "b": "y", "c": "z", "zz": "extra"})
    rec = run_evaluation(load_config(cfg))
    d = next(e for e in rec.examples if e["id"] == "d")
    assert d["errors"][0]["stage"] == "predict" and "no prediction" in d["errors"][0]["message"]
    assert rec.aggregates["exact_match"]["n"] == 3
    assert rec.aggregates["exact_match"]["n_errors"] == 1
    assert any("not in the dataset" in w for w in rec.warnings)


def test_system_exceptions_recorded_safely(tmp_path: Path, examples_dir: Path) -> None:
    rec = run_evaluation(load_config(examples_dir / "function-eval" / "config_buggy.yaml"))
    errored = [e for e in rec.examples if e["errors"]]
    assert {e["id"] for e in errored} == {"a5"}  # negative input raises
    err = errored[0]["errors"][0]
    assert err == {"stage": "predict", "type": "ValueError", "message": "negative inputs not supported"}
    assert "Traceback" not in json.dumps(rec.to_dict())


def test_record_round_trip_and_store(make_eval, tmp_path: Path) -> None:
    rec = run_evaluation(load_config(make_eval(REFS, REFS)))
    path = save_run(rec, tmp_path / "run.json")
    loaded = load_run(path)
    assert loaded.to_dict() == rec.to_dict()
    store = RunStore(tmp_path / "store")
    store.save(rec)
    assert store.load(rec.run_id[:12]).run_id == rec.run_id
    assert store.load("latest").run_id == rec.run_id
    assert store.resolve(str(path)) == path
    with pytest.raises(InvalidInputError):
        store.resolve("does-not-exist")


def test_no_secrets_or_environment_captured(make_eval, monkeypatch) -> None:
    # Fake keys are built by concatenation so secret scanners don't flag the test source.
    monkeypatch.setenv("OPENAI_API_KEY", "sk-" + "supersecretvalue1234567890")
    cfg = make_eval(REFS, REFS, extra={"description": "sk-" + "abcdefghijklmnopqrstuvwxyz"})
    text = json.dumps(run_evaluation(load_config(cfg)).to_dict())
    assert "supersecret" not in text
    assert "sk-abcdefghijklmnop" not in text
    assert "OPENAI_API_KEY" not in text


def test_redact_keys_recursively() -> None:
    data = {"api_key": "a", "nested": {"Auth_Token": "b", "ok": 1}, "list": [{"password": "c"}]}
    out = redact(data)
    assert out == {
        "api_key": REDACTED,
        "nested": {"Auth_Token": REDACTED, "ok": 1},
        "list": [{"password": REDACTED}],
    }


def test_load_run_rejects_bad_files(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text('{"schema_version": "7"}', encoding="utf-8")
    with pytest.raises(InvalidInputError, match="schema_version"):
        load_run(bad)
    bad.write_text("not json", encoding="utf-8")
    with pytest.raises(InvalidInputError, match="not valid JSON"):
        load_run(bad)


def test_config_validation(tmp_path: Path) -> None:
    p = tmp_path / "c.yaml"
    p.write_text("dataset: d.jsonl\nmetrics: []\nseed: x\nbogus: 1\n", encoding="utf-8")
    with pytest.raises(InvalidInputError) as info:
        load_config(p)
    text = str(info.value)
    for fragment in ("unknown key", "exactly one of", "non-empty list", "'seed'"):
        assert fragment in text
