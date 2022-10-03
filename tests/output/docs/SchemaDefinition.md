
# Class: schema_definition


a collection of subset, type, slot and class definitions

URI: [linkml:SchemaDefinition](https://w3id.org/linkml/SchemaDefinition)


[![img](images/SchemaDefinition.svg)](images/SchemaDefinition.svg)

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

