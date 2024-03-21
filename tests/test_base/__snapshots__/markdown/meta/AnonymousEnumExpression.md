
# Class: anonymous_enum_expression


An enum_expression that is not named

URI: [linkml:AnonymousEnumExpression](https://w3id.org/linkml/AnonymousEnumExpression)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ReachabilityQuery],[PermissibleValue],[MatchQuery],[EnumExpression],[EnumDefinition],[EnumExpression]++-%20include%200..*>[AnonymousEnumExpression&#124;code_set:uriorcurie%20%3F;code_set_tag:string%20%3F;code_set_version:string%20%3F;pv_formula:pv_formula_options%20%3F;concepts:uriorcurie%20*],[EnumExpression]++-%20minus%200..*>[AnonymousEnumExpression],[AnonymousEnumExpression]uses%20-.->[EnumExpression])](https://yuml.me/diagram/nofunky;dir:TB/class/[ReachabilityQuery],[PermissibleValue],[MatchQuery],[EnumExpression],[EnumDefinition],[EnumExpression]++-%20include%200..*>[AnonymousEnumExpression&#124;code_set:uriorcurie%20%3F;code_set_tag:string%20%3F;code_set_version:string%20%3F;pv_formula:pv_formula_options%20%3F;concepts:uriorcurie%20*],[EnumExpression]++-%20minus%200..*>[AnonymousEnumExpression],[AnonymousEnumExpression]uses%20-.->[EnumExpression])

## Uses Mixin

 *  mixin: [EnumExpression](EnumExpression.md) - An expression that constrains the range of a slot

## Referenced by Class

 *  **[EnumExpression](EnumExpression.md)** *[include](include.md)*  <sub>0..\*</sub>  **[AnonymousEnumExpression](AnonymousEnumExpression.md)**
 *  **[EnumExpression](EnumExpression.md)** *[minus](minus.md)*  <sub>0..\*</sub>  **[AnonymousEnumExpression](AnonymousEnumExpression.md)**

## Attributes


### Mixed in from enum_expression:

 * [code_set](code_set.md)  <sub>0..1</sub>
     * Description: the identifier of an enumeration code set.
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from enum_expression:

 * [code_set_tag](code_set_tag.md)  <sub>0..1</sub>
     * Description: the version tag of the enumeration code set
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

### Mixed in from enum_expression:

 * [code_set_version](code_set_version.md)  <sub>0..1</sub>
     * Description: the version identifier of the enumeration code set
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

### Mixed in from enum_expression:

 * [pv_formula](pv_formula.md)  <sub>0..1</sub>
     * Description: Defines the specific formula to be used to generate the permissible values.
     * Range: [pv_formula_options](pv_formula_options.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from enum_expression:

 * [permissible_values](permissible_values.md)  <sub>0..\*</sub>
     * Description: A list of possible values for a slot range
     * Range: [PermissibleValue](PermissibleValue.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from enum_expression:

 * [include](include.md)  <sub>0..\*</sub>
     * Description: An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set
     * Range: [AnonymousEnumExpression](AnonymousEnumExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from enum_expression:

 * [minus](minus.md)  <sub>0..\*</sub>
     * Description: An enum expression that yields a list of permissible values that are to be subtracted from the enum
     * Range: [AnonymousEnumExpression](AnonymousEnumExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from enum_expression:

 * [inherits](inherits.md)  <sub>0..\*</sub>
     * Description: An enum definition that is used as the basis to create a new enum
     * Range: [EnumDefinition](EnumDefinition.md)
     * in subsets: (SpecificationSubset)

### Mixed in from enum_expression:

 * [reachable_from](reachable_from.md)  <sub>0..1</sub>
     * Description: Specifies a query for obtaining a list of permissible values based on graph reachability
     * Range: [ReachabilityQuery](ReachabilityQuery.md)
     * in subsets: (SpecificationSubset)

### Mixed in from enum_expression:

 * [matches](matches.md)  <sub>0..1</sub>
     * Description: Specifies a match query that is used to calculate the list of permissible values
     * Range: [MatchQuery](MatchQuery.md)
     * in subsets: (SpecificationSubset)

### Mixed in from enum_expression:

 * [concepts](concepts.md)  <sub>0..\*</sub>
     * Description: A list of identifiers that are used to construct a set of permissible values
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset)
