
# Slot: inlined


True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.

URI: [linkml:inlined](https://w3id.org/linkml/inlined)


## Domain and Range

[SlotDefinition](SlotDefinition.md) &#8594;  <sub>0..1</sub> [Boolean](types/Boolean.md)

## Parents


## Children


## Used by

 * [AnonymousSlotExpression](AnonymousSlotExpression.md)
 * [SlotDefinition](SlotDefinition.md)
 * [SlotExpression](SlotExpression.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | classes without keys or identifiers are necessarily inlined as lists |
|  | | only applicable in tree-like serializations, e.g json, yaml |
| **In Subsets:** | | SpecificationSubset |
|  | | BasicSubset |
| **See also:** | | [https://w3id.org/linkml/docs/specification/06mapping/#collection-forms](https://w3id.org/linkml/docs/specification/06mapping/#collection-forms) |
|  | | [https://linkml.io/linkml/schemas/inlining.html](https://linkml.io/linkml/schemas/inlining.html) |

