NAME = personinfo
SRC = $(NAME).yaml
ROOT = Container
RUN = pipenv run
OUTDIR = $(NAME)
BUILD = build
INDEX_SLOT = persons

all: gen
gen:
	$(RUN) gen-project -d $(OUTDIR) $(SRC)

validate_all: validate-example_personinfo_data
validate-%: data/%.yaml
	$(RUN) linkml-convert -C $(ROOT) -s $(SRC) $<

build_all: build-all-example_personinfo_data

build-all-%: build-json-% build-ttl-%  build-tsv-%
	echo $*

build-json-%: $(BUILD)/%.json
	echo $*
build-ttl-%: $(BUILD)/%.ttl
	echo $*
build-yaml-%: $(BUILD)/%.yaml
	echo $*
build-tsv-%: $(BUILD)/%.tsv
	echo $*

$(BUILD)/%.json: data/%.yaml
	$(RUN) linkml-convert -C $(ROOT) -s $(SRC) $< -o $@
.PRECIOUS: $(BUILD)/%.json

$(BUILD)/%.ttl: data/%.yaml
	$(RUN) linkml-convert -C $(ROOT) -s $(SRC) $< -o $@
.PRECIOUS: $(BUILD)/%.ttl

$(BUILD)/%.yaml: data/%.yaml
	$(RUN) linkml-convert -C $(ROOT) -s $(SRC) $< -o $@
.PRECIOUS: $(BUILD)/%.yaml

$(BUILD)/%.tsv: data/%.yaml
	$(RUN) linkml-convert --index-slot $(INDEX_SLOT) -C $(ROOT) -s $(SRC) $< -o $@
.PRECIOUS: $(BUILD)/%.tsv
