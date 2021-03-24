
# Class: EntityToPhenotypicFeatureAssociationMixin




URI: [biolink:EntityToPhenotypicFeatureAssociationMixin](https://w3id.org/biolink/vocab/EntityToPhenotypicFeatureAssociationMixin)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SeverityValue],[PhenotypicFeature],[Onset],[PhenotypicFeature]<object%201..1-%20[EntityToPhenotypicFeatureAssociationMixin&#124;description:narrative_text%20%3F;frequency_qualifier(i):frequency_value%20%3F],[BiologicalSex]<sex%20qualifier%200..1-++[EntityToPhenotypicFeatureAssociationMixin],[VariantToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[GenotypeToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[GeneToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[ExposureEventToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[DiseaseToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[CaseToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[BehaviorToBehavioralFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[EntityToFeatureOrDiseaseQualifiersMixin]^-[EntityToPhenotypicFeatureAssociationMixin],[VariantToPhenotypicFeatureAssociation],[GenotypeToPhenotypicFeatureAssociation],[GeneToPhenotypicFeatureAssociation],[ExposureEventToPhenotypicFeatureAssociation],[EntityToFeatureOrDiseaseQualifiersMixin],[DiseaseToPhenotypicFeatureAssociation],[CaseToPhenotypicFeatureAssociation],[BiologicalSex],[BehaviorToBehavioralFeatureAssociation])

## Parents

 *  is_a: [EntityToFeatureOrDiseaseQualifiersMixin](EntityToFeatureOrDiseaseQualifiersMixin.md) - Qualifiers for entity to disease or phenotype associations.

## Mixin for

 * [BehaviorToBehavioralFeatureAssociation](BehaviorToBehavioralFeatureAssociation.md) (mixin)  - An association between an aggregate behavior and a behavioral feature manifested by the individual exhibited or has exhibited the behavior.
 * [CaseToPhenotypicFeatureAssociation](CaseToPhenotypicFeatureAssociation.md) (mixin)  - An association between a case (e.g. individual patient) and a phenotypic feature in which the individual has or has had the phenotype.
 * [DiseaseToPhenotypicFeatureAssociation](DiseaseToPhenotypicFeatureAssociation.md) (mixin)  - An association between a disease and a phenotypic feature in which the phenotypic feature is associated with the disease in some way.
 * [ExposureEventToPhenotypicFeatureAssociation](ExposureEventToPhenotypicFeatureAssociation.md) (mixin)  - Any association between an environment and a phenotypic feature, where being in the environment influences the phenotype.
 * [GeneToPhenotypicFeatureAssociation](GeneToPhenotypicFeatureAssociation.md) (mixin) 
 * [GenotypeToPhenotypicFeatureAssociation](GenotypeToPhenotypicFeatureAssociation.md) (mixin)  - Any association between one genotype and a phenotypic feature, where having the genotype confers the phenotype, either in isolation or through environment
 * [VariantToPhenotypicFeatureAssociation](VariantToPhenotypicFeatureAssociation.md) (mixin) 

## Referenced by class


## Attributes


### Own

 * [entity to phenotypic feature association mixin➞description](entity_to_phenotypic_feature_association_mixin_description.md)  <sub>OPT</sub>
     * Description: A description of specific aspects of this phenotype, not otherwise covered by the phenotype ontology class
     * range: [NarrativeText](types/NarrativeText.md)
 * [entity to phenotypic feature association mixin➞object](entity_to_phenotypic_feature_association_mixin_object.md)  <sub>REQ</sub>
     * Description: phenotypic class
     * range: [PhenotypicFeature](PhenotypicFeature.md)
     * Example:    
     * Example:    
     * Example:    
 * [sex qualifier](sex_qualifier.md)  <sub>OPT</sub>
     * Description: a qualifier used in a phenotypic association to state whether the association is specific to a particular sex.
     * range: [BiologicalSex](BiologicalSex.md)

### Inherited from entity to feature or disease qualifiers mixin:

 * [frequency qualifier](frequency_qualifier.md)  <sub>OPT</sub>
     * Description: a qualifier used in a phenotypic association to state how frequent the phenotype is observed in the subject
     * range: [FrequencyValue](types/FrequencyValue.md)
 * [onset qualifier](onset_qualifier.md)  <sub>OPT</sub>
     * Description: a qualifier used in a phenotypic association to state when the phenotype appears is in the subject
     * range: [Onset](Onset.md)
 * [severity qualifier](severity_qualifier.md)  <sub>OPT</sub>
     * Description: a qualifier used in a phenotypic association to state how severe the phenotype is in the subject
     * range: [SeverityValue](SeverityValue.md)
