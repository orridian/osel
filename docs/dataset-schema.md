# Dataset schema (version 1)

| Field | Required | Type | Notes |
|---|---|---|---|
| `id` | yes | non-empty string | Unique in the dataset; keep it stable across dataset versions |
| `input` | yes | any JSON | Passed to your system |
| `reference` | no | any JSON | Expected output; most metrics need it |
| `metadata` | no | object | Free-form tags, e.g. `{"source": "manual", "difficulty": "hard"}` |

Any other top-level key is an error. This catches typos like `refrence`.

## File formats

**JSONL** (`.jsonl`): one object per line. Blank lines are ignored.

```json
{"id": "q01", "input": "What is the capital of France?", "reference": "Paris"}
```

**JSON** (`.json`): either a list of objects, or

```json
{"schema_version": "1", "examples": [ {"id": "q01", "input": "...", "reference": "..."} ]}
```

Files are read as UTF-8 by default; a UTF-8 BOM is tolerated. Use `--encoding` (CLI) or `encoding:` (config) for anything else.

## Validation errors

`osel dataset validate` reports **every** problem with its row number. For example:

```text
INVALID: data.jsonl: 3 problem(s)
  - row 2: field 'id' must be a non-empty string
  - row 3: invalid JSON: Expecting property name enclosed in double quotes (column 2)
  - row 7: duplicate id 'e1' (first seen at row 1)
```

## Identity rules

`identity = "sha256:" + sha256(JSON of examples sorted by id, keys sorted, compact separators)`.
A `reference` of `null` is different from a missing `reference`.
