# OSEL — Open Source Engineering Lab

**`osel`: define an evaluation, run it, record exactly what produced the result, compare it with a baseline, and fail CI on regressions. Local-first, file-based, no account needed.**

> **Status: alpha (`0.1.0.dev0`).** Interfaces may change before 1.0. Not yet published to PyPI.

## What it does

- **Validates datasets** (JSON/JSONL) with row-level errors, and computes a content-derived **dataset identity**.
- **Runs evaluations** from a predictions file or directly against a Python function.
- **Records runs** as inspectable JSON: dataset identity, config (secrets redacted), metric versions, environment, git commit, per-example scores.
- **Compares runs honestly.** It refuses incompatible comparisons (changed dataset or metric version) and reports paired bootstrap confidence intervals with stated assumptions.
- **Checks for regressions in CI**, with explicit thresholds and stable exit codes.

> ⚠️ **Security:** an osel config can name Python code to run (`system:` and custom metrics), and osel runs it with **no sandbox**. Only run configs you trust. See [docs/config.md](docs/config.md).

## Quick start

Requires Python 3.10+. Until the first release, install from source:

```bash
git clone https://github.com/[osel-org]/osel.git && cd osel
pip install .
cd examples/quickstart
osel dataset validate data.jsonl
osel eval run config.yaml --output baseline.json
osel eval run config_v2.yaml --output current.json
osel compare baseline.json current.json
osel check --baseline baseline.json --current current.json   # exits 1: v2 regressed
```

Expected results are documented in [examples/quickstart/README.md](examples/quickstart/README.md) and verified in CI.

## Commands

| Command | Purpose |
|---|---|
| `osel dataset validate FILE` | Validate data and schema |
| `osel eval run CONFIG` | Execute a configured evaluation and store the run |
| `osel run show RUN_ID` / `osel run list` | Inspect stored runs (`.osel/runs/`) |
| `osel compare BASELINE CURRENT` | Compare compatible runs |
| `osel report RUN_ID --format json` | Export a report |
| `osel check --baseline B --current C` | CI-friendly regression check |

Exit codes: `0` ok · `1` regression detected · `2` invalid input · `3` internal error.

## Supported environments

Python 3.10–3.13 on Linux, macOS and Windows (tested in CI). The only runtime dependency is PyYAML.

## Documentation

[docs/](docs/) (built with MkDocs: `pip install -e ".[docs]" && mkdocs serve`).

## Project

- About OSEL: [FOUNDING.md](FOUNDING.md) · [MISSION.md](MISSION.md) · [VISION.md](VISION.md) · [ROADMAP.md](ROADMAP.md) · [GOVERNANCE.md](GOVERNANCE.md)
- Contribute: [CONTRIBUTING.md](CONTRIBUTING.md) · [Code of Conduct](CODE_OF_CONDUCT.md)
- Security: [SECURITY.md](SECURITY.md). Report vulnerabilities privately, never in public issues.
- Policies: [policies/](policies/)
- Cite: [CITATION.cff](CITATION.cff)

## Privacy

`osel` has **no telemetry** and makes no network requests. See [policies/telemetry.md](policies/telemetry.md).

## License

MIT. See [LICENSE](LICENSE).
