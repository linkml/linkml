
# Class: type_definition


A data type definition.

URI: [linkml:TypeDefinition](https://w3id.org/linkml/TypeDefinition)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeDefinition]<typeof%200..1-%20[TypeDefinition&#124;base:string%20%3F;uri:uriorcurie%20%3F;repr:string%20%3F;pattern:string%20%3F;name(i):string;title(i):string%20%3F;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;description(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F],[SchemaDefinition]-%20default_range%200..1>[TypeDefinition],[SchemaDefinition]++-%20types%200..*>[TypeDefinition],[Element]^-[TypeDefinition],[SubsetDefinition],[SchemaDefinition],[LocalName],[Extension],[Example],[Element],[Annotation],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeDefinition]<typeof%200..1-%20[TypeDefinition&#124;base:string%20%3F;uri:uriorcurie%20%3F;repr:string%20%3F;pattern:string%20%3F;name(i):string;title(i):string%20%3F;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;description(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F],[SchemaDefinition]-%20default_range%200..1>[TypeDefinition],[SchemaDefinition]++-%20types%200..*>[TypeDefinition],[Element]^-[TypeDefinition],[SubsetDefinition],[SchemaDefinition],[LocalName],[Extension],[Example],[Element],[Annotation],[AltDescription])

## Parents

 *  is_a: [Element](Element.md) - a named element in the model

## Referenced by Class

 *  **[SchemaDefinition](SchemaDefinition.md)** *[default_range](default_range.md)*  <sub>0..1</sub>  **[TypeDefinition](TypeDefinition.md)**
 *  **[TypeDefinition](TypeDefinition.md)** *[typeof](typeof.md)*  <sub>0..1</sub>  **[TypeDefinition](TypeDefinition.md)**
 *  **[SchemaDefinition](SchemaDefinition.md)** *[types](types.md)*  <sub>0..\*</sub>  **[TypeDefinition](TypeDefinition.md)**

## Attributes


### Own

 * [typeof](typeof.md)  <sub>0..1</sub>
     * Description: Names a parent type
     * Range: [TypeDefinition](TypeDefinition.md)
 * [base](base.md)  <sub>0..1</sub>
     * Description: python base type that implements this type definition
     * Range: [String](String.md)
 * [type_definition➞uri](type_uri.md)  <sub>0..1</sub>
     * Description: The uri that defines the possible values for the type definition
     * Range: [Uriorcurie](Uriorcurie.md)
 * [repr](repr.md)  <sub>0..1</sub>
     * Description: the name of the python object that implements this type definition
     * Range: [String](String.md)
 * [pattern](pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to this regular expression
     * Range: [String](String.md)

### Inherited from element:

 * [name](name.md)  <sub>1..1</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * Range: [String](String.md)
     * in subsets: (owl)
 * [title](title.md)  <sub>0..1</sub>
     * Description: the official title of the element
     * Range: [String](String.md)
     * in subsets: (owl)
 * [id_prefixes](id_prefixes.md)  <sub>0..\*</sub>
     * Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
     * Range: [Ncname](Ncname.md)
 * [definition_uri](definition_uri.md)  <sub>0..1</sub>
     * Description: the "native" URI of the element
     * Range: [Uriorcurie](Uriorcurie.md)
 * [aliases](aliases.md)  <sub>0..\*</sub>
     * Range: [String](String.md)
 * [local_names](local_names.md)  <sub>0..\*</sub>
     * Range: [LocalName](LocalName.md)
 * [mappings](mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * Range: [Uriorcurie](Uriorcurie.md)
 * [exact mappings](exact_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have identical meaning.
     * Range: [Uriorcurie](Uriorcurie.md)
 * [close mappings](close_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have close meaning.
     * Range: [Uriorcurie](Uriorcurie.md)
 * [related mappings](related_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have related meaning.
     * Range: [Uriorcurie](Uriorcurie.md)
 * [narrow mappings](narrow_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have narrower meaning.
     * Range: [Uriorcurie](Uriorcurie.md)
 * [broad mappings](broad_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have broader meaning.
     * Range: [Uriorcurie](Uriorcurie.md)
