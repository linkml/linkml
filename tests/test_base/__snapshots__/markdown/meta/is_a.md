
# Slot: is_a

A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded

URI: [linkml:is_a](https://w3id.org/linkml/is_a)


## Domain and Range

[Definition](Definition.md) &#8594;  <sub>0..1</sub> [Definition](Definition.md)

## Parents


## Children

 *  [class_definition➞is_a](class_definition_is_a.md)
 *  [permissible_value➞is_a](permissible_value_is_a.md)
 *  [slot_definition➞is_a](slot_definition_is_a.md)

## Used by

 * [AnonymousClassExpression](AnonymousClassExpression.md)
 * [Definition](Definition.md)
 * [EnumDefinition](EnumDefinition.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | SpecificationSubset |
|  | | BasicSubset |
|  | | ObjectOrientedProfile |
|  | | OwlProfile |