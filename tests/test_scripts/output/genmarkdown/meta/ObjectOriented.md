
# Subset: object_oriented


The set of constructs that have an equivalent in a minimal object oriented metamodel

URI: [linkml:object_oriented](https://w3id.org/linkml/object_oriented)


### Classes

 * [ClassDefinition](ClassDefinition.md) - the definition of a class or interface
 * [EnumDefinition](EnumDefinition.md) - List of values that constrain the range of a slot
 * [SchemaDefinition](SchemaDefinition.md) - a collection of subset, type, slot and class definitions

### Mixins


### Slots

 * [abstract](abstract.md) - an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
 * [attributes](attributes.md) - Inline definition of slots
 * [class_definition➞is_a](class_definition_is_a.md)
 * [class_definition➞mixins](class_definition_mixins.md)
 * [classes](classes.md) - class definitions
 * [enums](enums.md) - enumerated ranges
 * [is_a](is_a.md) - specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
 * [mixin](mixin.md) - this slot or class can only be used as a mixin.
 * [mixins](mixins.md) - List of definitions to be mixed in. Targets may be any definition of the same type
 * [multivalued](multivalued.md) - true means that slot can have more than one value
 * [name](name.md) - the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
 * [permissible_value➞is_a](permissible_value_is_a.md)
 * [permissible_value➞mixins](permissible_value_mixins.md)
 * [range](range.md) - defines the type of the object of the slot.  Given the following slot definition
 * [required](required.md) - true means that the slot must be present in the loaded definition
 * [schema_definition➞name](schema_definition_name.md)
 * [slot_definition➞is_a](slot_definition_is_a.md)
 * [slot_definition➞mixins](slot_definition_mixins.md)
 * [types](types.md) - data types used in the model

### Types


### Enums

