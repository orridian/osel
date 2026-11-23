# Strategy

## Problem

Evaluation results in ML, LLM and data-pipeline work are often produced by one-off scripts that lose the dataset version,
configuration and environment. Results then cannot be reproduced, comparisons are unreliable, and regressions reach users.

## Audience (initial)

Individual developers and small teams who already evaluate something (a model, prompt, function or pipeline) with scripts and want
reproducibility and CI regression checks **without adopting a platform**.

## Differentiation hypothesis (to be validated with interviews)

See [operations/competitor-matrix.md](operations/competitor-matrix.md).

1. **Local-first and file-based.** JSON/JSONL in, JSON out, nothing hosted.
2. **Evidence travels with results.** Every run records dataset identity, config, metric versions and environment.
3. **Honest comparisons.** Incompatible runs are refused; uncertainty intervals are shown with their assumptions.
4. **CI-native.** Stable exit codes and explicit thresholds.

## Distribution approach

- Useful technical proof: worked examples and a reproducible case study.
- Integrations where people already work (GitHub Actions, plain Python scripts).
- Targeted, respectful outreach to people who have publicly described this pain.

## Risks

See the full [risk register](operations/risk-register.md). Top three: wrong problem, too much scope, no distribution.

## Decision gates

| Gate | Evidence required | Decision |
|---|---|---|
| G1 — Problem validated | ≥ 8 discovery conversations, ≥ 4 describing concrete, recurring pain | Continue Product A, or narrow/change the problem |
| G2 — Alpha usable | An independent tester completes the documented workflow without help | Open alpha testing |
| G3 — Retention signal | ≥ 3 alpha users run evaluations in more than one week | Invest in CI integration and docs |
| G4 — First stable | Release policy criteria met; no open P0 bugs | Publish 1.0 |

## Expansion gate

A new product line (B, C or other) may start **only when all are true**:

- several independent users have requested the capability;
- the use case is documented;
- there is an owner other than the founder, or a credible plan to recruit one;
- maintenance costs are understood;
- Product A's reliability will not be harmed;
- the expansion has a measurable success criterion.
