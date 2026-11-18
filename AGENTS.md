# Claude Code Notes for LinkML

## Project Structure

This is a UV workspace monorepo that publishes **two PyPI packages**:

| Package | Source | Tests | PyPI |
| `linkml` | `packages/linkml/src/linkml/` | `tests/linkml/` | [linkml](https://pypi.org/project/linkml/) |
| `linkml-runtime` | `packages/linkml_runtime/src/linkml_runtime/` | `tests/linkml_runtime/` | [linkml-runtime](https://pypi.org/project/linkml-runtime/) |

All commands use `uv run` prefix (e.g., `uv run pytest`).

## Best Practices

* Read `.github/workflows/main.yaml` when something doesn't work locally - CI often has workarounds or uses external services that explain expected behavior.
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
* Optional dependencies are the documented exception to the two rules above. Guard the import, not the spec: `try: import x` / `except ImportError as exc: raise ImportError("x is required. Install with: pip install 'linkml[extra]'") from exc` - see `generators/bigquerygen.py`. `importlib.util.find_spec` raises under the test fixture below, which hides your message.
* Testing that an optional dependency is absent is not a mock test: use the `mock_missing_import` fixture in `tests/conftest.py`. Do not build isolated environments in CI for this.
* Follow the DRY principle
* Avoid repeating chunks of code, but also avoid premature over-abstraction
* Declarative principles are favored
* Always use type hints, always document methods and classes
* always use pytest, never unittest
