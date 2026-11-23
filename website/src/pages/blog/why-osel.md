---
layout: ../../layouts/Post.astro
title: "Why we're building osel"
date: "2026-11-11"
summary: "The problem OSEL starts with, what exists today, and what we don't know yet."
---

Most evaluation results are produced by scripts that throw away the context needed to trust them: which version of the data was used, which config, which metric code, which environment. When a number changes, it's hard to tell whether the system got better, the data changed, or the result is just noise.

## What exists today

`osel` is an **alpha** command-line tool and Python library. It can:

- validate a JSON/JSONL dataset and compute a content-based identity for it;
- run an evaluation from a predictions file or a Python function;
- save a run record with the config (secrets redacted), metric versions and environment;
- compare two runs with paired bootstrap confidence intervals, and refuse comparisons when the dataset or metric version changed;
- fail a CI job when a metric regresses beyond a threshold you set.

## What we don't know yet

We haven't yet validated that this is the most painful problem for our intended users. We're doing that through conversations with people who evaluate software. **There are no external users yet.** When that changes, we'll say so, with evidence.

## Limitations

The statistics are deliberately simple (a percentile bootstrap) and come with stated assumptions. They are unreliable on small datasets, and osel warns when that's the case. There is no hosted service and no telemetry.

If this matches a problem you have, we would like to hear about your workflow. The Community page (linked below) explains how to reach us.
