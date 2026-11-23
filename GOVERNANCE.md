# Governance

OSEL is founder-led and contributor-powered. This document says who decides what, and how decisions can be challenged.

## Project scope

In scope: Product A (`osel` evaluation toolkit), its documentation, website, and the community/research programs described in
[programs/](programs/). Products B and C are out of scope until the [expansion gate](STRATEGY.md#expansion-gate) is met.

## Decision rights

| Decision | Who decides | How |
|---|---|---|
| Day-to-day technical changes | Any maintainer, via PR review | Lazy consensus on the PR |
| Public API / CLI changes, deprecations | Maintainers | PR + entry in the decision log; Founding Technical Lead breaks ties |
| Releases | Maintainer running the release | [Release checklist](operations/release-checklist.md) |
| Roadmap, new programs, new products | Founding Technical Lead, after a public proposal | Proposal issue open ≥ 7 days; expansion gate for new products |
| Code of Conduct enforcement | Conduct contacts (see CODE_OF_CONDUCT.md) | Private process; anyone involved in a report recuses |
| Security response | Security contact(s) | [Security policy](SECURITY.md) |
| Legal, financial, contractual, registration matters | Founder **with parent/guardian or trusted adult**; qualified professional where needed | Never decided informally |
| Changes to this document | Founding Technical Lead, after a public proposal | PR open ≥ 14 days for comment |

## Role map

One person may hold several roles at first. Only filled roles are listed as filled; unfilled roles are not presented as a team.

| Role | Responsibilities | When appointed | Current holder |
|---|---|---|---|
| Founder / Founding Technical Lead | Mission, product direction, technical standards, early releases, community formation | At founding | [Founder name] |
| Project maintainer | Technical quality, reviews, releases, triage, component roadmap | When a contributor shows sustained capability | [Founder name] (only maintainer) |
| Documentation lead | Docs quality, tutorials, release docs, onboarding | When docs work becomes recurring | _unfilled_ |
| Community organizer | Events, discussions, welcome, moderation coordination | When community activity justifies it | _unfilled_ |
| Security contact | Private vulnerability intake and coordinated response | Before public release | [Founder name] + trusted adult |
| Research lead | Protocol quality, reproducibility, research collaborations | When real research work and a qualified collaborator exist | _unfilled_ |

## Becoming a maintainer

See [programs/contributor-programs.md](programs/contributor-programs.md#maintainer-development-program). Permissions are granted only as needed and reviewed quarterly ([access review](operations/access-review.md)).

## Conflict resolution

1. Discuss on the issue/PR, focusing on evidence and user impact.
2. If unresolved, a maintainer summarizes the options in the decision log.
3. The Founding Technical Lead decides and records the reasoning.
4. Anyone may ask for reconsideration with new evidence by opening a proposal issue.

## Succession and backup

Critical components and their backup owners are recorded in [operations/ownership.md](operations/ownership.md).
Until a second maintainer exists, a trusted adult holds emergency recovery access to the repository and domain accounts.
