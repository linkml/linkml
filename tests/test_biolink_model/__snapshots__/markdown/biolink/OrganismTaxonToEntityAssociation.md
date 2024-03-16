
# Class: organism taxon to entity association


An association between an organism taxon and another entity

URI: [biolink:OrganismTaxonToEntityAssociation](https://w3id.org/biolink/vocab/OrganismTaxonToEntityAssociation)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon]<subject%201..1-%20[OrganismTaxonToEntityAssociation],[OrganismTaxonToOrganismTaxonAssociation]uses%20-.->[OrganismTaxonToEntityAssociation],[OrganismTaxonToEnvironmentAssociation]uses%20-.->[OrganismTaxonToEntityAssociation],[OrganismTaxonToOrganismTaxonAssociation],[OrganismTaxonToEnvironmentAssociation],[OrganismTaxon])](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon]<subject%201..1-%20[OrganismTaxonToEntityAssociation],[OrganismTaxonToOrganismTaxonAssociation]uses%20-.->[OrganismTaxonToEntityAssociation],[OrganismTaxonToEnvironmentAssociation]uses%20-.->[OrganismTaxonToEntityAssociation],[OrganismTaxonToOrganismTaxonAssociation],[OrganismTaxonToEnvironmentAssociation],[OrganismTaxon])

## Mixin for

 * [OrganismTaxonToEnvironmentAssociation](OrganismTaxonToEnvironmentAssociation.md) (mixin) 
 * [OrganismTaxonToOrganismTaxonAssociation](OrganismTaxonToOrganismTaxonAssociation.md) (mixin)  - A relationship between two organism taxon nodes

## Referenced by Class


## Attributes


### Own

 * [organism taxon to entity association➞subject](organism_taxon_to_entity_association_subject.md)  <sub>1..1</sub>
     * Description: organism taxon that is the subject of the association
     * Range: [OrganismTaxon](OrganismTaxon.md)
