
# Class: DiseaseToEntityAssociationMixin




URI: [biolink:DiseaseToEntityAssociationMixin](https://w3id.org/biolink/vocab/DiseaseToEntityAssociationMixin)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Disease]<subject%201..1-%20[DiseaseToEntityAssociationMixin],[DiseaseToPhenotypicFeatureAssociation]uses%20-.->[DiseaseToEntityAssociationMixin],[DiseaseToExposureEventAssociation]uses%20-.->[DiseaseToEntityAssociationMixin],[DiseaseToPhenotypicFeatureAssociation],[DiseaseToExposureEventAssociation],[Disease])

## Mixin for

 * [DiseaseToExposureEventAssociation](DiseaseToExposureEventAssociation.md) (mixin)  - An association between an exposure event and a disease.
 * [DiseaseToPhenotypicFeatureAssociation](DiseaseToPhenotypicFeatureAssociation.md) (mixin)  - An association between a disease and a phenotypic feature in which the phenotypic feature is associated with the disease in some way.

## Referenced by class


## Attributes


### Own

 * [disease to entity association mixin➞subject](disease_to_entity_association_mixin_subject.md)  <sub>REQ</sub>
     * Description: disease class
     * range: [Disease](Disease.md)
     * Example:    
