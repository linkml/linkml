
# Class: GeneToEntityAssociationMixin




URI: [biolink:GeneToEntityAssociationMixin](https://w3id.org/biolink/vocab/GeneToEntityAssociationMixin)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[GeneOrGeneProduct]<subject%201..1-++[GeneToEntityAssociationMixin],[GeneToPhenotypicFeatureAssociation]uses%20-.->[GeneToEntityAssociationMixin],[GeneToDiseaseAssociation]uses%20-.->[GeneToEntityAssociationMixin],[GeneToPhenotypicFeatureAssociation],[GeneToDiseaseAssociation],[GeneOrGeneProduct])

## Mixin for

 * [GeneToDiseaseAssociation](GeneToDiseaseAssociation.md) (mixin) 
 * [GeneToPhenotypicFeatureAssociation](GeneToPhenotypicFeatureAssociation.md) (mixin) 

## Referenced by class


## Attributes


### Own

 * [gene to entity association mixin➞subject](gene_to_entity_association_mixin_subject.md)  <sub>REQ</sub>
     * Description: gene that is the subject of the association
     * range: [GeneOrGeneProduct](GeneOrGeneProduct.md)
