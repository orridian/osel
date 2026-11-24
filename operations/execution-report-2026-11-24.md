# Execution report — 24 Nov 2026 (Master Execution Brief, Phase 1 + independent parts of Phases 2–5)

Status words, as used in the brief: **Planned · In progress · Implemented · Tested · Published · Independently verified.**
Nothing in this report is **Published** or **Independently verified** yet: nothing has left this computer.

## 1. Verified facts (re-run today; not taken from earlier inventories)

| Check | Result | Status |
|---|---|---|
| Test suite | 90 passed, 0 failed | Tested |
| Ruff lint / mypy --strict | clean / no issues in 13 source files | Tested |
| Build sdist + wheel; clean venv install; documented quick start with 7 commands and exact exit codes | pass; results match docs | Tested |
| MkDocs `--strict` | pass | Tested |
| Website + docs together, link check at `/` and at `/osel/` (GitHub Pages project path) | 29 pages, 602 internal links, 0 broken | Tested |
| Secrets, personal emails, local paths in repo | none found (only the approved public address) | Tested |
| GitHub Actions: SHA-pinned, read-only default token, no `pull_request_target`, PyPI off unless `PUBLISH_TO_PYPI=true` | pass | Implemented (runs only after push) |
| YAML parsing | `yaml.safe_load` only | Tested |
| PyPI project `osel` | `https://pypi.org/pypi/osel/json` → 404 (no such project today) | Checked. PyPI only confirms a name at first upload |
| GitHub name `orridian` | `api.github.com/users/orridian` → 404 (unclaimed today) | Checked |
| `gh` CLI | signed in as `lokeshyarlagadda473` | Checked |

Full machine output: [launch-audit-report.md](launch-audit-report.md).

## 2. Changes made today

| Change | Files | Status |
|---|---|---|
| Identity: Orridian / OSEL, founder Lokesh Yarlagadda, `@lokeshyarlagadda473` in CODEOWNERS, `orridian/osel` URLs | ~40 files | Implemented, tested |
| Contacts: general → `orridian.contact@gmail.com`; **security → GitHub private vulnerability reporting only** (never the inbox); conduct → inbox + trusted-adult alternate | SECURITY, CoC, policies, website | Implemented |
| Version `0.1.0a1` in package, CITATION.cff, website | 3 files + docs | Tested (audit consistency check) |
| License (MIT) and privacy policy marked **Adopted**, recording the parent/guardian approval you reported | policies/README, license.md, privacy.md, decision log | Implemented |
| Orridian homepage (static HTML) for `orridian/orridian.github.io` | `C:\Users\godboss\orridian.github.io\` (own git repo) | Implemented; previewed desktop + 375px, no overflow |
| Org profile README for `orridian/.github` | `C:\Users\godboss\orridian-dotgithub\profile\README.md` (own git repo) | Implemented |
| OSEL site footer: "a flagship initiative of Orridian" | Base.astro, README | Implemented |
| Earlier today's passes: 5 bug fixes, edge-case tests, demos, demo repo, early access program, release dry-run, labels | see CHANGELOG | Tested |

## 3. GitHub Pages layout (decided)

| URL | Source repo | Type |
|---|---|---|
| `https://orridian.github.io/` | `orridian/orridian.github.io` (repo name must match exactly) | Organization site, deploy from branch `main` |
| `https://orridian.github.io/osel/` | `orridian/osel`, `pages.yml` | Project site (base path `/osel/` set automatically) |
| `https://orridian.github.io/osel/docs/` | same workflow (MkDocs) | Part of the project site |

These paths aren't interchangeable. The homepage links to `/osel/` and `/osel/docs/`, which only work once both repos are deployed.

## 4. Original milestones (Nov 2026 – Feb 2028) — honest status

| Milestone | Status |
|---|---|
| Nov 2026: competitive research | **Planned.** The matrix template exists; the sourced research (MLflow, Langfuse, Phoenix, Opik, Promptfoo, Ragas, plus B/C alternatives) is not done |
| Nov 2026: user interviews, problem statements | **Planned.** The kit and 10 testable problems exist; no interviews yet |
| Nov 2026: org and repository setup | **In progress.** Everything is ready locally; the org doesn't exist yet |
| Dec 2026: architecture, APIs, prototype, tests, CI | **Implemented and tested** (ahead of schedule). CI unverified until push |
| Dec 2026: external feedback | Planned |
| Jan–Feb 2027: complete workflow, comparisons, reproducible reports | **Implemented and tested** |
| Jan–Feb 2027: alpha release, external testing | Release gates ready; not published |
| Mar 2027 onward | Not started. Correctly, since they depend on users |

Moonshot metrics: all are **0 / not yet measurable**. Definitions are in METRICS.md. Atlas is excluded from every OSEL figure.

## 5. Blockers that need you (or a parent/guardian)

1. **Create the GitHub org `orridian`** at github.com/organizations/plan (Free plan). This accepts GitHub's terms, so do it with your parent or guardian. GitHub doesn't allow org creation through the API from a personal account. Turn on 2FA, and add a trusted adult as a second owner.
2. **Trusted adult's alternate contact for Code of Conduct reports** (an email they agree to have published, or a route like "message @their-github-handle"). This fills `[conduct-alternate-contact]`.
3. **Approval to push and publish** once the org exists. Then I can run, with your approval: create the 3 repos, push, enable Pages, private vulnerability reporting, Discussions with the 4 categories, labels, the 5 good first issues, and the branch ruleset. I'll verify each step.
4. **PyPI:** you create the PyPI account (adult involvement) and add a "pending publisher" for project `osel`, owner `orridian`, repo `osel`, workflow `release.yml`, environment `pypi`. Publishing happens only after you've reviewed a release summary.
5. **Check that `orridian.contact@gmail.com` works** by sending a test email from another account.

## 6. Proposed sequence from here

1. You: items 1, 2 and 5 above.
2. Me (after your go-ahead): push all three repos, apply settings, enable Pages, and verify that the live URLs load and CI is green on Linux, macOS and Windows.
3. Me: run the release dry run, then tag `v0.1.0a1` as a draft GitHub pre-release, and give you the release summary.
4. You: review, then enable PyPI, and I publish and verify `pip install osel==0.1.0a1` in a clean environment.
5. Me, meanwhile (no accounts needed): sourced competitive research for A, B and C.
6. You: invite the first 5–10 testers (`programs/early-access.md`). Plan for about 8–12 hours a week, school first.
