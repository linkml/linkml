# Working with Data

LinkML allows you to specify schemas for data in a variety of forms:

 * JSON / YAML
 * Python object models
 * SQL databases
 * Spreadsheets and tabular data
 * RDF/Linked Data
 * Property Graphs

The "native" form for LinkML can be considered JSON/YAML.

See [PersonSchema/data](https://github.com/linkml/linkml/tree/main/examples/PersonSchema/data) for example data files

## Conversion

The `linkml-convert` script can be used to convert data from one form to another, following a schema

This makes use of "loaders" and "dumpers" in the linkml-runtime

```bash
linkml-convert --help
Usage: linkml-convert [OPTIONS] INPUT

  Converts instance data to and from different LinkML Runtime serialization
  formats.

  The instance data must conform to a LinkML model, and there must be python
  dataclasses generated from that model. The converter works by first using
  a linkml-runtime loader to instantiate in-memory model objects, then
  dumpers are used to serialize. When converting to or from RDF, a JSON-lD
  context must also be passed

Options:
  -m, --module TEXT               Path to python datamodel module
  -o, --output TEXT               Path to output file
  -f, --input-format [yaml|json|rdf|csv|tsv]
                                  Input format. Inferred from input suffix if
                                  not specified

  -t, --output-format [yaml|json|rdf|csv|tsv]
                                  Output format. Inferred from output suffix
                                  if not specified

  -C, --target-class TEXT         name of class in datamodel that the root
                                  node instantiates

  -S, --index-slot TEXT           top level slot. Required for CSV
                                  dumping/loading

  -s, --schema TEXT               Path to schema specified as LinkML yaml
  --validate / --no-validate      Validate against the schema
  -c, --context TEXT              path to JSON-LD context file. Required for
                                  RDF input/output

  --help                          Show this message and exit.
```

## Programmatic usage

See [developer docs](../code) for documentation of the relevant python classes
