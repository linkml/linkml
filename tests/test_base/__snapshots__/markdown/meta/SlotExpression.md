
# Class: slot_expression

an expression that constrains the range of values a slot can take

URI: [linkml:SlotExpression](https://w3id.org/linkml/SlotExpression)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[AnonymousSlotExpression]<all_of%200..*-++[SlotExpression&#124;required:boolean%20%3F;recommended:boolean%20%3F;inlined:boolean%20%3F;inlined_as_list:boolean%20%3F;pattern:string%20%3F;implicit_prefix:string%20%3F;value_presence:presence_enum%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F;equals_expression:string%20%3F;exact_cardinality:integer%20%3F;minimum_cardinality:integer%20%3F;maximum_cardinality:integer%20%3F],[AnonymousSlotExpression]<any_of%200..*-++[SlotExpression],[AnonymousSlotExpression]<exactly_one_of%200..*-++[SlotExpression],[AnonymousSlotExpression]<none_of%200..*-++[SlotExpression],[AnonymousSlotExpression]<all_members%200..1-++[SlotExpression],[AnonymousSlotExpression]<has_member%200..1-++[SlotExpression],[UnitOfMeasure]<unit%200..1-++[SlotExpression],[PatternExpression]<structured_pattern%200..1-++[SlotExpression],[Anything]<maximum_value%200..1-++[SlotExpression],[Anything]<minimum_value%200..1-++[SlotExpression],[EnumExpression]<enum_range%200..1-++[SlotExpression],[AnonymousClassExpression]<range_expression%200..1-++[SlotExpression],[Element]<range%200..1-%20[SlotExpression],[SlotDefinition]uses%20-.->[SlotExpression],[AnonymousSlotExpression]uses%20-.->[SlotExpression],[Expression]^-[SlotExpression],[SlotDefinition],[PatternExpression],[Expression],[EnumExpression],[Element],[AnonymousSlotExpression],[AnonymousClassExpression],[UnitOfMeasure],[Anything])](https://yuml.me/diagram/nofunky;dir:TB/class/[AnonymousSlotExpression]<all_of%200..*-++[SlotExpression&#124;required:boolean%20%3F;recommended:boolean%20%3F;inlined:boolean%20%3F;inlined_as_list:boolean%20%3F;pattern:string%20%3F;implicit_prefix:string%20%3F;value_presence:presence_enum%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F;equals_expression:string%20%3F;exact_cardinality:integer%20%3F;minimum_cardinality:integer%20%3F;maximum_cardinality:integer%20%3F],[AnonymousSlotExpression]<any_of%200..*-++[SlotExpression],[AnonymousSlotExpression]<exactly_one_of%200..*-++[SlotExpression],[AnonymousSlotExpression]<none_of%200..*-++[SlotExpression],[AnonymousSlotExpression]<all_members%200..1-++[SlotExpression],[AnonymousSlotExpression]<has_member%200..1-++[SlotExpression],[UnitOfMeasure]<unit%200..1-++[SlotExpression],[PatternExpression]<structured_pattern%200..1-++[SlotExpression],[Anything]<maximum_value%200..1-++[SlotExpression],[Anything]<minimum_value%200..1-++[SlotExpression],[EnumExpression]<enum_range%200..1-++[SlotExpression],[AnonymousClassExpression]<range_expression%200..1-++[SlotExpression],[Element]<range%200..1-%20[SlotExpression],[SlotDefinition]uses%20-.->[SlotExpression],[AnonymousSlotExpression]uses%20-.->[SlotExpression],[Expression]^-[SlotExpression],[SlotDefinition],[PatternExpression],[Expression],[EnumExpression],[Element],[AnonymousSlotExpression],[AnonymousClassExpression],[UnitOfMeasure],[Anything])

## Parents

 *  is_a: [Expression](Expression.md) - general mixin for any class that can represent some form of expression

## Mixin for

 * [AnonymousSlotExpression](AnonymousSlotExpression.md) (mixin) 
 * [SlotDefinition](SlotDefinition.md) (mixin)  - an element that describes how instances are related to other instances

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
     * in subsets: (SpecificationSubset,MinimalSubset,BasicSubset,RelationalModelProfile,ObjectOrientedProfile)
 * [range_expression](range_expression.md)  <sub>0..1</sub>
     * Description: A range that is described as a boolean expression combining existing ranges
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
     * in subsets: (SpecificationSubset)
 * [enum_range](enum_range.md)  <sub>0..1</sub>
     * Description: An inlined enumeration
     * Range: [EnumExpression](EnumExpression.md)
     * in subsets: (SpecificationSubset)
 * [required](required.md)  <sub>0..1</sub>
     * Description: true means that the slot must be present in instances of the class definition
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,MinimalSubset,BasicSubset,RelationalModelProfile,ObjectOrientedProfile)
 * [recommended](recommended.md)  <sub>0..1</sub>
     * Description: true means that the slot should be present in instances of the class definition, but this is not required
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [inlined](inlined.md)  <sub>0..1</sub>
     * Description: True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [inlined_as_list](inlined_as_list.md)  <sub>0..1</sub>
     * Description: True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [minimum_value](minimum_value.md)  <sub>0..1</sub>
     * Description: For ordinal ranges, the value must be equal to or higher than this
     * Range: [Anything](Anything.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [maximum_value](maximum_value.md)  <sub>0..1</sub>
     * Description: For ordinal ranges, the value must be equal to or lower than this
     * Range: [Anything](Anything.md)
     * in subsets: (SpecificationSubset,BasicSubset)
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
 * [value_presence](value_presence.md)  <sub>0..1</sub>
     * Description: if true then a value must be present (for lists there must be at least one value). If false then a value must be absent (for lists, must be empty)
     * Range: [presence_enum](presence_enum.md)
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
 * [equals_expression](equals_expression.md)  <sub>0..1</sub>
     * Description: the value of the slot must equal the value of the evaluated expression
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)
 * [exact_cardinality](exact_cardinality.md)  <sub>0..1</sub>
     * Description: the exact number of entries for a multivalued slot
     * Range: [Integer](types/Integer.md)
     * in subsets: (SpecificationSubset)
 * [minimum_cardinality](minimum_cardinality.md)  <sub>0..1</sub>
     * Description: the minimum number of entries for a multivalued slot
     * Range: [Integer](types/Integer.md)
     * in subsets: (SpecificationSubset)
 * [maximum_cardinality](maximum_cardinality.md)  <sub>0..1</sub>
     * Description: the maximum number of entries for a multivalued slot
     * Range: [Integer](types/Integer.md)
     * in subsets: (SpecificationSubset)
 * [has_member](has_member.md)  <sub>0..1</sub>
     * Description: the value of the slot is multivalued with at least one member satisfying the condition
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
     * in subsets: (SpecificationSubset)
 * [all_members](all_members.md)  <sub>0..1</sub>
     * Description: the value of the slot is multivalued with all members satisfying the condition
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
     * in subsets: (SpecificationSubset)
 * [slot_expression➞none_of](slot_expression_none_of.md)  <sub>0..\*</sub>
     * Description: holds if none of the expressions hold
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
     * in subsets: (SpecificationSubset)
 * [slot_expression➞exactly_one_of](slot_expression_exactly_one_of.md)  <sub>0..\*</sub>
     * Description: holds if only one of the expressions hold
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
     * in subsets: (SpecificationSubset)
 * [slot_expression➞any_of](slot_expression_any_of.md)  <sub>0..\*</sub>
     * Description: holds if at least one of the expressions hold
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
     * in subsets: (SpecificationSubset)
 * [slot_expression➞all_of](slot_expression_all_of.md)  <sub>0..\*</sub>
     * Description: holds if all of the expressions hold
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
     * in subsets: (SpecificationSubset)
