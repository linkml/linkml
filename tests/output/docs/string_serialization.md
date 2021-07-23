
# Slot: string_serialization


Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm

URI: [linkml:string_serialization](https://w3id.org/linkml/string_serialization)


## Domain and Range

[Definition](Definition.md) &#8594;  <sub>0..1</sub> [String](types/String.md)

## Parents


## Children


## Used by

 * [ClassDefinition](ClassDefinition.md)
 * [Definition](Definition.md)
 * [SlotDefinition](SlotDefinition.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **See also:** | | https://github.com/linkml/issues/128 |

