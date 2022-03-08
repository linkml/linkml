
# Subset: relational_model


The set of constructs that have an equivalent in the classic relational mode as defined by Codd

URI: [linkml:relational_model](https://w3id.org/linkml/relational_model)


### Classes

 * [ClassDefinition](ClassDefinition.md) - the definition of a class or interface
 * [EnumDefinition](EnumDefinition.md) - List of values that constrain the range of a slot
 * [SchemaDefinition](SchemaDefinition.md) - a collection of subset, type, slot and class definitions
 * [UniqueKey](UniqueKey.md) - a collection of slots whose values uniquely identify an instance of a class

### Mixins


### Slots

 * [attributes](attributes.md) - Inline definition of slots
 * [classes](classes.md) - class definitions
 * [identifier](identifier.md) - True means that the key slot(s) uniquely identify the container. There can be at most one identifier or key per container
 * [key](key.md) - True means that the key slot(s) uniquely identify the container.
 * [name](name.md) - the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
 * [range](range.md) - defines the type of the object of the slot.  Given the following slot definition
 * [required](required.md) - true means that the slot must be present in the loaded definition
 * [schema_definition➞name](schema_definition_name.md)
 * [unique_key_name](unique_key_name.md) - name of the unique key
 * [unique_key_slots](unique_key_slots.md) - list of slot names that form a key
 * [unique_keys](unique_keys.md) - Set of unique keys for this slot

### Types


### Enums

