
# Class: anonymous_class_expression




URI: [linkml:AnonymousClassExpression](https://w3id.org/linkml/AnonymousClassExpression)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[SlotExpression],[SlotDefinition],[Extension],[Example],[Definition],[ClassExpression],[ClassDefinition],[AnonymousExpression],[Definition]<is_a%200..1-%20[AnonymousClassExpression&#124;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F],[ClassExpression]++-%20all_of%200..*>[AnonymousClassExpression],[ClassExpression]++-%20any_of%200..*>[AnonymousClassExpression],[ClassExpression]++-%20exactly_one_of%200..*>[AnonymousClassExpression],[ClassExpression]++-%20none_of%200..*>[AnonymousClassExpression],[ClassDefinition]++-%20classification_rules%200..*>[AnonymousClassExpression],[ClassRule]++-%20elseconditions%200..1>[AnonymousClassExpression],[ClassRule]++-%20postconditions%200..1>[AnonymousClassExpression],[ClassRule]++-%20preconditions%200..1>[AnonymousClassExpression],[SlotExpression]++-%20range_expression%200..1>[AnonymousClassExpression],[AnonymousClassExpression]uses%20-.->[ClassExpression],[AnonymousExpression]^-[AnonymousClassExpression],[ClassRule],[Annotation],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[SlotExpression],[SlotDefinition],[Extension],[Example],[Definition],[ClassExpression],[ClassDefinition],[AnonymousExpression],[Definition]<is_a%200..1-%20[AnonymousClassExpression&#124;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F],[ClassExpression]++-%20all_of%200..*>[AnonymousClassExpression],[ClassExpression]++-%20any_of%200..*>[AnonymousClassExpression],[ClassExpression]++-%20exactly_one_of%200..*>[AnonymousClassExpression],[ClassExpression]++-%20none_of%200..*>[AnonymousClassExpression],[ClassDefinition]++-%20classification_rules%200..*>[AnonymousClassExpression],[ClassRule]++-%20elseconditions%200..1>[AnonymousClassExpression],[ClassRule]++-%20postconditions%200..1>[AnonymousClassExpression],[ClassRule]++-%20preconditions%200..1>[AnonymousClassExpression],[SlotExpression]++-%20range_expression%200..1>[AnonymousClassExpression],[AnonymousClassExpression]uses%20-.->[ClassExpression],[AnonymousExpression]^-[AnonymousClassExpression],[ClassRule],[Annotation],[AltDescription])

## Parents

 *  is_a: [AnonymousExpression](AnonymousExpression.md)

## Uses Mixin

 *  mixin: [ClassExpression](ClassExpression.md) - A boolean expression that can be used to dynamically determine membership of a class

## Referenced by Class

 *  **[ClassExpression](ClassExpression.md)** *[class_expression➞all_of](class_expression_all_of.md)*  <sub>0..\*</sub>  **[AnonymousClassExpression](AnonymousClassExpression.md)**
 *  **[ClassExpression](ClassExpression.md)** *[class_expression➞any_of](class_expression_any_of.md)*  <sub>0..\*</sub>  **[AnonymousClassExpression](AnonymousClassExpression.md)**
 *  **[ClassExpression](ClassExpression.md)** *[class_expression➞exactly_one_of](class_expression_exactly_one_of.md)*  <sub>0..\*</sub>  **[AnonymousClassExpression](AnonymousClassExpression.md)**
 *  **[ClassExpression](ClassExpression.md)** *[class_expression➞none_of](class_expression_none_of.md)*  <sub>0..\*</sub>  **[AnonymousClassExpression](AnonymousClassExpression.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[classification_rules](classification_rules.md)*  <sub>0..\*</sub>  **[AnonymousClassExpression](AnonymousClassExpression.md)**
 *  **None** *[elseconditions](elseconditions.md)*  <sub>0..1</sub>  **[AnonymousClassExpression](AnonymousClassExpression.md)**
 *  **None** *[postconditions](postconditions.md)*  <sub>0..1</sub>  **[AnonymousClassExpression](AnonymousClassExpression.md)**
 *  **None** *[preconditions](preconditions.md)*  <sub>0..1</sub>  **[AnonymousClassExpression](AnonymousClassExpression.md)**
 *  **[SlotExpression](SlotExpression.md)** *[range_expression](range_expression.md)*  <sub>0..1</sub>  **[AnonymousClassExpression](AnonymousClassExpression.md)**

## Attributes


### Own

 * [is_a](is_a.md)  <sub>0..1</sub>
     * Description: specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
     * Range: [Definition](Definition.md)

### Mixed in from class_expression:

 * [class_expression➞any_of](class_expression_any_of.md)  <sub>0..\*</sub>
     * Description: holds if at least one of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)

### Mixed in from class_expression:

 * [class_expression➞exactly_one_of](class_expression_exactly_one_of.md)  <sub>0..\*</sub>
     * Description: holds if only one of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)

### Mixed in from class_expression:

 * [class_expression➞none_of](class_expression_none_of.md)  <sub>0..\*</sub>
     * Description: holds if none of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)

### Mixed in from class_expression:

 * [class_expression➞all_of](class_expression_all_of.md)  <sub>0..\*</sub>
     * Description: holds if all of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)

### Mixed in from class_expression:

 * [slot_conditions](slot_conditions.md)  <sub>0..\*</sub>
     * Description: the redefinition of a slot in the context of the containing class definition.
     * Range: [SlotDefinition](SlotDefinition.md)
