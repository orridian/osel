# Quickstart example

Ten capital-city questions, with two sets of predictions. `v2` is a deliberate regression.

```bash
cd examples/quickstart
osel dataset validate data.jsonl
osel eval run config.yaml --output baseline.json
osel eval run config_v2.yaml --output current.json
osel compare baseline.json current.json
osel check --baseline baseline.json --current current.json
```

## Expected results (verified in CI by `tests/test_examples.py`)

| Run | exact_match | token_f1 |
|---|---|---|
| v1 (`config.yaml`) | 0.8000 | 0.8000 |
| v2 (`config_v2.yaml`) | 0.6000 | 0.7333 |

- `osel dataset validate` prints `VALID: data.jsonl: 10 examples, identity sha256:...` and exits 0.
- `osel compare` shows both metrics as `DEGRADED` and exits 0. Compare informs; it does not fail.
- `osel check` prints `CHECK FAILED: 2 regression(s)` and exits **1**.
- `osel check ... --tolerance 0.25` passes (exit 0), because both drops are ≤ 0.2.

Because n = 10, every run warns that the bootstrap intervals are unreliable. That warning is correct: use larger datasets for real decisions.
