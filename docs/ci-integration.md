# CI integration

## GitHub Actions (composite action)

```yaml
- uses: [osel-org]/osel/integrations/github-action@v0.1.0
  with:
    config: evals/config.yaml
    baseline: evals/baseline.json
    max-drop: "exact_match=0.01"
    mode: fail             # fail | warn
    missing-baseline: warn # fail | warn
```

The action writes the check output to the job summary and sets the `exit-code` output.

## Any CI system

```bash
osel eval run evals/config.yaml --output current.json
osel check --baseline evals/baseline.json --current current.json --max-drop exact_match=0.01
```

| Exit code | Meaning | Typical CI handling |
|---|---|---|
| 0 | No regression beyond tolerance | pass |
| 1 | Regression detected | fail (or warn) |
| 2 | Invalid input: missing or bad file, incompatible runs | fail; fix the setup |
| 3 | Internal error in osel | fail; please report the bug |

## Pull requests from forks

A PR can change the evaluation config or your system code, and osel will execute it. Run the evaluation workflow with the `pull_request` trigger (no secrets, read-only token), **never** `pull_request_target`, and don't give the job any secrets it doesn't need.

## Failed examples

`check` also fails when more examples fail to produce a score than in the baseline (`max-new-errors`, default 0), because means only cover scored examples.

## Managing the baseline

- Commit `baseline.json` and refresh it **deliberately** in a PR that explains why.
- If the dataset or a metric version changes, `check` exits 2. Regenerate the baseline in the same PR.
- `--missing-baseline warn` is useful for the first PR that introduces evaluation.
