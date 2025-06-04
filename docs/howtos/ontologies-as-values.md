# Using ontology terms as values in data

LinkML provides a flexible way of modeling data. LinkML allows for the optional use
of *ontologies*, *vocabularies*, or *controlled vocabularies* to add semantics to
datamodels, for example, by mapping classes or slots to external terms.

This howto guide deals with another use case, where we want to include ontology
elements as data values in our data model. In formal terms, this is called including
ontology elements *in the domain of discourse*.

This is in principle straightforward - we just treat ontology elements
the same way we would any other identifier or object. However, in some
cases, this can lead to confusion about what the respective roles of
the LinkML schema, data, or ontologies are.

## Motivating Example: associations to ontology terms.

Let's say we want to model associations between genes and
phenotypes. This is a standard use case for biological ontologies -
creating *annotations* that associate some kind of entity with a descriptor.

In the simplest case, this might be communicated by a two-column file:

|Gene|Phenotype|
|---|---|
|PEX1|Seizure|
|PEX1|Hypotonia|

This uses labels, which is not best practice; we could instead do this:

|Gene|Phenotype|
|---|---|
|NCBIGene:5189|HP:0001250|
|NCBIGene:5189|HP:0001252|

Or perhaps a denormalized representation:

|Gene|Gene Label|Phenotype|Phenotype Label|
|---|---|---|---|
|NCBIGene:5189|PEX1|HP:0001250|Seizure|
|NCBIGene:5189|PEX1|HP:0001252|Hypotonia|

This is *denormalized* because we end up repeating values.

If we go with a richer data serialization form like YAML, JSON, RDF,
or a relational database model, we can *normalize* this model. For
YAML/JSON this may be implemented by *referencing* objects in another
collection, like this:

```yaml
associations:
  - gene: NCBIGene:5189
    phenotype: HP:0001250
  - gene: NCBIGene:5189
    phenotype: HP:0001252
genes:
  - id: NCBIGene:5189
    label: PEX1
phenotypes:
  - id: HP:0001250
    label: Seizure
  - id: HP:0001252
    label: Hypotonia
```

However, for now let's return to the simple 2-element model:

|Gene|Phenotype|
|---|---|
|NCBIGene:5189|HP:0001250|
|NCBIGene:5189|HP:0001252|

### Simple schema for pairwise associations

The simplest possible data model that could work for this case is:

```yaml
classes:
 GenePhenotypeAssociation:
   attributes:
     gene:
     phenotype:
```

Note that the schema doesn't care that the phenotypes come from an ontology, or that the genes
come from a standard resource - these are just pieces of data.

However, this isn't quite satisfactory - it allows the data provider to put any free text they like in.
We would like to constrain both `gene` and `phenotype` to be identifiers.

