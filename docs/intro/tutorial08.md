# Part 8: Generating Projects

In previous parts of this tutorial, we have covered

- how to generate JSON-Schema, for use in JSON validation
- how to generate Python classes, for use in code
- how to generate ShEx and JSON-LD contexts, for use with RDF data

Later on we will explore generation of other downstream artefacts like SQL CREATE TABLE statements and markdown documentation.

Even though you don't necessarily need all of these output artefacts,
it can be useful to regularly generate these whenever you change your
schema. The `gen-project` script will do this for you.

## Example

Given a schema:

personinfo.yaml:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:                                 
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
  personinfo: https://w3id.org/linkml/examples/personinfo/
  ORCID: https://orcid.org/
imports:
  - linkml:types
default_range: string
  
classes:
  Person:
    class_uri: schema:Person             
    slots:   ## specified as a list
     - id
     - full_name
     - aliases
     - phone
     - age
    id_prefixes:
      - ORCID
  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person

# slots are first-class entities in the metamodel
# declaring them here allows them to be reused elsewhere
slots:
  id:
    identifier: true
  full_name:
    required: true
    description:
      name of the person
    slot_uri: schema:name
  aliases:
    multivalued: true
    description:
      other names for the person
  phone:
    pattern: "^[\\d\\(\\)\\-]+$"
    slot_uri: schema:telephone 
  age:
    range: integer
    minimum_value: 0
    maximum_value: 200
```

The JSON-Schema that is generated should be the same as in the previous example:

```bash
gen-project -d personinfo/ personinfo.yaml
```

This will place all artefacts in the `personinfo` dir:

```bash
ls personinfo/
```

Outputs:

```text
docs
excel
graphql
java
jsonld
jsonschema
owl
personinfo.py
prefixmap
protobuf
shacl
shex
sqlschema
```


## See Also

### GitHub Guides

We recommend maintaining your source for your schema, plus all generated products in GitHub

Some resources to help you:

* [software carpentry guide](https://swcarpentry.github.io/git-novice/)
* We have created a [slide deck on GitHub](https://docs.google.com/presentation/u/0/d/1ydkB8y3cPYcDZYCT9DcENQk6gwWr0xR6/) for LinkML users

### ProjectGen docs

 * [project-generator](/generators/project-generator)

### linkml-model-template

The [linkml/linkml-model-template](https://github.com/linkml/linkml-model-template) utility will allow you to set up a whole GitHub repository, with a Makefile that can be used to regenerate all downstream products. However, note that this uses an older version of the templates.

### Registering your schema

Once you have authored a schema, generated a full project, and are
managing everything in GitHub, you may want to consider registering
your schema. To do this, make a GitHub Pull Request (PR) on the main
[linkml-registry](https://linkml.io/linkml-registry/home/) metadata
file, which is here:

[https://github.com/linkml/linkml-registry/blob/main/models.yaml](https://github.com/linkml/linkml-registry/blob/main/models.yaml)

