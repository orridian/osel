# Architecture

```text
              config.yaml
                   │
   data.jsonl ──► dataset.py ──► Dataset (examples + identity)
                   │
 predictions.jsonl │ or system callable
                   ▼
              runner.py ── metrics.py (built-in + custom)
                   │        stats.py  (bootstrap CIs)
                   ▼
              record.py ── RunRecord ──► .osel/runs/<id>.json  (+ --output file)
                   │
         compare.py (compatibility, paired stats, regressions)
                   │
              report.py (text / JSON)  ◄── cli.py (argparse, exit codes)
```

| Module | Responsibility |
|---|---|
| `schema.py` | Example schema v1 and record validation |
| `dataset.py` | JSON/JSONL loading, row errors, encoding, content identity |
| `metrics.py` | Metric protocol, built-ins, `module:attr` resolution, score validation |
| `config.py` | YAML/JSON config parsing and validation |
| `runner.py` | Predictions/system execution, safe per-example error capture, aggregation |
| `stats.py` | Mean, std, quantiles, bootstrap CI, paired differences |
| `record.py` | Run record schema, secret redaction, environment metadata, local store |
| `compare.py` | Compatibility checks, comparisons, regression detection |
| `report.py` | Terminal and JSON rendering |
| `cli.py` | Commands, argument parsing, exit codes |

## Decisions (see the decision log)

- **Local files only.** No database or server. SQLite will be considered only if structured querying becomes necessary.
- **argparse, not Typer.** Zero extra dependencies; help output is good enough.
- **Dataclasses, not Pydantic.** The schemas are small; this avoids a heavy dependency.
- **Single runtime dependency** (PyYAML).
- **Telemetry:** none.
