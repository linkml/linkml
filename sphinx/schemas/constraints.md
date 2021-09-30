# Adding constraints and rules

In addition to the basic [cardinality](slots) constraints for slots, additional constraints can be specified

## Unique Key

A [unique_key](https://w3id.org/linkml/unique_key) is a set of slots that are unique for members of any given class.

[identifier](https://w3id.org/linkml/identifier)s are special cases of unique keys.

## Patterns

The value of a slot can be constrained to conform to a particular string pattern using

[pattern](https://w3id.org/linkml/pattern)

## String serialization

A rule for generating the string value of a slot can be specified as a [string_serializationpattern](https://w3id.org/linkml/string_serializationpattern)

Note: this may not yet be implemented in all frameworks

## Minimum and Maximum values

Any numeric value can have minimum and maximum values specified

 * [minimum_value](https://w3id.org/linkml/minimum_value)
 * [maximum_value](https://w3id.org/linkml/maximum_value)




