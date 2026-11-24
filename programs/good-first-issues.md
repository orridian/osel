# Good first issues (ready to file)

File these with the labels `good first issue` and `help wanted`. Maintainer contact: @lokeshyarlagadda473.

---

### 1. Add a `--quiet` flag to `osel eval run`

- **Problem:** in scripts, the full results table is noise when only the run file matters.
- **Context:** `cmd_eval_run` in `src/osel/cli.py` always prints `render_run`.
- **Expected behavior:** `--quiet` prints only `Saved run <id> -> <path>`.
- **Files:** `src/osel/cli.py`, `docs/cli.md`, `tests/test_cli.py`
- **Acceptance criteria:** the flag exists in `--help`; the test asserts the output is a single line; docs updated; CHANGELOG entry.
- **Test command:** `pytest tests/test_cli.py`

### 2. Add a `regex_match` built-in metric

- **Problem:** users want to check that the output matches a pattern (e.g. a date format).
- **Context:** built-ins live in `src/osel/metrics.py` (`BUILTIN_METRICS`).
- **Expected behavior:** `{"use": "regex_match"}` scores 1.0 when `re.fullmatch(reference, str(prediction))` matches. An invalid regex raises `MetricError`.
- **Files:** `src/osel/metrics.py`, `docs/metrics.md`, `tests/test_metrics.py`
- **Acceptance criteria:** tests for match, no match and invalid pattern; docs table row; version "1".
- **Test command:** `pytest tests/test_metrics.py`

### 3. Show the number of compared examples in `osel compare` text output

- **Problem:** the paired CI is computed over examples scored in both runs, but the count isn't shown.
- **Files:** `src/osel/report.py` (`render_comparison`), `tests/test_cli.py`
- **Acceptance criteria:** a new `n` column shows `paired_n`; the existing tests still pass; a docs example is updated.
- **Test command:** `pytest`

### 4. Docs: add a "Evaluate a scikit-learn classifier" how-to

- **Problem:** there is no example for classical ML users.
- **Files:** new `docs/howto-sklearn.md`, add it to the `mkdocs.yml` nav
- **Acceptance criteria:** a predictions file is produced from a small public dataset; `exact_match` is used as accuracy; `mkdocs build --strict` passes; sklearn is **not** added as an osel dependency.
- **Test command:** `mkdocs build --strict`

### 5. Better error for a `.yml` config containing tabs

- **Problem:** YAML tab-indentation errors produce a cryptic parser message.
- **Files:** `src/osel/config.py`, `tests/test_runner_record.py`
- **Acceptance criteria:** if the file contains a tab and parsing fails, the error message adds "YAML does not allow tab indentation". A test covers it.
- **Test command:** `pytest tests/test_runner_record.py`
