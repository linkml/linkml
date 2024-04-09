
# Slot: key

True means that the key slot(s) uniquely identify the elements within a single container

URI: [linkml:key](https://w3id.org/linkml/key)


## Domain and Range

[SlotDefinition](SlotDefinition.md) &#8594;  <sub>0..1</sub> [Boolean](types/Boolean.md)

## Parents


## Children


## Used by

 * [SlotDefinition](SlotDefinition.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | key is inherited |
|  | | a given domain can have at most one key slot (restriction to be removed in the future) |
|  | | identifiers and keys are mutually exclusive.  A given domain cannot have both |
|  | | a key slot is automatically required.  Keys cannot be optional |
| **In Subsets:** | | SpecificationSubset |
|  | | BasicSubset |
|  | | RelationalModelProfile |
| **See also:** | | [linkml:unique_keys](linkml:unique_keys) |