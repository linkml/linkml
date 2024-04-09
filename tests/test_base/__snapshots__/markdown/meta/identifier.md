
# Slot: identifier

True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container

URI: [linkml:identifier](https://w3id.org/linkml/identifier)


## Domain and Range

[SlotDefinition](SlotDefinition.md) &#8594;  <sub>0..1</sub> [Boolean](types/Boolean.md)

## Parents


## Children


## Used by

 * [SlotDefinition](SlotDefinition.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | primary key |
|  | | ID |
|  | | UID |
|  | | code |
| **Comments:** | | identifier is inherited |
|  | | a key slot is automatically required.  Identifiers cannot be optional |
|  | | a given domain can have at most one identifier |
|  | | identifiers and keys are mutually exclusive.  A given domain cannot have both |
| **In Subsets:** | | SpecificationSubset |
|  | | MinimalSubset |
|  | | BasicSubset |
|  | | RelationalModelProfile |
| **See also:** | | [https://en.wikipedia.org/wiki/Identifier](https://en.wikipedia.org/wiki/Identifier) |
|  | | [linkml:unique_keys](linkml:unique_keys) |