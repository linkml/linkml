
# Subset: ObjectOrientedProfile


A profile that includes all the metamodel elements whose semantics can be expressed using a minimal
implementation of the object oriented metamodel as employed by languages such as Java and Python, or
in modeling frameworks like UML

URI: [linkml:ObjectOrientedProfile](https://w3id.org/linkml/ObjectOrientedProfile)


### Classes

 * [ClassDefinition](ClassDefinition.md) - an element whose instances are complex objects that may have slot-value assignments
 * [EnumDefinition](EnumDefinition.md) - an element whose instances must be drawn from a specified set of permissible values
 * [SchemaDefinition](SchemaDefinition.md) - A collection of definitions that make up a schema or a data model.

### Mixins


### Slots

 * [abstract](abstract.md) - Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.
 * [attributes](attributes.md) - Inline definition of slots
 * [class_definition➞is_a](class_definition_is_a.md) - A primary parent class from which inheritable metaslots are propagated
 * [class_definition➞mixins](class_definition_mixins.md) - A collection of secondary parent mixin classes from which inheritable metaslots are propagated
 * [classes](classes.md) - An index to the collection of all class definitions in the schema
 * [enums](enums.md) - An index to the collection of all enum definitions in the schema
 * [is_a](is_a.md) - A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
 * [mixin](mixin.md) - Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.
 * [mixins](mixins.md) - A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.
 * [multivalued](multivalued.md) - true means that slot can have more than one value and should be represented using a list or collection structure.
 * [name](name.md) - the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
 * [permissible_value➞is_a](permissible_value_is_a.md)
 * [permissible_value➞mixins](permissible_value_mixins.md)
 * [range](range.md) - defines the type of the object of the slot.  Given the following slot definition
 * [required](required.md) - true means that the slot must be present in instances of the class definition
 * [schema_definition➞name](schema_definition_name.md) - a unique name for the schema that is both human-readable and consists of only characters from the NCName set
 * [slot_definition➞is_a](slot_definition_is_a.md) - A primary parent slot from which inheritable metaslots are propagated
 * [slot_definition➞mixins](slot_definition_mixins.md) - A collection of secondary parent mixin slots from which inheritable metaslots are propagated
 * [types](types.md) - An index to the collection of all type definitions in the schema

### Types


### Enums

