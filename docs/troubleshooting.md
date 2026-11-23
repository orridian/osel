# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `cannot decode … as utf-8` | File is not UTF-8 | Pass `--encoding latin-1` (or the correct encoding), or set `encoding:` in the config |
| `unknown field(s) 'refrence'` | Typo in a dataset key | Allowed keys: `id`, `input`, `reference`, `metadata` |
| `no prediction for id 'x'` (in run errors) | Predictions file lacks that id | Regenerate predictions; check id spelling |
| `runs are not comparable: dataset changed` | Dataset content differs between runs | Re-run the baseline on the new dataset, or compare the right files |
| `metric 'm' version changed` | Metric scoring logic changed | Regenerate the baseline with the new metric version |
| `cannot import module 'my_system'` | Module not on the Python path | Add `python_path: ["."]` (relative to the config) |
| `only N scored examples; bootstrap intervals are unreliable` | Small dataset | Add examples. Treat the intervals as rough |
| `run reference 'abc' is ambiguous` | Prefix matches several runs | Use a longer prefix or the file path |
| `internal error` (exit 3) | A bug in osel | Re-run with `OSEL_DEBUG=1`, remove secrets, and open a bug report |
