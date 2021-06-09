
# Class: Extensible


mixin for classes that support extension

URI: [linkml:Extensible](https://w3id.org/linkml/Extensible)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Extension],[Extension]<extensions%200..*-++[Extensible],[PermissibleValue]uses%20-.->[Extensible],[Element]uses%20-.->[Extensible],[PermissibleValue],[Element])

## Mixin for

 * [Element](Element.md) (mixin)  - a named element in the model
 * [PermissibleValue](PermissibleValue.md) (mixin)  - a permissible value, accompanied by intended text and an optional mapping to a concept URI

## Referenced by class


## Attributes


### Own

 * [extensions](extensions.md)  <sub>0..\*</sub>
     * Description: a tag/text tuple attached to an arbitrary element
     * Range: [Extension](Extension.md)
