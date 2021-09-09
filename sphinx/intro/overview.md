# LinkML at a glance

LinkML is a flexible modeling language that allows you to author
[schemas](https://w3id.org/linkml/SchemaDefinition) ("models") in YAML that describe the structure of your
data. The language is designed to allow for both simple use cases such
as describing the column headers in a spreadsheet through to creating
a complex interlinked schema.

LinkML is designed to work in harmony with other frameworks, including
both semantic RDF-based frameworks as well as frameworks more familiar
to developers such as JSON.

## Introductory Example

See [PersonSchema](https://github.com/linkml/linkml/tree/main/examples/PersonSchema)

```yaml
classes:
  NamedThing:
    slots:
      - id
      - name
      - description
      - image
    ...
  Person:
    is_a: NamedThing
    slots:
      - primary_email
      - birth_date
      - age_in_years
      - gender
      - current_address
      - has_employment_history
      - has_familial_relationships
      - has_medical_history
...
```

## Features

- Rich modeling features including
    - [Polymorphism/Inheritance](../schemas/inheritance), including mixins/traits
    - [Semantic enumerations](../schema/enums)
- Leverages and interoperates with many [existing frameworks](../generators)
    - JSON-Schema
    - ShEx
    - OWL
    - Python dataclasses
- Turnkey solutions for generating a project plus documentation hosted on GitHub
- Ability to work with JSON, YAML, TSVs, SQL databases, RDF/JSON-LD

## Metamodel

The LinkML schema language is itself defined in LinkML

See the [linkml-model reference](https://linkml.github.io/linkml-model/docs/).

## Design your own models

LinkML models can be easily authored as YAML files. See [examples](../examples) for inspiration.

You can also bootstrap a model by converting from existing schema representations, or by inference from existing data

