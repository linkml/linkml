
# Class: schema_definition


a collection of subset, type, slot and class definitions

URI: [linkml:SchemaDefinition](https://w3id.org/linkml/SchemaDefinition)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeDefinition],[SubsetDefinition],[StructuredAlias],[SlotDefinition],[Setting],[Setting]<settings%200..*-++[SchemaDefinition&#124;id:uri;version:string%20%3F;imports:uriorcurie%20*;license:string%20%3F;emit_prefixes:ncname%20*;default_curi_maps:string%20*;default_prefix:string%20%3F;metamodel_version:string%20%3F;source_file:string%20%3F;source_file_date:datetime%20%3F;source_file_size:integer%20%3F;generation_date:datetime%20%3F;slot_names_unique:boolean%20%3F;categories:uriorcurie%20*;keywords:string%20*;name:ncname;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;rank(i):integer%20%3F],[ClassDefinition]<classes%200..*-++[SchemaDefinition],[SlotDefinition]<slots%200..*-++[SchemaDefinition],[EnumDefinition]<enums%200..*-++[SchemaDefinition],[TypeDefinition]<types%200..*-++[SchemaDefinition],[SubsetDefinition]<subsets%200..*-++[SchemaDefinition],[TypeDefinition]<default_range%200..1-%20[SchemaDefinition],[Prefix]<prefixes%200..*-++[SchemaDefinition],[Element]^-[SchemaDefinition],[Prefix],[LocalName],[Extension],[Example],[EnumDefinition],[Element],[ClassDefinition],[Annotation],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeDefinition],[SubsetDefinition],[StructuredAlias],[SlotDefinition],[Setting],[Setting]<settings%200..*-++[SchemaDefinition&#124;id:uri;version:string%20%3F;imports:uriorcurie%20*;license:string%20%3F;emit_prefixes:ncname%20*;default_curi_maps:string%20*;default_prefix:string%20%3F;metamodel_version:string%20%3F;source_file:string%20%3F;source_file_date:datetime%20%3F;source_file_size:integer%20%3F;generation_date:datetime%20%3F;slot_names_unique:boolean%20%3F;categories:uriorcurie%20*;keywords:string%20*;name:ncname;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;rank(i):integer%20%3F],[ClassDefinition]<classes%200..*-++[SchemaDefinition],[SlotDefinition]<slots%200..*-++[SchemaDefinition],[EnumDefinition]<enums%200..*-++[SchemaDefinition],[TypeDefinition]<types%200..*-++[SchemaDefinition],[SubsetDefinition]<subsets%200..*-++[SchemaDefinition],[TypeDefinition]<default_range%200..1-%20[SchemaDefinition],[Prefix]<prefixes%200..*-++[SchemaDefinition],[Element]^-[SchemaDefinition],[Prefix],[LocalName],[Extension],[Example],[EnumDefinition],[Element],[ClassDefinition],[Annotation],[AltDescription])

## Parents

 *  is_a: [Element](Element.md) - a named element in the model

## Referenced by Class


## Attributes


### Own

 * [id](id.md)  <sub>1..1</sub>
     * Description: The official schema URI
     * Range: [Uri](types/Uri.md)
     * in subsets: (minimal,basic)
 * [version](version.md)  <sub>0..1</sub>
     * Description: particular version of schema
     * Range: [String](types/String.md)
     * in subsets: (owl,basic)
 * [imports](imports.md)  <sub>0..\*</sub>
     * Description: other schemas that are included in this schema
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (basic)
 * [license](license.md)  <sub>0..1</sub>
     * Description: license for the schema
     * Range: [String](types/String.md)
     * in subsets: (owl,basic)
 * [prefixes](prefixes.md)  <sub>0..\*</sub>
     * Description: prefix / URI definitions to be added to the context beyond those fetched from prefixcommons in id prefixes
     * Range: [Prefix](Prefix.md)
     * in subsets: (basic)
 * [emit_prefixes](emit_prefixes.md)  <sub>0..\*</sub>
     * Description: a list of Curie prefixes that are used in the representation of instances of the model.  All prefixes in this list are added to the prefix sections of the target models.
     * Range: [Ncname](types/Ncname.md)
 * [default_curi_maps](default_curi_maps.md)  <sub>0..\*</sub>
     * Description: ordered list of prefixcommon biocontexts to be fetched to resolve id prefixes and inline prefix variables
     * Range: [String](types/String.md)
     * in subsets: (basic)
 * [default_prefix](default_prefix.md)  <sub>0..1</sub>
     * Description: default and base prefix -- used for ':' identifiers, @base and @vocab
     * Range: [String](types/String.md)
     * in subsets: (minimal,basic)
 * [default_range](default_range.md)  <sub>0..1</sub>
     * Description: default slot range to be used if range element is omitted from a slot definition
     * Range: [TypeDefinition](TypeDefinition.md)
     * in subsets: (minimal,basic)
 * [subsets](subsets.md)  <sub>0..\*</sub>
     * Description: list of subsets referenced in this model
     * Range: [SubsetDefinition](SubsetDefinition.md)
     * in subsets: (basic)
 * [types](types.md)  <sub>0..\*</sub>
     * Description: data types used in the model
     * Range: [TypeDefinition](TypeDefinition.md)
     * in subsets: (basic,object_oriented)
 * [enums](enums.md)  <sub>0..\*</sub>
     * Description: enumerated ranges
     * Range: [EnumDefinition](EnumDefinition.md)
     * in subsets: (basic,object_oriented)
 * [schema_definition➞slots](slot_definitions.md)  <sub>0..\*</sub>
     * Description: slot definitions
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (basic)
 * [classes](classes.md)  <sub>0..\*</sub>
     * Description: class definitions
     * Range: [ClassDefinition](ClassDefinition.md)
     * in subsets: (minimal,basic,relational_model,object_oriented)
 * [metamodel_version](metamodel_version.md)  <sub>0..1</sub>
     * Description: Version of the metamodel used to load the schema
     * Range: [String](types/String.md)
     * in subsets: (owl,basic)
 * [source_file](source_file.md)  <sub>0..1</sub>
     * Description: name, uri or description of the source of the schema
     * Range: [String](types/String.md)
     * in subsets: (owl,basic)
 * [source_file_date](source_file_date.md)  <sub>0..1</sub>
     * Description: modification date of the source of the schema
     * Range: [Datetime](types/Datetime.md)
     * in subsets: (owl,basic)
 * [source_file_size](source_file_size.md)  <sub>0..1</sub>
     * Description: size in bytes of the source of the schema
     * Range: [Integer](types/Integer.md)
     * in subsets: (owl,basic)
 * [generation_date](generation_date.md)  <sub>0..1</sub>
     * Description: date and time that the schema was loaded/generated
     * Range: [Datetime](types/Datetime.md)
     * in subsets: (owl,basic)
 * [slot_names_unique](slot_names_unique.md)  <sub>0..1</sub>
     * Description: if true then induced/mangled slot names are not created for class_usage and attributes
     * Range: [Boolean](types/Boolean.md)
 * [settings](settings.md)  <sub>0..\*</sub>
     * Description: A collection of global variable settings
     * Range: [Setting](Setting.md)
 * [categories](categories.md)  <sub>0..\*</sub>
     * Description: controlled terms used to categorize an element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (basic)
 * [keywords](keywords.md)  <sub>0..\*</sub>
     * Description: Keywords or tags used to describe the element
     * Range: [String](types/String.md)
     * in subsets: (basic)
 * [schema_definition➞name](schema_definition_name.md)  <sub>1..1</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * Range: [Ncname](types/Ncname.md)
     * in subsets: (owl,minimal,basic,relational_model,object_oriented)

### Inherited from element:

 * [id_prefixes](id_prefixes.md)  <sub>0..\*</sub>
     * Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
     * Range: [Ncname](types/Ncname.md)
     * in subsets: (basic)
 * [definition_uri](definition_uri.md)  <sub>0..1</sub>
     * Description: the "native" URI of the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [local_names](local_names.md)  <sub>0..\*</sub>
     * Range: [LocalName](LocalName.md)
 * [conforms_to](conforms_to.md)  <sub>0..1</sub>
     * Description: An established standard to which the element conforms.
     * Range: [String](types/String.md)
     * in subsets: (owl,basic)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | data dictionary |
| **In Subsets:** | | minimal |
|  | | basic |
|  | | relational_model |
|  | | object_oriented |
| **See also:** | | [https://en.wikipedia.org/wiki/Data_dictionary](https://en.wikipedia.org/wiki/Data_dictionary) |

