
# Class: anonymous_type_expression


A type expression that is not a top-level named type definition. Used for nesting.

URI: [linkml:AnonymousTypeExpression](https://w3id.org/linkml/AnonymousTypeExpression)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeExpression],[PatternExpression],[TypeExpression]++-%20all_of%200..*>[AnonymousTypeExpression&#124;pattern:string%20%3F;implicit_prefix:string%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F],[TypeExpression]++-%20any_of%200..*>[AnonymousTypeExpression],[TypeExpression]++-%20exactly_one_of%200..*>[AnonymousTypeExpression],[TypeExpression]++-%20none_of%200..*>[AnonymousTypeExpression],[AnonymousTypeExpression]uses%20-.->[TypeExpression],[UnitOfMeasure],[Anything])](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeExpression],[PatternExpression],[TypeExpression]++-%20all_of%200..*>[AnonymousTypeExpression&#124;pattern:string%20%3F;implicit_prefix:string%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F],[TypeExpression]++-%20any_of%200..*>[AnonymousTypeExpression],[TypeExpression]++-%20exactly_one_of%200..*>[AnonymousTypeExpression],[TypeExpression]++-%20none_of%200..*>[AnonymousTypeExpression],[AnonymousTypeExpression]uses%20-.->[TypeExpression],[UnitOfMeasure],[Anything])

## Uses Mixin

 *  mixin: [TypeExpression](TypeExpression.md) - An abstract class grouping named types and anonymous type expressions

## Referenced by Class

 *  **[TypeExpression](TypeExpression.md)** *[type_expression➞all_of](type_expression_all_of.md)*  <sub>0..\*</sub>  **[AnonymousTypeExpression](AnonymousTypeExpression.md)**
 *  **[TypeExpression](TypeExpression.md)** *[type_expression➞any_of](type_expression_any_of.md)*  <sub>0..\*</sub>  **[AnonymousTypeExpression](AnonymousTypeExpression.md)**
 *  **[TypeExpression](TypeExpression.md)** *[type_expression➞exactly_one_of](type_expression_exactly_one_of.md)*  <sub>0..\*</sub>  **[AnonymousTypeExpression](AnonymousTypeExpression.md)**
 *  **[TypeExpression](TypeExpression.md)** *[type_expression➞none_of](type_expression_none_of.md)*  <sub>0..\*</sub>  **[AnonymousTypeExpression](AnonymousTypeExpression.md)**

## Attributes


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
