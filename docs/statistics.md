# Comparing runs and statistics

## What osel computes

| Quantity | Method |
|---|---|
| Point estimate | Mean of per-example scores |
| Spread | Sample standard deviation (n − 1) |
| Run CI | Percentile bootstrap of the mean (default 1000 resamples, 95%, seeded) |
| Comparison CI | Paired percentile bootstrap of the mean per-example difference (current − baseline), over examples scored in both runs |

Quantiles use linear interpolation, the same definition as `statistics.quantiles(method="inclusive")` and NumPy's default. The test suite checks the implementation against the standard library (`tests/test_stats.py`).

## Assumptions and limitations

- **Independence.** Examples are treated as independent draws from the population you care about. Duplicated or near-duplicated examples make intervals too narrow.
- **Sample size.** Percentile bootstrap intervals are unreliable for small samples. osel warns below 30 scored examples.
- **Skewed or bounded scores.** For binary metrics with means near 0 or 1, intervals can be too narrow.
- **One comparison at a time.** No correction is made for comparing many metrics or many runs. If you test 20 metrics, about one may look "different" by chance.
- **No p-values, no "significant" label.** osel reports whether the paired CI excludes zero, at the stated confidence. It does not decide what matters for your use case.
- **Seeds.** Intervals are reproducible for a given seed, but a different seed gives slightly different bounds. Treat the bounds as approximate.

## Compatibility rules

`osel compare` refuses (exit 2) when:

- the dataset identity differs (the data changed);
- a shared metric's `version` or direction differs;
- the runs share no metrics.

`--allow-incompatible` shows aggregate deltas only, with **no** paired statistics, and labels the output `INCOMPATIBLE`. Never publish such comparisons as like-for-like.

## Regression checks

`osel check` flags a metric as a regression when **any** of these is true:

1. it is missing from the current run;
2. the current run could score **no** examples for it (the baseline could);
3. **more examples failed** than in the baseline, through prediction errors, missing predictions or scoring errors. `--max-new-errors N` allows N extra failures (default 0);
4. its mean degraded by more than the allowed tolerance:
    - `--tolerance X` sets the default allowed absolute degradation;
    - `--max-drop metric=X` sets a per-metric limit (repeatable);
    - `--require-ci` additionally requires the paired CI to exclude zero, which ignores noise-level changes.

Rule 3 matters because means are computed over **scored examples only**. Without it, a system that started crashing on its hardest examples could show an *improved* mean.

## What the intervals mean, and what they don't

- A 95% paired CI of `[-0.12, -0.03]` means: if these examples are representative and independent, resampling them suggests the true mean difference is likely in that range.
- It does **not** mean there is a 95% chance the change is real, and it says nothing about examples unlike those in your dataset.
- It does **not** account for randomness inside your system (e.g. sampling temperature). For that, run the system several times and compare the runs.
- A CI that includes 0 does **not** prove "no change". It means this data cannot tell.
