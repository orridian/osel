"""Statistical methods checked against independent reference calculations."""

from __future__ import annotations

import math
import random
import statistics

import pytest

from osel import stats


@pytest.mark.parametrize(
    "values",
    [[1.0, 2.0, 3.0, 4.0], [0.0, 1.0, 1.0, 0.0, 1.0], [2.5, -1.25, 7.0], [1e9, 1e9 + 1, 1e9 + 2]],
)
def test_mean_and_std_match_statistics_module(values: list[float]) -> None:
    assert math.isclose(stats.mean(values), statistics.fmean(values))  # type: ignore[arg-type]
    assert math.isclose(stats.sample_std(values), statistics.stdev(values))  # type: ignore[arg-type]


def test_degenerate_inputs() -> None:
    assert stats.mean([]) is None
    assert stats.sample_std([1.0]) is None
    assert stats.bootstrap_mean_ci([]) is None
    ci = stats.bootstrap_mean_ci([0.7])
    assert ci is not None and ci.low == ci.high == 0.7
    const = stats.bootstrap_mean_ci([0.5] * 50)
    assert const is not None and const.low == const.high == 0.5


def test_quantile_matches_statistics_inclusive() -> None:
    rng = random.Random(42)
    data = sorted(rng.uniform(-5, 5) for _ in range(37))
    ref = statistics.quantiles(data, n=100, method="inclusive")
    for k in (1, 5, 25, 50, 75, 95, 99):
        assert math.isclose(stats.quantile(data, k / 100), ref[k - 1], rel_tol=1e-12, abs_tol=1e-12)
    assert stats.quantile(data, 0) == data[0]
    assert stats.quantile(data, 1) == data[-1]


def test_bootstrap_is_seeded_and_sensible() -> None:
    rng = random.Random(1)
    values = [rng.gauss(0.6, 0.2) for _ in range(400)]
    a = stats.bootstrap_mean_ci(values, seed=7)
    b = stats.bootstrap_mean_ci(values, seed=7)
    assert a == b
    assert a is not None and a.low < statistics.fmean(values) < a.high
    # For a large sample the bootstrap CI is close to the normal-theory interval.
    se = statistics.stdev(values) / math.sqrt(len(values))
    assert math.isclose(a.high - a.low, 2 * 1.96 * se, rel_tol=0.15)


def test_ci_narrows_with_more_data() -> None:
    rng = random.Random(3)
    small = [float(rng.random() < 0.7) for _ in range(40)]
    large = [float(rng.random() < 0.7) for _ in range(1000)]
    s = stats.bootstrap_mean_ci(small)
    big = stats.bootstrap_mean_ci(large)
    assert s is not None and big is not None
    assert (big.high - big.low) < (s.high - s.low)


def test_paired_difference() -> None:
    base = [0.1 * i for i in range(50)]
    cur = [v + 0.2 for v in base]
    d = stats.paired_difference(base, cur)
    assert d is not None and d.n == 50 and math.isclose(d.mean_diff, 0.2)
    assert d.interval is not None and math.isclose(d.interval.low, 0.2)
    assert d.interval.excludes_zero()
    with pytest.raises(ValueError):
        stats.paired_difference([1.0], [1.0, 2.0])
    assert stats.paired_difference([], []) is None
