# Decision log

Format: ID · date · decision · evidence/reasoning · alternatives · owner · status. Newest last. Sensitive details are omitted.

| ID | Date | Decision | Evidence / reasoning | Alternatives considered | Owner | Status |
|---|---|---|---|---|---|---|
| D-001 | 2026-11-11 | One monorepo (`osel`) holds code, docs, website, policies and operations | Components are tightly coupled; one founder; simpler CI. Split a component when independent versioning, ownership or cadence justifies it | Five separate repos (blueprint §3.1) | Founder | Accepted |
| D-002 | 2026-11-11 | License: MIT (proposed) | Short, widely understood, compatible | Apache-2.0 (explicit patent grant) | Founder | Accepted. Approved by parent/guardian 24 Nov 2026 |
| D-003 | 2026-11-11 | Python ≥ 3.10, setuptools + pyproject | Broad compatibility; standard tooling | Poetry, Hatch | Founder | Accepted |
| D-004 | 2026-11-11 | CLI uses argparse | Zero extra dependencies; adequate help output | Typer | Founder | Accepted |
| D-005 | 2026-11-11 | Validation uses dataclasses and hand-written checks | Small schemas; avoids a heavy dependency | Pydantic | Founder | Accepted; revisit if schemas grow |
| D-006 | 2026-11-11 | Data formats: JSON/JSONL in, JSON run records out; local files only | Portable, inspectable; no demand for scale yet | Parquet, SQLite | Founder | Accepted |
| D-007 | 2026-11-11 | Statistics: percentile bootstrap (seeded); paired bootstrap for comparisons; no p-values | Simple, assumption-light, reproducible; avoids universal significance claims | t-intervals, permutation tests | Founder | Accepted; independent review wanted |
| D-008 | 2026-11-11 | Dataset identity is order-independent (sorted by id) | Reordering rows does not change meaning | Order-sensitive hash | Founder | Accepted |
| D-009 | 2026-11-11 | No telemetry | No question that requires it; privacy value | Opt-in telemetry | Founder | Accepted |
| D-010 | 2026-11-11 | Website: Astro static site; docs: MkDocs Material | Blueprint §2.2 recommendations; low cost and maintenance | Single generator for both | Founder | Accepted |
| D-011 | 2026-11-11 | Exit codes 0/1/2/3 (ok/regression/invalid input/internal error) | Blueprint §4.5; CI-friendly | — | Founder | Accepted; stable from 0.1.0 |
