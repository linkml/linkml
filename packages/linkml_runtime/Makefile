# Currently the main purposing of this makefile is to synchronize
# latest releases of linkml-model into linkml_runtime/linkml_model

BRANCH = main

all: update_model update_validation_model

update_model:
	# Clean up
	rm -rf linkml-model-github/
	mkdir -p linkml-model-github/
	rm -rf src/linkml_runtime/linkml_model
	mkdir -p src/linkml_runtime/linkml_model

	# Clone from latest main branch
	git clone --depth 1 --branch $(BRANCH) https://github.com/linkml/linkml-model.git linkml-model-github/

	cp -pr linkml-model-github/linkml_model/* src/linkml_runtime/linkml_model

	# Clean up some files that are not needed at the moment, https://github.com/linkml/linkml/issues/3129
	rm src/linkml_runtime/linkml_model/model/schema/extended_types.yaml
	cd ../../ && pre-commit run --all-files || pre-commit run --all-files

update_validation_model: src/linkml_runtime/processing/validation_datamodel.py
	cd ../../ && pre-commit run --all-files || pre-commit run --all-files

# temporary measure until linkml-model is synced
src/linkml_runtime/processing/validation_datamodel.py: src/linkml_runtime/processing/validation_datamodel.yaml
	gen-python $< > $@.tmp && mv $@.tmp $@
