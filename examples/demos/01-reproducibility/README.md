# Demo 1 — Reproducibility

**Claim:** if the dataset, config, metric versions and environment are the same, osel reproduces the same result. If the dataset changed, osel refuses to compare instead of silently giving a misleading answer.

## Run it twice

```bash
cd examples/quickstart
osel eval run config.yaml --output run1.json
osel eval run config.yaml --output run2.json
osel compare run1.json run2.json
```

```text
  metric            baseline   current     delta             paired 95% CI  result
  exact_match         0.8000    0.8000   +0.0000          [0.0000, 0.0000]  UNCHANGED
  token_f1            0.8000    0.8000   +0.0000          [0.0000, 0.0000]  UNCHANGED
```

The two run files have different `run_id`s and timestamps, but the same `dataset.identity`, metric versions and `aggregates`. The confidence intervals match too, because the bootstrap is seeded (`seed: 0`).

## Change one word in the dataset

Edit `data.jsonl` and change the reference `"Oslo"` to `"Bergen"`, then run again:

```bash
osel eval run config.yaml --output run3.json
osel compare run1.json run3.json
```

```text
error: runs are not comparable
  - dataset changed: baseline sha256:d989320b… vs current sha256:b11f789f…
```

The exit code is `2` (invalid input). A one-word change produces a different dataset identity, so osel won't present the two numbers as like-for-like. (`--allow-incompatible` shows the raw numbers, clearly labelled, with no paired statistics.)

Undo your edit afterwards: `git checkout data.jsonl`.

## What this does not show

The demo uses a predictions file, so it is fully deterministic. If your system itself is random (e.g. an LLM with temperature > 0), each run's predictions differ. osel records them faithfully, but it can't make them identical.
