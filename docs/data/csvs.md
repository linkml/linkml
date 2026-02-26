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

## Boolean Values

Boolean values in CSV/TSV files can be represented in various ways depending on the source (spreadsheets, databases, etc.). LinkML follows [Postel's law](https://en.wikipedia.org/wiki/Robustness_principle): **be liberal in what you accept, conservative in what you produce**.

- **Loading** (liberal): accepts multiple truthy/falsy representations, extensible per-schema
- **Dumping** (conservative): produces one canonical format, defaulting to `true`/`false`

### Loading Booleans

When loading CSV/TSV data, LinkML coerces string values to booleans for slots with `range: boolean`. The defaults follow pandas/R conventions (case-insensitive):

| Truthy Values | Falsy Values |
|---------------|--------------|
| `T`, `TRUE` (case-insensitive) | `F`, `FALSE` (case-insensitive) |

This coercion is **schema-aware** — only values in slots declared as `range: boolean` are converted. String values like "yes" in a text field remain as strings.

#### Empty strings

Empty strings (`""`) in CSV/TSV are coerced to null regardless of the slot type.

#### Extending the defaults

Many datasets (e.g. NCBI BioSamples, MIxS) use `yes`/`no`, `1`/`0`, or `on`/`off` for boolean values. You can add these via schema annotations or CLI options — they are **added to** the defaults, not replacing them.

**Schema annotations:**

```yaml
id: https://example.org/myschema
name: myschema
annotations:
  boolean_truthy: "yes,on,1"   # comma-separated, case-insensitive
  boolean_falsy: "no,off,0"
```

**CLI options:**

```bash
linkml-convert -s schema.yaml -C Container -S items -t json \
  --boolean-truthy "yes,on,1" \
  --boolean-falsy "no,off,0" \
  input.tsv
```

CLI options extend schema annotations if both are set.

### Dumping Booleans

By default, boolean values are written as lowercase `true`/`false`. This can be changed for interoperability with systems that expect a different format.

#### Schema Annotation

Add the `boolean_output` annotation at the schema level:

```yaml
id: https://example.org/myschema
name: myschema
annotations:
  boolean_output: "yes"  # Write booleans as yes/no
```

Supported values: `true`, `True`, `TRUE`, `yes`, `Yes`, `YES`, `on`, `On`, `ON`, `1`

#### CLI Option

Override the schema annotation with `--boolean-output`:

```bash
linkml-convert -s schema.yaml -C Container -S items -t tsv \
  --boolean-output yes \
  input.yaml
```

### Example

Given this data:

```yaml
items:
  - id: "1"
    is_active: true
  - id: "2"
    is_active: false
```

Default output (`true`/`false`):
```
id	is_active
1	true
2	false
```

With `--boolean-output yes`:
```
id	is_active
1	yes
2	no
```

With `--boolean-output 1`:
```
id	is_active
1	1
2	0
```

## Inference of schemas from tabular data

Use `generalize-tsv` command in the [schema-automator](https://github.com/linkml/schema-automator)
