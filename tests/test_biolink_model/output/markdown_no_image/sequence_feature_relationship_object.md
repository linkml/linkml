
# Slot: object


connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.

URI: [biolink:sequence_feature_relationship_object](https://w3id.org/biolink/vocab/sequence_feature_relationship_object)


## Domain and Range

[SequenceFeatureRelationship](SequenceFeatureRelationship.md) &#8594;  <sub>1..1</sub> [GenomicEntity](GenomicEntity.md)

## Parents

 *  is_a: [object](object.md)

## Children

 *  [exon to transcript relationship➞object](exon_to_transcript_relationship_object.md)
 *  [gene to gene product relationship➞object](gene_to_gene_product_relationship_object.md)
 *  [transcript to gene relationship➞object](transcript_to_gene_relationship_object.md)

## Used by

 * [SequenceFeatureRelationship](SequenceFeatureRelationship.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Local names:** | | descriptor (ga4gh) |
|  | | node with incoming relationship (neo4j) |
| **Mappings:** | | rdf:object |
| **Exact Mappings:** | | owl:annotatedTarget |
|  | | OBAN:association_has_object |

