# Products B and C — gated outlines (NOT STARTED)

> Do not implement until the [expansion gate](../STRATEGY.md#expansion-gate) is met **and** recorded in the decision log. These outlines exist so the work is well specified if and when the gate opens.

## Gate checklist

- [ ] Several independent users have requested the capability (links)
- [ ] The use case is documented
- [ ] An owner other than the founder, or a credible recruiting plan
- [ ] Maintenance cost estimated
- [ ] Product A reliability will not be harmed (no open P0s; release cadence holding)
- [ ] A measurable success criterion is defined

## Product B — Developer Reliability Infrastructure

| Step | First module scope | Success criterion (draft) |
|---|---|---|
| 1 | Ingest structured test results from one supported runner (JUnit XML) | Parses real reports from 3 projects |
| 2 | Store run metadata and test identifiers (reusing the osel run-record ideas) | Round-trip tested |
| 3 | Compare results across runs (new failures, fixed tests, flaky candidates) | Matches hand-labelled examples |
| 4 | Group recurring failures using transparent, inspectable rules (message normalization; no opaque ML) | Users agree with ≥ 80% of groupings |
| 5 | Report performance only with a controlled benchmark methodology | Methodology reviewed |
| 6 | CI integration with an explicit warn/fail policy | Integration test in a sample repo |
| 7 | Measure time saved **and** failures missed before promoting any change-aware test selection | Both numbers published |

## Product C — Benchmark & Reproducibility Ecosystem

| Step | Scope |
|---|---|
| 1 | A versioned benchmark specification (YAML), building on the osel config and dataset identity |
| 2 | Record dataset identity, evaluation code version, config, hardware/software metadata and raw results |
| 3 | A runner that executes a benchmark from a clean environment |
| 4 | Published reproducibility instructions and limitations |
| 5 | Methodology review before accepting public result claims |
| 6 | Labels: self-submitted vs independently reproduced |
| 7 | No ranking of incomparable hardware, datasets or configurations. **No public leaderboard** without rigorous comparability rules (blueprint §16) |
