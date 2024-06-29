
# Slot: bindings

A collection of enum bindings that specify how a slot can be bound to a permissible value from an enumeration.
LinkML provides enums to allow string values to be restricted to one of a set of permissible values (specified statically or dynamically).
Enum bindings allow enums to be bound to any object, including complex nested objects. For example, given a (generic) class Concept with slots id and label, it may be desirable to restrict the values the id takes on in a given context. For example, a HumanSample class may have a slot for representing sample site, with a range of concept, but the values of that slot may be restricted to concepts from a particular branch of an anatomy ontology.

URI: [linkml:bindings](https://w3id.org/linkml/bindings)


## Domain and Range

[Element](Element.md) &#8594;  <sub>0..\*</sub> [EnumBinding](EnumBinding.md)

## Parents


## Children


## Used by

 * [AnonymousSlotExpression](AnonymousSlotExpression.md)
 * [SchemaDefinition](SchemaDefinition.md)
 * [SlotDefinition](SlotDefinition.md)
 * [SlotExpression](SlotExpression.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | SpecificationSubset |