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
# Download latest metamodel files
METAMODEL_DIR="tests/linkml/test_metamodel_compat/input/metamodel"
BASE_URL="https://raw.githubusercontent.com/linkml/linkml-model/main/linkml_model/model/schema"

for file in meta.yaml types.yaml mappings.yaml extensions.yaml annotations.yaml units.yaml; do
  curl -sSL "${BASE_URL}/${file}" -o "${METAMODEL_DIR}/${file}"
done

# Update imports to use local paths
sed -i '' 's/- linkml:types/- types/g' "${METAMODEL_DIR}"/*.yaml
sed -i '' 's/- linkml:mappings/- mappings/g' "${METAMODEL_DIR}"/*.yaml
sed -i '' 's/- linkml:extensions/- extensions/g' "${METAMODEL_DIR}"/*.yaml
sed -i '' 's/- linkml:annotations/- annotations/g' "${METAMODEL_DIR}"/*.yaml
sed -i '' 's/- linkml:units/- units/g' "${METAMODEL_DIR}"/*.yaml

# Run tests
uv run pytest tests/linkml/test_metamodel_compat/ --with-slow -v
```

Note: On Linux, use `sed -i` instead of `sed -i ''`.

## File Structure

```
test_metamodel_compat/
├── README.md                      # This file
├── __init__.py
├── conftest.py                    # metamodel_path fixture
├── test_metamodel_projectgen.py   # Main test file
└── input/
    └── metamodel/
        ├── meta.yaml              # Main metamodel schema
        ├── types.yaml             # Type definitions
        ├── mappings.yaml          # Mapping definitions
        ├── extensions.yaml        # Extension mechanisms
        ├── annotations.yaml       # Annotation system
        └── units.yaml             # Unit definitions
```
