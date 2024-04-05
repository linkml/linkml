
# Slot: values_from


The identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.

URI: [linkml:values_from](https://w3id.org/linkml/values_from)


## Domain and Range

[Definition](Definition.md) &#8594;  <sub>0..\*</sub> [Uriorcurie](types/Uriorcurie.md)

## Parents


## Children


## Used by

 * [ClassDefinition](ClassDefinition.md)
 * [Definition](Definition.md)
 * [EnumDefinition](EnumDefinition.md)
 * [SlotDefinition](SlotDefinition.md)
