# OSEL Reproducibility Program

**Initial program:** publish a small set of carefully specified experiments that an independent person can rerun.
Governed by the [research integrity](../policies/research-integrity.md) (draft) and [benchmark integrity](../policies/benchmark-integrity.md) policies.

## Steps for each study

1. **Narrow question** connected to the validated product problem (after gate G1). Example: *"How often does a 1-point accuracy change on a 200-example eval set fall within resampling noise?"*
2. **Protocol before the main run:** use the [research protocol template](templates/research-protocol.md). Commit it with a date before running.
3. **Record everything:** dataset provenance (source, license, `osel` dataset identity), software versions (the run record captures these), configuration, hardware, seeds, exclusions.
4. **Fair baselines and comparisons:** same data, metrics and budget; report all configurations that were run.
5. **Publish** code, configs and permitted data, or data references where redistribution isn't allowed, in `benchmarks/<study>/`.
6. **Report negative and inconclusive results.**
7. **Independent reviewer:** someone outside the work follows the README on a clean machine and records the outcome.
8. **Label results:** *exploratory*, *confirmed* (protocol followed), or *independently reproduced*.

## Output

A `benchmarks/<study>/` folder with `PROTOCOL.md`, `README.md` (rerun instructions), configs, run records and `RESULTS.md` (including limitations and deviations from protocol).
