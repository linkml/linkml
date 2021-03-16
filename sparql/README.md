# BiolinkML SPARQL checks

These sparql checks can be used to query either biolinkML schemas or
instance data for biolinkML schemas.

The schema should be in the form of a .ttl file (using gen-rdf).

For instance data, this should be merged with the schema.ttl

The script [meta-sparql.sh](meta-sparql.sh) provides a convenient
wrapper that use robot to merge files and do queries.

## Naming conventions

 - queries over schemas are named `schema-*.rq`
 - queries intended to check for warnings/errors are named `*-check.rq`

## Examples (schemas)

To query for all elements in a schema:

`./sparql/meta-sparql.sh  -s examples/organization2.ttl -q sparql/element-list.rq`

The metamodel can be queried:

`./sparql/meta-sparql.sh  -s meta.ttl -q sparql/element-list.rq`

## Examples (instance data)

Find all unyped instances

`./sparql/meta-sparql.sh -i examples/organization2.ttl -s examples/organization2.ttl -q sparql/untyped-instance-violation.rq`

# TODO

 - move validation into python code
 - add tests
 - add more constraint checking

