
# Class: slot_expression


an expression that constrains the range of values a slot can take

URI: [linkml:SlotExpression](https://w3id.org/linkml/SlotExpression)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[AnonymousSlotExpression]<all_of%200..*-++[SlotExpression&#124;required:boolean%20%3F;recommended:boolean%20%3F;minimum_value:integer%20%3F;maximum_value:integer%20%3F;pattern:string%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F;equals_expression:string%20%3F;minimum_cardinality:integer%20%3F;maximum_cardinality:integer%20%3F],[AnonymousSlotExpression]<any_of%200..*-++[SlotExpression],[AnonymousSlotExpression]<exactly_one_of%200..*-++[SlotExpression],[AnonymousSlotExpression]<none_of%200..*-++[SlotExpression],[SlotDefinition]<all_members%200..*-++[SlotExpression],[AnonymousSlotExpression]<has_member%200..1-++[SlotExpression],[AnonymousClassExpression]<range_expression%200..1-++[SlotExpression],[Element]<range%200..1-%20[SlotExpression],[SlotDefinition]uses%20-.->[SlotExpression],[AnonymousSlotExpression]uses%20-.->[SlotExpression],[Expression]^-[SlotExpression],[SlotDefinition],[Expression],[Element],[AnonymousSlotExpression],[AnonymousClassExpression])](https://yuml.me/diagram/nofunky;dir:TB/class/[AnonymousSlotExpression]<all_of%200..*-++[SlotExpression&#124;required:boolean%20%3F;recommended:boolean%20%3F;minimum_value:integer%20%3F;maximum_value:integer%20%3F;pattern:string%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F;equals_expression:string%20%3F;minimum_cardinality:integer%20%3F;maximum_cardinality:integer%20%3F],[AnonymousSlotExpression]<any_of%200..*-++[SlotExpression],[AnonymousSlotExpression]<exactly_one_of%200..*-++[SlotExpression],[AnonymousSlotExpression]<none_of%200..*-++[SlotExpression],[SlotDefinition]<all_members%200..*-++[SlotExpression],[AnonymousSlotExpression]<has_member%200..1-++[SlotExpression],[AnonymousClassExpression]<range_expression%200..1-++[SlotExpression],[Element]<range%200..1-%20[SlotExpression],[SlotDefinition]uses%20-.->[SlotExpression],[AnonymousSlotExpression]uses%20-.->[SlotExpression],[Expression]^-[SlotExpression],[SlotDefinition],[Expression],[Element],[AnonymousSlotExpression],[AnonymousClassExpression])

## Parents

 *  is_a: [Expression](Expression.md) - todo

## Mixin for

 * [AnonymousSlotExpression](AnonymousSlotExpression.md) (mixin) 
 * [SlotDefinition](SlotDefinition.md) (mixin)  - the definition of a property or a slot

## Referenced by Class


## Attributes


### Own

 * [range](range.md)  <sub>0..1</sub>
     * Description: defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2

     * Range: [Element](Element.md)
 * [range_expression](range_expression.md)  <sub>0..1</sub>
     * Description: A range that is described as a boolean expression combining existing ranges
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
 * [required](required.md)  <sub>0..1</sub>
     * Description: true means that the slot must be present in the loaded definition
     * Range: [Boolean](types/Boolean.md)
 * [recommended](recommended.md)  <sub>0..1</sub>
     * Description: true means that the slot should be present in the loaded definition, but this is not required
     * Range: [Boolean](types/Boolean.md)
 * [minimum_value](minimum_value.md)  <sub>0..1</sub>
     * Description: for slots with ranges of type number, the value must be equal to or higher than this
     * Range: [Integer](types/Integer.md)
 * [maximum_value](maximum_value.md)  <sub>0..1</sub>
     * Description: for slots with ranges of type number, the value must be equal to or lowe than this
     * Range: [Integer](types/Integer.md)
 * [pattern](pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to this regular expression
     * Range: [String](types/String.md)
 * [equals_string](equals_string.md)  <sub>0..1</sub>
     * Description: the slot must have range string and the value of the slot must equal the specified value
     * Range: [String](types/String.md)
 * [equals_string_in](equals_string_in.md)  <sub>0..\*</sub>
     * Description: the slot must have range string and the value of the slot must equal one of the specified values
     * Range: [String](types/String.md)
 * [equals_number](equals_number.md)  <sub>0..1</sub>
     * Description: the slot must have range of a number and the value of the slot must equal the specified value
     * Range: [Integer](types/Integer.md)
 * [equals_expression](equals_expression.md)  <sub>0..1</sub>
     * Description: the value of the slot must equal the value of the evaluated expression
     * Range: [String](types/String.md)
 * [minimum_cardinality](minimum_cardinality.md)  <sub>0..1</sub>
     * Description: the minimum number of entries for a multivalued slot
     * Range: [Integer](types/Integer.md)
 * [maximum_cardinality](maximum_cardinality.md)  <sub>0..1</sub>
     * Description: the maximum number of entries for a multivalued slot
     * Range: [Integer](types/Integer.md)
 * [has_member](has_member.md)  <sub>0..1</sub>
     * Description: the values of the slot is multivalued with at least one member satisfying the condition
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
 * [all_members](all_members.md)  <sub>0..\*</sub>
     * Description: the value of the multiavlued slot is a list where all elements conform to the specified values.
this defines a dynamic class with named slots according to matching constraints

E.g to state that all members of a list are between 1 and 10
```
all_members:
  x:
    range: integer
    minimum_value: 10
    maximum_value: 10
```
     * Range: [SlotDefinition](SlotDefinition.md)
 * [slot_expression➞none_of](slot_expression_none_of.md)  <sub>0..\*</sub>
     * Description: holds if none of the expressions hold
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
 * [slot_expression➞exactly_one_of](slot_expression_exactly_one_of.md)  <sub>0..\*</sub>
     * Description: holds if only one of the expressions hold
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
 * [slot_expression➞any_of](slot_expression_any_of.md)  <sub>0..\*</sub>
     * Description: holds if at least one of the expressions hold
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
 * [slot_expression➞all_of](slot_expression_all_of.md)  <sub>0..\*</sub>
     * Description: holds if all of the expressions hold
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
