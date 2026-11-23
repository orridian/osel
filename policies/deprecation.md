# Deprecation policy — DRAFT (in force from 1.0)

**Owner:** Maintainers · **Questions:** issue labelled `deprecation` · **Enforcement:** removals that skip the notice period are reverted.

- **Notice period:** a public API, CLI command/flag or schema field is deprecated for at least **one minor release and 90 days** before removal.
- **Signals:** a `DeprecationWarning` (Python), a stderr warning (CLI), a changelog entry and a docs banner.
- **Migration guidance:** every deprecation names the replacement and includes a before/after example.
- **Security exception:** behavior that is itself a vulnerability may be removed immediately, with an advisory.
- **Support window:** after 1.0, the previous minor release gets security fixes for 6 months.
- **Pre-1.0:** best effort. Breaking changes are announced in the changelog under "Breaking changes".
