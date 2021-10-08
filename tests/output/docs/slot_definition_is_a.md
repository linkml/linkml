
# Slot: is_a


specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded

URI: [linkml:slot_definition_is_a](https://w3id.org/linkml/slot_definition_is_a)


## Domain and Range

[SlotDefinition](SlotDefinition.md) &#8594;  <sub>0..1</sub> [SlotDefinition](SlotDefinition.md)

## Parents

 *  is_a: [is_a](is_a.md)

## Children


## Used by

 * [SlotDefinition](SlotDefinition.md)
