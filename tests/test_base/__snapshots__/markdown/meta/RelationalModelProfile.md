
# Subset: RelationalModelProfile


A profile that includes all the metamodel elements whose semantics can be expressed using the classic Relational Model.
The Relational Model excludes collections (multivalued slots) as first class entities. Instead, these must be
mapped to backreferences

The classic Relational Model excludes inheritance and polymorphism -- these must be rolled down to
concrete classes or otherwise transformed.

URI: [linkml:RelationalModelProfile](https://w3id.org/linkml/RelationalModelProfile)


### Classes

 * [ClassDefinition](ClassDefinition.md) - an element whose instances are complex objects that may have slot-value assignments
 * [EnumDefinition](EnumDefinition.md) - an element whose instances must be drawn from a specified set of permissible values
 * [SchemaDefinition](SchemaDefinition.md) - A collection of definitions that make up a schema or a data model.
 * [UniqueKey](UniqueKey.md) - a collection of slots whose values uniquely identify an instance of a class

### Mixins


### Slots

 * [attributes](attributes.md) - Inline definition of slots
 * [classes](classes.md) - An index to the collection of all class definitions in the schema
 * [identifier](identifier.md) - True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container
 * [key](key.md) - True means that the key slot(s) uniquely identify the elements within a single container
 * [name](name.md) - the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
 * [range](range.md) - defines the type of the object of the slot.  Given the following slot definition
 * [required](required.md) - true means that the slot must be present in instances of the class definition
 * [schema_definition➞name](schema_definition_name.md) - a unique name for the schema that is both human-readable and consists of only characters from the NCName set
 * [unique_key_name](unique_key_name.md) - name of the unique key
 * [unique_key_slots](unique_key_slots.md) - list of slot names that form a key. The tuple formed from the values of all these slots should be unique.
 * [unique_keys](unique_keys.md) - A collection of named unique keys for this class. Unique keys may be singular or compound.

### Types


### Enums

