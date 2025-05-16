
# Class: type_definition

an element that whose instances are atomic scalar values that can be mapped to primitive types

URI: [linkml:TypeDefinition](https://w3id.org/linkml/TypeDefinition)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeExpression],[TypeDefinition]<union_of%200..*-%20[TypeDefinition&#124;base:string%20%3F;uri:uriorcurie%20%3F;repr:string%20%3F;pattern:string%20%3F;implicit_prefix:string%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F;name(i):string;id_prefixes(i):ncname%20*;id_prefixes_are_closed(i):boolean%20%3F;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;implements(i):uriorcurie%20*;instantiates(i):uriorcurie%20*;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;created_by(i):uriorcurie%20%3F;contributors(i):uriorcurie%20*;created_on(i):datetime%20%3F;last_updated_on(i):datetime%20%3F;modified_by(i):uriorcurie%20%3F;status(i):uriorcurie%20%3F;rank(i):integer%20%3F;categories(i):uriorcurie%20*;keywords(i):string%20*],[TypeDefinition]<typeof%200..1-%20[TypeDefinition],[SchemaDefinition]-%20default_range%200..1>[TypeDefinition],[TypeMapping]-%20type%200..1>[TypeDefinition],[SchemaDefinition]++-%20types%200..*>[TypeDefinition],[TypeDefinition]uses%20-.->[TypeExpression],[Element]^-[TypeDefinition],[TypeMapping],[SubsetDefinition],[StructuredAlias],[SchemaDefinition],[PatternExpression],[LocalName],[Extension],[Example],[Element],[AnonymousTypeExpression],[Annotation],[AltDescription],[UnitOfMeasure],[Anything])](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeExpression],[TypeDefinition]<union_of%200..*-%20[TypeDefinition&#124;base:string%20%3F;uri:uriorcurie%20%3F;repr:string%20%3F;pattern:string%20%3F;implicit_prefix:string%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F;name(i):string;id_prefixes(i):ncname%20*;id_prefixes_are_closed(i):boolean%20%3F;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;implements(i):uriorcurie%20*;instantiates(i):uriorcurie%20*;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;created_by(i):uriorcurie%20%3F;contributors(i):uriorcurie%20*;created_on(i):datetime%20%3F;last_updated_on(i):datetime%20%3F;modified_by(i):uriorcurie%20%3F;status(i):uriorcurie%20%3F;rank(i):integer%20%3F;categories(i):uriorcurie%20*;keywords(i):string%20*],[TypeDefinition]<typeof%200..1-%20[TypeDefinition],[SchemaDefinition]-%20default_range%200..1>[TypeDefinition],[TypeMapping]-%20type%200..1>[TypeDefinition],[SchemaDefinition]++-%20types%200..*>[TypeDefinition],[TypeDefinition]uses%20-.->[TypeExpression],[Element]^-[TypeDefinition],[TypeMapping],[SubsetDefinition],[StructuredAlias],[SchemaDefinition],[PatternExpression],[LocalName],[Extension],[Example],[Element],[AnonymousTypeExpression],[Annotation],[AltDescription],[UnitOfMeasure],[Anything])

## Parents

 *  is_a: [Element](Element.md) - A named element in the model

## Uses Mixin

 *  mixin: [TypeExpression](TypeExpression.md) - An abstract class grouping named types and anonymous type expressions

## Referenced by Class

 *  **[SchemaDefinition](SchemaDefinition.md)** *[default_range](default_range.md)*  <sub>0..1</sub>  **[TypeDefinition](TypeDefinition.md)**
 *  **None** *[➞type](mapped_type.md)*  <sub>0..1</sub>  **[TypeDefinition](TypeDefinition.md)**
 *  **[TypeDefinition](TypeDefinition.md)** *[type_definition➞union_of](type_definition_union_of.md)*  <sub>0..\*</sub>  **[TypeDefinition](TypeDefinition.md)**
 *  **[TypeDefinition](TypeDefinition.md)** *[typeof](typeof.md)*  <sub>0..1</sub>  **[TypeDefinition](TypeDefinition.md)**
 *  **[SchemaDefinition](SchemaDefinition.md)** *[types](types.md)*  <sub>0..\*</sub>  **[TypeDefinition](TypeDefinition.md)**

## Attributes


### Own

 * [typeof](typeof.md)  <sub>0..1</sub>
     * Description: A parent type from which type properties are inherited
     * Range: [TypeDefinition](TypeDefinition.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [base](base.md)  <sub>0..1</sub>
     * Description: python base type in the LinkML runtime that implements this type definition
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [type_definition➞uri](type_uri.md)  <sub>0..1</sub>
     * Description: The uri that defines the possible values for the type definition
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [repr](repr.md)  <sub>0..1</sub>
     * Description: the name of the python object that implements this type definition
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [type_definition➞union_of](type_definition_union_of.md)  <sub>0..\*</sub>
     * Description: indicates that the domain element consists exactly of the members of the element in the range.
     * Range: [TypeDefinition](TypeDefinition.md)
     * in subsets: (SpecificationSubset,OwlProfile)

### Inherited from element:

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

### Mixed in from type_expression:

 * [pattern](pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to this regular expression expressed in the string
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from type_expression:

 * [structured_pattern](structured_pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to the regular expression in the pattern expression
     * Range: [PatternExpression](PatternExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from type_expression:

 * [unit](unit.md)  <sub>0..1</sub>
     * Description: an encoding of a unit
     * Range: [UnitOfMeasure](UnitOfMeasure.md)

### Mixed in from type_expression:

 * [implicit_prefix](implicit_prefix.md)  <sub>0..1</sub>
     * Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)

### Mixed in from type_expression:

 * [equals_string](equals_string.md)  <sub>0..1</sub>
     * Description: the slot must have range string and the value of the slot must equal the specified value
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)

### Mixed in from type_expression:

 * [equals_string_in](equals_string_in.md)  <sub>0..\*</sub>
     * Description: the slot must have range string and the value of the slot must equal one of the specified values
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)

### Mixed in from type_expression:

 * [equals_number](equals_number.md)  <sub>0..1</sub>
     * Description: the slot must have range of a number and the value of the slot must equal the specified value
     * Range: [Integer](types/Integer.md)

### Mixed in from type_expression:

 * [minimum_value](minimum_value.md)  <sub>0..1</sub>
     * Description: For ordinal ranges, the value must be equal to or higher than this
     * Range: [Anything](Anything.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from type_expression:

 * [maximum_value](maximum_value.md)  <sub>0..1</sub>
     * Description: For ordinal ranges, the value must be equal to or lower than this
     * Range: [Anything](Anything.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from type_expression:

 * [type_expression➞none_of](type_expression_none_of.md)  <sub>0..\*</sub>
     * Description: holds if none of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from type_expression:

 * [type_expression➞exactly_one_of](type_expression_exactly_one_of.md)  <sub>0..\*</sub>
     * Description: holds if only one of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from type_expression:

 * [type_expression➞any_of](type_expression_any_of.md)  <sub>0..\*</sub>
     * Description: holds if at least one of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from type_expression:

 * [type_expression➞all_of](type_expression_all_of.md)  <sub>0..\*</sub>
     * Description: holds if all of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)
     * in subsets: (SpecificationSubset)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | SpecificationSubset |
|  | | BasicSubset |
|  | | OwlProfile |