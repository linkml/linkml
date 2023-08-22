# Using ontology terms as values in data

Let's say we want to model associations between genes and phenotypes.

In the simplest case, this might be communicated by a two-column file

|Gene|Phenotype|
|---|---|
|PEX1|Seizure|
|PEX1|Hypotonia|

We might prefer to use standard identifiers:

|Gene|Phenotype|
|---|---|
|NCBIGene:5189|HP:0001250|
|NCBIGene:5189|HP:0001252|

Or perhaps a denormalized representation:

|Gene|Gene Label|Phenotype|Phenotype Label|
|---|---|---|---|
|NCBIGene:5189|PEX1|HP:0001250|Seizure|
|NCBIGene:5189|PEX1HP:0001252|Hypotonia|

Let's focus on a model without the labels for now.

The simplest data model that could work for this case is:

```yaml
classes:
 GenePhenotypeAssociation:
   attributes:
     gene:
     phenotype:
```

However, this isn't quite satisfactory - it allows the data provider to put any free text they like in.

Let's constrain it a bit more:

```yaml
classes:
 GenePhenotypeAssociation:
   attributes:
     gene:
       range: uriorcurie
     phenotype:
       range: uriorcurie
```

We might be tempted to constrain it further:

```yaml
classes:
 GenePhenotypeAssociation:
   attributes:
     gene:
       range: uriorcurie
       pattern: "NCBIGene:\d+"
     phenotype:
       range: uriorcurie
       pattern: "HP:\d+"
```

Let's go one step further, and make a *class* for gene and phenotype:

```yaml
classes:
 GenePhenotypeAssociation:
   attributes:
     gene:
       range: Gene
     phenotype:
       range: Phenotype
       pattern: "HP:\d+"
 Gene:
   attributes:
     id:
       range: uriorcurie
     label:
 Phenotype:
   attributes:
     id:
       range: uriorcurie
     label:
```

We can abstract it a bit further to avoid repetition:

```yaml
classes:
 GenePhenotypeAssociation:
   attributes:
     gene:
       range: Gene
     phenotype:
       range: Phenotype
       pattern: "HP:\d+"
 NamedThing:
   attributes:
     id:
       range: uriorcurie
     label:
 Gene:
  is_a: NamedThing
 Phenotype:
  is_a: NamedThing
```

Note that inlining is non-default if a referenced entity has an identifiers. This means
that the right way to represent an association in a nested tree-like format like YAML or JSON is:

```yaml
gene: NCBIGene:5189
phenotype: HP:0001250
```

genes and phenotypes would be separate objects like this:

```yaml
id: HP:0001250
label: Seizure
```

## Ontology classes may be LinkML instances

So far, so good. This should so far be familiar to people who have modeled this kind of
ontological association in JSON-Schema, or relational databases.

However, this could potentially be confusing for people coming from a
particular kind of ontology modeling background, such as OBO. In this
community, a phenotype concepts like "Seizure" (HP:0001250) denotes a
*class*, and there are many such classes in an ontology. Instances of
seizures would be particular instances such as those experienced by an
individual at a particular space and time.

But here we are modeling HP:0001250 as an *instance*. What's going on?

In fact this is quite straightforward - ontology classes (typically
formalized in OWL) and classes in LinkML are not the same thing,
despite the name "class". And instances in LinkML and instances in
realist OBO ontologies are not the same thing.

So long as we realize this, there isn't any issue. Again, this is
usually quite straightforward for data modelers coming from a
traditional data modeling background, but some people coming from an
ontology background might get tripped up.

## Ontology class hierarchies and LinkML class hierarchies need not be mirrored.

Consider a schema that models both individual people and organisms, as well as taxonomic concepts
such as Homo sapiens or Vertebrate:

```yaml
classes:
 NamedThing:
   attributes:
     id:
       range: uriorcurie
     label:
 IndividualOrganism:
  is_a: NamedThing
  attributes:
    species:
      range: Species
  examples:
    - description: Seabiscuit the horse
    - description: Napoleon Bonaparte
 OrganismTaxonomicConcept:
  is_a: NamedThing
  abstract: true
  attributes:
    parent_concept:
      range: OrganismTaxonomicConcept
 Species:
  is_a: OrganismTaxonomicConcept
  examples:
    - description: Homo sapiens
    - description: Felis catus
 Genus:
  is_a: OrganismTaxonomicConcept
  examples:
    - description: Homo
    - description: Felis
```

Note we have decided to make subclasses of a generic taxon concept class for different taxonomic ranks
(we only should species and genus but we could add more).

Individual organisms are connected to species via a `species`
attribute, and species are connected up to parent taxa via a
`parent_concept` attribute.


IndividualOrganism:
```yaml
id: wikidata:Q517
label: Napoleon Bonaparte
species: NCBITaxon:9606
```

Species:
```yaml
id: NCBITaxon:9606
label: Homo sapiens
parent_concept: NCBITaxon:9605
```

Again, this should not be such a foreign way of modeling things from a standard database perspective.
But if you are coming from ontology modeling this could be confusing.

Consider how this is modeled in ontologies in OBO or clinical terminologies like SNOMED or NCIT.
In these ontologies, there is neither a "individual organism" class nor classes for ranks like "species".

Instead there is just a hierarchy of organism OWL classes, increasingly refined:

* Organism
    * Vertebrate
        * Homo
            * Homo sapiens

Intermediate nodes omitted for brevity. Individual organisms like Napolean instantiate these classes:

```rdf
wikidata:Q517 rdf:type NCBITaxon:9606 .
NCBITaxon:9606 rdfs:subClassOf NCBITaxon:9605
```

Compare to the RDF serialization of the LinkML instances:

```rdf
wikidata:Q517 my:species NCBITaxon:9606 .
NCBITaxon:9606 my:parent_concept NCBITaxon:9605
```

        
Note in this case, `rdf:type` corresponds roughly to the `species` attribute in the LinkML model. It's not quite the same, as we might have the following OWL:

```rdf
wikidata:Q517 rdf:type NCBITaxon:9605 .  ## Homo
```

This is valid (and entailed) but less specific

We might even have:


```rdf
wikidata:Q517 rdf:type My:HistoricPerson .
My:HistoricPerson rdfs:subClassOf NCBITaxon:9606 .
```

Note also the correspondence between the owl SubClassOf axiom and the 'parent_concept` attribute in our LinkML model.
These would correspond even further if we extended our model to other taxonomic ranks.

We could map these using `slot_uri`:

```yaml
classes:
 NamedThing:
   attributes:
     id:
       range: uriorcurie
     label:
 IndividualOrganism:
  is_a: NamedThing
  attributes:
    species:
      range: Species
      slot_uri: rdf:type
  examples:
    - description: Seabiscuit the horse
    - description: Napoleon Bonaparte
 OrganismTaxonomicConcept:
  is_a: NamedThing
  abstract: true
  attributes:
    parent_concept:
      range: OrganismTaxonomicConcept
      slot_uri: rdfs:subClassOf
 Species:
  is_a: OrganismTaxonomicConcept
  examples:
    - description: Homo sapiens
    - description: Felis catus
 Genus:
  is_a: OrganismTaxonomicConcept
  examples:
    - description: Homo
    - description: Felis
```

The LinkML instances now serialize as:

```rdf
wikidata:Q517 rdf:type NCBITaxon:9606 .
NCBITaxon:9606 rdfs:subClassOf NCBITaxon:9605
```

## Mirroring hierarchies

* schema.org
* biolink



