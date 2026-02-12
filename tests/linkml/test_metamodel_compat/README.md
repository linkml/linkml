# Metamodel Compatibility Tests

This test suite validates that the LinkML toolkit can successfully process the LinkML metamodel from [linkml-model](https://github.com/linkml/linkml-model).

## Why This Test Exists

The LinkML toolkit and the LinkML metamodel are developed in separate repositories:
- **linkml** (this repo): The toolkit that processes schemas
- **linkml-model**: The metamodel that defines the LinkML schema language itself

Changes to either repository can break compatibility. These tests catch such issues by running the full `ProjectGenerator` suite against a copy of the metamodel.

## How It Works

1. The test uses a **hardcoded copy** of the metamodel files in `input/metamodel/`
2. `test_metamodel_projectgen` runs `ProjectGenerator` and verifies key outputs (SQL, OWL, docs, JSON Schema)
3. `test_metamodel_python_compiles` verifies the generated Python code has no syntax errors

### Excluded Generators

Some generators are excluded due to known limitations with the metamodel:
- **shacl**: Doesn't support special ifabsent functions (e.g., `default_range`)
- **excel**: Metamodel has no tree_root classes, creating an empty workbook

## Connection to GitHub Actions

The workflow `.github/workflows/metamodel-compat.yaml` runs weekly (Mondays 9:00 UTC) and:

1. Downloads the **latest** metamodel files from linkml-model
2. Runs these compatibility tests against the fresh download
3. On **failure**: Creates/updates a GitHub issue with label `metamodel-compat`
4. On **success**: Creates a PR to update the hardcoded metamodel fixtures

This ensures we detect breaking changes in either direction and keep the test fixtures current.

## Running Locally

### Prerequisites

```bash
# From the repository root
uv sync --all-groups
```

### Run the tests

```bash
# These are slow tests (~30 seconds), so they require --with-slow
uv run pytest tests/linkml/test_metamodel_compat/ --with-slow -v
```

### Update metamodel fixtures manually

To test against the latest metamodel locally:

```bash
# Download from main (default)
make download-metamodel

# Or download from a specific branch/tag
make download-metamodel LINKML_MODEL_BRANCH=1.10.0-rc4

# Run tests
uv run pytest tests/linkml/test_metamodel_compat/ --with-slow -v
```

The `download-metamodel` Makefile target performs a shallow clone of the
[linkml-model](https://github.com/linkml/linkml-model) repository, copies all
schema YAML files, and rewrites `linkml:` import prefixes to local relative
paths. This automatically picks up any new schema files added to the metamodel.

## File Structure

```
test_metamodel_compat/
├── README.md                      # This file
├── __init__.py
├── conftest.py                    # metamodel_path fixture
├── test_metamodel_projectgen.py   # Main test file
└── input/
    └── metamodel/
        └── *.yaml                 # Schema files from linkml-model
```

The set of YAML files in `input/metamodel/` mirrors the contents of
`linkml_model/model/schema/` in the linkml-model repository. The entry point is
`meta.yaml`; all other files are imported from it.
