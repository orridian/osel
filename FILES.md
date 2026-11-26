# OSEL — file inventory

Every file in this project, what it is, and what it does. The project was built from the *OSEL Master Build & Operations Blueprint* (.docx).
Not listed (generated, don't upload): `.venv/` (Python environment), `website/node_modules/` (website packages), `site/` and `dist/` (build output).

**Verified locally (launch audit, 22 Nov 2026):** 90 automated tests pass; lint (`ruff`) and strict type checks (`mypy`) are clean; the package builds and the documented quick start passes in a fresh environment with the documented exit codes; the website and docs build together with 0 broken links (603 links) both at a custom-domain root and under a GitHub Pages sub-path; no secrets, personal emails or local paths are in the files; all GitHub Actions are pinned to commit SHAs. Run `python scripts/launch_audit.py` to repeat every check.

**Status (26 Nov 2026):** public at https://github.com/orridian/osel; v0.1.0a1 released on GitHub as a pre-release; website and docs live at https://orridian.github.io/osel/. PyPI publishing is being enabled. Full history: `operations/execution-report-2026-11-24.md`.

---

## 1. Founding documents (repo root) — blueprint §1

| File | What it is |
|---|---|
| `FOUNDING.md` | Founding record: date (11 Nov 2026), founder role, why OSEL exists, initial problem and scope, first artifacts, roles that actually exist |
| `MISSION.md` | One-sentence mission, who benefits, intended impact, boundaries (what OSEL won't claim or do) |
| `VISION.md` | Long-term three-product vision. Product A exists (alpha); B and C are labelled hypotheses |
| `VALUES.md` | Seven values, each paired with concrete behaviors that demonstrate it |
| `STRATEGY.md` | Problem, audience, differentiation hypothesis, distribution, risks, decision gates G1–G4, and the expansion gate for new products |
| `ROADMAP.md` | Now / Next / Later tables with owner, acceptance criteria and status; dates marked as targets |
| `METRICS.md` | Exact definitions of every metric (what counts and what doesn't), collection method, exclusions, reporting cadence |
| `GOVERNANCE.md` | Who decides what, role map (filled vs unfilled roles), how to become a maintainer, conflict resolution, succession |

## 2. Standard repository files — blueprint §3.2

| File | What it is |
|---|---|
| `README.md` | Project front page: what osel does, quick start, commands, exit codes, links |
| `LICENSE` | MIT License (proposed; marked for adult/expert review before first release) |
| `CONTRIBUTING.md` | Setup, how to run checks, style, branch/PR process, review expectations |
| `CODE_OF_CONDUCT.md` | 8-part Code of Conduct: scope, standards, unacceptable conduct, reporting (with an alternate contact), response, confidentiality, enforcement, review |
| `SECURITY.md` | Supported versions, private vulnerability reporting, the 7-step response process |
| `CHANGELOG.md` | User-visible changes (everything is under "Unreleased" for now) |
| `CITATION.cff` | How researchers should cite the software |
| `.gitignore` | Keeps the Python env, build output, secrets and private records out of git |
| `FILES.md` | This file |
| `RELEASE_NOTES_v0.1.0a1.md` | Draft release notes for the first public alpha |

## 3. GitHub setup — `.github/` — blueprint §3.2–3.3, §10

| File | What it is |
|---|---|
| `ISSUE_TEMPLATE/bug_report.yml` | Bug form: version, OS/Python, steps, expected vs actual, logs, a "no secrets" confirmation |
| `ISSUE_TEMPLATE/feature_request.yml` | Feature form: problem, who/workflow, workaround, why inadequate, desired outcome, success measure, implications |
| `ISSUE_TEMPLATE/documentation.yml` | Docs problem form |
| `ISSUE_TEMPLATE/alpha_feedback.yml` | Early-access tester feedback form (time to first run, where they got stuck) |
| `ISSUE_TEMPLATE/config.yml` | Disables blank issues; links to private security reporting and Discussions |
| `PULL_REQUEST_TEMPLATE.md` | Summary, motivation, tests, docs, breaking changes, AI-assistance disclosure, confirmations |
| `CODEOWNERS` | Who must review which paths (security-sensitive files flagged) |
| `labels.yml` | Issue label definitions (`bug`, `needs reproduction`, `priority: high`, `alpha-feedback`, …) |
| `dependabot.yml` | Weekly/monthly dependency update checks |
| `workflows/ci.yml` | CI: lint + types, tests on 3 OSes × 4 Python versions, build + clean-install quick-start test, strict docs build, license check, dependency review |
| `workflows/release.yml` | On a version tag: run checks, build, checksums, provenance attestation, draft GitHub release, publish to PyPI via Trusted Publishing |
| `workflows/action-integration.yml` | Tests the GitHub Action (pass, warn mode, fail mode, missing baseline) |
| `workflows/website.yml` | PR check: builds website + docs under a sub-path and checks every link |
| `workflows/pages.yml` | Deploys the website (/) and docs (/docs/) to GitHub Pages (free, no domain needed) |

## 4. The software — `osel` Python package — blueprint §4

`pyproject.toml` defines the package, the `osel` command, dependencies (only PyYAML at runtime) and settings for pytest, ruff and mypy.

| File (`src/osel/`) | What it does |
|---|---|
| `__init__.py` | Version number and the public Python API |
| `__main__.py` | Lets you run `python -m osel` |
| `errors.py` | Error types and exit codes: 0 ok, 1 regression, 2 invalid input, 3 internal error |
| `schema.py` | Dataset example format: `id`, `input`, optional `reference` and `metadata`; rejects unknown fields (catches typos) |
| `dataset.py` | Loads JSON/JSONL datasets, reports errors by row, handles encodings, computes a content hash ("dataset identity") that ignores row order and formatting but changes when any content changes |
| `metrics.py` | Metric interface plus built-ins (`exact_match`, `contains`, `token_f1`, `abs_error`); loads custom metrics from `module:Class`; rejects NaN or non-numeric scores |
| `config.py` | Reads and validates YAML/JSON evaluation configs |
| `runner.py` | Runs an evaluation from a predictions file or a Python function; records per-example errors without crashing; computes averages and confidence intervals |
| `record.py` | Run record format; saves and loads runs; redacts secrets; records environment (Python, OS, git commit) but never environment variables; local run store with ID-prefix and `latest` lookup |
| `stats.py` | Mean, standard deviation, quantiles, seeded bootstrap confidence intervals, paired differences, with assumptions documented |
| `compare.py` | Compares two runs, refuses incompatible ones (dataset or metric version changed), computes paired statistics, finds regressions against thresholds |
| `report.py` | Text and JSON output; statuses spelled out in words, never colour-only |
| `cli.py` | The commands: `dataset validate`, `eval run`, `run show`, `run list`, `compare`, `report`, `check` |
| `py.typed` | Marks the package as type-annotated |

## 5. Tests — `tests/` — blueprint §4.5 quality gates

| File | What it checks |
|---|---|
| `conftest.py` | Shared test helpers (builds small temporary evaluations) |
| `fixtures/valid.jsonl`, `fixtures/valid_reordered.json` | The same valid dataset in two formats and orders (must give the same identity) |
| `fixtures/invalid.jsonl` | One example of every kind of error (bad JSON, missing field, typo, duplicate ID…) |
| `test_dataset.py` | Loading, every row error, identity stability and change detection, empty files, encodings, BOM |
| `test_metrics.py` | Each built-in metric against hand-computed values; custom metric loading; bad configs |
| `test_stats.py` | Statistics checked against Python's own `statistics` module; seeded reproducibility; intervals narrow with more data |
| `test_runner_record.py` | Deterministic known results, errors recorded safely, save/load round trip, **no secrets or env vars in run files**, config validation |
| `test_compare.py` | Equal runs, improved/degraded, lower-is-better metrics, changed dataset, changed metric version, missing metric, noise vs real change |
| `test_cli.py` | Help, every exit code, the full documented workflow end to end, missing-baseline behaviour |
| `test_examples.py` | Every shipped example produces its documented numbers |
| `test_audit_edge_cases.py` | Launch-audit cases: tiny/identical/large-difference statistics, missing values, seeds, lower-is-better, new failures as regressions, secret-key rules, non-JSON outputs, `latest` ordering |
| `test_demos.py` | The claims in the three technical demos stay true |

## 6. Examples — `examples/`

| File | What it is |
|---|---|
| `quickstart/data.jsonl` | 10 capital-city questions |
| `quickstart/predictions_v1.jsonl`, `predictions_v2.jsonl` | Two "models": v1 scores 0.8; v2 is a deliberate regression (0.6) |
| `quickstart/config.yaml`, `config_v2.yaml` | Configs for each |
| `quickstart/README.md` | Commands and expected results |
| `function-eval/data.jsonl` | 6 addition problems |
| `function-eval/my_system.py` | A correct `add` function and a `buggy_add` function |
| `function-eval/custom_metrics.py` | Example of writing your own metric |
| `function-eval/config.yaml`, `config_buggy.yaml` | Evaluate a Python function directly |
| `demo-repo/` | Standalone demo project to publish as its own repo: baseline → changed function → regression → CI blocks the PR |
| `demos/README.md` | Index of the three technical demonstrations |
| `demos/01-reproducibility/README.md` | Same inputs → same result; changed data → comparison refused |
| `demos/02-regression/README.md` | Thresholds and newly failing examples caught by `osel check` |
| `demos/03-uncertainty/` | `generate.py` + `small/` (40) and `large/` (400) scenarios: same +5-point gain, noise vs clear |

## 7. CI integration — `integrations/github-action/`

| File | What it is |
|---|---|
| `action.yml` | A GitHub Action other projects can use to run osel and fail (or warn) on regressions |
| `README.md` | How to use it, and behaviour in each situation |

## 8. Documentation site — `docs/` + `mkdocs.yml` (MkDocs Material)

| File | Topic |
|---|---|
| `index.md` | Docs home page |
| `installation.md` | Install, upgrade, uninstall |
| `known-limitations.md` | Everything osel can't do yet (security, statistics, formats, platform) |
| `quickstart.md` | Install and the first run |
| `concepts.md` | Examples, identity, runs, comparisons |
| `dataset-schema.md` | Data format and validation |
| `config.md` | Every config option, plus security and secrets notes |
| `metrics.md` | Built-in metrics; how to write a custom one |
| `statistics.md` | Methods, assumptions and limitations, compatibility rules |
| `ci-integration.md` | Using it in CI; exit codes; managing baselines |
| `cli.md` | Command reference |
| `run-record.md` | Run file format |
| `api.md` | Python API |
| `architecture.md` | How the modules fit together; design decisions |
| `troubleshooting.md` | Common errors and fixes |
| `contributing.md` | Short contributor guide |

## 9. Website — `website/` (Astro static site) — blueprint §2

| File | What it is |
|---|---|
| `package.json`, `package-lock.json`, `astro.config.mjs` | Website setup (Astro + sitemap) |
| `src/site.ts` | Single place for domain, emails and links (placeholders to fill in) |
| `src/layouts/Base.astro` | Shared layout: skip link, navigation, footer, metadata |
| `src/layouts/Post.astro` | Blog post layout |
| `src/styles/global.css` | Visual style: light/dark mode, accessible contrast, mobile layout |
| `src/pages/index.astro` | Home: what OSEL is, who it's for, proof, status |
| `src/pages/about.astro` | Mission, origin, organization model, principles |
| `src/pages/projects.astro` | Products A/B/C with honest status labels |
| `src/pages/roadmap.astro` | Now/Next/Later, milestones, risks |
| `src/pages/community.astro` | Questions, bugs, contributing, alpha testers, response expectations |
| `src/pages/governance.astro` | Decision-making summary |
| `src/pages/security.astro` | Private vulnerability reporting |
| `src/pages/privacy.astro` | What data is collected (almost none) |
| `src/pages/contact.astro` | Role-based contacts with response targets |
| `src/pages/404.astro` | Not-found page |
| `src/pages/blog/index.astro` | Blog list |
| `src/pages/blog/why-osel.md` | First post: the problem, what exists, what's unknown, limitations |
| `public/favicon.svg` | Logo |
| `public/robots.txt` | Search-engine rules |
| `scripts/check-links.mjs` | Finds broken internal links (incl. docs) and links that ignore the deploy base path |
| `drafts/` | Unpublished blog posts: alpha announcement, architecture article (moved into `src/pages/blog/` when ready) |

## 10. Policies — `policies/` — blueprint §6

Each policy states its owner, review date, reporting channel and enforcement. `README.md` is the index with status (in force or draft) and trigger.

| File | Policy |
|---|---|
| `license.md` | License choice, third-party code, contribution licensing |
| `privacy.md` | Privacy policy (needs adult review before launch) |
| `telemetry.md` | No telemetry, plus strict rules if it's ever proposed |
| `data-handling.md` | Data classes and rules (draft) |
| `contribution.md` | How contributions are accepted and reviewed |
| `ai-assisted-contribution.md` | Rules for AI-generated contributions |
| `release.md` | Versioning, release criteria, yanking |
| `deprecation.md` | Notice periods (draft, from 1.0) |
| `vulnerability-disclosure.md` | Security workflow with target times |
| `conflict-of-interest.md` | Disclosure rules (draft) |
| `research-integrity.md` | Reproducibility and authorship rules (draft) |
| `benchmark-integrity.md` | No cherry-picking; verification labels |
| `community-events.md` | Event safety, consent, accessibility (draft) |
| `brand-and-attribution.md` | Name/logo use, accurate affiliation |
| `accessibility.md` | WCAG 2.2 AA target |
| `records-retention.md` | What records are kept and for how long |
| `incident-response.md` | Severity levels and response steps |

(Code of Conduct and Security policy live in the repo root.)

## 11. Operations — `operations/` — blueprint §§1.3, 2.3, 11–17

| File | What it is |
|---|---|
| `README.md` | Index; explains that private records live outside the repo |
| `launch-checklist.md` | **The 25-item public-alpha launch checklist with current status** |
| `content-calendar.md` | Six-week post-launch content plan |
| `launch-audit-report.md` | Latest output of `scripts/launch_audit.py` |
| `blueprint-coverage.md` | **Maps every blueprint section to its file and status** (best starting point for a reviewer) |
| `first-week-actions.md` | Blueprint §17 checklist with status |
| `project-board.md` | Board columns and starting cards |
| `decision-log.md` | 11 recorded decisions with reasoning and alternatives |
| `risk-register.md` | Risks, warning signs, mitigations, likelihood/impact |
| `cadence.md` | Weekly, monthly, quarterly, per-release and per-incident checklists |
| `ownership.md` | Owner, test method and maintenance plan for every component |
| `release-checklist.md` | 9-step release process |
| `quality-dashboard.md` | Quality signals and where to read them |
| `metric-ledger.md` | Template for the private evidence ledger behind reported numbers |
| `repo-settings.md` | GitHub org, branch protection and security settings to apply |
| `website-launch-checklist.md` | Pre-launch checks |
| `access-review.md` | Quarterly permissions audit template |
| `founder-evidence-archive.md` | What founding evidence to keep, and privacy rules |
| `competitor-matrix.md` | Six candidate competitors (**cells unverified; must be researched**) |
| `user-problems.md` | 10 testable candidate user problems |
| `interview-kit.md` | Interviewee list template, outreach message, interview script |
| `time-budget.md` | Weekly time budget built around school and sleep |
| `templates/weekly-plan.md`, `monthly-report.md`, `quarterly-impact-report.md`, `post-incident-review.md`, `alpha-feedback.md`, `early-access-tracker.md` | Reporting and tracking templates |

## 12. Programs — `programs/` — blueprint §§5, 7–10

| File | What it is |
|---|---|
| `README.md` | Program index with stage |
| `early-access.md` | **Early Access Program**: tester commitment, success criteria (30 invited → 10 installs → 5 workflows → 3 returning), outreach targets |
| `demo-video-script.md` | 75-second demo video script |
| `contributor-programs.md` | First Contribution, Regular Contributor, Maintainer Development, Ambassador (not launched), recognition |
| `good-first-issues.md` | 5 beginner issues written in full, ready to post |
| `reproducibility-program.md` | How each reproducibility study is run |
| `templates/research-protocol.md` | Protocol to write before running an experiment |
| `university-engagement.md` | 6-stage process plus a one-page brief template |
| `support.md` | Support channels, triage labels, response targets |
| `product-b-c-gated-specs.md` | Outlines for Products B and C. **Not started**; gated by the expansion rule |
| `workshop/README.md` | Workshop kit index |
| `workshop/outline.md` | Objectives, agenda, instructor notes, how learners are counted |
| `workshop/slides.md` | Slide content |
| `workshop/participant-guide.md` | Setup, 3 hands-on exercises, troubleshooting |
| `workshop/feedback-form.md` | Feedback questions |
| `workshop/event-checklist.md` | Before / during / after checklist |
| `workshop/follow-up.md` | Follow-up message |

## 13. Maintainer scripts — `scripts/`

| File | What it does |
|---|---|
| `launch_audit.py` | Runs every automated launch check (placeholders, secrets/personal info, versions, workflow pinning, policy status, links, tests, lint, types, clean install, docs + website builds) and lists the human steps. PASS/FAIL/HUMAN report |
| `create_labels.py` | Creates the labels from `.github/labels.yml` on GitHub via `gh` (dry run by default) |
| `set_identity.py` | Replaces the identity placeholders everywhere (already applied 24 Nov 2026; kept for reference) |

## 14. Other

| File | What it is |
|---|---|
| `benchmarks/README.md` | Folder structure for future reproducible studies (none published yet) |


---

## Intentionally NOT built (the blueprint says to wait)

Products B and C, the plugin system, the ambassador program, user accounts/login, a hosted SaaS dashboard, a database, a public leaderboard, telemetry.

## Needs a person (can't be done in code)

Filling in placeholders; checking the name is free; domain, hosting and email setup (with a parent/guardian); confirming the license; creating the GitHub org and pushing; user interviews; verifying the competitor matrix.
