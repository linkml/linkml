
# Class: schema_definition


A collection of definitions that make up a schema or a data model.

URI: [linkml:SchemaDefinition](https://w3id.org/linkml/SchemaDefinition)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeDefinition],[SubsetDefinition],[StructuredAlias],[SlotDefinition],[Setting],[Setting]<settings%200..*-++[SchemaDefinition&#124;id:uri;version:string%20%3F;imports:uriorcurie%20*;license:string%20%3F;emit_prefixes:ncname%20*;default_curi_maps:string%20*;default_prefix:string%20%3F;metamodel_version:string%20%3F;source_file:string%20%3F;source_file_date:datetime%20%3F;source_file_size:integer%20%3F;generation_date:datetime%20%3F;slot_names_unique:boolean%20%3F;name:ncname;id_prefixes(i):ncname%20*;id_prefixes_are_closed(i):boolean%20%3F;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;implements(i):uriorcurie%20*;instantiates(i):uriorcurie%20*;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;created_by(i):uriorcurie%20%3F;contributors(i):uriorcurie%20*;created_on(i):datetime%20%3F;last_updated_on(i):datetime%20%3F;modified_by(i):uriorcurie%20%3F;status(i):uriorcurie%20%3F;rank(i):integer%20%3F;categories(i):uriorcurie%20*;keywords(i):string%20*],[ClassDefinition]<classes%200..*-++[SchemaDefinition],[SlotDefinition]<slots%200..*-++[SchemaDefinition],[EnumDefinition]<enums%200..*-++[SchemaDefinition],[TypeDefinition]<types%200..*-++[SchemaDefinition],[SubsetDefinition]<subsets%200..*-++[SchemaDefinition],[TypeDefinition]<default_range%200..1-%20[SchemaDefinition],[Prefix]<prefixes%200..*-++[SchemaDefinition],[Element]^-[SchemaDefinition],[Prefix],[LocalName],[Extension],[Example],[EnumDefinition],[Element],[ClassDefinition],[Annotation],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeDefinition],[SubsetDefinition],[StructuredAlias],[SlotDefinition],[Setting],[Setting]<settings%200..*-++[SchemaDefinition&#124;id:uri;version:string%20%3F;imports:uriorcurie%20*;license:string%20%3F;emit_prefixes:ncname%20*;default_curi_maps:string%20*;default_prefix:string%20%3F;metamodel_version:string%20%3F;source_file:string%20%3F;source_file_date:datetime%20%3F;source_file_size:integer%20%3F;generation_date:datetime%20%3F;slot_names_unique:boolean%20%3F;name:ncname;id_prefixes(i):ncname%20*;id_prefixes_are_closed(i):boolean%20%3F;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;implements(i):uriorcurie%20*;instantiates(i):uriorcurie%20*;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;created_by(i):uriorcurie%20%3F;contributors(i):uriorcurie%20*;created_on(i):datetime%20%3F;last_updated_on(i):datetime%20%3F;modified_by(i):uriorcurie%20%3F;status(i):uriorcurie%20%3F;rank(i):integer%20%3F;categories(i):uriorcurie%20*;keywords(i):string%20*],[ClassDefinition]<classes%200..*-++[SchemaDefinition],[SlotDefinition]<slots%200..*-++[SchemaDefinition],[EnumDefinition]<enums%200..*-++[SchemaDefinition],[TypeDefinition]<types%200..*-++[SchemaDefinition],[SubsetDefinition]<subsets%200..*-++[SchemaDefinition],[TypeDefinition]<default_range%200..1-%20[SchemaDefinition],[Prefix]<prefixes%200..*-++[SchemaDefinition],[Element]^-[SchemaDefinition],[Prefix],[LocalName],[Extension],[Example],[EnumDefinition],[Element],[ClassDefinition],[Annotation],[AltDescription])

## Parents

 *  is_a: [Element](Element.md) - A named element in the model

## Referenced by Class


## Attributes


### Own

 * [id](id.md)  <sub>1..1</sub>
     * Description: The official schema URI
     * Range: [Uri](types/Uri.md)
     * in subsets: (SpecificationSubset,MinimalSubset,BasicSubset,OwlProfile)
 * [version](version.md)  <sub>0..1</sub>
     * Description: particular version of schema
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [imports](imports.md)  <sub>0..\*</sub>
     * Description: A list of schemas that are to be included in this schema
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset,BasicSubset,OwlProfile)
 * [license](license.md)  <sub>0..1</sub>
     * Description: license for the schema
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [prefixes](prefixes.md)  <sub>0..\*</sub>
     * Description: A collection of prefix expansions that specify how CURIEs can be expanded to URIs
     * Range: [Prefix](Prefix.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [emit_prefixes](emit_prefixes.md)  <sub>0..\*</sub>
     * Description: a list of Curie prefixes that are used in the representation of instances of the model.  All prefixes in this list are added to the prefix sections of the target models.
     * Range: [Ncname](types/Ncname.md)
 * [default_curi_maps](default_curi_maps.md)  <sub>0..\*</sub>
     * Description: ordered list of prefixcommon biocontexts to be fetched to resolve id prefixes and inline prefix variables
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [default_prefix](default_prefix.md)  <sub>0..1</sub>
     * Description: The prefix that is used for all elements within a schema
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset,MinimalSubset,BasicSubset)
 * [default_range](default_range.md)  <sub>0..1</sub>
     * Description: default slot range to be used if range element is omitted from a slot definition
     * Range: [TypeDefinition](TypeDefinition.md)
     * in subsets: (SpecificationSubset,MinimalSubset,BasicSubset)
 * [subsets](subsets.md)  <sub>0..\*</sub>
     * Description: An index to the collection of all subset definitions in the schema
     * Range: [SubsetDefinition](SubsetDefinition.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [types](types.md)  <sub>0..\*</sub>
     * Description: An index to the collection of all type definitions in the schema
     * Range: [TypeDefinition](TypeDefinition.md)
     * in subsets: (BasicSubset,ObjectOrientedProfile,OwlProfile)
 * [enums](enums.md)  <sub>0..\*</sub>
     * Description: An index to the collection of all enum definitions in the schema
     * Range: [EnumDefinition](EnumDefinition.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile,OwlProfile)
 * [schema_definition➞slots](slot_definitions.md)  <sub>0..\*</sub>
     * Description: An index to the collection of all slot definitions in the schema
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset,BasicSubset,OwlProfile)
 * [classes](classes.md)  <sub>0..\*</sub>
     * Description: An index to the collection of all class definitions in the schema
     * Range: [ClassDefinition](ClassDefinition.md)
     * in subsets: (SpecificationSubset,MinimalSubset,BasicSubset,RelationalModelProfile,ObjectOrientedProfile,OwlProfile)
 * [metamodel_version](metamodel_version.md)  <sub>0..1</sub>
     * Description: Version of the metamodel used to load the schema
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [source_file](source_file.md)  <sub>0..1</sub>
     * Description: name, uri or description of the source of the schema
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [source_file_date](source_file_date.md)  <sub>0..1</sub>
     * Description: modification date of the source of the schema
     * Range: [Datetime](types/Datetime.md)
     * in subsets: (BasicSubset)
 * [source_file_size](source_file_size.md)  <sub>0..1</sub>
     * Description: size in bytes of the source of the schema
     * Range: [Integer](types/Integer.md)
     * in subsets: (BasicSubset)
 * [generation_date](generation_date.md)  <sub>0..1</sub>
     * Description: date and time that the schema was loaded/generated
     * Range: [Datetime](types/Datetime.md)
     * in subsets: (BasicSubset)
 * [slot_names_unique](slot_names_unique.md)  <sub>0..1</sub>
     * Description: if true then induced/mangled slot names are not created for class_usage and attributes
     * Range: [Boolean](types/Boolean.md)
 * [settings](settings.md)  <sub>0..\*</sub>
     * Description: A collection of global variable settings
     * Range: [Setting](Setting.md)
     * in subsets: (SpecificationSubset)
 * [schema_definition➞name](schema_definition_name.md)  <sub>1..1</sub>
     * Description: a unique name for the schema that is both human-readable and consists of only characters from the NCName set
     * Range: [Ncname](types/Ncname.md)
     * in subsets: (SpecificationSubset,OwlProfile,MinimalSubset,BasicSubset,RelationalModelProfile,ObjectOrientedProfile)

### Inherited from element:

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

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | data dictionary |
|  | | data model |
|  | | information model |
|  | | logical model |
|  | | schema |
|  | | model |
| **In Subsets:** | | SpecificationSubset |
|  | | MinimalSubset |
|  | | BasicSubset |
|  | | RelationalModelProfile |
|  | | ObjectOrientedProfile |
|  | | OwlProfile |
| **See also:** | | [https://en.wikipedia.org/wiki/Data_dictionary](https://en.wikipedia.org/wiki/Data_dictionary) |
| **Close Mappings:** | | qb:ComponentSet |
|  | | owl:Ontology |

