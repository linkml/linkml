
# Class: SchemaDefinition


a collection of subset, type, slot and class definitions

URI: [linkml:SchemaDefinition](https://w3id.org/linkml/SchemaDefinition)


[![img](images/SchemaDefinition.svg)](images/SchemaDefinition.svg)

## Parents

 *  is_a: [Element](Element.md) - a named element in the model

## Referenced by class


## Attributes


### Own

 * [id](id.md)  <sub>1..1</sub>
     * Description: The official schema URI
     * Range: [Uri](types/Uri.md)
 * [title](title.md)  <sub>0..1</sub>
     * Description: the official title of the schema
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [version](version.md)  <sub>0..1</sub>
     * Description: particular version of schema
     * Range: [String](types/String.md)
 * [imports](imports.md)  <sub>0..\*</sub>
     * Description: other schemas that are included in this schema
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [license](license.md)  <sub>0..1</sub>
     * Description: license for the schema
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [prefixes](prefixes.md)  <sub>0..\*</sub>
     * Description: prefix / URI definitions to be added to the context beyond those fetched from prefixcommons in id prefixes
     * Range: [Prefix](Prefix.md)
 * [emit_prefixes](emit_prefixes.md)  <sub>0..\*</sub>
     * Description: a list of Curie prefixes that are used in the representation of instances of the model.  All prefixes in this list are added to the prefix sections of the target models.
     * Range: [Ncname](types/Ncname.md)
 * [default_curi_maps](default_curi_maps.md)  <sub>0..\*</sub>
     * Description: ordered list of prefixcommon biocontexts to be fetched to resolve id prefixes and inline prefix variables
     * Range: [String](types/String.md)
 * [default_prefix](default_prefix.md)  <sub>0..1</sub>
     * Description: default and base prefix -- used for ':' identifiers, @base and @vocab
     * Range: [String](types/String.md)
 * [default_range](default_range.md)  <sub>0..1</sub>
     * Description: default slot range to be used if range element is omitted from a slot definition
     * Range: [TypeDefinition](TypeDefinition.md)
 * [subsets](subsets.md)  <sub>0..\*</sub>
     * Description: list of subsets referenced in this model
     * Range: [SubsetDefinition](SubsetDefinition.md)
 * [types](types.md)  <sub>0..\*</sub>
     * Description: data types used in the model
     * Range: [TypeDefinition](TypeDefinition.md)
 * [enums](enums.md)  <sub>0..\*</sub>
     * Description: enumerated ranges
     * Range: [EnumDefinition](EnumDefinition.md)
 * [schema_definition➞slots](slot_definitions.md)  <sub>0..\*</sub>
     * Description: slot definitions
     * Range: [SlotDefinition](SlotDefinition.md)
 * [classes](classes.md)  <sub>0..\*</sub>
     * Description: class definitions
     * Range: [ClassDefinition](ClassDefinition.md)
 * [metamodel_version](metamodel_version.md)  <sub>0..1</sub>
     * Description: Version of the metamodel used to load the schema
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [source_file](source_file.md)  <sub>0..1</sub>
     * Description: name, uri or description of the source of the schema
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [source_file_date](source_file_date.md)  <sub>0..1</sub>
     * Description: modification date of the source of the schema
     * Range: [Datetime](types/Datetime.md)
     * in subsets: (owl)
 * [source_file_size](source_file_size.md)  <sub>0..1</sub>
     * Description: size in bytes of the source of the schema
     * Range: [Integer](types/Integer.md)
     * in subsets: (owl)
 * [generation_date](generation_date.md)  <sub>0..1</sub>
     * Description: date and time that the schema was loaded/generated
     * Range: [Datetime](types/Datetime.md)
     * in subsets: (owl)
 * [schema_definition➞name](schema_definition_name.md)  <sub>1..1</sub>
     * Range: [Ncname](types/Ncname.md)

### Inherited from element:

 * [id_prefixes](id_prefixes.md)  <sub>0..\*</sub>
     * Description: the identifier of this class or slot must begin with one of the URIs referenced by this prefix
     * Range: [Ncname](types/Ncname.md)
 * [definition_uri](definition_uri.md)  <sub>0..1</sub>
     * Description: the "native" URI of the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [aliases](aliases.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)
 * [local_names](local_names.md)  <sub>0..\*</sub>
     * Range: [LocalName](LocalName.md)
 * [mappings](mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: a description of the element's purpose and use
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [alt_descriptions](alt_descriptions.md)  <sub>0..\*</sub>
     * Range: [AltDescription](AltDescription.md)
 * [deprecated](deprecated.md)  <sub>0..1</sub>
     * Description: Description of why and when this element will no longer be used
     * Range: [String](types/String.md)
 * [todos](todos.md)  <sub>0..\*</sub>
     * Description: Outstanding issue that needs resolution
     * Range: [String](types/String.md)
 * [notes](notes.md)  <sub>0..\*</sub>
     * Description: editorial notes about an element intended for internal consumption
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [comments](comments.md)  <sub>0..\*</sub>
     * Description: notes and comments about an element intended for external consumption
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [examples](examples.md)  <sub>0..\*</sub>
     * Description: example usages of an element
     * Range: [Example](Example.md)
     * in subsets: (owl)
 * [in_subset](in_subset.md)  <sub>0..\*</sub>
     * Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
     * Range: [SubsetDefinition](SubsetDefinition.md)
 * [from_schema](from_schema.md)  <sub>0..1</sub>
     * Description: id of the schema that defined the element
     * Range: [Uri](types/Uri.md)
 * [imported_from](imported_from.md)  <sub>0..1</sub>
     * Description: the imports entry that this element was derived from.  Empty means primary source
     * Range: [String](types/String.md)
 * [see_also](see_also.md)  <sub>0..\*</sub>
     * Description: a reference
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (owl)
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
 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | data dictionary |
| **See also:** | | https://en.wikipedia.org/wiki/Data_dictionary |

