# Test Structure After Merge

After merging linkml-runtime into the main linkml repository, the test structure has been reorganized:

## Directory Structure

```
tests/
├── conftest.py              # Main conftest for all tests
├── __init__.py             
├── linkml/                  # LinkML core tests
│   ├── test_base/
│   ├── test_compliance/
│   ├── test_data/
│   ├── test_generators/
│   ├── test_issues/
│   ├── test_linter/
│   ├── test_notebooks/
│   ├── test_prefixes/
│   ├── test_scripts/
│   ├── test_transformers/
│   ├── test_utils/
│   ├── test_validation/
│   ├── test_validator/
│   ├── test_workspaces/
│   └── utils/              # Shared utilities for linkml tests
└── linkml_runtime/         # Runtime tests (from linkml-runtime repo)
    ├── test_enumerations/
    ├── test_index/
    ├── test_issues/
    ├── test_linkml_model/
    ├── test_loaders_dumpers/
    ├── test_processing/
    ├── test_utils/
    └── support/            # Shared utilities for runtime tests
```

## Running Tests

### Using pytest directly:

```bash
# Run all tests
uv run pytest tests/

# Run only LinkML tests
uv run pytest tests/linkml/

# Run only Runtime tests  
uv run pytest tests/linkml_runtime/

# With options
uv run pytest tests/ --with-slow --with-network

# With coverage
uv run coverage run -m pytest tests/
uv run coverage report
```

### Using the helper script:

```bash
# Run all tests
./run_tests.sh all

# Run LinkML tests only
./run_tests.sh linkml

# Run Runtime tests only
./run_tests.sh runtime

# With options
./run_tests.sh all --with-slow --with-network --coverage
```

## Import Changes

After the merge, imports have been updated:

- LinkML test imports: `from tests.utils.X` → `from tests.linkml.utils.X`
- Runtime test imports: `from tests.support.X` → `from tests.linkml_runtime.support.X`
- Compliance imports: `from tests.test_compliance.X` → `from tests.linkml.test_compliance.X`
- All other test module imports follow the same pattern

## GitHub Workflow Commands

For your GitHub Actions workflows, use:

```yaml
# Run all tests with coverage
- run: uv run coverage run -m pytest tests/ --with-slow --with-network
- run: uv run coverage xml
- run: uv run coverage report -m

# Run specific test suites
- run: uv run pytest tests/linkml/ --with-slow --with-network
- run: uv run pytest tests/linkml_runtime/ --with-slow --with-network
```

## Known Issues Fixed

1. **Import paths**: All imports updated to reflect new structure
2. **Conftest duplication**: Merged into single conftest.py at tests/ level
3. **Circular imports**: Fixed in linkml_runtime environment.py
4. **Missing dependencies**: Added `docker` and `testcontainers` to dev dependencies

## Configuration

- pytest configuration in `pyproject.toml`
- Coverage configuration in `pyproject.toml`
- Test markers defined for slow, network, and other test categories