
# Class: Annotation


a tag/value pair with the semantics of OWL Annotation

URI: [linkml:Annotation](https://w3id.org/linkml/Annotation)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Extension],[Annotation]<annotations%200..*-++[Annotation&#124;tag(i):uriorcurie;value(i):string],[Annotation]uses%20-.->[Annotatable],[Extension]^-[Annotation],[Annotatable])

## Parents

 *  is_a: [Extension](Extension.md) - a tag/value pair used to add non-model information to an entry

## Uses Mixins

 *  mixin: [Annotatable](Annotatable.md) - mixin for classes that support annotations

## Referenced by class

 *  **[Annotatable](Annotatable.md)** *[annotations](annotations.md)*  <sub>0..*</sub>
  **[Annotation](Annotation.md)**

## Attributes


### Own

 * [annotations](annotations.md)  <sub>0..*</sub>

     * Description: a collection of tag/text tuples with the semantics of OWL Annotation
     * range: [Annotation](Annotation.md)

### Inherited from extension:

 * [extension➞tag](extension_tag.md)  <sub>REQ</sub>

     * Description: a tag associated with an extension
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [extension➞value](extension_value.md)  <sub>REQ</sub>

     * Description: the actual annotation
     * range: [String](types/String.md)
 * [extensions](extensions.md)  <sub>0..*</sub>

     * Description: a tag/text tuple attached to an arbitrary element
     * range: [Extension](Extension.md)
