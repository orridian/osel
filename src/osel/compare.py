"""Compare two runs and detect regressions."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from osel import stats
from osel.errors import IncompatibleRunsError
from osel.record import RunRecord

EPS = 1e-12


@dataclass
class MetricComparison:
    metric: str
    higher_is_better: bool
    baseline_mean: float | None
    current_mean: float | None
    delta: float | None
    direction: str  # improved | degraded | unchanged | unknown
    baseline_n: int = 0
    current_n: int = 0
    baseline_n_errors: int = 0
    current_n_errors: int = 0
    paired_n: int = 0
    paired_mean_diff: float | None = None
    paired_ci_low: float | None = None
    paired_ci_high: float | None = None
    ci_excludes_zero: bool | None = None

    def degradation(self) -> float:
        """How much worse current is than baseline (positive = worse)."""
        if self.delta is None:
            return 0.0
        return -self.delta if self.higher_is_better else self.delta


@dataclass
class Comparison:
    baseline_run: str
    current_run: str
    compatible: bool
    issues: list[str]
    metrics: list[MetricComparison]
    missing_in_current: list[str] = field(default_factory=list)
    new_in_current: list[str] = field(default_factory=list)
    confidence: float = 0.95

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compatibility_issues(baseline: RunRecord, current: RunRecord) -> list[str]:
    issues: list[str] = []
    b_id, c_id = baseline.dataset.get("identity"), current.dataset.get("identity")
    if b_id != c_id:
        issues.append(f"dataset changed: baseline {b_id} vs current {c_id}")
    for name in sorted(set(baseline.metrics) & set(current.metrics)):
        bv = baseline.metrics[name].get("version")
        cv = current.metrics[name].get("version")
        if bv != cv:
            issues.append(f"metric {name!r} version changed: {bv} -> {cv}")
        if baseline.metrics[name].get("higher_is_better") != current.metrics[name].get(
            "higher_is_better"
        ):
            issues.append(f"metric {name!r} changed direction (higher_is_better)")
    if not set(baseline.metrics) & set(current.metrics):
        issues.append("runs share no metrics")
    return issues


def _direction(delta: float | None, higher_is_better: bool) -> str:
    if delta is None:
        return "unknown"
    if abs(delta) <= EPS:
        return "unchanged"
    better = delta > 0 if higher_is_better else delta < 0
    return "improved" if better else "degraded"


def compare_runs(
    baseline: RunRecord,
    current: RunRecord,
    *,
    allow_incompatible: bool = False,
    confidence: float | None = None,
    n_resamples: int | None = None,
    seed: int | None = None,
) -> Comparison:
    """Compare two runs. Raises IncompatibleRunsError unless allow_incompatible is set.

    Paired statistics are computed only for compatible runs, over example IDs scored in both.
    """
    issues = compatibility_issues(baseline, current)
    compatible = not issues
    if not compatible and not allow_incompatible:
        raise IncompatibleRunsError("runs are not comparable", issues)

    conf = confidence or float(current.statistics.get("confidence", 0.95))
    samples = n_resamples or int(current.statistics.get("bootstrap_samples", 1000))
    base_seed = seed if seed is not None else int(current.statistics.get("seed", 0))

    shared = [m for m in baseline.metrics if m in current.metrics]
    results: list[MetricComparison] = []
    for i, name in enumerate(shared):
        hib = bool(current.metrics[name].get("higher_is_better", True))
        b_agg = baseline.aggregates.get(name, {})
        c_agg = current.aggregates.get(name, {})
        b_mean, c_mean = b_agg.get("mean"), c_agg.get("mean")
        delta = (c_mean - b_mean) if (b_mean is not None and c_mean is not None) else None
        mc = MetricComparison(
            metric=name,
            higher_is_better=hib,
            baseline_mean=b_mean,
            current_mean=c_mean,
            delta=delta,
            direction=_direction(delta, hib),
            baseline_n=int(b_agg.get("n", 0)),
            current_n=int(c_agg.get("n", 0)),
            baseline_n_errors=int(b_agg.get("n_errors", 0)),
            current_n_errors=int(c_agg.get("n_errors", 0)),
        )
        if compatible:
            b_scores, c_scores = baseline.scores_by_id(name), current.scores_by_id(name)
            ids = sorted(set(b_scores) & set(c_scores))
            paired = stats.paired_difference(
                [b_scores[k] for k in ids],
                [c_scores[k] for k in ids],
                confidence=conf,
                n_resamples=samples,
                seed=base_seed + i,
            )
            if paired is not None:
                mc.paired_n = paired.n
                mc.paired_mean_diff = paired.mean_diff
                if paired.interval is not None:
                    mc.paired_ci_low = paired.interval.low
                    mc.paired_ci_high = paired.interval.high
                    mc.ci_excludes_zero = paired.interval.excludes_zero()
        results.append(mc)

    return Comparison(
        baseline_run=baseline.run_id,
        current_run=current.run_id,
        compatible=compatible,
        issues=issues,
        metrics=results,
        missing_in_current=sorted(set(baseline.metrics) - set(current.metrics)),
        new_in_current=sorted(set(current.metrics) - set(baseline.metrics)),
        confidence=conf,
    )


@dataclass
class Regression:
    metric: str
    degradation: float
    tolerance: float
    reason: str


def find_regressions(
    comparison: Comparison,
    *,
    tolerance: float = 0.0,
    per_metric: dict[str, float] | None = None,
    require_ci: bool = False,
    max_new_errors: int = 0,
) -> list[Regression]:
    """Return metrics that regressed.

    A metric regresses when any of these holds:

    - it is missing from the current run;
    - the current run scored no examples for it but the baseline did;
    - more examples failed (prediction or scoring errors) than in the baseline, beyond
      ``max_new_errors``. Means are computed over scored examples only, so without this
      rule a system that crashes on hard examples could *improve* its mean;
    - its mean degraded by more than the allowed tolerance (``tolerance``, overridden per
      metric by ``per_metric``). With ``require_ci`` this rule also needs the paired CI to
      exclude zero (the degradation is distinguishable from resampling noise).
    """
    limits = per_metric or {}
    out: list[Regression] = [
        Regression(m, float("inf"), limits.get(m, tolerance), "metric missing in current run")
        for m in comparison.missing_in_current
    ]
    for mc in comparison.metrics:
        allowed = limits.get(mc.metric, tolerance)
        if mc.baseline_mean is not None and mc.current_mean is None:
            out.append(
                Regression(mc.metric, float("inf"), allowed, "no examples could be scored in current run")
            )
            continue
        new_errors = mc.current_n_errors - mc.baseline_n_errors
        if new_errors > max_new_errors:
            out.append(
                Regression(
                    mc.metric,
                    float(new_errors),
                    float(max_new_errors),
                    f"{new_errors} more example(s) failed than in baseline "
                    f"({mc.baseline_n_errors} -> {mc.current_n_errors}; allowed {max_new_errors})",
                )
            )
            continue
        deg = mc.degradation()
        if deg <= allowed + EPS:
            continue
        if require_ci and mc.ci_excludes_zero is not True:
            continue
        out.append(
            Regression(mc.metric, deg, allowed, f"mean degraded by {deg:.6g} (allowed {allowed:g})")
        )
    return out
