# OSEL documentation

`osel` lets you **define** an evaluation, **run** it, **preserve** exactly what produced the result, **compare** it with a baseline, and **reproduce or inspect** it later.

!!! note "Status"
    Alpha (`0.1.0.dev0`). The CLI and file formats may change before 1.0. Every change is listed in the changelog.

| I want to… | Read |
|---|---|
| Install or upgrade | [Installation](installation.md) |
| Try it in 2 minutes | [Quick start](quickstart.md) |
| Know what it can't do yet | [Known limitations](known-limitations.md) |
| Understand runs, identity and comparisons | [Concepts](concepts.md) |
| Prepare my data | [Dataset schema](dataset-schema.md) |
| Write a config | [Evaluation config](config.md) |
| Add my own metric | [Metrics](metrics.md) |
| Know what the confidence intervals mean | [Statistics](statistics.md) |
| Block regressions in CI | [CI integration](ci-integration.md) |

**Design principles:** local-first · plain JSON files · no telemetry · refuse misleading comparisons · stable exit codes.
