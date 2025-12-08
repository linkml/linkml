# Claude Code Notes for LinkML

## Project Structure

This is a UV workspace monorepo that publishes **two PyPI packages**:

| Package | Source | Tests | PyPI |
|---------|--------|-------|------|
| `linkml` | `packages/linkml/src/linkml/` | `tests/linkml/` | [linkml](https://pypi.org/project/linkml/) |
| `linkml-runtime` | `packages/linkml_runtime/src/linkml_runtime/` | `tests/linkml_runtime/` | [linkml-runtime](https://pypi.org/project/linkml-runtime/) |

All commands use `uv run` prefix (e.g., `uv run pytest`).

## Task-Specific Guides

| Task | Guide |
|------|-------|
| Code coverage reports | [.claude/coverage.md](.claude/coverage.md) |

## Best Practices

1. **Check CI first** - When something doesn't work locally, check `.github/workflows/main.yaml` to see how CI handles it. CI often uses external services or has workarounds for local limitations.

2. **Use `uv run`** - Always prefix commands with `uv run` to ensure the correct environment.
