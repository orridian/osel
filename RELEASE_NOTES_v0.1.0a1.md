# osel v0.1.0a1 — first public alpha


**This is an alpha.** It's ready for evaluation by early testers, but not for production use. Interfaces and file formats may change before 1.0.

## What osel does

Define an evaluation, run it, record exactly what produced the result, compare it with a baseline, and fail CI on regressions. It is local-first and file-based, needs no account, and has no telemetry.

## Highlights

- `osel dataset validate` reports row-level errors and a content-based dataset identity.
- `osel eval run` evaluates from a predictions file or directly against a Python function, and records config (secrets redacted), metric versions, environment and git commit.
- `osel compare` uses paired bootstrap confidence intervals and refuses comparisons when the dataset or a metric version changed.
- `osel check` gives CI exit codes (0 ok · 1 regression · 2 invalid input · 3 internal error). It covers mean drops, missing metrics and newly failing examples.
- A GitHub Action is included.

## Install

See [docs/installation.md](docs/installation.md).

## Important

- **Configs can run Python code with no sandbox. Only run configs you trust.**
- Read [docs/known-limitations.md](docs/known-limitations.md) before relying on results.

## Feedback

We're running a small [Early Access Program](programs/early-access.md). Bug reports and confusing moments are the most useful thing you can send us.

## Full changelog

See [CHANGELOG.md](CHANGELOG.md).
