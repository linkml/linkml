
# Class: entity to disease association mixin


mixin class for any association whose object (target node) is a disease

URI: [biolink:EntityToDiseaseAssociationMixin](https://w3id.org/biolink/vocab/EntityToDiseaseAssociationMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SeverityValue],[Onset],[EntityToFeatureOrDiseaseQualifiersMixin],[Disease]<object%201..1-%20[EntityToDiseaseAssociationMixin&#124;frequency_qualifier(i):frequency_value%20%3F],[VariantToDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[VariantAsAModelOfDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[OrganismalEntityAsAModelOfDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[GenotypeToDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[GenotypeAsAModelOfDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[GeneToDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[GeneAsAModelOfDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[CellLineAsAModelOfDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[EntityToFeatureOrDiseaseQualifiersMixin]^-[EntityToDiseaseAssociationMixin],[VariantToDiseaseAssociation],[VariantAsAModelOfDiseaseAssociation],[OrganismalEntityAsAModelOfDiseaseAssociation],[GenotypeToDiseaseAssociation],[GenotypeAsAModelOfDiseaseAssociation],[GeneToDiseaseAssociation],[GeneAsAModelOfDiseaseAssociation],[Disease],[CellLineAsAModelOfDiseaseAssociation])](https://yuml.me/diagram/nofunky;dir:TB/class/[SeverityValue],[Onset],[EntityToFeatureOrDiseaseQualifiersMixin],[Disease]<object%201..1-%20[EntityToDiseaseAssociationMixin&#124;frequency_qualifier(i):frequency_value%20%3F],[VariantToDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[VariantAsAModelOfDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[OrganismalEntityAsAModelOfDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[GenotypeToDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[GenotypeAsAModelOfDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[GeneToDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[GeneAsAModelOfDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[CellLineAsAModelOfDiseaseAssociation]uses%20-.->[EntityToDiseaseAssociationMixin],[EntityToFeatureOrDiseaseQualifiersMixin]^-[EntityToDiseaseAssociationMixin],[VariantToDiseaseAssociation],[VariantAsAModelOfDiseaseAssociation],[OrganismalEntityAsAModelOfDiseaseAssociation],[GenotypeToDiseaseAssociation],[GenotypeAsAModelOfDiseaseAssociation],[GeneToDiseaseAssociation],[GeneAsAModelOfDiseaseAssociation],[Disease],[CellLineAsAModelOfDiseaseAssociation])

## Parents

 *  is_a: [EntityToFeatureOrDiseaseQualifiersMixin](EntityToFeatureOrDiseaseQualifiersMixin.md) - Qualifiers for entity to disease or phenotype associations.

## Mixin for

 * [CellLineAsAModelOfDiseaseAssociation](CellLineAsAModelOfDiseaseAssociation.md) (mixin) 
 * [GeneAsAModelOfDiseaseAssociation](GeneAsAModelOfDiseaseAssociation.md) (mixin) 
 * [GeneToDiseaseAssociation](GeneToDiseaseAssociation.md) (mixin) 
 * [GenotypeAsAModelOfDiseaseAssociation](GenotypeAsAModelOfDiseaseAssociation.md) (mixin) 
 * [GenotypeToDiseaseAssociation](GenotypeToDiseaseAssociation.md) (mixin) 
 * [OrganismalEntityAsAModelOfDiseaseAssociation](OrganismalEntityAsAModelOfDiseaseAssociation.md) (mixin) 
 * [VariantAsAModelOfDiseaseAssociation](VariantAsAModelOfDiseaseAssociation.md) (mixin) 
 * [VariantToDiseaseAssociation](VariantToDiseaseAssociation.md) (mixin) 

## Referenced by Class


## Attributes


### Own

 * [entity to disease association mixin➞object](entity_to_disease_association_mixin_object.md)  <sub>1..1</sub>
     * Description: disease
     * Range: [Disease](Disease.md)
     * Example: MONDO:0020066 Ehlers-Danlos syndrome

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
