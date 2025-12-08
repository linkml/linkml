# Code Coverage

## Getting Coverage Reports

**Don't run coverage locally** - the UV workspace + src layout causes "No data was collected" errors.

**Use the Codecov API instead:**

```
# File-level coverage data
https://api.codecov.io/api/v2/github/linkml/repos/linkml/report

# Summary totals
https://api.codecov.io/api/v2/github/linkml/repos/linkml/totals

# Quick overall percentage
https://codecov.io/gh/linkml/linkml/branch/main/graph/badge.txt
```

## Why Local Coverage Fails

The `.coveragerc` specifies `source = linkml` but packages live at `packages/linkml/src/linkml/`. Editable installs don't map cleanly to source paths, so coverage can't trace execution back to source files.

## Current Status (Dec 2025)

**Overall: ~80%** (12,792 / 16,040 lines)

### Low Coverage Targets

| File | Coverage | Missed Lines |
|------|----------|--------------|
| `generators/dotgen.py` | 47% | 48 |
| `converter/cli.py` | 53% | 36 |
| `rustgen.py` | 18% | - |
| `workspaces.py` | 0% | - |
