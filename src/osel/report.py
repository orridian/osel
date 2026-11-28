"""Human-readable and machine-readable reports.

Text output never relies on colour: every status is spelled out as a word.
"""

from __future__ import annotations

import json
from typing import Any

from osel.compare import Comparison, Regression
from osel.record import RunRecord


def _fmt(v: Any, digits: int = 4) -> str:
    if v is None:
        return "n/a"
    if isinstance(v, float):
        return f"{v:.{digits}f}"
    return str(v)


def to_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


def run_summary(record: RunRecord) -> dict[str, Any]:
    """Stable, machine-readable summary of a run (no per-example data)."""
    return {
        "schema_version": record.schema_version,
        "run_id": record.run_id,
        "name": record.name,
        "created_at": record.created_at,
        "osel_version": record.osel_version,
        "dataset": record.dataset,
        "metrics": record.metrics,
        "statistics": record.statistics,
        "aggregates": record.aggregates,
        "n_examples_with_errors": sum(1 for e in record.examples if e.get("errors")),
        "warnings": record.warnings,
    }


def render_run(record: RunRecord) -> str:
    conf = int(round(float(record.statistics.get("confidence", 0.95)) * 100))
    lines = [
        f"Run {record.run_id}  ({record.name})",
        f"  created:  {record.created_at}   osel {record.osel_version}",
        f"  dataset:  {record.dataset.get('path')}  "
        f"[{record.dataset.get('n_examples')} examples, {record.dataset.get('identity')}]",
        "",
        f"  {'metric':<16}{'mean':>10}{f'{conf}% CI':>22}{'n':>7}{'errors':>8}  better",
    ]
    for name, agg in record.aggregates.items():
        ci = f"[{_fmt(agg.get('ci_low'))}, {_fmt(agg.get('ci_high'))}]"
        better = "higher" if agg.get("higher_is_better") else "lower"
        flag = "  (small n)" if agg.get("small_sample") else ""
        lines.append(
            f"  {name:<16}{_fmt(agg.get('mean')):>10}{ci:>22}{agg.get('n', 0):>7}"
            f"{agg.get('n_errors', 0):>8}  {better}{flag}"
        )
    failed = [e for e in record.examples if e.get("errors")]
    if failed:
        lines += ["", f"  {len(failed)} example(s) had errors, e.g.:"]
        for e in failed[:5]:
            err = e["errors"][0]
            lines.append(f"    - {e['id']}: [{err['stage']}] {err['type']}: {err['message']}")
    if record.warnings:
        lines += ["", "  warnings:"] + [f"    - {w}" for w in record.warnings]
    return "\n".join(lines)


def render_comparison(cmp: Comparison) -> str:
    conf = int(round(cmp.confidence * 100))
    lines = [f"Compare baseline {cmp.baseline_run}  ->  current {cmp.current_run}"]
    if cmp.issues:
        lines.append("  INCOMPATIBLE — showing aggregate deltas only, no paired statistics:")
        lines += [f"    - {i}" for i in cmp.issues]
    lines += [
        "",
        f"  {'metric':<16}{'baseline':>10}{'current':>10}{'delta':>10}"
        f"{f'paired {conf}% CI':>26}  result",
    ]
    for mc in cmp.metrics:
        ci = (
            f"[{_fmt(mc.paired_ci_low)}, {_fmt(mc.paired_ci_high)}]"
            if mc.paired_ci_low is not None
            else "n/a"
        )
        note = ""
        if mc.ci_excludes_zero is False and mc.direction in ("improved", "degraded"):
            note = " (CI includes 0)"
        elif mc.ci_note is not None and mc.direction in ("improved", "degraded"):
            note = " (CI not informative)"
        delta = f"{mc.delta:+.4f}" if mc.delta is not None else "n/a"
        lines.append(
            f"  {mc.metric:<16}{_fmt(mc.baseline_mean):>10}{_fmt(mc.current_mean):>10}"
            f"{delta:>10}{ci:>26}  {mc.direction.upper()}{note}"
        )
    for mc in cmp.metrics:
        if mc.current_n_errors != mc.baseline_n_errors:
            lines.append(
                f"  {mc.metric}: failed examples {mc.baseline_n_errors} -> {mc.current_n_errors} "
                f"(scored {mc.baseline_n} -> {mc.current_n}; means use scored examples only)"
            )
    if cmp.missing_in_current:
        lines.append(f"  missing in current: {', '.join(cmp.missing_in_current)}")
    if cmp.new_in_current:
        lines.append(f"  new in current: {', '.join(cmp.new_in_current)}")
    if cmp.warnings:
        lines += ["", "  warnings:"] + [f"    - {w}" for w in cmp.warnings]
    return "\n".join(lines)


def render_check(cmp: Comparison, regressions: list[Regression]) -> str:
    head = render_comparison(cmp)
    if not regressions:
        return head + "\n\nCHECK PASSED: no metric degraded beyond its tolerance."
    lines = [head, "", f"CHECK FAILED: {len(regressions)} regression(s)"]
    lines += [f"  - {r.metric}: {r.reason}" for r in regressions]
    return "\n".join(lines)
