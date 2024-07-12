
# Subset: MinimalSubset

The absolute minimal set of elements necessary for defining any schema.

schemas conforming to the minimal subset consist of classes, with all slots
inlined as attributes. There are no enums.

URI: [linkml:MinimalSubset](https://w3id.org/linkml/MinimalSubset)


### Classes

 * [ClassDefinition](ClassDefinition.md) - an element whose instances are complex objects that may have slot-value assignments
 * [SchemaDefinition](SchemaDefinition.md) - A collection of definitions that make up a schema or a data model.
 * [SlotDefinition](SlotDefinition.md) - an element that describes how instances are related to other instances

### Mixins


### Slots

 * [attributes](attributes.md) - Inline definition of slots
 * [classes](classes.md) - An index to the collection of all class definitions in the schema
 * [default_prefix](default_prefix.md) - The prefix that is used for all elements within a schema
 * [default_range](default_range.md) - default slot range to be used if range element is omitted from a slot definition
 * [enum_binding➞range](enum_binding_range.md)
 * [id](id.md) - The official schema URI
 * [identifier](identifier.md) - True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container
 * [multivalued](multivalued.md) - true means that slot can have more than one value and should be represented using a list or collection structure.
 * [name](name.md) - the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
 * [range](range.md) - defines the type of the object of the slot.  Given the following slot definition
 * [required](required.md) - true means that the slot must be present in instances of the class definition
 * [schema_definition➞name](schema_definition_name.md) - a unique name for the schema that is both human-readable and consists of only characters from the NCName set

### Types


### Enums

