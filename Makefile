
SPECIFICATION.pdf: SPECIFICATION.md
	pandoc $< -o $@

# for now we only have one example
all-examples: all-examples-organization

# for each example schema, make all derived schema products, and derived serializations for the example data file
all-examples-%:  examples/%.py examples/%.schema.json  examples/%.shex  examples/%.graphql  examples/%.graphql  examples/%.shex examples/%.proto  examples/%.shex examples/%.valid examples/%-data.nt
	echo done

RUN=pipenv run

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

rtd:
	cd sphinx && $(RUN) make html
deploy-rtd:
	cd sphinx && $(RUN) make deploy
