
# Class: element

A named element in the model

URI: [linkml:Element](https://w3id.org/linkml/Element)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeDefinition],[SubsetDefinition],[StructuredAlias],[SlotDefinition],[SchemaDefinition],[LocalName],[Extension],[Extensible],[Example],[LocalName]<local_names%200..*-++[Element&#124;name:string;id_prefixes:ncname%20*;id_prefixes_are_closed:boolean%20%3F;definition_uri:uriorcurie%20%3F;conforms_to:string%20%3F;implements:uriorcurie%20*;instantiates:uriorcurie%20*;description:string%20%3F;title:string%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;source:uriorcurie%20%3F;in_language:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F;aliases:string%20*;mappings:uriorcurie%20*;exact_mappings:uriorcurie%20*;close_mappings:uriorcurie%20*;related_mappings:uriorcurie%20*;narrow_mappings:uriorcurie%20*;broad_mappings:uriorcurie%20*;created_by:uriorcurie%20%3F;contributors:uriorcurie%20*;created_on:datetime%20%3F;last_updated_on:datetime%20%3F;modified_by:uriorcurie%20%3F;status:uriorcurie%20%3F;rank:integer%20%3F;categories:uriorcurie%20*;keywords:string%20*],[EnumBinding]-%20range(i)%200..1>[Element],[SlotExpression]-%20range%200..1>[Element],[TypeDefinition]-%20union_of(i)%200..*>[Element],[SlotDefinition]-%20union_of(i)%200..*>[Element],[ClassDefinition]-%20union_of(i)%200..*>[Element],[Element]uses%20-.->[Extensible],[Element]uses%20-.->[Annotatable],[Element]uses%20-.->[CommonMetadata],[Element]^-[TypeDefinition],[Element]^-[SubsetDefinition],[Element]^-[SchemaDefinition],[Element]^-[Definition],[SlotExpression],[EnumBinding],[Definition],[CommonMetadata],[ClassDefinition],[Annotation],[Annotatable],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeDefinition],[SubsetDefinition],[StructuredAlias],[SlotDefinition],[SchemaDefinition],[LocalName],[Extension],[Extensible],[Example],[LocalName]<local_names%200..*-++[Element&#124;name:string;id_prefixes:ncname%20*;id_prefixes_are_closed:boolean%20%3F;definition_uri:uriorcurie%20%3F;conforms_to:string%20%3F;implements:uriorcurie%20*;instantiates:uriorcurie%20*;description:string%20%3F;title:string%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;source:uriorcurie%20%3F;in_language:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F;aliases:string%20*;mappings:uriorcurie%20*;exact_mappings:uriorcurie%20*;close_mappings:uriorcurie%20*;related_mappings:uriorcurie%20*;narrow_mappings:uriorcurie%20*;broad_mappings:uriorcurie%20*;created_by:uriorcurie%20%3F;contributors:uriorcurie%20*;created_on:datetime%20%3F;last_updated_on:datetime%20%3F;modified_by:uriorcurie%20%3F;status:uriorcurie%20%3F;rank:integer%20%3F;categories:uriorcurie%20*;keywords:string%20*],[EnumBinding]-%20range(i)%200..1>[Element],[SlotExpression]-%20range%200..1>[Element],[TypeDefinition]-%20union_of(i)%200..*>[Element],[SlotDefinition]-%20union_of(i)%200..*>[Element],[ClassDefinition]-%20union_of(i)%200..*>[Element],[Element]uses%20-.->[Extensible],[Element]uses%20-.->[Annotatable],[Element]uses%20-.->[CommonMetadata],[Element]^-[TypeDefinition],[Element]^-[SubsetDefinition],[Element]^-[SchemaDefinition],[Element]^-[Definition],[SlotExpression],[EnumBinding],[Definition],[CommonMetadata],[ClassDefinition],[Annotation],[Annotatable],[AltDescription])

## Uses Mixin

 *  mixin: [Extensible](Extensible.md) - mixin for classes that support extension
 *  mixin: [Annotatable](Annotatable.md) - mixin for classes that support annotations
 *  mixin: [CommonMetadata](CommonMetadata.md) - Generic metadata shared across definitions

## Children

 * [Definition](Definition.md) - abstract base class for core metaclasses
 * [SchemaDefinition](SchemaDefinition.md) - A collection of definitions that make up a schema or a data model.
 * [SubsetDefinition](SubsetDefinition.md) - an element that can be used to group other metamodel elements
 * [TypeDefinition](TypeDefinition.md) - an element that whose instances are atomic scalar values that can be mapped to primitive types

## Referenced by Class

 *  **[SlotDefinition](SlotDefinition.md)** *[range](range.md)*  <sub>0..1</sub>  **[Element](Element.md)**
 *  **[Element](Element.md)** *[union_of](union_of.md)*  <sub>0..\*</sub>  **[Element](Element.md)**

## Attributes


### Own

 * [name](name.md)  <sub>1..1</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset,OwlProfile,MinimalSubset,BasicSubset,RelationalModelProfile,ObjectOrientedProfile)
 * [id_prefixes](id_prefixes.md)  <sub>0..\*</sub>
     * Description: An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
     * Range: [Ncname](types/Ncname.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [id_prefixes_are_closed](id_prefixes_are_closed.md)  <sub>0..1</sub>
     * Description: If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.
     * Range: [Boolean](types/Boolean.md)
 * [definition_uri](definition_uri.md)  <sub>0..1</sub>
     * Description: The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [local_names](local_names.md)  <sub>0..\*</sub>
     * Range: [LocalName](LocalName.md)
 * [conforms_to](conforms_to.md)  <sub>0..1</sub>
     * Description: An established standard to which the element conforms.
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [implements](implements.md)  <sub>0..\*</sub>
     * Description: An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [instantiates](instantiates.md)  <sub>0..\*</sub>
     * Description: An element in another schema which this element instantiates.
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from extensible:

 * [extensions](extensions.md)  <sub>0..\*</sub>
     * Description: a tag/text tuple attached to an arbitrary element
     * Range: [Extension](Extension.md)

### Mixed in from annotatable:

 * [annotations](annotations.md)  <sub>0..\*</sub>
     * Description: a collection of tag/text tuples with the semantics of OWL Annotation
     * Range: [Annotation](Annotation.md)

### Mixed in from common_metadata:

 * [description](description.md)  <sub>0..1</sub>
     * Description: a textual description of the element's purpose and use
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

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
| **Aliases:** | | data element |
|  | | object |
| **In Subsets:** | | BasicSubset |
| **See also:** | | [https://en.wikipedia.org/wiki/Data_element](https://en.wikipedia.org/wiki/Data_element) |