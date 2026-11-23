# Incident response policy

**Owner:** Security contact · **Review:** every 6 months · **Channel:** `security@[osel-domain]` (external), private maintainer channel (internal) · **Enforcement:** every SEV1/SEV2 has a post-incident review.

## Scope

OSEL runs no production service, so incidents are things like: a leaked secret in the repo or CI, a compromised maintainer account, a malicious release or dependency, a vulnerability being exploited, or website defacement.

## Severity

| Level | Example | Notify |
|---|---|---|
| SEV1 | Malicious/compromised release published; maintainer account takeover | All maintainers + trusted adult immediately; users via advisory |
| SEV2 | Secret committed to a public repo; exploitable vulnerability with a public PoC | All maintainers within 24h |
| SEV3 | Vulnerable dependency without known exploitation; website defect | Owner of the component |

## Response steps

1. **Contain.** Revoke and rotate credentials; yank the release; disable the compromised workflow or account.
2. **Investigate.** Build a timeline and scope; preserve logs.
3. **Communicate.** Publish an advisory or status note for affected users, without exposing sensitive details.
4. **Fix and test.** Patch, add a regression test, and harden the process.
5. **Review.** Hold a blameless post-incident review within 14 days ([template](../operations/templates/post-incident-review.md)).

Incident records are kept private, with sensitive details restricted. A public summary is published where users were affected.
