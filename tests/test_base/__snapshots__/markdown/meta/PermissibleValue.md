
# Class: permissible_value


a permissible value, accompanied by intended text and an optional mapping to a concept URI

URI: [linkml:PermissibleValue](https://w3id.org/linkml/PermissibleValue)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[PermissibleValue]<mixins%200..*-%20[PermissibleValue&#124;text:string;description:string%20%3F;meaning:uriorcurie%20%3F;title:string%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;source:uriorcurie%20%3F;in_language:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F;aliases:string%20*;mappings:uriorcurie%20*;exact_mappings:uriorcurie%20*;close_mappings:uriorcurie%20*;related_mappings:uriorcurie%20*;narrow_mappings:uriorcurie%20*;broad_mappings:uriorcurie%20*;created_by:uriorcurie%20%3F;contributors:uriorcurie%20*;created_on:datetime%20%3F;last_updated_on:datetime%20%3F;modified_by:uriorcurie%20%3F;status:uriorcurie%20%3F;rank:integer%20%3F;categories:uriorcurie%20*;keywords:string%20*],[PermissibleValue]<is_a%200..1-%20[PermissibleValue],[UnitOfMeasure]<unit%200..1-++[PermissibleValue],[EnumExpression]++-%20permissible_values%200..*>[PermissibleValue],[PermissibleValue]uses%20-.->[Extensible],[PermissibleValue]uses%20-.->[Annotatable],[PermissibleValue]uses%20-.->[CommonMetadata],[Extension],[Extensible],[Example],[EnumExpression],[CommonMetadata],[Annotation],[Annotatable],[AltDescription],[UnitOfMeasure])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[PermissibleValue]<mixins%200..*-%20[PermissibleValue&#124;text:string;description:string%20%3F;meaning:uriorcurie%20%3F;title:string%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;source:uriorcurie%20%3F;in_language:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F;aliases:string%20*;mappings:uriorcurie%20*;exact_mappings:uriorcurie%20*;close_mappings:uriorcurie%20*;related_mappings:uriorcurie%20*;narrow_mappings:uriorcurie%20*;broad_mappings:uriorcurie%20*;created_by:uriorcurie%20%3F;contributors:uriorcurie%20*;created_on:datetime%20%3F;last_updated_on:datetime%20%3F;modified_by:uriorcurie%20%3F;status:uriorcurie%20%3F;rank:integer%20%3F;categories:uriorcurie%20*;keywords:string%20*],[PermissibleValue]<is_a%200..1-%20[PermissibleValue],[UnitOfMeasure]<unit%200..1-++[PermissibleValue],[EnumExpression]++-%20permissible_values%200..*>[PermissibleValue],[PermissibleValue]uses%20-.->[Extensible],[PermissibleValue]uses%20-.->[Annotatable],[PermissibleValue]uses%20-.->[CommonMetadata],[Extension],[Extensible],[Example],[EnumExpression],[CommonMetadata],[Annotation],[Annotatable],[AltDescription],[UnitOfMeasure])

## Uses Mixin

 *  mixin: [Extensible](Extensible.md) - mixin for classes that support extension
 *  mixin: [Annotatable](Annotatable.md) - mixin for classes that support annotations
 *  mixin: [CommonMetadata](CommonMetadata.md) - Generic metadata shared across definitions

## Referenced by Class

 *  **[PermissibleValue](PermissibleValue.md)** *[permissible_value➞is_a](permissible_value_is_a.md)*  <sub>0..1</sub>  **[PermissibleValue](PermissibleValue.md)**
 *  **[PermissibleValue](PermissibleValue.md)** *[permissible_value➞mixins](permissible_value_mixins.md)*  <sub>0..\*</sub>  **[PermissibleValue](PermissibleValue.md)**
 *  **[EnumExpression](EnumExpression.md)** *[permissible_values](permissible_values.md)*  <sub>0..\*</sub>  **[PermissibleValue](PermissibleValue.md)**

## Attributes


### Own

 * [text](text.md)  <sub>1..1</sub>
     * Description: The actual permissible value itself
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [description](description.md)  <sub>0..1</sub>
     * Description: a textual description of the element's purpose and use
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [meaning](meaning.md)  <sub>0..1</sub>
     * Description: the value meaning of a permissible value
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [unit](unit.md)  <sub>0..1</sub>
     * Description: an encoding of a unit
     * Range: [UnitOfMeasure](UnitOfMeasure.md)
 * [permissible_value➞is_a](permissible_value_is_a.md)  <sub>0..1</sub>
     * Description: A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
     * Range: [PermissibleValue](PermissibleValue.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile,OwlProfile)
 * [permissible_value➞mixins](permissible_value_mixins.md)  <sub>0..\*</sub>
     * Description: A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.
     * Range: [PermissibleValue](PermissibleValue.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile,OwlProfile)

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
     * Description: A sourced alternative description for an element
     * Range: [AltDescription](AltDescription.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [title](title.md)  <sub>0..1</sub>
     * Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [deprecated](deprecated.md)  <sub>0..1</sub>
     * Description: Description of why and when this element will no longer be used
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [todos](todos.md)  <sub>0..\*</sub>
     * Description: Outstanding issues that needs resolution
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [notes](notes.md)  <sub>0..\*</sub>
     * Description: editorial notes about an element intended primarily for internal consumption
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [comments](comments.md)  <sub>0..\*</sub>
     * Description: notes and comments about an element intended primarily for external consumption
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [examples](examples.md)  <sub>0..\*</sub>
     * Description: example usages of an element
     * Range: [Example](Example.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [in_subset](in_subset.md)  <sub>0..\*</sub>
     * Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
     * Range: [SubsetDefinition](SubsetDefinition.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [from_schema](from_schema.md)  <sub>0..1</sub>
     * Description: id of the schema that defined the element
     * Range: [Uri](types/Uri.md)
     * in subsets: (SpecificationSubset)

### Mixed in from common_metadata:

 * [imported_from](imported_from.md)  <sub>0..1</sub>
     * Description: the imports entry that this element was derived from.  Empty means primary source
     * Range: [String](types/String.md)

### Mixed in from common_metadata:

 * [source](source.md)  <sub>0..1</sub>
     * Description: A related resource from which the element is derived.
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [in_language](in_language.md)  <sub>0..1</sub>
     * Description: the primary language used in the sources
     * Range: [String](types/String.md)

### Mixed in from common_metadata:

 * [see_also](see_also.md)  <sub>0..\*</sub>
     * Description: A list of related entities or URLs that may be of relevance
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [aliases](aliases.md)  <sub>0..\*</sub>
     * Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [structured_aliases](structured_aliases.md)  <sub>0..\*</sub>
     * Description: A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.
     * Range: [StructuredAlias](StructuredAlias.md)

### Mixed in from common_metadata:

 * [mappings](mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [exact mappings](exact_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have identical meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [close mappings](close_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have close meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [related mappings](related_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have related meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [narrow mappings](narrow_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have narrower meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [broad mappings](broad_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have broader meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [created_by](created_by.md)  <sub>0..1</sub>
     * Description: agent that created the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [contributors](contributors.md)  <sub>0..\*</sub>
     * Description: agent that contributed to the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [created_on](created_on.md)  <sub>0..1</sub>
     * Description: time at which the element was created
     * Range: [Datetime](types/Datetime.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [last_updated_on](last_updated_on.md)  <sub>0..1</sub>
     * Description: time at which the element was last updated
     * Range: [Datetime](types/Datetime.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [modified_by](modified_by.md)  <sub>0..1</sub>
     * Description: agent that modified the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [status](status.md)  <sub>0..1</sub>
     * Description: status of the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * Example: bibo:draft None
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [rank](rank.md)  <sub>0..1</sub>
     * Description: the relative order in which the element occurs, lower values are given precedence
     * Range: [Integer](types/Integer.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from common_metadata:

 * [categories](categories.md)  <sub>0..\*</sub>
     * Description: Controlled terms used to categorize an element.
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (BasicSubset)

### Mixed in from common_metadata:

 * [keywords](keywords.md)  <sub>0..\*</sub>
     * Description: Keywords or tags used to describe the element
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | PV |
| **In Subsets:** | | SpecificationSubset |
|  | | BasicSubset |
| **Close Mappings:** | | skos:Concept |

