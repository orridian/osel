# Contributing to OSEL

Thank you for helping. This guide gets you from a clean machine to a reviewed pull request.
Please read the [Code of Conduct](CODE_OF_CONDUCT.md) and the [contribution policy](policies/contribution.md) first.

## 1. Environment setup

Requirements: Python 3.10+ and git.

```bash
git clone https://github.com/orridian/osel.git
cd osel
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
```

## 2. Run the checks (the same ones CI runs)

```bash
pytest                 # unit + integration tests
ruff check .           # lint
mypy src               # type checks
python -m build        # packaging
mkdocs build --strict  # docs (needs: pip install -e ".[docs]")
```

## 3. Style

- Formatting and linting: `ruff` (configured in `pyproject.toml`).
- Type hints on public functions.
- No new runtime dependencies without discussion in an issue first.
- User-visible behavior changes need **tests and docs** in the same PR.

## 4. Branch and PR process

1. Find or open an issue with a problem statement and acceptance criteria. Look for `good first issue` labels.
2. Create a branch: `fix/short-name` or `feat/short-name`.
3. Keep the PR focused and reasonably small.
4. Fill in the PR template: summary, motivation, tests, docs, breaking changes.
5. CI must pass. At least one maintainer review is required. Security-sensitive changes get a second review when feasible.
6. You can't approve your own PR.
7. Add a `CHANGELOG.md` entry under **Unreleased** for user-visible changes.

## 5. Review expectations

We aim to give a first response within **14 days**. This is a target, not a promise; OSEL is maintained by volunteers. If a PR has had no response after 14 days, a polite ping is welcome.
We will always tell you what happened to your contribution: merged, changes requested, or closed with a reason.

## 6. AI-assisted contributions

These are allowed under the [AI-assisted contribution policy](policies/ai-assisted-contribution.md). You remain responsible for the code. Test it, understand it, and disclose substantial generated work in the PR.

## 7. Non-code contributions

Documentation, testing, triage, design and community work are real contributions and are acknowledged in release notes (with your consent).

## 8. Never post secrets

Never put API keys, passwords, private datasets or personal information in issues, PRs or test fixtures.
