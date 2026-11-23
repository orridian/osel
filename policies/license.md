# Open-source license policy — PROPOSED (pending review)

**Owner:** Founder · **Review:** before v0.1.0, then yearly · **Questions:** open an issue labelled `license` · **Enforcement:** PRs that violate this policy are not merged; infringing code is removed.

## Chosen license

OSEL code is released under the **MIT License** ([LICENSE](../LICENSE)). MIT was chosen as a proposal because it is short, widely understood and compatible with most ecosystems. Apache-2.0 (explicit patent grant) is the main alternative considered. The choice is recorded in the [decision log](../operations/decision-log.md) and **must be confirmed after adult/expert review before the first public release.**

Documentation and website text are under the same license unless a file says otherwise.

## Contribution licensing

Contributions are accepted under the project license ("inbound = outbound"). No CLA is required. Contributors confirm they have the right to submit their work by ticking the PR template box.

## Third-party code and dependencies

- New runtime dependencies must use a license compatible with MIT (MIT, BSD, Apache-2.0, ISC, PSF). GPL/AGPL runtime dependencies are **not** accepted without a decision-log entry.
- Copied code must keep its copyright notice and license. Record the source in a comment and in `THIRD_PARTY_NOTICES.md` (created when first needed).
- CI runs a dependency-license check on every PR (`.github/workflows/ci.yml`, job `licenses`).

## Attribution

Required notices are preserved. Contributors are acknowledged in release notes with their consent.
