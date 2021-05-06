
# Class: Annotatable


mixin for classes that support annotations

URI: [linkml:Annotatable](https://w3id.org/linkml/Annotatable)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Annotation],[Annotation]<annotations%200..*-++[Annotatable],[PermissibleValue]uses%20-.->[Annotatable],[Element]uses%20-.->[Annotatable],[Annotation]uses%20-.->[Annotatable],[PermissibleValue],[Element])

## Mixin for

 * [Annotation](Annotation.md) (mixin)  - a tag/value pair with the semantics of OWL Annotation
 * [Element](Element.md) (mixin)  - a named element in the model
 * [PermissibleValue](PermissibleValue.md) (mixin)  - a permissible value, accompanied by intended text and an optional mapping to a concept URI

## Referenced by class


## Attributes


### Own

 * [annotations](annotations.md)  <sub>0..*</sub>

     * Description: a collection of tag/text tuples with the semantics of OWL Annotation
     * range: [Annotation](Annotation.md)
