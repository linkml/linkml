# SOP: Updating linkml-model in LinkML

This Standard Operating Procedure (SOP) documents the process for updating the
vendored copy of linkml-model schemas in the linkml-runtime package.

**Related issue:** [#3076 - Update linkml to 1.10.0 and the linkml-model to 1.10.0-rc1](https://github.com/linkml/linkml/issues/3076)

## Background

### Architecture Overview

The LinkML ecosystem consists of three main components with a specific dependency relationship:

```
┌─────────────────────────────────────────────────────────────┐
│  linkml-model (github.com/linkml/linkml-model)              │
│  ─────────────────────────────────────────────────────────  │
│  • Contains source YAML schemas (meta.yaml, types.yaml, etc)│
│  • NOT published as a PyPI package                          │
│  • Releases are git tags (e.g., v1.10.0)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │  make update_model (manual sync)
                      │  packages/linkml_runtime/Makefile
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  linkml-runtime (PyPI: linkml-runtime)                      │
│  ─────────────────────────────────────────────────────────  │
│  • Schemas VENDORED into: src/linkml_runtime/linkml_model/  │
│  • Ships with frozen copy of the model                      │
│  • NO PyPI dependency on linkml-model                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │  PyPI dependency
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  linkml (PyPI: linkml)                                      │
│  ─────────────────────────────────────────────────────────  │
│  • Depends on linkml-runtime >= X.Y.Z                       │
│  • Gets model schemas transitively                          │
└─────────────────────────────────────────────────────────────┘
```

### Why Vendoring?

The linkml-model schemas are copied (vendored) into linkml-runtime rather than
being a PyPI dependency because:

- **Version compatibility**: Ensures runtime code and model schemas are always compatible
- **Offline usage**: No network fetches required at runtime
- **Deterministic builds**: The exact model version is frozen in the package
- **Simplified deployment**: Users install one package, not two

### What Gets Synced

The `make update_model` command copies the entire `linkml_model/` directory from
the linkml-model repository, which includes:

- `model/schema/*.yaml` - Source LinkML schemas
- `*.py` - Generated Python dataclasses (meta.py, types.py, etc.)
- `json/`, `jsonld/`, `jsonschema/` - Generated artifacts
- `rdf/`, `owl/`, `shex/` - RDF/OWL artifacts

## Prerequisites

- Git access to both repositories
- UV installed for running tests
- Write access to the linkml repository (for committing changes)

## Procedure

### Phase 1: Prepare linkml-model Release

1. **Create a release candidate tag** in the linkml-model repository:
   ```bash
   # In the linkml-model repository
   git tag v1.10.0-rc1
   git push origin v1.10.0-rc1
   ```

2. **Verify the tag** is accessible:
   ```bash
   git ls-remote --tags https://github.com/linkml/linkml-model.git | grep v1.10.0
   ```

### Phase 2: Sync to linkml-runtime

1. **Navigate to the linkml repository** and update the Makefile tag:
   ```bash
   cd packages/linkml_runtime
   ```

2. **Edit the MODEL_TAG** in `Makefile` (or override on command line):
   ```makefile
   MODEL_TAG = v1.10.0-rc1
   ```

3. **Run the sync**:
   ```bash
   make update_model
   # Or override without editing:
   make update_model MODEL_TAG=v1.10.0-rc1
   ```

4. **Review the changes**:
   ```bash
   git diff src/linkml_runtime/linkml_model/
   git status
   ```

### Phase 3: Test Compatibility

1. **Run linkml-runtime tests**:
   ```bash
   # From workspace root
   uv run pytest tests/linkml_runtime/ -v
   ```

2. **Run full linkml test suite**:
   ```bash
   uv run pytest tests/linkml/ -v
   ```

3. **Check for breaking changes** by reviewing:
   - Changes to `meta.py` (the main metamodel)
   - Changes to slot/class definitions
   - Any removed or renamed elements

### Phase 4: Review and Sign-off

1. **Create a PR** with the synced changes:
   ```bash
   git checkout -b sync-linkml-model-v1.10.0-rc1
   git add packages/linkml_runtime/src/linkml_runtime/linkml_model/
   git add packages/linkml_runtime/Makefile  # if MODEL_TAG was updated
   git commit -m "Sync linkml-model v1.10.0-rc1"
   git push origin sync-linkml-model-v1.10.0-rc1
   ```

2. **Review with team leads** before merging (especially for major/minor versions)

3. **Merge to main** once approved and CI passes

### Phase 5: Final Release

Once the release candidate is validated:

1. **Tag final release** in linkml-model:
   ```bash
   # In linkml-model repository
   git tag v1.10.0
   git push origin v1.10.0
   ```

2. **Update linkml-runtime** with final tag:
   ```bash
   # In linkml repository
   cd packages/linkml_runtime
   make update_model MODEL_TAG=v1.10.0
   ```

3. **Commit and release**:
   - Commit the final sync
   - Create GitHub release for linkml-runtime
   - Create GitHub release for linkml

## Troubleshooting

### Tests fail after sync

1. Check if the linkml-model introduced breaking changes
2. Review the changelog/release notes in linkml-model
3. Update linkml-runtime or linkml code to accommodate changes
4. If changes are unintentional, report to linkml-model maintainers

### Clone fails

If `make update_model` fails to clone:

```bash
# Verify tag exists
git ls-remote --tags https://github.com/linkml/linkml-model.git

# Try manual clone to debug
git clone --depth 1 --branch v1.10.0 https://github.com/linkml/linkml-model.git /tmp/test-clone
```

### Partial sync or corrupted files

```bash
# Clean and re-sync
rm -rf .linkml-model-clone
rm -rf src/linkml_runtime/linkml_model/*
make update_model
```

## Notes on validation_datamodel

The file `src/linkml_runtime/processing/validation_datamodel.py` is **NOT** part
of linkml-model. It is a separate, extended validation schema maintained only in
linkml-runtime. See the comments in `packages/linkml_runtime/Makefile` for details.

If you need to update `validation_datamodel.py` after editing the YAML:
```bash
make src/linkml_runtime/processing/validation_datamodel.py
```

## Version Alignment Policy

Per [issue #3076](https://github.com/linkml/linkml/issues/3076):

- Minor version increases in `linkml` should be accompanied by a linkml-model release
- Patch releases may not require a linkml-model update
- Major version changes require coordination and sign-off from project leads

## Checklist

Use this checklist when performing a linkml-model update:

- [ ] linkml-model release candidate tagged
- [ ] MODEL_TAG updated in Makefile
- [ ] `make update_model` completed successfully
- [ ] `git diff` reviewed for unexpected changes
- [ ] linkml-runtime tests pass
- [ ] linkml tests pass
- [ ] PR created and reviewed
- [ ] Team sign-off obtained (for minor/major versions)
- [ ] Final linkml-model version tagged
- [ ] Final sync completed
- [ ] linkml-runtime released to PyPI
- [ ] linkml released to PyPI
