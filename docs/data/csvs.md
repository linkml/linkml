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

This is called "python" style (bracketed) and works well for round-tripping data through LinkML tools.
However, when working with spreadsheets, users often prefer typing values without brackets:

```
value1|value2|value3
```

You can customize the formatting using schema-level annotations:

```yaml
id: https://example.org/myschema
name: myschema
annotations:
  list_syntax: plaintext    # removes brackets from all multivalued fields
  list_delimiter: "|"       # delimiter between values (default)

slots:
  tags:
    range: string
    multivalued: true
  categories:
    range: string
    multivalued: true
```

Note: These annotations apply to ALL multivalued fields in the CSV/TSV output.
This is because the underlying json-flattener library uses a single global
configuration for list formatting.

#### Available annotations

| Annotation | Values | Default | Description |
|------------|--------|---------|-------------|
| `list_syntax` | `python`, `plaintext` | `python` | `python` uses brackets `[a\|b\|c]`, `plaintext` has no brackets `a\|b\|c` |
| `list_delimiter` | any string | `\|` | Character(s) used to separate list items |
| `list_strip_whitespace` | `true`, `false` | `true` | Strip whitespace around delimiters when loading (e.g., `a \| b` → `['a', 'b']`) |

#### CLI options

You can override schema annotations using CLI options on `linkml-convert`:

```bash
linkml-convert -s schema.yaml -C Container -S items -t tsv \
  --list-syntax plaintext \
  --list-delimiter "|" \
  --list-strip-whitespace \
  input.yaml
```

| CLI Option | Description |
|------------|-------------|
| `--list-syntax` | `python` or `plaintext` - overrides schema annotation |
| `--list-delimiter` | Delimiter string - overrides schema annotation |
| `--list-strip-whitespace` / `--no-list-strip-whitespace` | Strip whitespace from list values (default: strip) |

All three options apply to both input (loading) and output (dumping):

- **On input**: `a | b | c` is parsed as `['a', 'b', 'c']` (stripped) or `['a ', ' b ', ' c']` (preserved)
- **On output**: `['dog   ', 'cat']` is written as `dog|cat` (stripped) or `dog   |cat` (preserved)

#### Examples

**Default behavior (python style):**

```yaml
id: https://example.org/default
name: default_example
# No annotations - uses default python style

slots:
  aliases:
    range: string
    multivalued: true
```

TSV output: `[Alice|Bob|Charlie]`

**Plaintext style with pipe delimiter:**

```yaml
id: https://example.org/plaintext
name: plaintext_example
annotations:
  list_syntax: plaintext
  list_delimiter: "|"

slots:
  aliases:
    range: string
    multivalued: true
```

TSV output: `Alice|Bob|Charlie`

**Plaintext style with semicolon delimiter:**

```yaml
id: https://example.org/semicolon
name: semicolon_example
annotations:
  list_syntax: plaintext
  list_delimiter: ";"

slots:
  categories:
    range: string
    multivalued: true
```

TSV output: `category1;category2;category3`

#### Working example

To try this with existing test files in the repository, first compare the default output:

```bash
linkml-convert -s tests/linkml_runtime/test_loaders_dumpers/models/books_normalized.yaml \
  -C Shop -S all_book_series -t tsv \
  tests/linkml_runtime/test_loaders_dumpers/input/books_normalized_01.yaml
```

This produces python style (bracketed) output like `[scifi|fantasy]`.

To get plaintext output, copy the schema and add the annotations block after `imports:`:

```yaml
id: https://w3id.org/example
name: example
description: example

annotations:
  list_syntax: plaintext
  list_delimiter: "|"

imports:
- linkml:types
# ... rest of schema
```

Then run with your modified schema:

```bash
linkml-convert -s my_modified_schema.yaml \
  -C Shop -S all_book_series -t tsv \
  tests/linkml_runtime/test_loaders_dumpers/input/books_normalized_01.yaml
```

This produces plaintext output like `scifi|fantasy` (no brackets).

#### Loading plaintext-delimited TSV back to YAML

The annotations also control how TSV data is parsed back into structured YAML.
Given a TSV file with plaintext pipe-delimited values:

| id | name | genres |
|----|------|--------|
| S001 | Lord of the Rings | fantasy |
| S002 | The Culture Series | scifi |
| S003 | Book of the New Sun | scifi\|fantasy |

Using a schema with plaintext annotations:

```bash
linkml-convert -s my_modified_schema.yaml \
  -C Shop -S all_book_series -t yaml \
  my_data.tsv
```

The `scifi|fantasy` value is correctly parsed as a list:

```yaml
all_book_series:
- id: S001
  name: Lord of the Rings
  genres:
  - fantasy
- id: S002
  name: The Culture Series
  genres:
  - scifi
- id: S003
  name: Book of the New Sun
  genres:
  - scifi
  - fantasy
```

## Inference of schemas from tabular data

Use `generalize-tsv` command in the [schema-automator](https://github.com/linkml/schema-automator)
