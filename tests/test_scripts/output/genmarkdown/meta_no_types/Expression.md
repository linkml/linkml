
# Class: expression


general mixin for any class that can represent some form of expression

URI: [linkml:Expression](https://w3id.org/linkml/Expression)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeExpression],[SlotExpression],[TypeExpression]++-%20all_of(i)%200..*>[Expression],[PathExpression]++-%20all_of(i)%200..*>[Expression],[SlotExpression]++-%20all_of(i)%200..*>[Expression],[ClassExpression]++-%20all_of(i)%200..*>[Expression],[TypeExpression]++-%20any_of(i)%200..*>[Expression],[PathExpression]++-%20any_of(i)%200..*>[Expression],[SlotExpression]++-%20any_of(i)%200..*>[Expression],[ClassExpression]++-%20any_of(i)%200..*>[Expression],[TypeExpression]++-%20exactly_one_of(i)%200..*>[Expression],[PathExpression]++-%20exactly_one_of(i)%200..*>[Expression],[SlotExpression]++-%20exactly_one_of(i)%200..*>[Expression],[ClassExpression]++-%20exactly_one_of(i)%200..*>[Expression],[PathExpression]++-%20followed_by(i)%200..1>[Expression],[TypeExpression]++-%20none_of(i)%200..*>[Expression],[PathExpression]++-%20none_of(i)%200..*>[Expression],[SlotExpression]++-%20none_of(i)%200..*>[Expression],[ClassExpression]++-%20none_of(i)%200..*>[Expression],[StructuredAlias]uses%20-.->[Expression],[PathExpression]uses%20-.->[Expression],[AnonymousExpression]uses%20-.->[Expression],[Expression]^-[TypeExpression],[Expression]^-[SlotExpression],[Expression]^-[EnumExpression],[StructuredAlias],[PathExpression],[EnumExpression],[ClassExpression],[AnonymousExpression])](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeExpression],[SlotExpression],[TypeExpression]++-%20all_of(i)%200..*>[Expression],[PathExpression]++-%20all_of(i)%200..*>[Expression],[SlotExpression]++-%20all_of(i)%200..*>[Expression],[ClassExpression]++-%20all_of(i)%200..*>[Expression],[TypeExpression]++-%20any_of(i)%200..*>[Expression],[PathExpression]++-%20any_of(i)%200..*>[Expression],[SlotExpression]++-%20any_of(i)%200..*>[Expression],[ClassExpression]++-%20any_of(i)%200..*>[Expression],[TypeExpression]++-%20exactly_one_of(i)%200..*>[Expression],[PathExpression]++-%20exactly_one_of(i)%200..*>[Expression],[SlotExpression]++-%20exactly_one_of(i)%200..*>[Expression],[ClassExpression]++-%20exactly_one_of(i)%200..*>[Expression],[PathExpression]++-%20followed_by(i)%200..1>[Expression],[TypeExpression]++-%20none_of(i)%200..*>[Expression],[PathExpression]++-%20none_of(i)%200..*>[Expression],[SlotExpression]++-%20none_of(i)%200..*>[Expression],[ClassExpression]++-%20none_of(i)%200..*>[Expression],[StructuredAlias]uses%20-.->[Expression],[PathExpression]uses%20-.->[Expression],[AnonymousExpression]uses%20-.->[Expression],[Expression]^-[TypeExpression],[Expression]^-[SlotExpression],[Expression]^-[EnumExpression],[StructuredAlias],[PathExpression],[EnumExpression],[ClassExpression],[AnonymousExpression])

## Children

 * [EnumExpression](EnumExpression.md) - An expression that constrains the range of a slot
 * [SlotExpression](SlotExpression.md) - an expression that constrains the range of values a slot can take
 * [TypeExpression](TypeExpression.md) - An abstract class grouping named types and anonymous type expressions

## Mixin for

 * [AnonymousExpression](AnonymousExpression.md) (mixin)  - An abstract parent class for any nested expression
 * [PathExpression](PathExpression.md) (mixin)  - An expression that describes an abstract path from an object to another through a sequence of slot lookups
 * [StructuredAlias](StructuredAlias.md) (mixin)  - object that contains meta data about a synonym or alias including where it came from (source) and its scope (narrow, broad, etc.)

## Referenced by Class

 *  **None** *[all_of](all_of.md)*  <sub>0..\*</sub>  **[Expression](Expression.md)**
 *  **None** *[any_of](any_of.md)*  <sub>0..\*</sub>  **[Expression](Expression.md)**
 *  **None** *[boolean_slot](boolean_slot.md)*  <sub>0..\*</sub>  **[Expression](Expression.md)**
 *  **None** *[exactly_one_of](exactly_one_of.md)*  <sub>0..\*</sub>  **[Expression](Expression.md)**
 *  **None** *[followed_by](followed_by.md)*  <sub>0..1</sub>  **[Expression](Expression.md)**
 *  **None** *[none_of](none_of.md)*  <sub>0..\*</sub>  **[Expression](Expression.md)**

## Attributes

