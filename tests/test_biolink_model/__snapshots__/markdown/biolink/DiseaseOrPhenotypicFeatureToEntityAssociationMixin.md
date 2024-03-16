
# Class: disease or phenotypic feature to entity association mixin




URI: [biolink:DiseaseOrPhenotypicFeatureToEntityAssociationMixin](https://w3id.org/biolink/vocab/DiseaseOrPhenotypicFeatureToEntityAssociationMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[DiseaseOrPhenotypicFeature]<subject%201..1-%20[DiseaseOrPhenotypicFeatureToEntityAssociationMixin],[DiseaseOrPhenotypicFeatureToLocationAssociation]uses%20-.->[DiseaseOrPhenotypicFeatureToEntityAssociationMixin],[DiseaseOrPhenotypicFeatureToGeneticInheritanceAssociation]uses%20-.->[DiseaseOrPhenotypicFeatureToEntityAssociationMixin],[DiseaseOrPhenotypicFeatureToLocationAssociation],[DiseaseOrPhenotypicFeatureToGeneticInheritanceAssociation],[DiseaseOrPhenotypicFeature])](https://yuml.me/diagram/nofunky;dir:TB/class/[DiseaseOrPhenotypicFeature]<subject%201..1-%20[DiseaseOrPhenotypicFeatureToEntityAssociationMixin],[DiseaseOrPhenotypicFeatureToLocationAssociation]uses%20-.->[DiseaseOrPhenotypicFeatureToEntityAssociationMixin],[DiseaseOrPhenotypicFeatureToGeneticInheritanceAssociation]uses%20-.->[DiseaseOrPhenotypicFeatureToEntityAssociationMixin],[DiseaseOrPhenotypicFeatureToLocationAssociation],[DiseaseOrPhenotypicFeatureToGeneticInheritanceAssociation],[DiseaseOrPhenotypicFeature])

## Mixin for

 * [DiseaseOrPhenotypicFeatureToGeneticInheritanceAssociation](DiseaseOrPhenotypicFeatureToGeneticInheritanceAssociation.md) (mixin)  - An association between either a disease or a phenotypic feature and its mode of (genetic) inheritance.
 * [DiseaseOrPhenotypicFeatureToLocationAssociation](DiseaseOrPhenotypicFeatureToLocationAssociation.md) (mixin)  - An association between either a disease or a phenotypic feature and an anatomical entity, where the disease/feature manifests in that site.

## Referenced by Class


## Attributes


### Own

 * [disease or phenotypic feature to entity association mixin➞subject](disease_or_phenotypic_feature_to_entity_association_mixin_subject.md)  <sub>1..1</sub>
     * Description: disease or phenotype
     * Range: [DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)
     * Example: MONDO:0017314 Ehlers-Danlos syndrome, vascular type
     * Example: MP:0013229 abnormal brain ventricle size