We can do this by specifying a [range](https://w3id.org/linkml/range):

```yaml
classes:
 GenePhenotypeAssociation:
   attributes:
     gene:
       range: uriorcurie
     phenotype:
       range: uriorcurie
```

We can constrain it further still, by including a regexp [pattern](https://w3id.org/linkml/pattern):

```yaml
classes:
 GenePhenotypeAssociation:
   attributes:
     gene:
       range: uriorcurie
       pattern: "NCBIGene:\\d+"
     phenotype:
       range: uriorcurie
       pattern: "HP:\\d+"
```

(obviously this constrains the schema so tightly it can't be used
for other phenotype ontologies, which may or may not be what we want).

So far so good. But what if we want to have a data model where we
can communicate information about the genes and phenotypes themselves,
rather than forcing the client to do an external lookup?

Let's go one step further, and make a [class](https://w3id.org/linkml/ClassDefinition) for gene and phenotype:

```yaml
classes:
 GenePhenotypeAssociation:
   attributes:
     gene:
       range: Gene
     phenotype:
       range: Phenotype
 Gene:
   attributes:
     id:
       range: uriorcurie
       identifier: true
       pattern: "NCBIGene:\\d+"
     label:
 Phenotype:
   attributes:
     id:
       range: uriorcurie
       identifier: true
       pattern: "HP:\\d+"
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
 NamedThing:
   attributes:
     id:
       range: uriorcurie
       identifier: true
     label:
 Gene:
  is_a: NamedThing
  id_prefixes:
    - NCBIGene
 Phenotype:
  is_a: NamedThing
  id_prefixes:
    - HP
```

Note we are taking advantage of the `id_prefixes` metaslot, but
strictly speaking this is weaker than the previous regular expression pattern.

### Adding a container

Let's add a *container* class, to allow us to bundle lists of objects inside a single JSON or YAML document:

```
  Container:
    tree_root: true
    attributes:
      genes:
        range: Gene
        inlined_as_list: true
      phenotypes:
        range: Phenotype
        inlined_as_list: true
      associations:
        range: Association
        inlined_as_list: true  ## not necessary as Association has no id

```

Our container class allows genes, phenotypes, plus associations between them to be transmitted as a single YAML/JSON object/document.

Note that [inlining](https://linkml.io/linkml/schemas/inlining.html) is non-default if a referenced entity has an identifier. This means
that the right way to represent associations is using references (like foreign
keys in a relational database):

```yaml
associations:
  - gene: NCBIGene:5189
    phenotype: HP:0001250
  - gene: NCBIGene:5189
    phenotype: HP:0001252
```

### Example of separate collections

We can optionally communicate information about the referenced entities:

```yaml
associations:
  - gene: NCBIGene:5189
    phenotype: HP:0001250
  - gene: NCBIGene:5189
    phenotype: HP:0001252
genes:
  - id: NCBIGene:5189
    label: PEX1
phenotypes:
  - id: HP:0001250
    label: Seizure
  - id: HP:0001252
    label: Hypotonia
```

## Representing the ontology hierarchy as data

It's common practice to separate the ontology representation from the data,
but in some cases it may be useful to transmit everything using the same
schema, sending both associations and ontology classificiation in one YAML/JSON blob.

Let's do that here, by adding a `parents` slot in the schema:

```yaml
 Phenotype:
  is_a: NamedThing
  attributes:
    parents:
      range: Phenotype
      multiavalued: true
      slot_uri: rdfs:subClassOf
```

Note we could call this whatever we like. We include a [slot_uri](https://w3id.org/linkml/slot_uri) declaration
to indicate that this is equivalent to `rdfs:subClassOf`.

This modified schema allows data like:

```yaml
phenotypes:
  - id: HP:0001250
    label: Seizure
    parents:
      - HP:0012638
  - id: HP:0012638
    label:
      - Abnormal nervous system physiology
    parents:
       ...
```

This is very practical - consumers of the data can consume the
associations and the ontology hierarchy together to perform rollup
operations, etc.

The fact that we have two classification systems co-existing (LinkML
is_a hierarchy and ontology hierarchy as data) is not be a cause
for concern.

### Ontology classes may be LinkML instances

So far, so good. This should so far be familiar to people who have
modeled this kind of ontological association in JSON-Schema, or
relational databases.

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
"realist" OBO ontologies are not the same thing.

## Ontology class hierarchies and LinkML class hierarchies need not be mirrored

Next we will look at a more advanced example. Here we will also
talk about how what we are modeling is represented in RDF/OWL, so some
knowledge of these frameworks helps here.

### A model of organisms in LinkML

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

Note here that in the LinkML model, our __classes__ are
*IndividualOrganism*, *Species*, *Genus*, (and potentially other
ranks, and a generic grouping of these). Our __instances__ are
Napoleon, Homo sapiens, Homo.

When we translate the YAML above to RDF we get:

```turtle
wikidata:Q517 rdf:type my:IndividualOrganism .
NCBITaxon:9606 rdf:type my:Species .
NCBITaxon:9606 my:parent_concept NCBITaxon:9605
NCBITaxon:9605 rdf:type my:Genus .
```

In OWL terms, this is called the **ABox**

Our LinkML schema can also be represented as RDF or OWL (formally: **TBox**)

```turtle
my:IndividualOrganism a owl:Class .
my:Genus a owl:Class .
my:Species a owl:Class .
my:Genus rdfs:subClassOf my:OrganismTaxonomicConcept
my:Species rdfs:subClassOf my:OrganismTaxonomicConcept
```

(omitting some axioms for brevity)

Again, this should not be such a foreign way of modeling things from a standard database perspective.
But if you are coming from ontology modeling this could be confusing.

Next, we'll look at an ontologist's way to model the same domain. Let's first summarize the LinkML model:

- Individuals such as Napoleon as well as taxonomic concepts such as human or cat are *instances*
- individuals such as Napoleon instantiate "individual organism", whereas taxonomic concepts instantiate Species, Genus, etc
- we can add more properties and constraints on each LinkML class, e.g.
    - make `species` a required field
    - constrain the parent of `Species` to be a `Genus` rather than any taxonomic concept
    - add appropriate slots to "IndividualOrganism", e.g. a single-value-per-time geolocation
    - add appropriate slots to taxonomic concepts
        - common name vs scientific name
        - constrain species names to be binomial
        - geolocation ranges

From a LinkML modeling perspective, these additional properties would be Good Things. They allow
us to constrain our data model to avoid instance data that is invalid or surprising (for example,
Napoleon having a "species" value of "Vertebrate" or "HistoricHuman").

### A model of organisms following ontology conventions

Consider how this is modeled in ontologies in OBO or clinical terminologies like SNOMED or NCIT.
In these ontologies, there is neither a "individual organism" class nor classes for ranks like "species".

Instead there is just a hierarchy of organism OWL classes, increasingly refined:

* Organism
    * Vertebrate
        * Mammalia
            * Homo
                * Homo sapiens
            * Felis
                * Felis catus
                    * Russian blue


(Intermediate nodes omitted for brevity)

There is also nothing formally prohibiting classes such as
"FriendlyMammal" or "HistoricHuman", but by convention the class
hierarchy mirrors conventional classifications that mirror phylogeny.

In this model there are no logical elements "species" or "genus". It's common practice
to include the taxonomic rank as an OWL *annotation property*. If we want to include these
concepts as true first-class logical citizens in an OWL model, then we need to either introduce
*punning* (OWL-DL) or *metaclasses* (OWL-Full).

In practice, punning or metaclasses are not used much in OWL, so let's stick with the rank-free
model. Formally, concepts like "Homo sapiens" are not in the *domain of discourse*.

Individual organisms like Napoleon (Q517 in Wikidata) instantiate the classes in the hierarchy:

```
wikidata:Q517 rdf:type NCBITaxon:9606 .
NCBITaxon:9606 rdfs:subClassOf NCBITaxon:9605
```

Compare to the RDF serialization of the LinkML instances:

```
wikidata:Q517 my:species NCBITaxon:9606 .
NCBITaxon:9606 my:parent_concept NCBITaxon:9605
```

In this case, `rdf:type` corresponds roughly to the `species` attribute in the LinkML model. It's not quite the same, as we might have the following OWL:

```
wikidata:Q517 rdf:type NCBITaxon:9605 .  ## Homo
```

This is valid (and entailed) but less specific. Note that this would be disallowed
in the LinkML model, which intentionally forces the data provider to provide a species-level
taxon node ID rather than any other taxon ID.

In the RDF model we might even have:


```
wikidata:Q517 rdf:type My:HistoricPerson .
My:HistoricPerson rdfs:subClassOf NCBITaxon:9606 .
```

### Aligning the LinkML model with the ontological model

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
  class_uri: NCBITaxon:1   ## root node of NCBI taxonomy
  is_a: NamedThing
  attributes:
    species:
      range: Species
      slot_uri: rdf:type   ## map species to instantiation predicate
  examples:
    - description: Seabiscuit the horse
    - description: Napoleon Bonaparte
 OrganismTaxonomicConcept:
  is_a: NamedThing
  abstract: true
  attributes:
    parent_concept:
      range: OrganismTaxonomicConcept
      slot_uri: rdfs:subClassOf   ## map parent_concept to subsumption
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

```
wikidata:Q517 rdf:type NCBITaxon:1 .
wikidata:Q517 rdf:type NCBITaxon:9606 .
NCBITaxon:9606 rdf:type my:Species .
NCBITaxon:9606 rdfs:subClassOf NCBITaxon:9605
NCBITaxon:9605 rdf:type my:Genus .
```

Viewed through the lens of RDF/OWL this is potentially
confusing. Under OWL2 Description Logic semantics, we have introduced
*punning*, and under OWL-Full we have *metaclasses*. The latter
approach is quite common in knowledge bases such as Wikidata.

### Separate models

We can imagine people getting confused, and making incorrect inferences
such as the following:

1. Homo sapiens is a Species
2. Species is a Genus
3. Therefore, Homo sapiens is a Genus

Clearly this is wrong. In fact entailment is thankfully not justified
either via the LinkML or via the RDF/OWL (either punning model or metaclass).

The mistake is confusing the different levels of modeling.

## When should hierarchies be mirrored?

It should be clear that LinkML (and more generally, schema and shape
frameworks such as JSON-Schema, SHACL, and so on) and formal OWL
modeling are distinct. By keeping these separate, we avoid problems.

However, there are some cases where hierarchies in our data model do
trivially mirror our ontological hierarchies. There are some schemas
and data models that also resemble upper ontologies.

* schema.org for everyday concepts like Person, CreativeWork
* biolink for biological concepts like Gene, Chemical, Disease
* chemrof for chemical concepts like atom, isotope, molecule

In the case of schema.org, most elements can do double duty as
ontology classes compatible with OBO-style realist modeling (intended
to model the world scientifically) as well as schema classes (intended
to model how we exchange data about the things in the world).

However, this can get quite nuanced. Sometimes there are
classifications that make sense in one perspective and not in the
other.

The modeling of personhood in ontologies can get quite involved. Some
ontologies will treat Person as a subclass of Homo sapiens (which is
scientifically valid but from a modeling perspective mixes two
separate concerns); other ontologies may represent personhood as a
"role", which complicates things if you want to have straightforward
connections between concepts like "Person" and "Address"

This gets even more nuanced with biomedical concepts, where we have to deal with
multiple interlinked ontological debates about modeling concepts like
Gene and Allele, and whether these are classes or instances. Most
bio-ontologies eliminate the concept of "levels" in hierarchies, so
the concepts "eukaroyotic gene", "gene", "human Shh gene" and "human
Shh gene with foo variant" are all valid gene concepts, just at
different levels of the hierarchy.

Additionally, ontologists have a habit of grouping unlike entities or
separating like concepts, on the basis of upper ontologies.

A full discussion of these issues is well outside the scope of this
guide.

From a modeling perspective, the key points are:

- use the appropriate modeling framework for the problem at hand
- mirror hierarchies where appropriate
- do not assume hierarchies must be mirrored
