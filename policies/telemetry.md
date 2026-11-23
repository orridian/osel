# Telemetry policy

**Owner:** Founder · **Review:** before any telemetry-related PR · **Questions:** issue labelled `privacy` · **Enforcement:** telemetry code that does not meet this policy is not merged.

## Current state

**`osel` contains no telemetry.** It makes no network requests. Run records are written only to the local disk.

## Rules if telemetry is ever proposed

1. A public proposal issue must state the specific question the data would answer, and why it can't be answered by interviews or opt-in reports.
2. It must be **opt-in**, off by default, and clearly announced in the CLI and release notes.
3. **Fields:** the minimum needed. Never dataset contents, file paths, config values, environment variables, hostnames, usernames or IP-derived location.
4. **Aggregation:** only aggregate reporting. No individual-level dashboards.
5. **Retention:** raw events are deleted within 90 days.
6. **Documentation:** every field is listed in the docs, along with an `osel telemetry status` command.
7. **Review:** the privacy policy is updated and adult/expert review happens **before** release.
