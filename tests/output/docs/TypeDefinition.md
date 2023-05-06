
# Class: type_definition


A data type definition.

URI: [linkml:TypeDefinition](https://w3id.org/linkml/TypeDefinition)


[![img](images/TypeDefinition.svg)](images/TypeDefinition.svg)

## Parents

 *  is_a: [Element](Element.md) - a named element in the model

## Uses Mixin

 *  mixin: [TypeExpression](TypeExpression.md)

## Referenced by Class

 *  **[SchemaDefinition](SchemaDefinition.md)** *[default_range](default_range.md)*  <sub>0..1</sub>  **[TypeDefinition](TypeDefinition.md)**
 *  **[TypeDefinition](TypeDefinition.md)** *[typeof](typeof.md)*  <sub>0..1</sub>  **[TypeDefinition](TypeDefinition.md)**
 *  **[SchemaDefinition](SchemaDefinition.md)** *[types](types.md)*  <sub>0..\*</sub>  **[TypeDefinition](TypeDefinition.md)**

## Attributes


### Own

 * [typeof](typeof.md)  <sub>0..1</sub>
     * Description: Names a parent type
     * Range: [TypeDefinition](TypeDefinition.md)
     * in subsets: (basic)
 * [base](base.md)  <sub>0..1</sub>
     * Description: python base type that implements this type definition
     * Range: [String](types/String.md)
     * in subsets: (basic)
 * [type_definition➞uri](type_uri.md)  <sub>0..1</sub>
     * Description: The uri that defines the possible values for the type definition
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (basic)
 * [repr](repr.md)  <sub>0..1</sub>
     * Description: the name of the python object that implements this type definition
     * Range: [String](types/String.md)
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

### Mixed in from type_expression:

 * [pattern](pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to this regular expression expressed in the string
     * Range: [String](types/String.md)
     * in subsets: (basic)

### Mixed in from type_expression:

 * [structured_pattern](structured_pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to the regular expression in the pattern expression
     * Range: [PatternExpression](PatternExpression.md)

### Mixed in from type_expression:

 * [equals_string](equals_string.md)  <sub>0..1</sub>
     * Description: the slot must have range string and the value of the slot must equal the specified value
     * Range: [String](types/String.md)

### Mixed in from type_expression:

 * [equals_string_in](equals_string_in.md)  <sub>0..\*</sub>
     * Description: the slot must have range string and the value of the slot must equal one of the specified values
     * Range: [String](types/String.md)

### Mixed in from type_expression:

 * [equals_number](equals_number.md)  <sub>0..1</sub>
     * Description: the slot must have range of a number and the value of the slot must equal the specified value
     * Range: [Integer](types/Integer.md)

### Mixed in from type_expression:

 * [minimum_value](minimum_value.md)  <sub>0..1</sub>
     * Description: for slots with ranges of type number, the value must be equal to or higher than this
     * Range: [Integer](types/Integer.md)
     * in subsets: (basic)

### Mixed in from type_expression:

 * [maximum_value](maximum_value.md)  <sub>0..1</sub>
     * Description: for slots with ranges of type number, the value must be equal to or lowe than this
     * Range: [Integer](types/Integer.md)
     * in subsets: (basic)

### Mixed in from type_expression:

 * [type_expression➞none_of](type_expression_none_of.md)  <sub>0..\*</sub>
     * Description: holds if none of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)

### Mixed in from type_expression:

 * [type_expression➞exactly_one_of](type_expression_exactly_one_of.md)  <sub>0..\*</sub>
     * Description: holds if only one of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)

### Mixed in from type_expression:

 * [type_expression➞any_of](type_expression_any_of.md)  <sub>0..\*</sub>
     * Description: holds if at least one of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)

### Mixed in from type_expression:

 * [type_expression➞all_of](type_expression_all_of.md)  <sub>0..\*</sub>
     * Description: holds if all of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | basic |
