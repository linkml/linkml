
# Subset: basic


An extension of minimal that is a basic subset that can be implemented by a broad variety of tools

URI: [linkml:basic](https://w3id.org/linkml/basic)


### Classes

 * [AltDescription](AltDescription.md) - an attributed description
 * [ClassDefinition](ClassDefinition.md) - the definition of a class or interface
 * [Definition](Definition.md) - base class for definitions
 * [Element](Element.md) - a named element in the model
 * [EnumDefinition](EnumDefinition.md) - List of values that constrain the range of a slot
 * [Example](Example.md) - usage example and description
 * [PermissibleValue](PermissibleValue.md) - a permissible value, accompanied by intended text and an optional mapping to a concept URI
 * [Prefix](Prefix.md) - prefix URI tuple
 * [SchemaDefinition](SchemaDefinition.md) - a collection of subset, type, slot and class definitions
 * [SlotDefinition](SlotDefinition.md) - the definition of a property or a slot
 * [SubsetDefinition](SubsetDefinition.md) - the name and description of a subset
 * [TypeDefinition](TypeDefinition.md) - A data type definition.
 * [UniqueKey](UniqueKey.md) - a collection of slots whose values uniquely identify an instance of a class

### Mixins

 * [CommonMetadata](CommonMetadata.md) - Generic metadata shared across definitions

### Slots

 * [abstract](abstract.md) - an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
 * [aliases](aliases.md)
 * [alt_description➞source](alt_description_source.md) - the source of an attributed description
 * [alt_description➞description](alt_description_text.md) - text of an attributed description
 * [alt_descriptions](alt_descriptions.md)
 * [attributes](attributes.md) - Inline definition of slots
 * [base](base.md) - python base type that implements this type definition
 * [categories](categories.md) - controlled terms used to categorize an element
 * [class_definition➞is_a](class_definition_is_a.md)
 * [class_definition➞mixins](class_definition_mixins.md)
 * [class_uri](class_uri.md) - URI of the class in an RDF environment
 * [classes](classes.md) - class definitions
 * [code_set](code_set.md) - the identifier of an enumeration code set.
 * [code_set_tag](code_set_tag.md) - the version tag of the enumeration code set
 * [code_set_version](code_set_version.md) - the version identifier of the enumeration code set
 * [comments](comments.md) - notes and comments about an element intended for external consumption
 * [conforms_to](conforms_to.md) - An established standard to which the element conforms.
 * [created_by](created_by.md) - agent that created the element
 * [created_on](created_on.md) - time at which the element was created
 * [default_curi_maps](default_curi_maps.md) - ordered list of prefixcommon biocontexts to be fetched to resolve id prefixes and inline prefix variables
 * [default_prefix](default_prefix.md) - default and base prefix -- used for ':' identifiers, @base and @vocab
 * [default_range](default_range.md) - default slot range to be used if range element is omitted from a slot definition
 * [deprecated](deprecated.md) - Description of why and when this element will no longer be used
 * [description](description.md) - a description of the element's purpose and use
 * [enums](enums.md) - enumerated ranges
 * [examples](examples.md) - example usages of an element
 * [generation_date](generation_date.md) - date and time that the schema was loaded/generated
 * [id](id.md) - The official schema URI
 * [id_prefixes](id_prefixes.md) - the identifier of this class or slot must begin with the URIs referenced by this prefix
 * [identifier](identifier.md) - True means that the key slot(s) uniquely identify the container. There can be at most one identifier or key per container
 * [imports](imports.md) - other schemas that are included in this schema
 * [in_subset](in_subset.md) - used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
 * [inlined](inlined.md) - True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
 * [inlined_as_list](inlined_as_list.md) - True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
 * [is_a](is_a.md) - specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
 * [is_grouping_slot](is_grouping_slot.md) - true if this slot is a grouping slot
 * [key](key.md) - True means that the key slot(s) uniquely identify the container.
 * [keywords](keywords.md) - Keywords or tags used to describe the element
 * [last_updated_on](last_updated_on.md) - time at which the element was last updated
 * [license](license.md) - license for the schema
 * [maximum_value](maximum_value.md) - for slots with ranges of type number, the value must be equal to or lowe than this
 * [meaning](meaning.md) - the value meaning of a permissible value
 * [metamodel_version](metamodel_version.md) - Version of the metamodel used to load the schema
 * [minimum_value](minimum_value.md) - for slots with ranges of type number, the value must be equal to or higher than this
 * [mixin](mixin.md) - this slot or class can only be used as a mixin.
 * [mixins](mixins.md) - List of definitions to be mixed in. Targets may be any definition of the same type
 * [modified_by](modified_by.md) - agent that modified the element
 * [multivalued](multivalued.md) - true means that slot can have more than one value
 * [name](name.md) - the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
 * [notes](notes.md) - editorial notes about an element intended for internal consumption
 * [owned_by](owned_by.md) - agent that owns or is the steward of the element
 * [pattern](pattern.md) - the string value of the slot must conform to this regular expression expressed in the string
 * [permissible_value➞is_a](permissible_value_is_a.md)
 * [permissible_value➞mixins](permissible_value_mixins.md)
 * [permissible_values](permissible_values.md) - A list of possible values for a slot range
 * [prefix_prefix](prefix_prefix.md) - the nsname (sans ':' for a given prefix)
 * [prefix_reference](prefix_reference.md) - A URI associated with a given prefix
 * [prefixes](prefixes.md) - prefix / URI definitions to be added to the context beyond those fetched from prefixcommons in id prefixes
 * [pv_formula](pv_formula.md) - Defines the specific formula to be used to generate the permissible values.
 * [range](range.md) - defines the type of the object of the slot.  Given the following slot definition
 * [rank](rank.md) - the relative order in which the element occurs, lower values are given precedence
 * [recommended](recommended.md) - true means that the slot should be present in the loaded definition, but this is not required
 * [repr](repr.md) - the name of the python object that implements this type definition
 * [required](required.md) - true means that the slot must be present in the loaded definition
 * [schema_definition➞name](schema_definition_name.md)
 * [see_also](see_also.md) - a reference
 * [singular_name](singular_name.md) - a name that is used in the singular form
 * [slot_definition➞is_a](slot_definition_is_a.md)
 * [slot_definition➞mixins](slot_definition_mixins.md)
 * [schema_definition➞slots](slot_definitions.md) - slot definitions
 * [slot_group](slot_group.md) - allows for grouping of related slots into a grouping slot that serves the role of a group
 * [slot_uri](slot_uri.md) - predicate of this slot for semantic web application
 * [slot_usage](slot_usage.md) - the redefinition of a slot in the context of the containing class definition.
 * [slots](slots.md) - list of slot names that are applicable to a class
 * [source](source.md) - A related resource from which the element is derived.
 * [source_file](source_file.md) - name, uri or description of the source of the schema
 * [source_file_date](source_file_date.md) - modification date of the source of the schema
 * [source_file_size](source_file_size.md) - size in bytes of the source of the schema
 * [status](status.md) - status of the element
 * [structured_alias➞categories](structured_alias_categories.md) - The category or categories of an alias. This can be drawn from any relevant vocabulary
 * [subsets](subsets.md) - list of subsets referenced in this model
 * [text](text.md)
 * [title](title.md) - the official title of the element
 * [todos](todos.md) - Outstanding issue that needs resolution
 * [tree_root](tree_root.md) - indicator that this is the root class in tree structures
 * [type_definition➞uri](type_uri.md) - The uri that defines the possible values for the type definition
 * [typeof](typeof.md) - Names a parent type
 * [types](types.md) - data types used in the model
 * [unique_key_name](unique_key_name.md) - name of the unique key
 * [unique_key_slots](unique_key_slots.md) - list of slot names that form a key
 * [unique_keys](unique_keys.md) - Set of unique keys for this slot
 * [value](value.md) - example value
 * [example➞description](value_description.md) - description of what the value is doing
 * [version](version.md) - particular version of schema

### Types


### Enums

 * [Uriorcurie](types/Uriorcurie.md) - a URI or a CURIE
