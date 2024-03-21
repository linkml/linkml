
# Slot: ifabsent


function that provides a default value for the slot.  Possible values for this slot are defined in linkml.utils.ifabsent_functions.default_library:
  * [Tt]rue -- boolean True
  * [Ff]alse -- boolean False
  * bnode -- blank node identifier
  * class_curie -- CURIE for the containing class
  * class_uri -- URI for the containing class
  * default_ns -- schema default namespace
  * default_range -- schema default range
  * int(value) -- integer value
  * slot_uri -- URI for the slot
  * slot_curie -- CURIE for the slot
  * string(value) -- string value

URI: [linkml:ifabsent](https://w3id.org/linkml/ifabsent)


## Domain and Range

[SlotDefinition](SlotDefinition.md) &#8594;  <sub>0..1</sub> [String](types/String.md)

## Parents


## Children


## Used by

 * [SlotDefinition](SlotDefinition.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | SpecificationSubset |
| **See also:** | | [linkml:equals_expression](linkml:equals_expression) |
| **Close Mappings:** | | sh:defaultValue |

