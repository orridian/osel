# Trustworthy evaluation results
### in 90 minutes
OSEL workshop · osel alpha · Code of Conduct applies

---

## A familiar story
"v2 scores 0.82, v1 scored 0.80 — ship it!"
- Which data? Which config? Which metric code?
- Is +0.02 real, or noise?

---

## Three ways results go wrong
1. **Lost context.** You can't reproduce the number later.
2. **Changed ground.** The dataset or metric changed between runs.
3. **Noise read as signal.** Small test sets swing a lot.

---

## What a trustworthy result carries
- Dataset identity (a content hash)
- Config and metric versions
- Environment and code commit
- Per-example scores, not just an average
- An uncertainty interval, with its assumptions

---

## Paired comparisons
- Compare the **same examples** in both runs
- Bootstrap the mean per-example difference
- A CI that includes 0 means you can't distinguish the change from noise at this confidence level

---

## Limitations (honestly)
- Small n means wide, unreliable intervals
- Examples are assumed independent
- Many metrics mean some "differences" by chance
- Statistics don't decide what *matters*. You do.

---

## Exercise time
Open the participant guide → Exercise 1

---

## Gate it in CI
`osel check --baseline baseline.json --current current.json --max-drop exact_match=0.01`
Exit 0 ok · 1 regression · 2 invalid input · 3 bug

---

## Next steps
- Try it on your own evaluation
- Good first issues in the repository
- Feedback form (2 minutes). Thank you!
