# GitHub organization and repository settings

Apply after creating the organization (with a parent/guardian if the provider's terms require an adult account holder).

## Organization

- [ ] Organization name checked for conflicts (decision log)
- [ ] Two-factor authentication required for all members
- [ ] Base member permission: **Read**
- [ ] Trusted adult added as a second owner, for emergency recovery only
- [ ] Discussions enabled, with categories: Q&A, Ideas, Alpha testers, Show and tell

## Repository `osel`

- [ ] Replace placeholders: `[osel-org]`, `[osel-domain]`, `@[founder-handle]`, `[Founder name]`. Search: `grep -rn "\[osel-\|\[Founder\|\[founder-" .`
- [ ] **Private vulnerability reporting:** on (Settings → Security)
- [ ] **Secret scanning + push protection:** on
- [ ] **Dependabot alerts and security updates:** on
- [ ] Labels: `bug`, `enhancement`, `documentation`, `good first issue`, `help wanted`, `needs-triage`, `P0`, `P1`, `P2`, `security`, `license`, `release`, `benchmark`, `accessibility`, `privacy`, `regression`

## Branch protection (ruleset on `main`)

- [ ] Require a pull request before merging
- [ ] Require 1 approval; dismiss stale approvals on new commits
- [ ] Require review from Code Owners (CODEOWNERS covers security-sensitive paths)
- [ ] Require status checks: `lint-types`, `test (...)`, `build-and-clean-install`, `docs`, `licenses`
- [ ] Block force pushes and deletion
- [ ] Do not allow bypassing. Document any exception in the decision log instead of quietly bypassing

> While the founder is the only maintainer, they can't get an independent approval. Until a second maintainer exists, the ruleset requires CI only, and each self-merged PR states "self-merged: sole maintainer". This exception is recorded as a decision-log entry.

## Actions and Pages

- [ ] Settings → Actions → General → Workflow permissions: **Read repository contents** (the default token is read-only; jobs that need more request it explicitly)
- [ ] Settings → Actions → General → "Require approval for all outside collaborators" for fork PR workflows
- [ ] Settings → Pages → Source: **GitHub Actions** (deploys website + docs via `pages.yml`)
- [ ] Add the label `alpha-feedback`
- [ ] Discussions categories: Q&A, Ideas, Alpha testers, Show and tell

## Releases

- [ ] **Leave the repository variable `PUBLISH_TO_PYPI` unset** until the license, package metadata and Trusted Publisher setup have been reviewed. Until then, releases go to GitHub only.

- [ ] Create the `pypi` environment with required reviewer = maintainer
- [ ] Configure the PyPI Trusted Publisher (repo `osel`, workflow `release.yml`, environment `pypi`)
- [ ] Tag protection: `v*` tags can only be created by maintainers

Some of this can be scripted with `gh`, for example:

```bash
gh repo create [osel-org]/osel --public --source . --push
gh api -X PUT repos/[osel-org]/osel/private-vulnerability-reporting
```
