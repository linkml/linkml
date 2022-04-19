# LinkML at a glance

LinkML is a flexible modeling language that allows you to author
[schemas](https://w3id.org/linkml/SchemaDefinition) ("models") in YAML that describe the structure of your
data. The language is designed to allow for both simple use cases such
as describing the column headers in a spreadsheet through to creating
a complex interlinked schema.

LinkML is designed to work in harmony with other frameworks, including
both semantic RDF-based frameworks as well as frameworks more familiar
to developers such as JSON.

## Feature: Easy to author schemas

LinkML models are organized around the core concepts of **Classes**
and **Slots**. They are authored in YAML and allow both rich
expressivity while keeping things simple in a way that allows
non-technical domain modelers to contribute.

Example schema fragment, for modeling people:

```yaml
classes:
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
      - current_address
      - has_employment_history
      - has_familial_relationships
      - has_medical_history
...
```

See [PersonSchema](https://github.com/linkml/linkml/tree/main/examples/PersonSchema) for the complete example

## Feature: Rich modeling language

LinkML offers many features of use to data modelers, while retaining a simple core

- Classes can be arranged in [inheritance hierarchies](../schemas/inheritance)
- Powerful [Semantic enumerations](../schema/enums) that can optionally be backed by ontologies
- Create data models that are independent of a database technology
- Ability to provide rich annotations, metadata, and mappings as part of a model
- "Linked Data" ready
   - All schemas have a corresponding JSON-LD context
   - Compatability with RDF tooling, without committing to an RDF stack

## A bridge between frameworks

Many frameworks lock you in to a particular view of the world or
technology. This can lead to silos, and the need to create mappings
and transformations between different representations of the same
data; for example, if your JSON documents need to work in concert with
your relational database or graph store.

LinkML has many different generators [existing
frameworks](../generators) that allow the translation of a LinkML
schema to other frameworks:

- Convert to JSON-LD contexts, and instantly port your data to RDF
- Convert to JSON-Schema and using JSON-Schema validators
- Convert to ShEx and validate your data as RDF
- Convert to Python dataclasses for easy use within applications

## Feature: Generation of documentation and websites

Using the LinkML toolchain you can go from a schema to statically
hosted searchable website in minutes, with pages for each of your
schema elements. Using lightweight namespace registries such as
w3id.org you can easily have resolvable URIs for all your concepts.

## A rapidly growing toolchain

The core LinkML toolchain allows for:

- conversion between JSON, TSV, and RDF
- data validation of JSON, TSVs, or RDF using either JSON-Schema, SPARQL, or ShEx
- easy programmatic manipulation of schemas

LinkML is part of a growing [ecosystem](../ecosystem) of general purpose tools that make curating, mapping, ingesting, and organizing data much easier

 - [linkml-model-enrichment](https://github.com/linkml/linkml-model-enrichment) bootstraps schemas from existing structured and semi-structured sources
 - [linkml-owl](https://github.com/linkml/linkml-owl) allows for generation of complex OWL axioms from datamodels
 - [DataHarmonizer](https://github.com/Public-Health-Bioinformatics/DataHarmonizer) is a ontology-based curation tool that is being adapter to LinkML

## We eat our own dogfood!

The LinkML schema language is itself defined in LinkML, and we use our own toolchain for working with it!

For example, the [linkml-model reference](https://linkml.github.io/linkml-model/docs/) is generated from the [source metamodel](https://github.com/linkml/linkml-model/tree/main/linkml_model/model/schema)

## More examples

See the [examples](../examples)

