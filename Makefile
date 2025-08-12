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

lint-fix:
	$(RUN) tox -e format

format: lint-fix

test:
	$(RUN) pytest

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
	$(RUN) gen-markdown $< -d $@

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
