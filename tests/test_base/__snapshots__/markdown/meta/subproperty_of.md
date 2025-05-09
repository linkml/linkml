
# Slot: subproperty_of

Ontology property which this slot is a subproperty of.  Note: setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.

URI: [linkml:subproperty_of](https://w3id.org/linkml/subproperty_of)


## Domain and Range

[SlotDefinition](SlotDefinition.md) &#8594;  <sub>0..1</sub> [SlotDefinition](SlotDefinition.md)

## Parents


## Children


## Used by

 * [SlotDefinition](SlotDefinition.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | rdfs:subPropertyOf |
| **Examples:** | | Example({
  'value': 'RO:HOM0000001',
  'description': ('this is the RO term for "in homology relationship with", and used as a value '
     'of subproperty of this means that any ontological child (related to '
     'RO:HOM0000001 via an is_a relationship), is a valid value for the slot that '
     'declares this with the subproperty_of tag.  This differs from the '
     "'values_from' meta model component in that 'values_from' requires the id of "
     'a value set (said another way, if an entire ontology had a curie/identifier '
     'that was the identifier for the entire ontology, then that identifier would '
     "be used in 'values_from.')")
}) |