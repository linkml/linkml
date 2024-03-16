
# Slot: object


connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.

URI: [biolink:gene_to_disease_association_object](https://w3id.org/biolink/vocab/gene_to_disease_association_object)


## Domain and Range

[GeneToDiseaseAssociation](GeneToDiseaseAssociation.md) &#8594;  <sub>1..1</sub> [Disease](Disease.md)

## Parents

 *  is_a: [object](object.md)

## Children

 *  [gene has variant that contributes to disease association➞object](gene_has_variant_that_contributes_to_disease_association_object.md)

## Used by

 * [DruggableGeneToDiseaseAssociation](DruggableGeneToDiseaseAssociation.md)
 * [GeneAsAModelOfDiseaseAssociation](GeneAsAModelOfDiseaseAssociation.md)
 * [GeneToDiseaseAssociation](GeneToDiseaseAssociation.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Local names:** | | descriptor (ga4gh) |
|  | | node with incoming relationship (neo4j) |
| **Mappings:** | | rdf:object |
| **Exact Mappings:** | | owl:annotatedTarget |
|  | | OBAN:association_has_object |

