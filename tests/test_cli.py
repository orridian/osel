"""CLI behavior: help, exit codes, errors, and the complete documented workflow."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from osel.cli import main


def run(argv: list[str], capsys) -> tuple[int, str, str]:
    code = main(argv)
    out = capsys.readouterr()
    return code, out.out, out.err


@pytest.fixture
def quickstart(tmp_path: Path, examples_dir: Path) -> Path:
    dst = tmp_path / "qs"
    shutil.copytree(examples_dir / "quickstart", dst)
    return dst


def test_help_and_version(capsys) -> None:
    with pytest.raises(SystemExit) as info:
        main(["--help"])
    assert info.value.code == 0
    assert "Exit codes" in capsys.readouterr().out
    with pytest.raises(SystemExit):
        main(["--version"])
    assert "osel" in capsys.readouterr().out


def test_bad_arguments_exit_2(capsys) -> None:
    with pytest.raises(SystemExit) as info:
        main(["compare"])
    assert info.value.code == 2


def test_validate_exit_codes(capsys, fixtures: Path) -> None:
    code, out, _ = run(["dataset", "validate", str(fixtures / "valid.jsonl")], capsys)
    assert code == 0 and out.startswith("VALID")
    code, _, err = run(["dataset", "validate", str(fixtures / "invalid.jsonl")], capsys)
    assert code == 2 and "INVALID" in err and "row 3" in err
    code, out, _ = run(["dataset", "validate", "--json", str(fixtures / "invalid.jsonl")], capsys)
    assert code == 2 and json.loads(out)["valid"] is False
    code, _, err = run(["dataset", "validate", "missing.jsonl"], capsys)
    assert code == 2 and "not found" in err


def test_full_workflow(capsys, quickstart: Path, monkeypatch) -> None:
    """The quickstart, exactly as documented, with known expected results."""
    monkeypatch.chdir(quickstart)
    code, out, _ = run(["eval", "run", "config.yaml", "--output", "baseline.json"], capsys)
    assert code == 0 and "Saved run" in out
    code, out, _ = run(["eval", "run", "config_v2.yaml", "--output", "current.json"], capsys)
    assert code == 0

    base = json.loads(Path("baseline.json").read_text(encoding="utf-8"))
    cur = json.loads(Path("current.json").read_text(encoding="utf-8"))
    assert base["aggregates"]["exact_match"]["mean"] == pytest.approx(0.8)
    assert base["aggregates"]["token_f1"]["mean"] == pytest.approx(0.8)
    assert cur["aggregates"]["exact_match"]["mean"] == pytest.approx(0.6)
    assert cur["aggregates"]["token_f1"]["mean"] == pytest.approx(0.73333, abs=1e-4)

    code, out, _ = run(["run", "list"], capsys)
    assert code == 0 and len(out.strip().splitlines()) == 2
    code, out, _ = run(["run", "show", "latest"], capsys)
    assert code == 0 and "capitals-v2" in out
    code, out, _ = run(["run", "show", base["run_id"], "--json"], capsys)
    assert json.loads(out)["run_id"] == base["run_id"]

    code, out, _ = run(["compare", "baseline.json", "current.json"], capsys)
    assert code == 0 and "DEGRADED" in out

    code, out, _ = run(["report", base["run_id"], "--format", "json"], capsys)
    assert code == 0 and "examples" not in json.loads(out)
    code, out, _ = run(["report", base["run_id"], "--format", "json", "--full"], capsys)
    assert len(json.loads(out)["examples"]) == 10

    code, out, _ = run(["check", "--baseline", "baseline.json", "--current", "current.json"], capsys)
    assert code == 1 and "CHECK FAILED" in out
    code, out, _ = run(
        ["check", "--baseline", "baseline.json", "--current", "current.json", "--tolerance", "0.25"],
        capsys,
    )
    assert code == 0 and "CHECK PASSED" in out
    code, out, _ = run(
        ["check", "--baseline", "baseline.json", "--current", "current.json",
         "--max-drop", "exact_match=0.25", "--max-drop", "token_f1=0.1", "--json"],
        capsys,
    )
    assert code == 0 and json.loads(out)["passed"] is True
    code, out, _ = run(["check", "--baseline", "baseline.json", "--current", "baseline.json"], capsys)
    assert code == 0


def test_missing_baseline_behaviour(capsys, quickstart: Path, monkeypatch) -> None:
    monkeypatch.chdir(quickstart)
    run(["eval", "run", "config.yaml", "-o", "current.json"], capsys)
    code, _, err = run(["check", "--baseline", "nope.json", "--current", "current.json"], capsys)
    assert code == 2 and "baseline not found" in err
    code, _, err = run(
        ["check", "--baseline", "nope.json", "--current", "current.json",
         "--missing-baseline", "warn"],
        capsys,
    )
    assert code == 0 and "WARNING" in err


def test_bad_max_drop_and_incompatible(capsys, quickstart: Path, monkeypatch) -> None:
    monkeypatch.chdir(quickstart)
    run(["eval", "run", "config.yaml", "-o", "a.json"], capsys)
    code, _, err = run(
        ["check", "--baseline", "a.json", "--current", "a.json", "--max-drop", "oops"], capsys
    )
    assert code == 2 and "METRIC=NUMBER" in err
    data = json.loads(Path("a.json").read_text(encoding="utf-8"))
    data["dataset"]["identity"] = "sha256:other"
    Path("b.json").write_text(json.dumps(data), encoding="utf-8")
    code, _, err = run(["compare", "a.json", "b.json"], capsys)
    assert code == 2 and "dataset changed" in err
    code, out, _ = run(["compare", "a.json", "b.json", "--allow-incompatible"], capsys)
    assert code == 0 and "INCOMPATIBLE" in out


def test_internal_error_exit_3(capsys, monkeypatch) -> None:
    import osel.cli as cli

    def boom(args):  # noqa: ANN001
        raise RuntimeError("unexpected")

    monkeypatch.setattr(cli, "cmd_run_list", boom)
    code, _, err = run(["run", "list"], capsys)
    assert code == 3 and "internal error" in err


def test_module_entry_point(tmp_path: Path) -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "osel", "--version"], capture_output=True, text=True, check=False
    )
    assert proc.returncode == 0 and "osel" in proc.stdout
