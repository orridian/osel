# Run record format (schema version 1)

```json
{
  "schema_version": "1",
  "run_id": "20261112T042444Z-113b33db",
  "created_at": "2026-11-12T04:24:44.857616Z",
  "name": "capitals-v1",
  "osel_version": "0.1.0.dev0",
  "config": { "...": "the config as written, secrets redacted" },
  "dataset": { "path": "data.jsonl", "identity": "sha256:…", "n_examples": 10, "schema_version": "1" },
  "metrics": { "exact_match": { "version": "1", "higher_is_better": true } },
  "environment": {
    "osel_version": "0.1.0.dev0", "python_version": "3.12.4", "python_implementation": "CPython",
    "platform": "Linux-6.8-x86_64", "machine": "x86_64", "byteorder": "little",
    "git": { "commit": "abc123…", "dirty": false }
  },
  "statistics": { "method": "percentile bootstrap of the mean", "confidence": 0.95, "bootstrap_samples": 1000, "seed": 0 },
  "aggregates": {
    "exact_match": { "n": 10, "n_errors": 0, "mean": 0.8, "std": 0.42, "min": 0.0, "max": 1.0,
                     "ci_low": 0.5, "ci_high": 1.0, "higher_is_better": true, "small_sample": true }
  },
  "examples": [
    { "id": "q01", "prediction": "Paris", "scores": { "exact_match": 1.0 }, "errors": [] },
    { "id": "q05", "scores": {}, "errors": [ { "stage": "predict", "type": "ValueError", "message": "…" } ] }
  ],
  "warnings": [ "…" ]
}
```

- `run_id` = UTC timestamp + a short hash of the config, dataset identity and timestamp.
- `environment.git` is `null` when the config folder is not in a git repository.
- **Never stored:** environment variables, tracebacks, or values under secret-looking keys.
- Readers reject unknown `schema_version`s. Future osel versions will read every schema version they have shipped (see the release policy).
