# =============================================================================
# LinkML Runtime Makefile
# =============================================================================
#
# OVERVIEW
# --------
# This Makefile manages the synchronization of linkml-model schemas into the
# linkml-runtime package. Understanding this process is critical for releases.
#
# ARCHITECTURE
# ------------
# The LinkML ecosystem has three main components:
#
#   1. linkml-model (github.com/linkml/linkml-model)
#      - Contains the source YAML schemas (meta.yaml, types.yaml, etc.)
#      - NOT published as a PyPI package
#      - Releases are tagged (e.g., v1.10.0)
#
#   2. linkml-runtime (PyPI: linkml-runtime)
#      - The schemas from linkml-model are VENDORED (copied) into:
#        src/linkml_runtime/linkml_model/
#      - This means linkml-runtime ships with a frozen copy of the model
#      - There is NO PyPI dependency on linkml-model
#
#   3. linkml (PyPI: linkml)
#      - Depends on linkml-runtime via PyPI
#      - Gets the model schemas transitively through linkml-runtime
#
# DEPENDENCY FLOW
# ---------------
#
#   linkml-model repo
#         │
#         │  make update_model (manual sync via this Makefile)
#         ▼
#   linkml-runtime/linkml_model/  (vendored copy)
#         │
#         │  PyPI dependency
#         ▼
#   linkml package
#
# WHY VENDORING?
# --------------
# - Ensures version compatibility between runtime code and model schemas
# - Avoids network fetches at runtime
# - Allows offline usage
# - Provides deterministic builds
#
# RELEASE PROCESS
# ---------------
# See: docs/sop-linkml-model-update.md for the full Standard Operating Procedure
#
# Quick summary:
#   1. Release linkml-model with a new tag (e.g., v1.10.0)
#   2. Update MODEL_TAG below to the new tag
#   3. Run: make update_model
#   4. Run tests to verify compatibility
#   5. Release linkml-runtime and linkml
#
# See also: https://github.com/linkml/linkml/issues/3076
#
# =============================================================================

# -----------------------------------------------------------------------------
# Configuration for linkml-model version
# -----------------------------------------------------------------------------
# MODEL_REPO: The GitHub repository URL for linkml-model
# MODEL_TAG:  The git tag to sync (update this when releasing a new version)
# MODEL_CLONE_DIR: Temporary directory for shallow clone (cleaned up after sync)

MODEL_REPO = https://github.com/linkml/linkml-model.git
MODEL_TAG = v1.10.0-rc2
MODEL_CLONE_DIR = .linkml-model-clone

# -----------------------------------------------------------------------------
# update_model: Sync linkml-model schemas into linkml-runtime
# -----------------------------------------------------------------------------
# This target:
#   1. Removes any previous temporary clone
#   2. Does a shallow clone (--depth 1) of the specified tag (fast, minimal download)
#   3. Copies all schema artifacts into src/linkml_runtime/linkml_model/
#   4. Cleans up the temporary clone
#
# Usage:
#   make update_model                         # Use default MODEL_TAG
#   make update_model MODEL_TAG=v1.11.0       # Override tag on command line
#
# After running, verify changes with:
#   git diff src/linkml_runtime/linkml_model/
#   uv run pytest tests/linkml_runtime/

.PHONY: update_model
update_model:
	rm -rf $(MODEL_CLONE_DIR)
	git clone --depth 1 --branch $(MODEL_TAG) $(MODEL_REPO) $(MODEL_CLONE_DIR)
	cp -pr $(MODEL_CLONE_DIR)/linkml_model/* src/linkml_runtime/linkml_model
	rm -rf $(MODEL_CLONE_DIR)
	@echo ""
	@echo "Successfully synced linkml-model $(MODEL_TAG) into src/linkml_runtime/linkml_model/"
	@echo "Next steps:"
	@echo "  1. Review changes: git diff src/linkml_runtime/linkml_model/"
	@echo "  2. Run tests: uv run pytest tests/linkml_runtime/"
	@echo "  3. If tests pass, commit the changes"

# -----------------------------------------------------------------------------
# test: Run the linkml-runtime test suite
# -----------------------------------------------------------------------------
# Note: Tests are located at the workspace root in tests/linkml_runtime/
# Running from this directory will find 0 tests (that's expected).
# For full test coverage, run from the workspace root:
#   uv run pytest tests/linkml_runtime/

.PHONY: test
test:
	uv run pytest


# =============================================================================
# VALIDATION DATAMODEL (SEPARATE FROM LINKML-MODEL)
# =============================================================================
#
# IMPORTANT: The validation_datamodel is NOT part of linkml-model!
#
# src/linkml_runtime/processing/validation_datamodel.yaml is a separate,
# extended validation schema maintained only in linkml-runtime. It contains:
#   - ConstraintType enum (30+ constraint types)
#   - ValidationConfiguration class
#   - RepairConfiguration, RepairReport, RepairOperation classes
#
# This is MORE COMPREHENSIVE than the basic validation.yaml in linkml-model.
# The referencevalidator.py imports from this local schema.
#
# The TODO in validation_datamodel.yaml says "fold this back into linkml-model"
# but this hasn't happened yet. Until then, if you edit the YAML, regenerate:
#   make src/linkml_runtime/processing/validation_datamodel.py
#
# This rule is NOT triggered by update_model - they are independent.
# -----------------------------------------------------------------------------

src/linkml_runtime/processing/validation_datamodel.py: src/linkml_runtime/processing/validation_datamodel.yaml
	gen-python $< > $@.tmp && mv $@.tmp $@
