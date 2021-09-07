# Models

A LinkML model describes the structure of your data. Your data can be
expressed as JSON or YAML files (the default form for LinkML), or as
CSVs, or as a relational database, or even a triplestore or graph
database.

LinkML models are authored as YAML files. These files can be understood as data files that instantiate [SchemaDefinitions](https://w3id.org/linkml/SchemaDefinition) in the LinkML metamodel.

To illustrate we will use the example [PersonSchema](https://github.com/linkml/linkml/tree/main/examples/PersonSchema)

## Model metadata and directives

A LinkML model/schema may have various pieces of metadata associated with it, for example:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
description: |-
  Information about people, based on [schema.org](http://schema.org)
license: https://creativecommons.org/publicdomain/zero/1.0/
default_curi_maps:
  - semweb_context
imports:
  - linkml:types
prefixes:
  personinfo: https://w3id.org/linkml/examples/personinfo/
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  prov: http://www.w3.org/ns/prov#
default_prefix: personinfo
default_range: string
...
```

 * names, identifiers, and metadata
     * [id](https://w3id.org/linkml/id) -- the unique identifier for the schema, as a IRI
     * [name](https://w3id.org/linkml/name) -- the schema name. Use only alphanumeric characters, underscores, and dashes
     * [description](https://w3id.org/linkml/description) -- a summary of the schema. Can include markdown formatting
     * [license](https://w3id.org/linkml/license) -- CC0 recommended
 * modules
     * [imports](https://w3id.org/linkml/imports) -- See [imports](imports)
 * prefix management
     * [prefixes](https://w3id.org/linkml/prefixes) -- A map of prefixes. See [prefixes](prefixes)
     * [default_prefixes](https://w3id.org/linkml/default_prefix) -- The prefix used for all elements in this schema
     * [default_curi_maps](https://w3id.org/linkml/default_curi_maps) -- prefix maps from prefixcommons
 * other
     * [default_range](https://w3id.org/linkml/default_range) -- The default range for all slots

## Classes

Classes provide templates for organizing data. Data objects should instantiate classes in the schema

Example of a class:

```yaml
  Person:
    is_a: NamedThing
    description: >-
      A person (alive, dead, undead, or fictional).
    class_uri: schema:Person
    mixins:
      - HasAliases
    slots:
      - primary_email
      - birth_date
      - age_in_years
      - gender
      - has_employment_history
      - has_familial_relationships
      - has_medical_history
```

See [ClassDefinition](https://w3id.org/linkml/ClassDefinition) for a full list of allowed slots

## Slots

...

See [SlotDefinition](https://w3id.org/linkml/SlotDefinition) for a full list of allowed slots


## Types

...

## Enums


```yaml
enums:
  FamilialRelationshipType:
    permissible_values:
      SIBLING_OF:
      PARENT_OF:
      CHILD_OF:
```

## Subsets

...

