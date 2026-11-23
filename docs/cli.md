# CLI reference

Global options: `--store DIR` (run store, default `.osel/runs`) · `--version` · `--help`.

| Command | Description | Key options |
|---|---|---|
| `osel dataset validate PATH` | Validate a dataset; prints identity | `--encoding`, `--json` |
| `osel eval run CONFIG` | Run an evaluation; saves it to the store | `--output/-o FILE`, `--name`, `--json` |
| `osel run show RUN` | Show a run summary | `--json` |
| `osel run list` | List stored run IDs (oldest first) | |
| `osel compare BASELINE CURRENT` | Compare two runs | `--allow-incompatible`, `--json` |
| `osel report RUN` | Export a report | `--format json\|text`, `--full`, `--output/-o` |
| `osel check --baseline B --current C` | Regression gate | `--tolerance`, `--max-drop M=X`, `--max-new-errors N`, `--require-ci`, `--missing-baseline fail\|warn`, `--json` |

`RUN`, `BASELINE` and `CURRENT` accept a file path, a full run ID, a unique run-ID prefix, or `latest`.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Success / check passed |
| 1 | Regression detected (`check` only) |
| 2 | Invalid input (dataset, config, run file, arguments, incompatible runs) |
| 3 | Internal error — a bug in osel. Set `OSEL_DEBUG=1` to print a traceback, remove any secrets, and report it |

Text output always spells statuses out (`VALID`, `DEGRADED`, `CHECK FAILED`) and never relies on colour.
