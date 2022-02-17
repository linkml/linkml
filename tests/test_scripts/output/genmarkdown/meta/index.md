
# meta


**metamodel version:** 1.7.0

**version:** 2.0.0


A metamodel for defining linked open data schemas


### Classes

 * [AltDescription](AltDescription.md) - an attributed description
 * [AnonymousExpression](AnonymousExpression.md)
     * [AnonymousClassExpression](AnonymousClassExpression.md)
     * [AnonymousSlotExpression](AnonymousSlotExpression.md)
 * [AnonymousTypeExpression](AnonymousTypeExpression.md)
 * [ClassLevelRule](ClassLevelRule.md) - A rule that is applied to classes
     * [ClassRule](ClassRule.md) - A rule that applies to instances of a class
 * [Element](Element.md) - a named element in the model
     * [Definition](Definition.md) - base class for definitions
         * [ClassDefinition](ClassDefinition.md) - the definition of a class or interface
         * [SlotDefinition](SlotDefinition.md) - the definition of a property or a slot
     * [EnumDefinition](EnumDefinition.md) - List of values that constrain the range of a slot
     * [SchemaDefinition](SchemaDefinition.md) - a collection of subset, type, slot and class definitions
     * [SubsetDefinition](SubsetDefinition.md) - the name and description of a subset
     * [TypeDefinition](TypeDefinition.md) - A data type definition.
 * [Example](Example.md) - usage example and description
 * [Extension](Extension.md) - a tag/value pair used to add non-model information to an entry
     * [Annotation](Annotation.md) - a tag/value pair with the semantics of OWL Annotation
 * [LocalName](LocalName.md) - an attributed label
 * [PermissibleValue](PermissibleValue.md) - a permissible value, accompanied by intended text and an optional mapping to a concept URI
 * [Prefix](Prefix.md) - prefix URI tuple
 * [UniqueKey](UniqueKey.md) - a collection of slots whose values uniquely identify an instance of a class

### Mixins

 * [Annotatable](Annotatable.md) - mixin for classes that support annotations
 * [ClassExpression](ClassExpression.md) - A boolean expression that can be used to dynamically determine membership of a class
 * [CommonMetadata](CommonMetadata.md) - Generic metadata shared across definitions
 * [Expression](Expression.md) - todo
     * [SlotExpression](SlotExpression.md) - an expression that constrains the range of values a slot can take
     * [TypeExpression](TypeExpression.md)
 * [Extensible](Extensible.md) - mixin for classes that support extension
 * [SlotExpression](SlotExpression.md) - an expression that constrains the range of values a slot can take
 * [TypeExpression](TypeExpression.md)

