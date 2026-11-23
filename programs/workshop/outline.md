# Workshop outline

**Duration:** 90 minutes · **Format:** online or in person · **Size:** ≤ 20 participants per moderator

## Learning objectives

By the end, participants can:

1. explain why a single accuracy number without data/config/version context can't be trusted;
2. validate a dataset and run a recorded evaluation with osel;
3. read a paired confidence interval and say whether a change is distinguishable from noise;
4. add a regression check to CI with an explicit threshold.

## Prerequisites

Python 3.10+, git, a terminal. Basic Python. Setup steps are sent 3 days before.

## Agenda

| Min | Segment | Activity |
|---|---|---|
| 0–10 | Welcome, CoC, recording notice | Moderator introduces the Code of Conduct and the recording opt-out |
| 10–25 | Why results go wrong | Slides 1–6 |
| 25–45 | **Exercise 1:** validate and run | Participant guide, Ex. 1 |
| 45–65 | **Exercise 2:** compare and interpret | Ex. 2. Discuss "CI includes 0" |
| 65–80 | **Exercise 3:** custom metric + CI gate | Ex. 3 |
| 80–90 | Wrap-up, feedback form, next steps | |

## Instructor notes

- Do a dry run on a clean machine 48 hours before.
- Common blockers: PATH not set after `pip install` on Windows (use `python -m osel`); old Python versions.
- Emphasize the limitation: n = 10 in the examples is deliberately too small.
- Don't promise features on the roadmap; point to the roadmap page.

## Counting (METRICS.md)

Report **registered**, **attended** and **completed** separately. *Completed* = finished Exercise 2, confirmed by a pasted `osel compare` output or the moderator's check.
