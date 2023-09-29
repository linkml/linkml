
# Slot: recommended


true means that the slot should be present in instances of the class definition, but this is not required

URI: [linkml:recommended](https://w3id.org/linkml/recommended)


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
| **Comments:** | | This is to be used where not all data is expected to conform to having a required field |
|  | | If a slot is recommended, and it is not populated, applications must not treat this as an error. Applications may use this to inform the user of missing data |
| **In Subsets:** | | SpecificationSubset |
|  | | BasicSubset |
| **See also:** | | [https://github.com/linkml/linkml/issues/177](https://github.com/linkml/linkml/issues/177) |

