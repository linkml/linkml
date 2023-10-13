
# Slot: inlined


True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.

URI: [linkml:inlined](https://w3id.org/linkml/inlined)


## Domain and Range

slot_definition &#8594;  <sub>0..1</sub> boolean

## Parents


## Children


## Used by

 * anonymous_slot_expression
 * slot_definition
 * slot_expression

## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | classes without keys or identifiers are necessarily inlined as lists |
|  | | only applicable in tree-like serializations, e.g json, yaml |
| **In Subsets:** | | SpecificationSubset |
|  | | BasicSubset |
| **See also:** | | [https://w3id.org/linkml/docs/specification/06mapping/#collection-forms](https://w3id.org/linkml/docs/specification/06mapping/#collection-forms) |

