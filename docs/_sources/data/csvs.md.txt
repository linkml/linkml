# CSVs and Tabular Data

LinkML can support both complex interlinked normalized relational data as well as flat/denormalized data as typically found in spreadsheets and in CSVs used by data scientists.

Our philosophy is "always have a schema" even when working with simple tabular data

## Conversion

the `linkml-convert` script can be used to convert between CSVs/TSVs and other formats like JSON/RDF. The same tooling for [validating-data](validating-data) operate in the same way.


## On the fly denormalization

See [https://github.com/cmungall/json-flattener/](https://github.com/cmungall/json-flattener/)

## Inference of schemas from tabular data

Use `tsvs2linkml` in the enrichment toolkit

