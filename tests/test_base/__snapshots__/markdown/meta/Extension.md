
# Class: extension


a tag/value pair used to add non-model information to an entry

URI: [linkml:Extension](https://w3id.org/linkml/Extension)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Extension]<extensions%200..*-++[Extension&#124;tag(pk):uriorcurie],[AnyValue]<value%201..1-++[Extension],[Extension]^-[Annotation],[Extensible],[Annotation],[AnyValue])](https://yuml.me/diagram/nofunky;dir:TB/class/[Extension]<extensions%200..*-++[Extension&#124;tag(pk):uriorcurie],[AnyValue]<value%201..1-++[Extension],[Extension]^-[Annotation],[Extensible],[Annotation],[AnyValue])

## Children

 * [Annotation](Annotation.md) - a tag/value pair with the semantics of OWL Annotation

## Referenced by Class

 *  **[Extensible](Extensible.md)** *[extensions](extensions.md)*  <sub>0..\*</sub>  **[Extension](Extension.md)**

## Attributes


### Own

 * [extension➞tag](extension_tag.md)  <sub>1..1</sub>
     * Description: a tag associated with an extension
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [extension➞value](extension_value.md)  <sub>1..1</sub>
     * Description: the actual annotation
     * Range: [AnyValue](AnyValue.md)
 * [extensions](extensions.md)  <sub>0..\*</sub>
     * Description: a tag/text tuple attached to an arbitrary element
     * Range: [Extension](Extension.md)
