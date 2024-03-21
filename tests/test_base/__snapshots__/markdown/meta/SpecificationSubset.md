
# Subset: SpecificationSubset


A subset that includes all the metamodel elements that form part of the normative LinkML specification.

The complete LinkML specification can be found at [linkml:specification](https://w3id.org/linkml/specification)

URI: [linkml:SpecificationSubset](https://w3id.org/linkml/SpecificationSubset)


### Classes

 * [ClassDefinition](ClassDefinition.md) - an element whose instances are complex objects that may have slot-value assignments
 * [ClassRule](ClassRule.md) - A rule that applies to instances of a class
 * [EnumDefinition](EnumDefinition.md) - an element whose instances must be drawn from a specified set of permissible values
 * [MatchQuery](MatchQuery.md) - A query that is used on an enum expression to dynamically obtain a set of permissivle values via a query that  matches on properties of the external concepts.
 * [PermissibleValue](PermissibleValue.md) - a permissible value, accompanied by intended text and an optional mapping to a concept URI
 * [Prefix](Prefix.md) - prefix URI tuple
 * [ReachabilityQuery](ReachabilityQuery.md) - A query that is used on an enum expression to dynamically obtain a set of permissible values via walking from a  set of source nodes to a set of descendants or ancestors over a set of relationship types.
 * [SchemaDefinition](SchemaDefinition.md) - A collection of definitions that make up a schema or a data model.
 * [Setting](Setting.md) - assignment of a key to a value
 * [SlotDefinition](SlotDefinition.md) - an element that describes how instances are related to other instances
 * [SubsetDefinition](SubsetDefinition.md) - an element that can be used to group other metamodel elements
 * [TypeDefinition](TypeDefinition.md) - an element that whose instances are atomic scalar values that can be mapped to primitive types
 * [UniqueKey](UniqueKey.md) - a collection of slots whose values uniquely identify an instance of a class

### Mixins


### Slots

 * [abstract](abstract.md) - Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.
 * [alias](alias.md) - the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.
 * [all_members](all_members.md) - the value of the slot is multivalued with all members satisfying the condition
 * [all_of](all_of.md) - holds if all of the expressions hold
 * [any_of](any_of.md) - holds if at least one of the expressions hold
 * [asymmetric](asymmetric.md) - If s is antisymmetric, and i.s=v where i is different from v, v.s cannot have value i
 * [attributes](attributes.md) - Inline definition of slots
 * [base](base.md) - python base type in the LinkML runtime that implements this type definition
 * [bidirectional](bidirectional.md) - in addition to preconditions entailing postconditions, the postconditions entail the preconditions
 * [class_definition➞disjoint_with](class_definition_disjoint_with.md)
 * [class_definition➞is_a](class_definition_is_a.md) - A primary parent class from which inheritable metaslots are propagated
 * [class_definition➞mixins](class_definition_mixins.md) - A collection of secondary parent mixin classes from which inheritable metaslots are propagated
 * [class_definition➞rules](class_definition_rules.md)
 * [class_definition➞union_of](class_definition_union_of.md)
 * [class_expression➞all_of](class_expression_all_of.md)
 * [class_expression➞any_of](class_expression_any_of.md)
 * [class_expression➞exactly_one_of](class_expression_exactly_one_of.md)
 * [class_expression➞none_of](class_expression_none_of.md)
 * [class_uri](class_uri.md) - URI of the class that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas
 * [classes](classes.md) - An index to the collection of all class definitions in the schema
 * [classification_rules](classification_rules.md) - The collection of classification rules that apply to all members of this class. Classification rules allow for automatically assigning the instantiated type of an instance.
 * [code_set](code_set.md) - the identifier of an enumeration code set.
 * [concepts](concepts.md) - A list of identifiers that are used to construct a set of permissible values
 * [default_prefix](default_prefix.md) - The prefix that is used for all elements within a schema
 * [default_range](default_range.md) - default slot range to be used if range element is omitted from a slot definition
 * [designates_type](designates_type.md) - True means that the key slot(s) is used to determine the instantiation (types) relation between objects and a ClassDefinition
 * [disjoint_with](disjoint_with.md) - Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances
 * [domain](domain.md) - defines the type of the subject of the slot.  Given the following slot definition
 * [elseconditions](elseconditions.md) - an expression that must hold for an instance of the class, if the preconditions no not hold
 * [enum_range](enum_range.md) - An inlined enumeration
 * [enum_uri](enum_uri.md) - URI of the enum that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas
 * [enums](enums.md) - An index to the collection of all enum definitions in the schema
 * [equals_expression](equals_expression.md) - the value of the slot must equal the value of the evaluated expression
 * [equals_number_in](equals_number_in.md) - the slot must have range number and the value of the slot must equal one of the specified values
 * [equals_string](equals_string.md) - the slot must have range string and the value of the slot must equal the specified value
 * [equals_string_in](equals_string_in.md) - the slot must have range string and the value of the slot must equal one of the specified values
 * [exact_cardinality](exact_cardinality.md) - the exact number of entries for a multivalued slot
 * [exactly_one_of](exactly_one_of.md) - holds if only one of the expressions hold
 * [from_schema](from_schema.md) - id of the schema that defined the element
 * [has_member](has_member.md) - the value of the slot is multivalued with at least one member satisfying the condition
 * [id](id.md) - The official schema URI
 * [id_prefixes](id_prefixes.md) - An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
 * [identifier](identifier.md) - True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container
 * [identifier_pattern](identifier_pattern.md) - A regular expression that is used to obtain a set of identifiers from a source_ontology to construct a set of permissible values
 * [ifabsent](ifabsent.md) - function that provides a default value for the slot.  Possible values for this slot are defined in linkml.utils.ifabsent_functions.default_library:
 * [implicit_prefix](implicit_prefix.md) - Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
 * [imports](imports.md) - A list of schemas that are to be included in this schema
 * [inapplicable](inapplicable.md) - true means that values for this slot must not be present
 * [include](include.md) - An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set
 * [include_self](include_self.md) - True if the query is reflexive
 * [inherited](inherited.md) - true means that the *value* of a slot is inherited by subclasses
 * [inherits](inherits.md) - An enum definition that is used as the basis to create a new enum
 * [inlined](inlined.md) - True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
 * [inlined_as_list](inlined_as_list.md) - True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
 * [inlined_as_simple_dict](inlined_as_simple_dict.md) - True means that an inlined slot is represented as a simple dict whose values are all atoms
 * [interpolated](interpolated.md) - if true then the pattern is first string interpolated
 * [inverse](inverse.md) - indicates that any instance of d s r implies that there is also an instance of r s' d
 * [irreflexive](irreflexive.md) - If s is irreflexive, then there exists no i such i.s=i
 * [is_a](is_a.md) - A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
 * [is_direct](is_direct.md) - True if the reachability query should only include directly related nodes, if False then include also transitively connected
 * [is_grouping_slot](is_grouping_slot.md) - true if this slot is a grouping slot
 * [key](key.md) - True means that the key slot(s) uniquely identify the elements within a single container
 * [list_elements_ordered](list_elements_ordered.md) - If True, then the order of elements of a multivalued slot is guaranteed to be preserved. If False, the order may still be preserved but this is not guaranteed
 * [list_elements_unique](list_elements_unique.md) - If True, then there must be no duplicates in the elements of a multivalued slot
 * [locally_reflexive](locally_reflexive.md) - If s is locally_reflexive, then i.s=i for all instances i where s is a class slot for the type of i
 * [matches](matches.md) - Specifies a match query that is used to calculate the list of permissible values
 * [maximum_cardinality](maximum_cardinality.md) - the maximum number of entries for a multivalued slot
 * [maximum_value](maximum_value.md) - For ordinal ranges, the value must be equal to or lower than this
 * [meaning](meaning.md) - the value meaning of a permissible value
 * [minimum_cardinality](minimum_cardinality.md) - the minimum number of entries for a multivalued slot
 * [minimum_value](minimum_value.md) - For ordinal ranges, the value must be equal to or higher than this
 * [minus](minus.md) - An enum expression that yields a list of permissible values that are to be subtracted from the enum
 * [mixin](mixin.md) - Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.
 * [mixins](mixins.md) - A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.
 * [multivalued](multivalued.md) - true means that slot can have more than one value and should be represented using a list or collection structure.
 * [name](name.md) - the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
 * [none_of](none_of.md) - holds if none of the expressions hold
 * [open_world](open_world.md) - if true, the the postconditions may be omitted in instance data, but it is valid for an inference engine to add these
 * [partial_match](partial_match.md) - if not true then the pattern must match the whole string, as if enclosed in ^...$
 * [path_expression➞all_of](path_expression_all_of.md)
 * [path_expression➞any_of](path_expression_any_of.md)
 * [path_expression➞exactly_one_of](path_expression_exactly_one_of.md)
 * [path_expression➞none_of](path_expression_none_of.md)
 * [pattern](pattern.md) - the string value of the slot must conform to this regular expression expressed in the string
 * [permissible_value➞is_a](permissible_value_is_a.md)
 * [permissible_value➞mixins](permissible_value_mixins.md)
 * [permissible_values](permissible_values.md) - A list of possible values for a slot range
 * [postconditions](postconditions.md) - an expression that must hold for an instance of the class, if the preconditions hold
 * [preconditions](preconditions.md) - an expression that must hold in order for the rule to be applicable to an instance
 * [prefix_prefix](prefix_prefix.md) - The prefix components of a prefix expansions. This is the part that appears before the colon in a CURIE.
 * [prefix_reference](prefix_reference.md) - The namespace to which a prefix expands to.
 * [prefixes](prefixes.md) - A collection of prefix expansions that specify how CURIEs can be expanded to URIs
 * [pv_formula](pv_formula.md) - Defines the specific formula to be used to generate the permissible values.
 * [range](range.md) - defines the type of the object of the slot.  Given the following slot definition
 * [range_expression](range_expression.md) - A range that is described as a boolean expression combining existing ranges
 * [rank](rank.md) - the relative order in which the element occurs, lower values are given precedence
 * [reachable_from](reachable_from.md) - Specifies a query for obtaining a list of permissible values based on graph reachability
 * [recommended](recommended.md) - true means that the slot should be present in instances of the class definition, but this is not required
 * [reflexive](reflexive.md) - If s is reflexive, then i.s=i for all instances i
 * [reflexive_transitive_form_of](reflexive_transitive_form_of.md) - transitive_form_of including the reflexive case
 * [relationship_types](relationship_types.md) - A list of relationship types (properties) that are used in a reachability query
 * [repr](repr.md) - the name of the python object that implements this type definition
 * [required](required.md) - true means that the slot must be present in instances of the class definition
 * [rules](rules.md) - the collection of rules that apply to all members of this class
 * [schema_definition➞name](schema_definition_name.md) - a unique name for the schema that is both human-readable and consists of only characters from the NCName set
 * [setting_key](setting_key.md) - the variable name for a setting
 * [setting_value](setting_value.md) - The value assigned for a setting
 * [settings](settings.md) - A collection of global variable settings
 * [shared](shared.md) - If True, then the relationship between the slot domain and range is many to one or many to many
 * [slot_conditions](slot_conditions.md) - expresses constraints on a group of slots for a class expression
 * [slot_definition➞disjoint_with](slot_definition_disjoint_with.md)
 * [slot_definition➞is_a](slot_definition_is_a.md) - A primary parent slot from which inheritable metaslots are propagated
 * [slot_definition➞mixins](slot_definition_mixins.md) - A collection of secondary parent mixin slots from which inheritable metaslots are propagated
 * [slot_definition➞union_of](slot_definition_union_of.md)
 * [schema_definition➞slots](slot_definitions.md) - An index to the collection of all slot definitions in the schema
 * [slot_expression➞all_of](slot_expression_all_of.md)
 * [slot_expression➞any_of](slot_expression_any_of.md)
 * [slot_expression➞exactly_one_of](slot_expression_exactly_one_of.md)
 * [slot_expression➞none_of](slot_expression_none_of.md)
 * [slot_group](slot_group.md) - allows for grouping of related slots into a grouping slot that serves the role of a group
 * [slot_uri](slot_uri.md) - URI of the class that provides a semantic interpretation of the slot in a linked data context. The URI may come from any namespace and may be shared between schemas.
 * [slot_usage](slot_usage.md) - the refinement of a slot in the context of the containing class definition.
 * [slots](slots.md) - collection of slot names that are applicable to a class
 * [source_nodes](source_nodes.md) - A list of nodes that are used in the reachability query
 * [source_ontology](source_ontology.md) - An ontology or vocabulary or terminology that is used in a query to obtain a set of permissible values
 * [string_serialization](string_serialization.md) - Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
 * [structured_pattern](structured_pattern.md) - the string value of the slot must conform to the regular expression in the pattern expression
 * [subsets](subsets.md) - An index to the collection of all subset definitions in the schema
 * [symmetric](symmetric.md) - If s is symmetric, and i.s=v, then v.s=i
 * [syntax](syntax.md) - the string value of the slot must conform to this regular expression expressed in the string. May be interpolated.
 * [text](text.md) - The actual permissible value itself
 * [transitive](transitive.md) - If s is transitive, and i.s=z, and s.s=j, then i.s=j
 * [transitive_form_of](transitive_form_of.md) - If s transitive_form_of d, then (1) s holds whenever d holds (2) s is transitive (3) d holds whenever s holds and there are no intermediates, and s is not reflexive
 * [traverse_up](traverse_up.md) - True if the direction of the reachability query is reversed and ancestors are retrieved
 * [tree_root](tree_root.md) - Indicates that this is the Container class which forms the root of the serialized document structure in tree serializations
 * [type_definition➞union_of](type_definition_union_of.md)
 * [type_expression➞all_of](type_expression_all_of.md)
 * [type_expression➞any_of](type_expression_any_of.md)
 * [type_expression➞exactly_one_of](type_expression_exactly_one_of.md)
 * [type_expression➞none_of](type_expression_none_of.md)
 * [type_definition➞uri](type_uri.md) - The uri that defines the possible values for the type definition
 * [typeof](typeof.md) - A parent type from which type properties are inherited
 * [union_of](union_of.md) - indicates that the domain element consists exactly of the members of the element in the range.
 * [unique_key_name](unique_key_name.md) - name of the unique key
 * [unique_key_slots](unique_key_slots.md) - list of slot names that form a key. The tuple formed from the values of all these slots should be unique.
 * [unique_keys](unique_keys.md) - A collection of named unique keys for this class. Unique keys may be singular or compound.

### Types


### Enums

 * [Uriorcurie](types/Uriorcurie.md) - a URI or a CURIE
