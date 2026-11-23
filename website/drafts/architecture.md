---
layout: ../../layouts/Post.astro  # valid once moved to src/pages/blog/
title: "How osel is built, and why it's so small"
date: "2027-01-08"
summary: "Engineering decisions behind osel: plain files, one dependency, refusing bad comparisons, and testing the statistics."
draft: true
---

> **Draft.** Review and publish after the alpha announcement.

osel has one runtime dependency (PyYAML), stores everything as JSON files, and has about ten modules. That's deliberate.

## Plain files instead of a server

Runs are JSON files in `.osel/runs/`, or wherever you write them. You can diff them, commit a baseline next to your code, and read them without osel. A database or service would add setup cost before we know anyone needs it.

## Identity before numbers

Every dataset gets a content hash that ignores row order and formatting but changes when any example changes. Every metric has a version. `osel compare` refuses to compare runs whose dataset identity or metric versions differ. We think a loud refusal is better than a quiet, misleading number.

## Failures count

A mean only covers examples that could be scored. Our own launch audit found that, as first written, a system crashing on half its inputs would pass `osel check`. Now an increase in failed examples is a regression in its own right. The bug and fix are in the changelog.

## Statistics we can defend

We use a seeded percentile bootstrap for intervals and a paired bootstrap for comparisons. There are no p-values and no "significant" labels. The implementation is tested against Python's `statistics` module, and its assumptions and limitations are documented next to it.

## Exit codes are an API

`0` ok, `1` regression, `2` invalid input, `3` internal error. CI systems depend on these, so they're stable from the first release.

## What we left out on purpose

A plugin system, a web UI, accounts, telemetry and a leaderboard. Each might make sense later, once real users ask for it.
