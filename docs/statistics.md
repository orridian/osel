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

### When an interval is not informative

A bootstrap interval has **zero width** when only one example is paired, or when every per-example difference is identical. A zero-width interval at a non-zero value would "exclude zero" without any evidence about noise, so osel handles it explicitly:

- **One paired example:** `ci_excludes_zero` is `null` and the comparison says why. `--require-ci` does not count it as evidence.
- **All differences identical and non-zero:** the evidence is that every example moved the same way. osel uses a two-sided sign test: the chance of that under "no real change" is `2 × 0.5ⁿ`. It counts as evidence only when that is below `1 − confidence`, i.e. **n ≥ 6 at 95%**. Below that, `ci_excludes_zero` is `null` with a note.
- **All differences exactly zero:** the runs agree on every example; the interval `[0, 0]` is reported as including zero.

The plain tolerance rule (without `--require-ci`) is unaffected: a degradation beyond tolerance still fails the check.

### Warnings shown with every comparison

`osel compare` and `osel check` print (and include in `--json` as `warnings`):

- **Small samples:** fewer than 30 paired examples for a metric. Percentile bootstrap intervals are unreliable there.
- **Uninformative intervals:** the cases above.
- **Several metrics:** when k ≥ 2 metrics have intervals, the chance that *at least one* excludes zero by noise alone is about `1 − confidence^k` if the metrics were independent (14% for three metrics at 95%), and up to `k × (1 − confidence)` otherwise. osel does not adjust the intervals. Pick one primary metric before looking at results, and treat the others as supporting evidence.

Rule 3 matters because means are computed over **scored examples only**. Without it, a system that started crashing on its hardest examples could show an *improved* mean.

## What the intervals mean, and what they don't

- A 95% paired CI of `[-0.12, -0.03]` means: if these examples are representative and independent, resampling them suggests the true mean difference is likely in that range.
- It does **not** mean there is a 95% chance the change is real, and it says nothing about examples unlike those in your dataset.
- It does **not** account for randomness inside your system (e.g. sampling temperature). For that, run the system several times and compare the runs.
- A CI that includes 0 does **not** prove "no change". It means this data cannot tell.
