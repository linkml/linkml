
# Class: unique_key


a collection of slots whose values uniquely identify an instance of a class

URI: [linkml:UniqueKey](https://w3id.org/linkml/UniqueKey)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SlotDefinition]<unique_key_slots%201..*-%20[UniqueKey],[UniqueKey]uses%20-.->[Extensible],[UniqueKey]uses%20-.->[Annotatable],[SlotDefinition],[Extension],[Extensible],[ClassDefinition],[Annotation],[Annotatable])](https://yuml.me/diagram/nofunky;dir:TB/class/[SlotDefinition]<unique_key_slots%201..*-%20[UniqueKey],[UniqueKey]uses%20-.->[Extensible],[UniqueKey]uses%20-.->[Annotatable],[SlotDefinition],[Extension],[Extensible],[ClassDefinition],[Annotation],[Annotatable])

## Uses Mixin

 *  mixin: [Extensible](Extensible.md) - mixin for classes that support extension
 *  mixin: [Annotatable](Annotatable.md) - mixin for classes that support annotations

## Referenced by Class

 *  **[ClassDefinition](ClassDefinition.md)** *[unique_keys](unique_keys.md)*  <sub>0..\*</sub>  **[UniqueKey](UniqueKey.md)**

## Attributes


### Own

 * [unique_key_slots](unique_key_slots.md)  <sub>1..\*</sub>
     * Description: list of slot names that form a key
     * Range: [SlotDefinition](SlotDefinition.md)

### Mixed in from extensible:

 * [extensions](extensions.md)  <sub>0..\*</sub>
     * Description: a tag/text tuple attached to an arbitrary element
     * Range: [Extension](Extension.md)

### Mixed in from annotatable:

 * [annotations](annotations.md)  <sub>0..\*</sub>
     * Description: a collection of tag/text tuples with the semantics of OWL Annotation
     * Range: [Annotation](Annotation.md)
