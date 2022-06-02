SCHEMA_FILE=genome_schema.yaml
RUN=poetry run
OUTDIR=../../output/issue_815/

.PHONY: clean all query_dumped_db

all: clean $(OUTDIR)genome_schema_generated.yaml $(OUTDIR)genome_data.tsv $(OUTDIR)genome_data.db

clean:
	rm -rf $(OUTDIR)genome_schema_generated.yaml
	rm -rf $(OUTDIR)genome_data.tsv
	rm -rf $(OUTDIR)genome_data.db

$(OUTDIR)genome_schema_generated.yaml:
	# lightweight schema validation
	# or gen-linkml --format yaml
	$(RUN) gen-yaml $(SCHEMA_FILE) > $@

$(OUTDIR)genome_data.tsv: $(SCHEMA_FILE) genome_data.yaml
	# show that LinkML tools can handle this data in general
	$(RUN) linkml-convert \
		--output $@ \
		--target-class Genome \
		--index-slot genes \
		--schema $^

$(OUTDIR)genome_data.db:  $(SCHEMA_FILE) $(OUTDIR)genome_data.tsv
	$(RUN) linkml-sqldb dump\
		--db $@ \
		--target-class Genome \
		--index-slot genes \
		--schema $^

#all: clean \
#$(OUTDIR)birthday_schema_generated.yaml \
#$(OUTDIR)contacts_data_converted.yaml \
#query_dumped_db
#
#clean:
#	rm -rf $(OUTDIR)birthday_schema_generated.yaml
#	rm -rf $(OUTDIR)contacts_data_converted.yaml
#	rm -rf $(OUTDIR)contacts_data.db
#
#$(OUTDIR)birthday_schema_generated.yaml:
#	# lightweight schema validation
#	# or gen-linkml --format yaml
#	$(RUN) gen-yaml $(SCHEMA_FILE) > $@
#
#$(OUTDIR)contacts_data_converted.yaml: $(SCHEMA_FILE) contacts_data.tsv
#	# show that LinkML tools can handle this data in general
#	$(RUN) linkml-convert \
#		--output $@ \
#		--target-class Contacts \
#		--index-slot people \
#		--schema $^
#
#$(OUTDIR)contacts_data.db:  $(SCHEMA_FILE) contacts_data.tsv
#	$(RUN) linkml-sqldb dump\
#		--db $@ \
#		--target-class Contacts \
#		--index-slot people \
#		--schema $^
#
#query_dumped_db: $(OUTDIR)contacts_data.db
#	sqlite3 $< \
#		".headers on" \
#		"select * from Person" ""