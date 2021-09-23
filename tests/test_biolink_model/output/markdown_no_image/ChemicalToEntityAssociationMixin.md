
# Class: chemical to entity association mixin


An interaction between a chemical entity and another entity

URI: [biolink:ChemicalToEntityAssociationMixin](https://w3id.org/biolink/vocab/ChemicalToEntityAssociationMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[MolecularEntityToEntityAssociationMixin],[ChemicalSubstance]<subject%201..1-%20[ChemicalToEntityAssociationMixin],[ChemicalToPathwayAssociation]uses%20-.->[ChemicalToEntityAssociationMixin],[ChemicalToGeneAssociation]uses%20-.->[ChemicalToEntityAssociationMixin],[ChemicalToDiseaseOrPhenotypicFeatureAssociation]uses%20-.->[ChemicalToEntityAssociationMixin],[ChemicalToChemicalAssociation]uses%20-.->[ChemicalToEntityAssociationMixin],[MolecularEntityToEntityAssociationMixin]^-[ChemicalToEntityAssociationMixin],[ChemicalToPathwayAssociation],[ChemicalToGeneAssociation],[ChemicalToDiseaseOrPhenotypicFeatureAssociation],[ChemicalToChemicalAssociation],[ChemicalSubstance])](https://yuml.me/diagram/nofunky;dir:TB/class/[MolecularEntityToEntityAssociationMixin],[ChemicalSubstance]<subject%201..1-%20[ChemicalToEntityAssociationMixin],[ChemicalToPathwayAssociation]uses%20-.->[ChemicalToEntityAssociationMixin],[ChemicalToGeneAssociation]uses%20-.->[ChemicalToEntityAssociationMixin],[ChemicalToDiseaseOrPhenotypicFeatureAssociation]uses%20-.->[ChemicalToEntityAssociationMixin],[ChemicalToChemicalAssociation]uses%20-.->[ChemicalToEntityAssociationMixin],[MolecularEntityToEntityAssociationMixin]^-[ChemicalToEntityAssociationMixin],[ChemicalToPathwayAssociation],[ChemicalToGeneAssociation],[ChemicalToDiseaseOrPhenotypicFeatureAssociation],[ChemicalToChemicalAssociation],[ChemicalSubstance])

## Parents

 *  is_a: [MolecularEntityToEntityAssociationMixin](MolecularEntityToEntityAssociationMixin.md) - An interaction between a molecular entity and another entity

## Mixin for

 * [ChemicalToChemicalAssociation](ChemicalToChemicalAssociation.md) (mixin)  - A relationship between two chemical entities. This can encompass actual interactions as well as temporal causal edges, e.g. one chemical converted to another.
 * [ChemicalToDiseaseOrPhenotypicFeatureAssociation](ChemicalToDiseaseOrPhenotypicFeatureAssociation.md) (mixin)  - An interaction between a chemical entity and a phenotype or disease, where the presence of the chemical gives rise to or exacerbates the phenotype.
 * [ChemicalToGeneAssociation](ChemicalToGeneAssociation.md) (mixin)  - An interaction between a chemical entity and a gene or gene product.
 * [ChemicalToPathwayAssociation](ChemicalToPathwayAssociation.md) (mixin)  - An interaction between a chemical entity and a biological process or pathway.

## Referenced by Class


## Attributes


### Own

 * [chemical to entity association mixin➞subject](chemical_to_entity_association_mixin_subject.md)  <sub>1..1</sub>
     * Description: the chemical substance or entity that is an interactor
     * Range: [ChemicalSubstance](ChemicalSubstance.md)
