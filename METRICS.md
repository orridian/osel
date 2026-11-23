# Metrics

Every reported number must be reproducible by a second person from these definitions and the private
[metric ledger](operations/metric-ledger.md). Collect no more personal data than a metric strictly needs.

| Metric | Count only when | Collection method | Exclusions |
|---|---|---|---|
| Installation | A distinct, reasonably deduplicated installation event is recorded | Package-index download stats. **Limits:** includes CI and mirrors; this is not a user count | Identifiable bot/mirror traffic |
| Monthly active user | A distinct person performs a meaningful product action (e.g. runs an evaluation) during the month | Opt-in self-report or alpha-tester check-ins only (no telemetry exists) | Founder, maintainers, CI bots |
| Returning user | The same pseudonymous/consented identifier is active in more than one month | Alpha-tester log | As above |
| External contributor | A non-founder makes a substantive accepted contribution | Merged PRs; accepted docs/design/triage work | Typo-only bot PRs, spam |
| Regular contributor | Substantive contributions in ≥ 3 distinct months within a 6-month window | Contribution history | — |
| Verified organization | An independently identifiable organization confirms actual use or evaluation in writing | Written confirmation stored in ledger | Unconfirmed mentions, stars |
| Research collaboration | Documented joint research/technical work exists | Written scope + outputs | Correspondence only |
| External maintainer | A non-founder holds real ongoing maintenance permissions and responsibilities | Access list + GOVERNANCE.md | — |
| Workshop | An event actually took place | Event record; registered / attended / completed reported separately | Cancelled events |
| Learner | Completed a hands-on exercise or structured learning activity | Exercise completion evidence | Registrations, viewers |
| Case study | A documented outcome has supporting evidence and permission to publish | Approved write-up | — |

## Reporting cadence

- **Monthly:** internal project report ([template](operations/templates/monthly-report.md)).
- **Quarterly:** public impact report ([template](operations/templates/quarterly-impact-report.md)) with definitions, period, methods, limitations and corrections.

## Rules

- Stars, downloads and page views are never presented as users, adoption or partnerships.
- When an earlier number is found to be wrong, the correction is published in the next report.
