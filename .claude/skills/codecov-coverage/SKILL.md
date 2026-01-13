---
name: codecov-coverage
description: Fetch and analyze code coverage from Codecov API for the linkml project. Use when checking coverage before making a PR, analyzing coverage changes, or finding low-coverage files.
allowed-tools: WebFetch, Bash
---

# Codecov Coverage Skill

Fetch and analyze code coverage data from Codecov for the LinkML project.

## When to Use This Skill

- Before creating a PR: check that coverage won't decrease
- When adding new code: identify if new files need tests
- When asked about test coverage or low-coverage areas

## Coverage Expectations

**PRs must not decrease coverage.** The CI will flag coverage decreases.

When adding new code:
- New modules should target >80% coverage
- New public functions need at least one test

## How to Check Coverage

### Quick overall percentage
Use WebFetch on:
```
https://codecov.io/gh/linkml/linkml/branch/main/graph/badge.txt
```
Returns plain text like "80%"

### Detailed totals (lines, hits, misses)
Use WebFetch on:
```
https://api.codecov.io/api/v2/github/linkml/repos/linkml/totals
```
Returns JSON with files count, lines, hits, misses, coverage percentage

### File-level coverage report
Use WebFetch on:
```
https://api.codecov.io/api/v2/github/linkml/repos/linkml/report
```
Returns per-file coverage data - useful for finding low-coverage files

## Why Local Coverage Fails

The UV workspace + src layout breaks local coverage. The `.coveragerc` specifies `source = linkml` but packages live at `packages/linkml/src/linkml/`. Use the Codecov API instead.

## Known Low-Coverage Areas

These areas currently have low coverage and may need tests:
- `generators/rustgen/` - experimental
- `generators/dotgen.py` - ~47%
- `converter/cli.py` - ~53%
- `workspaces/` - minimal coverage
