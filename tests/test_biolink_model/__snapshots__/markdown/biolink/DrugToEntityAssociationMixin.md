
# Class: drug to entity association mixin


An interaction between a drug and another entity

URI: [biolink:DrugToEntityAssociationMixin](https://w3id.org/biolink/vocab/DrugToEntityAssociationMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Drug]<subject%201..1-%20[DrugToEntityAssociationMixin],[DrugToGeneAssociation]uses%20-.->[DrugToEntityAssociationMixin],[ChemicalEntityToEntityAssociationMixin]^-[DrugToEntityAssociationMixin],[DrugToGeneAssociation],[Drug],[ChemicalEntityToEntityAssociationMixin])](https://yuml.me/diagram/nofunky;dir:TB/class/[Drug]<subject%201..1-%20[DrugToEntityAssociationMixin],[DrugToGeneAssociation]uses%20-.->[DrugToEntityAssociationMixin],[ChemicalEntityToEntityAssociationMixin]^-[DrugToEntityAssociationMixin],[DrugToGeneAssociation],[Drug],[ChemicalEntityToEntityAssociationMixin])

## Parents

 *  is_a: [ChemicalEntityToEntityAssociationMixin](ChemicalEntityToEntityAssociationMixin.md) - An interaction between a chemical entity and another entity

## Mixin for

 * [DrugToGeneAssociation](DrugToGeneAssociation.md) (mixin)  - An interaction between a drug and a gene or gene product.

## Referenced by Class


## Attributes


### Own

 * [drug to entity association mixin➞subject](drug_to_entity_association_mixin_subject.md)  <sub>1..1</sub>
     * Description: the drug that is an interactor
     * Range: [Drug](Drug.md)
