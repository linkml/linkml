
# Slot: value_presence


if true then a value must be present (for lists there must be at least one value). If false then a value must be absent (for lists, must be empty)

URI: [linkml:value_presence](https://w3id.org/linkml/value_presence)


## Domain and Range

slot_definition &#8594;  <sub>0..1</sub> [presence_enum](presence_enum.md)

## Parents

 *  is_a: list_value_specification_constant

## Children


## Used by

 * anonymous_slot_expression
 * slot_definition
 * slot_expression

## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | if set to true this has the same effect as required=true. In contrast, required=false allows a value to be present |

