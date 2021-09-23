
# Class: variant to entity association mixin




URI: [biolink:VariantToEntityAssociationMixin](https://w3id.org/biolink/vocab/VariantToEntityAssociationMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SequenceVariant]<subject%201..1-%20[VariantToEntityAssociationMixin],[VariantToPopulationAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToPhenotypicFeatureAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToGeneAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToDiseaseAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToPopulationAssociation],[VariantToPhenotypicFeatureAssociation],[VariantToGeneAssociation],[VariantToDiseaseAssociation],[SequenceVariant])](https://yuml.me/diagram/nofunky;dir:TB/class/[SequenceVariant]<subject%201..1-%20[VariantToEntityAssociationMixin],[VariantToPopulationAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToPhenotypicFeatureAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToGeneAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToDiseaseAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToPopulationAssociation],[VariantToPhenotypicFeatureAssociation],[VariantToGeneAssociation],[VariantToDiseaseAssociation],[SequenceVariant])

## Mixin for

 * [VariantToDiseaseAssociation](VariantToDiseaseAssociation.md) (mixin) 
 * [VariantToGeneAssociation](VariantToGeneAssociation.md) (mixin)  - An association between a variant and a gene, where the variant has a genetic association with the gene (i.e. is in linkage disequilibrium)
 * [VariantToPhenotypicFeatureAssociation](VariantToPhenotypicFeatureAssociation.md) (mixin) 
 * [VariantToPopulationAssociation](VariantToPopulationAssociation.md) (mixin)  - An association between a variant and a population, where the variant has particular frequency in the population

## Referenced by Class


## Attributes


### Own

 * [variant to entity association mixin➞subject](variant_to_entity_association_mixin_subject.md)  <sub>1..1</sub>
     * Description: a sequence variant in which the allele state is associated with some other entity
     * Range: [SequenceVariant](SequenceVariant.md)
     * Example: ClinVar:38077 ClinVar representation of NM_000059.3(BRCA2):c.7007G>A (p.Arg2336His)
     * Example: ClinGen:CA024716 chr13:g.32921033G>C (hg19) in ClinGen

## Other properties

|  |  |  |
| --- | --- | --- |
| **Local names:** | | variant annotation (ga4gh) |

