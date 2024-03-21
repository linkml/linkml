
# Subset: BasicSubset


An extension of MinimalSubset that avoids advanced constructs and can be implemented by a broad variety of tools.

This subset roughly corresponds to the union of most standard constructs used in relational datamodel modeling,
object oriented modeling, and simple JSON-style modeling, while avoiding more advanced constructs from these languages.

It is often possible to translate from a more expressive schema to a BasicSubset schema, through a schema derivation
process

URI: [linkml:BasicSubset](https://w3id.org/linkml/BasicSubset)


### Classes

 * [AltDescription](AltDescription.md) - an attributed description
 * [ClassDefinition](ClassDefinition.md) - an element whose instances are complex objects that may have slot-value assignments
 * [Definition](Definition.md) - abstract base class for core metaclasses
 * [Element](Element.md) - A named element in the model
 * [EnumDefinition](EnumDefinition.md) - an element whose instances must be drawn from a specified set of permissible values
 * [Example](Example.md) - usage example and description
 * [PermissibleValue](PermissibleValue.md) - a permissible value, accompanied by intended text and an optional mapping to a concept URI
 * [Prefix](Prefix.md) - prefix URI tuple
 * [SchemaDefinition](SchemaDefinition.md) - A collection of definitions that make up a schema or a data model.
 * [SlotDefinition](SlotDefinition.md) - an element that describes how instances are related to other instances
 * [SubsetDefinition](SubsetDefinition.md) - an element that can be used to group other metamodel elements
 * [TypeDefinition](TypeDefinition.md) - an element that whose instances are atomic scalar values that can be mapped to primitive types
 * [UniqueKey](UniqueKey.md) - a collection of slots whose values uniquely identify an instance of a class

### Mixins

 * [CommonMetadata](CommonMetadata.md) - Generic metadata shared across definitions

### Slots

 * [abstract](abstract.md) - Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.
 * [aliases](aliases.md) - Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
 * [alt_description➞source](alt_description_source.md) - the source of an attributed description
 * [alt_description➞description](alt_description_text.md) - text of an attributed description
 * [alt_descriptions](alt_descriptions.md) - A sourced alternative description for an element
 * [attributes](attributes.md) - Inline definition of slots
 * [base](base.md) - python base type in the LinkML runtime that implements this type definition
 * [categories](categories.md) - Controlled terms used to categorize an element.
 * [class_definition➞is_a](class_definition_is_a.md) - A primary parent class from which inheritable metaslots are propagated
 * [class_definition➞mixins](class_definition_mixins.md) - A collection of secondary parent mixin classes from which inheritable metaslots are propagated
 * [class_uri](class_uri.md) - URI of the class that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas
 * [classes](classes.md) - An index to the collection of all class definitions in the schema
 * [code_set](code_set.md) - the identifier of an enumeration code set.
 * [code_set_tag](code_set_tag.md) - the version tag of the enumeration code set
 * [code_set_version](code_set_version.md) - the version identifier of the enumeration code set
 * [comments](comments.md) - notes and comments about an element intended primarily for external consumption
 * [conforms_to](conforms_to.md) - An established standard to which the element conforms.
 * [contributors](contributors.md) - agent that contributed to the element
 * [created_by](created_by.md) - agent that created the element
 * [created_on](created_on.md) - time at which the element was created
 * [default_curi_maps](default_curi_maps.md) - ordered list of prefixcommon biocontexts to be fetched to resolve id prefixes and inline prefix variables
 * [default_prefix](default_prefix.md) - The prefix that is used for all elements within a schema
 * [default_range](default_range.md) - default slot range to be used if range element is omitted from a slot definition
 * [deprecated](deprecated.md) - Description of why and when this element will no longer be used
 * [description](description.md) - a textual description of the element's purpose and use
 * [enum_uri](enum_uri.md) - URI of the enum that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas
 * [enums](enums.md) - An index to the collection of all enum definitions in the schema
 * [examples](examples.md) - example usages of an element
 * [generation_date](generation_date.md) - date and time that the schema was loaded/generated
 * [id](id.md) - The official schema URI
 * [id_prefixes](id_prefixes.md) - An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
 * [identifier](identifier.md) - True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container
 * [imports](imports.md) - A list of schemas that are to be included in this schema
 * [in_subset](in_subset.md) - used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
 * [inlined](inlined.md) - True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
 * [inlined_as_list](inlined_as_list.md) - True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
 * [is_a](is_a.md) - A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
 * [is_grouping_slot](is_grouping_slot.md) - true if this slot is a grouping slot
 * [key](key.md) - True means that the key slot(s) uniquely identify the elements within a single container
 * [keywords](keywords.md) - Keywords or tags used to describe the element
 * [last_updated_on](last_updated_on.md) - time at which the element was last updated
 * [license](license.md) - license for the schema
 * [maximum_value](maximum_value.md) - For ordinal ranges, the value must be equal to or lower than this
 * [meaning](meaning.md) - the value meaning of a permissible value
 * [metamodel_version](metamodel_version.md) - Version of the metamodel used to load the schema
 * [minimum_value](minimum_value.md) - For ordinal ranges, the value must be equal to or higher than this
 * [mixin](mixin.md) - Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.
 * [mixins](mixins.md) - A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.
 * [modified_by](modified_by.md) - agent that modified the element
 * [multivalued](multivalued.md) - true means that slot can have more than one value and should be represented using a list or collection structure.
 * [name](name.md) - the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
 * [notes](notes.md) - editorial notes about an element intended primarily for internal consumption
 * [owned_by](owned_by.md) - agent that owns or is the steward of the element
 * [pattern](pattern.md) - the string value of the slot must conform to this regular expression expressed in the string
 * [permissible_value➞is_a](permissible_value_is_a.md)
 * [permissible_value➞mixins](permissible_value_mixins.md)
 * [permissible_values](permissible_values.md) - A list of possible values for a slot range
 * [prefix_prefix](prefix_prefix.md) - The prefix components of a prefix expansions. This is the part that appears before the colon in a CURIE.
 * [prefix_reference](prefix_reference.md) - The namespace to which a prefix expands to.
 * [prefixes](prefixes.md) - A collection of prefix expansions that specify how CURIEs can be expanded to URIs
 * [publisher](publisher.md) - An entity responsible for making the resource available
 * [pv_formula](pv_formula.md) - Defines the specific formula to be used to generate the permissible values.
 * [range](range.md) - defines the type of the object of the slot.  Given the following slot definition
 * [rank](rank.md) - the relative order in which the element occurs, lower values are given precedence
 * [recommended](recommended.md) - true means that the slot should be present in instances of the class definition, but this is not required
 * [repr](repr.md) - the name of the python object that implements this type definition
 * [required](required.md) - true means that the slot must be present in instances of the class definition
 * [schema_definition➞name](schema_definition_name.md) - a unique name for the schema that is both human-readable and consists of only characters from the NCName set
 * [see_also](see_also.md) - A list of related entities or URLs that may be of relevance
 * [singular_name](singular_name.md) - a name that is used in the singular form
 * [slot_definition➞is_a](slot_definition_is_a.md) - A primary parent slot from which inheritable metaslots are propagated
 * [slot_definition➞mixins](slot_definition_mixins.md) - A collection of secondary parent mixin slots from which inheritable metaslots are propagated
 * [schema_definition➞slots](slot_definitions.md) - An index to the collection of all slot definitions in the schema
 * [slot_group](slot_group.md) - allows for grouping of related slots into a grouping slot that serves the role of a group
 * [slot_uri](slot_uri.md) - URI of the class that provides a semantic interpretation of the slot in a linked data context. The URI may come from any namespace and may be shared between schemas.
 * [slot_usage](slot_usage.md) - the refinement of a slot in the context of the containing class definition.
 * [slots](slots.md) - collection of slot names that are applicable to a class
 * [source](source.md) - A related resource from which the element is derived.
 * [source_file](source_file.md) - name, uri or description of the source of the schema
 * [source_file_date](source_file_date.md) - modification date of the source of the schema
 * [source_file_size](source_file_size.md) - size in bytes of the source of the schema
 * [status](status.md) - status of the element
 * [structured_alias➞categories](structured_alias_categories.md) - The category or categories of an alias. This can be drawn from any relevant vocabulary
 * [subsets](subsets.md) - An index to the collection of all subset definitions in the schema
 * [text](text.md) - The actual permissible value itself
 * [title](title.md) - A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
 * [todos](todos.md) - Outstanding issues that needs resolution
 * [tree_root](tree_root.md) - Indicates that this is the Container class which forms the root of the serialized document structure in tree serializations
 * [type_definition➞uri](type_uri.md) - The uri that defines the possible values for the type definition
 * [typeof](typeof.md) - A parent type from which type properties are inherited
 * [types](types.md) - An index to the collection of all type definitions in the schema
 * [unique_key_name](unique_key_name.md) - name of the unique key
 * [unique_key_slots](unique_key_slots.md) - list of slot names that form a key. The tuple formed from the values of all these slots should be unique.
 * [unique_keys](unique_keys.md) - A collection of named unique keys for this class. Unique keys may be singular or compound.
 * [value](value.md) - example value
 * [example➞description](value_description.md) - description of what the value is doing
 * [example➞object](value_object.md) - direct object representation of the example
 * [version](version.md) - particular version of schema

### Types


### Enums

 * [Uriorcurie](types/Uriorcurie.md) - a URI or a CURIE
