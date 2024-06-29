
# meta


**metamodel version:** 1.7.0

**version:** None


The metamodel for schemas defined using the Linked Data Modeling Language framework.

For more information on LinkML:

* [linkml.io](https://linkml.io) main website
* [specification](https://w3id.org/linkml/docs/specification/)

LinkML is self-describing. Every LinkML schema consists of elements
that instantiate classes in this metamodel.

Core metaclasses:

* [SchemaDefinition](https://w3id.org/linkml/SchemaDefinition)
* [ClassDefinition](https://w3id.org/linkml/ClassDefinition)
* [SlotDefinition](https://w3id.org/linkml/SlotDefinition)
* [TypeDefinition](https://w3id.org/linkml/TypeDefinition)

There are many subsets of *profiles* of the metamodel, for different purposes:

* [MinimalSubset](https://w3id.org/linkml/MinimalSubset)
* [BasicSubset](https://w3id.org/linkml/BasicSubset)

For canonical reference documentation on any metamodel construct,
refer to the official URI for each construct, e.g.
[https://w3id.org/linkml/is_a](https://w3id.org/linkml/is_a)


### Classes

 * [AnyValue](AnyValue.md)
 * [Anything](Anything.md)
 * [UnitOfMeasure](UnitOfMeasure.md) - A unit of measure, or unit, is a particular quantity value that has been chosen as a scale for  measuring other quantities the same kind (more generally of equivalent dimension).
 * [AltDescription](AltDescription.md) - an attributed description
 * [AnonymousEnumExpression](AnonymousEnumExpression.md) - An enum_expression that is not named
 * [AnonymousExpression](AnonymousExpression.md) - An abstract parent class for any nested expression
     * [AnonymousClassExpression](AnonymousClassExpression.md)
     * [AnonymousSlotExpression](AnonymousSlotExpression.md)
 * [AnonymousTypeExpression](AnonymousTypeExpression.md) - A type expression that is not a top-level named type definition. Used for nesting.
 * [ArrayExpression](ArrayExpression.md) - defines the dimensions of an array
 * [ClassLevelRule](ClassLevelRule.md) - A rule that is applied to classes
     * [ClassRule](ClassRule.md) - A rule that applies to instances of a class
 * [DimensionExpression](DimensionExpression.md) - defines one of the dimensions of an array
 * [Element](Element.md) - A named element in the model
     * [Definition](Definition.md) - abstract base class for core metaclasses
         * [ClassDefinition](ClassDefinition.md) - an element whose instances are complex objects that may have slot-value assignments
         * [EnumDefinition](EnumDefinition.md) - an element whose instances must be drawn from a specified set of permissible values
         * [SlotDefinition](SlotDefinition.md) - an element that describes how instances are related to other instances
     * [SchemaDefinition](SchemaDefinition.md) - A collection of definitions that make up a schema or a data model.
     * [SubsetDefinition](SubsetDefinition.md) - an element that can be used to group other metamodel elements
     * [TypeDefinition](TypeDefinition.md) - an element that whose instances are atomic scalar values that can be mapped to primitive types
 * [EnumBinding](EnumBinding.md) - A binding of a slot or a class to a permissible value from an enumeration.
 * [Example](Example.md) - usage example and description
 * [Extension](Extension.md) - a tag/value pair used to add non-model information to an entry
     * [Annotation](Annotation.md) - a tag/value pair with the semantics of OWL Annotation
 * [ImportExpression](ImportExpression.md) - an expression describing an import
 * [LocalName](LocalName.md) - an attributed label
 * [MatchQuery](MatchQuery.md) - A query that is used on an enum expression to dynamically obtain a set of permissivle values via a query that  matches on properties of the external concepts.
 * [PathExpression](PathExpression.md) - An expression that describes an abstract path from an object to another through a sequence of slot lookups
 * [PatternExpression](PatternExpression.md) - a regular expression pattern used to evaluate conformance of a string
 * [PermissibleValue](PermissibleValue.md) - a permissible value, accompanied by intended text and an optional mapping to a concept URI
 * [Prefix](Prefix.md) - prefix URI tuple
 * [ReachabilityQuery](ReachabilityQuery.md) - A query that is used on an enum expression to dynamically obtain a set of permissible values via walking from a  set of source nodes to a set of descendants or ancestors over a set of relationship types.
 * [Setting](Setting.md) - assignment of a key to a value
 * [StructuredAlias](StructuredAlias.md) - object that contains meta data about a synonym or alias including where it came from (source) and its scope (narrow, broad, etc.)
 * [TypeMapping](TypeMapping.md) - Represents how a slot or type can be serialized to a format.
 * [UniqueKey](UniqueKey.md) - a collection of slots whose values uniquely identify an instance of a class

### Mixins

 * [Annotatable](Annotatable.md) - mixin for classes that support annotations
 * [ClassExpression](ClassExpression.md) - A boolean expression that can be used to dynamically determine membership of a class
 * [CommonMetadata](CommonMetadata.md) - Generic metadata shared across definitions
 * [Expression](Expression.md) - general mixin for any class that can represent some form of expression
     * [EnumExpression](EnumExpression.md) - An expression that constrains the range of a slot
     * [SlotExpression](SlotExpression.md) - an expression that constrains the range of values a slot can take
     * [TypeExpression](TypeExpression.md) - An abstract class grouping named types and anonymous type expressions
 * [Extensible](Extensible.md) - mixin for classes that support extension
 * [SlotExpression](SlotExpression.md) - an expression that constrains the range of values a slot can take
 * [TypeExpression](TypeExpression.md) - An abstract class grouping named types and anonymous type expressions

### Slots

 * [abbreviation](abbreviation.md) - An abbreviation for a unit is a short ASCII string that is used in place of the full name for the unit in  contexts where non-ASCII characters would be problematic, or where using the abbreviation will enhance  readability. When a power of a base unit needs to be expressed, such as squares this can be done using  abbreviations rather than symbols (source: qudt)
 * [abstract](abstract.md) - Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.
 * [alias](alias.md) - the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.
 * [structured_alias➞contexts](alias_contexts.md) - The context in which an alias should be applied
 * [structured_alias➞predicate](alias_predicate.md) - The relationship between an element and its alias.
 * [aliases](aliases.md) - Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
 * [alt_description➞source](alt_description_source.md) - the source of an attributed description
 * [alt_description➞description](alt_description_text.md) - text of an attributed description
 * [alt_descriptions](alt_descriptions.md) - A sourced alternative description for an element
 * [apply_to](apply_to.md) - Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
     * [class_definition➞apply_to](class_definition_apply_to.md)
     * [slot_definition➞apply_to](slot_definition_apply_to.md)
 * [array](array.md) - coerces the value of the slot into an array and defines the dimensions of that array
 * [attributes](attributes.md) - Inline definition of slots
 * [base](base.md) - python base type in the LinkML runtime that implements this type definition
 * [bidirectional](bidirectional.md) - in addition to preconditions entailing postconditions, the postconditions entail the preconditions
 * [bindings](bindings.md) - A collection of enum bindings that specify how a slot can be bound to a permissible value from an enumeration.
 * [binds_value_of](binds_value_of.md) - A path to a slot that is being bound to a permissible value from an enumeration.
 * [boolean_slot](boolean_slot.md) - A grouping of slots that expression a boolean operator over a list of operands
     * [all_of](all_of.md) - holds if all of the expressions hold
         * [class_expression➞all_of](class_expression_all_of.md)
         * [path_expression➞all_of](path_expression_all_of.md)
         * [slot_expression➞all_of](slot_expression_all_of.md)
         * [type_expression➞all_of](type_expression_all_of.md)
     * [any_of](any_of.md) - holds if at least one of the expressions hold
         * [class_expression➞any_of](class_expression_any_of.md)
         * [path_expression➞any_of](path_expression_any_of.md)
         * [slot_expression➞any_of](slot_expression_any_of.md)
         * [type_expression➞any_of](type_expression_any_of.md)
     * [exactly_one_of](exactly_one_of.md) - holds if only one of the expressions hold
         * [class_expression➞exactly_one_of](class_expression_exactly_one_of.md)
         * [path_expression➞exactly_one_of](path_expression_exactly_one_of.md)
         * [slot_expression➞exactly_one_of](slot_expression_exactly_one_of.md)
         * [type_expression➞exactly_one_of](type_expression_exactly_one_of.md)
     * [none_of](none_of.md) - holds if none of the expressions hold
         * [class_expression➞none_of](class_expression_none_of.md)
         * [path_expression➞none_of](path_expression_none_of.md)
         * [slot_expression➞none_of](slot_expression_none_of.md)
         * [type_expression➞none_of](type_expression_none_of.md)
 * [categories](categories.md) - Controlled terms used to categorize an element.
     * [structured_alias➞categories](structured_alias_categories.md) - The category or categories of an alias. This can be drawn from any relevant vocabulary
 * [children_are_mutually_disjoint](children_are_mutually_disjoint.md) - If true then all direct is_a children are mutually disjoint and share no instances in common
 * [class_uri](class_uri.md) - URI of the class that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas
 * [classes](classes.md) - An index to the collection of all class definitions in the schema
 * [classification_rules](classification_rules.md) - The collection of classification rules that apply to all members of this class. Classification rules allow for automatically assigning the instantiated type of an instance.
 * [code_set](code_set.md) - the identifier of an enumeration code set.
 * [code_set_tag](code_set_tag.md) - the version tag of the enumeration code set
 * [code_set_version](code_set_version.md) - the version identifier of the enumeration code set
 * [comments](comments.md) - notes and comments about an element intended primarily for external consumption
 * [concepts](concepts.md) - A list of identifiers that are used to construct a set of permissible values
 * [conforms_to](conforms_to.md) - An established standard to which the element conforms.
 * [consider_nulls_inequal](consider_nulls_inequal.md) - By default, None values are considered equal for the purposes of comparisons in determining uniqueness. Set this to true to treat missing values as per ANSI-SQL NULLs, i.e NULL=NULL is always False.
 * [contributors](contributors.md) - agent that contributed to the element
 * [created_by](created_by.md) - agent that created the element
 * [created_on](created_on.md) - time at which the element was created
 * [deactivated](deactivated.md) - a deactivated rule is not executed by the rules engine
 * [default_curi_maps](default_curi_maps.md) - ordered list of prefixcommon biocontexts to be fetched to resolve id prefixes and inline prefix variables
 * [default_prefix](default_prefix.md) - The prefix that is used for all elements within a schema
 * [default_range](default_range.md) - default slot range to be used if range element is omitted from a slot definition
 * [defining_slots](defining_slots.md) - The combination of is a plus defining slots form a genus-differentia definition, or the set of necessary and sufficient conditions that can be transformed into an OWL equivalence axiom
 * [definition_uri](definition_uri.md) - The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri
 * [deprecated](deprecated.md) - Description of why and when this element will no longer be used
 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md) - When an element is deprecated, it can be automatically replaced by this uri or curie
 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md) - When an element is deprecated, it can be potentially replaced by this uri or curie
 * [derivation](derivation.md) - Expression for deriving this unit from other units
 * [description](description.md) - a textual description of the element's purpose and use
 * [descriptive_name](descriptive_name.md) - the spelled out name of the unit, for example, meter
 * [designates_type](designates_type.md) - True means that the key slot(s) is used to determine the instantiation (types) relation between objects and a ClassDefinition
 * [dimensions](dimensions.md) - definitions of each axis in the array
 * [disjoint_with](disjoint_with.md) - Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances
     * [class_definition➞disjoint_with](class_definition_disjoint_with.md)
     * [slot_definition➞disjoint_with](slot_definition_disjoint_with.md)
 * [domain](domain.md) - defines the type of the subject of the slot.  Given the following slot definition
 * [domain_of](domain_of.md) - the class(es) that reference the slot in a "slots" or "slot_usage" context
 * [elseconditions](elseconditions.md) - an expression that must hold for an instance of the class, if the preconditions no not hold
 * [emit_prefixes](emit_prefixes.md) - a list of Curie prefixes that are used in the representation of instances of the model.  All prefixes in this list are added to the prefix sections of the target models.
 * [enum_range](enum_range.md) - An inlined enumeration
 * [enum_uri](enum_uri.md) - URI of the enum that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas
 * [enums](enums.md) - An index to the collection of all enum definitions in the schema
 * [exact_number_dimensions](exact_number_dimensions.md) - exact number of dimensions in the array
 * [examples](examples.md) - example usages of an element
 * [extension➞tag](extension_tag.md) - a tag associated with an extension
 * [extension➞value](extension_value.md) - the actual annotation
 * [extensions](extensions.md) - a tag/text tuple attached to an arbitrary element
     * [annotations](annotations.md) - a collection of tag/text tuples with the semantics of OWL Annotation
 * [followed_by](followed_by.md) - in a sequential list, this indicates the next member
     * [path_expression➞followed_by](path_expression_followed_by.md)
 * [➞framework](framework_key.md) - The name of a format that can be used to serialize LinkML data. The string value should be a code from the LinkML frameworks vocabulary, but this is not strictly enforced
 * [from_schema](from_schema.md) - id of the schema that defined the element
 * [generation_date](generation_date.md) - date and time that the schema was loaded/generated
 * [has_quantity_kind](has_quantity_kind.md) - Concept in a vocabulary or ontology that denotes the kind of quantity being measured, e.g. length
 * [id](id.md) - The official schema URI
 * [id_prefixes](id_prefixes.md) - An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
 * [id_prefixes_are_closed](id_prefixes_are_closed.md) - If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.
 * [identifier](identifier.md) - True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container
 * [identifier_pattern](identifier_pattern.md) - A regular expression that is used to obtain a set of identifiers from a source_ontology to construct a set of permissible values
 * [iec61360code](iec61360code.md)
 * [ifabsent](ifabsent.md) - function that provides a default value for the slot.
 * [implements](implements.md) - An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.
 * [implicit_prefix](implicit_prefix.md) - Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
 * [import_as](import_as.md)
 * [import_from](import_from.md)
 * [import_map](import_map.md)
 * [imported_from](imported_from.md) - the imports entry that this element was derived from.  Empty means primary source
 * [imports](imports.md) - A list of schemas that are to be included in this schema
 * [in_language](in_language.md) - the primary language used in the sources
 * [in_subset](in_subset.md) - used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
 * [inapplicable](inapplicable.md) - true means that values for this slot must not be present
 * [include](include.md) - An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set
 * [include_self](include_self.md) - True if the query is reflexive
 * [inherited](inherited.md) - true means that the *value* of a slot is inherited by subclasses
 * [inherits](inherits.md) - An enum definition that is used as the basis to create a new enum
 * [inlined](inlined.md) - True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
 * [inlined_as_list](inlined_as_list.md) - True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
 * [inlined_as_simple_dict](inlined_as_simple_dict.md) - True means that an inlined slot is represented as a simple dict whose values are all atoms
 * [instantiates](instantiates.md) - An element in another schema which this element instantiates.
 * [interpolated](interpolated.md) - if true then the pattern is first string interpolated
 * [inverse](inverse.md) - indicates that any instance of d s r implies that there is also an instance of r s' d
 * [is_a](is_a.md) - A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
     * [class_definition➞is_a](class_definition_is_a.md) - A primary parent class from which inheritable metaslots are propagated
     * [permissible_value➞is_a](permissible_value_is_a.md)
     * [slot_definition➞is_a](slot_definition_is_a.md) - A primary parent slot from which inheritable metaslots are propagated
 * [is_class_field](is_class_field.md) - indicates that for any instance, i, the domain of this slot will include an assertion of i s range
 * [is_direct](is_direct.md) - True if the reachability query should only include directly related nodes, if False then include also transitively connected
 * [is_grouping_slot](is_grouping_slot.md) - true if this slot is a grouping slot
 * [is_usage_slot](is_usage_slot.md) - True means that this slot was defined in a slot_usage situation
 * [key](key.md) - True means that the key slot(s) uniquely identify the elements within a single container
 * [keywords](keywords.md) - Keywords or tags used to describe the element
 * [last_updated_on](last_updated_on.md) - time at which the element was last updated
 * [license](license.md) - license for the schema
 * [list_elements_ordered](list_elements_ordered.md) - If True, then the order of elements of a multivalued slot is guaranteed to be preserved. If False, the order may still be preserved but this is not guaranteed
 * [list_elements_unique](list_elements_unique.md) - If True, then there must be no duplicates in the elements of a multivalued slot
 * [list_value_specification_constant](list_value_specification_constant.md) - Grouping for metamodel slots that constrain members of a multivalued slot value to equal a specified constant
     * [all_members](all_members.md) - the value of the slot is multivalued with all members satisfying the condition
     * [equals_expression](equals_expression.md) - the value of the slot must equal the value of the evaluated expression
     * [equals_number](equals_number.md) - the slot must have range of a number and the value of the slot must equal the specified value
     * [equals_number_in](equals_number_in.md) - the slot must have range number and the value of the slot must equal one of the specified values
     * [equals_string](equals_string.md) - the slot must have range string and the value of the slot must equal the specified value
     * [equals_string_in](equals_string_in.md) - the slot must have range string and the value of the slot must equal one of the specified values
     * [exact_cardinality](exact_cardinality.md) - the exact number of entries for a multivalued slot
     * [has_member](has_member.md) - the value of the slot is multivalued with at least one member satisfying the condition
     * [maximum_cardinality](maximum_cardinality.md) - the maximum number of entries for a multivalued slot
     * [minimum_cardinality](minimum_cardinality.md) - the minimum number of entries for a multivalued slot
     * [value_presence](value_presence.md) - if PRESENT then a value must be present (for lists there must be at least one value). If ABSENT then a value must be absent (for lists, must be empty)
 * [literal_form](literal_form.md) - The literal lexical form of a structured alias; i.e the actual alias value.
 * [local_name_source](local_name_source.md) - the ncname of the source of the name
 * [local_name_value](local_name_value.md) - a name assigned to an element in a given ontology
 * [local_names](local_names.md)
 * [➞type](mapped_type.md) - type to coerce to
 * [mappings](mappings.md) - A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * [broad mappings](broad_mappings.md) - A list of terms from different schemas or terminology systems that have broader meaning.
     * [close mappings](close_mappings.md) - A list of terms from different schemas or terminology systems that have close meaning.
     * [exact mappings](exact_mappings.md) - A list of terms from different schemas or terminology systems that have identical meaning.
         * [UnitOfMeasure➞exact mappings](UnitOfMeasure_exact_mappings.md) - Used to link a unit to equivalent concepts in ontologies such as UO, SNOMED, OEM, OBOE, NCIT
     * [narrow mappings](narrow_mappings.md) - A list of terms from different schemas or terminology systems that have narrower meaning.
     * [related mappings](related_mappings.md) - A list of terms from different schemas or terminology systems that have related meaning.
 * [matches](matches.md) - Specifies a match query that is used to calculate the list of permissible values
 * [maximum_number_dimensions](maximum_number_dimensions.md) - maximum number of dimensions in the array, or False if explicitly no maximum. If this is unset, and an explicit list of dimensions are passed using dimensions, then this is interpreted as a closed list and the maximum_number_dimensions is the length of the dimensions list, unless this value is set to False
 * [maximum_value](maximum_value.md) - For ordinal ranges, the value must be equal to or lower than this
 * [meaning](meaning.md) - the value meaning of a permissible value
 * [metamodel_version](metamodel_version.md) - Version of the metamodel used to load the schema
 * [minimum_number_dimensions](minimum_number_dimensions.md) - minimum number of dimensions in the array
 * [minimum_value](minimum_value.md) - For ordinal ranges, the value must be equal to or higher than this
 * [minus](minus.md) - An enum expression that yields a list of permissible values that are to be subtracted from the enum
 * [mixin](mixin.md) - Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.
 * [mixins](mixins.md) - A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.
     * [class_definition➞mixins](class_definition_mixins.md) - A collection of secondary parent mixin classes from which inheritable metaslots are propagated
     * [permissible_value➞mixins](permissible_value_mixins.md)
     * [slot_definition➞mixins](slot_definition_mixins.md) - A collection of secondary parent mixin slots from which inheritable metaslots are propagated
 * [modified_by](modified_by.md) - agent that modified the element
 * [multivalued](multivalued.md) - true means that slot can have more than one value and should be represented using a list or collection structure.
 * [name](name.md) - the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * [schema_definition➞name](schema_definition_name.md) - a unique name for the schema that is both human-readable and consists of only characters from the NCName set
 * [notes](notes.md) - editorial notes about an element intended primarily for internal consumption
 * [obligation_level](obligation_level.md) - The level of obligation or recommendation strength for a metadata element
 * [open_world](open_world.md) - if true, the the postconditions may be omitted in instance data, but it is valid for an inference engine to add these
 * [owned_by](owned_by.md) - agent that owns or is the steward of the element
 * [owner](owner.md) - the "owner" of the slot. It is the class if it appears in the slots list, otherwise the declaring slot
 * [partial_match](partial_match.md) - if not true then the pattern must match the whole string, as if enclosed in ^...$
 * [path_rule](path_rule.md) - a rule for inferring a slot assignment based on evaluating a path through a sequence of slot assignments
 * [pattern](pattern.md) - the string value of the slot must conform to this regular expression expressed in the string
 * [permissible_values](permissible_values.md) - A list of possible values for a slot range
 * [postconditions](postconditions.md) - an expression that must hold for an instance of the class, if the preconditions hold
 * [preconditions](preconditions.md) - an expression that must hold in order for the rule to be applicable to an instance
 * [prefix_prefix](prefix_prefix.md) - The prefix components of a prefix expansions. This is the part that appears before the colon in a CURIE.
 * [prefix_reference](prefix_reference.md) - The namespace to which a prefix expands to.
 * [prefixes](prefixes.md) - A collection of prefix expansions that specify how CURIEs can be expanded to URIs
 * [publisher](publisher.md) - An entity responsible for making the resource available
 * [pv_formula](pv_formula.md) - Defines the specific formula to be used to generate the permissible values.
 * [range](range.md) - defines the type of the object of the slot.  Given the following slot definition
     * [enum_binding➞range](enum_binding_range.md)
 * [range_expression](range_expression.md) - A range that is described as a boolean expression combining existing ranges
 * [rank](rank.md) - the relative order in which the element occurs, lower values are given precedence
 * [reachable_from](reachable_from.md) - Specifies a query for obtaining a list of permissible values based on graph reachability
 * [readonly](readonly.md) - If present, slot is read only.  Text explains why
 * [recommended](recommended.md) - true means that the slot should be present in instances of the class definition, but this is not required
 * [relational_logical_characteristic](relational_logical_characteristic.md) - An abstract grouping for metaslots that describe logical properties of a slot
     * [asymmetric](asymmetric.md) - If s is antisymmetric, and i.s=v where i is different from v, v.s cannot have value i
     * [irreflexive](irreflexive.md) - If s is irreflexive, then there exists no i such i.s=i
     * [locally_reflexive](locally_reflexive.md) - If s is locally_reflexive, then i.s=i for all instances i where s is a class slot for the type of i
     * [reflexive](reflexive.md) - If s is reflexive, then i.s=i for all instances i
     * [symmetric](symmetric.md) - If s is symmetric, and i.s=v, then v.s=i
     * [transitive](transitive.md) - If s is transitive, and i.s=z, and s.s=j, then i.s=j
 * [relational_role](relational_role.md) - the role a slot on a relationship class plays, for example, the subject, object or predicate roles
 * [relationship_types](relationship_types.md) - A list of relationship types (properties) that are used in a reachability query
 * [repr](repr.md) - the name of the python object that implements this type definition
 * [represents_relationship](represents_relationship.md) - true if this class represents a relationship rather than an entity
 * [required](required.md) - true means that the slot must be present in instances of the class definition
 * [reversed](reversed.md) - true if the slot is to be inversed
 * [role](role.md) - a textual descriptor that indicates the role played by the slot range
 * [rules](rules.md) - the collection of rules that apply to all members of this class
     * [class_definition➞rules](class_definition_rules.md)
 * [see_also](see_also.md) - A list of related entities or URLs that may be of relevance
 * [setting_key](setting_key.md) - the variable name for a setting
 * [setting_value](setting_value.md) - The value assigned for a setting
 * [settings](settings.md) - A collection of global variable settings
 * [shared](shared.md) - If True, then the relationship between the slot domain and range is many to one or many to many
 * [singular_name](singular_name.md) - a name that is used in the singular form
 * [slot_conditions](slot_conditions.md) - expresses constraints on a group of slots for a class expression
 * [schema_definition➞slots](slot_definitions.md) - An index to the collection of all slot definitions in the schema
 * [slot_group](slot_group.md) - allows for grouping of related slots into a grouping slot that serves the role of a group
 * [slot_names_unique](slot_names_unique.md) - if true then induced/mangled slot names are not created for class_usage and attributes
 * [slot_uri](slot_uri.md) - URI of the class that provides a semantic interpretation of the slot in a linked data context. The URI may come from any namespace and may be shared between schemas.
 * [slot_usage](slot_usage.md) - the refinement of a slot in the context of the containing class definition.
 * [slots](slots.md) - collection of slot names that are applicable to a class
 * [source](source.md) - A related resource from which the element is derived.
 * [source_file](source_file.md) - name, uri or description of the source of the schema
 * [source_file_date](source_file_date.md) - modification date of the source of the schema
 * [source_file_size](source_file_size.md) - size in bytes of the source of the schema
 * [source_nodes](source_nodes.md) - A list of nodes that are used in the reachability query
 * [source_ontology](source_ontology.md) - An ontology or vocabulary or terminology that is used in a query to obtain a set of permissible values
 * [status](status.md) - status of the element
 * [string_serialization](string_serialization.md) - Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
 * [structured_aliases](structured_aliases.md) - A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.
 * [structured_imports](structured_imports.md) - A list of specifications for how to import elements from external schemas
 * [structured_pattern](structured_pattern.md) - the string value of the slot must conform to the regular expression in the pattern expression
 * [subclass_of](subclass_of.md) - DEPRECATED -- rdfs:subClassOf to be emitted in OWL generation
 * [subproperty_of](subproperty_of.md) - Ontology property which this slot is a subproperty of.  Note: setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
 * [subsets](subsets.md) - An index to the collection of all subset definitions in the schema
 * [symbol](symbol.md) - name of the unit encoded as a symbol
 * [syntax](syntax.md) - the string value of the slot must conform to this regular expression expressed in the string. May be interpolated.
 * [text](text.md) - The actual permissible value itself
 * [title](title.md) - A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
 * [todos](todos.md) - Outstanding issues that needs resolution
 * [transitive_form_of](transitive_form_of.md) - If s transitive_form_of d, then (1) s holds whenever d holds (2) s is transitive (3) d holds whenever s holds and there are no intermediates, and s is not reflexive
     * [reflexive_transitive_form_of](reflexive_transitive_form_of.md) - transitive_form_of including the reflexive case
 * [traverse](traverse.md) - the slot to traverse
 * [traverse_up](traverse_up.md) - True if the direction of the reachability query is reversed and ancestors are retrieved
 * [tree_root](tree_root.md) - Indicates that this is the Container class which forms the root of the serialized document structure in tree serializations
 * [type_mappings](type_mappings.md) - A collection of type mappings that specify how a slot's range should be mapped or serialized in different frameworks
 * [type_definition➞uri](type_uri.md) - The uri that defines the possible values for the type definition
 * [typeof](typeof.md) - A parent type from which type properties are inherited
 * [types](types.md) - An index to the collection of all type definitions in the schema
 * [ucum_code](ucum_code.md) - associates a QUDT unit with its UCUM code (case-sensitive).
 * [union_of](union_of.md) - indicates that the domain element consists exactly of the members of the element in the range.
     * [class_definition➞union_of](class_definition_union_of.md)
     * [slot_definition➞union_of](slot_definition_union_of.md)
     * [type_definition➞union_of](type_definition_union_of.md)
 * [unique_key_name](unique_key_name.md) - name of the unique key
 * [unique_key_slots](unique_key_slots.md) - list of slot names that form a key. The tuple formed from the values of all these slots should be unique.
 * [unique_keys](unique_keys.md) - A collection of named unique keys for this class. Unique keys may be singular or compound.
 * [unit](unit.md) - an encoding of a unit
 * [usage_slot_name](usage_slot_name.md) - The name of the slot referenced in the slot_usage
 * [value](value.md) - example value
 * [example➞description](value_description.md) - description of what the value is doing
 * [example➞object](value_object.md) - direct object representation of the example
 * [value_specification_constant](value_specification_constant.md) - Grouping for metamodel slots that constrain the a slot value to equal a specified constant
 * [values_from](values_from.md) - The identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
 * [version](version.md) - particular version of schema

### Enums

 * [alias_predicate_enum](alias_predicate_enum.md) - permissible values for the relationship between an element and an alias
 * [obligation_level_enum](obligation_level_enum.md) - The level of obligation or recommendation strength for a metadata element
 * [presence_enum](presence_enum.md) - enumeration of conditions by which a slot value should be set
 * [pv_formula_options](pv_formula_options.md) - The formula used to generate the set of permissible values from the code_set values
 * [relational_role_enum](relational_role_enum.md) - enumeration of roles a slot on a relationship class can play

### Subsets

 * [BasicSubset](BasicSubset.md) - An extension of MinimalSubset that avoids advanced constructs and can be implemented by a broad variety of tools.
 * [MinimalSubset](MinimalSubset.md) - The absolute minimal set of elements necessary for defining any schema.
 * [ObjectOrientedProfile](ObjectOrientedProfile.md) - A profile that includes all the metamodel elements whose semantics can be expressed using a minimal
 * [OwlProfile](OwlProfile.md) - A profile that includes all the metamodel elements whose semantics can be expressed in OWL
 * [RelationalModelProfile](RelationalModelProfile.md) - A profile that includes all the metamodel elements whose semantics can be expressed using the classic Relational Model.
 * [SpecificationSubset](SpecificationSubset.md) - A subset that includes all the metamodel elements that form part of the normative LinkML specification.

### Types


#### Built in

 * **Bool**
 * **Curie**
 * **Decimal**
 * **ElementIdentifier**
 * **NCName**
 * **NodeIdentifier**
 * **URI**
 * **URIorCURIE**
 * **XSDDate**
 * **XSDDateTime**
 * **XSDTime**
 * **float**
 * **int**
 * **str**

#### Defined

 * [Boolean](types/Boolean.md)  (**Bool**)  - A binary (true or false) value
 * [Curie](types/Curie.md)  (**Curie**)  - a compact URI
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [DateOrDatetime](types/DateOrDatetime.md)  (**str**)  - Either a date or a datetime
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Decimal](types/Decimal.md)  (**Decimal**)  - A real number with arbitrary precision that conforms to the xsd:decimal specification
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [Jsonpath](types/Jsonpath.md)  (**str**)  - A string encoding a JSON Path. The value of the string MUST conform to JSON Point syntax and SHOULD dereference to zero or more valid objects within the current instance document when encoded in tree form.
 * [Jsonpointer](types/Jsonpointer.md)  (**str**)  - A string encoding a JSON Pointer. The value of the string MUST conform to JSON Point syntax and SHOULD dereference to a valid object within the current instance document when encoded in tree form.
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [Sparqlpath](types/Sparqlpath.md)  (**str**)  - A string encoding a SPARQL Property Path. The value of the string MUST conform to SPARQL syntax and SHOULD dereference to zero or more valid objects within the current instance document when encoded as RDF.
 * [String](types/String.md)  (**str**)  - A character string
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
