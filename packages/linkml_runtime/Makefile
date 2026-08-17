# Currently the main purpose of this makefile is to synchronize the
# latest release of linkml-model (including release candidates) into
# linkml_runtime/linkml_model.
#
# Run `make update_model` to pull the newest release or pre-release from
# https://github.com/linkml/linkml-model/releases, copy the vendored files,
# and record the upstream commit SHA in src/linkml_runtime/linkml_model/UPSTREAM_SHA.
# Commit the resulting changes together.

UPSTREAM_SHA_FILE = src/linkml_runtime/linkml_model/UPSTREAM_SHA

# Single source of truth for "which linkml-model revision should we be on".
# `update_model` vendors it; the weekly metamodel-compat workflow compares it
# against UPSTREAM_SHA to notice a release we have not adopted. Keeping one
# resolver means the two can never disagree about what "latest" means.
#
# The commits endpoint is used rather than /git/refs/tags because it dereferences
# annotated tags to a commit; /git/refs/tags returns the tag *object* SHA, which
# `git fetch <sha>` cannot resolve.
define LATEST_MODEL_RELEASE_PY
import json
import sys
import urllib.request

BASE = "https://api.github.com/repos/linkml/linkml-model"

releases = json.load(urllib.request.urlopen(BASE + "/releases?per_page=1"))
if not releases:
    sys.exit("No linkml-model releases returned. Refusing to guess a revision.")

tag = releases[0]["tag_name"]
sha = json.load(urllib.request.urlopen(BASE + "/commits/" + tag))["sha"]
print(tag, sha)
endef
export LATEST_MODEL_RELEASE_PY

all: update_model update_validation_model

# Prints "<tag> <commit-sha>" for the newest release, prereleases included.
.PHONY: print_latest_model_release
print_latest_model_release:
	@python3 -c "$$LATEST_MODEL_RELEASE_PY"

update_model:
	$(eval LINKML_MODEL_RELEASE := $(shell $(MAKE) -s print_latest_model_release))
	$(eval LINKML_MODEL_TAG := $(word 1,$(LINKML_MODEL_RELEASE)))
	$(eval LINKML_MODEL_SHA := $(word 2,$(LINKML_MODEL_RELEASE)))

	@test -n "$(LINKML_MODEL_TAG)" -a -n "$(LINKML_MODEL_SHA)" \
		|| { echo "Could not resolve the latest linkml-model release; aborting."; exit 1; }

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
