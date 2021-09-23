
# Class: gene expression mixin


Observed gene expression intensity, context (site, stage) and associated phenotypic status within which the expression occurs.

URI: [biolink:GeneExpressionMixin](https://w3id.org/biolink/vocab/GeneExpressionMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[OntologyClass],[LifeStage],[DiseaseOrPhenotypicFeature]<phenotypic%20state%200..1-%20[GeneExpressionMixin],[LifeStage]<stage%20qualifier%200..1-%20[GeneExpressionMixin],[AnatomicalEntity]<expression%20site%200..1-%20[GeneExpressionMixin],[OntologyClass]<quantifier%20qualifier%200..1-++[GeneExpressionMixin],[VariantToGeneExpressionAssociation]uses%20-.->[GeneExpressionMixin],[GeneToGeneCoexpressionAssociation]uses%20-.->[GeneExpressionMixin],[VariantToGeneExpressionAssociation],[GeneToGeneCoexpressionAssociation],[DiseaseOrPhenotypicFeature],[AnatomicalEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[OntologyClass],[LifeStage],[DiseaseOrPhenotypicFeature]<phenotypic%20state%200..1-%20[GeneExpressionMixin],[LifeStage]<stage%20qualifier%200..1-%20[GeneExpressionMixin],[AnatomicalEntity]<expression%20site%200..1-%20[GeneExpressionMixin],[OntologyClass]<quantifier%20qualifier%200..1-++[GeneExpressionMixin],[VariantToGeneExpressionAssociation]uses%20-.->[GeneExpressionMixin],[GeneToGeneCoexpressionAssociation]uses%20-.->[GeneExpressionMixin],[VariantToGeneExpressionAssociation],[GeneToGeneCoexpressionAssociation],[DiseaseOrPhenotypicFeature],[AnatomicalEntity])

## Mixin for

 * [GeneToGeneCoexpressionAssociation](GeneToGeneCoexpressionAssociation.md) (mixin)  - Indicates that two genes are co-expressed, generally under the same conditions.
 * [VariantToGeneExpressionAssociation](VariantToGeneExpressionAssociation.md) (mixin)  - An association between a variant and expression of a gene (i.e. e-QTL)

## Referenced by Class


## Attributes


### Own

 * [gene expression mixin➞quantifier qualifier](gene_expression_mixin_quantifier_qualifier.md)  <sub>0..1</sub>
     * Description: Optional quantitative value indicating degree of expression.
     * Range: [OntologyClass](OntologyClass.md)
 * [expression site](expression_site.md)  <sub>0..1</sub>
     * Description: location in which gene or protein expression takes place. May be cell, tissue, or organ.
     * Range: [AnatomicalEntity](AnatomicalEntity.md)
     * Example: UBERON:0002037 cerebellum
 * [stage qualifier](stage_qualifier.md)  <sub>0..1</sub>
     * Description: stage during which gene or protein expression of takes place.
     * Range: [LifeStage](LifeStage.md)
     * Example: UBERON:0000069 larval stage
 * [phenotypic state](phenotypic_state.md)  <sub>0..1</sub>
     * Description: in experiments (e.g. gene expression) assaying diseased or unhealthy tissue, the phenotypic state can be put here, e.g. MONDO ID. For healthy tissues, use XXX.
     * Range: [DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)
