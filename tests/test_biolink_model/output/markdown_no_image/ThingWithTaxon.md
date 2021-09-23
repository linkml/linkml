
# Class: thing with taxon


A mixin that can be used on any entity that can be taxonomically classified. This includes individual organisms; genes, their products and other molecular entities; body parts; biological processes

URI: [biolink:ThingWithTaxon](https://w3id.org/biolink/vocab/ThingWithTaxon)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon]<in%20taxon%200..*-%20[ThingWithTaxon],[PopulationOfIndividualOrganisms]uses%20-.->[ThingWithTaxon],[MolecularEntity]uses%20-.->[ThingWithTaxon],[LifeStage]uses%20-.->[ThingWithTaxon],[IndividualOrganism]uses%20-.->[ThingWithTaxon],[DiseaseOrPhenotypicFeature]uses%20-.->[ThingWithTaxon],[AnatomicalEntity]uses%20-.->[ThingWithTaxon],[PopulationOfIndividualOrganisms],[OrganismTaxon],[MolecularEntity],[LifeStage],[IndividualOrganism],[DiseaseOrPhenotypicFeature],[AnatomicalEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon]<in%20taxon%200..*-%20[ThingWithTaxon],[PopulationOfIndividualOrganisms]uses%20-.->[ThingWithTaxon],[MolecularEntity]uses%20-.->[ThingWithTaxon],[LifeStage]uses%20-.->[ThingWithTaxon],[IndividualOrganism]uses%20-.->[ThingWithTaxon],[DiseaseOrPhenotypicFeature]uses%20-.->[ThingWithTaxon],[AnatomicalEntity]uses%20-.->[ThingWithTaxon],[PopulationOfIndividualOrganisms],[OrganismTaxon],[MolecularEntity],[LifeStage],[IndividualOrganism],[DiseaseOrPhenotypicFeature],[AnatomicalEntity])

## Mixin for

 * [AnatomicalEntity](AnatomicalEntity.md) (mixin)  - A subcellular location, cell type or gross anatomical part
 * [DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md) (mixin)  - Either one of a disease or an individual phenotypic feature. Some knowledge resources such as Monarch treat these as distinct, others such as MESH conflate.
 * [IndividualOrganism](IndividualOrganism.md) (mixin)  - An instance of an organism. For example, Richard Nixon, Charles Darwin, my pet cat. Example ID: ORCID:0000-0002-5355-2576
 * [LifeStage](LifeStage.md) (mixin)  - A stage of development or growth of an organism, including post-natal adult stages
 * [MolecularEntity](MolecularEntity.md) (mixin)  - A gene, gene product, small molecule or macromolecule (including protein complex)"
 * [PopulationOfIndividualOrganisms](PopulationOfIndividualOrganisms.md) (mixin)  - A collection of individuals from the same taxonomic class distinguished by one or more characteristics.  Characteristics can include, but are not limited to, shared geographic location, genetics, phenotypes [Alliance for Genome Resources]

## Referenced by Class


## Attributes


### Own

 * [in taxon](in_taxon.md)  <sub>0..\*</sub>
     * Description: connects an entity to its taxonomic classification. Only certain kinds of entities can be taxonomically classified; see 'thing with taxon'
     * Range: [OrganismTaxon](OrganismTaxon.md)
     * in subsets: (translator_minimal)
