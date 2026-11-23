# Benchmark integrity policy

**Owner:** Maintainers · **Review:** before the first benchmark publication · **Channel:** issue labelled `benchmark` · **Enforcement:** non-conforming claims are not published, or are retracted with a visible correction.

1. **Comparable configurations.** Only compare runs with the same dataset identity, metric versions and evaluation settings. `osel compare` refuses incompatible runs by default; do not override this for published claims.
2. **Complete metadata.** Publish the hardware, OS, Python version, package versions, config, seeds and raw results with every claim.
3. **Repeated runs** where results vary. Report the number of repeats and the spread, not only the best run.
4. **No cherry-picking.** Report all configurations that were run for the claim, including unfavorable ones. Exclusions are stated with reasons.
5. **Verification labels:** *self-reported*, *maintainer-reproduced* or *independently reproduced*.
6. **No rankings of incomparable results** (different hardware, datasets or configurations) as if they were directly comparable.
7. **Methodology review** by someone other than the author before publication.
