
# Class: exposure event to entity association mixin


An association between some exposure event and some entity.

URI: [biolink:ExposureEventToEntityAssociationMixin](https://w3id.org/biolink/vocab/ExposureEventToEntityAssociationMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ExposureEvent]<subject%201..1-++[ExposureEventToEntityAssociationMixin],[ExposureEventToOutcomeAssociation]uses%20-.->[ExposureEventToEntityAssociationMixin],[ExposureEventToOutcomeAssociation],[ExposureEvent])](https://yuml.me/diagram/nofunky;dir:TB/class/[ExposureEvent]<subject%201..1-++[ExposureEventToEntityAssociationMixin],[ExposureEventToOutcomeAssociation]uses%20-.->[ExposureEventToEntityAssociationMixin],[ExposureEventToOutcomeAssociation],[ExposureEvent])

## Mixin for

 * [ExposureEventToOutcomeAssociation](ExposureEventToOutcomeAssociation.md) (mixin)  - An association between an exposure event and an outcome.

## Referenced by Class


## Attributes


### Own

 * [exposure event to entity association mixin➞subject](exposure_event_to_entity_association_mixin_subject.md)  <sub>1..1</sub>
     * Description: connects an association to the subject of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
     * Range: [ExposureEvent](ExposureEvent.md)
