# Installation and upgrading

## Requirements

Python 3.10–3.13 on Linux, macOS or Windows. The only runtime dependency is PyYAML.

## Install (alpha, from source)

Use a virtual environment so osel doesn't affect other projects:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install "git+https://github.com/[osel-org]/osel.git@v0.1.0a1"
osel --version
```

Pin the version tag (`@v0.1.0a1`). Alpha releases may change behavior between versions.

Once osel is on PyPI, this will become `pip install "osel==0.1.0a1"`.

If `osel` isn't found after installing, the virtual environment probably isn't active. You can always use `python -m osel ...` instead.

## Upgrading

```bash
pip install --upgrade "git+https://github.com/[osel-org]/osel.git@<new-tag>"
```

Before upgrading:

1. Read the changelog for **Breaking changes** (pre-1.0 minor versions may contain them).
2. If a metric's `version` changed, old and new runs are no longer comparable. Regenerate your baseline with the new version in the same change.
3. Run `osel check` against your existing baseline once. If it exits `2`, read the message: it tells you what became incompatible.

## Uninstall

```bash
pip uninstall osel
```

Run records you created (`.osel/runs/`, `--output` files) are plain JSON. They stay where they are until you delete them.
