# Demo 2 — Regression detection

**Claim:** `osel check` turns a comparison into a CI decision with an explicit threshold. It also catches a system that started **failing** on examples, which an average alone would hide.

## A worse model (quickstart)

```bash
cd examples/quickstart
osel eval run config.yaml --output baseline.json
osel eval run config_v2.yaml --output current.json
osel check --baseline baseline.json --current current.json      # exit 1
osel check --baseline baseline.json --current current.json --tolerance 0.25   # exit 0
```

```text
CHECK FAILED: 2 regression(s)
  - exact_match: mean degraded by 0.2 (allowed 0)
  - token_f1: mean degraded by 0.0666667 (allowed 0)
```

The threshold is your decision. osel makes it explicit and version-controlled.

## A system that crashes on some inputs (function-eval)

`my_system.buggy_add` raises an error on negative numbers and is off by one for large ones:

```bash
cd examples/function-eval
osel eval run config.yaml --output good.json
osel eval run config_buggy.yaml --output buggy.json
osel check --baseline good.json --current buggy.json     # exit 1
```

```text
  abs_error: failed examples 0 -> 1 (scored 6 -> 5; means use scored examples only)

CHECK FAILED: 2 regression(s)
  - abs_error: 1 more example(s) failed than in baseline (0 -> 1; allowed 0)
  - within_tolerance: 1 more example(s) failed than in baseline (0 -> 1; allowed 0)
```

Why this matters: means are computed over the examples that could be scored. A system that starts crashing on its *hardest* inputs can raise its average. osel treats any increase in failed examples as a regression (`--max-new-errors N` relaxes this).

## In GitHub Actions

See `integrations/github-action/README.md`. The same rules run on every pull request.
