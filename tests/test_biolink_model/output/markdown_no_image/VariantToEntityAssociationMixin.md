
# Class: VariantToEntityAssociationMixin




URI: [biolink:VariantToEntityAssociationMixin](https://w3id.org/biolink/vocab/VariantToEntityAssociationMixin)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SequenceVariant]<subject%201..1-%20[VariantToEntityAssociationMixin],[VariantToPopulationAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToPhenotypicFeatureAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToGeneAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToDiseaseAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToPopulationAssociation],[VariantToPhenotypicFeatureAssociation],[VariantToGeneAssociation],[VariantToDiseaseAssociation],[SequenceVariant])

## Mixin for

 * [VariantToDiseaseAssociation](VariantToDiseaseAssociation.md) (mixin) 
 * [VariantToGeneAssociation](VariantToGeneAssociation.md) (mixin)  - An association between a variant and a gene, where the variant has a genetic association with the gene (i.e. is in linkage disequilibrium)
 * [VariantToPhenotypicFeatureAssociation](VariantToPhenotypicFeatureAssociation.md) (mixin) 
 * [VariantToPopulationAssociation](VariantToPopulationAssociation.md) (mixin)  - An association between a variant and a population, where the variant has particular frequency in the population

## Referenced by class


## Attributes


### Own

 * [variant to entity association mixin➞subject](variant_to_entity_association_mixin_subject.md)  <sub>REQ</sub>
     * Description: a sequence variant in which the allele state is associated with some other entity
     * range: [SequenceVariant](SequenceVariant.md)
     * Example:    
     * Example:    

## Other properties

|  |  |  |
| --- | --- | --- |
| **Local names:** | | variant annotation (ga4gh) |

