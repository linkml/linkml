
# Slot: object


connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.

URI: [biolink:entity_to_phenotypic_feature_association_mixin_object](https://w3id.org/biolink/vocab/entity_to_phenotypic_feature_association_mixin_object)


## Domain and Range

[EntityToPhenotypicFeatureAssociationMixin](EntityToPhenotypicFeatureAssociationMixin.md) &#8594;  <sub>1..1</sub> [PhenotypicFeature](PhenotypicFeature.md)

## Parents

 *  is_a: [object](object.md)

## Children


## Used by

 * [EntityToPhenotypicFeatureAssociationMixin](EntityToPhenotypicFeatureAssociationMixin.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Local names:** | | descriptor (ga4gh) |
|  | | node with incoming relationship (neo4j) |
| **Mappings:** | | rdf:object |
| **Examples:** | | Example(value='HP:0002487', description='Hyperkinesis', object=None) |
|  | | Example(value='WBPhenotype:0000180', description='axon morphology variant', object=None) |
|  | | Example(value='MP:0001569', description='abnormal circulating bilirubin level', object=None) |
| **Exact Mappings:** | | owl:annotatedTarget |
|  | | OBAN:association_has_object |

