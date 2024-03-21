
# Class: extensible


mixin for classes that support extension

URI: [linkml:Extensible](https://w3id.org/linkml/Extensible)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Extension],[Extension]<extensions%200..*-++[Extensible],[UniqueKey]uses%20-.->[Extensible],[StructuredAlias]uses%20-.->[Extensible],[PermissibleValue]uses%20-.->[Extensible],[PatternExpression]uses%20-.->[Extensible],[PathExpression]uses%20-.->[Extensible],[ImportExpression]uses%20-.->[Extensible],[Element]uses%20-.->[Extensible],[DimensionExpression]uses%20-.->[Extensible],[ClassRule]uses%20-.->[Extensible],[ArrayExpression]uses%20-.->[Extensible],[AnonymousExpression]uses%20-.->[Extensible],[UniqueKey],[StructuredAlias],[PermissibleValue],[PatternExpression],[PathExpression],[ImportExpression],[Element],[DimensionExpression],[ClassRule],[ArrayExpression],[AnonymousExpression])](https://yuml.me/diagram/nofunky;dir:TB/class/[Extension],[Extension]<extensions%200..*-++[Extensible],[UniqueKey]uses%20-.->[Extensible],[StructuredAlias]uses%20-.->[Extensible],[PermissibleValue]uses%20-.->[Extensible],[PatternExpression]uses%20-.->[Extensible],[PathExpression]uses%20-.->[Extensible],[ImportExpression]uses%20-.->[Extensible],[Element]uses%20-.->[Extensible],[DimensionExpression]uses%20-.->[Extensible],[ClassRule]uses%20-.->[Extensible],[ArrayExpression]uses%20-.->[Extensible],[AnonymousExpression]uses%20-.->[Extensible],[UniqueKey],[StructuredAlias],[PermissibleValue],[PatternExpression],[PathExpression],[ImportExpression],[Element],[DimensionExpression],[ClassRule],[ArrayExpression],[AnonymousExpression])

## Mixin for

 * [AnonymousExpression](AnonymousExpression.md) (mixin)  - An abstract parent class for any nested expression
 * [ArrayExpression](ArrayExpression.md) (mixin)  - defines the dimensions of an array
 * [ClassRule](ClassRule.md) (mixin)  - A rule that applies to instances of a class
 * [DimensionExpression](DimensionExpression.md) (mixin)  - defines one of the dimensions of an array
 * [Element](Element.md) (mixin)  - A named element in the model
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
