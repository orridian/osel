# Release checklist — vX.Y.Z

Copy into the release-tracking issue.

1. [ ] **Scope and freeze.** Candidate scope confirmed; no new features merged after freeze.
2. [ ] **Full checks.** CI green on the release commit: tests (all OS/Python versions), ruff, mypy, build, `mkdocs build --strict`, clean-install smoke test, action integration.
3. [ ] **Alerts.** Dependabot and security alerts reviewed; nothing critical open.
4. [ ] **Clean-environment examples.** Quick start run by hand in a fresh venv from the built wheel; output matches the docs.
5. [ ] **Changelog.** `CHANGELOG.md` moved from Unreleased to vX.Y.Z; breaking changes and migration notes called out.
6. [ ] **Version and compatibility.** `src/osel/__init__.py` version bumped; README/docs compatibility claims (Python, OS) are accurate; `CITATION.cff` version updated.
7. [ ] **Build and verify artifacts.** Push tag `vX.Y.Z` → `release.yml` builds, checksums and attests. Download, verify the SHA256SUMS and install the wheel once.
8. [ ] **Publish.** Edit the draft GitHub release using the changelog text; approve the PyPI environment; update the website status and roadmap; post the announcement.
9. [ ] **Monitor.** Watch issues for 7 days; prepare a patch if needed. Yank (never rewrite) a broken release.

Never rewrite a published release. A mistake is fixed with a new patch version.
