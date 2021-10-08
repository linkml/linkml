
# Slot: subject


the subject gene in the association. If the relation is symmetric, subject vs object is arbitrary. We allow a gene product to stand as a proxy for the gene or vice versa.

URI: [biolink:gene_to_gene_association_subject](https://w3id.org/biolink/vocab/gene_to_gene_association_subject)


## Domain and Range

[GeneToGeneAssociation](GeneToGeneAssociation.md) &#8594;  <sub>1..1</sub> [GeneOrGeneProduct](GeneOrGeneProduct.md)

## Parents

 *  is_a: [subject](subject.md)

## Children

 *  [pairwise molecular interaction➞subject](pairwise_molecular_interaction_subject.md)

## Used by

 * [GeneToGeneAssociation](GeneToGeneAssociation.md)
 * [GeneToGeneCoexpressionAssociation](GeneToGeneCoexpressionAssociation.md)
 * [GeneToGeneHomologyAssociation](GeneToGeneHomologyAssociation.md)
 * [PairwiseGeneToGeneInteraction](PairwiseGeneToGeneInteraction.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Local names:** | | annotation subject (ga4gh) |
|  | | node with outgoing relationship (neo4j) |
| **Mappings:** | | rdf:subject |
| **Exact Mappings:** | | owl:annotatedSource |
|  | | OBAN:association_has_subject |

