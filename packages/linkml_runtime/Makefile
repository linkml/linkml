# Currently the main purposing of this makefile is to synchronize
# latest releases of linkml-model into linkml_runtime/linkml_model
#
# Set LINKML_MODEL_RELEASE to the linkml-model release tag to sync from
# (see https://github.com/linkml/linkml-model/releases). Bump manually
# when pulling in a new linkml-model release.

LINKML_MODEL_RELEASE = v1.11.0

all: update_model update_validation_model

update_model:
	# Clean up
	rm -rf linkml-model-github/
	mkdir -p linkml-model-github/
	rm -rf src/linkml_runtime/linkml_model
	mkdir -p src/linkml_runtime/linkml_model

	# Clone from the pinned linkml-model release tag
	git clone --depth 1 --branch $(LINKML_MODEL_RELEASE) https://github.com/linkml/linkml-model.git linkml-model-github/

	cp -pr linkml-model-github/linkml_model/* src/linkml_runtime/linkml_model

	# Clean up some files that are not needed at the moment, https://github.com/linkml/linkml/issues/3129
	rm src/linkml_runtime/linkml_model/model/schema/extended_types.yaml
	cd ../../ && pre-commit run --all-files || pre-commit run --all-files

update_validation_model: src/linkml_runtime/processing/validation_datamodel.py
	cd ../../ && pre-commit run --all-files || pre-commit run --all-files

# temporary measure until linkml-model is synced
src/linkml_runtime/processing/validation_datamodel.py: src/linkml_runtime/processing/validation_datamodel.yaml
	uv sync
	uv run gen-python $< > $@.tmp && mv $@.tmp $@
