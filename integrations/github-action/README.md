# osel GitHub Action

Runs an evaluation on every pull request and compares it with a committed baseline run.

```yaml
# .github/workflows/eval.yml in YOUR repository
name: eval
on: [pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - uses: orridian/osel/integrations/github-action@v0.1.0a1
        with:
          config: evals/config.yaml
          baseline: evals/baseline.json
          max-drop: "exact_match=0.01"
          mode: fail            # or: warn
          missing-baseline: warn
```

## Behaviour

| Situation | Result |
|---|---|
| No metric degraded beyond its limit | ✅ job passes, summary posted |
| Regression, `mode: fail` | ❌ job fails (exit 1) |
| Regression, `mode: warn` | ⚠️ warning annotation, job passes |
| Baseline file missing | `missing-baseline: fail` → exit 2; `warn` → passes with a warning |
| Dataset or metric version changed | exit 2 (runs are incompatible). Regenerate and commit a new baseline on purpose. |

Create or refresh the baseline deliberately:

```bash
osel eval run evals/config.yaml --output evals/baseline.json
```

The integration test lives in `.github/workflows/action-integration.yml`. It uses this repository's `examples/quickstart` as the sample project.
