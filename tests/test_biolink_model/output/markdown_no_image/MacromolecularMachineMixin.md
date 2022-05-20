
# Class: macromolecular machine mixin


A union of gene locus, gene product, and macromolecular complex mixin. These are the basic units of function in a cell. They either carry out individual biological activities, or they encode molecules which do this.

URI: [biolink:MacromolecularMachineMixin](https://w3id.org/biolink/vocab/MacromolecularMachineMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[MolecularActivity],[ChemicalToChemicalDerivationAssociation]++-%20catalyst%20qualifier(i)%200..*>[MacromolecularMachineMixin&#124;name:symbol_type%20%3F],[ChemicalToChemicalDerivationAssociation]++-%20catalyst%20qualifier%200..*>[MacromolecularMachineMixin],[FunctionalAssociation]++-%20subject%201..1>[MacromolecularMachineMixin],[MolecularActivity]++-%20enabled%20by%200..*>[MacromolecularMachineMixin],[MacromolecularMachineMixin]^-[MacromolecularComplexMixin],[MacromolecularMachineMixin]^-[GeneOrGeneProduct],[MacromolecularComplexMixin],[GeneOrGeneProduct],[FunctionalAssociation],[ChemicalToChemicalDerivationAssociation],[Association])](https://yuml.me/diagram/nofunky;dir:TB/class/[MolecularActivity],[ChemicalToChemicalDerivationAssociation]++-%20catalyst%20qualifier(i)%200..*>[MacromolecularMachineMixin&#124;name:symbol_type%20%3F],[ChemicalToChemicalDerivationAssociation]++-%20catalyst%20qualifier%200..*>[MacromolecularMachineMixin],[FunctionalAssociation]++-%20subject%201..1>[MacromolecularMachineMixin],[MolecularActivity]++-%20enabled%20by%200..*>[MacromolecularMachineMixin],[MacromolecularMachineMixin]^-[MacromolecularComplexMixin],[MacromolecularMachineMixin]^-[GeneOrGeneProduct],[MacromolecularComplexMixin],[GeneOrGeneProduct],[FunctionalAssociation],[ChemicalToChemicalDerivationAssociation],[Association])

## Children

 * [GeneOrGeneProduct](GeneOrGeneProduct.md) - A union of gene loci or gene products. Frequently an identifier for one will be used as proxy for another
 * [MacromolecularComplexMixin](MacromolecularComplexMixin.md) - A stable assembly of two or more macromolecules, i.e. proteins, nucleic acids, carbohydrates or lipids, in which at least one component is a protein and the constituent parts function together.

## Referenced by Class

 *  **[Association](Association.md)** *[catalyst qualifier](catalyst_qualifier.md)*  <sub>0..\*</sub>  **[MacromolecularMachineMixin](MacromolecularMachineMixin.md)**
 *  **[ChemicalToChemicalDerivationAssociation](ChemicalToChemicalDerivationAssociation.md)** *[chemical to chemical derivation association➞catalyst qualifier](chemical_to_chemical_derivation_association_catalyst_qualifier.md)*  <sub>0..\*</sub>  **[MacromolecularMachineMixin](MacromolecularMachineMixin.md)**
 *  **[FunctionalAssociation](FunctionalAssociation.md)** *[functional association➞subject](functional_association_subject.md)*  <sub>1..1</sub>  **[MacromolecularMachineMixin](MacromolecularMachineMixin.md)**
 *  **[MolecularActivity](MolecularActivity.md)** *[molecular activity➞enabled by](molecular_activity_enabled_by.md)*  <sub>0..\*</sub>  **[MacromolecularMachineMixin](MacromolecularMachineMixin.md)**

## Attributes


### Own

 * [macromolecular machine mixin➞name](macromolecular_machine_mixin_name.md)  <sub>0..1</sub>
     * Description: genes are typically designated by a short symbol and a full name. We map the symbol to the default display name and use an additional slot for full name
     * Range: [SymbolType](types/SymbolType.md)
     * in subsets: (translator_minimal,samples)
