
# Class: type_expression


An abstract class grouping named types and anonymous type expressions

URI: [linkml:TypeExpression](https://w3id.org/linkml/TypeExpression)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[AnonymousTypeExpression]<all_of%200..*-++[TypeExpression&#124;pattern:string%20%3F;implicit_prefix:string%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F],[AnonymousTypeExpression]<any_of%200..*-++[TypeExpression],[AnonymousTypeExpression]<exactly_one_of%200..*-++[TypeExpression],[AnonymousTypeExpression]<none_of%200..*-++[TypeExpression],[Anything]<maximum_value%200..1-++[TypeExpression],[Anything]<minimum_value%200..1-++[TypeExpression],[UnitOfMeasure]<unit%200..1-++[TypeExpression],[PatternExpression]<structured_pattern%200..1-++[TypeExpression],[TypeDefinition]uses%20-.->[TypeExpression],[AnonymousTypeExpression]uses%20-.->[TypeExpression],[Expression]^-[TypeExpression],[TypeDefinition],[PatternExpression],[Expression],[AnonymousTypeExpression],[UnitOfMeasure],[Anything])](https://yuml.me/diagram/nofunky;dir:TB/class/[AnonymousTypeExpression]<all_of%200..*-++[TypeExpression&#124;pattern:string%20%3F;implicit_prefix:string%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F],[AnonymousTypeExpression]<any_of%200..*-++[TypeExpression],[AnonymousTypeExpression]<exactly_one_of%200..*-++[TypeExpression],[AnonymousTypeExpression]<none_of%200..*-++[TypeExpression],[Anything]<maximum_value%200..1-++[TypeExpression],[Anything]<minimum_value%200..1-++[TypeExpression],[UnitOfMeasure]<unit%200..1-++[TypeExpression],[PatternExpression]<structured_pattern%200..1-++[TypeExpression],[TypeDefinition]uses%20-.->[TypeExpression],[AnonymousTypeExpression]uses%20-.->[TypeExpression],[Expression]^-[TypeExpression],[TypeDefinition],[PatternExpression],[Expression],[AnonymousTypeExpression],[UnitOfMeasure],[Anything])

## Parents

 *  is_a: [Expression](Expression.md) - general mixin for any class that can represent some form of expression

## Mixin for

 * [AnonymousTypeExpression](AnonymousTypeExpression.md) (mixin)  - A type expression that is not a top-level named type definition. Used for nesting.
 * [TypeDefinition](TypeDefinition.md) (mixin)  - an element that whose instances are atomic scalar values that can be mapped to primitive types

## Referenced by Class


## Attributes


### Own

 * [pattern](pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to this regular expression expressed in the string
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [structured_pattern](structured_pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to the regular expression in the pattern expression
     * Range: [PatternExpression](PatternExpression.md)
     * in subsets: (SpecificationSubset)
 * [unit](unit.md)  <sub>0..1</sub>
     * Description: an encoding of a unit
     * Range: [UnitOfMeasure](UnitOfMeasure.md)
 * [implicit_prefix](implicit_prefix.md)  <sub>0..1</sub>
     * Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)
 * [equals_string](equals_string.md)  <sub>0..1</sub>
     * Description: the slot must have range string and the value of the slot must equal the specified value
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)
 * [equals_string_in](equals_string_in.md)  <sub>0..\*</sub>
     * Description: the slot must have range string and the value of the slot must equal one of the specified values
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)
 * [equals_number](equals_number.md)  <sub>0..1</sub>
     * Description: the slot must have range of a number and the value of the slot must equal the specified value
     * Range: [Integer](types/Integer.md)
 * [minimum_value](minimum_value.md)  <sub>0..1</sub>
     * Description: For ordinal ranges, the value must be equal to or higher than this
     * Range: [Anything](Anything.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [maximum_value](maximum_value.md)  <sub>0..1</sub>
     * Description: For ordinal ranges, the value must be equal to or lower than this
     * Range: [Anything](Anything.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [type_expression➞none_of](type_expression_none_of.md)  <sub>0..\*</sub>
     * Description: holds if none of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)
     * in subsets: (SpecificationSubset)
 * [type_expression➞exactly_one_of](type_expression_exactly_one_of.md)  <sub>0..\*</sub>
     * Description: holds if only one of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)
     * in subsets: (SpecificationSubset)
 * [type_expression➞any_of](type_expression_any_of.md)  <sub>0..\*</sub>
     * Description: holds if at least one of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)
     * in subsets: (SpecificationSubset)
 * [type_expression➞all_of](type_expression_all_of.md)  <sub>0..\*</sub>
     * Description: holds if all of the expressions hold
     * Range: [AnonymousTypeExpression](AnonymousTypeExpression.md)
     * in subsets: (SpecificationSubset)
