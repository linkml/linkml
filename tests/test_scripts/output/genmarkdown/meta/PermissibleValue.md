
# Class: PermissibleValue


a permissible value, accompanied by intended text and an optional mapping to a concept URI

URI: [linkml:PermissibleValue](https://w3id.org/linkml/PermissibleValue)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[PermissibleValue]<mixins%200..*-%20[PermissibleValue&#124;text:string;description:string%20%3F;meaning:uriorcurie%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F],[PermissibleValue]<is_a%200..1-%20[PermissibleValue],[SubsetDefinition]<in_subset%200..*-%20[PermissibleValue],[Example]<examples%200..*-++[PermissibleValue],[AltDescription]<alt_descriptions%200..*-++[PermissibleValue],[EnumDefinition]++-%20permissible_values%200..*>[PermissibleValue],[PermissibleValue]uses%20-.->[Extensible],[PermissibleValue]uses%20-.->[Annotatable],[Extension],[Extensible],[Example],[EnumDefinition],[Annotation],[Annotatable],[AltDescription])

## Uses Mixins

 *  mixin: [Extensible](Extensible.md) - mixin for classes that support extension
 *  mixin: [Annotatable](Annotatable.md) - mixin for classes that support annotations

## Referenced by class

 *  **[PermissibleValue](PermissibleValue.md)** *[permissible_value➞is_a](permissible_value_is_a.md)*  <sub>OPT</sub>  **[PermissibleValue](PermissibleValue.md)**
 *  **[PermissibleValue](PermissibleValue.md)** *[permissible_value➞mixins](permissible_value_mixins.md)*  <sub>0..*</sub>  **[PermissibleValue](PermissibleValue.md)**
 *  **[EnumDefinition](EnumDefinition.md)** *[permissible_values](permissible_values.md)*  <sub>0..*</sub>  **[PermissibleValue](PermissibleValue.md)**

## Attributes


### Own

 * [alt_descriptions](alt_descriptions.md)  <sub>0..*</sub>
     * range: [AltDescription](AltDescription.md)
 * [comments](comments.md)  <sub>0..*</sub>
     * Description: notes and comments about an element intended for external consumption
     * range: [String](types/String.md)
     * in subsets: (owl)
 * [deprecated](deprecated.md)  <sub>OPT</sub>
     * Description: Description of why and when this element will no longer be used
     * range: [String](types/String.md)
 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>OPT</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>OPT</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [description](description.md)  <sub>OPT</sub>
     * Description: a description of the element's purpose and use
     * range: [String](types/String.md)
     * in subsets: (owl)
 * [examples](examples.md)  <sub>0..*</sub>
     * Description: example usages of an element
     * range: [Example](Example.md)
     * in subsets: (owl)
 * [from_schema](from_schema.md)  <sub>OPT</sub>
     * Description: id of the schema that defined the element
     * range: [Uri](types/Uri.md)
 * [imported_from](imported_from.md)  <sub>OPT</sub>
     * Description: the imports entry that this element was derived from.  Empty means primary source
     * range: [String](types/String.md)
 * [in_subset](in_subset.md)  <sub>0..*</sub>
     * Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
     * range: [SubsetDefinition](SubsetDefinition.md)
 * [meaning](meaning.md)  <sub>OPT</sub>
     * Description: the value meaning (in the 11179 sense) of a permissible value
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [notes](notes.md)  <sub>0..*</sub>
     * Description: editorial notes about an element intended for internal consumption
     * range: [String](types/String.md)
     * in subsets: (owl)
 * [permissible_value➞is_a](permissible_value_is_a.md)  <sub>OPT</sub>
     * range: [PermissibleValue](PermissibleValue.md)
 * [permissible_value➞mixins](permissible_value_mixins.md)  <sub>0..*</sub>
     * range: [PermissibleValue](PermissibleValue.md)
 * [see_also](see_also.md)  <sub>0..*</sub>
     * Description: a reference
     * range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (owl)
 * [text](text.md)  <sub>REQ</sub>
     * range: [String](types/String.md)
 * [todos](todos.md)  <sub>0..*</sub>
     * Description: Outstanding issue that needs resolution
     * range: [String](types/String.md)

### Mixed in from annotatable:

 * [annotations](annotations.md)  <sub>0..*</sub>
     * Description: a collection of tag/text tuples with the semantics of OWL Annotation
     * range: [Annotation](Annotation.md)

### Mixed in from extensible:

 * [extensions](extensions.md)  <sub>0..*</sub>
     * Description: a tag/text tuple attached to an arbitrary element
     * range: [Extension](Extension.md)
