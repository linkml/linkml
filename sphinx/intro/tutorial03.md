# Part 3: Adding constraints and performing validation

Now we will add richer information to our schema, including:

 - adding *range*s for fields such as age
 - using *pattern* to force a field to conform to a regular expression
 - declaring the `id` slot to be an *identifier*
 - declaring the `full_name` slot to be required
 - adding textual descriptions of schema elements

## Example schema

personinfo.yaml:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
  
classes:
  Person:
    attributes:
      id:
        identifier: true     ## unique key for a person
      full_name:
        required: true       ## must be supplied
        description:
          name of the person
      aliases:
        multivalued: true    ## range is a list
        description:
          other names for the person
      phone:
        pattern: "^[\\d\\(\\)\\-]+$"   ## regular expression
      age:
        range: integer       ## an int between 0 and 200
        minimum_value: 0
        maximum_value: 200
  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person
```

We use yaml comment syntax (i.e the part after `#`) for comments - these are ignored by the parser.

Note that we haven't declared ranges for some fields, but the *default_range* directive at the schema level ensures things default to string.

## Example data

Let's deliberately introduce some bad data to make sure our validator is working:

bad-data.yaml:

```yaml
persons:
  - id: ORCID:1234
    full_name: Clark Kent
    age: 9000
    phone: 1-800-kryptonite
  - id: ORCID:1234
    age: 33
```

Running the following command:

<!-- FAIL -->
```bash
linkml-validate -s personinfo.yaml bad-data.yaml
```

Will result in:

```
ValueError: full_name must be supplied
```

better-data-v1.yaml:

```yaml
persons:
  - id: ORCID:1234
    full_name: Clark Kent
    age: 9000
    phone: 1-800-kryptonite
  - id: ORCID:1234
    full_name: Lois Lane
    age: 33
```

<!-- FAIL -->
```bash
linkml-validate -s personinfo.yaml better-data-v1.yaml
```

Will result in:

```
ValueError: File "<file>", line 6, col 9: ORCID:1234: duplicate key
```

Let's fix that:

better-data-v2.yaml:

```yaml
persons:
  - id: ORCID:1234
    full_name: Clark Kent
    age: 9000
    phone: 1-800-kryptonite
  - id: ORCID:4567
    full_name: Lois Lane
    age: 33
```

<!-- FAIL -->
```bash
linkml-validate -s personinfo.yaml better-data-v2.yaml
```

Will result in:

```
{'pattern': '^[\\d\\(\\)\\-]+$', 'type': 'string'}

On instance['persons'][0]['phone']:
    '1-800-kryptonite'
```
## Exercises

 1. See if you can iterate on the example file to get something that works.

## Using the JSON Schema directly

The `linkml-validate` command is a wrapper than can be used for an
open-ended number of validator implementations. The current default is
to use a JSON Schema validator. This involves converting LinkML to
JSON-Schema - note that there are some features of LinkML not
supported by JSON-Schema, so the current validator is not guaranteed
to be complete.

If you prefer you can use your own JSON Schema validator. First compile to jsonschema:

```bash
gen-json-schema personinfo.yaml > personinfo.schema.json
```

<!-- FAIL -->
```bash
jsonschema -i bad-data.yaml personinfo.schema.json
```

In general this should give you similar results, with some caveats:

 - the `linkml-validator` will first perform an internal conversion prior to using the jsonschema validator, and some errors may be caught at that stage
 - the conversion process may mask some errors - e.g. if a slot has range integer and is supplied as a string, implicit conversion is used

See the [JSON-Schema generator](../generators/json-schema) docs for more info on JSON-Schema validation

## Other validation strategies

Other strategies include

 - converting data to a relational database and doing performant evaluation in SQL
 - converting data to RDF and using either Shape validators or SPARQL queries

The next section deals with working with RDF data.

## Further reading

* [Working with Data](../data/working-with-data)
* Metamodel Specification
    * [identifier](https://w3id.org/linkml/identifier) slot
    * [required](https://w3id.org/linkml/required) slot
    * [minimum_value](https://w3id.org/linkml/minimum_value) slot    
    * [maximum_value](https://w3id.org/linkml/maximum_value) slot    
* FAQ:
    - [LinkML vs shape languages](../faq/why-linkml.html#why-should-i-use-linkml-over-shex-shacl)
* Generators:
    - [JSON Schema Generator](../generators/json-schema)
