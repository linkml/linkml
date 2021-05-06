
# Class: OrganismTaxon


A classification of a set of organisms. Example instances: NCBITaxon:9606 (Homo sapiens), NCBITaxon:2 (Bacteria). Can also be used to represent strains or subspecies.

URI: [biolink:OrganismTaxon](https://w3id.org/biolink/vocab/OrganismTaxon)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[ThingWithTaxon],[TaxonomicRank],[OrganismTaxonToOrganismTaxonSpecialization],[OrganismTaxonToOrganismTaxonInteraction],[OrganismTaxonToOrganismTaxonAssociation],[OrganismTaxonToEnvironmentAssociation],[OrganismTaxonToEntityAssociation],[OrganismTaxon]<subclass%20of%200..*-++[OrganismTaxon],[TaxonomicRank]<has%20taxonomic%20rank%200..1-++[OrganismTaxon],[ThingWithTaxon]++-%20in%20taxon%200..*>[OrganismTaxon],[OrganismTaxonToEntityAssociation]++-%20subject%201..1>[OrganismTaxon],[OrganismTaxonToEnvironmentAssociation]++-%20subject%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonAssociation]++-%20object%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonAssociation]++-%20subject%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonInteraction]++-%20object%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonInteraction]++-%20subject%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonSpecialization]++-%20object%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonSpecialization]++-%20subject%201..1>[OrganismTaxon],[OrganismTaxon]^-[BioticExposure],[OntologyClass]^-[OrganismTaxon],[OntologyClass],[BioticExposure])

## Identifier prefixes

 * NCBITaxon
 * MESH

## Parents

 *  is_a: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Children

 * [BioticExposure](BioticExposure.md) - An external biotic exposure is an intake of (sometimes pathological) biological organisms (including viruses).

## Referenced by class

 *  **[ThingWithTaxon](ThingWithTaxon.md)** *[in taxon](in_taxon.md)*  <sub>0..*</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToEntityAssociation](OrganismTaxonToEntityAssociation.md)** *[organism taxon to entity association➞subject](organism_taxon_to_entity_association_subject.md)*  <sub>REQ</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToEnvironmentAssociation](OrganismTaxonToEnvironmentAssociation.md)** *[organism taxon to environment association➞subject](organism_taxon_to_environment_association_subject.md)*  <sub>REQ</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToOrganismTaxonAssociation](OrganismTaxonToOrganismTaxonAssociation.md)** *[organism taxon to organism taxon association➞object](organism_taxon_to_organism_taxon_association_object.md)*  <sub>REQ</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToOrganismTaxonAssociation](OrganismTaxonToOrganismTaxonAssociation.md)** *[organism taxon to organism taxon association➞subject](organism_taxon_to_organism_taxon_association_subject.md)*  <sub>REQ</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToOrganismTaxonInteraction](OrganismTaxonToOrganismTaxonInteraction.md)** *[organism taxon to organism taxon interaction➞object](organism_taxon_to_organism_taxon_interaction_object.md)*  <sub>REQ</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToOrganismTaxonInteraction](OrganismTaxonToOrganismTaxonInteraction.md)** *[organism taxon to organism taxon interaction➞subject](organism_taxon_to_organism_taxon_interaction_subject.md)*  <sub>REQ</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToOrganismTaxonSpecialization](OrganismTaxonToOrganismTaxonSpecialization.md)** *[organism taxon to organism taxon specialization➞object](organism_taxon_to_organism_taxon_specialization_object.md)*  <sub>REQ</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToOrganismTaxonSpecialization](OrganismTaxonToOrganismTaxonSpecialization.md)** *[organism taxon to organism taxon specialization➞subject](organism_taxon_to_organism_taxon_specialization_subject.md)*  <sub>REQ</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxon](OrganismTaxon.md)** *[organism taxon➞subclass of](organism_taxon_subclass_of.md)*  <sub>0..*</sub>  **[OrganismTaxon](OrganismTaxon.md)**

## Attributes


### Own

 * [organism taxon➞has taxonomic rank](organism_taxon_has_taxonomic_rank.md)  <sub>OPT</sub>
     * range: [TaxonomicRank](TaxonomicRank.md)
 * [organism taxon➞subclass of](organism_taxon_subclass_of.md)  <sub>0..*</sub>
     * Description: subclass of holds between two taxa, e.g. human subclass of mammal
     * range: [OrganismTaxon](OrganismTaxon.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | taxon |
|  | | taxonomic classification |
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | WIKIDATA:Q16521 |
| **Narrow Mappings:** | | UMLSSC:T005 |
|  | | UMLSST:virs |
|  | | UMLSSC:T007 |
|  | | UMLSST:bact |
|  | | UMLSSC:T194 |
|  | | UMLSST:arch |
|  | | UMLSSC:T204 |
|  | | UMLSST:euka |
|  | | UMLSSC:T002 |
|  | | UMLSST:plnt |
|  | | UMLSSC:T004 |
|  | | UMLSST:fngs |
|  | | UMLSSC:T008 |
|  | | UMLSST:anim |
|  | | UMLSSC:T010 |
|  | | UMLSST:vtbt |
|  | | UMLSSC:T011 |
|  | | UMLSST:amph |
|  | | UMLSSC:T012 |
|  | | UMLSST:bird |
|  | | UMLSSC:T013 |
|  | | UMLSST:fish |
|  | | UMLSSC:T014 |
|  | | UMLSST:rept |
|  | | UMLSSC:T015 |
|  | | UMLSST:mamm |
|  | | UMLSSC:T016 |
|  | | UMLSST:humn |

