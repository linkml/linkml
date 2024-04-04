
# Slot: represents_relationship


true if this class represents a relationship rather than an entity

URI: [linkml:represents_relationship](https://w3id.org/linkml/represents_relationship)


## Domain and Range

[ClassDefinition](ClassDefinition.md) &#8594;  <sub>0..1</sub> [Boolean](types/Boolean.md)

## Parents


## Children


## Used by

 * [ClassDefinition](ClassDefinition.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | is_reified |
| **Comments:** | | in the context of Entity-Relationship (ER) modeling, this is used to state that a class models a relationship between entities, and should be drawn with a diamond |
|  | | in the context of RDF, this should be used when instances of the class are `rdf:Statement`s |
|  | | in the context of property graphs, this should be used when a class is used to represent an edge that connects nodes |
| **See also:** | | [rdf:Statement](rdf:Statement) |
|  | | [https://patterns.dataincubator.org/book/qualified-relation.html](https://patterns.dataincubator.org/book/qualified-relation.html) |