### Slots

 * [abstract](abstract.md) - an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
 * [alias](alias.md) - the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.
 * [aliases](aliases.md)
 * [alt_description➞source](alt_description_source.md) - the source of an attributed description
 * [alt_description➞description](alt_description_text.md) - text of an attributed description
 * [alt_descriptions](alt_descriptions.md)
 * [apply_to](apply_to.md) - Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
     * [class_definition➞apply_to](class_definition_apply_to.md)
     * [slot_definition➞apply_to](slot_definition_apply_to.md)
 * [attributes](attributes.md) - Inline definition of slots
 * [base](base.md) - python base type that implements this type definition
 * [bidirectional](bidirectional.md) - in addition to preconditions entailing postconditions, the postconditions entail the preconditions
 * [boolean_slot](boolean_slot.md) - A grouping of slots that expression a boolean operator over a list of operands
     * [all_of](all_of.md) - holds if all of the expressions hold
         * [class_expression➞all_of](class_expression_all_of.md)
         * [slot_expression➞all_of](slot_expression_all_of.md)
         * [type_expression➞all_of](type_expression_all_of.md)
     * [any_of](any_of.md) - holds if at least one of the expressions hold
         * [class_expression➞any_of](class_expression_any_of.md)
         * [slot_expression➞any_of](slot_expression_any_of.md)
         * [type_expression➞any_of](type_expression_any_of.md)
     * [exactly_one_of](exactly_one_of.md) - holds if only one of the expressions hold
         * [class_expression➞exactly_one_of](class_expression_exactly_one_of.md)
         * [slot_expression➞exactly_one_of](slot_expression_exactly_one_of.md)
         * [type_expression➞exactly_one_of](type_expression_exactly_one_of.md)
     * [none_of](none_of.md) - holds if none of the expressions hold
         * [class_expression➞none_of](class_expression_none_of.md)
         * [slot_expression➞none_of](slot_expression_none_of.md)
         * [type_expression➞none_of](type_expression_none_of.md)
 * [class_uri](class_uri.md) - URI of the class in an RDF environment
 * [classes](classes.md) - class definitions
 * [classification_rules](classification_rules.md) - the collection of classification rules that apply to all members of this class
 * [code_set](code_set.md) - the identifier of an enumeration code set.
 * [code_set_tag](code_set_tag.md) - the version tag of the enumeration code set
 * [code_set_version](code_set_version.md) - the version identifier of the enumeration code set
 * [comments](comments.md) - notes and comments about an element intended for external consumption
 * [conforms_to](conforms_to.md) - An established standard to which the element conforms.
 * [created_by](created_by.md) - agent that created the element
 * [created_on](created_on.md) - time at which the element was created
 * [deactivated](deactivated.md) - a deactivated rule is not executed by the rules engine
 * [default_curi_maps](default_curi_maps.md) - ordered list of prefixcommon biocontexts to be fetched to resolve id prefixes and inline prefix variables
 * [default_prefix](default_prefix.md) - default and base prefix -- used for ':' identifiers, @base and @vocab
 * [default_range](default_range.md) - default slot range to be used if range element is omitted from a slot definition
 * [defining_slots](defining_slots.md) - The combination of is a plus defining slots form a genus-differentia definition, or the set of necessary and sufficient conditions that can be transformed into an OWL equivalence axiom
 * [definition_uri](definition_uri.md) - the "native" URI of the element
 * [deprecated](deprecated.md) - Description of why and when this element will no longer be used
 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md) - When an element is deprecated, it can be automatically replaced by this uri or curie
 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md) - When an element is deprecated, it can be potentially replaced by this uri or curie
 * [description](description.md) - a description of the element's purpose and use
 * [designates_type](designates_type.md) - True means that the key slot(s) is used to determine the instantiation (types) relation between objects and a ClassDefinition
 * [domain](domain.md) - defines the type of the subject of the slot.  Given the following slot definition
 * [domain_of](domain_of.md) - the class(es) that reference the slot in a "slots" or "slot_usage" context
 * [elseconditions](elseconditions.md) - an expression that must hold for an instance of the class, if the preconditions no not hold
 * [emit_prefixes](emit_prefixes.md) - a list of Curie prefixes that are used in the representation of instances of the model.  All prefixes in this list are added to the prefix sections of the target models.
 * [enums](enums.md) - enumerated ranges
 * [examples](examples.md) - example usages of an element
 * [extension➞tag](extension_tag.md) - a tag associated with an extension
 * [extension➞value](extension_value.md) - the actual annotation
 * [extensions](extensions.md) - a tag/text tuple attached to an arbitrary element
     * [annotations](annotations.md) - a collection of tag/text tuples with the semantics of OWL Annotation
 * [from_schema](from_schema.md) - id of the schema that defined the element
 * [generation_date](generation_date.md) - date and time that the schema was loaded/generated
 * [id](id.md) - The official schema URI
 * [id_prefixes](id_prefixes.md) - the identifier of this class or slot must begin with the URIs referenced by this prefix
 * [identifier](identifier.md) - True means that the key slot(s) uniquely identify the container. There can be at most one identifier or key per container
 * [ifabsent](ifabsent.md) - function that provides a default value for the slot.  Possible values for this slot are defined in biolink.utils.ifabsent_functions.default_library:
 * [imported_from](imported_from.md) - the imports entry that this element was derived from.  Empty means primary source
 * [imports](imports.md) - other schemas that are included in this schema
 * [in_subset](in_subset.md) - used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
 * [inherited](inherited.md) - true means that the *value* of a slot is inherited by subclasses
 * [inlined](inlined.md) - True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
 * [inlined_as_list](inlined_as_list.md) - True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
 * [inverse](inverse.md) - indicates that any instance of d s r implies that there is also an instance of r s' d
 * [is_a](is_a.md) - specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
     * [class_definition➞is_a](class_definition_is_a.md)
     * [permissible_value➞is_a](permissible_value_is_a.md)
     * [slot_definition➞is_a](slot_definition_is_a.md)
 * [is_class_field](is_class_field.md) - indicates that any instance, i,  the domain of this slot will include an assert of i s range
 * [is_usage_slot](is_usage_slot.md) - True means that this slot was defined in a slot_usage situation
 * [key](key.md) - True means that the key slot(s) uniquely identify the container.
 * [last_updated_on](last_updated_on.md) - time at which the element was last updated
 * [license](license.md) - license for the schema
 * [list_value_specification_constant](list_value_specification_constant.md) - Grouping for metamodel slots that constrain members of a multivalued slot value to equal a specified constant
     * [all_members](all_members.md) - the value of the multiavlued slot is a list where all elements conform to the specified values.
     * [equals_number_in](equals_number_in.md) - the slot must have range number and the value of the slot must equal one of the specified values
     * [equals_string_in](equals_string_in.md) - the slot must have range string and the value of the slot must equal one of the specified values
     * [has_member](has_member.md) - the values of the slot is multivalued with at least one member satisfying the condition
 * [local_name_source](local_name_source.md) - the ncname of the source of the name
 * [local_name_value](local_name_value.md) - a name assigned to an element in a given ontology
 * [local_names](local_names.md)
 * [mappings](mappings.md) - A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * [broad mappings](broad_mappings.md) - A list of terms from different schemas or terminology systems that have broader meaning.
     * [close mappings](close_mappings.md) - A list of terms from different schemas or terminology systems that have close meaning.
     * [exact mappings](exact_mappings.md) - A list of terms from different schemas or terminology systems that have identical meaning.
     * [narrow mappings](narrow_mappings.md) - A list of terms from different schemas or terminology systems that have narrower meaning.
     * [related mappings](related_mappings.md) - A list of terms from different schemas or terminology systems that have related meaning.
 * [maximum_value](maximum_value.md) - for slots with ranges of type number, the value must be equal to or lowe than this
 * [meaning](meaning.md) - the value meaning (in the 11179 sense) of a permissible value
 * [metamodel_version](metamodel_version.md) - Version of the metamodel used to load the schema
 * [minimum_value](minimum_value.md) - for slots with ranges of type number, the value must be equal to or higher than this
 * [mixin](mixin.md) - this slot or class can only be used as a mixin.
 * [mixins](mixins.md) - List of definitions to be mixed in. Targets may be any definition of the same type
     * [class_definition➞mixins](class_definition_mixins.md)
     * [permissible_value➞mixins](permissible_value_mixins.md)
     * [slot_definition➞mixins](slot_definition_mixins.md)
 * [modified_by](modified_by.md) - agent that modified the element
 * [multivalued](multivalued.md) - true means that slot can have more than one value
 * [name](name.md) - the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * [schema_definition➞name](schema_definition_name.md)
 * [notes](notes.md) - editorial notes about an element intended for internal consumption
 * [open_world](open_world.md) - if true, the the postconditions may be omitted in instance data, but it is valid for an inference engine to add these
 * [owner](owner.md) - the "owner" of the slot. It is the class if it appears in the slots list, otherwise the declaring slot
 * [pattern](pattern.md) - the string value of the slot must conform to this regular expression
 * [permissible_values](permissible_values.md) - A list of possible values for a slot range
 * [postconditions](postconditions.md) - an expression that must hold for an instance of the class, if the preconditions hold
 * [precedence](precedence.md) - the relative order in which the rule is applied
 * [preconditions](preconditions.md) - an expression that must hold in order for the rule to be applicable to an instance
 * [prefix_prefix](prefix_prefix.md) - the nsname (sans ':' for a given prefix)
 * [prefix_reference](prefix_reference.md) - A URI associated with a given prefix
 * [prefixes](prefixes.md) - prefix / URI definitions to be added to the context beyond those fetched from prefixcommons in id prefixes
 * [pv_formula](pv_formula.md) - Defines the specific formula to be used to generate the permissible values.
 * [range](range.md) - defines the type of the object of the slot.  Given the following slot definition
 * [range_expression](range_expression.md) - A range that is described as a boolean expression combining existing ranges
 * [readonly](readonly.md) - If present, slot is read only.  Text explains why
 * [recommended](recommended.md) - true means that the slot should be present in the loaded definition, but this is not required
 * [repr](repr.md) - the name of the python object that implements this type definition
 * [required](required.md) - true means that the slot must be present in the loaded definition
 * [role](role.md) - the role played by the slot range
 * [rules](rules.md) - the collection of rules that apply to all members of this class
     * [class_definition➞rules](class_definition_rules.md)
 * [see_also](see_also.md) - a reference
 * [singular_name](singular_name.md) - a name that is used in the singular form
 * [slot_conditions](slot_conditions.md) - the redefinition of a slot in the context of the containing class definition.
 * [schema_definition➞slots](slot_definitions.md) - slot definitions
 * [slot_uri](slot_uri.md) - predicate of this slot for semantic web application
 * [slot_usage](slot_usage.md) - the redefinition of a slot in the context of the containing class definition.
 * [slots](slots.md) - list of slot names that are applicable to a class
 * [source_file](source_file.md) - name, uri or description of the source of the schema
 * [source_file_date](source_file_date.md) - modification date of the source of the schema
 * [source_file_size](source_file_size.md) - size in bytes of the source of the schema
 * [status](status.md) - status of the element
 * [string_serialization](string_serialization.md) - Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
 * [subclass_of](subclass_of.md) - rdfs:subClassOf to be emitted in OWL generation
 * [subproperty_of](subproperty_of.md) - Ontology property which this slot is a subproperty of
 * [subsets](subsets.md) - list of subsets referenced in this model
 * [symmetric](symmetric.md) - True means that any instance of  d s r implies that there is also an instance of r s d
 * [text](text.md)
 * [title](title.md) - the official title of the element
 * [todos](todos.md) - Outstanding issue that needs resolution
 * [tree_root](tree_root.md) - indicator that this is the root class in tree structures
 * [type_definition➞uri](type_uri.md) - The uri that defines the possible values for the type definition
 * [typeof](typeof.md) - Names a parent type
 * [types](types.md) - data types used in the model
 * [union_of](union_of.md) - indicates that the domain class consists exactly of the members of the classes in the range
 * [unique_key_slots](unique_key_slots.md) - list of slot names that form a key
 * [unique_keys](unique_keys.md) - Set of unique keys for this slot
 * [usage_slot_name](usage_slot_name.md) - The name of the slot referenced in the slot_usage
 * [value](value.md) - example value
 * [example➞description](value_description.md) - description of what the value is doing
 * [value_specification_constant](value_specification_constant.md) - Grouping for metamodel slots that constrain the a slot value to equal a specified constant
     * [equals_expression](equals_expression.md) - the value of the slot must equal the value of the evaluated expression
     * [equals_number](equals_number.md) - the slot must have range of a number and the value of the slot must equal the specified value
     * [equals_string](equals_string.md) - the slot must have range string and the value of the slot must equal the specified value
     * [maximum_cardinality](maximum_cardinality.md) - the maximum number of entries for a multivalued slot
     * [minimum_cardinality](minimum_cardinality.md) - the minimum number of entries for a multivalued slot
     * [value_presence](value_presence.md) - if true then a value must be present (for lists there must be at least one value). If false then a value must be absent (for lists, must be empty)
 * [values_from](values_from.md) - the identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot
 * [version](version.md) - particular version of schema

### Enums

 * [presence_enum](presence_enum.md) - enumeration of conditions by which a slot value should be set
 * [pv_formula_options](pv_formula_options.md) - The formula used to generate the set of permissible values from the code_set values

### Subsets

 * [Owl](Owl.md) - Set of slots that appear in the OWL representation of a model

### Types


#### Built in

 * **Bool**
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
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Decimal](types/Decimal.md)  (**Decimal**)  - A real number with arbitrary precision that conforms to the xsd:decimal specification
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [String](types/String.md)  (**str**)  - A character string
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
