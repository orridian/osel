# Technical demonstrations

Three short, reproducible demonstrations of why osel exists. Every output shown here is real, and `tests/test_demos.py` checks the claims in CI.

| Demo | Shows | Folder |
|---|---|---|
| 1. Reproducibility | Same data + config + metric versions → identical results; changed data → comparison refused | [01-reproducibility](01-reproducibility/README.md) |
| 2. Regression detection | A threshold catches a degraded system, including examples that started *failing* | [02-regression](02-regression/README.md) |
| 3. Statistical uncertainty | The same +5-point gain is noise on 40 examples but clear on 400 | [03-uncertainty](03-uncertainty/README.md) |
