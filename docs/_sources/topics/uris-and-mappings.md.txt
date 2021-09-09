# URIs and Mappings

### exact_mappings

The `exact_mappings` slot can be used to define external concepts, predicates, or properties which are considered to be exact mappings to the class (or slot) being defined.


```yaml
  same as:
    is_a: exact match
    description: >-
      holds between two entities that are considered equivalent to each other
    in_subset:
      - translator_minimal
    exact_mappings:
      - owl:sameAs
      - skos:exactMatch
      - WIKIDATA_PROPERTY:P2888
      - CHEMBL.MECHANISM:equivalent_to
      - MONDO:equivalentTo
```

Here we define a list of 5 predicates that are semantically equivalent to the Biolink Model predicate slot `same as`.


### close_mappings

The `close_mappings` slot can be used to define external concepts, predicates, or properties which are considered to be close mappings to the class (or slot) being defined.

```yaml
  same as:
    is_a: exact match
    description: >-
      holds between two entities that are considered equivalent to each other
    in_subset:
      - translator_minimal
    exact_mappings:
      - owl:sameAs
      - skos:exactMatch
      - WIKIDATA_PROPERTY:P2888
      - CHEMBL.MECHANISM:equivalent_to
      - MONDO:equivalentTo
    close_mappings:
      - owl:equivalentClass
```

Here we define `owl:equivalentClass` as being a close match to the Biolink Model predicate slot `same as`.


### narrow_mappings

The `narrow_mappings` slot can be used to define external concepts, predicates, or properties which are considered to be narrow mappings to the class (or slot) being defined.

```yaml
  same as:
    is_a: exact match
    description: >-
      holds between two entities that are considered equivalent to each other
    in_subset:
      - translator_minimal
    close_mappings:
      - owl:equivalentClass
    exact_mappings:
      - owl:sameAs
      - skos:exactMatch
      - WIKIDATA_PROPERTY:P2888
      - CHEMBL.MECHANISM:equivalent_to
      - MONDO:equivalentTo
    narrow_mappings:
      - DRUGBANK:external-identifier
```

Here we define `DRUGBANK:external-identifier` as being a narrow match to the predicate slot `same as`.

By narrow we mean that the scope of `DRUGBANK:external-identifier` is more narrower and restrictive than `same as`.

If we were to create a new predicate slot as a proxy for `DRUGBANK:external-identifier` then that new slot would be a child of `same as`.


### broad_mappings

The `broad_mappings` slot can be used to define external concepts, predicates, or properties which are considered to be broad mappings to the class (or slot) being defined.

```yaml
  in complex with:
    description: >-
      holds between two genes or gene products that are part of (or code for products that are part of) in the same macromolecular complex
    is_a: coexists with
    domain: gene or gene product
    range: gene or gene product
    in_subset:
      - translator_minimal
    broad_mappings:
      - SIO:010285
```

Here we define `SIO:010285` (molecular complex formation) as a broad mapping to the predicate slot `in complex with`. 

By broad we mean that the scope of `SIO:010285` is more broad and relaxed than `in complex with`.

If we were to create a new predicate slot as a proxy for `SIO:010285` then that new slot would be a parent of `in complex with`.


### related_mappings

The `related_mappings` slot can be used to define external concepts, predicates, or properties which are considered to be related mappings to the class (or slot) being defined.

```yaml
  in complex with:
    description: >-
      holds between two genes or gene products that are part of (or code for products that are part of) in the same macromolecular complex
    is_a: coexists with
    domain: gene or gene product
    range: gene or gene product
    in_subset:
      - translator_minimal
    broad_mappings:
      - SIO:010285
    related_mappings:
      - SIO:010497
```

Here we define `SIO:010497` (protein complex) as a related mapping to the predicate slot `in complex with`.

By related we mean that the scope of `SIO:010497` is related to the predicate slot `in complex with` and it's difficult to infer any further granularity.

### slot_uri

The `slot_uri` slot can be used to define a canonical URI that is the true representation for that particular slot. That is, the value of `slot_uri` can be used interchangably with the slot being defined.

```yaml
  name:
    is_a: node property
    aliases: ['label', 'display name']
    domain: named thing
    range: label type
    slot_uri: rdfs:label
```

Here we define `rdfs:label` as the canonical URI for the property slot `name`. When serializing a graph into RDF, the name of an instance of entity class `named thing` will be represented using `rdfs:label` instead of `biolink:name`.

This is to ensure that we use certain core RDF predicates as is.



### id_prefixes

The `id_prefixes` slot can be used to define a list of valid ID prefixes that instances of this class ought to have as part of their CURIE.

The order of the list matters since its a prioritized list with the ID prefix with the highest priority appearing at the top of the list.

```yaml
  gene:
    is_a: gene or gene product
    aliases: ['locus']
    slots:
      - id
      - name
      - symbol
      - description
      - synonym
      - xref
    mappings:
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






