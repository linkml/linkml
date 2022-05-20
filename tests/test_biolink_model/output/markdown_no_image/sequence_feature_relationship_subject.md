
# Slot: subject


connects an association to the subject of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.

URI: [biolink:sequence_feature_relationship_subject](https://w3id.org/biolink/vocab/sequence_feature_relationship_subject)


## Domain and Range

[SequenceFeatureRelationship](SequenceFeatureRelationship.md) &#8594;  <sub>1..1</sub> [GenomicEntity](GenomicEntity.md)

## Parents

 *  is_a: [subject](subject.md)

## Children

 *  [exon to transcript relationship➞subject](exon_to_transcript_relationship_subject.md)
 *  [gene to gene product relationship➞subject](gene_to_gene_product_relationship_subject.md)
 *  [transcript to gene relationship➞subject](transcript_to_gene_relationship_subject.md)

## Used by

 * [SequenceFeatureRelationship](SequenceFeatureRelationship.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Local names:** | | annotation subject (ga4gh) |
|  | | node with outgoing relationship (neo4j) |
| **Mappings:** | | rdf:subject |
| **Exact Mappings:** | | owl:annotatedSource |
|  | | OBAN:association_has_subject |

