"""Command-line interface.

Exit codes (stable):
  0  success / check passed
  1  regression detected (``osel check``)
  2  invalid input (bad dataset, config, run file, arguments, incompatible runs)
  3  internal error (a bug in osel - please report it)
"""

from __future__ import annotations

import argparse
import os
import sys
import traceback
from collections.abc import Sequence
from pathlib import Path

from osel import __version__
from osel.compare import compare_runs, find_regressions
from osel.config import load_config
from osel.dataset import validate_dataset
from osel.errors import (
    EXIT_INTERNAL_ERROR,
    EXIT_INVALID_INPUT,
    EXIT_OK,
    EXIT_REGRESSION,
    InvalidInputError,
    OselError,
)
from osel.record import RunStore, save_run
from osel.report import (
    render_check,
    render_comparison,
    render_run,
    run_summary,
    to_json,
)
from osel.runner import run_evaluation


def _out(text: str) -> None:
    print(text)


def _err(text: str) -> None:
    print(text, file=sys.stderr)


# --- commands -------------------------------------------------------------------------------


def cmd_dataset_validate(args: argparse.Namespace) -> int:
    dataset, errors = validate_dataset(args.path, encoding=args.encoding)
    if args.json:
        _out(
            to_json(
                {
                    "valid": dataset is not None,
                    "path": args.path,
                    "n_examples": len(dataset) if dataset else None,
                    "identity": dataset.identity if dataset else None,
                    "errors": [{"row": e.row, "message": e.message} for e in errors],
                }
            )
        )
    elif dataset is not None:
        _out(f"VALID: {args.path}: {len(dataset)} examples, identity {dataset.identity}")
    else:
        _err(f"INVALID: {args.path}: {len(errors)} problem(s)")
        for e in errors[:50]:
            _err(f"  - {e}")
        if len(errors) > 50:
            _err(f"  ... and {len(errors) - 50} more")
    return EXIT_OK if dataset is not None else EXIT_INVALID_INPUT


