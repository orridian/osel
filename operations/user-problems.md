# Candidate user problems (testable)

Each is written so an interview can confirm or reject it. **Evidence for** = the person describes a specific recent instance, a workaround, and a cost.

| # | Candidate problem | Who | Confirming evidence | Rejecting evidence |
|---|---|---|---|---|
| 1 | After changing a model/prompt, developers can't tell whether a metric change is real or noise | ML/LLM developers | Recent example of a mistaken "improvement"; no uncertainty estimate used | They already use CIs or a large enough test set |
| 2 | Evaluation results can't be reproduced weeks later because the dataset version or config was not recorded | Researchers, ML engineers | A recent failed reproduction; time lost | Experiment tracker already captures all of it |
| 3 | Quality regressions reach main because CI doesn't run evaluations | Teams shipping LLM features | A regression found by users or late QA | Evals already gate merges |
| 4 | Comparing runs across a silently changed test set gives misleading conclusions | Teams with evolving eval sets | An incident caused by dataset drift | Test sets are frozen and versioned |
| 5 | Evaluation scripts are one-off and copied between projects | Individual developers | ≥ 2 projects with copied eval code | A shared internal library exists |
| 6 | Existing eval tools need an account, server or heavy framework that is too much for small projects | Solo devs, students, small labs | Abandoned a tool due to setup cost | Setup cost is not a factor |
| 7 | Per-example failures are hidden behind an average, slowing debugging | Developers debugging models | Time spent finding which examples broke | They already inspect per-example diffs easily |
| 8 | Reviewers can't verify the evaluation claims in a PR | Code reviewers, tech leads | PR approved on an unverifiable number | Results are attached and reproducible |
| 9 | Researchers report a single run without variance, and reviewers object | Academic researchers | Reviewer comments requesting variance | Tooling already handles repeats |
| 10 | Secrets or private data leak into saved experiment logs | Anyone logging configs | A past leak or near miss | Logs are already scrubbed |

After 8+ conversations, rank the problems by frequency × severity in the decision log (gate G1).
