# Data Validation

LinkML is designed to allow for a variety of strategies for data
validation. The overall philosophy is to provide maximum expressivity
in the language to allow model designers to state all consraints in a
declarative fashion, and then to leverage existing frameworks and to
allow the user to balance concerns such as expressivity vs efficiency.

Currently there are 4 supported strategies:

 * validation via Python object instantiation
 * validation through JSON-Schema
 * validation of triples in a triplestore or RDF file via generation of SPARQL constraints
 * validation of RDF via generation of ShEx

However, others will be supported in future

## Validation of JSON documents

The `linkml-convert` command will automatically perform data validation.

Currently it performs two level validation:

 * it will convert data to in-memory Python objects, using dataclass validation
 * it will then convert the LinkML schema to JSON-Schema and employ JSON-Schema validation

Note that you can easily generate JSON-Schema and use your validator of choice, see [JSON Schema Generation](../generators/json-schema)

## Validation of RDF triplestores using generated SPARQL

The LinkML framework can also be used to validate RDF, either in a file, or a triplestore. There are two steps:

 - generation of SPARQL constraint-style queries (see [sparqlgen](../generators/sparql) )
 - execution of those queries on an in-memory graph or external triplestore

The user can choose to run only the first step, to obtain a bank of SPARQL queries that can be applied selectively

```bash
linkml-sparql-validate --help
Usage: linkml-sparql-validate [OPTIONS]

  Validates sparql

  Example:

      linkml-sparql-validate -U http://sparql.hegroup.org/sparql -s
      tests/test_validation/input/omo.yaml

Options:
  -G, --named-graph TEXT          Constrain query to a named graph
  -i, --input TEXT                Input file to validate
  -U, --endpoint-url TEXT         URL of sparql endpoint
  -L, --limit TEXT                Max results per query
  -o, --output TEXT               Path to report file
  -f, --input-format [yaml|json|rdf|csv|tsv]
                                  Input format. Inferred from input suffix if
                                  not specified

  -t, --output-format [yaml|json|rdf|csv|tsv]
                                  Output format. Inferred from output suffix
                                  if not specified

  -s, --schema TEXT               Path to schema specified as LinkML yaml
  --help                          Show this message and exit.
```  

## Future plans

Future versions of LinkML will employ a powerful constraint and inference language.

One of the use cases here is being able to specify that the `length` field is equal to `end - start`. This declarative knowledge can then be used to either (1) infer the value of `length` if unspecified (2) infer either `start` or `end` if only one of these is specified alongside `length` (3) check consistency if all three are specified.

These constraints can then be executed over large databases via a variety of strategies including:

 * generation of datalog programs for efficient engines such as souffle
 * generation of SQL queries to be used with relational databases

We also plan to support generation of SHACL from LinkML
