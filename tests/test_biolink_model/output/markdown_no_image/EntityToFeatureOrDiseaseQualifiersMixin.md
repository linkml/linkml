
# Class: EntityToFeatureOrDiseaseQualifiersMixin


Qualifiers for entity to disease or phenotype associations.

URI: [biolink:EntityToFeatureOrDiseaseQualifiersMixin](https://w3id.org/biolink/vocab/EntityToFeatureOrDiseaseQualifiersMixin)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SeverityValue],[Onset],[FrequencyQualifierMixin],[EntityToPhenotypicFeatureAssociationMixin],[Onset]<onset%20qualifier%200..1-++[EntityToFeatureOrDiseaseQualifiersMixin&#124;frequency_qualifier(i):frequency_value%20%3F],[SeverityValue]<severity%20qualifier%200..1-++[EntityToFeatureOrDiseaseQualifiersMixin],[EntityToFeatureOrDiseaseQualifiersMixin]^-[EntityToPhenotypicFeatureAssociationMixin],[EntityToFeatureOrDiseaseQualifiersMixin]^-[EntityToDiseaseAssociationMixin],[FrequencyQualifierMixin]^-[EntityToFeatureOrDiseaseQualifiersMixin],[EntityToDiseaseAssociationMixin])

## Parents

 *  is_a: [FrequencyQualifierMixin](FrequencyQualifierMixin.md) - Qualifier for frequency type associations

## Children

 * [EntityToDiseaseAssociationMixin](EntityToDiseaseAssociationMixin.md) - mixin class for any association whose object (target node) is a disease
 * [EntityToPhenotypicFeatureAssociationMixin](EntityToPhenotypicFeatureAssociationMixin.md)

## Referenced by class


## Attributes


### Own

 * [onset qualifier](onset_qualifier.md)  <sub>OPT</sub>
     * Description: a qualifier used in a phenotypic association to state when the phenotype appears is in the subject
     * range: [Onset](Onset.md)
 * [severity qualifier](severity_qualifier.md)  <sub>OPT</sub>
     * Description: a qualifier used in a phenotypic association to state how severe the phenotype is in the subject
     * range: [SeverityValue](SeverityValue.md)

### Inherited from frequency qualifier mixin:

 * [frequency qualifier](frequency_qualifier.md)  <sub>OPT</sub>
     * Description: a qualifier used in a phenotypic association to state how frequent the phenotype is observed in the subject
     * range: [FrequencyValue](types/FrequencyValue.md)
