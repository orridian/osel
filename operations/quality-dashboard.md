# Quality dashboard

Reviewed monthly and filled into the monthly report. No dashboard software is needed yet; each signal has a source.

| Signal | What to monitor | Source | Healthy | Value (month) |
|---|---|---|---|---|
| Correctness | Test failures, regression bugs, reproducibility failures | CI on `main`; `bug` + `regression` labels | CI green; 0 open P0 | |
| Installability | Clean-install success across supported environments | `build-and-clean-install` job; OS×Python matrix | All green | |
| Reliability | Crashes (exit 3 reports), failed workflows, open bug severity | `bug` issues by severity label | 0 open exit-3 bugs > 14 days | |
| Usability | Time to first successful evaluation; onboarding failures | Alpha-tester sessions (timed); `documentation` issues | < 10 min to first run | |
| Maintenance | Issue age, PR review delay, stale deps, single-owner components | GitHub insights; Dependabot; [ownership.md](ownership.md) | First response ≤ 14 days | |
| Adoption | Meaningful active and repeat use (privacy-safe) | Alpha-tester log in the metric ledger. **Not downloads** | Growing returning users | |
| Community | Substantive external contributors; maintainer retention | Merged PRs by non-founders | ≥ 1 new contributor/quarter | |

Useful queries:

```bash
gh issue list --label bug --state open
gh pr list --state open --json number,createdAt,title
gh run list --branch main --limit 10
```
