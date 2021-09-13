# URIs and Mappings

One feature that sets LinkML apart from frameworks such as JSON-Schema and UML is that fact that each element of your schema has a globally unique IRI/URI. This is somewhat hidden behind the scenes, so you can ignore this feature if you like, but it is also very easy to use this, which can provide benefits in terms of reusing and linking schemas, and working with the linked data stack.

## background: URIs, IRIs, and CURIEs

URIs and IRIs are generalizations of URLs. URIs are used as identifiers in linked data standards and vocabularies.

For example, in [schema.org](http://schema.org), the URI [http://schema.org/Person](http://schema.org/Person) is the identifier for the Person concept.

URIs can be shortended as CURIEs (Compact URIs). Given a prefix declaration where we map `schema` to `http://schema.org/`, then we can use the CURIE `schema:Person` to denote the person concept

## prefixes

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

## class uri and slot uri

The two slots

 * [class_uri](https://w3id.org/linkml/class_uri)
 * [slot_uri](https://w3id.org/linkml/slot_uri)

can be used to declare URIs for classes and slots respectively. These are typically specified as CURIEs

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




