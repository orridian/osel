# Vision

> Everything below Product A is a **hypothesis / roadmap item**, not an existing product.

## Long-term picture

A small family of local-first tools that make engineering evidence trustworthy: evaluations you can reproduce, test results you can compare, and benchmarks that say exactly what was measured.

| Product | Status | Intended users | Hypothesis |
|---|---|---|---|
| **A — `osel` evaluation toolkit** | Alpha (in development) | Developers and researchers evaluating models, prompts, functions or pipelines | People will adopt a lightweight CLI/SDK that records and compares evaluation runs if it fits into scripts and CI with almost no setup. |
| **B — Developer Reliability Infrastructure** | Planned (gated) | Teams with flaky or slow test suites | Teams want transparent cross-run test-result comparison and failure grouping. Start **only** after Product A users ask for adjacent reliability features. |
| **C — Benchmark & Reproducibility Ecosystem** | Planned (gated) | Researchers and tool authors publishing performance claims | A versioned benchmark spec, plus labels separating self-submitted from independently reproduced results, would improve trust in published numbers. |

Products B and C may start only when the [expansion gate](STRATEGY.md#expansion-gate) is met. Their first-module outlines are kept in
[programs/product-b-c-gated-specs.md](programs/product-b-c-gated-specs.md) so the work is ready when (and if) the gate opens.
