# Part 8: Generating Projects

In previous parts of this tutorial, we have covered

- how to generate JSON-Schema, for use in JSON validation
- how to generate Python classes, for use in code
- how to generate ShEx and JSON-LD contexts, for use with RDF data

Later on we will explore generation of other downstream artefacts like SQL CREATE TABLE statements

It is rare that all of these are useful for all use cases, but it can be useful to pregenerate all these in advance for a project.

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
# delcaring them here allows them to be reused elsewhere
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
shex
sqlschema
```


...
