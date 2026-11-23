# Competitor matrix

> **Unverified starting point.** The blueprint refers to six projects "listed in the earlier strategy", which is not in this repo. These six are candidates. Verify every cell against each project's current docs and repository, and add a source link and date, before using any of it publicly or in decisions. Do not publish claims about other projects without sources.

| Project | Primary focus (to verify) | Local-first? | Dataset identity / versioning? | Run comparison? | CI regression gate? | Uncertainty reporting? | Source + date checked |
|---|---|---|---|---|---|---|---|
| OpenAI Evals | LLM eval framework and registry | | | | | | |
| EleutherAI lm-evaluation-harness | Standard LLM benchmark harness | | | | | | |
| promptfoo | Prompt/LLM testing, CLI + CI | | | | | | |
| DeepEval | LLM evaluation in pytest style | | | | | | |
| UK AISI Inspect | LLM evaluation framework | | | | | | |
| MLflow (evaluate / tracking) | Experiment tracking with eval features | | | | | | |

## Questions to answer per project

1. Who is it for, and which workflow does it fit?
2. What does it record about a run, and can someone else reproduce the result?
3. Does it refuse or flag incompatible comparisons?
4. How does it express uncertainty?
5. Setup cost: install only, or an account/server?

## Differentiation hypothesis (test in interviews; don't assume)

osel is not a benchmark suite or an LLM-specific framework. It is a small, general, file-based *record / compare / gate* layer that could sit **alongside** these tools. If interviews show people already have this solved, record that in the decision log and revisit the problem (gate G1).
