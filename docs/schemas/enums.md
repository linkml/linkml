# Semantic Enumerations

Enumerations are common features in modeling frameworks. These can be
thought of as a "drop-down" of permissible values for a
field/slot. For example, a "vital status" slot may have an enumeration
with permissible values `LIVING` or `DEAD`.

LinkML supports enumerations, and goes beyond what is possible in frameworks like JSON-Schema

- Permissible Values can be mapped to *ontology terms*, enhancing interoperability and FAIRness
- Enumerations can be *static* or *dynamic*, where dynamic enums are defined by a set of constraints (e.g. a branch of an ontology)

## Basic Enums

The core enumeration model is the same as for familiar systems, where there is a set of allowed string values:


```yaml
enums:
  FamilialRelationshipType:
    permissible_values:
      SIBLING_OF:
      PARENT_OF:
      CHILD_OF:
```

You can also make your enums into a richer controlled vocabulary, with definitions built in:

```yaml
enums:
  FamilialRelationshipType:
    permissible_values:
      SIBLING OF:
        description: A family relationship where the two members have a parent on common
      PARENT OF:
        description: A family relationship between offspring and their parent
      CHILD OF:
        description: inverse of the PARENT_OF relationship
```


## Mapping Permissible Values to Ontologies

As an example, we will map the Permissible Values above to terms from the GA4GH [pedigree standard](https://github.com/GA4GH-Pedigree-Standard/) kinship ontology.

We will first add a base prefix declaration (KIN concepts have PURLs of the form http://purl.org/ga4gh/kin.owl#KIN_007):

```yaml
prefixes:
  kin: http://purl.org/ga4gh/kin.owl#
  ...
```

Then further down we can annotate our enums using [meaning](https://w3id.org/linkml/meaning) slots:

```yaml
enums:
  FamilialRelationshipType:
    permissible_values:
      SIBLING OF:
        description: A family relationship where the two members have a parent on common
        meaning: kin:KIN_007
      PARENT OF:
        description: A family relationship between offspring and their parent
        meaning: kin:KIN_003
      CHILD OF:
        description: inverse of the PARENT_OF relationship
        meaning: kin:KIN_002
```


## Working with Enums in Python

Enumerations are mapped directly to Python enums. See

 * [enumerations notebook](https://github.com/linkml/linkml/blob/main/notebooks/enumerations.ipynb)

for examples.

## Dynamic Enums

Starting with LinkML 1.3, enums do not have to be a static hardcoded list; instead they can be *dynamic*, populated by a query.

This allows the enum to be synced with some upstream source, and avoids hardcoding very long lists where there are a lot of possibilities.

There are several metaslots that can be used to support defining constraints for dynamic enums:
- [reachable_from](https://linkml.io/linkml-model/latest/docs/reachable_from/)
- [matches](https://linkml.io/linkml-model/latest/docs/matches/)
- [include](https://linkml.io/linkml-model/latest/docs/include/) / [minus](https://linkml.io/linkml-model/latest/docs/minus/)

The following example uses `reachable_from` to define an enumeration that selects any subtype of "neuron" from the OBO
cell type ontology:

```yaml
enums:
  NeuronTypeEnum:
    reachable_from:
      source_ontology: obo:cl
      source_nodes:
        - CL:0000540 ## neuron
      include_self: false
      relationship_types:
        - rdfs:subClassOf
```

The `matches` metaslot provides an alternative approach using regular expressions to restrict values to a specific set of IRIs
from a source ontology.

This approach is particularly useful for SKOS collections or other non-OWL vocabularies where hierarchical relationships
may not be available or where pattern-based matching is sufficient.

```yaml
enums:
  MarinePlatformCategories:
    matches:
      source_ontology: "SDN:C16"
      identifier_pattern: "http://vocab.nerc.ac.uk/collection/C16/current/.+/"
```

Arbitrarily nested boolean expressions can be used by combining the [include](https://w3id.org/linkml/include) and
[minus](https://w3id.org/linkml/minus) operators to subtract from sets:

```yaml
enums:
  LoincExample:
    enum_uri: http://hl7.org/fhir/ValueSet/example-intensional
    see_also:
      - https://build.fhir.org/valueset-example-intensional.json.html
    include:
      - reachable_from:
          source_ontology: bioregistry:loinc
          source_nodes:
            - LOINC:LP43571-6
          is_direct: true
    minus:
      concepts:
        - LOINC:5932-9
```

Lastly, enums can extend other enums using [inherits](https://w3id.org/linkml/inherits):

```yaml
enums:
  Disease:
    reachable_from:
      source_ontology: bioregistry:mondo
      source_nodes:
        - MONDO:0000001 ## disease or disorder
      is_direct: false
      relationship_types:
        - rdfs:subClassOf
    minus:
      permissible_values:
        root_node:
          meaning: MONDO:0000001 ## disease or disorder

  HumanDisease:
    description: Extends the Disease value set, including NCIT neoplasms, excluding non-human diseases
    inherits:
      - Disease
    include:
      - reachable_from:
          source_ontology: bioregistry:ncit
          source_nodes:
            - NCIT:C3262
    minus:
      - reachable_from:
          source_ontology: bioregistry:mondo
          source_nodes:
            - MONDO:0005583 ## non-human animal disease
          relationship_types:
            - rdfs:subClassOf
      - permissible_values:
          NOT_THIS_ONE:
            meaning: MONDO:9999
            description: Example of excluding a single node
```

## Tooling to support dynamic enums

Different tool chains may choose to implement dynamic enums differently.

For example, if you have a stack that uses JSON-Schema for validation,
then tools may choose to *materialize* a dynamic query into a static
list of terms at the time of schema compilation.

Other tools may choose to perform the query at runtime. For example, a
data entry tool may choose to use an advanced autocomplete API to
restrict autocomplete to defined values.

At this time, tooling support for dynamic enums is maturing, but you
can still go ahead and use them in your schemas. The default behavior
will be too permissive -- however, you still gain additional clarity
in your schema documentation.

The [Ontology Access Kit](https://github.com/INCATools/ontology-access-kit) (OAK)
has a tool called vskit for expanding value sets.

vskit natively supports resolving many OBO ontologies. For ontologies not natively supported within vskit, prefix
resolvers can be declared through a `config.yaml` file, and mapped to various backends such as BioPortal,
Wikidata, or local .ttl files.

To run:

```bash
pip install oaklib
vskit expand -s my_schema.yaml -o my_schema_expanded.yaml
```

Support for `reachable_from` expansions in vskit is limited to OWL ontologies, where each `relationship_type` must be
declared as an `owl:ObjectProperty` in the source ontology.
