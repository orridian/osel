# Blueprint coverage

Maps every section of the *OSEL Master Build & Operations Blueprint* to its implementation.
**Status key:** ✅ built and verified · 🟡 built, needs a human action (review, account, decision) · ⏳ intentionally deferred by the blueprint's own gates · 👤 can only be done by a person.

| § | Item | Where | Status |
|---|---|---|---|
| 0 | Priorities P0/P1/P2, definition of complete | [ownership.md](ownership.md) (owner, purpose, implementation, test, maintenance per component) | ✅ |
| 1.1 | Identity | [FOUNDING.md](../FOUNDING.md); name/domain conflict check | 🟡 name check is 👤 |
| 1.2 | FOUNDING, MISSION, VISION, VALUES, STRATEGY, ROADMAP, METRICS, GOVERNANCE | repo root | ✅ drafts; replace `Lokesh Yarlagadda` |
| 1.3 | Founder evidence archive | [founder-evidence-archive.md](founder-evidence-archive.md) | 🟡 create the private archive |
| 2.1 | Website: /, /about, /projects, /roadmap, /community, /governance, /security, /privacy, /contact, /blog | [website/](../website/) (Astro, 12 pages, link-checked) | ✅ built · 🟡 not deployed |
| 2.2 | Web stack: Astro, static host, MkDocs, no analytics, role email | website/, mkdocs.yml | 🟡 host, domain, email are 👤 with adult help |
| 2.3 | Website launch checklist | [website-launch-checklist.md](website-launch-checklist.md) | 🟡 run at launch |
| 3.1 | Repositories | Monorepo (decision D-001); split later if justified | ✅ |
| 3.2 | Standard files: README, LICENSE, CONTRIBUTING, CoC, SECURITY, CHANGELOG, CITATION, issue/PR templates, workflows, docs, tests, examples, benchmarks | repo root, .github/ | ✅ |
| 3.3 | Branch and review rules | [repo-settings.md](repo-settings.md), CODEOWNERS | 🟡 apply after creating the GitHub org |
| 4.1–4.2 | Product goal, technical baseline | `src/osel`, pyproject.toml | ✅ |
| 4.3 | Modules: schema, loader, identity, metric interface, runner, run record, comparison, statistics, report, CLI, CI action | `src/osel/*`, `integrations/github-action` | ✅ (52 tests) |
| 4.3 | Plugin/extension API | — | ⏳ "only after use cases emerge" |
| 4.4 | Command set: validate, run, show, compare, report, check | `osel` CLI | ✅ |
| 4.5 | Quality gates | CI workflow + tests (clean install, quick start, exit codes, no secrets, stats checked vs reference) | ✅ locally · 🟡 CI runs on first push |
| 5.1–5.2 | Product B, Product C | [programs/product-b-c-gated-specs.md](../programs/product-b-c-gated-specs.md) | ⏳ gated |
| 5.3 | Expansion gate | [STRATEGY.md](../STRATEGY.md#expansion-gate) | ✅ |
| 6 | 19 policies | [policies/](../policies/) with owner, review date, channel, enforcement | ✅ written · 🟡 adult/expert review for license, privacy, data handling |
| 6.1 | Code of Conduct structure (8 parts) | [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) | ✅ · 🟡 set up conduct/alternate addresses |
| 6.2 | Security disclosure workflow (8 steps) | [SECURITY.md](../SECURITY.md), [vulnerability-disclosure.md](../policies/vulnerability-disclosure.md) | ✅ |
| 7.1–7.5 | Contributor programs | [programs/contributor-programs.md](../programs/contributor-programs.md), [good-first-issues.md](../programs/good-first-issues.md) | ✅ First Contribution ready · ⏳ ambassador (later stage) |
| 8.1 | Reproducibility Program | [programs/reproducibility-program.md](../programs/reproducibility-program.md) + protocol template | ✅ designed · ⏳ first protocol after discovery |
| 8.2 | University engagement | [programs/university-engagement.md](../programs/university-engagement.md) | ✅ process · 👤 outreach |
| 9.1 | Workshop: outline, slides, hands-on repo, participant guide, feedback form, event checklist, follow-up | [programs/workshop/](../programs/workshop/) | ✅ |
| 9.2 | Learner counting | [METRICS.md](../METRICS.md), workshop outline | ✅ |
| 10.1–10.3 | Support channels, bug and feature templates | [programs/support.md](../programs/support.md), .github/ISSUE_TEMPLATE | ✅ |
| 11.1–11.2 | Release process, versioning | [release-checklist.md](release-checklist.md), [policies/release.md](../policies/release.md), release.yml | ✅ |
| 11.3 | Quality dashboard | [quality-dashboard.md](quality-dashboard.md) | ✅ |
| 12 | Metric definitions, impact report, ledger | METRICS.md, [metric-ledger.md](metric-ledger.md), templates/ | ✅ |
| 13 | Cadence and role map | [cadence.md](cadence.md), GOVERNANCE.md | ✅ |
| 14 | Risk register | [risk-register.md](risk-register.md) | ✅ |
| 15 | First 90-day build order | Steps 1, 3–10, 12 built; 2 and 11 need people | 🟡 |
| 16 | What not to build yet | Not built: auth, SaaS, database, marketplace, extra teams, ambassadors, fellowships, leaderboard, conference, telemetry | ✅ respected |
| 17 | First-week action list | [first-week-actions.md](first-week-actions.md) | 🟡 |
| 18 | Final operating rules | Enforced through templates (issue/PR), METRICS.md, policies index, ownership.md | ✅ |
