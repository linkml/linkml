
# Class: annotatable


mixin for classes that support annotations

URI: [linkml:Annotatable](https://w3id.org/linkml/Annotatable)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Annotation],[Annotation]<annotations%200..*-++[Annotatable],[UniqueKey]uses%20-.->[Annotatable],[StructuredAlias]uses%20-.->[Annotatable],[PermissibleValue]uses%20-.->[Annotatable],[PatternExpression]uses%20-.->[Annotatable],[PathExpression]uses%20-.->[Annotatable],[ImportExpression]uses%20-.->[Annotatable],[Element]uses%20-.->[Annotatable],[DimensionExpression]uses%20-.->[Annotatable],[ClassRule]uses%20-.->[Annotatable],[ArrayExpression]uses%20-.->[Annotatable],[AnonymousExpression]uses%20-.->[Annotatable],[Annotation]uses%20-.->[Annotatable],[UniqueKey],[StructuredAlias],[PermissibleValue],[PatternExpression],[PathExpression],[ImportExpression],[Element],[DimensionExpression],[ClassRule],[ArrayExpression],[AnonymousExpression])](https://yuml.me/diagram/nofunky;dir:TB/class/[Annotation],[Annotation]<annotations%200..*-++[Annotatable],[UniqueKey]uses%20-.->[Annotatable],[StructuredAlias]uses%20-.->[Annotatable],[PermissibleValue]uses%20-.->[Annotatable],[PatternExpression]uses%20-.->[Annotatable],[PathExpression]uses%20-.->[Annotatable],[ImportExpression]uses%20-.->[Annotatable],[Element]uses%20-.->[Annotatable],[DimensionExpression]uses%20-.->[Annotatable],[ClassRule]uses%20-.->[Annotatable],[ArrayExpression]uses%20-.->[Annotatable],[AnonymousExpression]uses%20-.->[Annotatable],[Annotation]uses%20-.->[Annotatable],[UniqueKey],[StructuredAlias],[PermissibleValue],[PatternExpression],[PathExpression],[ImportExpression],[Element],[DimensionExpression],[ClassRule],[ArrayExpression],[AnonymousExpression])

## Mixin for

 * [Annotation](Annotation.md) (mixin)  - a tag/value pair with the semantics of OWL Annotation
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

 * [annotations](annotations.md)  <sub>0..\*</sub>
     * Description: a collection of tag/text tuples with the semantics of OWL Annotation
     * Range: [Annotation](Annotation.md)
