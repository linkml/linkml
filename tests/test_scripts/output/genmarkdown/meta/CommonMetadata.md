
# Class: common_metadata


Generic metadata shared across definitions

URI: [linkml:CommonMetadata](https://w3id.org/linkml/CommonMetadata)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[Example],[StructuredAlias]<structured_aliases%200..*-++[CommonMetadata&#124;description:string%20%3F;title:string%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;source:uriorcurie%20%3F;in_language:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F;aliases:string%20*;mappings:uriorcurie%20*;exact_mappings:uriorcurie%20*;close_mappings:uriorcurie%20*;related_mappings:uriorcurie%20*;narrow_mappings:uriorcurie%20*;broad_mappings:uriorcurie%20*;rank:integer%20%3F],[SubsetDefinition]<in_subset%200..*-%20[CommonMetadata],[Example]<examples%200..*-++[CommonMetadata],[AltDescription]<alt_descriptions%200..*-++[CommonMetadata],[UniqueKey]uses%20-.->[CommonMetadata],[StructuredAlias]uses%20-.->[CommonMetadata],[PermissibleValue]uses%20-.->[CommonMetadata],[PatternExpression]uses%20-.->[CommonMetadata],[PathExpression]uses%20-.->[CommonMetadata],[ImportExpression]uses%20-.->[CommonMetadata],[Element]uses%20-.->[CommonMetadata],[ClassRule]uses%20-.->[CommonMetadata],[AnonymousExpression]uses%20-.->[CommonMetadata],[UniqueKey],[PermissibleValue],[PatternExpression],[PathExpression],[ImportExpression],[Element],[ClassRule],[AnonymousExpression],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[Example],[StructuredAlias]<structured_aliases%200..*-++[CommonMetadata&#124;description:string%20%3F;title:string%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;source:uriorcurie%20%3F;in_language:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F;aliases:string%20*;mappings:uriorcurie%20*;exact_mappings:uriorcurie%20*;close_mappings:uriorcurie%20*;related_mappings:uriorcurie%20*;narrow_mappings:uriorcurie%20*;broad_mappings:uriorcurie%20*;rank:integer%20%3F],[SubsetDefinition]<in_subset%200..*-%20[CommonMetadata],[Example]<examples%200..*-++[CommonMetadata],[AltDescription]<alt_descriptions%200..*-++[CommonMetadata],[UniqueKey]uses%20-.->[CommonMetadata],[StructuredAlias]uses%20-.->[CommonMetadata],[PermissibleValue]uses%20-.->[CommonMetadata],[PatternExpression]uses%20-.->[CommonMetadata],[PathExpression]uses%20-.->[CommonMetadata],[ImportExpression]uses%20-.->[CommonMetadata],[Element]uses%20-.->[CommonMetadata],[ClassRule]uses%20-.->[CommonMetadata],[AnonymousExpression]uses%20-.->[CommonMetadata],[UniqueKey],[PermissibleValue],[PatternExpression],[PathExpression],[ImportExpression],[Element],[ClassRule],[AnonymousExpression],[AltDescription])

## Mixin for

 * [AnonymousExpression](AnonymousExpression.md) (mixin) 
 * [ClassRule](ClassRule.md) (mixin)  - A rule that applies to instances of a class
 * [Element](Element.md) (mixin)  - a named element in the model
 * [ImportExpression](ImportExpression.md) (mixin)  - an expression describing an import
 * [PathExpression](PathExpression.md) (mixin)  - An expression that describes an abstract path from an object to another through a sequence of slot lookups
 * [PatternExpression](PatternExpression.md) (mixin)  - a regular expression pattern used to evaluate conformance of a string
 * [PermissibleValue](PermissibleValue.md) (mixin)  - a permissible value, accompanied by intended text and an optional mapping to a concept URI
 * [StructuredAlias](StructuredAlias.md) (mixin)  - object that contains meta data about a synonym or alias including where it came from (source) and its scope (narrow, broad, etc.)
 * [UniqueKey](UniqueKey.md) (mixin)  - a collection of slots whose values uniquely identify an instance of a class

## Referenced by Class


## Attributes


### Own

 * [description](description.md)  <sub>0..1</sub>
     * Description: a description of the element's purpose and use
     * Range: [String](types/String.md)
     * in subsets: (basic)
 * [alt_descriptions](alt_descriptions.md)  <sub>0..\*</sub>
     * Range: [AltDescription](AltDescription.md)
     * in subsets: (basic)
 * [title](title.md)  <sub>0..1</sub>
     * Description: the official title of the element
     * Range: [String](types/String.md)
     * in subsets: (owl,basic)
 * [deprecated](deprecated.md)  <sub>0..1</sub>
     * Description: Description of why and when this element will no longer be used
     * Range: [String](types/String.md)
     * in subsets: (basic)
 * [todos](todos.md)  <sub>0..\*</sub>
     * Description: Outstanding issue that needs resolution
     * Range: [String](types/String.md)
     * in subsets: (basic)
 * [notes](notes.md)  <sub>0..\*</sub>
     * Description: editorial notes about an element intended for internal consumption
     * Range: [String](types/String.md)
     * in subsets: (owl,basic)
 * [comments](comments.md)  <sub>0..\*</sub>
     * Description: notes and comments about an element intended for external consumption
     * Range: [String](types/String.md)
     * in subsets: (owl,basic)
 * [examples](examples.md)  <sub>0..\*</sub>
     * Description: example usages of an element
     * Range: [Example](Example.md)
     * in subsets: (owl,basic)
 * [in_subset](in_subset.md)  <sub>0..\*</sub>
     * Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
     * Range: [SubsetDefinition](SubsetDefinition.md)
     * in subsets: (basic)
 * [from_schema](from_schema.md)  <sub>0..1</sub>
     * Description: id of the schema that defined the element
     * Range: [Uri](types/Uri.md)
 * [imported_from](imported_from.md)  <sub>0..1</sub>
     * Description: the imports entry that this element was derived from.  Empty means primary source
     * Range: [String](types/String.md)
 * [source](source.md)  <sub>0..1</sub>
     * Description: A related resource from which the element is derived.
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (basic)
 * [in_language](in_language.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [see_also](see_also.md)  <sub>0..\*</sub>
     * Description: a reference
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (owl,basic)
 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [aliases](aliases.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)
     * in subsets: (basic)
 * [structured_aliases](structured_aliases.md)  <sub>0..\*</sub>
     * Description: A list of structured_alias objects.
     * Range: [StructuredAlias](StructuredAlias.md)
 * [mappings](mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [exact mappings](exact_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have identical meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [close mappings](close_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have close meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [related mappings](related_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have related meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [narrow mappings](narrow_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have narrower meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [broad mappings](broad_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have broader meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [rank](rank.md)  <sub>0..1</sub>
     * Description: the relative order in which the element occurs, lower values are given precedence
     * Range: [Integer](types/Integer.md)
     * in subsets: (basic)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | basic |

