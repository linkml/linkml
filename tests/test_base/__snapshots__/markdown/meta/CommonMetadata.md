
# Class: common_metadata

Generic metadata shared across definitions

URI: [linkml:CommonMetadata](https://w3id.org/linkml/CommonMetadata)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[Example],[StructuredAlias]<structured_aliases%200..*-++[CommonMetadata&#124;description:string%20%3F;title:string%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;source:uriorcurie%20%3F;in_language:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F;aliases:string%20*;mappings:uriorcurie%20*;exact_mappings:uriorcurie%20*;close_mappings:uriorcurie%20*;related_mappings:uriorcurie%20*;narrow_mappings:uriorcurie%20*;broad_mappings:uriorcurie%20*;created_by:uriorcurie%20%3F;contributors:uriorcurie%20*;created_on:datetime%20%3F;last_updated_on:datetime%20%3F;modified_by:uriorcurie%20%3F;status:uriorcurie%20%3F;rank:integer%20%3F;categories:uriorcurie%20*;keywords:string%20*],[SubsetDefinition]<in_subset%200..*-%20[CommonMetadata],[Example]<examples%200..*-++[CommonMetadata],[AltDescription]<alt_descriptions%200..*-++[CommonMetadata],[UniqueKey]uses%20-.->[CommonMetadata],[TypeMapping]uses%20-.->[CommonMetadata],[StructuredAlias]uses%20-.->[CommonMetadata],[PermissibleValue]uses%20-.->[CommonMetadata],[PatternExpression]uses%20-.->[CommonMetadata],[PathExpression]uses%20-.->[CommonMetadata],[ImportExpression]uses%20-.->[CommonMetadata],[EnumBinding]uses%20-.->[CommonMetadata],[Element]uses%20-.->[CommonMetadata],[DimensionExpression]uses%20-.->[CommonMetadata],[ClassRule]uses%20-.->[CommonMetadata],[ArrayExpression]uses%20-.->[CommonMetadata],[AnonymousExpression]uses%20-.->[CommonMetadata],[UniqueKey],[TypeMapping],[PermissibleValue],[PatternExpression],[PathExpression],[ImportExpression],[EnumBinding],[Element],[DimensionExpression],[ClassRule],[ArrayExpression],[AnonymousExpression],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[Example],[StructuredAlias]<structured_aliases%200..*-++[CommonMetadata&#124;description:string%20%3F;title:string%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;source:uriorcurie%20%3F;in_language:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F;aliases:string%20*;mappings:uriorcurie%20*;exact_mappings:uriorcurie%20*;close_mappings:uriorcurie%20*;related_mappings:uriorcurie%20*;narrow_mappings:uriorcurie%20*;broad_mappings:uriorcurie%20*;created_by:uriorcurie%20%3F;contributors:uriorcurie%20*;created_on:datetime%20%3F;last_updated_on:datetime%20%3F;modified_by:uriorcurie%20%3F;status:uriorcurie%20%3F;rank:integer%20%3F;categories:uriorcurie%20*;keywords:string%20*],[SubsetDefinition]<in_subset%200..*-%20[CommonMetadata],[Example]<examples%200..*-++[CommonMetadata],[AltDescription]<alt_descriptions%200..*-++[CommonMetadata],[UniqueKey]uses%20-.->[CommonMetadata],[TypeMapping]uses%20-.->[CommonMetadata],[StructuredAlias]uses%20-.->[CommonMetadata],[PermissibleValue]uses%20-.->[CommonMetadata],[PatternExpression]uses%20-.->[CommonMetadata],[PathExpression]uses%20-.->[CommonMetadata],[ImportExpression]uses%20-.->[CommonMetadata],[EnumBinding]uses%20-.->[CommonMetadata],[Element]uses%20-.->[CommonMetadata],[DimensionExpression]uses%20-.->[CommonMetadata],[ClassRule]uses%20-.->[CommonMetadata],[ArrayExpression]uses%20-.->[CommonMetadata],[AnonymousExpression]uses%20-.->[CommonMetadata],[UniqueKey],[TypeMapping],[PermissibleValue],[PatternExpression],[PathExpression],[ImportExpression],[EnumBinding],[Element],[DimensionExpression],[ClassRule],[ArrayExpression],[AnonymousExpression],[AltDescription])

## Mixin for

 * [AnonymousExpression](AnonymousExpression.md) (mixin)  - An abstract parent class for any nested expression
 * [ArrayExpression](ArrayExpression.md) (mixin)  - defines the dimensions of an array
 * [ClassRule](ClassRule.md) (mixin)  - A rule that applies to instances of a class
 * [DimensionExpression](DimensionExpression.md) (mixin)  - defines one of the dimensions of an array
 * [Element](Element.md) (mixin)  - A named element in the model
 * [EnumBinding](EnumBinding.md) (mixin)  - A binding of a slot or a class to a permissible value from an enumeration.
 * [ImportExpression](ImportExpression.md) (mixin)  - an expression describing an import
 * [PathExpression](PathExpression.md) (mixin)  - An expression that describes an abstract path from an object to another through a sequence of slot lookups
 * [PatternExpression](PatternExpression.md) (mixin)  - a regular expression pattern used to evaluate conformance of a string
 * [PermissibleValue](PermissibleValue.md) (mixin)  - a permissible value, accompanied by intended text and an optional mapping to a concept URI
 * [StructuredAlias](StructuredAlias.md) (mixin)  - object that contains meta data about a synonym or alias including where it came from (source) and its scope (narrow, broad, etc.)
 * [TypeMapping](TypeMapping.md) (mixin)  - Represents how a slot or type can be serialized to a format.
 * [UniqueKey](UniqueKey.md) (mixin)  - a collection of slots whose values uniquely identify an instance of a class

## Referenced by Class


## Attributes


### Own

 * [description](description.md)  <sub>0..1</sub>
     * Description: a textual description of the element's purpose and use
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [alt_descriptions](alt_descriptions.md)  <sub>0..\*</sub>
     * Description: A sourced alternative description for an element
     * Range: [AltDescription](AltDescription.md)
     * in subsets: (BasicSubset)
 * [title](title.md)  <sub>0..1</sub>
     * Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [deprecated](deprecated.md)  <sub>0..1</sub>
     * Description: Description of why and when this element will no longer be used
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [todos](todos.md)  <sub>0..\*</sub>
     * Description: Outstanding issues that needs resolution
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [notes](notes.md)  <sub>0..\*</sub>
     * Description: editorial notes about an element intended primarily for internal consumption
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [comments](comments.md)  <sub>0..\*</sub>
     * Description: notes and comments about an element intended primarily for external consumption
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [examples](examples.md)  <sub>0..\*</sub>
     * Description: example usages of an element
     * Range: [Example](Example.md)
     * in subsets: (BasicSubset)
 * [in_subset](in_subset.md)  <sub>0..\*</sub>
     * Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
     * Range: [SubsetDefinition](SubsetDefinition.md)
     * in subsets: (BasicSubset)
 * [from_schema](from_schema.md)  <sub>0..1</sub>
     * Description: id of the schema that defined the element
     * Range: [Uri](types/Uri.md)
     * in subsets: (SpecificationSubset)
 * [imported_from](imported_from.md)  <sub>0..1</sub>
     * Description: the imports entry that this element was derived from.  Empty means primary source
     * Range: [String](types/String.md)
 * [source](source.md)  <sub>0..1</sub>
     * Description: A related resource from which the element is derived.
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (BasicSubset)
 * [in_language](in_language.md)  <sub>0..1</sub>
     * Description: the primary language used in the sources
     * Range: [String](types/String.md)
 * [see_also](see_also.md)  <sub>0..\*</sub>
     * Description: A list of related entities or URLs that may be of relevance
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (BasicSubset)
 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [aliases](aliases.md)  <sub>0..\*</sub>
     * Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [structured_aliases](structured_aliases.md)  <sub>0..\*</sub>
     * Description: A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.
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
 * [created_by](created_by.md)  <sub>0..1</sub>
     * Description: agent that created the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (BasicSubset)
 * [contributors](contributors.md)  <sub>0..\*</sub>
     * Description: agent that contributed to the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (BasicSubset)
 * [created_on](created_on.md)  <sub>0..1</sub>
     * Description: time at which the element was created
     * Range: [Datetime](types/Datetime.md)
     * in subsets: (BasicSubset)
 * [last_updated_on](last_updated_on.md)  <sub>0..1</sub>
     * Description: time at which the element was last updated
     * Range: [Datetime](types/Datetime.md)
     * in subsets: (BasicSubset)
 * [modified_by](modified_by.md)  <sub>0..1</sub>
     * Description: agent that modified the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (BasicSubset)
 * [status](status.md)  <sub>0..1</sub>
     * Description: status of the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * Example: bibo:draft None
     * in subsets: (BasicSubset)
 * [rank](rank.md)  <sub>0..1</sub>
     * Description: the relative order in which the element occurs, lower values are given precedence
     * Range: [Integer](types/Integer.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [categories](categories.md)  <sub>0..\*</sub>
     * Description: Controlled terms used to categorize an element.
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (BasicSubset)
 * [keywords](keywords.md)  <sub>0..\*</sub>
     * Description: Keywords or tags used to describe the element
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | BasicSubset |