# Metrics

## Built-in metrics

| Name | Version | Better | Definition |
|---|---|---|---|
| `exact_match` | 1 | higher | 1 if prediction == reference. Strings are compared after stripping whitespace; `normalize: true` also lower-cases and collapses spaces |
| `contains` | 1 | higher | 1 if the (normalized) reference string appears in the prediction |
| `token_f1` | 1 | higher | Token-overlap F1 over lower-cased whitespace tokens. Both empty = 1 |
| `abs_error` | 1 | lower | \|prediction − reference\| for numeric values |

All built-ins need a `reference`. Examples without one are recorded as metric errors, not silently skipped.

## Writing a custom metric

A metric is any object with `name`, `version`, `higher_is_better` and `score(prediction, example) -> float`:

```python
# my_metrics.py
from osel.errors import MetricError

class WithinTolerance:
    version = "1"              # bump when scoring logic changes!
    higher_is_better = True

    def __init__(self, tolerance: float = 1e-9, name: str = "within_tolerance"):
        self.tolerance = tolerance
        self.name = name

    def score(self, prediction, example) -> float:
        if not example.has_reference:
            raise MetricError("needs a reference")   # recorded per example, run continues
        return float(abs(float(prediction) - float(example.reference)) <= self.tolerance)
```

```yaml
python_path: ["."]
metrics:
  - use: "my_metrics:WithinTolerance"
    params: { tolerance: 0.001 }
```

Rules:

- Return a finite number. `NaN`, infinity and non-numbers are recorded as errors.
- Raise `MetricError` for "cannot score this example". Any other exception is also caught and recorded.
- **Bump `version`** whenever behavior changes. `osel compare` will then refuse to compare the old and new runs. This is intentional.

A complete working example is in `examples/function-eval/`.

## Plugin API

There is no plugin/extension registry yet. It will be designed once real use cases emerge (see the roadmap).
