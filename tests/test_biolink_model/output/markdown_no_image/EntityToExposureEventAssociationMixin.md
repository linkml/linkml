
# Class: entity to exposure event association mixin


An association between some entity and an exposure event.

URI: [biolink:EntityToExposureEventAssociationMixin](https://w3id.org/biolink/vocab/EntityToExposureEventAssociationMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ExposureEvent],[ExposureEvent]<object%201..1-++[EntityToExposureEventAssociationMixin],[DiseaseToExposureEventAssociation]uses%20-.->[EntityToExposureEventAssociationMixin],[DiseaseToExposureEventAssociation])](https://yuml.me/diagram/nofunky;dir:TB/class/[ExposureEvent],[ExposureEvent]<object%201..1-++[EntityToExposureEventAssociationMixin],[DiseaseToExposureEventAssociation]uses%20-.->[EntityToExposureEventAssociationMixin],[DiseaseToExposureEventAssociation])

## Mixin for

 * [DiseaseToExposureEventAssociation](DiseaseToExposureEventAssociation.md) (mixin)  - An association between an exposure event and a disease.

## Referenced by Class


## Attributes


### Own

 * [entity to exposure event association mixin➞object](entity_to_exposure_event_association_mixin_object.md)  <sub>1..1</sub>
     * Description: connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
     * Range: [ExposureEvent](ExposureEvent.md)
