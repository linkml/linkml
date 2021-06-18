
# Class: EnumDefinition


List of values that constrain the range of a slot

URI: [linkml:EnumDefinition](https://w3id.org/linkml/EnumDefinition)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[SchemaDefinition],[PermissibleValue],[LocalName],[Extension],[Example],[PermissibleValue]<permissible_values%200..*-++[EnumDefinition&#124;code_set:uriorcurie%20%3F;code_set_tag:string%20%3F;code_set_version:string%20%3F;pv_formula:pv_formula_options%20%3F;name(i):string;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;description(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;see_also(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F],[SchemaDefinition]++-%20enums%200..*>[EnumDefinition],[Element]^-[EnumDefinition],[Element],[Annotation],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[SchemaDefinition],[PermissibleValue],[LocalName],[Extension],[Example],[PermissibleValue]<permissible_values%200..*-++[EnumDefinition&#124;code_set:uriorcurie%20%3F;code_set_tag:string%20%3F;code_set_version:string%20%3F;pv_formula:pv_formula_options%20%3F;name(i):string;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;description(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;see_also(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F],[SchemaDefinition]++-%20enums%200..*>[EnumDefinition],[Element]^-[EnumDefinition],[Element],[Annotation],[AltDescription])

## Parents

 *  is_a: [Element](Element.md) - a named element in the model

## Referenced by class

 *  **[SchemaDefinition](SchemaDefinition.md)** *[enums](enums.md)*  <sub>0..\*</sub>  **[EnumDefinition](EnumDefinition.md)**

## Attributes


### Own

 * [code_set](code_set.md)  <sub>OPT</sub>
     * Description: the identifier of an enumeration code set.
     * Range: [Uriorcurie](Uriorcurie.md)
 * [code_set_tag](code_set_tag.md)  <sub>OPT</sub>
     * Description: the version tag of the enumeration code set
     * Range: [String](String.md)
 * [code_set_version](code_set_version.md)  <sub>OPT</sub>
     * Description: the version identifier of the enumeration code set
     * Range: [String](String.md)
 * [pv_formula](pv_formula.md)  <sub>OPT</sub>
     * Description: Defines the specific formula to be used to generate the permissible values.
     * Range: [pv_formula_options](pv_formula_options.md)
 * [permissible_values](permissible_values.md)  <sub>0..\*</sub>
     * Description: A list of possible values for a slot range
     * Range: [PermissibleValue](PermissibleValue.md)

### Inherited from element:

 * [name](name.md)  <sub>REQ</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * Range: [String](String.md)
     * in subsets: (owl)
 * [id_prefixes](id_prefixes.md)  <sub>0..\*</sub>
     * Description: the identifier of this class or slot must begin with one of the URIs referenced by this prefix
     * Range: [Ncname](Ncname.md)
 * [definition_uri](definition_uri.md)  <sub>OPT</sub>
     * Description: the "native" URI of the element
     * Range: [Uriorcurie](Uriorcurie.md)
 * [aliases](aliases.md)  <sub>0..\*</sub>
     * Range: [String](String.md)
 * [local_names](local_names.md)  <sub>0..\*</sub>
     * Range: [LocalName](LocalName.md)
 * [mappings](mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * Range: [Uriorcurie](Uriorcurie.md)
 * [description](description.md)  <sub>OPT</sub>
     * Description: a description of the element's purpose and use
     * Range: [String](String.md)
     * in subsets: (owl)
 * [alt_descriptions](alt_descriptions.md)  <sub>0..\*</sub>
     * Range: [AltDescription](AltDescription.md)
 * [deprecated](deprecated.md)  <sub>OPT</sub>
     * Description: Description of why and when this element will no longer be used
     * Range: [String](String.md)
 * [todos](todos.md)  <sub>0..\*</sub>
     * Description: Outstanding issue that needs resolution
     * Range: [String](String.md)
 * [notes](notes.md)  <sub>0..\*</sub>
     * Description: editorial notes about an element intended for internal consumption
     * Range: [String](String.md)
     * in subsets: (owl)
 * [comments](comments.md)  <sub>0..\*</sub>
     * Description: notes and comments about an element intended for external consumption
     * Range: [String](String.md)
     * in subsets: (owl)
 * [examples](examples.md)  <sub>0..\*</sub>
     * Description: example usages of an element
     * Range: [Example](Example.md)
     * in subsets: (owl)
 * [in_subset](in_subset.md)  <sub>0..\*</sub>
     * Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
     * Range: [SubsetDefinition](SubsetDefinition.md)
 * [from_schema](from_schema.md)  <sub>OPT</sub>
     * Description: id of the schema that defined the element
     * Range: [Uri](Uri.md)
 * [imported_from](imported_from.md)  <sub>OPT</sub>
     * Description: the imports entry that this element was derived from.  Empty means primary source
     * Range: [String](String.md)
 * [see_also](see_also.md)  <sub>0..\*</sub>
     * Description: a reference
     * Range: [Uriorcurie](Uriorcurie.md)
     * in subsets: (owl)
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
 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>OPT</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * Range: [Uriorcurie](Uriorcurie.md)
 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>OPT</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * Range: [Uriorcurie](Uriorcurie.md)
