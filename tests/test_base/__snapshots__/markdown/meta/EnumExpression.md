
# Class: enum_expression


An expression that constrains the range of a slot

URI: [linkml:EnumExpression](https://w3id.org/linkml/EnumExpression)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ReachabilityQuery],[PermissibleValue],[MatchQuery],[Expression],[MatchQuery]<matches%200..1-++[EnumExpression&#124;code_set:uriorcurie%20%3F;code_set_tag:string%20%3F;code_set_version:string%20%3F;pv_formula:pv_formula_options%20%3F;concepts:uriorcurie%20*],[ReachabilityQuery]<reachable_from%200..1-++[EnumExpression],[EnumDefinition]<inherits%200..*-%20[EnumExpression],[AnonymousEnumExpression]<minus%200..*-++[EnumExpression],[AnonymousEnumExpression]<include%200..*-++[EnumExpression],[PermissibleValue]<permissible_values%200..*-++[EnumExpression],[SlotExpression]++-%20enum_range%200..1>[EnumExpression],[EnumDefinition]uses%20-.->[EnumExpression],[AnonymousEnumExpression]uses%20-.->[EnumExpression],[Expression]^-[EnumExpression],[SlotExpression],[EnumDefinition],[AnonymousEnumExpression])](https://yuml.me/diagram/nofunky;dir:TB/class/[ReachabilityQuery],[PermissibleValue],[MatchQuery],[Expression],[MatchQuery]<matches%200..1-++[EnumExpression&#124;code_set:uriorcurie%20%3F;code_set_tag:string%20%3F;code_set_version:string%20%3F;pv_formula:pv_formula_options%20%3F;concepts:uriorcurie%20*],[ReachabilityQuery]<reachable_from%200..1-++[EnumExpression],[EnumDefinition]<inherits%200..*-%20[EnumExpression],[AnonymousEnumExpression]<minus%200..*-++[EnumExpression],[AnonymousEnumExpression]<include%200..*-++[EnumExpression],[PermissibleValue]<permissible_values%200..*-++[EnumExpression],[SlotExpression]++-%20enum_range%200..1>[EnumExpression],[EnumDefinition]uses%20-.->[EnumExpression],[AnonymousEnumExpression]uses%20-.->[EnumExpression],[Expression]^-[EnumExpression],[SlotExpression],[EnumDefinition],[AnonymousEnumExpression])

## Parents

 *  is_a: [Expression](Expression.md) - general mixin for any class that can represent some form of expression

## Mixin for

 * [AnonymousEnumExpression](AnonymousEnumExpression.md) (mixin)  - An enum_expression that is not named
 * [EnumDefinition](EnumDefinition.md) (mixin)  - an element whose instances must be drawn from a specified set of permissible values

## Referenced by Class

 *  **None** *[enum_range](enum_range.md)*  <sub>0..1</sub>  **[EnumExpression](EnumExpression.md)**

## Attributes


### Own

 * [code_set](code_set.md)  <sub>0..1</sub>
     * Description: the identifier of an enumeration code set.
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [code_set_tag](code_set_tag.md)  <sub>0..1</sub>
     * Description: the version tag of the enumeration code set
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [code_set_version](code_set_version.md)  <sub>0..1</sub>
     * Description: the version identifier of the enumeration code set
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [pv_formula](pv_formula.md)  <sub>0..1</sub>
     * Description: Defines the specific formula to be used to generate the permissible values.
     * Range: [pv_formula_options](pv_formula_options.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [permissible_values](permissible_values.md)  <sub>0..\*</sub>
     * Description: A list of possible values for a slot range
     * Range: [PermissibleValue](PermissibleValue.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [include](include.md)  <sub>0..\*</sub>
     * Description: An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set
     * Range: [AnonymousEnumExpression](AnonymousEnumExpression.md)
     * in subsets: (SpecificationSubset)
 * [minus](minus.md)  <sub>0..\*</sub>
     * Description: An enum expression that yields a list of permissible values that are to be subtracted from the enum
     * Range: [AnonymousEnumExpression](AnonymousEnumExpression.md)
     * in subsets: (SpecificationSubset)
 * [inherits](inherits.md)  <sub>0..\*</sub>
     * Description: An enum definition that is used as the basis to create a new enum
     * Range: [EnumDefinition](EnumDefinition.md)
     * in subsets: (SpecificationSubset)
 * [reachable_from](reachable_from.md)  <sub>0..1</sub>
     * Description: Specifies a query for obtaining a list of permissible values based on graph reachability
     * Range: [ReachabilityQuery](ReachabilityQuery.md)
     * in subsets: (SpecificationSubset)
 * [matches](matches.md)  <sub>0..1</sub>
     * Description: Specifies a match query that is used to calculate the list of permissible values
     * Range: [MatchQuery](MatchQuery.md)
     * in subsets: (SpecificationSubset)
 * [concepts](concepts.md)  <sub>0..\*</sub>
     * Description: A list of identifiers that are used to construct a set of permissible values
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset)
