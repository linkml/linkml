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

* Check CI first - When something doesn't work locally, check `.github/workflows/main.yaml` to see how CI handles it. CI often uses external services or has workarounds for local limitations.
* Use `uv run` - Always prefix commands with `uv run` to ensure the correct environment.
* Use doctests liberally—these serve as both explanatory examples for humans and as unit tests
* For longer examples, write pytest tests
* always write pytest functional style rather than unittest OO style
* use modern pytest idioms, including `@pytest.mark.parametrize` to test for combinations of inputs
* NEVER write mock tests unless requested. I need to rely on tests to know if something breaks
* For tests that have external dependencies, you can do `@pytest.mark.integration`
* Do not "fix" issues by changing or weakening test conditions. Try harder, or ask questions if a test fails.
* Avoid try/except blocks, these can mask bugs
* Failing fast is a good principle
* Follow the DRY principle
* Avoid repeating chunks of code, but also avoid premature over-abstraction
* Declarative principles are favored
* Always use type hints, always document methods and classes
* always use pytest, never unittest