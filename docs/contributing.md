# Contributing

The canonical guide is [CONTRIBUTING.md](https://github.com/orridian/osel/blob/main/CONTRIBUTING.md) in the repository. In short:

```bash
pip install -e ".[dev]"
pytest && ruff check . && mypy src
```

- Pick an issue labelled `good first issue`. Each one states the problem, context, acceptance criteria, test command and a maintainer contact.
- Keep PRs focused. Tests and docs are required for user-visible changes.
- First response target: 14 days. This is a target, not a promise.
- Documentation, testing, triage and design work are acknowledged in release notes (with your consent).

The newcomer program is described in `programs/contributor-programs.md`.
