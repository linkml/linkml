
# Class: entity to phenotypic feature association mixin




URI: [biolink:EntityToPhenotypicFeatureAssociationMixin](https://w3id.org/biolink/vocab/EntityToPhenotypicFeatureAssociationMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SeverityValue],[PhenotypicFeature],[Onset],[FrequencyQuantifier],[PhenotypicFeature]<object%201..1-%20[EntityToPhenotypicFeatureAssociationMixin&#124;has_count:integer%20%3F;has_total:integer%20%3F;has_quotient:double%20%3F;has_percentage:double%20%3F;frequency_qualifier(i):frequency_value%20%3F],[BiologicalSex]<sex%20qualifier%200..1-%20[EntityToPhenotypicFeatureAssociationMixin],[EntityToPhenotypicFeatureAssociationMixin]uses%20-.->[FrequencyQuantifier],[VariantToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[GenotypeToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[GeneToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[ExposureEventToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[DiseaseToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[CaseToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[BehaviorToBehavioralFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[EntityToFeatureOrDiseaseQualifiersMixin]^-[EntityToPhenotypicFeatureAssociationMixin],[VariantToPhenotypicFeatureAssociation],[GenotypeToPhenotypicFeatureAssociation],[GeneToPhenotypicFeatureAssociation],[ExposureEventToPhenotypicFeatureAssociation],[EntityToFeatureOrDiseaseQualifiersMixin],[DiseaseToPhenotypicFeatureAssociation],[CaseToPhenotypicFeatureAssociation],[BiologicalSex],[BehaviorToBehavioralFeatureAssociation])](https://yuml.me/diagram/nofunky;dir:TB/class/[SeverityValue],[PhenotypicFeature],[Onset],[FrequencyQuantifier],[PhenotypicFeature]<object%201..1-%20[EntityToPhenotypicFeatureAssociationMixin&#124;has_count:integer%20%3F;has_total:integer%20%3F;has_quotient:double%20%3F;has_percentage:double%20%3F;frequency_qualifier(i):frequency_value%20%3F],[BiologicalSex]<sex%20qualifier%200..1-%20[EntityToPhenotypicFeatureAssociationMixin],[EntityToPhenotypicFeatureAssociationMixin]uses%20-.->[FrequencyQuantifier],[VariantToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[GenotypeToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[GeneToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[ExposureEventToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[DiseaseToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[CaseToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[BehaviorToBehavioralFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[EntityToFeatureOrDiseaseQualifiersMixin]^-[EntityToPhenotypicFeatureAssociationMixin],[VariantToPhenotypicFeatureAssociation],[GenotypeToPhenotypicFeatureAssociation],[GeneToPhenotypicFeatureAssociation],[ExposureEventToPhenotypicFeatureAssociation],[EntityToFeatureOrDiseaseQualifiersMixin],[DiseaseToPhenotypicFeatureAssociation],[CaseToPhenotypicFeatureAssociation],[BiologicalSex],[BehaviorToBehavioralFeatureAssociation])

## Parents

 *  is_a: [EntityToFeatureOrDiseaseQualifiersMixin](EntityToFeatureOrDiseaseQualifiersMixin.md) - Qualifiers for entity to disease or phenotype associations.

## Uses Mixin

 *  mixin: [FrequencyQuantifier](FrequencyQuantifier.md)

## Mixin for

 * [BehaviorToBehavioralFeatureAssociation](BehaviorToBehavioralFeatureAssociation.md) (mixin)  - An association between an mixture behavior and a behavioral feature manifested by the individual exhibited or has exhibited the behavior.
 * [CaseToPhenotypicFeatureAssociation](CaseToPhenotypicFeatureAssociation.md) (mixin)  - An association between a case (e.g. individual patient) and a phenotypic feature in which the individual has or has had the phenotype.
 * [DiseaseToPhenotypicFeatureAssociation](DiseaseToPhenotypicFeatureAssociation.md) (mixin)  - An association between a disease and a phenotypic feature in which the phenotypic feature is associated with the disease in some way.
 * [ExposureEventToPhenotypicFeatureAssociation](ExposureEventToPhenotypicFeatureAssociation.md) (mixin)  - Any association between an environment and a phenotypic feature, where being in the environment influences the phenotype.
 * [GeneToPhenotypicFeatureAssociation](GeneToPhenotypicFeatureAssociation.md) (mixin) 
 * [GenotypeToPhenotypicFeatureAssociation](GenotypeToPhenotypicFeatureAssociation.md) (mixin)  - Any association between one genotype and a phenotypic feature, where having the genotype confers the phenotype, either in isolation or through environment
 * [VariantToPhenotypicFeatureAssociation](VariantToPhenotypicFeatureAssociation.md) (mixin) 

## Referenced by Class


## Attributes


### Own

 * [sex qualifier](sex_qualifier.md)  <sub>0..1</sub>
     * Description: a qualifier used in a phenotypic association to state whether the association is specific to a particular sex.
     * Range: [BiologicalSex](BiologicalSex.md)
 * [entity to phenotypic feature association mixin➞object](entity_to_phenotypic_feature_association_mixin_object.md)  <sub>1..1</sub>
     * Description: connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
     * Range: [PhenotypicFeature](PhenotypicFeature.md)
     * Example: HP:0002487 Hyperkinesis
     * Example: WBPhenotype:0000180 axon morphology variant
     * Example: MP:0001569 abnormal circulating bilirubin level

### Inherited from entity to feature or disease qualifiers mixin:

 * [frequency qualifier](frequency_qualifier.md)  <sub>0..1</sub>
     * Description: a qualifier used in a phenotypic association to state how frequent the phenotype is observed in the subject
     * Range: [FrequencyValue](types/FrequencyValue.md)
 * [severity qualifier](severity_qualifier.md)  <sub>0..1</sub>
     * Description: a qualifier used in a phenotypic association to state how severe the phenotype is in the subject
     * Range: [SeverityValue](SeverityValue.md)
 * [onset qualifier](onset_qualifier.md)  <sub>0..1</sub>
     * Description: a qualifier used in a phenotypic association to state when the phenotype appears is in the subject
     * Range: [Onset](Onset.md)

### Mixed in from frequency quantifier:

 * [has count](has_count.md)  <sub>0..1</sub>
     * Description: number of things with a particular property
     * Range: [Integer](types/Integer.md)

### Mixed in from frequency quantifier:

 * [has total](has_total.md)  <sub>0..1</sub>
     * Description: total number of things in a particular reference set
     * Range: [Integer](types/Integer.md)

### Mixed in from frequency quantifier:

 * [has quotient](has_quotient.md)  <sub>0..1</sub>
     * Range: [Double](types/Double.md)

### Mixed in from frequency quantifier:

 * [has percentage](has_percentage.md)  <sub>0..1</sub>
     * Description: equivalent to has quotient multiplied by 100
     * Range: [Double](types/Double.md)
