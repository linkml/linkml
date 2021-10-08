
# Class: permissible_value


a permissible value, accompanied by intended text and an optional mapping to a concept URI

URI: [linkml:PermissibleValue](https://w3id.org/linkml/PermissibleValue)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[PermissibleValue]<mixins%200..*-%20[PermissibleValue&#124;text:string;description:string%20%3F;meaning:uriorcurie%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F],[PermissibleValue]<is_a%200..1-%20[PermissibleValue],[EnumDefinition]++-%20permissible_values%200..*>[PermissibleValue],[PermissibleValue]uses%20-.->[Extensible],[PermissibleValue]uses%20-.->[Annotatable],[PermissibleValue]uses%20-.->[CommonMetadata],[Extension],[Extensible],[Example],[EnumDefinition],[CommonMetadata],[Annotation],[Annotatable],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[PermissibleValue]<mixins%200..*-%20[PermissibleValue&#124;text:string;description:string%20%3F;meaning:uriorcurie%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F],[PermissibleValue]<is_a%200..1-%20[PermissibleValue],[EnumDefinition]++-%20permissible_values%200..*>[PermissibleValue],[PermissibleValue]uses%20-.->[Extensible],[PermissibleValue]uses%20-.->[Annotatable],[PermissibleValue]uses%20-.->[CommonMetadata],[Extension],[Extensible],[Example],[EnumDefinition],[CommonMetadata],[Annotation],[Annotatable],[AltDescription])

## Uses Mixin

 *  mixin: [Extensible](Extensible.md) - mixin for classes that support extension
 *  mixin: [Annotatable](Annotatable.md) - mixin for classes that support annotations
 *  mixin: [CommonMetadata](CommonMetadata.md) - Generic metadata shared across definitions

## Referenced by Class

 *  **[PermissibleValue](PermissibleValue.md)** *[permissible_value➞is_a](permissible_value_is_a.md)*  <sub>0..1</sub>  **[PermissibleValue](PermissibleValue.md)**
 *  **[PermissibleValue](PermissibleValue.md)** *[permissible_value➞mixins](permissible_value_mixins.md)*  <sub>0..\*</sub>  **[PermissibleValue](PermissibleValue.md)**
 *  **[EnumDefinition](EnumDefinition.md)** *[permissible_values](permissible_values.md)*  <sub>0..\*</sub>  **[PermissibleValue](PermissibleValue.md)**

## Attributes


### Own

 * [text](text.md)  <sub>1..1</sub>
     * Range: [String](String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: a description of the element's purpose and use
     * Range: [String](String.md)
     * in subsets: (owl)
 * [meaning](meaning.md)  <sub>0..1</sub>
     * Description: the value meaning (in the 11179 sense) of a permissible value
     * Range: [Uriorcurie](Uriorcurie.md)
 * [permissible_value➞is_a](permissible_value_is_a.md)  <sub>0..1</sub>
     * Description: specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
     * Range: [PermissibleValue](PermissibleValue.md)
 * [permissible_value➞mixins](permissible_value_mixins.md)  <sub>0..\*</sub>
     * Description: List of definitions to be mixed in. Targets may be any definition of the same type
     * Range: [PermissibleValue](PermissibleValue.md)

### Mixed in from extensible:

 * [extensions](extensions.md)  <sub>0..\*</sub>
     * Description: a tag/text tuple attached to an arbitrary element
     * Range: [Extension](Extension.md)

### Mixed in from annotatable:

 * [annotations](annotations.md)  <sub>0..\*</sub>
     * Description: a collection of tag/text tuples with the semantics of OWL Annotation
     * Range: [Annotation](Annotation.md)

### Mixed in from common_metadata:

 * [alt_descriptions](alt_descriptions.md)  <sub>0..\*</sub>
     * Range: [AltDescription](AltDescription.md)

### Mixed in from common_metadata:

 * [deprecated](deprecated.md)  <sub>0..1</sub>
     * Description: Description of why and when this element will no longer be used
     * Range: [String](String.md)

### Mixed in from common_metadata:

 * [todos](todos.md)  <sub>0..\*</sub>
     * Description: Outstanding issue that needs resolution
     * Range: [String](String.md)

### Mixed in from common_metadata:

 * [notes](notes.md)  <sub>0..\*</sub>
     * Description: editorial notes about an element intended for internal consumption
     * Range: [String](String.md)
     * in subsets: (owl)

### Mixed in from common_metadata:

 * [comments](comments.md)  <sub>0..\*</sub>
     * Description: notes and comments about an element intended for external consumption
     * Range: [String](String.md)
     * in subsets: (owl)

### Mixed in from common_metadata:

 * [examples](examples.md)  <sub>0..\*</sub>
     * Description: example usages of an element
     * Range: [Example](Example.md)
     * in subsets: (owl)

### Mixed in from common_metadata:

 * [in_subset](in_subset.md)  <sub>0..\*</sub>
     * Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
     * Range: [SubsetDefinition](SubsetDefinition.md)

### Mixed in from common_metadata:

 * [from_schema](from_schema.md)  <sub>0..1</sub>
     * Description: id of the schema that defined the element
     * Range: [Uri](Uri.md)

### Mixed in from common_metadata:

 * [imported_from](imported_from.md)  <sub>0..1</sub>
     * Description: the imports entry that this element was derived from.  Empty means primary source
     * Range: [String](String.md)

### Mixed in from common_metadata:

 * [see_also](see_also.md)  <sub>0..\*</sub>
     * Description: a reference
     * Range: [Uriorcurie](Uriorcurie.md)
     * in subsets: (owl)

### Mixed in from common_metadata:

 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * Range: [Uriorcurie](Uriorcurie.md)

### Mixed in from common_metadata:

 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * Range: [Uriorcurie](Uriorcurie.md)
