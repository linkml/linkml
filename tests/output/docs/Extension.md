
# Class: Extension


a tag/value pair used to add non-model information to an entry

URI: [linkml:Extension](https://w3id.org/linkml/Extension)


![img](images/Extension.svg)

## Children

 * [Annotation](Annotation.md) - a tag/value pair with the semantics of OWL Annotation

## Referenced by class

 *  **[Extensible](Extensible.md)** *[extensions](extensions.md)*  <sub>0..*</sub>
  **[Extension](Extension.md)**

## Attributes


### Own

 * [extension➞tag](extension_tag.md)  <sub>REQ</sub>

     * Description: a tag associated with an extension
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [extension➞value](extension_value.md)  <sub>REQ</sub>

     * Description: the actual annotation
     * range: [String](types/String.md)
 * [extensions](extensions.md)  <sub>0..*</sub>

     * Description: a tag/text tuple attached to an arbitrary element
     * range: [Extension](Extension.md)
