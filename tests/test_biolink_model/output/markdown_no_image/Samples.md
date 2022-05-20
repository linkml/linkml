
# Subset: samples


Sample/biosample datamodel

URI: [biolink:samples](https://w3id.org/biolink/vocab/samples)


### Classes

 * [Attribute](Attribute.md) - A property or characteristic of an entity. For example, an apple may have properties such as color, shape, age, crispiness. An environmental sample may have attributes such as depth, lat, long, material.

### Mixins


### Slots

 * [agent➞name](agent_name.md) - it is recommended that an author's 'name' property be formatted as "surname, firstname initial."
 * [attribute➞name](attribute_name.md) - The human-readable 'attribute name' can be set to a string which reflects its context of interpretation, e.g. SEPIO evidence/provenance/confidence annotation or it can default to the name associated with the 'has attribute type' slot ontology term.
 * [clinical finding➞has attribute](clinical_finding_has_attribute.md)
 * [clinical measurement➞has attribute type](clinical_measurement_has_attribute_type.md)
 * [derives from](derives_from.md) - holds between two distinct material entities, the new entity and the old entity, in which the new entity begins to exist when the old entity ceases to exist, and the new entity inherits the significant portion of the matter of the old entity
 * [has attribute](has_attribute.md) - connects any entity to an attribute
 * [has attribute type](has_attribute_type.md) - connects an attribute to a class that describes it
 * [has numeric value](has_numeric_value.md) - connects a quantity value to a number
 * [has qualitative value](has_qualitative_value.md) - connects an attribute to a value
 * [has quantitative value](has_quantitative_value.md) - connects an attribute to a value
 * [has unit](has_unit.md) - connects a quantity value to a unit
 * [iri](iri.md) - An IRI for an entity. This is determined by the id using expansion rules.
 * [macromolecular machine mixin➞name](macromolecular_machine_mixin_name.md) - genes are typically designated by a short symbol and a full name. We map the symbol to the default display name and use an additional slot for full name
 * [name](name.md) - A human-readable name for an attribute or entity.
 * [organismal entity➞has attribute](organismal_entity_has_attribute.md) - may often be an organism attribute
 * [publication➞name](publication_name.md) - the 'title' of the publication is generally recorded in the 'name' property (inherited from NamedThing). The field name 'title' is now also tagged as an acceptable alias for the node property 'name' (just in case).
 * [socioeconomic exposure➞has attribute](socioeconomic_exposure_has_attribute.md)

### Types


### Enums

