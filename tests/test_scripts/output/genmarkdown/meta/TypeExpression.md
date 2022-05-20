
# Class: type_expression




URI: [linkml:TypeExpression](https://w3id.org/linkml/TypeExpression)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[AnonymousTypeExpression]<all_of%200..*-++[TypeExpression&#124;pattern:string%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F;minimum_value:integer%20%3F;maximum_value:integer%20%3F],[AnonymousTypeExpression]<any_of%200..*-++[TypeExpression],[AnonymousTypeExpression]<exactly_one_of%200..*-++[TypeExpression],[AnonymousTypeExpression]<none_of%200..*-++[TypeExpression],[PatternExpression]<structured_pattern%200..1-++[TypeExpression],[TypeDefinition]uses%20-.->[TypeExpression],[AnonymousTypeExpression]uses%20-.->[TypeExpression],[Expression]^-[TypeExpression],[TypeDefinition],[PatternExpression],[Expression],[AnonymousTypeExpression])](https://yuml.me/diagram/nofunky;dir:TB/class/[AnonymousTypeExpression]<all_of%200..*-++[TypeExpression&#124;pattern:string%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F;minimum_value:integer%20%3F;maximum_value:integer%20%3F],[AnonymousTypeExpression]<any_of%200..*-++[TypeExpression],[AnonymousTypeExpression]<exactly_one_of%200..*-++[TypeExpression],[AnonymousTypeExpression]<none_of%200..*-++[TypeExpression],[PatternExpression]<structured_pattern%200..1-++[TypeExpression],[TypeDefinition]uses%20-.->[TypeExpression],[AnonymousTypeExpression]uses%20-.->[TypeExpression],[Expression]^-[TypeExpression],[TypeDefinition],[PatternExpression],[Expression],[AnonymousTypeExpression])

## Parents

 *  is_a: [Expression](Expression.md) - general mixin for any class that can represent some form of expression

## Mixin for

 * [AnonymousTypeExpression](AnonymousTypeExpression.md) (mixin) 
 * [TypeDefinition](TypeDefinition.md) (mixin)  - A data type definition.

## Referenced by Class


## Attributes


### Own

 * [pattern](pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to this regular expression expressed in the string
     * Range: [String](types/String.md)
     * in subsets: (basic)
 * [structured_pattern](structured_pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to the regular expression in the pattern expression
     * Range: [PatternExpression](PatternExpression.md)
 * [equals_string](equals_string.md)  <sub>0..1</sub>
     * Description: the slot must have range string and the value of the slot must equal the specified value
     * Range: [String](types/String.md)
 * [equals_string_in](equals_string_in.md)  <sub>0..\*</sub>
     * Description: the slot must have range string and the value of the slot must equal one of the specified values
     * Range: [String](types/String.md)
 * [equals_number](equals_number.md)  <sub>0..1</sub>
     * Description: the slot must have range of a number and the value of the slot must equal the specified value
     * Range: [Integer](types/Integer.md)
 * [minimum_value](minimum_value.md)  <sub>0..1</sub>
     * Description: for slots with ranges of type number, the value must be equal to or higher than this
     * Range: [Integer](types/Integer.md)
     * in subsets: (basic)
 * [maximum_value](maximum_value.md)  <sub>0..1</sub>
     * Description: for slots with ranges of type number, the value must be equal to or lowe than this
     * Range: [Integer](types/Integer.md)
     * in subsets: (basic)
 * [type_expression➞none_of](type_expression_none_of.md)  <sub>0..\*</sub>
     * Description: holds if none of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)
 * [type_expression➞exactly_one_of](type_expression_exactly_one_of.md)  <sub>0..\*</sub>
     * Description: holds if only one of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)
 * [type_expression➞any_of](type_expression_any_of.md)  <sub>0..\*</sub>
     * Description: holds if at least one of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)
 * [type_expression➞all_of](type_expression_all_of.md)  <sub>0..\*</sub>
     * Description: holds if all of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)
