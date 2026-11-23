# Evaluation config

YAML (`.yaml`/`.yml`) or JSON (`.json`). Relative paths are resolved from the config file's folder.

```yaml
name: capitals-v1                 # optional; defaults to the dataset file name
description: optional free text
dataset: data.jsonl               # required
encoding: utf-8                   # optional
predictions: predictions.jsonl    # set exactly one of predictions / system
# system: "my_package.module:predict"
python_path: ["."]                # optional; folders added to sys.path for system/custom metrics
metrics:                          # required, non-empty
  - exact_match
  - use: exact_match
    params: { normalize: true, name: exact_match_normalized }
  - use: "my_metrics:MyMetric"
    params: { threshold: 0.5 }
seed: 0                           # bootstrap seed (results are reproducible)
bootstrap_samples: 1000
confidence: 0.95
record_predictions: true          # store each prediction in the run record
```

Unknown keys are rejected.

!!! danger "Security: configs execute code, and there is no sandbox"
    `system:`, custom metrics (`module:Class`) and `python_path` make osel **import and execute Python code** with your user's permissions. Nothing is isolated or sandboxed. Only run configs and metric modules you trust. Never run configs submitted by strangers on your machine, or in a CI job that has secrets (a fork's PR can change the config).

!!! note "Secrets"
    Config values under keys that look secret (`api_key`, `token`, `password`, `secret`, `auth`, …) and values that look like common API keys are replaced with `[REDACTED]` in run records. Environment variables are never recorded. Even so, don't put secrets in configs; read them from the environment inside your system function.
