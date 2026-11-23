# Component ownership

A component is complete only when it has an owner, a documented purpose, a working implementation, a test or review method, and a maintenance plan.

| Component | Purpose | Implementation | Test / review method | Maintenance plan | Owner | Backup |
|---|---|---|---|---|---|---|
| `osel` core (schema, dataset, metrics, runner) | Run evaluations | `src/osel/` | pytest (unit + integration), mypy strict, ruff | Bugs triaged weekly; deps via Dependabot | Founder | Trusted adult (repo access only) |
| Run record + redaction | Durable, safe results | `src/osel/record.py` | Round-trip and no-secrets tests; 2nd review for changes | Schema changes follow the release policy | Founder | — |
| Statistics | Honest uncertainty | `src/osel/stats.py` | Tests vs `statistics` module; independent review wanted | Methods documented in docs/statistics.md | Founder | — |
| CLI + exit codes | User and CI interface | `src/osel/cli.py` | CLI tests incl. every exit code | Exit codes stable from 0.1.0 | Founder | — |
| GitHub Action | CI integration | `integrations/github-action/` | `action-integration.yml` workflow | Tagged with releases | Founder | — |
| Docs | Learn and use osel | `docs/`, `mkdocs.yml` | `mkdocs build --strict` in CI; examples tested | Updated in the same PR as behavior changes | Founder → docs lead | — |
| Website | Public presence | `website/` | Build + link check in CI; launch checklist | Updated on every release/policy/status change | Founder | — |
| Policies | Rules that reflect practice | `policies/` | Index review dates | Reviewed per index schedule | Founder | Trusted adult |
| Security intake | Private vulnerability handling | SECURITY.md, GitHub private reporting | Annual dry run | Contacts verified quarterly | Founder | Trusted adult |
| Community programs | Contributor growth | `programs/` | Feedback from contributors | Reviewed quarterly | Founder → community organizer | — |

**Single-owner components:** all of them, for now. This is the "founder bottleneck" risk. Recruiting a second maintainer is on the roadmap.
