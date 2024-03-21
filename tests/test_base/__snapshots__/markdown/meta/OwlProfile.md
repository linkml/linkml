
# Subset: OwlProfile


A profile that includes all the metamodel elements whose semantics can be expressed in OWL

URI: [linkml:OwlProfile](https://w3id.org/linkml/OwlProfile)


### Classes

 * [ClassDefinition](ClassDefinition.md) - an element whose instances are complex objects that may have slot-value assignments
 * [EnumDefinition](EnumDefinition.md) - an element whose instances must be drawn from a specified set of permissible values
 * [SchemaDefinition](SchemaDefinition.md) - A collection of definitions that make up a schema or a data model.
 * [SlotDefinition](SlotDefinition.md) - an element that describes how instances are related to other instances
 * [TypeDefinition](TypeDefinition.md) - an element that whose instances are atomic scalar values that can be mapped to primitive types

### Mixins


### Slots

 * [attributes](attributes.md) - Inline definition of slots
 * [class_definition➞is_a](class_definition_is_a.md) - A primary parent class from which inheritable metaslots are propagated
 * [class_definition➞mixins](class_definition_mixins.md) - A collection of secondary parent mixin classes from which inheritable metaslots are propagated
 * [class_definition➞union_of](class_definition_union_of.md)
 * [classes](classes.md) - An index to the collection of all class definitions in the schema
 * [enums](enums.md) - An index to the collection of all enum definitions in the schema
 * [id](id.md) - The official schema URI
 * [imports](imports.md) - A list of schemas that are to be included in this schema
 * [is_a](is_a.md) - A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
 * [mixins](mixins.md) - A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.
 * [name](name.md) - the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
 * [permissible_value➞is_a](permissible_value_is_a.md)
 * [permissible_value➞mixins](permissible_value_mixins.md)
 * [schema_definition➞name](schema_definition_name.md) - a unique name for the schema that is both human-readable and consists of only characters from the NCName set
 * [slot_definition➞is_a](slot_definition_is_a.md) - A primary parent slot from which inheritable metaslots are propagated
 * [slot_definition➞mixins](slot_definition_mixins.md) - A collection of secondary parent mixin slots from which inheritable metaslots are propagated
 * [slot_definition➞union_of](slot_definition_union_of.md)
 * [schema_definition➞slots](slot_definitions.md) - An index to the collection of all slot definitions in the schema
 * [type_definition➞union_of](type_definition_union_of.md)
 * [types](types.md) - An index to the collection of all type definitions in the schema
 * [union_of](union_of.md) - indicates that the domain element consists exactly of the members of the element in the range.

### Types


### Enums

