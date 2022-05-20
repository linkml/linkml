
# Class: extensible


mixin for classes that support extension

URI: [linkml:Extensible](https://w3id.org/linkml/Extensible)


[![img](images/Extensible.svg)](images/Extensible.svg)

## Mixin for

 * [AnonymousExpression](AnonymousExpression.md) (mixin) 
 * [ClassRule](ClassRule.md) (mixin)  - A rule that applies to instances of a class
 * [Element](Element.md) (mixin)  - a named element in the model
 * [ImportExpression](ImportExpression.md) (mixin)  - an expression describing an import
 * [PathExpression](PathExpression.md) (mixin)  - An expression that describes an abstract path from an object to another through a sequence of slot lookups
 * [PatternExpression](PatternExpression.md) (mixin)  - a regular expression pattern used to evaluate conformance of a string
 * [PermissibleValue](PermissibleValue.md) (mixin)  - a permissible value, accompanied by intended text and an optional mapping to a concept URI
 * [StructuredAlias](StructuredAlias.md) (mixin)  - object that contains meta data about a synonym or alias including where it came from (source) and its scope (narrow, broad, etc.)
 * [UniqueKey](UniqueKey.md) (mixin)  - a collection of slots whose values uniquely identify an instance of a class

## Referenced by Class


## Attributes


### Own

 * [extensions](extensions.md)  <sub>0..\*</sub>
     * Description: a tag/text tuple attached to an arbitrary element
     * Range: [Extension](Extension.md)
