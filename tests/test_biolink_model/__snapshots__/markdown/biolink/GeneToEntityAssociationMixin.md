
# Class: gene to entity association mixin




URI: [biolink:GeneToEntityAssociationMixin](https://w3id.org/biolink/vocab/GeneToEntityAssociationMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[GeneOrGeneProduct]<subject%201..1-++[GeneToEntityAssociationMixin],[GeneToPhenotypicFeatureAssociation]uses%20-.->[GeneToEntityAssociationMixin],[GeneToPathwayAssociation]uses%20-.->[GeneToEntityAssociationMixin],[GeneToDiseaseAssociation]uses%20-.->[GeneToEntityAssociationMixin],[DruggableGeneToDiseaseAssociation]uses%20-.->[GeneToEntityAssociationMixin],[GeneToPhenotypicFeatureAssociation],[GeneToPathwayAssociation],[GeneToDiseaseAssociation],[GeneOrGeneProduct],[DruggableGeneToDiseaseAssociation])](https://yuml.me/diagram/nofunky;dir:TB/class/[GeneOrGeneProduct]<subject%201..1-++[GeneToEntityAssociationMixin],[GeneToPhenotypicFeatureAssociation]uses%20-.->[GeneToEntityAssociationMixin],[GeneToPathwayAssociation]uses%20-.->[GeneToEntityAssociationMixin],[GeneToDiseaseAssociation]uses%20-.->[GeneToEntityAssociationMixin],[DruggableGeneToDiseaseAssociation]uses%20-.->[GeneToEntityAssociationMixin],[GeneToPhenotypicFeatureAssociation],[GeneToPathwayAssociation],[GeneToDiseaseAssociation],[GeneOrGeneProduct],[DruggableGeneToDiseaseAssociation])

## Mixin for

 * [DruggableGeneToDiseaseAssociation](DruggableGeneToDiseaseAssociation.md) (mixin) 
 * [GeneToDiseaseAssociation](GeneToDiseaseAssociation.md) (mixin) 
 * [GeneToPathwayAssociation](GeneToPathwayAssociation.md) (mixin)  - An interaction between a gene or gene product and a biological process or pathway.
 * [GeneToPhenotypicFeatureAssociation](GeneToPhenotypicFeatureAssociation.md) (mixin) 

## Referenced by Class


## Attributes


### Own

 * [gene to entity association mixin➞subject](gene_to_entity_association_mixin_subject.md)  <sub>1..1</sub>
     * Description: gene that is the subject of the association
     * Range: [GeneOrGeneProduct](GeneOrGeneProduct.md)
