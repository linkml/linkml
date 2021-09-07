# LinkML at a glance

LinkML is a flexible modeling language that allows you to author
schemas ("models") in YAML that describe the structure of your
data. The language is designed to allow for both simple use cases such
as describing the column headers in a spreadsheet through to creating
a complex interlinked schema.

LinkML is designed to work in harmony with other frameworks, including
both semantic RDF-based frameworks as well as frameworks more familiar
to developers such as JSON.

## Introductory Example

See [PersonSchema](https://github.com/linkml/linkml/tree/main/examples/PersonSchema)

## Language Features

- Polymorphism/Inheritance, see [is_a](https://linkml.github.io/linkml-model/docs/is_a)
- [Abstract](https://linkml.github.io/linkml-model/docs/abstract) and [Mixin](https://linkml.github.io/linkml-model/docs/mixin) classes 
- Control JSON-LD mappings to URIs via [prefix](https://linkml.github.io/linkml-model/docs/prefixes) declarations 
- Ability to refine the meaning of a _slot_ in the context of a particular class via [slot usage](https://linkml.github.io/linkml-model/docs/slot_usage)

## Leveraging Existing Frameworks

LinkML is a general purpose modeling language following object-oriented and ontological principles. LinkML models can be specified in YAML, JSON or RDF.

A variety of artefacts can be generated from the model:
- ShEx
- JSON Schema
- OWL
- Python dataclasses
- UML diagrams
- Markdown pages (for deployment in a GitHub pages site)

...and more.

The documentation can also be viewed on the [LinkML documentation](https://linkml.github.io/linkml-model/docs/).

## Design you model

...

## Installation

...
