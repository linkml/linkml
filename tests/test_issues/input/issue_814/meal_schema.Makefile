SCHEMA_FILE=meal_schema.yaml
RUN=poetry run
OUTDIR=../../output/issue_814/

.PHONY: clean all query_dumped_db

all: clean $(OUTDIR)meal_schema_generated.yaml $(OUTDIR)meal_data_converted.tsv $(OUTDIR)meal_data.db query_dumped_db

clean:
	rm -rf $(OUTDIR)meal_schema_generated.yaml
	rm -rf $(OUTDIR)meal_data_converted.tsv
	rm -rf $(OUTDIR)meal_data.db

$(OUTDIR)meal_schema_generated.yaml:
	# lightweight schema validation
	# or gen-linkml --format yaml
	$(RUN) gen-yaml $(SCHEMA_FILE) > $@

$(OUTDIR)meal_data_converted.tsv: $(SCHEMA_FILE) meal_data.yaml
	# show that LinkML tools can handle this data in general
	$(RUN) linkml-convert \
		--output $@ \
		--target-class MealLog \
		--index-slot meals \
		--schema $^

$(OUTDIR)meal_data.db:  $(SCHEMA_FILE) meal_data.yaml
	$(RUN) linkml-sqldb dump\
		--db $@ \
		--target-class MealLog \
		--index-slot meals \
		--schema $^

query_dumped_db: $(OUTDIR)meal_data.db
	sqlite3 $< \
		".headers on" \
		"select * from Meal" ""
