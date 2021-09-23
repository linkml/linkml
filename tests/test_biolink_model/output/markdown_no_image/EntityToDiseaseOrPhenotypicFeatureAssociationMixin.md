
# Class: entity to disease or phenotypic feature association mixin




URI: [biolink:EntityToDiseaseOrPhenotypicFeatureAssociationMixin](https://w3id.org/biolink/vocab/EntityToDiseaseOrPhenotypicFeatureAssociationMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[DiseaseOrPhenotypicFeature]<object%201..1-%20[EntityToDiseaseOrPhenotypicFeatureAssociationMixin],[MaterialSampleToDiseaseOrPhenotypicFeatureAssociation]uses%20-.->[EntityToDiseaseOrPhenotypicFeatureAssociationMixin],[ChemicalToDiseaseOrPhenotypicFeatureAssociation]uses%20-.->[EntityToDiseaseOrPhenotypicFeatureAssociationMixin],[CellLineToDiseaseOrPhenotypicFeatureAssociation]uses%20-.->[EntityToDiseaseOrPhenotypicFeatureAssociationMixin],[MaterialSampleToDiseaseOrPhenotypicFeatureAssociation],[DiseaseOrPhenotypicFeature],[ChemicalToDiseaseOrPhenotypicFeatureAssociation],[CellLineToDiseaseOrPhenotypicFeatureAssociation])](https://yuml.me/diagram/nofunky;dir:TB/class/[DiseaseOrPhenotypicFeature]<object%201..1-%20[EntityToDiseaseOrPhenotypicFeatureAssociationMixin],[MaterialSampleToDiseaseOrPhenotypicFeatureAssociation]uses%20-.->[EntityToDiseaseOrPhenotypicFeatureAssociationMixin],[ChemicalToDiseaseOrPhenotypicFeatureAssociation]uses%20-.->[EntityToDiseaseOrPhenotypicFeatureAssociationMixin],[CellLineToDiseaseOrPhenotypicFeatureAssociation]uses%20-.->[EntityToDiseaseOrPhenotypicFeatureAssociationMixin],[MaterialSampleToDiseaseOrPhenotypicFeatureAssociation],[DiseaseOrPhenotypicFeature],[ChemicalToDiseaseOrPhenotypicFeatureAssociation],[CellLineToDiseaseOrPhenotypicFeatureAssociation])

## Mixin for

 * [CellLineToDiseaseOrPhenotypicFeatureAssociation](CellLineToDiseaseOrPhenotypicFeatureAssociation.md) (mixin)  - An relationship between a cell line and a disease or a phenotype, where the cell line is derived from an individual with that disease or phenotype.
 * [ChemicalToDiseaseOrPhenotypicFeatureAssociation](ChemicalToDiseaseOrPhenotypicFeatureAssociation.md) (mixin)  - An interaction between a chemical entity and a phenotype or disease, where the presence of the chemical gives rise to or exacerbates the phenotype.
 * [MaterialSampleToDiseaseOrPhenotypicFeatureAssociation](MaterialSampleToDiseaseOrPhenotypicFeatureAssociation.md) (mixin)  - An association between a material sample and a disease or phenotype.

## Referenced by Class


## Attributes


### Own

 * [entity to disease or phenotypic feature association mixin➞object](entity_to_disease_or_phenotypic_feature_association_mixin_object.md)  <sub>1..1</sub>
     * Description: disease or phenotype
     * Range: [DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)
     * Example: MONDO:0017314 Ehlers-Danlos syndrome, vascular type
     * Example: MP:0013229 abnormal brain ventricle size
