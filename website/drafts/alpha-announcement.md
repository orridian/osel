---
layout: ../../layouts/Post.astro  # valid once moved to src/pages/blog/
title: "osel 0.1.0a1: first public alpha"
date: "2027-01-01"
summary: "The first public alpha of osel, an early access program, and what we're asking testers for."
draft: true
---

> **Draft.** Publish (remove `draft: true`, set the real date) only when the release is tagged and the repository is public.

Today we're releasing **osel 0.1.0a1**, the first public alpha of a small command-line tool and Python library for evaluation results you can reproduce, compare and gate in CI.

## What it does

You define an evaluation (a dataset plus either a predictions file or a Python function, plus metrics). osel runs it and saves a run record with the dataset's content hash, the config (secrets redacted), metric versions, environment and git commit. You can then:

- **compare** two runs with paired confidence intervals. osel refuses the comparison if the dataset or a metric changed;
- **check** for regressions in CI with explicit thresholds, including examples that newly fail.

Three short [demonstrations](https://github.com/orridian/osel/tree/main/examples/demos) show reproducibility, regression detection, and why an average alone can mislead.

## What it is not (yet)

It's an alpha. It isn't on PyPI yet, file formats may change, and there's no hosted service. Configs can run Python code and there is **no sandbox**, so only run configs you trust. The full list is in Known limitations in the docs.

## We're looking for testers

If you evaluate models, prompts or pipelines with scripts, we'd value an hour of your time: install it, run the quick start or your own data, and tell us where it got in the way. Feedback goes through the "Alpha feedback" issue form on GitHub.

We'll report what we learn, including what didn't work.
