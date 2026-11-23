# Participant guide

## Setup (before the workshop, about 10 min)

```bash
git clone https://github.com/[osel-org]/osel.git
cd osel
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install .
osel --version
```

## Exercise 1 — Validate and run

```bash
cd examples/quickstart
osel dataset validate data.jsonl
osel eval run config.yaml --output baseline.json
```

1. Write down the dataset identity.
2. Open `data.jsonl` and change one reference. Validate again. What changed?
3. Undo your edit, and confirm the identity is back to the original.

## Exercise 2 — Compare and interpret

```bash
osel eval run config_v2.yaml --output current.json
osel compare baseline.json current.json
```

1. Which metrics degraded, and by how much?
2. What does "CI includes 0" mean here, and why?
3. Open `current.json`. Find the examples that changed.

## Exercise 3 — Custom metric + CI gate

```bash
cd ../function-eval
osel eval run config.yaml --output good.json
osel eval run config_buggy.yaml --output buggy.json
osel check --baseline good.json --current buggy.json
echo $?        # PowerShell: $LASTEXITCODE
```

1. Read `custom_metrics.py`. What would you need to change if you changed its scoring logic?
2. Which example raised an error in the buggy system, and where is the error recorded?

## Troubleshooting

| Problem | Fix |
|---|---|
| `osel: command not found` | Activate the venv, or use `python -m osel` |
| Python too old | Install Python 3.10+ |
| Windows: `$?` shows True/False | Use `$LASTEXITCODE` |

## Next steps

Try osel on one of your own evaluations, then tell us what got in the way (GitHub Discussions).
