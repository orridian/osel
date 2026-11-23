# 75-second demo video script

**Goal:** show the problem first, then the workflow. A terminal with large font (≥ 20pt), recorded at 1080p. Add captions (accessibility policy).

| Time | On screen | Narration |
|---|---|---|
| 0:00–0:10 | Two numbers: "v1: 0.80 · v2: 0.82" | "You changed your model and the score went up. But is that real? Same data? Same metric? Could it be noise?" |
| 0:10–0:20 | `osel dataset validate data.jsonl` → VALID + identity | "osel starts by fingerprinting your dataset. Change one example and the fingerprint changes." |
| 0:20–0:35 | `osel eval run config.yaml -o baseline.json`, results table | "Each run is saved with exactly what produced it: data fingerprint, config, metric versions, environment, git commit. Secrets are redacted." |
| 0:35–0:50 | `osel compare baseline.json current.json`: DEGRADED (CI includes 0) | "Compare two runs and you get the difference *and* how sure you can be. Here, 10 examples aren't enough to tell, and osel says so." |
| 0:50–1:05 | `osel check ...`, CHECK FAILED, `echo $?` → 1 | "In CI, osel check fails the build when a metric drops past your threshold, or when examples start failing." |
| 1:05–1:15 | README + "alpha · looking for testers" | "osel is an open-source alpha. If you evaluate models or pipelines, try it and tell us what got in the way." |

**Recording checklist:** clean terminal (no usernames or paths with personal info), the quickstart example only, and output that matches the docs exactly.
