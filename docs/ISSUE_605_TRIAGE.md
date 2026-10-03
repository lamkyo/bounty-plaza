# Issue #605 — Triage Note

## Summary

Issue #605 requests transpiling the **tg-station** codebase (BYOND / Dream Maker)
to TypeScript so it can run in stock Chromium.

## Assessment

**Out of scope for this repository.**

This repository (`bounty-plaza`) is a bounty aggregation platform consisting of:

- Python CLI scripts (`scripts/`)
- GitHub Actions workflows (`.github/workflows/`)
- Documentation and reward policy files

The tg-station source tree (`.dm` files, Dream Maker code) is **not present**
in this repository, so no transpilation work can be performed here.

## Recommended Action

- Close the issue as `not-planned` / `out-of-scope`, or
- Re-file it against the actual repository (`Iamgoofball/-tg-station`).

No code changes are required in `bounty-plaza` for this issue.
