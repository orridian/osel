# Quick start

!!! danger "Configs can run code — only run configs you trust"
    An osel config can name a Python function (`system:`) or a custom metric, and osel **imports and runs that code with your permissions**. osel has **no sandbox**. Treat running someone else's config like running their script. Don't run configs from strangers, and don't run untrusted configs in CI jobs that have access to secrets.

## Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   ·   macOS/Linux: source .venv/bin/activate
pip install "git+https://github.com/[osel-org]/osel.git"   # PyPI release pending
osel --version
```

## Run the example

```bash
git clone https://github.com/[osel-org]/osel.git
cd osel/examples/quickstart
osel dataset validate data.jsonl
```

```text
VALID: data.jsonl: 10 examples, identity sha256:d989320b...
```

Run the baseline (model v1) and the candidate (model v2):

```bash
osel eval run config.yaml --output baseline.json
osel eval run config_v2.yaml --output current.json
```

Each run prints a table: mean, confidence interval, number of examples scored, number of errors, and whether higher or lower is better. Each run is also saved under `.osel/runs/`.

Compare them:

```bash
osel compare baseline.json current.json
```

```text
  metric            baseline   current     delta             paired 95% CI  result
  exact_match         0.8000    0.6000   -0.2000         [-0.5000, 0.0000]  DEGRADED (CI includes 0)
  token_f1            0.8000    0.7333   -0.0667         [-0.1342, 0.0000]  DEGRADED (CI includes 0)
```

"CI includes 0" means that with only 10 examples, this drop can't be distinguished from noise at 95% confidence. Use more examples for real decisions.

Gate it like CI would:

```bash
osel check --baseline baseline.json --current current.json
echo $?    # 1 = regression detected
osel check --baseline baseline.json --current current.json --tolerance 0.25
echo $?    # 0 = within tolerance
```

## Use your own data

1. Write a JSONL dataset: `{"id": "...", "input": ..., "reference": ...}` per line ([schema](dataset-schema.md)).
2. Produce predictions as `{"id": "...", "output": ...}` per line, **or** point `system:` at a Python function ([config](config.md)).
3. `osel eval run your-config.yaml`.
