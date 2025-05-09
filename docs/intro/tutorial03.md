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

Depicted as:

![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Container]++-%20persons%200..*>[Person|id:string;full_name:string;aliases:string%20*;phone:string%20%3F;age:integer%20%3F],[Container])

Note that we haven't declared ranges for some fields, but the *default_range* directive at the schema level ensures things default to string.

## Example data

Let's deliberately introduce some bad data to make sure our validator is working:

bad-data.yaml:

```{literalinclude} ../../examples/tutorial/tutorial03/bad-data.yaml
:language: yaml
```

Running the following command will result in errors printed to the console:

<!-- FAIL -->
```bash
linkml-validate -s personinfo.yaml bad-data.yaml
```

Output:

```text
[ERROR] [bad-data.yaml/0] '1-800-kryptonite' does not match '^[\\d\\(\\)\\-]+$' in /persons/0/phone
[ERROR] [bad-data.yaml/0] 'full_name' is a required property in /persons/1
```

This indicates there are two issues with our data. The first says that the phone number of the first entry in the persons list (`/persons/0/phone`) doesn’t conform to the regular expression syntax we stated. The second says that we are missing the required `full_name` slot on the second entry in the person list (`/persons/1`).

Let's fix the second issue.

better-data.yaml:

```{literalinclude} ../../examples/tutorial/tutorial03/better-data.yaml
:language: yaml
```

<!-- FAIL -->
```bash
linkml-validate -s personinfo.yaml better-data.yaml
```

Output:

```text
[ERROR] [better-data.yaml/0] '1-800-kryptonite' does not match '^[\\d\\(\\)\\-]+$' in /persons/0/phone
```

We have successfully fixed one of the issues with the data!

## Exercises

 1. See if you can iterate on the example data to get something that validates.

## Using the JSON Schema directly

The `linkml-validate` command is a wrapper than can be used for an
open-ended number of validator implementations. The current default is
to use a JSON Schema validator. This involves converting LinkML to
JSON-Schema - note that there are some features of LinkML not
supported by JSON-Schema, so the current validator is not guaranteed
to be complete.

If you prefer you can use your own JSON Schema validator. First compile to jsonschema. Unlike the `linkml-validate` command, the `gen-json-schema` command does not attempt to automatically infer which class in your schema to use for validation. You must either identify it in your schema by setting `tree_root: true` on one class or pass the `-t/--top-class` option to `gen-json-schema`.

```bash
gen-json-schema personinfo.yaml --top-class Container > personinfo.schema.json
```

You can then use the `jsonschema` command that comes with the python library (any jsonschema validator will do here)

<!-- Note: this will actually fail when executed because 'bad-data.json' does not exist. -->
<!-- FAIL -->
```bash
jsonschema -i bad-data.json personinfo.schema.json
```

In general this should give you similar results, with some caveats:
 - the `bad-data.yaml` can be converted to `bad-data.json` using https://www.json2yaml.com/.
 - the `linkml-validator` will first perform an internal conversion prior to using the jsonschema validator, and some errors may be caught at that stage
 - the conversion process may mask some errors - e.g. if a slot has range integer and is supplied as a string, implicit conversion is used

See the [JSON-Schema generator](../generators/json-schema) docs for more info on JSON-Schema validation

## Other validation strategies

Other strategies include

 - converting data to a relational database and doing performant evaluation in SQL
 - converting data to RDF and using either Shape validators or SPARQL queries

The next section deals with working with RDF data.

## Further reading

* [Working with Data](/data/index)
* Metamodel Specification
    * [identifier](https://w3id.org/linkml/identifier) slot
    * [required](https://w3id.org/linkml/required) slot
    * [minimum_value](https://w3id.org/linkml/minimum_value) slot
    * [maximum_value](https://w3id.org/linkml/maximum_value) slot
    * [tree_root](https://w3id.org/linkml/tree_root) slot
* FAQ:
    - {ref}`LinkML vs shape languages <faq/why-linkml:why should i use linkml over shex/shacl?>`
* Generators:
    - [JSON Schema Generator](../generators/json-schema)
