# Python API

Everything the CLI does is available from Python:

```python
from osel import load_config, run_evaluation, save_run, load_run, compare_runs
from osel.compare import find_regressions
from osel.report import render_comparison

baseline = load_run("baseline.json")
current = run_evaluation(load_config("evals/config.yaml"))
save_run(current, "current.json")

cmp = compare_runs(baseline, current)          # raises IncompatibleRunsError if not comparable
print(render_comparison(cmp))
if find_regressions(cmp, per_metric={"exact_match": 0.01}):
    raise SystemExit(1)
```

| Name | Purpose |
|---|---|
| `load_dataset(path, encoding="utf-8") -> Dataset` | Load and validate; raises `InvalidInputError` with row-level `details` |
| `osel.dataset.validate_dataset(path)` | `(dataset or None, [RowError])` without raising for row problems |
| `load_config(path) -> EvalConfig` | Parse and validate a config |
| `run_evaluation(config) -> RunRecord` | Execute (does not save) |
| `save_run(record, path)` / `load_run(path)` | Persist and read run records |
| `osel.record.RunStore(root)` | `.save()`, `.list()`, `.resolve(ref)`, `.load(ref)` |
| `compare_runs(baseline, current, allow_incompatible=False)` | → `Comparison` |
| `osel.compare.find_regressions(cmp, tolerance=0, per_metric=None, require_ci=False)` | → list of `Regression` |
| `osel.stats` | `mean`, `sample_std`, `quantile`, `bootstrap_mean_ci`, `paired_difference` |

Exceptions: `OselError` → `InvalidInputError` (exit code 2) → `IncompatibleRunsError`. Metrics raise `osel.errors.MetricError`.
