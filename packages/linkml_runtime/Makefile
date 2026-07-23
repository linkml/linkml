# Currently the main purpose of this makefile is to synchronize the
# latest release of linkml-model (including release candidates) into
# linkml_runtime/linkml_model.
#
# Run `make update_model` to pull the newest release or pre-release from
# https://github.com/linkml/linkml-model/releases, copy the vendored files,
# and record the upstream commit SHA in src/linkml_runtime/linkml_model/UPSTREAM_SHA.
# Commit the resulting changes together.

UPSTREAM_SHA_FILE = src/linkml_runtime/linkml_model/UPSTREAM_SHA

all: update_model update_validation_model

update_model:
	# Resolve the latest release or pre-release tag from the GitHub Releases API
	$(eval LINKML_MODEL_TAG := $(shell \
		curl -fsSL "https://api.github.com/repos/linkml/linkml-model/releases?per_page=1" \
		| python3 -c "import sys, json; releases = json.load(sys.stdin); print(releases[0]['tag_name'])"))

	# Resolve the tag to its commit SHA via the Git refs API
	$(eval LINKML_MODEL_SHA := $(shell \
		curl -fsSL "https://api.github.com/repos/linkml/linkml-model/git/refs/tags/$(LINKML_MODEL_TAG)" \
		| python3 -c "import sys, json; d = json.load(sys.stdin); print(d['object']['sha'])"))

	@echo "Vendoring linkml-model $(LINKML_MODEL_TAG) @ $(LINKML_MODEL_SHA)"

	# Clean up
	rm -rf linkml-model-github/
	mkdir -p linkml-model-github/
	rm -rf src/linkml_runtime/linkml_model
	mkdir -p src/linkml_runtime/linkml_model

	# Clone from the resolved tag
	git clone --depth 1 --branch $(LINKML_MODEL_TAG) https://github.com/linkml/linkml-model.git linkml-model-github/

	cp -pr linkml-model-github/linkml_model/* src/linkml_runtime/linkml_model

	# Record the upstream commit SHA so tests can compare against the exact vendored revision
	echo "$(LINKML_MODEL_SHA)" > $(UPSTREAM_SHA_FILE)

	# Clean up some files that are not needed at the moment, https://github.com/linkml/linkml/issues/3129
	rm src/linkml_runtime/linkml_model/model/schema/extended_types.yaml
	cd ../../ && pre-commit run --all-files || pre-commit run --all-files

update_validation_model: src/linkml_runtime/processing/validation_datamodel.py
	cd ../../ && pre-commit run --all-files || pre-commit run --all-files

# temporary measure until linkml-model is synced
src/linkml_runtime/processing/validation_datamodel.py: src/linkml_runtime/processing/validation_datamodel.yaml
	uv sync
	uv run gen-python $< > $@.tmp && mv $@.tmp $@
