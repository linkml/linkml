
# Class: extensible


mixin for classes that support extension

URI: [linkml:Extensible](https://w3id.org/linkml/Extensible)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Extension],[Extension]<extensions%200..*-++[Extensible],[UniqueKey]uses%20-.->[Extensible],[PermissibleValue]uses%20-.->[Extensible],[Element]uses%20-.->[Extensible],[UniqueKey],[PermissibleValue],[Element])](https://yuml.me/diagram/nofunky;dir:TB/class/[Extension],[Extension]<extensions%200..*-++[Extensible],[UniqueKey]uses%20-.->[Extensible],[PermissibleValue]uses%20-.->[Extensible],[Element]uses%20-.->[Extensible],[UniqueKey],[PermissibleValue],[Element])

## Mixin for

 * [Element](Element.md) (mixin)  - a named element in the model
 * [PermissibleValue](PermissibleValue.md) (mixin)  - a permissible value, accompanied by intended text and an optional mapping to a concept URI
 * [UniqueKey](UniqueKey.md) (mixin)  - a collection of slots whose values uniquely identify an instance of a class

## Referenced by Class


## Attributes


### Own

 * [extensions](extensions.md)  <sub>0..\*</sub>
     * Description: a tag/text tuple attached to an arbitrary element
     * Range: [Extension](Extension.md)
