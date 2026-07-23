VERSION = $(shell git tag | tail -1)

SPECIFICATION.pdf: SPECIFICATION.md
	pandoc $< -o $@

# for now we only have one example
all-examples: all-examples-organization

# for each example schema, make all derived schema products, and derived serializations for the example data file
all-examples-%:  examples/%.py examples/%.schema.json  examples/%.shex  examples/%.graphql  examples/%.graphql  examples/%.shex examples/%.proto  examples/%.shex examples/%.valid examples/%-data.nt
	echo done

#RUN=pipenv run
RUN=uv run

# Extra pytest flags (e.g. parallelism): `make test PYTEST_FLAGS="-n auto"`
# Default: skip notebooks (they mutate the shared venv and always fail locally).
PYTEST_FLAGS ?= --ignore=tests/linkml/test_notebooks

# Wrap with coverage.py: `make test COVERAGE=true`
ifdef COVERAGE
RUNNER = $(RUN) coverage run -m pytest
else
RUNNER = $(RUN) pytest
endif

lint-fix:
	$(RUN) tox -e format

format: lint-fix

# Fast tests (excludes slow, kroki).
# Override test path: `make test-linkml TEST_PATH=tests/linkml/test_compliance/`
.PHONY: test test-linkml test-linkml-runtime test-slow test-all

test-linkml: TEST_PATH ?= tests/linkml/
test-linkml:
	$(RUNNER) $(TEST_PATH) \
		--with-network \
		-m "not kroki and not slow" \
		$(PYTEST_FLAGS)

test-linkml-runtime: TEST_PATH ?= tests/linkml_runtime/
test-linkml-runtime:
	$(RUNNER) $(TEST_PATH) \
		--with-network \
		-m "not kroki and not slow" \
		$(PYTEST_FLAGS)

test: test-linkml test-linkml-runtime

# Slow tests only.
test-slow: TEST_PATH ?= tests/linkml/
test-slow:
	$(RUNNER) $(TEST_PATH) \
		--with-slow --with-biolink \
		-m "slow and not kroki" \
		$(PYTEST_FLAGS)

# Full suite (fast + slow, no duplication).
test-all: test test-slow

# Determine which packages have changes in the current branch (vs main) and run
# only their fast tests.
.PHONY: test-branch
test-branch:
	base="$$(git merge-base HEAD main)"; \
	changes="$$(git diff --name-only "$$base"...HEAD)"; \
	linkml=; linkml_runtime=; \
	if echo "$$changes" | grep -qE '^packages/linkml/|^tests/linkml/'; then linkml=1; fi; \
	if echo "$$changes" | grep -qE '^packages/linkml_runtime/|^tests/linkml_runtime/'; then linkml_runtime=1; fi; \
	if [ -n "$$linkml" ]; then $(MAKE) test-linkml; fi; \
	if [ -n "$$linkml_runtime" ]; then $(MAKE) test-linkml-runtime; fi; \
	if [ -z "$$linkml$$linkml_runtime" ]; then echo "No package changes detected (only infra/docs?). Running full fast suite."; $(MAKE) test; fi

# Metamodel compatibility: download latest metamodel from linkml-model
LINKML_MODEL_BRANCH ?= main
LINKML_MODEL_REPO = https://github.com/linkml/linkml-model.git
METAMODEL_DIR = tests/linkml/test_metamodel_compat/input/metamodel

download-metamodel:
	rm -rf temp/linkml-model
	git clone --depth 1 --branch $(LINKML_MODEL_BRANCH) $(LINKML_MODEL_REPO) temp/linkml-model
	rm -f $(METAMODEL_DIR)/*.yaml
	cp temp/linkml-model/linkml_model/model/schema/*.yaml $(METAMODEL_DIR)/
	sed -i.bak '/^#.*- linkml:/d' $(METAMODEL_DIR)/*.yaml
	sed -i.bak 's/- linkml:\([a-zA-Z_]*\)/- \1/g' $(METAMODEL_DIR)/*.yaml
	rm -f $(METAMODEL_DIR)/*.bak
	rm -rf temp/linkml-model

test-metamodel:
	mkdir -p temp
	$(RUN) pytest tests/linkml/test_metamodel_compat/ --with-slow -v 2>&1 | tee temp/test_output.txt

## Example schema products
examples/%.py: examples/%.yaml
	$(RUN) gen-py-classes $< > $@ && $(RUN) python -m examples.$*
examples/%.shex: examples/%.yaml
	$(RUN) gen-shex $< > $@
examples/%.schema.json: examples/%.yaml
	$(RUN) gen-json-schema -t $* $< > $@
examples/%.context.jsonld: examples/%.yaml
	$(RUN) gen-jsonld-context -t $* $< > $@
examples/%.graphql: examples/%.yaml
	$(RUN) gen-graphql $< > $@
examples/%.context.jsonld: examples/%.yaml
	$(RUN) gen-jsonld-context $< > $@
examples/%.jsonld: examples/%.yaml
	$(RUN) gen-jsonld $< > $@
examples/%.shex: examples/%.yaml
	$(RUN) gen-shex $< > $@
examples/%.proto: examples/%.yaml
	$(RUN) gen-proto $< > $@
examples/%.owl: examples/%.yaml
	$(RUN) gen-owl $< > $@
examples/%.ttl: examples/%.yaml
	$(RUN) gen-rdf $< > $@
examples/%-docs: examples/%.yaml
	$(RUN) gen-doc $< -d $@

## Example instance data products
examples/%.valid: examples/%-data.json examples/%.schema.json
	jsonschema -i $^
examples/%-data.jsonld: examples/%-data.json examples/%.context.jsonld
	jq -s '.[0] * .[1]' $^ > $@
examples/%-data.nt: examples/%-data.jsonld
	riot $< > $@

linkml/workspaces/datamodel/workspaces.py: linkml/workspaces/datamodel/workspaces.yaml
	$(RUN) gen-python $< > $@.tmp && mv $@.tmp $@

linkml/linter/config/datamodel/config.py: linkml/linter/config/datamodel/config.yaml
	$(RUN) gen-python $< > $@.tmp && mv $@.tmp $@

TUTORIALS = 01 02 03 04 05 06 07 08 09 10
test-tutorials: $(patsubst %, test-tutorial-%, $(TUTORIALS))
test-tutorial-%: docs/intro/tutorial%.md
	$(RUN) python -m linkml.utils.execute_tutorial -d /tmp/tutorial $<

build-generator-dashboard:
	$(RUN) pytest tests/linkml/test_compliance/ --with-output -q
	$(RUN) python scripts/generate_dashboard.py

docs:
	cd docs && $(RUN) make html

################################################
#### Commands for building the Docker image ####
################################################

IM=linkml/linkml

docker-build-no-cache:
	@docker build --no-cache -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest

docker-build:
	@docker build -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest

docker-build-use-cache-dev:
	@docker build -t $(DEV):$(VERSION) . \
	&& docker tag $(DEV):$(VERSION) $(DEV):latest

docker-clean:
	docker kill $(IM) || echo not running ;
	docker rm $(IM) || echo not made

docker-publish-no-build:
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest

docker-publish-dev-no-build:
	@docker push $(DEV):$(VERSION) \
	&& docker push $(DEV):latest

docker-publish: docker-build
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest

docker-run:
	@docker run  -v $(PWD):/work -w /work -ti $(IM):$(VERSION)
