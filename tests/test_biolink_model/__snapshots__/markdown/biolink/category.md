
# Slot: category


Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}

URI: [biolink:category](https://w3id.org/biolink/vocab/category)


## Domain and Range

[Entity](Entity.md) &#8594;  <sub>0..\*</sub> [CategoryType](types/CategoryType.md)

## Parents

 *  is_a: [type](type.md)

## Children

 *  [association➞category](association_category.md)
 *  [named thing➞category](named_thing_category.md)

## Used by

 * [Entity](Entity.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | translator_minimal |

