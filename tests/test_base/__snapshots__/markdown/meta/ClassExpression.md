
# Class: class_expression


A boolean expression that can be used to dynamically determine membership of a class

URI: [linkml:ClassExpression](https://w3id.org/linkml/ClassExpression)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SlotDefinition],[SlotDefinition]<slot_conditions%200..*-++[ClassExpression],[AnonymousClassExpression]<all_of%200..*-++[ClassExpression],[AnonymousClassExpression]<none_of%200..*-++[ClassExpression],[AnonymousClassExpression]<exactly_one_of%200..*-++[ClassExpression],[AnonymousClassExpression]<any_of%200..*-++[ClassExpression],[ClassDefinition]uses%20-.->[ClassExpression],[AnonymousClassExpression]uses%20-.->[ClassExpression],[ClassDefinition],[AnonymousClassExpression])](https://yuml.me/diagram/nofunky;dir:TB/class/[SlotDefinition],[SlotDefinition]<slot_conditions%200..*-++[ClassExpression],[AnonymousClassExpression]<all_of%200..*-++[ClassExpression],[AnonymousClassExpression]<none_of%200..*-++[ClassExpression],[AnonymousClassExpression]<exactly_one_of%200..*-++[ClassExpression],[AnonymousClassExpression]<any_of%200..*-++[ClassExpression],[ClassDefinition]uses%20-.->[ClassExpression],[AnonymousClassExpression]uses%20-.->[ClassExpression],[ClassDefinition],[AnonymousClassExpression])

## Mixin for

 * [AnonymousClassExpression](AnonymousClassExpression.md) (mixin) 
 * [ClassDefinition](ClassDefinition.md) (mixin)  - an element whose instances are complex objects that may have slot-value assignments

## Referenced by Class


## Attributes


### Own

 * [class_expression➞any_of](class_expression_any_of.md)  <sub>0..\*</sub>
     * Description: holds if at least one of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
     * in subsets: (SpecificationSubset)
 * [class_expression➞exactly_one_of](class_expression_exactly_one_of.md)  <sub>0..\*</sub>
     * Description: holds if only one of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
     * in subsets: (SpecificationSubset)
 * [class_expression➞none_of](class_expression_none_of.md)  <sub>0..\*</sub>
     * Description: holds if none of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
     * in subsets: (SpecificationSubset)
 * [class_expression➞all_of](class_expression_all_of.md)  <sub>0..\*</sub>
     * Description: holds if all of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
     * in subsets: (SpecificationSubset)
 * [slot_conditions](slot_conditions.md)  <sub>0..\*</sub>
     * Description: expresses constraints on a group of slots for a class expression
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset)
