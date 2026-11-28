# Changelog

All notable user-visible changes are recorded here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: see [policies/release.md](policies/release.md).

## [Unreleased]

### Fixed
- `--require-ci` no longer treats a zero-width paired interval as statistical evidence. With one paired example, or with identical non-zero differences on too few examples (sign test: fewer than 6 at 95%), `ci_excludes_zero` is now `null` with an explanation (`ci_note`). Identical differences on enough examples still count.

### Added
- Comparisons now carry `warnings`, shown by `osel compare` and `osel check` and included in their JSON: small paired samples (< 30), uninformative intervals, and the higher chance of a false alarm when several metrics are compared.

## [0.1.0a1] — 2026-11-24 (first public alpha)

### Added
- Dataset schema v1 (`id`, `input`, optional `reference`, `metadata`) with row-level validation errors.
- JSON/JSONL dataset loader with explicit encoding and content-derived dataset identity.
- Metric interface plus built-in metrics: `exact_match`, `contains`, `token_f1`, `abs_error`. Custom metrics load via `module:attr`.
- Evaluation runner using a predictions file or a Python callable. Per-example exceptions are recorded safely.
- Run records with environment metadata and secret redaction; local run store in `.osel/runs/`.
- Comparison engine with compatibility checks, and a statistical layer (seeded bootstrap CIs, paired differences).
- CLI: `osel dataset validate`, `osel eval run`, `osel run show`, `osel compare`, `osel report`, `osel check`.
- Stable exit codes: 0 ok, 1 regression, 2 invalid input, 3 internal error.
- Composite GitHub Action for CI regression checks.
- `osel check --max-new-errors N`: an increase in failed examples is now a regression (default: any increase).

### Fixed (launch audit)
- `osel check` passed when the current system failed on some or all examples, because means only cover scored examples. New failures and "no scored examples" are now regressions.
- Secret redaction no longer hides ordinary config keys such as `author` or `max_tokens`. It matches whole words (`token`, `password`, `apiKey`, …) and recognizes more token formats.
- Runs no longer crash at save time when a system returns a non-JSON value (e.g. a set). The value is stored as text and a warning is added.
- The GitHub Action passes inputs through environment variables instead of interpolating them into shell scripts.
- `osel run show latest` and `osel run list` order runs by creation time (microseconds), not run ID. Previously two runs in the same second could be returned in the wrong order.

### Added (launch preparation)
- Docs: installation and upgrading, known limitations; prominent "configs execute code, no sandbox" warnings.
- Three tested technical demonstrations in `examples/demos/` (reproducibility, regression detection, statistical uncertainty).
- GitHub Pages deployment for the website and docs; all GitHub Actions pinned to commit SHAs; PyPI publishing gated behind a repository variable; alpha versions published as pre-releases.
- `scripts/launch_audit.py` and `scripts/set_identity.py`.
