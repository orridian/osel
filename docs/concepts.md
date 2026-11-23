# Concepts

**Example.** One item to evaluate: a stable `id`, an `input`, an optional `reference`, and optional `metadata`.

**Dataset identity.** A SHA-256 hash of the dataset's canonical content. Row order, key order, whitespace and JSON vs JSONL do **not** change it. Any change to an example **does**. Two runs are comparable only if their dataset identities match.

**System.** What you are evaluating. Either a predictions file (`{"id", "output"}` per line) or a Python callable that takes `input` and returns an output.

**Metric.** Scores one prediction against one example and returns a number. Each metric has a `version`. If scoring logic changes, its version changes, and old and new runs are refused as incompatible.

**Run record.** A JSON file containing everything about one run: config (secrets redacted), dataset identity, metric versions, environment (Python, OS, osel version, git commit), per-example scores and errors, and aggregates. See [run record format](run-record.md).

**Run store.** Runs are also saved to `.osel/runs/<run_id>.json`. Refer to a run by full ID, a unique prefix, `latest`, or a file path.

**Comparison.** Per-metric baseline vs current means, the delta, and a *paired* bootstrap confidence interval over the examples scored in both runs. See [statistics](statistics.md).

**Check.** A comparison plus thresholds. It exits with code `1` if any metric degraded by more than its allowed tolerance.

## Errors don't stop runs

If your system raises an exception, or a metric can't score an example, the error (type and message, without a traceback) is stored on that example, and the run continues. Aggregates report `n` (scored) and `n_errors` separately, so missing scores are never silently ignored.
