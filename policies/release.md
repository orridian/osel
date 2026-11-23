# Release policy

**Owner:** Maintainers · **Review:** before 1.0 · **Questions:** issue labelled `release` · **Enforcement:** a release missing any criterion is not published, or is yanked.

## Versioning

[Semantic Versioning](https://semver.org/):

- **major** for incompatible changes;
- **minor** for backward-compatible features;
- **patch** for backward-compatible fixes.

**Pre-1.0 exception:** in `0.x`, a minor bump (0.1 → 0.2) may contain breaking changes. These are always listed under "Breaking changes" in the changelog. Patch releases never break compatibility.

Run-record and dataset schemas carry their own `schema_version`. Readers must accept every schema version they have shipped.

## Release criteria

- All CI checks pass on the release commit: tests, lint, types, build, docs, and a clean-install smoke test.
- No open issues labelled `P0`.
- `CHANGELOG.md` updated, with behavior changes and breaking changes called out.
- Examples are verified in a clean environment.
- Process: [operations/release-checklist.md](../operations/release-checklist.md).

## Artifacts

Source distribution and wheel are built by CI from a tag, never from a laptop. Each GitHub release publishes SHA-256 checksums. Trusted publishing to PyPI with build provenance is used where practical.

## Never rewrite a release

Published tags and artifacts are never changed. A mistake is fixed with a new patch release.

## Rollback / yank

A release with a serious defect is **yanked** on the package index, with a reason. A fixed patch is released, and the GitHub release notes are updated to point to it.
