# Security Policy

| Owner | Review date | Reporting channel |
|---|---|---|
| Security contact (Founder, with trusted adult support) | Every release, and at least every 6 months | GitHub **private vulnerability reporting** on this repository, or `security@[osel-domain]` |

## Supported versions

| Version | Supported |
|---|---|
| Latest `0.x` minor release | ✅ security fixes |
| Older `0.x` releases | ❌ — please upgrade |

Before 1.0, only the latest minor release receives fixes.

## Reporting a vulnerability

**Do not open a public issue for security problems.** Report privately using GitHub's "Report a vulnerability" button (Security tab), or by email to `security@[osel-domain]`. Please include:

- the affected version;
- a description and the impact;
- reproduction steps;
- any suggested fix.

Do not include real credentials or other people's personal data.

## What happens next

1. An authorized maintainer acknowledges receipt (best-effort target: **7 days**; OSEL is volunteer-run, so if you get no reply in 14 days, please follow up through the same channel) and records a private tracking ID (`OSEL-SEC-YYYY-NNN`).
2. The maintainer assesses severity, affected versions, exploitability and whether immediate containment is needed.
3. A fix and tests are prepared privately when public disclosure would expose users.
4. A disclosure timeline is coordinated with the reporter, normally ≤ 90 days.
5. An advisory is published with fixed versions and mitigations. Reporters are credited **only with their permission**.
6. Regression tests are added and supported-version guidance is updated.
7. A short post-incident review is held. It never blames the reporter.

Process detail: [policies/vulnerability-disclosure.md](policies/vulnerability-disclosure.md).

## Scope notes

`osel` runs locally and executes user-supplied Python callables named in evaluation configs. **Running an untrusted config is equivalent to running untrusted code.** This is documented behavior, not a vulnerability.
