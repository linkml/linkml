
# Slot: identifier


True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container

URI: [linkml:identifier](https://w3id.org/linkml/identifier)


## Domain and Range

slot_definition &#8594;  <sub>0..1</sub> boolean

## Parents


## Children


## Used by

 * slot_definition

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

