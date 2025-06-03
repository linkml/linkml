# The metamodel

LinkML is fully described by a *metamodel* that is itself described in LinkML

- [linkml-model repo](https://github.com/linkml/linkml-model/)
- [linkml-model documentation](https://linkml.io/linkml-model/docs/)
- [Part 3](https://linkml.io/linkml-model/docs/specification/03schemas/) of specification

## Metamodel Versioning scheme

The LinkML project uses Semantic Versioning (SemVer)

Note there are a number of different artefacts in the LinkML project

- Core artefacts
   - linkml-model: the metamodel, the actual LinkML standard
   - linkml-runtime
   - linkml
- Additional artefacts
   - linkml-model-enrichment
   - other related projects, e.g. schemasheets

These each have their own distinct versioning schemes, which need not be connected.
Versions are tracked in GitHub, alongside respective PyPI releases.

However, starting with the release of linkml-model 1.2, **core
artefacts version numbers are loosely coupled**:

- The major and minor version should match the major and minor version of the metamodel
- The patch number can vary independently

For example, linkml-runtime 1.5.12 uses the 1.5 series of the metamodel.

## Release Candidates

All release candidates are given a version number `MAJOR.MINOR.PATCHrcNUM`

These are tagged as pre-releases on GitHub

## Metamodel Release Notes

For complete release notes tied to patch releases, see the release notes on GitHub:

- https://github.com/linkml/linkml-model/releases
- https://github.com/linkml/linkml-runtime/releases
- https://github.com/linkml/linkml/releases

### LinkML-Model 1.3

Highlights:

- dynamic enums: restrict slots to ontology terms based on queries
- unit support: annotate slots or types with unit information
- structured patterns: reuse common elements in regular expression pattern constraints
- structured aliases: include provenance of naming information

Complete changelog: https://github.com/linkml/linkml-model/compare/v1.2.0...v1.3.0

### LinkML-Model 1.2

Highlights:

- A richer set of slots that can be used for schema metadata
- The introduction of boolean conditions and rules
- A validation datamodel based on SHACL validation
- A dataset datamodel based on frictionless, void, dcat, and the HCLS dataset description standard
- Ability to constrain field values using regular expressions

Selected Changelog:

- new slot: string serialization https://github.com/linkml/linkml-model/pull/25
- new slot: recommended https://github.com/linkml/linkml-model/pull/26
- unique keys: https://github.com/linkml/linkml-model/pull/16
- data validation datamodel: https://github.com/linkml/linkml-model/pull/42
- pattern on type definitions: https://github.com/linkml/linkml-model/pull/43
- adding conforms_to: https://github.com/linkml/linkml-model/pull/50
- add min-max-val-to-type-expression: https://github.com/linkml/linkml-model/pull/57
- aligning-validation model: https://github.com/linkml/linkml-model/pull/68
- new slot: source: https://github.com/linkml/linkml-model/pull/62
- new slots: relational characteristics: https://github.com/linkml/linkml-model/pull/69
- datasets schema: https://github.com/linkml/linkml-model/pull/67
- reified statements/edge properties: https://github.com/linkml/linkml-model/pull/61
- property groups: https://github.com/linkml/linkml-model/pull/71
- path: https://github.com/linkml/linkml-model/pull/72
- disjoint_with: https://github.com/linkml/linkml-model/pull/78
- structured_alias: https://github.com/linkml/linkml-model/pull/66
- align to skosxl: https://github.com/linkml/linkml-model/pull/86

Complete changelog: https://github.com/linkml/linkml-model/compare/v1.0.0...v1.2.0

Corresponding framework change highlights, from 1.1 (linkml and linkml-runtime):

- dropped support for rdflib5 -- rdflib6 is now required
- Reduced library dependencies
- new generators:
    - SQL DDL
    - SQL Alchemy
    - SHACL
    - Typescript
- Added SchemaView utility

### LinkML-Model 1.0: June 2021

This is the first version of LinkML seeded from the historic BiolinkML project
