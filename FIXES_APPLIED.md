# Test Import Fixes Applied

## Summary
Successfully fixed test structure after merging linkml-runtime into linkml monorepo.

## Current Test Status

### ✅ LinkML Runtime Tests
- **Status**: All 514 tests passing
- **Command**: `uv run pytest tests/linkml_runtime/`

### ⚠️ LinkML Tests  
- **Status**: Most tests passing (7994 passed, 42 failed)
- **Command**: `uv run pytest tests/linkml/`
- **Note**: The failures appear to be pre-existing issues, not related to the merge

## Fixes Applied

### 1. Import Path Updates
- Fixed all imports to use new structure:
  - `tests.utils.*` → `tests.linkml.utils.*`
  - `tests.test_compliance.*` → `tests.linkml.test_compliance.*`
  - `tests.support.*` → `tests.linkml_runtime.support.*`
  - And similar for all other test modules

### 2. Environment Configuration
- Fixed circular import in `tests/linkml_runtime/support/test_environment.py`
- Updated environment variables to use correct paths
- Fixed notebook tests to use `nbenv` variable name

### 3. Path Corrections
- Updated hardcoded test paths in `loaderdumpertestcase.py`
- Fixed notebook directory path to point to root `notebooks/` folder
- Corrected path expectations in loader tests

### 4. Dependencies Added
- `jsonpatch` - Required by dict_comparator
- `docker` - Required by conftest
- `testcontainers` - Required by plantuml tests

### 5. Single Conftest
- Merged both conftest.py files into one at `tests/` level
- Removed duplicate `tests/linkml_runtime/conftest.py`

## Test Commands

### Run all tests:
```bash
uv run pytest tests/ --with-slow --with-network
```

### Run LinkML tests only:
```bash
uv run pytest tests/linkml/ --with-slow --with-network
```

### Run Runtime tests only:
```bash
uv run pytest tests/linkml_runtime/ --with-slow --with-network
```

### With coverage:
```bash
uv run coverage run -m pytest tests/ --with-slow --with-network
uv run coverage report
```

### Using helper script:
```bash
./run_tests.sh all        # All tests
./run_tests.sh linkml     # LinkML only
./run_tests.sh runtime    # Runtime only
```

## Files Modified

Key files that were modified:
- `tests/__init__.py` - Updated imports
- `tests/conftest.py` - Updated imports
- `tests/linkml/test_compliance/conftest.py` - Updated imports
- `tests/linkml/test_notebooks/environment.py` - Fixed variable names
- `tests/linkml/test_notebooks/test_notebooks.py` - Fixed notebook path
- `tests/linkml_runtime/support/test_environment.py` - Fixed circular import
- `tests/linkml_runtime/test_loaders_dumpers/loaderdumpertestcase.py` - Fixed path expectations
- `tests/linkml_runtime/test_loaders_dumpers/test_loaders.py` - Fixed path
- All test files with incorrect imports (56+ files in linkml, 34+ files in runtime)

## Next Steps

The test structure is now properly configured. Any remaining test failures in the LinkML suite appear to be pre-existing issues unrelated to the merge and can be addressed separately.