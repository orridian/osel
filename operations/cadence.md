# Operating cadence

## Weekly (≈ 30 min of ops; rest is engineering) → output: weekly plan + brief status note

- [ ] Triage new issues: label, reply, close duplicates
- [ ] Review open PRs (oldest first)
- [ ] Inspect CI on `main`; fix or file red builds
- [ ] Contact at least one user or tester
- [ ] Update the project board
- [ ] Protect engineering time in the [time budget](time-budget.md)
- [ ] Write the [weekly plan](templates/weekly-plan.md)

## Monthly → output: [monthly report](templates/monthly-report.md)

- [ ] Release, or write down why there was no release
- [ ] Publish a short public update (blog or discussion)
- [ ] Review adoption evidence in the metric ledger
- [ ] Review contributors and thank them
- [ ] Check security alerts, Dependabot and stale dependencies
- [ ] Refresh docs that changed
- [ ] Review the risk register

## Quarterly → output: roadmap update + [impact report](templates/quarterly-impact-report.md)

- [ ] Reassess strategy against the decision gates
- [ ] Review governance; check maintainer capacity
- [ ] Audit access ([access-review.md](access-review.md))
- [ ] Review metrics and risks; publish the impact report with corrections
- [ ] Records retention: delete what has expired ([policy](../policies/records-retention.md))

## Per release → output: tagged release and release notes

[release-checklist.md](release-checklist.md)

## Per incident → output: incident record (sensitive details restricted)

Contain → investigate → communicate appropriately → fix → test → [post-incident review](templates/post-incident-review.md). See the [incident response policy](../policies/incident-response.md).
