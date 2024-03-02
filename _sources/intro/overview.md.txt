# LinkML at a glance

LinkML is a flexible modeling language that allows you to author
[schemas](https://w3id.org/linkml/SchemaDefinition) ("models") in YAML that describe the structure of your
data. The language is designed to allow for both simple use cases such
as describing the column headers in a spreadsheet through to creating
a complex interlinked schema.

LinkML is designed to work in harmony with other frameworks, including
both semantic RDF-based frameworks, as well as frameworks that are more familiar
to developers such as JSON.

- Quick links: [ 
    [Schemas](../schemas/index) | 
    [Spec](../specifications/linkml-spec.md) |
    [Slides](https://www.slideshare.net/cmungall/linkml-intro-july-2022pptx) |
    [Notebooks](https://github.com/linkml/linkml/blob/main/notebooks) |
    [SchemaSheets](https://linkml.io/schemasheets/) |
    [Schema Automator](https://linkml.io/schema-automator/) |
    [FAQ: Why LinkML?](../faq/why-linkml.md) |
    [GitHub](https://github.com/linkml/linkml/)
  ]
- Example schemas: [ 
  [PersonInfo](https://github.com/linkml/linkml/blob/main/examples/PersonSchema/personinfo.yaml) |
  [Biolink](https://github.com/biolink/biolink-model/blob/master/biolink-model.yaml) | 
  [LinkML](https://github.com/linkml/linkml-model/blob/main/linkml_model/model/schema/meta.yaml) |
  [SSSOM](https://github.com/mapping-commons/sssom/blob/master/src/sssom_schema/schema/sssom_schema.yaml)
  ]

## Feature: Easy to author schemas

LinkML models are organized around the core concepts of **Classes**
and **Slots**. They are authored in YAML and allow both rich
expressivity while keeping things simple in a way that allows
non-technical domain modelers to contribute.

Example schema fragment, for modeling a simple "Person" concept:

```yaml
classes:
  Person:
    is_a: NamedThing  ## parent class, defines id, name, ...
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

- Classes can be arranged in [inheritance hierarchies](../schemas/inheritance.md)
- Powerful yet easy to use [Semantic enumerations](../schemas/enums.md) that can optionally be backed by ontologies
- Create [data models](/schemas/index) that are independent of a database technology
- Develop machine-actionable reporting standards and data dictionaries 
- Include rich annotations and [mappings](../schemas/uris-and-mappings.md) as part of a model
- "Linked Data" ready
   - All schemas have a corresponding JSON-LD context
   - [Compatibility with RDF tooling](../data/rdf), without committing to an RDF stack
   - Compilation to [SHACL](../generators/shacl) and [ShEx](../generators/shex)
   - Export of data models to [OWL Schemas](../generators/owl)
  
## A bridge between frameworks

Many frameworks lock you in to a particular view of the world or
technology. This can lead to *silos*, and the need to create mappings
and transformations between different representations of the same
data; for example, if your JSON documents need to work in concert with
your relational database or graph store.

LinkML has [many different generators for existing
frameworks](../generators/index) that allow the translation of a LinkML
schema to other frameworks:

- Convert to JSON-LD contexts, and instantly port your data to RDF
- Convert to [JSON-Schema](../generators/json-schema) and using JSON-Schema validators
- Convert to [SHACL](/generators/shacl) or [ShEx](../generators/shex) and validate your RDF data
- Convert to Python [dataclasses](../generators/python) or  [pydantic](../generators/pydantic) for easy use within applications
- Generate [SQL Schemas](../generators/sqltable) or  [SQL Alchemy](../generators/sqlalchemy) for use with relational databases


## Feature: Generation of documentation and websites

Using the LinkML toolchain you can go from a schema to a statically
hosted searchable website in minutes, with pages for each of your
schema elements. Using lightweight namespace registries such as
w3id.org you can easily have resolvable URIs for all your concepts.

Showcase:

* [Biolink Model docs](https://biolink.github.io/biolink-model/)
* [CCDH Model docs](https://cancerdhc.github.io/ccdhmodel)
* [NMDC docs](https://microbiomedata.github.io/nmdc-schema/)
* [LinkML Metamodel docs](https://w3id.org/linkml/)
* [SSSOM docs](https://w3id.org/sssom/)

## A rapidly growing toolchain

LinkML can be thought of as two interlocking parts:

- A *standard* for representing schemas, data dictionaries, standards, and metadata
- A *reference tool stack* for doing things with artefacts that conform to the standard

The [core LinkML toolchain](https://github.com/linkml/linkml) is written in Python allows for:

- generating downstream schema artefacts, including:
    - documentation and static sites
    - code for use by developers (data class in Python, Java, and Typescript, ORMs, enumerations)
    - conversion between alternate representations like JSON-Schema, SQL DDL, RDF Shapes, Protobuf, ...
- validation and linting of schemas
- data [conversion](../data/conversion) between JSON, TSV, and RDF (where that data *conforms* to a LinkML schema)
- data [validation](../data/validating-data) of JSON, TSVs, or RDF using either JSON-Schema, SPARQL, or ShEx
- easy [programmatic manipulation of schemas](../developers/manipulating-schemas)


LinkML is part of a growing [ecosystem](../ecosystem) of general purpose tools that make curating, mapping, ingesting, and organizing data much easier

- [schema-automator](https://github.com/linkml/schema-automator) bootstraps schemas from existing structured and semi-structured sources
- [LinkML-OWL](https://github.com/linkml/linkml-owl) allows for generation of complex OWL axioms from datamodels
- [SchemaSheets](https://linkml.io/schemasheets/) converts between spreadsheets and schemas
- [DataHarmonizer](https://github.com/Public-Health-Bioinformatics/DataHarmonizer) is an ontology-based curation tool that is being adapted to LinkML

## We eat our own dogfood!

The LinkML schema language is itself [defined in LinkML](https://github.com/linkml/linkml-model/blob/main/linkml_model/model/schema/meta.yaml), and we use our own toolchain for working with it!

## More examples

See the [examples](../examples) pages

