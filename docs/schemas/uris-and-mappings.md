# URIs and Mappings

One feature that sets LinkML apart from frameworks such as JSON-Schema and UML is that fact that each element of your schema has a globally unique [IRI/URI](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier). This is somewhat hidden behind the scenes, so you can ignore this feature if you like, but it is also very easy to use this, which can provide benefits in terms of reusing and linking schemas, and working with the linked data stack.

## background: URIs, IRIs, and CURIEs

URIs and IRIs are generalizations of URLs. URIs are used as identifiers in linked data standards and vocabularies.

For example, in [schema.org](http://schema.org), the URI [http://schema.org/Person](http://schema.org/Person) is the identifier for the Person concept.

URIs can be shortened as CURIEs (Compact URIs). Given a prefix declaration where we map `schema` to `http://schema.org/`, then we can use the CURIE `schema:Person` to denote the person concept.

For more on URIs and their importance in Linked Data, see

- [Linked Data](https://www.w3.org/DesignIssues/LinkedData.html) by Tim Berners-Lee from 2006
- [What are URIs?](https://www.cogsci.ed.ac.uk/~ht/WhatAreURIs/) by Henry S Thompson from 2010

## URI Prefixes

A typical header for a linkml schema may look like this:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
default_curi_maps:
  - semweb_context
prefixes:
  personinfo: https://w3id.org/linkml/examples/personinfo/
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  prov: http://www.w3.org/ns/prov#
default_prefix: personinfo

emit_prefixes:
  - rdf
  - rdfs
  - xsd
  - skos
imports:
  - linkml:types
```

The [prefixes](https://w3id.org/linkml/prefixes) section contains a list of prefix expansions that can be used to specify CURIEs. Additionally, prefixmaps can be imported from prefixcommons.

With the above prefixmap, the CURIE `schema:Person` will expand to http://schema.org/Person

LinkML also provides a way to import prefix maps to avoid repetitively declaring them, through
[default_curi_maps](https://w3id.org/linkml/default_curi_maps). However, we now consider it
best practice to explicitly declare prefix maps, and to use the linter to check for
consistency with standard prefix registries like bioregistry and prefix.cc.

## class uri and slot uri

Slot and class URIs in LinkML provide the *meaning* for a class or slot, and give a robust and unique place to consistently find information about a class or slot in a LinkML model on the web.

The two metamodel slots

 * [class_uri](https://w3id.org/linkml/class_uri)
 * [slot_uri](https://w3id.org/linkml/slot_uri)

can be used to declare URIs for classes and slots respectively. These are typically specified as CURIEs.

```yaml
classes:

  Person:
    is_a: NamedThing
    description: >-
      A person (alive, dead, undead, or fictional).
    class_uri: schema:Person
  ...

slots:
  id:
    identifier: true
    slot_uri: schema:identifier
  name:
    slot_uri: schema:name
  ...
```

When a [JSON-LD context is generated](../generators/jsonld-context) for this schema, it will map json elements to their full linked data IRIs

If class and slot uris are omitted, then they are still generated behind the scenes, using the [default_prefix](https://w3id.org/linkml/default_prefix) slot at the schema level

For example, if Person did not declare a class_uri, then a CURIE `personinfo:Person` would be used, which would expand to `https://w3id.org/linkml/examples/personinfo/Person`


## Enumerations and the meaning slot

The metamodel slot [meaning](https://w3id.org/linkml/meaning) Can be optionally used with a [PermissibleValue](https://w3id.org/linkml/PermissibleValue) as part of an *enumeration*

For example, two of the permissible values in the following enumeration map to ontology terms via `meaning`:

```yaml
enums:
  PersonStatus:
    permissible_values:
      ALIVE:
        description: the person is living
        meaning: PATO:0001421 
      DEAD:
        description: the person is deceased
        meaning: PATO:0001422
      UNKNOWN:
        description: the vital status is not known
        todos:
          - map this to an ontology
```

## Relationship to ISO-11179-3

The LinkML metamodel is strongly influenced by and attempts to conform to the model in [ISO/IEC 11179-3](https://www.iso.org/standard/50340.html) - Metadata registries -- Part 3: Registry metamodel and basic attributes.

For those familiar with the ISO 11179-3 model, the class_uri identifies the object class referenced by the data element.  The slot_uri names the particular property.

For more, see this short slide deck:

<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vQyQsRIBjSxhaDie5ASDAOTfJO9JqFjYmdoBHgCVVKMHzKo0AyL04lGNqWdgbCnyV8a-syk1U81tRXg/embed?start=false&loop=false&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>


## mappings

You may wish to avoid committing to completely reusing a linked data concept, whilst wanting to retain a mapping. LinkML makes use of [SKOS predicates](https://www.w3.org/2004/02/skos/) as metamodel slots:

Example:

```yaml
  NamedThing:
    description: >-
      A generic grouping for any identifiable entity
    slots:
      - id
      - name
      - description
      - image
    close_mappings:
     - schema:Thing
```


## id_prefixes

The [id_prefixes](https://w3id.org/linkml/id_prefixes) slot can be used to define a list of valid ID prefixes that instances of this class ought to have as part of their CURIE.

The order of the list matters since its a prioritized list with the ID prefix with the highest priority appearing at the top of the list.

For example, the biolink model defines a list of allowed id_prefixes for gene objects:

```yaml
  gene:
    slots:
      - id
      - name
      - symbol
      - description
      - synonym
      - xref
    exact_mappings:
      - SO:0000704
      - SIO:010035
      - WIKIDATA:Q7187
    id_prefixes:
      - NCBIGene
      - ENSEMBL
      - HGNC
      - UniProtKB
      - MGI
      - ZFIN
      - dictyBase
      - WB
      - WormBase
      - FlyBase
      - FB
      - RGD
      - SGD
      - PomBase
```

Here we define the entity class `gene` to have a list of ID prefixes with `NCBIGene` having the highest priority.

## See Also

[this notebook](https://github.com/linkml/linkml/blob/main/notebooks/context_issue.ipynb) demonstrates some potential pitfalls of JSON-LD 1.0 with some forms of CURIEs




