# CSVs and Tabular Data

LinkML can support both complex interlinked normalized relational data as well as flat/denormalized data as typically found in spreadsheets and in CSVs used by data scientists.

Our philosophy is "always have a schema" even when working with simple tabular data.

## Conversion

the `linkml-convert` script can be used to convert between CSVs/TSVs and other formats like JSON/RDF. The same tooling for [validating-data](validating-data) operate in the same way.

### Conventions for working with tabular data

LinkML allows you to create schemas with complex nested data - these
don't necessarily have a simple unified mapping to
tables/TSVs. However, you can still work with tabular representations
if your schema has a certain "shape" and you provide sufficient hints.

### Container objects

See [part 2 of the tutorial](../intro/tutorial02) for an introduction to container objects.

To serialize your data objects as TSVs, it's assumed that you have a
class in your schema that serves the role of *container*. It can be
called whatever you like. You can also annotate this with
[tree_root](https://w3id.org/linkml/tree_root) set to true. This class will have a multivalued slot pointing at the list of things you want to serialize in the TSV. This slot is known as the *index slot*

For example, in the [PersonSchema](https://github.com/linkml/linkml/tree/main/examples/PersonSchema) schema, the Container class has two possible index slots:

* persons: points at a list of Person objects
* organizations: points at a list of Organization objects

You can only serialize one of these in any one TSV (using more advanced techniques you could create a union class for Person and Organization and serialize this, but this is outside the scope of this tutorial)

The linkml command line tools for conversion and validation will do
their best to guess the index slot and the container, but if there is
no unambiguous choice, then have to provide these using the following
arguments:

```text
  -C, --target-class TEXT         name of class in datamodel that the root
                                  node instantiates

  -S, --index-slot TEXT           top level slot. Required for CSV
                                  dumping/loading
```

For example, to serialize the organizations in the provided YAML data file in this repository, you can run:

```bash
linkml-convert -t tsv -s examples/PersonSchema/personinfo.yaml -C Container -S organizations examples/PersonSchema/data/example_personinfo_data.yaml
```

Note that currently serializing the person objects won't work, as the Person class is too nested to be serialized as TSV

### On the fly denormalization

The [json-flattener/](https://github.com/cmungall/json-flattener/) library is used to do on-the-fly denormalizations. For example:

* multivalued slots are serialized using a `|` separator
* nested slots are flattened to paths, e.g if Container has a slot persons, and Person has a slot name, then the path with be `persons_name`

### Customizing multivalued field formatting

By default, multivalued fields are serialized with brackets and pipe delimiters:

```
[value1|value2|value3]
```

This format (called "python" style) works well for round-tripping data through LinkML tools.
However, when working with spreadsheets, users often prefer typing values without brackets:

```
value1|value2|value3
```

You can customize the formatting using slot annotations:

```yaml
slots:
  tags:
    range: string
    multivalued: true
    annotations:
      list_syntax: plaintext    # removes brackets
      list_delimiter: "|"       # delimiter between values (default)
```

#### Available annotations

| Annotation | Values | Default | Description |
|------------|--------|---------|-------------|
| `list_syntax` | `python`, `plaintext` | `python` | `python` uses brackets `[a|b|c]`, `plaintext` has no brackets `a|b|c` |
| `list_delimiter` | any string | `|` | Character(s) used to separate list items |

#### Examples

**Default behavior (python style):**

```yaml
slots:
  aliases:
    range: string
    multivalued: true
```

TSV output: `[Alice|Bob|Charlie]`

**Plaintext style with pipe delimiter:**

```yaml
slots:
  aliases:
    range: string
    multivalued: true
    annotations:
      list_syntax: plaintext
      list_delimiter: "|"
```

TSV output: `Alice|Bob|Charlie`

**Plaintext style with semicolon delimiter:**

```yaml
slots:
  categories:
    range: string
    multivalued: true
    annotations:
      list_syntax: plaintext
      list_delimiter: ";"
```

TSV output: `category1;category2;category3`

#### Schema-level settings

You can also set these as schema-level defaults using `settings`:

```yaml
id: https://example.org/myschema
name: myschema
settings:
  list_syntax: plaintext
  list_delimiter: "|"

slots:
  tags:
    multivalued: true
  categories:
    multivalued: true
    annotations:
      list_delimiter: ";"  # override schema default for this slot
```

Slot-level annotations take precedence over schema-level settings.

## Inference of schemas from tabular data

Use `generalize-tsv` command in the [schema-automator](https://github.com/linkml/schema-automator)
