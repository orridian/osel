"""Statistical helpers.

Methods and assumptions (also documented in docs/statistics.md):

- Point estimate: arithmetic mean of per-example scores.
- Spread: sample standard deviation (n - 1 denominator).
- Uncertainty: percentile bootstrap confidence interval for the mean, with a fixed seed so
  results are reproducible. Assumes examples are independent draws from the population of
  interest. Percentile bootstrap intervals are unreliable for small samples (n < 30) and for
  heavily skewed scores; reports flag small n.
- Paired comparison: bootstrap CI of the mean per-example difference (current - baseline) over
  examples scored in *both* runs. This accounts for example difficulty, which unpaired
  comparisons ignore.
- No p-values or universal "significant" labels are produced. A CI that excludes zero is
  reported as such, with its confidence level — nothing more.

Quantiles use linear interpolation between order statistics (the same definition as
``statistics.quantiles(method="inclusive")`` and NumPy's default), which tests check.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence
from dataclasses import dataclass

SMALL_SAMPLE = 30


def mean(values: Sequence[float]) -> float | None:
    return math.fsum(values) / len(values) if values else None


def sample_std(values: Sequence[float]) -> float | None:
    n = len(values)
    if n < 2:
        return None
    m = math.fsum(values) / n
    return math.sqrt(math.fsum((v - m) ** 2 for v in values) / (n - 1))


def quantile(sorted_values: Sequence[float], q: float) -> float:
    """Linear-interpolation quantile of already-sorted values, 0 <= q <= 1."""
    if not sorted_values:
        raise ValueError("quantile of empty sequence")
    if not 0.0 <= q <= 1.0:
        raise ValueError("q must be within [0, 1]")
    pos = (len(sorted_values) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return float(sorted_values[lo])
    frac = pos - lo
    return float(sorted_values[lo] + (sorted_values[hi] - sorted_values[lo]) * frac)


@dataclass(frozen=True)
class Interval:
    low: float
    high: float
    confidence: float

    def excludes_zero(self) -> bool:
        return self.low > 0 or self.high < 0


def bootstrap_mean_ci(
    values: Sequence[float], *, confidence: float = 0.95, n_resamples: int = 1000, seed: int = 0
) -> Interval | None:
    """Percentile bootstrap CI for the mean. None if there are no values."""
    n = len(values)
    if n == 0:
        return None
    if not 0 < confidence < 1:
        raise ValueError("confidence must be in (0, 1)")
    if n_resamples < 1:
        raise ValueError("n_resamples must be >= 1")
    if all(v == values[0] for v in values):  # includes n == 1: no variation to resample
        v = float(values[0])
        return Interval(v, v, confidence)
    rng = random.Random(seed)  # noqa: S311 - statistical resampling, not cryptography
    means = sorted(math.fsum(rng.choices(values, k=n)) / n for _ in range(n_resamples))
    alpha = (1 - confidence) / 2
    return Interval(quantile(means, alpha), quantile(means, 1 - alpha), confidence)


@dataclass(frozen=True)
class PairedDifference:
    n: int
    mean_diff: float
    interval: Interval | None


def paired_difference(
    baseline: Sequence[float],
    current: Sequence[float],
    *,
    confidence: float = 0.95,
    n_resamples: int = 1000,
    seed: int = 0,
) -> PairedDifference | None:
    """Mean and bootstrap CI of (current - baseline) over aligned pairs."""
    if len(baseline) != len(current):
        raise ValueError("paired sequences must have equal length")
    if not baseline:
        return None
    diffs = [c - b for b, c in zip(baseline, current, strict=True)]
    m = math.fsum(diffs) / len(diffs)
    ci = bootstrap_mean_ci(diffs, confidence=confidence, n_resamples=n_resamples, seed=seed)
    return PairedDifference(n=len(diffs), mean_diff=m, interval=ci)