def cmd_eval_run(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    if args.name:
        config.name = args.name
    record = run_evaluation(config)
    path = RunStore(args.store).save(record)
    if args.output:
        save_run(record, args.output)
    if args.json:
        _out(to_json(run_summary(record)))
    else:
        _out(render_run(record))
        _out(f"\nSaved run {record.run_id} -> {path}")
        if args.output:
            _out(f"Also written to {args.output}")
    return EXIT_OK


def cmd_run_show(args: argparse.Namespace) -> int:
    record = RunStore(args.store).load(args.run)
    _out(to_json(run_summary(record)) if args.json else render_run(record))
    return EXIT_OK


def cmd_run_list(args: argparse.Namespace) -> int:
    store = RunStore(args.store)
    runs = store.list()
    if not runs:
        _out(f"No runs stored in {store.root}")
        return EXIT_OK
    for p in runs:
        _out(p.stem)
    return EXIT_OK


def cmd_compare(args: argparse.Namespace) -> int:
    store = RunStore(args.store)
    cmp = compare_runs(
        store.load(args.baseline), store.load(args.current),
        allow_incompatible=args.allow_incompatible,
    )
    _out(to_json(cmp.to_dict()) if args.json else render_comparison(cmp))
    return EXIT_OK


def cmd_report(args: argparse.Namespace) -> int:
    record = RunStore(args.store).load(args.run)
    if args.format == "json":
        text = to_json(record.to_dict() if args.full else run_summary(record))
    else:
        text = render_run(record)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
        _out(f"Report written to {args.output}")
    else:
        _out(text)
    return EXIT_OK


def _parse_max_drop(items: Sequence[str]) -> dict[str, float]:
    limits: dict[str, float] = {}
    for item in items:
        name, sep, value = item.partition("=")
        try:
            if not sep or not name:
                raise ValueError
            limits[name] = float(value)
        except ValueError:
            raise InvalidInputError(f"--max-drop expects METRIC=NUMBER, got {item!r}") from None
    return limits


def cmd_check(args: argparse.Namespace) -> int:
    store = RunStore(args.store)
    try:
        baseline_path = store.resolve(args.baseline)
    except InvalidInputError as exc:
        if args.missing_baseline == "warn":
            _err(f"WARNING: baseline not found ({exc.message}); check skipped.")
            return EXIT_OK
        raise InvalidInputError(
            f"baseline not found: {args.baseline}. Create one with `osel eval run "
            "CONFIG --output baseline.json`, or pass --missing-baseline warn."
        ) from exc
    baseline = store.load(str(baseline_path))
    current = store.load(args.current)
    cmp = compare_runs(baseline, current)
    regressions = find_regressions(
        cmp,
        tolerance=args.tolerance,
        per_metric=_parse_max_drop(args.max_drop),
        require_ci=args.require_ci,
        max_new_errors=args.max_new_errors,
    )
    if args.json:
        _out(
            to_json(
                {
                    "passed": not regressions,
                    "comparison": cmp.to_dict(),
                    "regressions": [r.__dict__ for r in regressions],
                }
            )
        )
    else:
        _out(render_check(cmp, regressions))
    return EXIT_REGRESSION if regressions else EXIT_OK


# --- parser ---------------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="osel",
        description="Reproducible, local-first evaluation runs.",
        epilog="Exit codes: 0 ok, 1 regression, 2 invalid input, 3 internal error.",
    )
    p.add_argument("--version", action="version", version=f"osel {__version__}")
    p.add_argument(
        "--store", default=".osel/runs", help="run store directory (default: .osel/runs)"
    )
    sub = p.add_subparsers(dest="command", required=True, metavar="COMMAND")

    ds = sub.add_parser("dataset", help="dataset commands").add_subparsers(
        dest="sub", required=True, metavar="SUBCOMMAND"
    )
    v = ds.add_parser("validate", help="validate a dataset file against the schema")
    v.add_argument("path")
    v.add_argument("--encoding", default="utf-8")
    v.add_argument("--json", action="store_true", help="machine-readable output")
    v.set_defaults(func=cmd_dataset_validate)

    ev = sub.add_parser("eval", help="evaluation commands").add_subparsers(
        dest="sub", required=True, metavar="SUBCOMMAND"
    )
    r = ev.add_parser("run", help="execute a configured evaluation and store the run")
    r.add_argument("config", help="evaluation config (.yaml/.yml/.json)")
    r.add_argument("--output", "-o", help="also write the run record to this path")
    r.add_argument("--name", help="override the run name")
    r.add_argument("--json", action="store_true")
    r.set_defaults(func=cmd_eval_run)

    rn = sub.add_parser("run", help="inspect stored runs").add_subparsers(
        dest="sub", required=True, metavar="SUBCOMMAND"
    )
    s = rn.add_parser("show", help="show a stored run (ID, unique prefix, 'latest' or path)")
    s.add_argument("run")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_run_show)
    ls = rn.add_parser("list", help="list stored run IDs")
    ls.set_defaults(func=cmd_run_list)

    c = sub.add_parser("compare", help="compare two compatible runs")
    c.add_argument("baseline", help="run ID, prefix, 'latest' or file path")
    c.add_argument("current", help="run ID, prefix, 'latest' or file path")
    c.add_argument(
        "--allow-incompatible", action="store_true",
        help="show aggregate deltas even if dataset/metric versions differ (no paired stats)",
    )
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_compare)

    rp = sub.add_parser("report", help="export a report for a run")
    rp.add_argument("run")
    rp.add_argument("--format", choices=["json", "text"], default="text")
    rp.add_argument("--full", action="store_true", help="JSON: include per-example results")
    rp.add_argument("--output", "-o")
    rp.set_defaults(func=cmd_report)

    ck = sub.add_parser("check", help="CI regression check: exit 1 if a metric degraded")
    ck.add_argument("--baseline", required=True)
    ck.add_argument("--current", required=True)
    ck.add_argument(
        "--tolerance", type=float, default=0.0,
        help="allowed absolute degradation of each metric mean (default 0)",
    )
    ck.add_argument(
        "--max-drop", action="append", default=[], metavar="METRIC=VALUE",
        help="per-metric allowed degradation; repeatable",
    )
    ck.add_argument(
        "--require-ci", action="store_true",
        help="only fail when the paired confidence interval also excludes zero",
    )
    ck.add_argument(
        "--max-new-errors", type=int, default=0, metavar="N",
        help="allowed increase in failed examples per metric before failing (default 0)",
    )
    ck.add_argument("--missing-baseline", choices=["fail", "warn"], default="fail")
    ck.add_argument("--json", action="store_true")
    ck.set_defaults(func=cmd_check)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(errors="replace")
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except OselError as exc:
        _err(f"error: {exc}")
        return exc.exit_code
    except KeyboardInterrupt:
        _err("interrupted")
        return EXIT_INTERNAL_ERROR
    except Exception as exc:  # noqa: BLE001
        _err(f"internal error: {type(exc).__name__}: {exc}")
        _err("This is a bug in osel. Please report it (remove any secrets from the output).")
        if os.environ.get("OSEL_DEBUG"):
            traceback.print_exc()
        return EXIT_INTERNAL_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
