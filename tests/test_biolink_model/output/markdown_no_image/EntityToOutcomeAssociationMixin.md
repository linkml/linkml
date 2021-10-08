
# Class: entity to outcome association mixin


An association between some entity and an outcome

URI: [biolink:EntityToOutcomeAssociationMixin](https://w3id.org/biolink/vocab/EntityToOutcomeAssociationMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Outcome],[Outcome]<object%201..1-++[EntityToOutcomeAssociationMixin],[ExposureEventToOutcomeAssociation]uses%20-.->[EntityToOutcomeAssociationMixin],[ExposureEventToOutcomeAssociation])](https://yuml.me/diagram/nofunky;dir:TB/class/[Outcome],[Outcome]<object%201..1-++[EntityToOutcomeAssociationMixin],[ExposureEventToOutcomeAssociation]uses%20-.->[EntityToOutcomeAssociationMixin],[ExposureEventToOutcomeAssociation])

## Mixin for

 * [ExposureEventToOutcomeAssociation](ExposureEventToOutcomeAssociation.md) (mixin)  - An association between an exposure event and an outcome.

## Referenced by Class


## Attributes


### Own

 * [entity to outcome association mixin➞object](entity_to_outcome_association_mixin_object.md)  <sub>1..1</sub>
     * Description: connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
     * Range: [Outcome](Outcome.md)
