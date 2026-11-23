# Public alpha launch checklist

Status as of 22 Nov 2026. ✅ done and verified · 🔧 built, waiting on a person's action · 👤 can only be done by a person (with a parent/guardian where noted).
Automated checks: run `python scripts/launch_audit.py --report operations/launch-audit-report.md`.

## 1. Technical release

| # | Item | Status | Evidence / what's left |
|---|---|---|---|
| 1 | Review the source code and security-sensitive paths | ✅ | Launch audit found and fixed 5 bugs (see CHANGELOG "Fixed"): failing examples passed `check`; over-eager secret redaction; crash on non-JSON predictions; shell-injection-prone action inputs; `run show latest` picking the wrong run within the same second |
| 2 | Verify all tests and CI checks from a clean checkout | 🔧 | 89 tests (8 consecutive clean runs), lint and strict types pass locally; clean wheel install passes. CI runs on the first push |
| 3 | Test installation on Linux, macOS and Windows | 🔧 | Windows verified locally; CI matrix covers all 3 OSes × Python 3.10–3.13. Confirm the first CI run is green |
| 4 | Verify statistics and comparison behavior independently | ✅ / 👤 | Tests against Python's `statistics` module plus edge cases (tiny n, identical runs, large differences, missing values, seeds, lower-is-better, incompatible data). An independent human reviewer is still recommended |
| 5 | Verify the GitHub Action in a real test repository | 🔧 | `action-integration.yml` tests pass, warn, fail and missing-baseline. A separate real repo needs the org first |
| 6 | Test the complete quick start as a new user | 🔧 / 👤 | Automated in the audit (7 steps, exit codes match the docs). Still needs someone other than the founder |

## 2. Organization and GitHub

| # | Item | Status | Evidence / what's left |
|---|---|---|---|
| 7 | Resolve founder, organization, domain and email placeholders | 🔧 👤 | Decide the values, then `python scripts/set_identity.py ... --apply` replaces all of them |
| 8 | Review the license with adult/expert support | 👤 | Marked **Proposed** in `policies/README.md` until approved |
| 9 | Create the GitHub organization and public repository | 👤 | With adult support; 2FA required; trusted adult as backup owner |
| 10 | Commit and push the complete repository | 🔧 | A local commit is ready. Push after #7 and #9 |
| 11 | Configure branch protection and workflow permissions | 🔧 | Workflows already use read-only tokens, SHA-pinned actions and no `pull_request_target`. Apply the ruleset in `repo-settings.md` |
| 12 | Enable private vulnerability reporting and Dependabot | 👤 | Settings toggles (`repo-settings.md`); `dependabot.yml` is ready |

## 3. Public infrastructure

| # | Item | Status | Evidence / what's left |
|---|---|---|---|
| 13 | Deploy the main website | 🔧 | `pages.yml` deploys free to GitHub Pages; enable Pages → Source: GitHub Actions. A custom domain is optional (adult help) |
| 14 | Deploy the MkDocs documentation | 🔧 | Same workflow publishes the docs at `/docs/` |
| 15 | Verify every public link and contact channel | ✅ / 👤 | 603 internal links, 0 broken, at both root and sub-path. Role email addresses need setting up and testing |
| 16 | Publish the privacy and security information | 🔧 👤 | Pages exist; the privacy policy needs adult review first |
| 17 | Publish the roadmap and alpha limitations | ✅ | `/roadmap` and `docs/known-limitations.md` |
| 18 | Prepare release notes and demo | ✅ / 👤 | `RELEASE_NOTES_v0.1.0a1.md`, three verified demos, video script. Recording the video is 👤 |

## 4. Community and distribution

| # | Item | Status | Evidence / what's left |
|---|---|---|---|
| 19 | Open the alpha testing program | 🔧 | `programs/early-access.md` + "Alpha feedback" issue form |
| 20 | Prepare a list of 30 prospective testers | 👤 | Private tracker template: `operations/templates/early-access-tracker.md` |
| 21 | Personally invite the first 10 testers | 👤 | Personalized outreach message in `interview-kit.md` |
| 22 | Record installation and workflow feedback | 🔧 | Feedback form asks for time-to-first-run and where they got stuck |
| 23 | Resolve the first high-priority usability issues | 👤 | After the first batch of testers |
| 24 | Publish the first technical demonstration | 🔧 | `examples/demos/`; draft posts in `website/drafts/` |
| 25 | Invite the first external contribution | 🔧 | 5 ready-to-file issues in `programs/good-first-issues.md` |

## Recommended order for the human steps

1. With a parent/guardian: pick the public name/handle, org name and domain (or skip the domain and use GitHub Pages); review the license and privacy policy.
2. `python scripts/set_identity.py --founder-name ... --org ... --domain ... --founder-handle ... --apply`
3. `python scripts/launch_audit.py`. It should report no FAIL items.
4. Create the org, push, apply `repo-settings.md`, enable Pages, and watch CI go green.
5. Set `src/osel/__init__.py` (and CITATION.cff and website `site.ts`) to `0.1.0a1`, tag `v0.1.0a1`, and publish the draft GitHub release. Keep PyPI off for now.
6. Ask one person to follow the quick start, then invite testers in batches of 5–10.
