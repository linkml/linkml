
# Class: DrugToEntityAssociationMixin


An interaction between a drug and another entity

URI: [biolink:DrugToEntityAssociationMixin](https://w3id.org/biolink/vocab/DrugToEntityAssociationMixin)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[MolecularEntityToEntityAssociationMixin],[Drug]<subject%201..1-%20[DrugToEntityAssociationMixin],[DrugToGeneAssociation]uses%20-.->[DrugToEntityAssociationMixin],[MolecularEntityToEntityAssociationMixin]^-[DrugToEntityAssociationMixin],[DrugToGeneAssociation],[Drug])

## Parents

 *  is_a: [MolecularEntityToEntityAssociationMixin](MolecularEntityToEntityAssociationMixin.md) - An interaction between a molecular entity and another entity

## Mixin for

 * [DrugToGeneAssociation](DrugToGeneAssociation.md) (mixin)  - An interaction between a drug and a gene or gene product.

## Referenced by class


## Attributes


### Own

 * [drug to entity association mixin➞subject](drug_to_entity_association_mixin_subject.md)  <sub>REQ</sub>
     * Description: the drug that is an interactor
     * range: [Drug](Drug.md)
