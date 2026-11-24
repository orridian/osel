# osel demo repository

A tiny project that gates its pull requests on an [osel](https://github.com/orridian/osel) evaluation.
Publish this folder as its **own** GitHub repository (e.g. `orridian/osel-demo`). It exercises the
GitHub Action exactly as an outside project would.

## Walkthrough (expected outputs verified in OSEL's test suite)

```bash
pip install "git+https://github.com/orridian/osel.git@v0.1.0a1"
cd evals
osel eval run config.yaml --output baseline.json     # abs_error 0.0, exact_match 1.0, 6 examples
git add baseline.json && git commit -m "Add evaluation baseline"
```

Now make the "change": in `evals/config.yaml` set `system: "calculator:add_v2"`, then:

```bash
osel eval run config.yaml --output current.json
osel check --baseline baseline.json --current current.json ; echo "exit $?"
```

```text
CHECK FAILED: 2 regression(s)
  - abs_error: 1 more example(s) failed than in baseline (0 -> 1; allowed 0)
  - exact_match: 1 more example(s) failed than in baseline (0 -> 1; allowed 0)
exit 1
```

Push that change as a pull request, and `.github/workflows/eval.yml` fails the same way in CI, with the report in the job summary.

## What it demonstrates

1. A baseline evaluation, committed next to the code
2. A changed function
3. A measurable regression, including an input that now **crashes**
4. osel comparing the two runs with paired statistics
5. A CI check that blocks the PR

The dataset has only 6 examples, so osel warns that the intervals are unreliable. That's intentional: the point is the workflow, not the statistics.
