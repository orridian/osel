# OSEL Early Access Program (alpha testers)

**Purpose:** find out whether osel solves a real, recurring engineering problem for people outside OSEL.
**Status:** ready to open once the repository is public and the launch checklist's blockers are done.
**Owner:** Founder.

## Tester commitment (about 1 hour)

1. Install osel ([installation](../docs/installation.md)).
2. Complete one documented evaluation (the quick start, or their own data).
3. Compare two runs.
4. Try a regression check.
5. Report problems and confusing moments, through the **Alpha feedback** issue form or a short call.

## What OSEL provides

- A direct feedback channel and a reply to every report (target: 7 days).
- Acknowledgment of useful bug reports in release notes, **with permission**.
- An invitation to contribute improvements ([good first issues](good-first-issues.md)).
- Nothing else is promised: no payment, credentials, endorsements or jobs.

## Success criteria (first 30 days after launch)

| Measure | Target | Counted how ([METRICS.md](../METRICS.md)) |
|---|---|---|
| People personally invited | 30 | Outreach tracker |
| Successful independent installations | 10 | Tester reports `osel --version` works |
| Completed evaluation workflows (run + compare + check) | 5 | Tester confirms, or pastes output |
| Returning users (used it again in a later week) | 3 | Follow-up check-in |
| Concrete, actionable pieces of feedback | ≥ 3 | Issues filed |

Downloads, stars and page views are **not** success measures.

## Who to invite (outreach targets, not claims about existing users)

| Group | Target |
|---|---|
| Individual ML developers | 10 |
| LLM application developers | 5 |
| University researchers and students | 5 |
| Open-source contributors | 5 |
| Other Python developers with evaluation scripts | 5 |
| **Total** | **30** |

Find people who have **publicly** described evaluation or reproducibility problems: GitHub issues and discussions, community forums, blog posts. Personalize every invitation. **No mass messaging.** Use the interview kit's [outreach message](../operations/interview-kit.md) and add the alpha link. Keep the tracker private: [templates/early-access-tracker.md](../operations/templates/early-access-tracker.md).

## Process

1. Invite in batches of 5–10, so feedback can be acted on between batches.
2. Watch the first session live, if the tester agrees. Time-to-first-run is the most revealing number.
3. File every confusing moment as an issue, labelled `alpha-feedback`.
4. Fix the top usability issues before the next batch.
5. Check in one to two weeks later: "Did you use it again? Why or why not?"
6. Thank testers and tell them what changed because of their feedback.

## Safety and privacy

Collect only a public handle and a contact route. Never ask testers for their datasets, credentials or employer details. A parent or guardian should know about scheduled calls with adults.
