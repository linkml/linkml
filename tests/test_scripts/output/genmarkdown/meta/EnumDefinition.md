
# Class: enum_definition


List of values that constrain the range of a slot

URI: [linkml:EnumDefinition](https://w3id.org/linkml/EnumDefinition)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[SchemaDefinition],[PermissibleValue],[LocalName],[Extension],[Example],[PermissibleValue]<permissible_values%200..*-++[EnumDefinition&#124;code_set:uriorcurie%20%3F;code_set_tag:string%20%3F;code_set_version:string%20%3F;pv_formula:pv_formula_options%20%3F;name(i):string;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;rank(i):integer%20%3F],[SchemaDefinition]++-%20enums%200..*>[EnumDefinition],[Element]^-[EnumDefinition],[Element],[Annotation],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[SchemaDefinition],[PermissibleValue],[LocalName],[Extension],[Example],[PermissibleValue]<permissible_values%200..*-++[EnumDefinition&#124;code_set:uriorcurie%20%3F;code_set_tag:string%20%3F;code_set_version:string%20%3F;pv_formula:pv_formula_options%20%3F;name(i):string;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;rank(i):integer%20%3F],[SchemaDefinition]++-%20enums%200..*>[EnumDefinition],[Element]^-[EnumDefinition],[Element],[Annotation],[AltDescription])

## Parents

 *  is_a: [Element](Element.md) - a named element in the model

## Referenced by Class

 *  **[SchemaDefinition](SchemaDefinition.md)** *[enums](enums.md)*  <sub>0..\*</sub>  **[EnumDefinition](EnumDefinition.md)**

## Attributes


### Own

 * [code_set](code_set.md)  <sub>0..1</sub>
     * Description: the identifier of an enumeration code set.
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (basic)
 * [code_set_tag](code_set_tag.md)  <sub>0..1</sub>
     * Description: the version tag of the enumeration code set
     * Range: [String](types/String.md)
     * in subsets: (basic)
 * [code_set_version](code_set_version.md)  <sub>0..1</sub>
     * Description: the version identifier of the enumeration code set
     * Range: [String](types/String.md)
     * in subsets: (basic)
 * [pv_formula](pv_formula.md)  <sub>0..1</sub>
     * Description: Defines the specific formula to be used to generate the permissible values.
     * Range: [pv_formula_options](pv_formula_options.md)
     * in subsets: (basic)
 * [permissible_values](permissible_values.md)  <sub>0..\*</sub>
     * Description: A list of possible values for a slot range
     * Range: [PermissibleValue](PermissibleValue.md)
     * in subsets: (basic)

### Inherited from element:

 * [name](name.md)  <sub>1..1</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * Range: [String](types/String.md)
     * in subsets: (owl,minimal,basic,relational_model,object_oriented)
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
| **In Subsets:** | | basic |
|  | | relational_model |
|  | | object_oriented |
| **Close Mappings:** | | qb:HierarchicalCodeList |

