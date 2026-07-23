# Claude Code Notes for LinkML

## Project Structure

This is a UV workspace monorepo that publishes **two PyPI packages**:

| Package | Source | Tests | PyPI |
| `linkml` | `packages/linkml/src/linkml/` | `tests/linkml/` | [linkml](https://pypi.org/project/linkml/) |
| `linkml-runtime` | `packages/linkml_runtime/src/linkml_runtime/` | `tests/linkml_runtime/` | [linkml-runtime](https://pypi.org/project/linkml-runtime/) |

## Testing

Use Makefile targets (✅) instead of ad-hoc pytest commands. CI mirrors these targets for local-CI symmetry.

| Target | Scope | Example with custom path |
|---|---|---|
| `make test-linkml` | Fast tests for `linkml` package | `make test-linkml TEST_PATH=tests/linkml/test_compliance/` |
| `make test-linkml-runtime` | Fast tests for `linkml-runtime` package | `make test-linkml-runtime TEST_PATH=tests/linkml_runtime/test_foo.py` |
| `make test` | Both fast targets (linkml + runtime) | — |
| `make test-slow` | Slow-marked tests only | `make test-slow TEST_PATH=tests/linkml/test_biolink/` |
| `make test-all` | Fast + slow, no duplication | — |
| `make test-branch` | Auto-detect changed package(s) and run their fast tests | — |

**Flags** — append via `PYTEST_FLAGS`:
- `make test PYTEST_FLAGS="-n auto"` — parallel execution
- `make test PYTEST_FLAGS="-x --tb=short"` — stop on first failure, short traceback
- `make test COVERAGE=true` — wrap with coverage.py (matches CI)

Default `PYTEST_FLAGS` skips `tests/linkml/test_notebooks` (notebooks mutate the shared venv and always fail locally).

### Workflow

1. **Run `make test-branch`** — auto-detects which package(s) changed vs `main` and runs their fast tests with `-n auto`. Always leave at least 2 cores free: set `-n $(python -c "import os; print(max(1, os.cpu_count()-2))")`.
2. **If tests fail**, run only the failing tests:
   `make test-linkml TEST_PATH=<path> PYTEST_FLAGS="-x --tb=short -n $(python -c "import os; print(max(1, os.cpu_count()-2))")"`
3. **Once failing tests pass**, re-run the full fast suite for the affected package(s):
   `make test-linkml` (and/or `make test-linkml-runtime`)
4. **When fast tests are green**, run slow tests:
   `make test-slow PYTEST_FLAGS="-n $(python -c "import os; print(max(1, os.cpu_count()-2))")"`

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
* Follow the DRY principle
* Avoid repeating chunks of code, but also avoid premature over-abstraction
* Declarative principles are favored
* Always use type hints, always document methods and classes
* always use pytest, never unittest
