# Known limitations (alpha)

osel is **alpha** software. These are the limitations we know about. If you hit one that isn't listed, please open an issue.

## Security

- **Configs can execute code, with no sandbox.** `system:` and custom metrics import Python modules and run them with your permissions. Only run configs you trust.
- Secret redaction in run records is keyword- and pattern-based. It can miss a secret stored under an innocent-looking key. Don't put secrets in configs.

## Statistics

- The percentile bootstrap is unreliable below about 30 scored examples (osel warns), and can be too narrow for binary metrics near 0 or 1.
- Examples are assumed independent. Near-duplicates make intervals too narrow.
- No correction is made for comparing many metrics.
- Randomness *inside your system* (sampling, nondeterministic models) is not captured by a single run. Run it several times.
- Bootstrap cost grows with examples × resamples. Very large datasets (100k+ examples) will be slow. Lower `bootstrap_samples` if needed.

## Data and formats

- Only JSON and JSONL datasets are supported. No CSV or Parquet yet.
- The whole dataset is loaded into memory.
- Means cover **scored examples only**. Failed examples are counted separately (`n_errors`), and `osel check` treats an increase in failures as a regression.
- Run-record and dataset schemas are version 1 and may change before 1.0. Changes will be listed in the changelog.

## Python execution

- Systems run one example at a time, in-process. There is no parallelism, timeouts or retries.
- If two configs in the same Python process use modules with the same name from different folders, Python's module cache returns the first one. The CLI runs one config per process, so this only affects library use.

## Platform and distribution

- Tested on Linux, macOS and Windows with Python 3.10–3.13 in CI.
- Not yet published to PyPI. Install from source.
- There is no plugin system, web UI or hosted service, by design for now.
