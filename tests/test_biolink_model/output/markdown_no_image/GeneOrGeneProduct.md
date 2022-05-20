
# Class: gene or gene product


A union of gene loci or gene products. Frequently an identifier for one will be used as proxy for another

URI: [biolink:GeneOrGeneProduct](https://w3id.org/biolink/vocab/GeneOrGeneProduct)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[MacromolecularMachineMixin],[GeneToPhenotypicFeatureAssociation],[GeneToGeneAssociation],[GeneToExpressionSiteAssociation],[GeneToEntityAssociationMixin],[GeneToDiseaseAssociation],[GeneRegulatoryRelationship],[GeneProductMixin],[ChemicalToGeneAssociation]++-%20object%201..1>[GeneOrGeneProduct&#124;name(i):symbol_type%20%3F],[DrugToGeneAssociation]++-%20object%201..1>[GeneOrGeneProduct],[GeneAsAModelOfDiseaseAssociation]++-%20subject%201..1>[GeneOrGeneProduct],[GeneHasVariantThatContributesToDiseaseAssociation]++-%20subject%201..1>[GeneOrGeneProduct],[GeneRegulatoryRelationship]++-%20object%201..1>[GeneOrGeneProduct],[GeneRegulatoryRelationship]++-%20subject%201..1>[GeneOrGeneProduct],[GeneToDiseaseAssociation]++-%20subject%201..1>[GeneOrGeneProduct],[GeneToEntityAssociationMixin]++-%20subject%201..1>[GeneOrGeneProduct],[GeneToExpressionSiteAssociation]++-%20subject%201..1>[GeneOrGeneProduct],[GeneToGeneAssociation]++-%20object%201..1>[GeneOrGeneProduct],[GeneToGeneAssociation]++-%20subject%201..1>[GeneOrGeneProduct],[GeneToPhenotypicFeatureAssociation]++-%20subject%201..1>[GeneOrGeneProduct],[Gene]uses%20-.->[GeneOrGeneProduct],[GeneOrGeneProduct]^-[GeneProductMixin],[MacromolecularMachineMixin]^-[GeneOrGeneProduct],[GeneHasVariantThatContributesToDiseaseAssociation],[GeneAsAModelOfDiseaseAssociation],[Gene],[DrugToGeneAssociation],[ChemicalToGeneAssociation],[AnatomicalEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[MacromolecularMachineMixin],[GeneToPhenotypicFeatureAssociation],[GeneToGeneAssociation],[GeneToExpressionSiteAssociation],[GeneToEntityAssociationMixin],[GeneToDiseaseAssociation],[GeneRegulatoryRelationship],[GeneProductMixin],[ChemicalToGeneAssociation]++-%20object%201..1>[GeneOrGeneProduct&#124;name(i):symbol_type%20%3F],[DrugToGeneAssociation]++-%20object%201..1>[GeneOrGeneProduct],[GeneAsAModelOfDiseaseAssociation]++-%20subject%201..1>[GeneOrGeneProduct],[GeneHasVariantThatContributesToDiseaseAssociation]++-%20subject%201..1>[GeneOrGeneProduct],[GeneRegulatoryRelationship]++-%20object%201..1>[GeneOrGeneProduct],[GeneRegulatoryRelationship]++-%20subject%201..1>[GeneOrGeneProduct],[GeneToDiseaseAssociation]++-%20subject%201..1>[GeneOrGeneProduct],[GeneToEntityAssociationMixin]++-%20subject%201..1>[GeneOrGeneProduct],[GeneToExpressionSiteAssociation]++-%20subject%201..1>[GeneOrGeneProduct],[GeneToGeneAssociation]++-%20object%201..1>[GeneOrGeneProduct],[GeneToGeneAssociation]++-%20subject%201..1>[GeneOrGeneProduct],[GeneToPhenotypicFeatureAssociation]++-%20subject%201..1>[GeneOrGeneProduct],[Gene]uses%20-.->[GeneOrGeneProduct],[GeneOrGeneProduct]^-[GeneProductMixin],[MacromolecularMachineMixin]^-[GeneOrGeneProduct],[GeneHasVariantThatContributesToDiseaseAssociation],[GeneAsAModelOfDiseaseAssociation],[Gene],[DrugToGeneAssociation],[ChemicalToGeneAssociation],[AnatomicalEntity])

## Identifier prefixes

 * CHEMBL.TARGET
 * IUPHAR.FAMILY

## Parents

 *  is_a: [MacromolecularMachineMixin](MacromolecularMachineMixin.md) - A union of gene locus, gene product, and macromolecular complex mixin. These are the basic units of function in a cell. They either carry out individual biological activities, or they encode molecules which do this.

## Children

 * [GeneProductMixin](GeneProductMixin.md) - The functional molecular product of a single gene locus. Gene products are either proteins or functional RNA molecules.

## Mixin for

 * [Gene](Gene.md) (mixin)  - A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene locus may include regulatory regions, transcribed regions and/or other functional sequence regions.

## Referenced by Class

 *  **[ChemicalToGeneAssociation](ChemicalToGeneAssociation.md)** *[chemical to gene association➞object](chemical_to_gene_association_object.md)*  <sub>1..1</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneOrGeneProduct](GeneOrGeneProduct.md)** *[coexpressed with](coexpressed_with.md)*  <sub>0..\*</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[DrugToGeneAssociation](DrugToGeneAssociation.md)** *[drug to gene association➞object](drug_to_gene_association_object.md)*  <sub>1..1</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[AnatomicalEntity](AnatomicalEntity.md)** *[expresses](expresses.md)*  <sub>0..\*</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneAsAModelOfDiseaseAssociation](GeneAsAModelOfDiseaseAssociation.md)** *[gene as a model of disease association➞subject](gene_as_a_model_of_disease_association_subject.md)*  <sub>1..1</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneHasVariantThatContributesToDiseaseAssociation](GeneHasVariantThatContributesToDiseaseAssociation.md)** *[gene has variant that contributes to disease association➞subject](gene_has_variant_that_contributes_to_disease_association_subject.md)*  <sub>1..1</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneRegulatoryRelationship](GeneRegulatoryRelationship.md)** *[gene regulatory relationship➞object](gene_regulatory_relationship_object.md)*  <sub>1..1</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneRegulatoryRelationship](GeneRegulatoryRelationship.md)** *[gene regulatory relationship➞subject](gene_regulatory_relationship_subject.md)*  <sub>1..1</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneToDiseaseAssociation](GeneToDiseaseAssociation.md)** *[gene to disease association➞subject](gene_to_disease_association_subject.md)*  <sub>1..1</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneToEntityAssociationMixin](GeneToEntityAssociationMixin.md)** *[gene to entity association mixin➞subject](gene_to_entity_association_mixin_subject.md)*  <sub>1..1</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneToExpressionSiteAssociation](GeneToExpressionSiteAssociation.md)** *[gene to expression site association➞subject](gene_to_expression_site_association_subject.md)*  <sub>1..1</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneToGeneAssociation](GeneToGeneAssociation.md)** *[gene to gene association➞object](gene_to_gene_association_object.md)*  <sub>1..1</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneToGeneAssociation](GeneToGeneAssociation.md)** *[gene to gene association➞subject](gene_to_gene_association_subject.md)*  <sub>1..1</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneToPhenotypicFeatureAssociation](GeneToPhenotypicFeatureAssociation.md)** *[gene to phenotypic feature association➞subject](gene_to_phenotypic_feature_association_subject.md)*  <sub>1..1</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneOrGeneProduct](GeneOrGeneProduct.md)** *[in cell population with](in_cell_population_with.md)*  <sub>0..\*</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneOrGeneProduct](GeneOrGeneProduct.md)** *[in complex with](in_complex_with.md)*  <sub>0..\*</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**
 *  **[GeneOrGeneProduct](GeneOrGeneProduct.md)** *[in pathway with](in_pathway_with.md)*  <sub>0..\*</sub>  **[GeneOrGeneProduct](GeneOrGeneProduct.md)**

## Attributes


### Inherited from macromolecular machine mixin:

 * [macromolecular machine mixin➞name](macromolecular_machine_mixin_name.md)  <sub>0..1</sub>
     * Description: genes are typically designated by a short symbol and a full name. We map the symbol to the default display name and use an additional slot for full name
     * Range: [SymbolType](types/SymbolType.md)
     * in subsets: (translator_minimal,samples)
