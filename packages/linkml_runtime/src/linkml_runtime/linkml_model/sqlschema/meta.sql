-- # Class: Anything
--     * Slot: id
-- # Class: common_metadata Description: Generic metadata shared across definitions
--     * Slot: id
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Abstract Class: element Description: A named element in the model
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: id_prefixes_are_closed Description: If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.
--     * Slot: definition_uri Description: The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: schema_definition Description: A collection of definitions that make up a schema or a data model.
--     * Slot: id Description: The official schema URI
--     * Slot: version Description: particular version of schema
--     * Slot: license Description: license for the schema
--     * Slot: default_prefix Description: The prefix that is used for all elements within a schema
--     * Slot: default_range Description: default slot range to be used if range element is omitted from a slot definition
--     * Slot: metamodel_version Description: Version of the metamodel used to load the schema
--     * Slot: source_file Description: name, uri or description of the source of the schema
--     * Slot: source_file_date Description: modification date of the source of the schema
--     * Slot: source_file_size Description: size in bytes of the source of the schema
--     * Slot: generation_date Description: date and time that the schema was loaded/generated
--     * Slot: slot_names_unique Description: if true then induced/mangled slot names are not created for class_usage and attributes
--     * Slot: name Description: a unique name for the schema that is both human-readable and consists of only characters from the NCName set
--     * Slot: id_prefixes_are_closed Description: If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.
--     * Slot: definition_uri Description: The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: type_expression Description: An abstract class grouping named types and anonymous type expressions
--     * Slot: id
--     * Slot: pattern Description: the string value of the slot must conform to this regular expression expressed in the string
--     * Slot: implicit_prefix Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
--     * Slot: equals_string Description: the slot must have range string and the value of the slot must equal the specified value
--     * Slot: equals_number Description: the slot must have range of a number and the value of the slot must equal the specified value
--     * Slot: structured_pattern_id Description: the string value of the slot must conform to the regular expression in the pattern expression
--     * Slot: unit_id Description: an encoding of a unit
--     * Slot: minimum_value_id Description: For ordinal ranges, the value must be equal to or higher than this
--     * Slot: maximum_value_id Description: For ordinal ranges, the value must be equal to or lower than this
-- # Class: anonymous_type_expression Description: A type expression that is not a top-level named type definition. Used for nesting.
--     * Slot: id
--     * Slot: pattern Description: the string value of the slot must conform to this regular expression expressed in the string
--     * Slot: implicit_prefix Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
--     * Slot: equals_string Description: the slot must have range string and the value of the slot must equal the specified value
--     * Slot: equals_number Description: the slot must have range of a number and the value of the slot must equal the specified value
--     * Slot: structured_pattern_id Description: the string value of the slot must conform to the regular expression in the pattern expression
--     * Slot: unit_id Description: an encoding of a unit
--     * Slot: minimum_value_id Description: For ordinal ranges, the value must be equal to or higher than this
--     * Slot: maximum_value_id Description: For ordinal ranges, the value must be equal to or lower than this
-- # Class: type_definition Description: an element that whose instances are atomic scalar values that can be mapped to primitive types
--     * Slot: typeof Description: A parent type from which type properties are inherited
--     * Slot: base Description: python base type in the LinkML runtime that implements this type definition
--     * Slot: uri Description: The uri that defines the possible values for the type definition
--     * Slot: repr Description: the name of the python object that implements this type definition
--     * Slot: pattern Description: the string value of the slot must conform to this regular expression expressed in the string
--     * Slot: implicit_prefix Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
--     * Slot: equals_string Description: the slot must have range string and the value of the slot must equal the specified value
--     * Slot: equals_number Description: the slot must have range of a number and the value of the slot must equal the specified value
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: id_prefixes_are_closed Description: If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.
--     * Slot: definition_uri Description: The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: structured_pattern_id Description: the string value of the slot must conform to the regular expression in the pattern expression
--     * Slot: unit_id Description: an encoding of a unit
--     * Slot: minimum_value_id Description: For ordinal ranges, the value must be equal to or higher than this
--     * Slot: maximum_value_id Description: For ordinal ranges, the value must be equal to or lower than this
-- # Class: subset_definition Description: an element that can be used to group other metamodel elements
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: id_prefixes_are_closed Description: If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.
--     * Slot: definition_uri Description: The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: schema_definition_name Description: Autocreated FK slot
-- # Abstract Class: definition Description: abstract base class for core metaclasses
--     * Slot: is_a Description: A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
--     * Slot: abstract Description: Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.
--     * Slot: mixin Description: Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.
--     * Slot: string_serialization Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERATE: implement automated to_string labeling of complex objectsFor example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: id_prefixes_are_closed Description: If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.
--     * Slot: definition_uri Description: The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: enum_expression Description: An expression that constrains the range of a slot
--     * Slot: id
--     * Slot: code_set Description: the identifier of an enumeration code set.
--     * Slot: code_set_tag Description: the version tag of the enumeration code set
--     * Slot: code_set_version Description: the version identifier of the enumeration code set
--     * Slot: pv_formula Description: Defines the specific formula to be used to generate the permissible values.
--     * Slot: reachable_from_id Description: Specifies a query for obtaining a list of permissible values based on graph reachability
--     * Slot: matches_id Description: Specifies a match query that is used to calculate the list of permissible values
-- # Class: anonymous_enum_expression Description: An enum_expression that is not named
--     * Slot: id
--     * Slot: code_set Description: the identifier of an enumeration code set.
--     * Slot: code_set_tag Description: the version tag of the enumeration code set
--     * Slot: code_set_version Description: the version identifier of the enumeration code set
--     * Slot: pv_formula Description: Defines the specific formula to be used to generate the permissible values.
--     * Slot: reachable_from_id Description: Specifies a query for obtaining a list of permissible values based on graph reachability
--     * Slot: matches_id Description: Specifies a match query that is used to calculate the list of permissible values
-- # Class: enum_definition Description: an element whose instances must be drawn from a specified set of permissible values
--     * Slot: enum_uri Description: URI of the enum that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas
--     * Slot: code_set Description: the identifier of an enumeration code set.
--     * Slot: code_set_tag Description: the version tag of the enumeration code set
--     * Slot: code_set_version Description: the version identifier of the enumeration code set
--     * Slot: pv_formula Description: Defines the specific formula to be used to generate the permissible values.
--     * Slot: is_a Description: A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
--     * Slot: abstract Description: Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.
--     * Slot: mixin Description: Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.
--     * Slot: string_serialization Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERATE: implement automated to_string labeling of complex objectsFor example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: id_prefixes_are_closed Description: If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.
--     * Slot: definition_uri Description: The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: reachable_from_id Description: Specifies a query for obtaining a list of permissible values based on graph reachability
--     * Slot: matches_id Description: Specifies a match query that is used to calculate the list of permissible values
-- # Class: enum_binding Description: A binding of a slot or a class to a permissible value from an enumeration.
--     * Slot: id
--     * Slot: range Description: defines the type of the object of the slot.  Given the following slot definition  S1:    domain: C1    range:  C2the declaration  X:    S1: Yimplicitly asserts Y is an instance of C2
--     * Slot: obligation_level Description: The level of obligation or recommendation strength for a metadata element
--     * Slot: binds_value_of Description: A path to a slot that is being bound to a permissible value from an enumeration.
--     * Slot: pv_formula Description: Defines the specific formula to be used to generate the permissible values.
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: slot_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
-- # Class: match_query Description: A query that is used on an enum expression to dynamically obtain a set of permissivle values via a query that  matches on properties of the external concepts.
--     * Slot: id
--     * Slot: identifier_pattern Description: A regular expression that is used to obtain a set of identifiers from a source_ontology to construct a set of permissible values
--     * Slot: source_ontology Description: An ontology or vocabulary or terminology that is used in a query to obtain a set of permissible values
-- # Class: reachability_query Description: A query that is used on an enum expression to dynamically obtain a set of permissible values via walking from a  set of source nodes to a set of descendants or ancestors over a set of relationship types.
--     * Slot: id
--     * Slot: source_ontology Description: An ontology or vocabulary or terminology that is used in a query to obtain a set of permissible values
--     * Slot: is_direct Description: True if the reachability query should only include directly related nodes, if False then include also transitively connected
--     * Slot: include_self Description: True if the query is reflexive
--     * Slot: traverse_up Description: True if the direction of the reachability query is reversed and ancestors are retrieved
-- # Class: structured_alias Description: object that contains meta data about a synonym or alias including where it came from (source) and its scope (narrow, broad, etc.)
--     * Slot: id
--     * Slot: literal_form Description: The literal lexical form of a structured alias; i.e the actual alias value.
--     * Slot: predicate Description: The relationship between an element and its alias.
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: type_mapping_framework Description: Autocreated FK slot
-- # Abstract Class: expression Description: general mixin for any class that can represent some form of expression
--     * Slot: id
-- # Abstract Class: anonymous_expression Description: An abstract parent class for any nested expression
--     * Slot: id
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: path_expression Description: An expression that describes an abstract path from an object to another through a sequence of slot lookups
--     * Slot: id
--     * Slot: reversed Description: true if the slot is to be inversed
--     * Slot: traverse Description: the slot to traverse
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: followed_by_id Description: in a sequential list, this indicates the next member
--     * Slot: range_expression_id Description: A range that is described as a boolean expression combining existing ranges
-- # Class: slot_expression Description: an expression that constrains the range of values a slot can take
--     * Slot: id
--     * Slot: range Description: defines the type of the object of the slot.  Given the following slot definition  S1:    domain: C1    range:  C2the declaration  X:    S1: Yimplicitly asserts Y is an instance of C2
--     * Slot: required Description: true means that the slot must be present in instances of the class definition
--     * Slot: recommended Description: true means that the slot should be present in instances of the class definition, but this is not required
--     * Slot: multivalued Description: true means that slot can have more than one value and should be represented using a list or collection structure.
--     * Slot: inlined Description: True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
--     * Slot: inlined_as_list Description: True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
--     * Slot: pattern Description: the string value of the slot must conform to this regular expression expressed in the string
--     * Slot: implicit_prefix Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
--     * Slot: value_presence Description: if PRESENT then a value must be present (for lists there must be at least one value). If ABSENT then a value must be absent (for lists, must be empty)
--     * Slot: equals_string Description: the slot must have range string and the value of the slot must equal the specified value
--     * Slot: equals_number Description: the slot must have range of a number and the value of the slot must equal the specified value
--     * Slot: equals_expression Description: the value of the slot must equal the value of the evaluated expression
--     * Slot: exact_cardinality Description: the exact number of entries for a multivalued slot
--     * Slot: minimum_cardinality Description: the minimum number of entries for a multivalued slot
--     * Slot: maximum_cardinality Description: the maximum number of entries for a multivalued slot
--     * Slot: range_expression_id Description: A range that is described as a boolean expression combining existing ranges
--     * Slot: enum_range_id Description: An inlined enumeration
--     * Slot: minimum_value_id Description: For ordinal ranges, the value must be equal to or higher than this
--     * Slot: maximum_value_id Description: For ordinal ranges, the value must be equal to or lower than this
--     * Slot: structured_pattern_id Description: the string value of the slot must conform to the regular expression in the pattern expression
--     * Slot: unit_id Description: an encoding of a unit
--     * Slot: has_member_id Description: the value of the slot is multivalued with at least one member satisfying the condition
--     * Slot: all_members_id Description: the value of the slot is multivalued with all members satisfying the condition
--     * Slot: array_id Description: coerces the value of the slot into an array and defines the dimensions of that array
-- # Class: anonymous_slot_expression
--     * Slot: id
--     * Slot: range Description: defines the type of the object of the slot.  Given the following slot definition  S1:    domain: C1    range:  C2the declaration  X:    S1: Yimplicitly asserts Y is an instance of C2
--     * Slot: required Description: true means that the slot must be present in instances of the class definition
--     * Slot: recommended Description: true means that the slot should be present in instances of the class definition, but this is not required
--     * Slot: multivalued Description: true means that slot can have more than one value and should be represented using a list or collection structure.
--     * Slot: inlined Description: True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
--     * Slot: inlined_as_list Description: True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
--     * Slot: pattern Description: the string value of the slot must conform to this regular expression expressed in the string
--     * Slot: implicit_prefix Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
--     * Slot: value_presence Description: if PRESENT then a value must be present (for lists there must be at least one value). If ABSENT then a value must be absent (for lists, must be empty)
--     * Slot: equals_string Description: the slot must have range string and the value of the slot must equal the specified value
--     * Slot: equals_number Description: the slot must have range of a number and the value of the slot must equal the specified value
--     * Slot: equals_expression Description: the value of the slot must equal the value of the evaluated expression
--     * Slot: exact_cardinality Description: the exact number of entries for a multivalued slot
--     * Slot: minimum_cardinality Description: the minimum number of entries for a multivalued slot
--     * Slot: maximum_cardinality Description: the maximum number of entries for a multivalued slot
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: range_expression_id Description: A range that is described as a boolean expression combining existing ranges
--     * Slot: enum_range_id Description: An inlined enumeration
--     * Slot: minimum_value_id Description: For ordinal ranges, the value must be equal to or higher than this
--     * Slot: maximum_value_id Description: For ordinal ranges, the value must be equal to or lower than this
--     * Slot: structured_pattern_id Description: the string value of the slot must conform to the regular expression in the pattern expression
--     * Slot: unit_id Description: an encoding of a unit
--     * Slot: has_member_id Description: the value of the slot is multivalued with at least one member satisfying the condition
--     * Slot: all_members_id Description: the value of the slot is multivalued with all members satisfying the condition
--     * Slot: array_id Description: coerces the value of the slot into an array and defines the dimensions of that array
-- # Class: slot_definition Description: an element that describes how instances are related to other instances
--     * Slot: singular_name Description: a name that is used in the singular form
--     * Slot: domain Description: defines the type of the subject of the slot.  Given the following slot definition  S1:    domain: C1    range:  C2the declaration  X:    S1: Yimplicitly asserts that X is an instance of C1
--     * Slot: slot_uri Description: URI of the class that provides a semantic interpretation of the slot in a linked data context. The URI may come from any namespace and may be shared between schemas.
--     * Slot: inherited Description: true means that the *value* of a slot is inherited by subclasses
--     * Slot: readonly Description: If present, slot is read only.  Text explains why
--     * Slot: ifabsent Description: function that provides a default value for the slot.  * [Tt]rue -- boolean True  * [Ff]alse -- boolean False  * bnode -- blank node identifier  * class_curie -- CURIE for the containing class  * class_uri -- URI for the containing class  * default_ns -- schema default namespace  * default_range -- schema default range  * int(value) -- integer value  * slot_uri -- URI for the slot  * slot_curie -- CURIE for the slot  * string(value) -- string value  * EnumName(PermissibleValue) -- enum value
--     * Slot: list_elements_unique Description: If True, then there must be no duplicates in the elements of a multivalued slot
--     * Slot: list_elements_ordered Description: If True, then the order of elements of a multivalued slot is guaranteed to be preserved. If False, the order may still be preserved but this is not guaranteed
--     * Slot: shared Description: If True, then the relationship between the slot domain and range is many to one or many to many
--     * Slot: key Description: True means that the key slot(s) uniquely identify the elements within a single container
--     * Slot: identifier Description: True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container
--     * Slot: designates_type Description: True means that the key slot(s) is used to determine the instantiation (types) relation between objects and a ClassDefinition
--     * Slot: alias Description: the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.
--     * Slot: owner Description: the "owner" of the slot. It is the class if it appears in the slots list, otherwise the declaring slot
--     * Slot: subproperty_of Description: Ontology property which this slot is a subproperty of.  Note: setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
--     * Slot: symmetric Description: If s is symmetric, and i.s=v, then v.s=i
--     * Slot: reflexive Description: If s is reflexive, then i.s=i for all instances i
--     * Slot: locally_reflexive Description: If s is locally_reflexive, then i.s=i for all instances i where s is a class slot for the type of i
--     * Slot: irreflexive Description: If s is irreflexive, then there exists no i such i.s=i
--     * Slot: asymmetric Description: If s is antisymmetric, and i.s=v where i is different from v, v.s cannot have value i
--     * Slot: transitive Description: If s is transitive, and i.s=z, and s.s=j, then i.s=j
--     * Slot: inverse Description: indicates that any instance of d s r implies that there is also an instance of r s' d
--     * Slot: is_class_field Description: indicates that for any instance, i, the domain of this slot will include an assertion of i s range
--     * Slot: transitive_form_of Description: If s transitive_form_of d, then (1) s holds whenever d holds (2) s is transitive (3) d holds whenever s holds and there are no intermediates, and s is not reflexive
--     * Slot: reflexive_transitive_form_of Description: transitive_form_of including the reflexive case
--     * Slot: role Description: a textual descriptor that indicates the role played by the slot range
--     * Slot: is_usage_slot Description: True means that this slot was defined in a slot_usage situation
--     * Slot: usage_slot_name Description: The name of the slot referenced in the slot_usage
--     * Slot: relational_role Description: the role a slot on a relationship class plays, for example, the subject, object or predicate roles
--     * Slot: slot_group Description: allows for grouping of related slots into a grouping slot that serves the role of a group
--     * Slot: is_grouping_slot Description: true if this slot is a grouping slot
--     * Slot: children_are_mutually_disjoint Description: If true then all direct is_a children are mutually disjoint and share no instances in common
--     * Slot: range Description: defines the type of the object of the slot.  Given the following slot definition  S1:    domain: C1    range:  C2the declaration  X:    S1: Yimplicitly asserts Y is an instance of C2
--     * Slot: required Description: true means that the slot must be present in instances of the class definition
--     * Slot: recommended Description: true means that the slot should be present in instances of the class definition, but this is not required
--     * Slot: multivalued Description: true means that slot can have more than one value and should be represented using a list or collection structure.
--     * Slot: inlined Description: True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
--     * Slot: inlined_as_list Description: True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
--     * Slot: pattern Description: the string value of the slot must conform to this regular expression expressed in the string
--     * Slot: implicit_prefix Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
--     * Slot: value_presence Description: if PRESENT then a value must be present (for lists there must be at least one value). If ABSENT then a value must be absent (for lists, must be empty)
--     * Slot: equals_string Description: the slot must have range string and the value of the slot must equal the specified value
--     * Slot: equals_number Description: the slot must have range of a number and the value of the slot must equal the specified value
--     * Slot: equals_expression Description: the value of the slot must equal the value of the evaluated expression
--     * Slot: exact_cardinality Description: the exact number of entries for a multivalued slot
--     * Slot: minimum_cardinality Description: the minimum number of entries for a multivalued slot
--     * Slot: maximum_cardinality Description: the maximum number of entries for a multivalued slot
--     * Slot: is_a Description: A primary parent slot from which inheritable metaslots are propagated
--     * Slot: abstract Description: Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.
--     * Slot: mixin Description: Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.
--     * Slot: string_serialization Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERATE: implement automated to_string labeling of complex objectsFor example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: id_prefixes_are_closed Description: If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.
--     * Slot: definition_uri Description: The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: class_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: path_rule_id Description: a rule for inferring a slot assignment based on evaluating a path through a sequence of slot assignments
--     * Slot: range_expression_id Description: A range that is described as a boolean expression combining existing ranges
--     * Slot: enum_range_id Description: An inlined enumeration
--     * Slot: minimum_value_id Description: For ordinal ranges, the value must be equal to or higher than this
--     * Slot: maximum_value_id Description: For ordinal ranges, the value must be equal to or lower than this
--     * Slot: structured_pattern_id Description: the string value of the slot must conform to the regular expression in the pattern expression
--     * Slot: unit_id Description: an encoding of a unit
--     * Slot: has_member_id Description: the value of the slot is multivalued with at least one member satisfying the condition
--     * Slot: all_members_id Description: the value of the slot is multivalued with all members satisfying the condition
--     * Slot: array_id Description: coerces the value of the slot into an array and defines the dimensions of that array
-- # Class: class_expression Description: A boolean expression that can be used to dynamically determine membership of a class
--     * Slot: id
-- # Class: anonymous_class_expression
--     * Slot: id
--     * Slot: is_a Description: A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: class_definition_name Description: Autocreated FK slot
-- # Class: class_definition Description: an element whose instances are complex objects that may have slot-value assignments
--     * Slot: class_uri Description: URI of the class that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas
--     * Slot: subclass_of Description: DEPRECATED -- rdfs:subClassOf to be emitted in OWL generation
--     * Slot: tree_root Description: Indicates that this is the Container class which forms the root of the serialized document structure in tree serializations
--     * Slot: slot_names_unique Description: if true then induced/mangled slot names are not created for class_usage and attributes
--     * Slot: represents_relationship Description: true if this class represents a relationship rather than an entity
--     * Slot: children_are_mutually_disjoint Description: If true then all direct is_a children are mutually disjoint and share no instances in common
--     * Slot: alias Description: the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.
--     * Slot: is_a Description: A primary parent class from which inheritable metaslots are propagated
--     * Slot: abstract Description: Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.
--     * Slot: mixin Description: Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.
--     * Slot: string_serialization Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERATE: implement automated to_string labeling of complex objectsFor example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: id_prefixes_are_closed Description: If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.
--     * Slot: definition_uri Description: The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: extra_slots_id Description: How a class instance handles extra data not specified in the class definition.Note that this does *not* define the constraints that are placed on additional slots defined by inheriting classes.Possible values:- `allowed: true` - allow all additional data- `allowed: false` (or `allowed:` or `allowed: null` while `range_expression` is `null`) -   forbid all additional data (default) - `range_expression: ...`  - allow additional data if it matches the slot expression (see examples)
-- # Abstract Class: class_level_rule Description: A rule that is applied to classes
--     * Slot: id
-- # Class: class_rule Description: A rule that applies to instances of a class
--     * Slot: id
--     * Slot: bidirectional Description: in addition to preconditions entailing postconditions, the postconditions entail the preconditions
--     * Slot: open_world Description: if true, the the postconditions may be omitted in instance data, but it is valid for an inference engine to add these
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: deactivated Description: a deactivated rule is not executed by the rules engine
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: preconditions_id Description: an expression that must hold in order for the rule to be applicable to an instance
--     * Slot: postconditions_id Description: an expression that must hold for an instance of the class, if the preconditions hold
--     * Slot: elseconditions_id Description: an expression that must hold for an instance of the class, if the preconditions no not hold
-- # Class: array_expression Description: defines the dimensions of an array
--     * Slot: id
--     * Slot: exact_number_dimensions Description: exact number of dimensions in the array
--     * Slot: minimum_number_dimensions Description: minimum number of dimensions in the array
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: maximum_number_dimensions_id Description: maximum number of dimensions in the array, or False if explicitly no maximum. If this is unset, and an explicit list of dimensions are passed using dimensions, then this is interpreted as a closed list and the maximum_number_dimensions is the length of the dimensions list, unless this value is set to False
-- # Class: dimension_expression Description: defines one of the dimensions of an array
--     * Slot: id
--     * Slot: alias Description: the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.
--     * Slot: maximum_cardinality Description: the maximum number of entries for a multivalued slot
--     * Slot: minimum_cardinality Description: the minimum number of entries for a multivalued slot
--     * Slot: exact_cardinality Description: the exact number of entries for a multivalued slot
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: pattern_expression Description: a regular expression pattern used to evaluate conformance of a string
--     * Slot: id
--     * Slot: syntax Description: the string value of the slot must conform to this regular expression expressed in the string. May be interpolated.
--     * Slot: interpolated Description: if true then the pattern is first string interpolated
--     * Slot: partial_match Description: if not true then the pattern must match the whole string, as if enclosed in ^...$
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: import_expression Description: an expression describing an import
--     * Slot: id
--     * Slot: import_from
--     * Slot: import_as
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: setting Description: assignment of a key to a value
--     * Slot: setting_key Description: the variable name for a setting
--     * Slot: setting_value Description: The value assigned for a setting
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: import_expression_id Description: Autocreated FK slot
-- # Class: prefix Description: prefix URI tuple
--     * Slot: prefix_prefix Description: The prefix components of a prefix expansions. This is the part that appears before the colon in a CURIE.
--     * Slot: prefix_reference Description: The namespace to which a prefix expands to.
--     * Slot: schema_definition_name Description: Autocreated FK slot
-- # Class: local_name Description: an attributed label
--     * Slot: local_name_source Description: the ncname of the source of the name
--     * Slot: local_name_value Description: a name assigned to an element in a given ontology
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
-- # Class: example Description: usage example and description
--     * Slot: id
--     * Slot: value Description: example value
--     * Slot: description Description: description of what the value is doing
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: object_id Description: direct object representation of the example
-- # Class: alt_description Description: an attributed description
--     * Slot: source Description: the source of an attributed description
--     * Slot: description Description: text of an attributed description
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: type_mapping_framework Description: Autocreated FK slot
-- # Class: permissible_value Description: a permissible value, accompanied by intended text and an optional mapping to a concept URI
--     * Slot: text Description: The actual permissible value itself
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: meaning Description: the value meaning of a permissible value
--     * Slot: is_a Description: A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: enum_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_enum_expression_id Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: unit_id Description: an encoding of a unit
-- # Class: unique_key Description: a collection of slots whose values uniquely identify an instance of a class
--     * Slot: unique_key_name Description: name of the unique key
--     * Slot: consider_nulls_inequal Description: By default, None values are considered equal for the purposes of comparisons in determining uniqueness. Set this to true to treat missing values as per ANSI-SQL NULLs, i.e NULL=NULL is always False.
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: class_definition_name Description: Autocreated FK slot
-- # Class: type_mapping Description: Represents how a slot or type can be serialized to a format.
--     * Slot: framework Description: The name of a format that can be used to serialize LinkML data. The string value should be a code from the LinkML frameworks vocabulary, but this is not strictly enforced
--     * Slot: type Description: type to coerce to
--     * Slot: string_serialization Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERATE: implement automated to_string labeling of complex objectsFor example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
--     * Slot: description Description: a textual description of the element's purpose and use
--     * Slot: title Description: A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: the primary language used in the sources
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: extra_slots_expression Description: An expression that defines how to handle additional data in an instance of classbeyond the slots/attributes defined for that class. See `extra_slots` for usage examples.
--     * Slot: id
--     * Slot: allowed Description: Whether or not something is allowed. Usage defined by context.
--     * Slot: range_expression_id Description: A range that is described as a boolean expression combining existing ranges
-- # Class: AnyValue
--     * Slot: id
-- # Class: extension Description: a tag/value pair used to add non-model information to an entry
--     * Slot: tag Description: a tag associated with an extension
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: extension_tag Description: Autocreated FK slot
--     * Slot: extensible_id Description: Autocreated FK slot
--     * Slot: annotation_tag Description: Autocreated FK slot
--     * Slot: value_id Description: the actual annotation
-- # Class: extensible Description: mixin for classes that support extension
--     * Slot: id
-- # Class: annotatable Description: mixin for classes that support annotations
--     * Slot: id
-- # Class: annotation Description: a tag/value pair with the semantics of OWL Annotation
--     * Slot: tag Description: a tag associated with an extension
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: annotatable_id Description: Autocreated FK slot
--     * Slot: annotation_tag Description: Autocreated FK slot
--     * Slot: value_id Description: the actual annotation
-- # Class: UnitOfMeasure Description: A unit of measure, or unit, is a particular quantity value that has been chosen as a scale for  measuring other quantities the same kind (more generally of equivalent dimension).
--     * Slot: id
--     * Slot: symbol Description: name of the unit encoded as a symbol
--     * Slot: abbreviation Description: An abbreviation for a unit is a short ASCII string that is used in place of the full name for the unit in  contexts where non-ASCII characters would be problematic, or where using the abbreviation will enhance  readability. When a power of a base unit needs to be expressed, such as squares this can be done using  abbreviations rather than symbols (source: qudt)
--     * Slot: descriptive_name Description: the spelled out name of the unit, for example, meter
--     * Slot: ucum_code Description: associates a QUDT unit with its UCUM code (case-sensitive).
--     * Slot: derivation Description: Expression for deriving this unit from other units
--     * Slot: has_quantity_kind Description: Concept in a vocabulary or ontology that denotes the kind of quantity being measured, e.g. length
--     * Slot: iec61360code
-- # Class: common_metadata_todos
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: common_metadata_notes
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: common_metadata_comments
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: common_metadata_in_subset
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: common_metadata_see_also
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: common_metadata_aliases
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: common_metadata_mappings
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: common_metadata_exact_mappings
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: common_metadata_close_mappings
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: common_metadata_related_mappings
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: common_metadata_narrow_mappings
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: common_metadata_broad_mappings
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: common_metadata_contributors
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: common_metadata_category
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: common_metadata_keyword
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: element_id_prefixes
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: element_implements
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: implements Description: An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.
-- # Class: element_instantiates
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: instantiates Description: An element in another schema which this element instantiates.
-- # Class: element_todos
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: element_notes
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: element_comments
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: element_in_subset
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: element_see_also
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: element_aliases
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: element_mappings
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: element_exact_mappings
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: element_close_mappings
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: element_related_mappings
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: element_narrow_mappings
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: element_broad_mappings
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: element_contributors
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: element_category
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: element_keyword
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: schema_definition_imports
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: imports Description: A list of schemas that are to be included in this schema
-- # Class: schema_definition_emit_prefixes
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: emit_prefixes Description: a list of Curie prefixes that are used in the representation of instances of the model.  All prefixes in this list are added to the prefix sections of the target models.
-- # Class: schema_definition_default_curi_maps
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: default_curi_maps Description: ordered list of prefixcommon biocontexts to be fetched to resolve id prefixes and inline prefix variables
-- # Class: schema_definition_id_prefixes
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: schema_definition_implements
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: implements Description: An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.
-- # Class: schema_definition_instantiates
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: instantiates Description: An element in another schema which this element instantiates.
-- # Class: schema_definition_todos
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: schema_definition_notes
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: schema_definition_comments
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: schema_definition_in_subset
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: schema_definition_see_also
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: schema_definition_aliases
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: schema_definition_mappings
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: schema_definition_exact_mappings
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: schema_definition_close_mappings
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: schema_definition_related_mappings
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: schema_definition_narrow_mappings
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: schema_definition_broad_mappings
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: schema_definition_contributors
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: schema_definition_category
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: schema_definition_keyword
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: type_expression_equals_string_in
--     * Slot: type_expression_id Description: Autocreated FK slot
--     * Slot: equals_string_in Description: the slot must have range string and the value of the slot must equal one of the specified values
-- # Class: type_expression_none_of
--     * Slot: type_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: type_expression_exactly_one_of
--     * Slot: type_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: type_expression_any_of
--     * Slot: type_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: type_expression_all_of
--     * Slot: type_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: anonymous_type_expression_equals_string_in
--     * Slot: anonymous_type_expression_id Description: Autocreated FK slot
--     * Slot: equals_string_in Description: the slot must have range string and the value of the slot must equal one of the specified values
-- # Class: anonymous_type_expression_none_of
--     * Slot: anonymous_type_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: anonymous_type_expression_exactly_one_of
--     * Slot: anonymous_type_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: anonymous_type_expression_any_of
--     * Slot: anonymous_type_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: anonymous_type_expression_all_of
--     * Slot: anonymous_type_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: type_definition_union_of
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: union_of_name Description: indicates that the domain element consists exactly of the members of the element in the range.
-- # Class: type_definition_equals_string_in
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: equals_string_in Description: the slot must have range string and the value of the slot must equal one of the specified values
-- # Class: type_definition_none_of
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: type_definition_exactly_one_of
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: type_definition_any_of
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: type_definition_all_of
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: type_definition_id_prefixes
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: type_definition_implements
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: implements Description: An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.
-- # Class: type_definition_instantiates
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: instantiates Description: An element in another schema which this element instantiates.
-- # Class: type_definition_todos
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: type_definition_notes
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: type_definition_comments
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: type_definition_in_subset
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: type_definition_see_also
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: type_definition_aliases
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: type_definition_mappings
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: type_definition_exact_mappings
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: type_definition_close_mappings
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: type_definition_related_mappings
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: type_definition_narrow_mappings
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: type_definition_broad_mappings
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: type_definition_contributors
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: type_definition_category
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: type_definition_keyword
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: subset_definition_id_prefixes
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: subset_definition_implements
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: implements Description: An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.
-- # Class: subset_definition_instantiates
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: instantiates Description: An element in another schema which this element instantiates.
-- # Class: subset_definition_todos
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: subset_definition_notes
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: subset_definition_comments
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: subset_definition_in_subset
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: subset_definition_see_also
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: subset_definition_aliases
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: subset_definition_mappings
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: subset_definition_exact_mappings
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: subset_definition_close_mappings
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: subset_definition_related_mappings
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: subset_definition_narrow_mappings
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: subset_definition_broad_mappings
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: subset_definition_contributors
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: subset_definition_category
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: subset_definition_keyword
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: definition_mixins
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: mixins_name Description: A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.
-- # Class: definition_apply_to
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: apply_to_name Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
-- # Class: definition_values_from
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: values_from Description: The identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
-- # Class: definition_id_prefixes
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: definition_implements
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: implements Description: An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.
-- # Class: definition_instantiates
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: instantiates Description: An element in another schema which this element instantiates.
-- # Class: definition_todos
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: definition_notes
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: definition_comments
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: definition_in_subset
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: definition_see_also
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: definition_aliases
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: definition_mappings
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: definition_exact_mappings
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: definition_close_mappings
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: definition_related_mappings
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: definition_narrow_mappings
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: definition_broad_mappings
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: definition_contributors
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: definition_category
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: definition_keyword
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: enum_expression_include
--     * Slot: enum_expression_id Description: Autocreated FK slot
--     * Slot: include_id Description: An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set
-- # Class: enum_expression_minus
--     * Slot: enum_expression_id Description: Autocreated FK slot
--     * Slot: minus_id Description: An enum expression that yields a list of permissible values that are to be subtracted from the enum
-- # Class: enum_expression_inherits
--     * Slot: enum_expression_id Description: Autocreated FK slot
--     * Slot: inherits_name Description: An enum definition that is used as the basis to create a new enum
-- # Class: enum_expression_concepts
--     * Slot: enum_expression_id Description: Autocreated FK slot
--     * Slot: concepts Description: A list of identifiers that are used to construct a set of permissible values
-- # Class: anonymous_enum_expression_include
--     * Slot: anonymous_enum_expression_id Description: Autocreated FK slot
--     * Slot: include_id Description: An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set
-- # Class: anonymous_enum_expression_minus
--     * Slot: anonymous_enum_expression_id Description: Autocreated FK slot
--     * Slot: minus_id Description: An enum expression that yields a list of permissible values that are to be subtracted from the enum
-- # Class: anonymous_enum_expression_inherits
--     * Slot: anonymous_enum_expression_id Description: Autocreated FK slot
--     * Slot: inherits_name Description: An enum definition that is used as the basis to create a new enum
-- # Class: anonymous_enum_expression_concepts
--     * Slot: anonymous_enum_expression_id Description: Autocreated FK slot
--     * Slot: concepts Description: A list of identifiers that are used to construct a set of permissible values
-- # Class: enum_definition_include
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: include_id Description: An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set
-- # Class: enum_definition_minus
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: minus_id Description: An enum expression that yields a list of permissible values that are to be subtracted from the enum
-- # Class: enum_definition_inherits
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: inherits_name Description: An enum definition that is used as the basis to create a new enum
-- # Class: enum_definition_concepts
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: concepts Description: A list of identifiers that are used to construct a set of permissible values
-- # Class: enum_definition_mixins
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: mixins_name Description: A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.
-- # Class: enum_definition_apply_to
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: apply_to_name Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
-- # Class: enum_definition_values_from
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: values_from Description: The identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
-- # Class: enum_definition_id_prefixes
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: enum_definition_implements
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: implements Description: An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.
-- # Class: enum_definition_instantiates
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: instantiates Description: An element in another schema which this element instantiates.
-- # Class: enum_definition_todos
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: enum_definition_notes
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: enum_definition_comments
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: enum_definition_in_subset
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: enum_definition_see_also
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: enum_definition_aliases
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: enum_definition_mappings
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: enum_definition_exact_mappings
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: enum_definition_close_mappings
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: enum_definition_related_mappings
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: enum_definition_narrow_mappings
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: enum_definition_broad_mappings
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: enum_definition_contributors
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: enum_definition_category
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: enum_definition_keyword
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: enum_binding_todos
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: enum_binding_notes
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: enum_binding_comments
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: enum_binding_in_subset
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: enum_binding_see_also
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: enum_binding_aliases
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: enum_binding_mappings
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: enum_binding_exact_mappings
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: enum_binding_close_mappings
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: enum_binding_related_mappings
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: enum_binding_narrow_mappings
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: enum_binding_broad_mappings
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: enum_binding_contributors
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: enum_binding_category
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: enum_binding_keyword
--     * Slot: enum_binding_id Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: reachability_query_source_nodes
--     * Slot: reachability_query_id Description: Autocreated FK slot
--     * Slot: source_nodes Description: A list of nodes that are used in the reachability query
-- # Class: reachability_query_relationship_types
--     * Slot: reachability_query_id Description: Autocreated FK slot
--     * Slot: relationship_types Description: A list of relationship types (properties) that are used in a reachability query
-- # Class: structured_alias_category
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: category Description: The category or categories of an alias. This can be drawn from any relevant vocabulary
-- # Class: structured_alias_contexts
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: contexts Description: The context in which an alias should be applied
-- # Class: structured_alias_todos
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: structured_alias_notes
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: structured_alias_comments
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: structured_alias_in_subset
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: structured_alias_see_also
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: structured_alias_aliases
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: structured_alias_mappings
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: structured_alias_exact_mappings
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: structured_alias_close_mappings
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: structured_alias_related_mappings
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: structured_alias_narrow_mappings
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: structured_alias_broad_mappings
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: structured_alias_contributors
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: structured_alias_keyword
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: anonymous_expression_todos
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: anonymous_expression_notes
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: anonymous_expression_comments
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: anonymous_expression_in_subset
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: anonymous_expression_see_also
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: anonymous_expression_aliases
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: anonymous_expression_mappings
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: anonymous_expression_exact_mappings
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: anonymous_expression_close_mappings
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: anonymous_expression_related_mappings
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: anonymous_expression_narrow_mappings
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: anonymous_expression_broad_mappings
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: anonymous_expression_contributors
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: anonymous_expression_category
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: anonymous_expression_keyword
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: path_expression_none_of
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: path_expression_any_of
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: path_expression_all_of
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: path_expression_exactly_one_of
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: path_expression_todos
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: path_expression_notes
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: path_expression_comments
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: path_expression_in_subset
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: path_expression_see_also
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: path_expression_aliases
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: path_expression_mappings
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: path_expression_exact_mappings
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: path_expression_close_mappings
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: path_expression_related_mappings
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: path_expression_narrow_mappings
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: path_expression_broad_mappings
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: path_expression_contributors
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: path_expression_category
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: path_expression_keyword
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: slot_expression_equals_string_in
--     * Slot: slot_expression_id Description: Autocreated FK slot
--     * Slot: equals_string_in Description: the slot must have range string and the value of the slot must equal one of the specified values
-- # Class: slot_expression_none_of
--     * Slot: slot_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: slot_expression_exactly_one_of
--     * Slot: slot_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: slot_expression_any_of
--     * Slot: slot_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: slot_expression_all_of
--     * Slot: slot_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: anonymous_slot_expression_equals_string_in
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: equals_string_in Description: the slot must have range string and the value of the slot must equal one of the specified values
-- # Class: anonymous_slot_expression_none_of
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: anonymous_slot_expression_exactly_one_of
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: anonymous_slot_expression_any_of
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: anonymous_slot_expression_all_of
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: anonymous_slot_expression_todos
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: anonymous_slot_expression_notes
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: anonymous_slot_expression_comments
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: anonymous_slot_expression_in_subset
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: anonymous_slot_expression_see_also
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: anonymous_slot_expression_aliases
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: anonymous_slot_expression_mappings
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: anonymous_slot_expression_exact_mappings
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: anonymous_slot_expression_close_mappings
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: anonymous_slot_expression_related_mappings
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: anonymous_slot_expression_narrow_mappings
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: anonymous_slot_expression_broad_mappings
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: anonymous_slot_expression_contributors
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: anonymous_slot_expression_category
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: anonymous_slot_expression_keyword
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: slot_definition_domain_of
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: domain_of_name Description: the class(es) that reference the slot in a "slots" or "slot_usage" context
-- # Class: slot_definition_disjoint_with
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: disjoint_with_name Description: Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances
-- # Class: slot_definition_union_of
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: union_of_name Description: indicates that the domain element consists exactly of the members of the element in the range.
-- # Class: slot_definition_type_mappings
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: type_mappings_framework Description: A collection of type mappings that specify how a slot's range should be mapped or serialized in different frameworks
-- # Class: slot_definition_equals_string_in
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: equals_string_in Description: the slot must have range string and the value of the slot must equal one of the specified values
-- # Class: slot_definition_none_of
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: slot_definition_exactly_one_of
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: slot_definition_any_of
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: slot_definition_all_of
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: slot_definition_mixins
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: mixins_name Description: A collection of secondary parent mixin slots from which inheritable metaslots are propagated
-- # Class: slot_definition_apply_to
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: apply_to_name Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
-- # Class: slot_definition_values_from
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: values_from Description: The identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
-- # Class: slot_definition_id_prefixes
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: slot_definition_implements
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: implements Description: An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.
-- # Class: slot_definition_instantiates
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: instantiates Description: An element in another schema which this element instantiates.
-- # Class: slot_definition_todos
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: slot_definition_notes
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: slot_definition_comments
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: slot_definition_in_subset
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: slot_definition_see_also
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: slot_definition_aliases
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: slot_definition_mappings
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: slot_definition_exact_mappings
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: slot_definition_close_mappings
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: slot_definition_related_mappings
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: slot_definition_narrow_mappings
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: slot_definition_broad_mappings
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: slot_definition_contributors
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: slot_definition_category
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: slot_definition_keyword
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: class_expression_any_of
--     * Slot: class_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: class_expression_exactly_one_of
--     * Slot: class_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: class_expression_none_of
--     * Slot: class_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: class_expression_all_of
--     * Slot: class_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: anonymous_class_expression_any_of
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: anonymous_class_expression_exactly_one_of
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: anonymous_class_expression_none_of
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: anonymous_class_expression_all_of
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: anonymous_class_expression_todos
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: anonymous_class_expression_notes
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: anonymous_class_expression_comments
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: anonymous_class_expression_in_subset
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: anonymous_class_expression_see_also
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: anonymous_class_expression_aliases
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: anonymous_class_expression_mappings
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: anonymous_class_expression_exact_mappings
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: anonymous_class_expression_close_mappings
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: anonymous_class_expression_related_mappings
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: anonymous_class_expression_narrow_mappings
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: anonymous_class_expression_broad_mappings
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: anonymous_class_expression_contributors
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: anonymous_class_expression_category
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: anonymous_class_expression_keyword
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: class_definition_slots
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: slots_name Description: collection of slot names that are applicable to a class
-- # Class: class_definition_union_of
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: union_of_name Description: indicates that the domain element consists exactly of the members of the element in the range.
-- # Class: class_definition_defining_slots
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: defining_slots_name Description: The combination of is a plus defining slots form a genus-differentia definition, or the set of necessary and sufficient conditions that can be transformed into an OWL equivalence axiom
-- # Class: class_definition_disjoint_with
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: disjoint_with_name Description: Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances
-- # Class: class_definition_any_of
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: class_definition_exactly_one_of
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: class_definition_none_of
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: class_definition_all_of
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: class_definition_mixins
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: mixins_name Description: A collection of secondary parent mixin classes from which inheritable metaslots are propagated
-- # Class: class_definition_apply_to
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: apply_to_name Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
-- # Class: class_definition_values_from
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: values_from Description: The identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
-- # Class: class_definition_id_prefixes
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: class_definition_implements
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: implements Description: An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.
-- # Class: class_definition_instantiates
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: instantiates Description: An element in another schema which this element instantiates.
-- # Class: class_definition_todos
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: class_definition_notes
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: class_definition_comments
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: class_definition_in_subset
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: class_definition_see_also
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: class_definition_aliases
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: class_definition_mappings
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: class_definition_exact_mappings
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: class_definition_close_mappings
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: class_definition_related_mappings
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: class_definition_narrow_mappings
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: class_definition_broad_mappings
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: class_definition_contributors
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: class_definition_category
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: class_definition_keyword
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: class_rule_todos
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: class_rule_notes
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: class_rule_comments
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: class_rule_in_subset
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: class_rule_see_also
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: class_rule_aliases
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: class_rule_mappings
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: class_rule_exact_mappings
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: class_rule_close_mappings
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: class_rule_related_mappings
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: class_rule_narrow_mappings
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: class_rule_broad_mappings
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: class_rule_contributors
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: class_rule_category
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: class_rule_keyword
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: array_expression_dimensions
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: dimensions_id Description: definitions of each axis in the array
-- # Class: array_expression_todos
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: array_expression_notes
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: array_expression_comments
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: array_expression_in_subset
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: array_expression_see_also
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: array_expression_aliases
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: array_expression_mappings
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: array_expression_exact_mappings
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: array_expression_close_mappings
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: array_expression_related_mappings
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: array_expression_narrow_mappings
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: array_expression_broad_mappings
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: array_expression_contributors
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: array_expression_category
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: array_expression_keyword
--     * Slot: array_expression_id Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: dimension_expression_todos
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: dimension_expression_notes
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: dimension_expression_comments
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: dimension_expression_in_subset
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: dimension_expression_see_also
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: dimension_expression_aliases
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: dimension_expression_mappings
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: dimension_expression_exact_mappings
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: dimension_expression_close_mappings
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: dimension_expression_related_mappings
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: dimension_expression_narrow_mappings
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: dimension_expression_broad_mappings
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: dimension_expression_contributors
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: dimension_expression_category
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: dimension_expression_keyword
--     * Slot: dimension_expression_id Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: pattern_expression_todos
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: pattern_expression_notes
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: pattern_expression_comments
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: pattern_expression_in_subset
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: pattern_expression_see_also
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: pattern_expression_aliases
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: pattern_expression_mappings
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: pattern_expression_exact_mappings
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: pattern_expression_close_mappings
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: pattern_expression_related_mappings
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: pattern_expression_narrow_mappings
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: pattern_expression_broad_mappings
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: pattern_expression_contributors
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: pattern_expression_category
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: pattern_expression_keyword
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: import_expression_todos
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: import_expression_notes
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: import_expression_comments
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: import_expression_in_subset
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: import_expression_see_also
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: import_expression_aliases
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: import_expression_mappings
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: import_expression_exact_mappings
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: import_expression_close_mappings
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: import_expression_related_mappings
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: import_expression_narrow_mappings
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: import_expression_broad_mappings
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: import_expression_contributors
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: import_expression_category
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: import_expression_keyword
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: permissible_value_instantiates
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: instantiates Description: An element in another schema which this element instantiates.
-- # Class: permissible_value_implements
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: implements Description: An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.
-- # Class: permissible_value_mixins
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: mixins_text Description: A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.
-- # Class: permissible_value_todos
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: permissible_value_notes
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: permissible_value_comments
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: permissible_value_in_subset
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: permissible_value_see_also
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: permissible_value_aliases
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: permissible_value_mappings
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: permissible_value_exact_mappings
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: permissible_value_close_mappings
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: permissible_value_related_mappings
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: permissible_value_narrow_mappings
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: permissible_value_broad_mappings
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: permissible_value_contributors
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: permissible_value_category
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: permissible_value_keyword
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: unique_key_unique_key_slots
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: unique_key_slots_name Description: list of slot names that form a key. The tuple formed from the values of all these slots should be unique.
-- # Class: unique_key_todos
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: unique_key_notes
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: unique_key_comments
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: unique_key_in_subset
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: unique_key_see_also
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: unique_key_aliases
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: unique_key_mappings
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: unique_key_exact_mappings
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: unique_key_close_mappings
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: unique_key_related_mappings
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: unique_key_narrow_mappings
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: unique_key_broad_mappings
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: unique_key_contributors
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: unique_key_category
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: unique_key_keyword
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: type_mapping_todos
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issues that needs resolution
-- # Class: type_mapping_notes
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended primarily for internal consumption
-- # Class: type_mapping_comments
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended primarily for external consumption
-- # Class: type_mapping_in_subset
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: in_subset_name Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application.
-- # Class: type_mapping_see_also
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: see_also Description: A list of related entities or URLs that may be of relevance
-- # Class: type_mapping_aliases
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: aliases Description: Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.
-- # Class: type_mapping_mappings
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: type_mapping_exact_mappings
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: type_mapping_close_mappings
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: type_mapping_related_mappings
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: type_mapping_narrow_mappings
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: type_mapping_broad_mappings
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: type_mapping_contributors
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: contributors Description: agent that contributed to the element
-- # Class: type_mapping_category
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: category Description: Controlled terms used to categorize an element.
-- # Class: type_mapping_keyword
--     * Slot: type_mapping_framework Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: UnitOfMeasure_exact_mappings
--     * Slot: UnitOfMeasure_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: Used to link a unit to equivalent concepts in ontologies such as UO, SNOMED, OEM, OBOE, NCIT

CREATE TABLE "Anything" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Anything_id" ON "Anything" (id);

CREATE TABLE common_metadata (
	id INTEGER NOT NULL,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX ix_common_metadata_id ON common_metadata (id);

CREATE TABLE element (
	name TEXT NOT NULL,
	id_prefixes_are_closed BOOLEAN,
	definition_uri TEXT,
	conforms_to TEXT,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	PRIMARY KEY (name)
);
CREATE INDEX ix_element_name ON element (name);

CREATE TABLE schema_definition (
	id TEXT NOT NULL,
	version TEXT,
	license TEXT,
	default_prefix TEXT,
	default_range TEXT,
	metamodel_version TEXT,
	source_file TEXT,
	source_file_date DATETIME,
	source_file_size INTEGER,
	generation_date DATETIME,
	slot_names_unique BOOLEAN,
	name TEXT NOT NULL,
	id_prefixes_are_closed BOOLEAN,
	definition_uri TEXT,
	conforms_to TEXT,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	PRIMARY KEY (name),
	FOREIGN KEY(default_range) REFERENCES type_definition (name)
);
CREATE INDEX ix_schema_definition_name ON schema_definition (name);

CREATE TABLE type_definition (
	typeof TEXT,
	base TEXT,
	uri TEXT,
	repr TEXT,
	pattern TEXT,
	implicit_prefix TEXT,
	equals_string TEXT,
	equals_number INTEGER,
	name TEXT NOT NULL,
	id_prefixes_are_closed BOOLEAN,
	definition_uri TEXT,
	conforms_to TEXT,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	schema_definition_name TEXT,
	structured_pattern_id INTEGER,
	unit_id INTEGER,
	minimum_value_id INTEGER,
	maximum_value_id INTEGER,
	PRIMARY KEY (name),
	FOREIGN KEY(typeof) REFERENCES type_definition (name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(structured_pattern_id) REFERENCES pattern_expression (id),
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id),
	FOREIGN KEY(minimum_value_id) REFERENCES "Anything" (id),
	FOREIGN KEY(maximum_value_id) REFERENCES "Anything" (id)
);
CREATE INDEX ix_type_definition_name ON type_definition (name);

CREATE TABLE definition (
	is_a TEXT,
	abstract BOOLEAN,
	mixin BOOLEAN,
	string_serialization TEXT,
	name TEXT NOT NULL,
	id_prefixes_are_closed BOOLEAN,
	definition_uri TEXT,
	conforms_to TEXT,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	PRIMARY KEY (name),
	FOREIGN KEY(is_a) REFERENCES definition (name)
);
CREATE INDEX ix_definition_name ON definition (name);

CREATE TABLE match_query (
	id INTEGER NOT NULL,
	identifier_pattern TEXT,
	source_ontology TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX ix_match_query_id ON match_query (id);

CREATE TABLE reachability_query (
	id INTEGER NOT NULL,
	source_ontology TEXT,
	is_direct BOOLEAN,
	include_self BOOLEAN,
	traverse_up BOOLEAN,
	PRIMARY KEY (id)
);
CREATE INDEX ix_reachability_query_id ON reachability_query (id);

CREATE TABLE expression (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX ix_expression_id ON expression (id);

CREATE TABLE anonymous_expression (
	id INTEGER NOT NULL,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX ix_anonymous_expression_id ON anonymous_expression (id);

CREATE TABLE path_expression (
	id INTEGER NOT NULL,
	reversed BOOLEAN,
	traverse TEXT,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	followed_by_id INTEGER,
	range_expression_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(traverse) REFERENCES slot_definition (name),
	FOREIGN KEY(followed_by_id) REFERENCES path_expression (id),
	FOREIGN KEY(range_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_path_expression_id ON path_expression (id);

CREATE TABLE slot_definition (
	singular_name TEXT,
	domain TEXT,
	slot_uri TEXT,
	inherited BOOLEAN,
	readonly TEXT,
	ifabsent TEXT,
	list_elements_unique BOOLEAN,
	list_elements_ordered BOOLEAN,
	shared BOOLEAN,
	"key" BOOLEAN,
	identifier BOOLEAN,
	designates_type BOOLEAN,
	alias TEXT,
	owner TEXT,
	subproperty_of TEXT,
	symmetric BOOLEAN,
	reflexive BOOLEAN,
	locally_reflexive BOOLEAN,
	irreflexive BOOLEAN,
	asymmetric BOOLEAN,
	transitive BOOLEAN,
	inverse TEXT,
	is_class_field BOOLEAN,
	transitive_form_of TEXT,
	reflexive_transitive_form_of TEXT,
	role TEXT,
	is_usage_slot BOOLEAN,
	usage_slot_name TEXT,
	relational_role VARCHAR(10),
	slot_group TEXT,
	is_grouping_slot BOOLEAN,
	children_are_mutually_disjoint BOOLEAN,
	range TEXT,
	required BOOLEAN,
	recommended BOOLEAN,
	multivalued BOOLEAN,
	inlined BOOLEAN,
	inlined_as_list BOOLEAN,
	pattern TEXT,
	implicit_prefix TEXT,
	value_presence VARCHAR(11),
	equals_string TEXT,
	equals_number INTEGER,
	equals_expression TEXT,
	exact_cardinality INTEGER,
	minimum_cardinality INTEGER,
	maximum_cardinality INTEGER,
	is_a TEXT,
	abstract BOOLEAN,
	mixin BOOLEAN,
	string_serialization TEXT,
	name TEXT NOT NULL,
	id_prefixes_are_closed BOOLEAN,
	definition_uri TEXT,
	conforms_to TEXT,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	schema_definition_name TEXT,
	class_expression_id INTEGER,
	anonymous_class_expression_id INTEGER,
	class_definition_name TEXT,
	path_rule_id INTEGER,
	range_expression_id INTEGER,
	enum_range_id INTEGER,
	minimum_value_id INTEGER,
	maximum_value_id INTEGER,
	structured_pattern_id INTEGER,
	unit_id INTEGER,
	has_member_id INTEGER,
	all_members_id INTEGER,
	array_id INTEGER,
	PRIMARY KEY (name),
	FOREIGN KEY(domain) REFERENCES class_definition (name),
	FOREIGN KEY(owner) REFERENCES definition (name),
	FOREIGN KEY(subproperty_of) REFERENCES slot_definition (name),
	FOREIGN KEY(inverse) REFERENCES slot_definition (name),
	FOREIGN KEY(transitive_form_of) REFERENCES slot_definition (name),
	FOREIGN KEY(reflexive_transitive_form_of) REFERENCES slot_definition (name),
	FOREIGN KEY(slot_group) REFERENCES slot_definition (name),
	FOREIGN KEY(range) REFERENCES element (name),
	FOREIGN KEY(is_a) REFERENCES slot_definition (name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(class_expression_id) REFERENCES class_expression (id),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(path_rule_id) REFERENCES path_expression (id),
	FOREIGN KEY(range_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(enum_range_id) REFERENCES enum_expression (id),
	FOREIGN KEY(minimum_value_id) REFERENCES "Anything" (id),
	FOREIGN KEY(maximum_value_id) REFERENCES "Anything" (id),
	FOREIGN KEY(structured_pattern_id) REFERENCES pattern_expression (id),
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id),
	FOREIGN KEY(has_member_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(all_members_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(array_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_slot_definition_name ON slot_definition (name);

CREATE TABLE class_expression (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX ix_class_expression_id ON class_expression (id);

CREATE TABLE anonymous_class_expression (
	id INTEGER NOT NULL,
	is_a TEXT,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	class_definition_name TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(is_a) REFERENCES definition (name),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_anonymous_class_expression_id ON anonymous_class_expression (id);

CREATE TABLE class_definition (
	class_uri TEXT,
	subclass_of TEXT,
	tree_root BOOLEAN,
	slot_names_unique BOOLEAN,
	represents_relationship BOOLEAN,
	children_are_mutually_disjoint BOOLEAN,
	alias TEXT,
	is_a TEXT,
	abstract BOOLEAN,
	mixin BOOLEAN,
	string_serialization TEXT,
	name TEXT NOT NULL,
	id_prefixes_are_closed BOOLEAN,
	definition_uri TEXT,
	conforms_to TEXT,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	schema_definition_name TEXT,
	extra_slots_id INTEGER,
	PRIMARY KEY (name),
	FOREIGN KEY(is_a) REFERENCES class_definition (name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(extra_slots_id) REFERENCES extra_slots_expression (id)
);
CREATE INDEX ix_class_definition_name ON class_definition (name);

CREATE TABLE class_level_rule (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX ix_class_level_rule_id ON class_level_rule (id);

CREATE TABLE dimension_expression (
	id INTEGER NOT NULL,
	alias TEXT,
	maximum_cardinality INTEGER,
	minimum_cardinality INTEGER,
	exact_cardinality INTEGER,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX ix_dimension_expression_id ON dimension_expression (id);

CREATE TABLE pattern_expression (
	id INTEGER NOT NULL,
	syntax TEXT,
	interpolated BOOLEAN,
	partial_match BOOLEAN,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX ix_pattern_expression_id ON pattern_expression (id);

CREATE TABLE import_expression (
	id INTEGER NOT NULL,
	import_from TEXT NOT NULL,
	import_as TEXT,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX ix_import_expression_id ON import_expression (id);

CREATE TABLE extra_slots_expression (
	id INTEGER NOT NULL,
	allowed BOOLEAN,
	range_expression_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(range_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_extra_slots_expression_id ON extra_slots_expression (id);

CREATE TABLE "AnyValue" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_AnyValue_id" ON "AnyValue" (id);

CREATE TABLE extensible (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX ix_extensible_id ON extensible (id);

CREATE TABLE annotatable (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX ix_annotatable_id ON annotatable (id);

CREATE TABLE "UnitOfMeasure" (
	id INTEGER NOT NULL,
	symbol TEXT,
	abbreviation TEXT,
	descriptive_name TEXT,
	ucum_code TEXT,
	derivation TEXT,
	has_quantity_kind TEXT,
	iec61360code TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_UnitOfMeasure_id" ON "UnitOfMeasure" (id);

CREATE TABLE type_expression (
	id INTEGER NOT NULL,
	pattern TEXT,
	implicit_prefix TEXT,
	equals_string TEXT,
	equals_number INTEGER,
	structured_pattern_id INTEGER,
	unit_id INTEGER,
	minimum_value_id INTEGER,
	maximum_value_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(structured_pattern_id) REFERENCES pattern_expression (id),
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id),
	FOREIGN KEY(minimum_value_id) REFERENCES "Anything" (id),
	FOREIGN KEY(maximum_value_id) REFERENCES "Anything" (id)
);
CREATE INDEX ix_type_expression_id ON type_expression (id);

CREATE TABLE anonymous_type_expression (
	id INTEGER NOT NULL,
	pattern TEXT,
	implicit_prefix TEXT,
	equals_string TEXT,
	equals_number INTEGER,
	structured_pattern_id INTEGER,
	unit_id INTEGER,
	minimum_value_id INTEGER,
	maximum_value_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(structured_pattern_id) REFERENCES pattern_expression (id),
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id),
	FOREIGN KEY(minimum_value_id) REFERENCES "Anything" (id),
	FOREIGN KEY(maximum_value_id) REFERENCES "Anything" (id)
);
CREATE INDEX ix_anonymous_type_expression_id ON anonymous_type_expression (id);

CREATE TABLE subset_definition (
	name TEXT NOT NULL,
	id_prefixes_are_closed BOOLEAN,
	definition_uri TEXT,
	conforms_to TEXT,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	schema_definition_name TEXT,
	PRIMARY KEY (name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_subset_definition_name ON subset_definition (name);

CREATE TABLE enum_expression (
	id INTEGER NOT NULL,
	code_set TEXT,
	code_set_tag TEXT,
	code_set_version TEXT,
	pv_formula VARCHAR(11),
	reachable_from_id INTEGER,
	matches_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(reachable_from_id) REFERENCES reachability_query (id),
	FOREIGN KEY(matches_id) REFERENCES match_query (id)
);
CREATE INDEX ix_enum_expression_id ON enum_expression (id);

CREATE TABLE anonymous_enum_expression (
	id INTEGER NOT NULL,
	code_set TEXT,
	code_set_tag TEXT,
	code_set_version TEXT,
	pv_formula VARCHAR(11),
	reachable_from_id INTEGER,
	matches_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(reachable_from_id) REFERENCES reachability_query (id),
	FOREIGN KEY(matches_id) REFERENCES match_query (id)
);
CREATE INDEX ix_anonymous_enum_expression_id ON anonymous_enum_expression (id);

CREATE TABLE enum_definition (
	enum_uri TEXT,
	code_set TEXT,
	code_set_tag TEXT,
	code_set_version TEXT,
	pv_formula VARCHAR(11),
	is_a TEXT,
	abstract BOOLEAN,
	mixin BOOLEAN,
	string_serialization TEXT,
	name TEXT NOT NULL,
	id_prefixes_are_closed BOOLEAN,
	definition_uri TEXT,
	conforms_to TEXT,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	schema_definition_name TEXT,
	reachable_from_id INTEGER,
	matches_id INTEGER,
	PRIMARY KEY (name),
	FOREIGN KEY(is_a) REFERENCES definition (name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(reachable_from_id) REFERENCES reachability_query (id),
	FOREIGN KEY(matches_id) REFERENCES match_query (id)
);
CREATE INDEX ix_enum_definition_name ON enum_definition (name);

CREATE TABLE class_rule (
	id INTEGER NOT NULL,
	bidirectional BOOLEAN,
	open_world BOOLEAN,
	rank INTEGER,
	deactivated BOOLEAN,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	class_definition_name TEXT,
	preconditions_id INTEGER,
	postconditions_id INTEGER,
	elseconditions_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(preconditions_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(postconditions_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(elseconditions_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_class_rule_id ON class_rule (id);

CREATE TABLE array_expression (
	id INTEGER NOT NULL,
	exact_number_dimensions INTEGER,
	minimum_number_dimensions INTEGER,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	maximum_number_dimensions_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(maximum_number_dimensions_id) REFERENCES "Anything" (id)
);
CREATE INDEX ix_array_expression_id ON array_expression (id);

CREATE TABLE setting (
	setting_key TEXT NOT NULL,
	setting_value TEXT NOT NULL,
	schema_definition_name TEXT,
	import_expression_id INTEGER,
	PRIMARY KEY (setting_key, setting_value, schema_definition_name, import_expression_id),
	UNIQUE (schema_definition_name, setting_key),
	UNIQUE (import_expression_id, setting_key),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX setting_schema_definition_name_setting_key_idx ON setting (schema_definition_name, setting_key);
CREATE INDEX ix_setting_schema_definition_name ON setting (schema_definition_name);
CREATE INDEX ix_setting_import_expression_id ON setting (import_expression_id);
CREATE INDEX setting_import_expression_id_setting_key_idx ON setting (import_expression_id, setting_key);
CREATE INDEX ix_setting_setting_key ON setting (setting_key);
CREATE INDEX ix_setting_setting_value ON setting (setting_value);

CREATE TABLE prefix (
	prefix_prefix TEXT NOT NULL,
	prefix_reference TEXT NOT NULL,
	schema_definition_name TEXT,
	PRIMARY KEY (prefix_prefix, prefix_reference, schema_definition_name),
	UNIQUE (schema_definition_name, prefix_prefix),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_prefix_schema_definition_name ON prefix (schema_definition_name);
CREATE INDEX ix_prefix_prefix_reference ON prefix (prefix_reference);
CREATE INDEX ix_prefix_prefix_prefix ON prefix (prefix_prefix);
CREATE INDEX prefix_schema_definition_name_prefix_prefix_idx ON prefix (schema_definition_name, prefix_prefix);

CREATE TABLE unique_key (
	unique_key_name TEXT NOT NULL,
	consider_nulls_inequal BOOLEAN,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	class_definition_name TEXT,
	PRIMARY KEY (unique_key_name, consider_nulls_inequal, description, title, deprecated, from_schema, imported_from, source, in_language, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, created_by, created_on, last_updated_on, modified_by, status, rank, class_definition_name),
	UNIQUE (class_definition_name, unique_key_name),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_unique_key_created_by ON unique_key (created_by);
CREATE INDEX ix_unique_key_consider_nulls_inequal ON unique_key (consider_nulls_inequal);
CREATE INDEX ix_unique_key_last_updated_on ON unique_key (last_updated_on);
CREATE INDEX ix_unique_key_status ON unique_key (status);
CREATE INDEX ix_unique_key_class_definition_name ON unique_key (class_definition_name);
CREATE INDEX unique_key_class_definition_name_unique_key_name_idx ON unique_key (class_definition_name, unique_key_name);
CREATE INDEX ix_unique_key_description ON unique_key (description);
CREATE INDEX ix_unique_key_deprecated ON unique_key (deprecated);
CREATE INDEX ix_unique_key_imported_from ON unique_key (imported_from);
CREATE INDEX ix_unique_key_in_language ON unique_key (in_language);
CREATE INDEX ix_unique_key_unique_key_name ON unique_key (unique_key_name);
CREATE INDEX ix_unique_key_deprecated_element_has_possible_replacement ON unique_key (deprecated_element_has_possible_replacement);
CREATE INDEX ix_unique_key_modified_by ON unique_key (modified_by);
CREATE INDEX ix_unique_key_created_on ON unique_key (created_on);
CREATE INDEX ix_unique_key_rank ON unique_key (rank);
CREATE INDEX ix_unique_key_title ON unique_key (title);
CREATE INDEX ix_unique_key_from_schema ON unique_key (from_schema);
CREATE INDEX ix_unique_key_source ON unique_key (source);
CREATE INDEX ix_unique_key_deprecated_element_has_exact_replacement ON unique_key (deprecated_element_has_exact_replacement);

CREATE TABLE type_mapping (
	framework TEXT NOT NULL,
	type TEXT,
	string_serialization TEXT,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	PRIMARY KEY (framework, type, string_serialization, description, title, deprecated, from_schema, imported_from, source, in_language, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, created_by, created_on, last_updated_on, modified_by, status, rank),
	FOREIGN KEY(type) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_mapping_description ON type_mapping (description);
CREATE INDEX ix_type_mapping_deprecated_element_has_possible_replacement ON type_mapping (deprecated_element_has_possible_replacement);
CREATE INDEX ix_type_mapping_framework ON type_mapping (framework);
CREATE INDEX ix_type_mapping_created_by ON type_mapping (created_by);
CREATE INDEX ix_type_mapping_title ON type_mapping (title);
CREATE INDEX ix_type_mapping_deprecated_element_has_exact_replacement ON type_mapping (deprecated_element_has_exact_replacement);
CREATE INDEX ix_type_mapping_created_on ON type_mapping (created_on);
CREATE INDEX ix_type_mapping_string_serialization ON type_mapping (string_serialization);
CREATE INDEX ix_type_mapping_deprecated ON type_mapping (deprecated);
CREATE INDEX ix_type_mapping_last_updated_on ON type_mapping (last_updated_on);
CREATE INDEX ix_type_mapping_type ON type_mapping (type);
CREATE INDEX ix_type_mapping_from_schema ON type_mapping (from_schema);
CREATE INDEX ix_type_mapping_source ON type_mapping (source);
CREATE INDEX ix_type_mapping_in_language ON type_mapping (in_language);
CREATE INDEX ix_type_mapping_imported_from ON type_mapping (imported_from);
CREATE INDEX ix_type_mapping_modified_by ON type_mapping (modified_by);
CREATE INDEX ix_type_mapping_status ON type_mapping (status);
CREATE INDEX ix_type_mapping_rank ON type_mapping (rank);

CREATE TABLE common_metadata_todos (
	common_metadata_id INTEGER,
	todos TEXT,
	PRIMARY KEY (common_metadata_id, todos),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_todos_common_metadata_id ON common_metadata_todos (common_metadata_id);
CREATE INDEX ix_common_metadata_todos_todos ON common_metadata_todos (todos);

CREATE TABLE common_metadata_notes (
	common_metadata_id INTEGER,
	notes TEXT,
	PRIMARY KEY (common_metadata_id, notes),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_notes_common_metadata_id ON common_metadata_notes (common_metadata_id);
CREATE INDEX ix_common_metadata_notes_notes ON common_metadata_notes (notes);

CREATE TABLE common_metadata_comments (
	common_metadata_id INTEGER,
	comments TEXT,
	PRIMARY KEY (common_metadata_id, comments),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_comments_comments ON common_metadata_comments (comments);
CREATE INDEX ix_common_metadata_comments_common_metadata_id ON common_metadata_comments (common_metadata_id);

CREATE TABLE common_metadata_see_also (
	common_metadata_id INTEGER,
	see_also TEXT,
	PRIMARY KEY (common_metadata_id, see_also),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_see_also_common_metadata_id ON common_metadata_see_also (common_metadata_id);
CREATE INDEX ix_common_metadata_see_also_see_also ON common_metadata_see_also (see_also);

CREATE TABLE common_metadata_aliases (
	common_metadata_id INTEGER,
	aliases TEXT,
	PRIMARY KEY (common_metadata_id, aliases),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_aliases_common_metadata_id ON common_metadata_aliases (common_metadata_id);
CREATE INDEX ix_common_metadata_aliases_aliases ON common_metadata_aliases (aliases);

CREATE TABLE common_metadata_mappings (
	common_metadata_id INTEGER,
	mappings TEXT,
	PRIMARY KEY (common_metadata_id, mappings),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_mappings_mappings ON common_metadata_mappings (mappings);
CREATE INDEX ix_common_metadata_mappings_common_metadata_id ON common_metadata_mappings (common_metadata_id);

CREATE TABLE common_metadata_exact_mappings (
	common_metadata_id INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY (common_metadata_id, exact_mappings),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_exact_mappings_common_metadata_id ON common_metadata_exact_mappings (common_metadata_id);
CREATE INDEX ix_common_metadata_exact_mappings_exact_mappings ON common_metadata_exact_mappings (exact_mappings);

CREATE TABLE common_metadata_close_mappings (
	common_metadata_id INTEGER,
	close_mappings TEXT,
	PRIMARY KEY (common_metadata_id, close_mappings),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_close_mappings_close_mappings ON common_metadata_close_mappings (close_mappings);
CREATE INDEX ix_common_metadata_close_mappings_common_metadata_id ON common_metadata_close_mappings (common_metadata_id);

CREATE TABLE common_metadata_related_mappings (
	common_metadata_id INTEGER,
	related_mappings TEXT,
	PRIMARY KEY (common_metadata_id, related_mappings),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_related_mappings_related_mappings ON common_metadata_related_mappings (related_mappings);
CREATE INDEX ix_common_metadata_related_mappings_common_metadata_id ON common_metadata_related_mappings (common_metadata_id);

CREATE TABLE common_metadata_narrow_mappings (
	common_metadata_id INTEGER,
	narrow_mappings TEXT,
	PRIMARY KEY (common_metadata_id, narrow_mappings),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_narrow_mappings_common_metadata_id ON common_metadata_narrow_mappings (common_metadata_id);
CREATE INDEX ix_common_metadata_narrow_mappings_narrow_mappings ON common_metadata_narrow_mappings (narrow_mappings);

CREATE TABLE common_metadata_broad_mappings (
	common_metadata_id INTEGER,
	broad_mappings TEXT,
	PRIMARY KEY (common_metadata_id, broad_mappings),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_broad_mappings_broad_mappings ON common_metadata_broad_mappings (broad_mappings);
CREATE INDEX ix_common_metadata_broad_mappings_common_metadata_id ON common_metadata_broad_mappings (common_metadata_id);

CREATE TABLE common_metadata_contributors (
	common_metadata_id INTEGER,
	contributors TEXT,
	PRIMARY KEY (common_metadata_id, contributors),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_contributors_contributors ON common_metadata_contributors (contributors);
CREATE INDEX ix_common_metadata_contributors_common_metadata_id ON common_metadata_contributors (common_metadata_id);

CREATE TABLE common_metadata_category (
	common_metadata_id INTEGER,
	category TEXT,
	PRIMARY KEY (common_metadata_id, category),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_category_category ON common_metadata_category (category);
CREATE INDEX ix_common_metadata_category_common_metadata_id ON common_metadata_category (common_metadata_id);

CREATE TABLE common_metadata_keyword (
	common_metadata_id INTEGER,
	keyword TEXT,
	PRIMARY KEY (common_metadata_id, keyword),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE INDEX ix_common_metadata_keyword_common_metadata_id ON common_metadata_keyword (common_metadata_id);
CREATE INDEX ix_common_metadata_keyword_keyword ON common_metadata_keyword (keyword);

CREATE TABLE element_id_prefixes (
	element_name TEXT,
	id_prefixes TEXT,
	PRIMARY KEY (element_name, id_prefixes),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_id_prefixes_element_name ON element_id_prefixes (element_name);
CREATE INDEX ix_element_id_prefixes_id_prefixes ON element_id_prefixes (id_prefixes);

CREATE TABLE element_implements (
	element_name TEXT,
	implements TEXT,
	PRIMARY KEY (element_name, implements),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_implements_implements ON element_implements (implements);
CREATE INDEX ix_element_implements_element_name ON element_implements (element_name);

CREATE TABLE element_instantiates (
	element_name TEXT,
	instantiates TEXT,
	PRIMARY KEY (element_name, instantiates),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_instantiates_element_name ON element_instantiates (element_name);
CREATE INDEX ix_element_instantiates_instantiates ON element_instantiates (instantiates);

CREATE TABLE element_todos (
	element_name TEXT,
	todos TEXT,
	PRIMARY KEY (element_name, todos),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_todos_todos ON element_todos (todos);
CREATE INDEX ix_element_todos_element_name ON element_todos (element_name);

CREATE TABLE element_notes (
	element_name TEXT,
	notes TEXT,
	PRIMARY KEY (element_name, notes),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_notes_element_name ON element_notes (element_name);
CREATE INDEX ix_element_notes_notes ON element_notes (notes);

CREATE TABLE element_comments (
	element_name TEXT,
	comments TEXT,
	PRIMARY KEY (element_name, comments),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_comments_comments ON element_comments (comments);
CREATE INDEX ix_element_comments_element_name ON element_comments (element_name);

CREATE TABLE element_see_also (
	element_name TEXT,
	see_also TEXT,
	PRIMARY KEY (element_name, see_also),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_see_also_element_name ON element_see_also (element_name);
CREATE INDEX ix_element_see_also_see_also ON element_see_also (see_also);

CREATE TABLE element_aliases (
	element_name TEXT,
	aliases TEXT,
	PRIMARY KEY (element_name, aliases),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_aliases_element_name ON element_aliases (element_name);
CREATE INDEX ix_element_aliases_aliases ON element_aliases (aliases);

CREATE TABLE element_mappings (
	element_name TEXT,
	mappings TEXT,
	PRIMARY KEY (element_name, mappings),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_mappings_mappings ON element_mappings (mappings);
CREATE INDEX ix_element_mappings_element_name ON element_mappings (element_name);

CREATE TABLE element_exact_mappings (
	element_name TEXT,
	exact_mappings TEXT,
	PRIMARY KEY (element_name, exact_mappings),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_exact_mappings_exact_mappings ON element_exact_mappings (exact_mappings);
CREATE INDEX ix_element_exact_mappings_element_name ON element_exact_mappings (element_name);

CREATE TABLE element_close_mappings (
	element_name TEXT,
	close_mappings TEXT,
	PRIMARY KEY (element_name, close_mappings),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_close_mappings_element_name ON element_close_mappings (element_name);
CREATE INDEX ix_element_close_mappings_close_mappings ON element_close_mappings (close_mappings);

CREATE TABLE element_related_mappings (
	element_name TEXT,
	related_mappings TEXT,
	PRIMARY KEY (element_name, related_mappings),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_related_mappings_element_name ON element_related_mappings (element_name);
CREATE INDEX ix_element_related_mappings_related_mappings ON element_related_mappings (related_mappings);

CREATE TABLE element_narrow_mappings (
	element_name TEXT,
	narrow_mappings TEXT,
	PRIMARY KEY (element_name, narrow_mappings),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_narrow_mappings_narrow_mappings ON element_narrow_mappings (narrow_mappings);
CREATE INDEX ix_element_narrow_mappings_element_name ON element_narrow_mappings (element_name);

CREATE TABLE element_broad_mappings (
	element_name TEXT,
	broad_mappings TEXT,
	PRIMARY KEY (element_name, broad_mappings),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_broad_mappings_element_name ON element_broad_mappings (element_name);
CREATE INDEX ix_element_broad_mappings_broad_mappings ON element_broad_mappings (broad_mappings);

CREATE TABLE element_contributors (
	element_name TEXT,
	contributors TEXT,
	PRIMARY KEY (element_name, contributors),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_contributors_contributors ON element_contributors (contributors);
CREATE INDEX ix_element_contributors_element_name ON element_contributors (element_name);

CREATE TABLE element_category (
	element_name TEXT,
	category TEXT,
	PRIMARY KEY (element_name, category),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_category_element_name ON element_category (element_name);
CREATE INDEX ix_element_category_category ON element_category (category);

CREATE TABLE element_keyword (
	element_name TEXT,
	keyword TEXT,
	PRIMARY KEY (element_name, keyword),
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE INDEX ix_element_keyword_keyword ON element_keyword (keyword);
CREATE INDEX ix_element_keyword_element_name ON element_keyword (element_name);

CREATE TABLE schema_definition_imports (
	schema_definition_name TEXT,
	imports TEXT,
	PRIMARY KEY (schema_definition_name, imports),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_imports_schema_definition_name ON schema_definition_imports (schema_definition_name);
CREATE INDEX ix_schema_definition_imports_imports ON schema_definition_imports (imports);

CREATE TABLE schema_definition_emit_prefixes (
	schema_definition_name TEXT,
	emit_prefixes TEXT,
	PRIMARY KEY (schema_definition_name, emit_prefixes),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_emit_prefixes_emit_prefixes ON schema_definition_emit_prefixes (emit_prefixes);
CREATE INDEX ix_schema_definition_emit_prefixes_schema_definition_name ON schema_definition_emit_prefixes (schema_definition_name);

CREATE TABLE schema_definition_default_curi_maps (
	schema_definition_name TEXT,
	default_curi_maps TEXT,
	PRIMARY KEY (schema_definition_name, default_curi_maps),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_default_curi_maps_schema_definition_name ON schema_definition_default_curi_maps (schema_definition_name);
CREATE INDEX ix_schema_definition_default_curi_maps_default_curi_maps ON schema_definition_default_curi_maps (default_curi_maps);

CREATE TABLE schema_definition_id_prefixes (
	schema_definition_name TEXT,
	id_prefixes TEXT,
	PRIMARY KEY (schema_definition_name, id_prefixes),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_id_prefixes_id_prefixes ON schema_definition_id_prefixes (id_prefixes);
CREATE INDEX ix_schema_definition_id_prefixes_schema_definition_name ON schema_definition_id_prefixes (schema_definition_name);

CREATE TABLE schema_definition_implements (
	schema_definition_name TEXT,
	implements TEXT,
	PRIMARY KEY (schema_definition_name, implements),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_implements_schema_definition_name ON schema_definition_implements (schema_definition_name);
CREATE INDEX ix_schema_definition_implements_implements ON schema_definition_implements (implements);

CREATE TABLE schema_definition_instantiates (
	schema_definition_name TEXT,
	instantiates TEXT,
	PRIMARY KEY (schema_definition_name, instantiates),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_instantiates_instantiates ON schema_definition_instantiates (instantiates);
CREATE INDEX ix_schema_definition_instantiates_schema_definition_name ON schema_definition_instantiates (schema_definition_name);

CREATE TABLE schema_definition_todos (
	schema_definition_name TEXT,
	todos TEXT,
	PRIMARY KEY (schema_definition_name, todos),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_todos_schema_definition_name ON schema_definition_todos (schema_definition_name);
CREATE INDEX ix_schema_definition_todos_todos ON schema_definition_todos (todos);

CREATE TABLE schema_definition_notes (
	schema_definition_name TEXT,
	notes TEXT,
	PRIMARY KEY (schema_definition_name, notes),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_notes_schema_definition_name ON schema_definition_notes (schema_definition_name);
CREATE INDEX ix_schema_definition_notes_notes ON schema_definition_notes (notes);

CREATE TABLE schema_definition_comments (
	schema_definition_name TEXT,
	comments TEXT,
	PRIMARY KEY (schema_definition_name, comments),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_comments_comments ON schema_definition_comments (comments);
CREATE INDEX ix_schema_definition_comments_schema_definition_name ON schema_definition_comments (schema_definition_name);

CREATE TABLE schema_definition_see_also (
	schema_definition_name TEXT,
	see_also TEXT,
	PRIMARY KEY (schema_definition_name, see_also),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_see_also_schema_definition_name ON schema_definition_see_also (schema_definition_name);
CREATE INDEX ix_schema_definition_see_also_see_also ON schema_definition_see_also (see_also);

CREATE TABLE schema_definition_aliases (
	schema_definition_name TEXT,
	aliases TEXT,
	PRIMARY KEY (schema_definition_name, aliases),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_aliases_schema_definition_name ON schema_definition_aliases (schema_definition_name);
CREATE INDEX ix_schema_definition_aliases_aliases ON schema_definition_aliases (aliases);

CREATE TABLE schema_definition_mappings (
	schema_definition_name TEXT,
	mappings TEXT,
	PRIMARY KEY (schema_definition_name, mappings),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_mappings_schema_definition_name ON schema_definition_mappings (schema_definition_name);
CREATE INDEX ix_schema_definition_mappings_mappings ON schema_definition_mappings (mappings);

CREATE TABLE schema_definition_exact_mappings (
	schema_definition_name TEXT,
	exact_mappings TEXT,
	PRIMARY KEY (schema_definition_name, exact_mappings),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_exact_mappings_schema_definition_name ON schema_definition_exact_mappings (schema_definition_name);
CREATE INDEX ix_schema_definition_exact_mappings_exact_mappings ON schema_definition_exact_mappings (exact_mappings);

CREATE TABLE schema_definition_close_mappings (
	schema_definition_name TEXT,
	close_mappings TEXT,
	PRIMARY KEY (schema_definition_name, close_mappings),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_close_mappings_close_mappings ON schema_definition_close_mappings (close_mappings);
CREATE INDEX ix_schema_definition_close_mappings_schema_definition_name ON schema_definition_close_mappings (schema_definition_name);

CREATE TABLE schema_definition_related_mappings (
	schema_definition_name TEXT,
	related_mappings TEXT,
	PRIMARY KEY (schema_definition_name, related_mappings),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_related_mappings_related_mappings ON schema_definition_related_mappings (related_mappings);
CREATE INDEX ix_schema_definition_related_mappings_schema_definition_name ON schema_definition_related_mappings (schema_definition_name);

CREATE TABLE schema_definition_narrow_mappings (
	schema_definition_name TEXT,
	narrow_mappings TEXT,
	PRIMARY KEY (schema_definition_name, narrow_mappings),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_narrow_mappings_schema_definition_name ON schema_definition_narrow_mappings (schema_definition_name);
CREATE INDEX ix_schema_definition_narrow_mappings_narrow_mappings ON schema_definition_narrow_mappings (narrow_mappings);

CREATE TABLE schema_definition_broad_mappings (
	schema_definition_name TEXT,
	broad_mappings TEXT,
	PRIMARY KEY (schema_definition_name, broad_mappings),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_broad_mappings_schema_definition_name ON schema_definition_broad_mappings (schema_definition_name);
CREATE INDEX ix_schema_definition_broad_mappings_broad_mappings ON schema_definition_broad_mappings (broad_mappings);

CREATE TABLE schema_definition_contributors (
	schema_definition_name TEXT,
	contributors TEXT,
	PRIMARY KEY (schema_definition_name, contributors),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_contributors_schema_definition_name ON schema_definition_contributors (schema_definition_name);
CREATE INDEX ix_schema_definition_contributors_contributors ON schema_definition_contributors (contributors);

CREATE TABLE schema_definition_category (
	schema_definition_name TEXT,
	category TEXT,
	PRIMARY KEY (schema_definition_name, category),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_category_schema_definition_name ON schema_definition_category (schema_definition_name);
CREATE INDEX ix_schema_definition_category_category ON schema_definition_category (category);

CREATE TABLE schema_definition_keyword (
	schema_definition_name TEXT,
	keyword TEXT,
	PRIMARY KEY (schema_definition_name, keyword),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);
CREATE INDEX ix_schema_definition_keyword_schema_definition_name ON schema_definition_keyword (schema_definition_name);
CREATE INDEX ix_schema_definition_keyword_keyword ON schema_definition_keyword (keyword);

CREATE TABLE type_definition_union_of (
	type_definition_name TEXT,
	union_of_name TEXT,
	PRIMARY KEY (type_definition_name, union_of_name),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name),
	FOREIGN KEY(union_of_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_union_of_type_definition_name ON type_definition_union_of (type_definition_name);
CREATE INDEX ix_type_definition_union_of_union_of_name ON type_definition_union_of (union_of_name);

CREATE TABLE type_definition_equals_string_in (
	type_definition_name TEXT,
	equals_string_in TEXT,
	PRIMARY KEY (type_definition_name, equals_string_in),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_equals_string_in_type_definition_name ON type_definition_equals_string_in (type_definition_name);
CREATE INDEX ix_type_definition_equals_string_in_equals_string_in ON type_definition_equals_string_in (equals_string_in);

CREATE TABLE type_definition_id_prefixes (
	type_definition_name TEXT,
	id_prefixes TEXT,
	PRIMARY KEY (type_definition_name, id_prefixes),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_id_prefixes_id_prefixes ON type_definition_id_prefixes (id_prefixes);
CREATE INDEX ix_type_definition_id_prefixes_type_definition_name ON type_definition_id_prefixes (type_definition_name);

CREATE TABLE type_definition_implements (
	type_definition_name TEXT,
	implements TEXT,
	PRIMARY KEY (type_definition_name, implements),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_implements_type_definition_name ON type_definition_implements (type_definition_name);
CREATE INDEX ix_type_definition_implements_implements ON type_definition_implements (implements);

CREATE TABLE type_definition_instantiates (
	type_definition_name TEXT,
	instantiates TEXT,
	PRIMARY KEY (type_definition_name, instantiates),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_instantiates_type_definition_name ON type_definition_instantiates (type_definition_name);
CREATE INDEX ix_type_definition_instantiates_instantiates ON type_definition_instantiates (instantiates);

CREATE TABLE type_definition_todos (
	type_definition_name TEXT,
	todos TEXT,
	PRIMARY KEY (type_definition_name, todos),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_todos_type_definition_name ON type_definition_todos (type_definition_name);
CREATE INDEX ix_type_definition_todos_todos ON type_definition_todos (todos);

CREATE TABLE type_definition_notes (
	type_definition_name TEXT,
	notes TEXT,
	PRIMARY KEY (type_definition_name, notes),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_notes_type_definition_name ON type_definition_notes (type_definition_name);
CREATE INDEX ix_type_definition_notes_notes ON type_definition_notes (notes);

CREATE TABLE type_definition_comments (
	type_definition_name TEXT,
	comments TEXT,
	PRIMARY KEY (type_definition_name, comments),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_comments_comments ON type_definition_comments (comments);
CREATE INDEX ix_type_definition_comments_type_definition_name ON type_definition_comments (type_definition_name);

CREATE TABLE type_definition_see_also (
	type_definition_name TEXT,
	see_also TEXT,
	PRIMARY KEY (type_definition_name, see_also),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_see_also_see_also ON type_definition_see_also (see_also);
CREATE INDEX ix_type_definition_see_also_type_definition_name ON type_definition_see_also (type_definition_name);

CREATE TABLE type_definition_aliases (
	type_definition_name TEXT,
	aliases TEXT,
	PRIMARY KEY (type_definition_name, aliases),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_aliases_type_definition_name ON type_definition_aliases (type_definition_name);
CREATE INDEX ix_type_definition_aliases_aliases ON type_definition_aliases (aliases);

CREATE TABLE type_definition_mappings (
	type_definition_name TEXT,
	mappings TEXT,
	PRIMARY KEY (type_definition_name, mappings),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_mappings_mappings ON type_definition_mappings (mappings);
CREATE INDEX ix_type_definition_mappings_type_definition_name ON type_definition_mappings (type_definition_name);

CREATE TABLE type_definition_exact_mappings (
	type_definition_name TEXT,
	exact_mappings TEXT,
	PRIMARY KEY (type_definition_name, exact_mappings),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_exact_mappings_exact_mappings ON type_definition_exact_mappings (exact_mappings);
CREATE INDEX ix_type_definition_exact_mappings_type_definition_name ON type_definition_exact_mappings (type_definition_name);

CREATE TABLE type_definition_close_mappings (
	type_definition_name TEXT,
	close_mappings TEXT,
	PRIMARY KEY (type_definition_name, close_mappings),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_close_mappings_type_definition_name ON type_definition_close_mappings (type_definition_name);
CREATE INDEX ix_type_definition_close_mappings_close_mappings ON type_definition_close_mappings (close_mappings);

CREATE TABLE type_definition_related_mappings (
	type_definition_name TEXT,
	related_mappings TEXT,
	PRIMARY KEY (type_definition_name, related_mappings),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_related_mappings_type_definition_name ON type_definition_related_mappings (type_definition_name);
CREATE INDEX ix_type_definition_related_mappings_related_mappings ON type_definition_related_mappings (related_mappings);

CREATE TABLE type_definition_narrow_mappings (
	type_definition_name TEXT,
	narrow_mappings TEXT,
	PRIMARY KEY (type_definition_name, narrow_mappings),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_narrow_mappings_narrow_mappings ON type_definition_narrow_mappings (narrow_mappings);
CREATE INDEX ix_type_definition_narrow_mappings_type_definition_name ON type_definition_narrow_mappings (type_definition_name);

CREATE TABLE type_definition_broad_mappings (
	type_definition_name TEXT,
	broad_mappings TEXT,
	PRIMARY KEY (type_definition_name, broad_mappings),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_broad_mappings_type_definition_name ON type_definition_broad_mappings (type_definition_name);
CREATE INDEX ix_type_definition_broad_mappings_broad_mappings ON type_definition_broad_mappings (broad_mappings);

CREATE TABLE type_definition_contributors (
	type_definition_name TEXT,
	contributors TEXT,
	PRIMARY KEY (type_definition_name, contributors),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_contributors_contributors ON type_definition_contributors (contributors);
CREATE INDEX ix_type_definition_contributors_type_definition_name ON type_definition_contributors (type_definition_name);

CREATE TABLE type_definition_category (
	type_definition_name TEXT,
	category TEXT,
	PRIMARY KEY (type_definition_name, category),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_category_type_definition_name ON type_definition_category (type_definition_name);
CREATE INDEX ix_type_definition_category_category ON type_definition_category (category);

CREATE TABLE type_definition_keyword (
	type_definition_name TEXT,
	keyword TEXT,
	PRIMARY KEY (type_definition_name, keyword),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE INDEX ix_type_definition_keyword_type_definition_name ON type_definition_keyword (type_definition_name);
CREATE INDEX ix_type_definition_keyword_keyword ON type_definition_keyword (keyword);

CREATE TABLE definition_mixins (
	definition_name TEXT,
	mixins_name TEXT,
	PRIMARY KEY (definition_name, mixins_name),
	FOREIGN KEY(definition_name) REFERENCES definition (name),
	FOREIGN KEY(mixins_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_mixins_definition_name ON definition_mixins (definition_name);
CREATE INDEX ix_definition_mixins_mixins_name ON definition_mixins (mixins_name);

CREATE TABLE definition_apply_to (
	definition_name TEXT,
	apply_to_name TEXT,
	PRIMARY KEY (definition_name, apply_to_name),
	FOREIGN KEY(definition_name) REFERENCES definition (name),
	FOREIGN KEY(apply_to_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_apply_to_apply_to_name ON definition_apply_to (apply_to_name);
CREATE INDEX ix_definition_apply_to_definition_name ON definition_apply_to (definition_name);

CREATE TABLE definition_values_from (
	definition_name TEXT,
	values_from TEXT,
	PRIMARY KEY (definition_name, values_from),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_values_from_definition_name ON definition_values_from (definition_name);
CREATE INDEX ix_definition_values_from_values_from ON definition_values_from (values_from);

CREATE TABLE definition_id_prefixes (
	definition_name TEXT,
	id_prefixes TEXT,
	PRIMARY KEY (definition_name, id_prefixes),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_id_prefixes_definition_name ON definition_id_prefixes (definition_name);
CREATE INDEX ix_definition_id_prefixes_id_prefixes ON definition_id_prefixes (id_prefixes);

CREATE TABLE definition_implements (
	definition_name TEXT,
	implements TEXT,
	PRIMARY KEY (definition_name, implements),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_implements_implements ON definition_implements (implements);
CREATE INDEX ix_definition_implements_definition_name ON definition_implements (definition_name);

CREATE TABLE definition_instantiates (
	definition_name TEXT,
	instantiates TEXT,
	PRIMARY KEY (definition_name, instantiates),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_instantiates_definition_name ON definition_instantiates (definition_name);
CREATE INDEX ix_definition_instantiates_instantiates ON definition_instantiates (instantiates);

CREATE TABLE definition_todos (
	definition_name TEXT,
	todos TEXT,
	PRIMARY KEY (definition_name, todos),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_todos_todos ON definition_todos (todos);
CREATE INDEX ix_definition_todos_definition_name ON definition_todos (definition_name);

CREATE TABLE definition_notes (
	definition_name TEXT,
	notes TEXT,
	PRIMARY KEY (definition_name, notes),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_notes_definition_name ON definition_notes (definition_name);
CREATE INDEX ix_definition_notes_notes ON definition_notes (notes);

CREATE TABLE definition_comments (
	definition_name TEXT,
	comments TEXT,
	PRIMARY KEY (definition_name, comments),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_comments_comments ON definition_comments (comments);
CREATE INDEX ix_definition_comments_definition_name ON definition_comments (definition_name);

CREATE TABLE definition_see_also (
	definition_name TEXT,
	see_also TEXT,
	PRIMARY KEY (definition_name, see_also),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_see_also_see_also ON definition_see_also (see_also);
CREATE INDEX ix_definition_see_also_definition_name ON definition_see_also (definition_name);

CREATE TABLE definition_aliases (
	definition_name TEXT,
	aliases TEXT,
	PRIMARY KEY (definition_name, aliases),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_aliases_definition_name ON definition_aliases (definition_name);
CREATE INDEX ix_definition_aliases_aliases ON definition_aliases (aliases);

CREATE TABLE definition_mappings (
	definition_name TEXT,
	mappings TEXT,
	PRIMARY KEY (definition_name, mappings),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_mappings_mappings ON definition_mappings (mappings);
CREATE INDEX ix_definition_mappings_definition_name ON definition_mappings (definition_name);

CREATE TABLE definition_exact_mappings (
	definition_name TEXT,
	exact_mappings TEXT,
	PRIMARY KEY (definition_name, exact_mappings),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_exact_mappings_definition_name ON definition_exact_mappings (definition_name);
CREATE INDEX ix_definition_exact_mappings_exact_mappings ON definition_exact_mappings (exact_mappings);

CREATE TABLE definition_close_mappings (
	definition_name TEXT,
	close_mappings TEXT,
	PRIMARY KEY (definition_name, close_mappings),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_close_mappings_close_mappings ON definition_close_mappings (close_mappings);
CREATE INDEX ix_definition_close_mappings_definition_name ON definition_close_mappings (definition_name);

CREATE TABLE definition_related_mappings (
	definition_name TEXT,
	related_mappings TEXT,
	PRIMARY KEY (definition_name, related_mappings),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_related_mappings_definition_name ON definition_related_mappings (definition_name);
CREATE INDEX ix_definition_related_mappings_related_mappings ON definition_related_mappings (related_mappings);

CREATE TABLE definition_narrow_mappings (
	definition_name TEXT,
	narrow_mappings TEXT,
	PRIMARY KEY (definition_name, narrow_mappings),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_narrow_mappings_narrow_mappings ON definition_narrow_mappings (narrow_mappings);
CREATE INDEX ix_definition_narrow_mappings_definition_name ON definition_narrow_mappings (definition_name);

CREATE TABLE definition_broad_mappings (
	definition_name TEXT,
	broad_mappings TEXT,
	PRIMARY KEY (definition_name, broad_mappings),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_broad_mappings_definition_name ON definition_broad_mappings (definition_name);
CREATE INDEX ix_definition_broad_mappings_broad_mappings ON definition_broad_mappings (broad_mappings);

CREATE TABLE definition_contributors (
	definition_name TEXT,
	contributors TEXT,
	PRIMARY KEY (definition_name, contributors),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_contributors_contributors ON definition_contributors (contributors);
CREATE INDEX ix_definition_contributors_definition_name ON definition_contributors (definition_name);

CREATE TABLE definition_category (
	definition_name TEXT,
	category TEXT,
	PRIMARY KEY (definition_name, category),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_category_category ON definition_category (category);
CREATE INDEX ix_definition_category_definition_name ON definition_category (definition_name);

CREATE TABLE definition_keyword (
	definition_name TEXT,
	keyword TEXT,
	PRIMARY KEY (definition_name, keyword),
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE INDEX ix_definition_keyword_definition_name ON definition_keyword (definition_name);
CREATE INDEX ix_definition_keyword_keyword ON definition_keyword (keyword);

CREATE TABLE reachability_query_source_nodes (
	reachability_query_id INTEGER,
	source_nodes TEXT,
	PRIMARY KEY (reachability_query_id, source_nodes),
	FOREIGN KEY(reachability_query_id) REFERENCES reachability_query (id)
);
CREATE INDEX ix_reachability_query_source_nodes_source_nodes ON reachability_query_source_nodes (source_nodes);
CREATE INDEX ix_reachability_query_source_nodes_reachability_query_id ON reachability_query_source_nodes (reachability_query_id);

CREATE TABLE reachability_query_relationship_types (
	reachability_query_id INTEGER,
	relationship_types TEXT,
	PRIMARY KEY (reachability_query_id, relationship_types),
	FOREIGN KEY(reachability_query_id) REFERENCES reachability_query (id)
);
CREATE INDEX ix_reachability_query_relationship_types_reachability_query_id ON reachability_query_relationship_types (reachability_query_id);
CREATE INDEX ix_reachability_query_relationship_types_relationship_types ON reachability_query_relationship_types (relationship_types);

CREATE TABLE anonymous_expression_todos (
	anonymous_expression_id INTEGER,
	todos TEXT,
	PRIMARY KEY (anonymous_expression_id, todos),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_todos_anonymous_expression_id ON anonymous_expression_todos (anonymous_expression_id);
CREATE INDEX ix_anonymous_expression_todos_todos ON anonymous_expression_todos (todos);

CREATE TABLE anonymous_expression_notes (
	anonymous_expression_id INTEGER,
	notes TEXT,
	PRIMARY KEY (anonymous_expression_id, notes),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_notes_notes ON anonymous_expression_notes (notes);
CREATE INDEX ix_anonymous_expression_notes_anonymous_expression_id ON anonymous_expression_notes (anonymous_expression_id);

CREATE TABLE anonymous_expression_comments (
	anonymous_expression_id INTEGER,
	comments TEXT,
	PRIMARY KEY (anonymous_expression_id, comments),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_comments_anonymous_expression_id ON anonymous_expression_comments (anonymous_expression_id);
CREATE INDEX ix_anonymous_expression_comments_comments ON anonymous_expression_comments (comments);

CREATE TABLE anonymous_expression_see_also (
	anonymous_expression_id INTEGER,
	see_also TEXT,
	PRIMARY KEY (anonymous_expression_id, see_also),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_see_also_anonymous_expression_id ON anonymous_expression_see_also (anonymous_expression_id);
CREATE INDEX ix_anonymous_expression_see_also_see_also ON anonymous_expression_see_also (see_also);

CREATE TABLE anonymous_expression_aliases (
	anonymous_expression_id INTEGER,
	aliases TEXT,
	PRIMARY KEY (anonymous_expression_id, aliases),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_aliases_aliases ON anonymous_expression_aliases (aliases);
CREATE INDEX ix_anonymous_expression_aliases_anonymous_expression_id ON anonymous_expression_aliases (anonymous_expression_id);

CREATE TABLE anonymous_expression_mappings (
	anonymous_expression_id INTEGER,
	mappings TEXT,
	PRIMARY KEY (anonymous_expression_id, mappings),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_mappings_anonymous_expression_id ON anonymous_expression_mappings (anonymous_expression_id);
CREATE INDEX ix_anonymous_expression_mappings_mappings ON anonymous_expression_mappings (mappings);

CREATE TABLE anonymous_expression_exact_mappings (
	anonymous_expression_id INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY (anonymous_expression_id, exact_mappings),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_exact_mappings_exact_mappings ON anonymous_expression_exact_mappings (exact_mappings);
CREATE INDEX ix_anonymous_expression_exact_mappings_anonymous_expression_id ON anonymous_expression_exact_mappings (anonymous_expression_id);

CREATE TABLE anonymous_expression_close_mappings (
	anonymous_expression_id INTEGER,
	close_mappings TEXT,
	PRIMARY KEY (anonymous_expression_id, close_mappings),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_close_mappings_anonymous_expression_id ON anonymous_expression_close_mappings (anonymous_expression_id);
CREATE INDEX ix_anonymous_expression_close_mappings_close_mappings ON anonymous_expression_close_mappings (close_mappings);

CREATE TABLE anonymous_expression_related_mappings (
	anonymous_expression_id INTEGER,
	related_mappings TEXT,
	PRIMARY KEY (anonymous_expression_id, related_mappings),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_related_mappings_related_mappings ON anonymous_expression_related_mappings (related_mappings);
CREATE INDEX ix_anonymous_expression_related_mappings_anonymous_expression_id ON anonymous_expression_related_mappings (anonymous_expression_id);

CREATE TABLE anonymous_expression_narrow_mappings (
	anonymous_expression_id INTEGER,
	narrow_mappings TEXT,
	PRIMARY KEY (anonymous_expression_id, narrow_mappings),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_narrow_mappings_anonymous_expression_id ON anonymous_expression_narrow_mappings (anonymous_expression_id);
CREATE INDEX ix_anonymous_expression_narrow_mappings_narrow_mappings ON anonymous_expression_narrow_mappings (narrow_mappings);

CREATE TABLE anonymous_expression_broad_mappings (
	anonymous_expression_id INTEGER,
	broad_mappings TEXT,
	PRIMARY KEY (anonymous_expression_id, broad_mappings),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_broad_mappings_broad_mappings ON anonymous_expression_broad_mappings (broad_mappings);
CREATE INDEX ix_anonymous_expression_broad_mappings_anonymous_expression_id ON anonymous_expression_broad_mappings (anonymous_expression_id);

CREATE TABLE anonymous_expression_contributors (
	anonymous_expression_id INTEGER,
	contributors TEXT,
	PRIMARY KEY (anonymous_expression_id, contributors),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_contributors_anonymous_expression_id ON anonymous_expression_contributors (anonymous_expression_id);
CREATE INDEX ix_anonymous_expression_contributors_contributors ON anonymous_expression_contributors (contributors);

CREATE TABLE anonymous_expression_category (
	anonymous_expression_id INTEGER,
	category TEXT,
	PRIMARY KEY (anonymous_expression_id, category),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_category_category ON anonymous_expression_category (category);
CREATE INDEX ix_anonymous_expression_category_anonymous_expression_id ON anonymous_expression_category (anonymous_expression_id);

CREATE TABLE anonymous_expression_keyword (
	anonymous_expression_id INTEGER,
	keyword TEXT,
	PRIMARY KEY (anonymous_expression_id, keyword),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE INDEX ix_anonymous_expression_keyword_keyword ON anonymous_expression_keyword (keyword);
CREATE INDEX ix_anonymous_expression_keyword_anonymous_expression_id ON anonymous_expression_keyword (anonymous_expression_id);

CREATE TABLE path_expression_none_of (
	path_expression_id INTEGER,
	none_of_id INTEGER,
	PRIMARY KEY (path_expression_id, none_of_id),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id),
	FOREIGN KEY(none_of_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_none_of_none_of_id ON path_expression_none_of (none_of_id);
CREATE INDEX ix_path_expression_none_of_path_expression_id ON path_expression_none_of (path_expression_id);

CREATE TABLE path_expression_any_of (
	path_expression_id INTEGER,
	any_of_id INTEGER,
	PRIMARY KEY (path_expression_id, any_of_id),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id),
	FOREIGN KEY(any_of_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_any_of_path_expression_id ON path_expression_any_of (path_expression_id);
CREATE INDEX ix_path_expression_any_of_any_of_id ON path_expression_any_of (any_of_id);

CREATE TABLE path_expression_all_of (
	path_expression_id INTEGER,
	all_of_id INTEGER,
	PRIMARY KEY (path_expression_id, all_of_id),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id),
	FOREIGN KEY(all_of_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_all_of_path_expression_id ON path_expression_all_of (path_expression_id);
CREATE INDEX ix_path_expression_all_of_all_of_id ON path_expression_all_of (all_of_id);

CREATE TABLE path_expression_exactly_one_of (
	path_expression_id INTEGER,
	exactly_one_of_id INTEGER,
	PRIMARY KEY (path_expression_id, exactly_one_of_id),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id),
	FOREIGN KEY(exactly_one_of_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_exactly_one_of_path_expression_id ON path_expression_exactly_one_of (path_expression_id);
CREATE INDEX ix_path_expression_exactly_one_of_exactly_one_of_id ON path_expression_exactly_one_of (exactly_one_of_id);

CREATE TABLE path_expression_todos (
	path_expression_id INTEGER,
	todos TEXT,
	PRIMARY KEY (path_expression_id, todos),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_todos_path_expression_id ON path_expression_todos (path_expression_id);
CREATE INDEX ix_path_expression_todos_todos ON path_expression_todos (todos);

CREATE TABLE path_expression_notes (
	path_expression_id INTEGER,
	notes TEXT,
	PRIMARY KEY (path_expression_id, notes),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_notes_notes ON path_expression_notes (notes);
CREATE INDEX ix_path_expression_notes_path_expression_id ON path_expression_notes (path_expression_id);

CREATE TABLE path_expression_comments (
	path_expression_id INTEGER,
	comments TEXT,
	PRIMARY KEY (path_expression_id, comments),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_comments_path_expression_id ON path_expression_comments (path_expression_id);
CREATE INDEX ix_path_expression_comments_comments ON path_expression_comments (comments);

CREATE TABLE path_expression_see_also (
	path_expression_id INTEGER,
	see_also TEXT,
	PRIMARY KEY (path_expression_id, see_also),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_see_also_path_expression_id ON path_expression_see_also (path_expression_id);
CREATE INDEX ix_path_expression_see_also_see_also ON path_expression_see_also (see_also);

CREATE TABLE path_expression_aliases (
	path_expression_id INTEGER,
	aliases TEXT,
	PRIMARY KEY (path_expression_id, aliases),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_aliases_aliases ON path_expression_aliases (aliases);
CREATE INDEX ix_path_expression_aliases_path_expression_id ON path_expression_aliases (path_expression_id);

CREATE TABLE path_expression_mappings (
	path_expression_id INTEGER,
	mappings TEXT,
	PRIMARY KEY (path_expression_id, mappings),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_mappings_mappings ON path_expression_mappings (mappings);
CREATE INDEX ix_path_expression_mappings_path_expression_id ON path_expression_mappings (path_expression_id);

CREATE TABLE path_expression_exact_mappings (
	path_expression_id INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY (path_expression_id, exact_mappings),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_exact_mappings_path_expression_id ON path_expression_exact_mappings (path_expression_id);
CREATE INDEX ix_path_expression_exact_mappings_exact_mappings ON path_expression_exact_mappings (exact_mappings);

CREATE TABLE path_expression_close_mappings (
	path_expression_id INTEGER,
	close_mappings TEXT,
	PRIMARY KEY (path_expression_id, close_mappings),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_close_mappings_close_mappings ON path_expression_close_mappings (close_mappings);
CREATE INDEX ix_path_expression_close_mappings_path_expression_id ON path_expression_close_mappings (path_expression_id);

CREATE TABLE path_expression_related_mappings (
	path_expression_id INTEGER,
	related_mappings TEXT,
	PRIMARY KEY (path_expression_id, related_mappings),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_related_mappings_related_mappings ON path_expression_related_mappings (related_mappings);
CREATE INDEX ix_path_expression_related_mappings_path_expression_id ON path_expression_related_mappings (path_expression_id);

CREATE TABLE path_expression_narrow_mappings (
	path_expression_id INTEGER,
	narrow_mappings TEXT,
	PRIMARY KEY (path_expression_id, narrow_mappings),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_narrow_mappings_path_expression_id ON path_expression_narrow_mappings (path_expression_id);
CREATE INDEX ix_path_expression_narrow_mappings_narrow_mappings ON path_expression_narrow_mappings (narrow_mappings);

CREATE TABLE path_expression_broad_mappings (
	path_expression_id INTEGER,
	broad_mappings TEXT,
	PRIMARY KEY (path_expression_id, broad_mappings),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_broad_mappings_broad_mappings ON path_expression_broad_mappings (broad_mappings);
CREATE INDEX ix_path_expression_broad_mappings_path_expression_id ON path_expression_broad_mappings (path_expression_id);

CREATE TABLE path_expression_contributors (
	path_expression_id INTEGER,
	contributors TEXT,
	PRIMARY KEY (path_expression_id, contributors),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_contributors_contributors ON path_expression_contributors (contributors);
CREATE INDEX ix_path_expression_contributors_path_expression_id ON path_expression_contributors (path_expression_id);

CREATE TABLE path_expression_category (
	path_expression_id INTEGER,
	category TEXT,
	PRIMARY KEY (path_expression_id, category),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_category_category ON path_expression_category (category);
CREATE INDEX ix_path_expression_category_path_expression_id ON path_expression_category (path_expression_id);

CREATE TABLE path_expression_keyword (
	path_expression_id INTEGER,
	keyword TEXT,
	PRIMARY KEY (path_expression_id, keyword),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE INDEX ix_path_expression_keyword_path_expression_id ON path_expression_keyword (path_expression_id);
CREATE INDEX ix_path_expression_keyword_keyword ON path_expression_keyword (keyword);

CREATE TABLE slot_definition_domain_of (
	slot_definition_name TEXT,
	domain_of_name TEXT,
	PRIMARY KEY (slot_definition_name, domain_of_name),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(domain_of_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_slot_definition_domain_of_domain_of_name ON slot_definition_domain_of (domain_of_name);
CREATE INDEX ix_slot_definition_domain_of_slot_definition_name ON slot_definition_domain_of (slot_definition_name);

CREATE TABLE slot_definition_disjoint_with (
	slot_definition_name TEXT,
	disjoint_with_name TEXT,
	PRIMARY KEY (slot_definition_name, disjoint_with_name),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(disjoint_with_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_disjoint_with_disjoint_with_name ON slot_definition_disjoint_with (disjoint_with_name);
CREATE INDEX ix_slot_definition_disjoint_with_slot_definition_name ON slot_definition_disjoint_with (slot_definition_name);

CREATE TABLE slot_definition_union_of (
	slot_definition_name TEXT,
	union_of_name TEXT,
	PRIMARY KEY (slot_definition_name, union_of_name),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(union_of_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_union_of_slot_definition_name ON slot_definition_union_of (slot_definition_name);
CREATE INDEX ix_slot_definition_union_of_union_of_name ON slot_definition_union_of (union_of_name);

CREATE TABLE slot_definition_equals_string_in (
	slot_definition_name TEXT,
	equals_string_in TEXT,
	PRIMARY KEY (slot_definition_name, equals_string_in),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_equals_string_in_equals_string_in ON slot_definition_equals_string_in (equals_string_in);
CREATE INDEX ix_slot_definition_equals_string_in_slot_definition_name ON slot_definition_equals_string_in (slot_definition_name);

CREATE TABLE slot_definition_mixins (
	slot_definition_name TEXT,
	mixins_name TEXT,
	PRIMARY KEY (slot_definition_name, mixins_name),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(mixins_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_mixins_slot_definition_name ON slot_definition_mixins (slot_definition_name);
CREATE INDEX ix_slot_definition_mixins_mixins_name ON slot_definition_mixins (mixins_name);

CREATE TABLE slot_definition_apply_to (
	slot_definition_name TEXT,
	apply_to_name TEXT,
	PRIMARY KEY (slot_definition_name, apply_to_name),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(apply_to_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_apply_to_apply_to_name ON slot_definition_apply_to (apply_to_name);
CREATE INDEX ix_slot_definition_apply_to_slot_definition_name ON slot_definition_apply_to (slot_definition_name);

CREATE TABLE slot_definition_values_from (
	slot_definition_name TEXT,
	values_from TEXT,
	PRIMARY KEY (slot_definition_name, values_from),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_values_from_values_from ON slot_definition_values_from (values_from);
CREATE INDEX ix_slot_definition_values_from_slot_definition_name ON slot_definition_values_from (slot_definition_name);

CREATE TABLE slot_definition_id_prefixes (
	slot_definition_name TEXT,
	id_prefixes TEXT,
	PRIMARY KEY (slot_definition_name, id_prefixes),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_id_prefixes_id_prefixes ON slot_definition_id_prefixes (id_prefixes);
CREATE INDEX ix_slot_definition_id_prefixes_slot_definition_name ON slot_definition_id_prefixes (slot_definition_name);

CREATE TABLE slot_definition_implements (
	slot_definition_name TEXT,
	implements TEXT,
	PRIMARY KEY (slot_definition_name, implements),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_implements_implements ON slot_definition_implements (implements);
CREATE INDEX ix_slot_definition_implements_slot_definition_name ON slot_definition_implements (slot_definition_name);

CREATE TABLE slot_definition_instantiates (
	slot_definition_name TEXT,
	instantiates TEXT,
	PRIMARY KEY (slot_definition_name, instantiates),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_instantiates_instantiates ON slot_definition_instantiates (instantiates);
CREATE INDEX ix_slot_definition_instantiates_slot_definition_name ON slot_definition_instantiates (slot_definition_name);

CREATE TABLE slot_definition_todos (
	slot_definition_name TEXT,
	todos TEXT,
	PRIMARY KEY (slot_definition_name, todos),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_todos_slot_definition_name ON slot_definition_todos (slot_definition_name);
CREATE INDEX ix_slot_definition_todos_todos ON slot_definition_todos (todos);

CREATE TABLE slot_definition_notes (
	slot_definition_name TEXT,
	notes TEXT,
	PRIMARY KEY (slot_definition_name, notes),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_notes_slot_definition_name ON slot_definition_notes (slot_definition_name);
CREATE INDEX ix_slot_definition_notes_notes ON slot_definition_notes (notes);

CREATE TABLE slot_definition_comments (
	slot_definition_name TEXT,
	comments TEXT,
	PRIMARY KEY (slot_definition_name, comments),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_comments_comments ON slot_definition_comments (comments);
CREATE INDEX ix_slot_definition_comments_slot_definition_name ON slot_definition_comments (slot_definition_name);

CREATE TABLE slot_definition_see_also (
	slot_definition_name TEXT,
	see_also TEXT,
	PRIMARY KEY (slot_definition_name, see_also),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_see_also_slot_definition_name ON slot_definition_see_also (slot_definition_name);
CREATE INDEX ix_slot_definition_see_also_see_also ON slot_definition_see_also (see_also);

CREATE TABLE slot_definition_aliases (
	slot_definition_name TEXT,
	aliases TEXT,
	PRIMARY KEY (slot_definition_name, aliases),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_aliases_slot_definition_name ON slot_definition_aliases (slot_definition_name);
CREATE INDEX ix_slot_definition_aliases_aliases ON slot_definition_aliases (aliases);

CREATE TABLE slot_definition_mappings (
	slot_definition_name TEXT,
	mappings TEXT,
	PRIMARY KEY (slot_definition_name, mappings),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_mappings_mappings ON slot_definition_mappings (mappings);
CREATE INDEX ix_slot_definition_mappings_slot_definition_name ON slot_definition_mappings (slot_definition_name);

CREATE TABLE slot_definition_exact_mappings (
	slot_definition_name TEXT,
	exact_mappings TEXT,
	PRIMARY KEY (slot_definition_name, exact_mappings),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_exact_mappings_exact_mappings ON slot_definition_exact_mappings (exact_mappings);
CREATE INDEX ix_slot_definition_exact_mappings_slot_definition_name ON slot_definition_exact_mappings (slot_definition_name);

CREATE TABLE slot_definition_close_mappings (
	slot_definition_name TEXT,
	close_mappings TEXT,
	PRIMARY KEY (slot_definition_name, close_mappings),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_close_mappings_slot_definition_name ON slot_definition_close_mappings (slot_definition_name);
CREATE INDEX ix_slot_definition_close_mappings_close_mappings ON slot_definition_close_mappings (close_mappings);

CREATE TABLE slot_definition_related_mappings (
	slot_definition_name TEXT,
	related_mappings TEXT,
	PRIMARY KEY (slot_definition_name, related_mappings),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_related_mappings_related_mappings ON slot_definition_related_mappings (related_mappings);
CREATE INDEX ix_slot_definition_related_mappings_slot_definition_name ON slot_definition_related_mappings (slot_definition_name);

CREATE TABLE slot_definition_narrow_mappings (
	slot_definition_name TEXT,
	narrow_mappings TEXT,
	PRIMARY KEY (slot_definition_name, narrow_mappings),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_narrow_mappings_slot_definition_name ON slot_definition_narrow_mappings (slot_definition_name);
CREATE INDEX ix_slot_definition_narrow_mappings_narrow_mappings ON slot_definition_narrow_mappings (narrow_mappings);

CREATE TABLE slot_definition_broad_mappings (
	slot_definition_name TEXT,
	broad_mappings TEXT,
	PRIMARY KEY (slot_definition_name, broad_mappings),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_broad_mappings_broad_mappings ON slot_definition_broad_mappings (broad_mappings);
CREATE INDEX ix_slot_definition_broad_mappings_slot_definition_name ON slot_definition_broad_mappings (slot_definition_name);

CREATE TABLE slot_definition_contributors (
	slot_definition_name TEXT,
	contributors TEXT,
	PRIMARY KEY (slot_definition_name, contributors),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_contributors_slot_definition_name ON slot_definition_contributors (slot_definition_name);
CREATE INDEX ix_slot_definition_contributors_contributors ON slot_definition_contributors (contributors);

CREATE TABLE slot_definition_category (
	slot_definition_name TEXT,
	category TEXT,
	PRIMARY KEY (slot_definition_name, category),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_category_slot_definition_name ON slot_definition_category (slot_definition_name);
CREATE INDEX ix_slot_definition_category_category ON slot_definition_category (category);

CREATE TABLE slot_definition_keyword (
	slot_definition_name TEXT,
	keyword TEXT,
	PRIMARY KEY (slot_definition_name, keyword),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_slot_definition_keyword_keyword ON slot_definition_keyword (keyword);
CREATE INDEX ix_slot_definition_keyword_slot_definition_name ON slot_definition_keyword (slot_definition_name);

CREATE TABLE class_expression_any_of (
	class_expression_id INTEGER,
	any_of_id INTEGER,
	PRIMARY KEY (class_expression_id, any_of_id),
	FOREIGN KEY(class_expression_id) REFERENCES class_expression (id),
	FOREIGN KEY(any_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_class_expression_any_of_any_of_id ON class_expression_any_of (any_of_id);
CREATE INDEX ix_class_expression_any_of_class_expression_id ON class_expression_any_of (class_expression_id);

CREATE TABLE class_expression_exactly_one_of (
	class_expression_id INTEGER,
	exactly_one_of_id INTEGER,
	PRIMARY KEY (class_expression_id, exactly_one_of_id),
	FOREIGN KEY(class_expression_id) REFERENCES class_expression (id),
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_class_expression_exactly_one_of_exactly_one_of_id ON class_expression_exactly_one_of (exactly_one_of_id);
CREATE INDEX ix_class_expression_exactly_one_of_class_expression_id ON class_expression_exactly_one_of (class_expression_id);

CREATE TABLE class_expression_none_of (
	class_expression_id INTEGER,
	none_of_id INTEGER,
	PRIMARY KEY (class_expression_id, none_of_id),
	FOREIGN KEY(class_expression_id) REFERENCES class_expression (id),
	FOREIGN KEY(none_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_class_expression_none_of_none_of_id ON class_expression_none_of (none_of_id);
CREATE INDEX ix_class_expression_none_of_class_expression_id ON class_expression_none_of (class_expression_id);

CREATE TABLE class_expression_all_of (
	class_expression_id INTEGER,
	all_of_id INTEGER,
	PRIMARY KEY (class_expression_id, all_of_id),
	FOREIGN KEY(class_expression_id) REFERENCES class_expression (id),
	FOREIGN KEY(all_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_class_expression_all_of_class_expression_id ON class_expression_all_of (class_expression_id);
CREATE INDEX ix_class_expression_all_of_all_of_id ON class_expression_all_of (all_of_id);

CREATE TABLE anonymous_class_expression_any_of (
	anonymous_class_expression_id INTEGER,
	any_of_id INTEGER,
	PRIMARY KEY (anonymous_class_expression_id, any_of_id),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(any_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_any_of_any_of_id ON anonymous_class_expression_any_of (any_of_id);
CREATE INDEX ix_anonymous_class_expression_any_of_anonymous_class_expression_id ON anonymous_class_expression_any_of (anonymous_class_expression_id);

CREATE TABLE anonymous_class_expression_exactly_one_of (
	anonymous_class_expression_id INTEGER,
	exactly_one_of_id INTEGER,
	PRIMARY KEY (anonymous_class_expression_id, exactly_one_of_id),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_exactly_one_of_exactly_one_of_id ON anonymous_class_expression_exactly_one_of (exactly_one_of_id);
CREATE INDEX ix_anonymous_class_expression_exactly_one_of_anonymous_class_expression_id ON anonymous_class_expression_exactly_one_of (anonymous_class_expression_id);

CREATE TABLE anonymous_class_expression_none_of (
	anonymous_class_expression_id INTEGER,
	none_of_id INTEGER,
	PRIMARY KEY (anonymous_class_expression_id, none_of_id),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(none_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_none_of_anonymous_class_expression_id ON anonymous_class_expression_none_of (anonymous_class_expression_id);
CREATE INDEX ix_anonymous_class_expression_none_of_none_of_id ON anonymous_class_expression_none_of (none_of_id);

CREATE TABLE anonymous_class_expression_all_of (
	anonymous_class_expression_id INTEGER,
	all_of_id INTEGER,
	PRIMARY KEY (anonymous_class_expression_id, all_of_id),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(all_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_all_of_all_of_id ON anonymous_class_expression_all_of (all_of_id);
CREATE INDEX ix_anonymous_class_expression_all_of_anonymous_class_expression_id ON anonymous_class_expression_all_of (anonymous_class_expression_id);

CREATE TABLE anonymous_class_expression_todos (
	anonymous_class_expression_id INTEGER,
	todos TEXT,
	PRIMARY KEY (anonymous_class_expression_id, todos),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_todos_todos ON anonymous_class_expression_todos (todos);
CREATE INDEX ix_anonymous_class_expression_todos_anonymous_class_expression_id ON anonymous_class_expression_todos (anonymous_class_expression_id);

CREATE TABLE anonymous_class_expression_notes (
	anonymous_class_expression_id INTEGER,
	notes TEXT,
	PRIMARY KEY (anonymous_class_expression_id, notes),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_notes_anonymous_class_expression_id ON anonymous_class_expression_notes (anonymous_class_expression_id);
CREATE INDEX ix_anonymous_class_expression_notes_notes ON anonymous_class_expression_notes (notes);

CREATE TABLE anonymous_class_expression_comments (
	anonymous_class_expression_id INTEGER,
	comments TEXT,
	PRIMARY KEY (anonymous_class_expression_id, comments),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_comments_anonymous_class_expression_id ON anonymous_class_expression_comments (anonymous_class_expression_id);
CREATE INDEX ix_anonymous_class_expression_comments_comments ON anonymous_class_expression_comments (comments);

CREATE TABLE anonymous_class_expression_see_also (
	anonymous_class_expression_id INTEGER,
	see_also TEXT,
	PRIMARY KEY (anonymous_class_expression_id, see_also),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_see_also_see_also ON anonymous_class_expression_see_also (see_also);
CREATE INDEX ix_anonymous_class_expression_see_also_anonymous_class_expression_id ON anonymous_class_expression_see_also (anonymous_class_expression_id);

CREATE TABLE anonymous_class_expression_aliases (
	anonymous_class_expression_id INTEGER,
	aliases TEXT,
	PRIMARY KEY (anonymous_class_expression_id, aliases),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_aliases_aliases ON anonymous_class_expression_aliases (aliases);
CREATE INDEX ix_anonymous_class_expression_aliases_anonymous_class_expression_id ON anonymous_class_expression_aliases (anonymous_class_expression_id);

CREATE TABLE anonymous_class_expression_mappings (
	anonymous_class_expression_id INTEGER,
	mappings TEXT,
	PRIMARY KEY (anonymous_class_expression_id, mappings),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_mappings_mappings ON anonymous_class_expression_mappings (mappings);
CREATE INDEX ix_anonymous_class_expression_mappings_anonymous_class_expression_id ON anonymous_class_expression_mappings (anonymous_class_expression_id);

CREATE TABLE anonymous_class_expression_exact_mappings (
	anonymous_class_expression_id INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY (anonymous_class_expression_id, exact_mappings),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_exact_mappings_anonymous_class_expression_id ON anonymous_class_expression_exact_mappings (anonymous_class_expression_id);
CREATE INDEX ix_anonymous_class_expression_exact_mappings_exact_mappings ON anonymous_class_expression_exact_mappings (exact_mappings);

CREATE TABLE anonymous_class_expression_close_mappings (
	anonymous_class_expression_id INTEGER,
	close_mappings TEXT,
	PRIMARY KEY (anonymous_class_expression_id, close_mappings),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_close_mappings_anonymous_class_expression_id ON anonymous_class_expression_close_mappings (anonymous_class_expression_id);
CREATE INDEX ix_anonymous_class_expression_close_mappings_close_mappings ON anonymous_class_expression_close_mappings (close_mappings);

CREATE TABLE anonymous_class_expression_related_mappings (
	anonymous_class_expression_id INTEGER,
	related_mappings TEXT,
	PRIMARY KEY (anonymous_class_expression_id, related_mappings),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_related_mappings_anonymous_class_expression_id ON anonymous_class_expression_related_mappings (anonymous_class_expression_id);
CREATE INDEX ix_anonymous_class_expression_related_mappings_related_mappings ON anonymous_class_expression_related_mappings (related_mappings);

CREATE TABLE anonymous_class_expression_narrow_mappings (
	anonymous_class_expression_id INTEGER,
	narrow_mappings TEXT,
	PRIMARY KEY (anonymous_class_expression_id, narrow_mappings),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_narrow_mappings_narrow_mappings ON anonymous_class_expression_narrow_mappings (narrow_mappings);
CREATE INDEX ix_anonymous_class_expression_narrow_mappings_anonymous_class_expression_id ON anonymous_class_expression_narrow_mappings (anonymous_class_expression_id);

CREATE TABLE anonymous_class_expression_broad_mappings (
	anonymous_class_expression_id INTEGER,
	broad_mappings TEXT,
	PRIMARY KEY (anonymous_class_expression_id, broad_mappings),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_broad_mappings_broad_mappings ON anonymous_class_expression_broad_mappings (broad_mappings);
CREATE INDEX ix_anonymous_class_expression_broad_mappings_anonymous_class_expression_id ON anonymous_class_expression_broad_mappings (anonymous_class_expression_id);

CREATE TABLE anonymous_class_expression_contributors (
	anonymous_class_expression_id INTEGER,
	contributors TEXT,
	PRIMARY KEY (anonymous_class_expression_id, contributors),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_contributors_contributors ON anonymous_class_expression_contributors (contributors);
CREATE INDEX ix_anonymous_class_expression_contributors_anonymous_class_expression_id ON anonymous_class_expression_contributors (anonymous_class_expression_id);

CREATE TABLE anonymous_class_expression_category (
	anonymous_class_expression_id INTEGER,
	category TEXT,
	PRIMARY KEY (anonymous_class_expression_id, category),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_category_anonymous_class_expression_id ON anonymous_class_expression_category (anonymous_class_expression_id);
CREATE INDEX ix_anonymous_class_expression_category_category ON anonymous_class_expression_category (category);

CREATE TABLE anonymous_class_expression_keyword (
	anonymous_class_expression_id INTEGER,
	keyword TEXT,
	PRIMARY KEY (anonymous_class_expression_id, keyword),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_anonymous_class_expression_keyword_keyword ON anonymous_class_expression_keyword (keyword);
CREATE INDEX ix_anonymous_class_expression_keyword_anonymous_class_expression_id ON anonymous_class_expression_keyword (anonymous_class_expression_id);

CREATE TABLE class_definition_slots (
	class_definition_name TEXT,
	slots_name TEXT,
	PRIMARY KEY (class_definition_name, slots_name),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(slots_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_class_definition_slots_class_definition_name ON class_definition_slots (class_definition_name);
CREATE INDEX ix_class_definition_slots_slots_name ON class_definition_slots (slots_name);

CREATE TABLE class_definition_union_of (
	class_definition_name TEXT,
	union_of_name TEXT,
	PRIMARY KEY (class_definition_name, union_of_name),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(union_of_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_union_of_class_definition_name ON class_definition_union_of (class_definition_name);
CREATE INDEX ix_class_definition_union_of_union_of_name ON class_definition_union_of (union_of_name);

CREATE TABLE class_definition_defining_slots (
	class_definition_name TEXT,
	defining_slots_name TEXT,
	PRIMARY KEY (class_definition_name, defining_slots_name),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(defining_slots_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_class_definition_defining_slots_defining_slots_name ON class_definition_defining_slots (defining_slots_name);
CREATE INDEX ix_class_definition_defining_slots_class_definition_name ON class_definition_defining_slots (class_definition_name);

CREATE TABLE class_definition_disjoint_with (
	class_definition_name TEXT,
	disjoint_with_name TEXT,
	PRIMARY KEY (class_definition_name, disjoint_with_name),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(disjoint_with_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_disjoint_with_class_definition_name ON class_definition_disjoint_with (class_definition_name);
CREATE INDEX ix_class_definition_disjoint_with_disjoint_with_name ON class_definition_disjoint_with (disjoint_with_name);

CREATE TABLE class_definition_any_of (
	class_definition_name TEXT,
	any_of_id INTEGER,
	PRIMARY KEY (class_definition_name, any_of_id),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(any_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_class_definition_any_of_any_of_id ON class_definition_any_of (any_of_id);
CREATE INDEX ix_class_definition_any_of_class_definition_name ON class_definition_any_of (class_definition_name);

CREATE TABLE class_definition_exactly_one_of (
	class_definition_name TEXT,
	exactly_one_of_id INTEGER,
	PRIMARY KEY (class_definition_name, exactly_one_of_id),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_class_definition_exactly_one_of_class_definition_name ON class_definition_exactly_one_of (class_definition_name);
CREATE INDEX ix_class_definition_exactly_one_of_exactly_one_of_id ON class_definition_exactly_one_of (exactly_one_of_id);

CREATE TABLE class_definition_none_of (
	class_definition_name TEXT,
	none_of_id INTEGER,
	PRIMARY KEY (class_definition_name, none_of_id),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(none_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_class_definition_none_of_none_of_id ON class_definition_none_of (none_of_id);
CREATE INDEX ix_class_definition_none_of_class_definition_name ON class_definition_none_of (class_definition_name);

CREATE TABLE class_definition_all_of (
	class_definition_name TEXT,
	all_of_id INTEGER,
	PRIMARY KEY (class_definition_name, all_of_id),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(all_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE INDEX ix_class_definition_all_of_class_definition_name ON class_definition_all_of (class_definition_name);
CREATE INDEX ix_class_definition_all_of_all_of_id ON class_definition_all_of (all_of_id);

CREATE TABLE class_definition_mixins (
	class_definition_name TEXT,
	mixins_name TEXT,
	PRIMARY KEY (class_definition_name, mixins_name),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(mixins_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_mixins_mixins_name ON class_definition_mixins (mixins_name);
CREATE INDEX ix_class_definition_mixins_class_definition_name ON class_definition_mixins (class_definition_name);

CREATE TABLE class_definition_apply_to (
	class_definition_name TEXT,
	apply_to_name TEXT,
	PRIMARY KEY (class_definition_name, apply_to_name),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(apply_to_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_apply_to_apply_to_name ON class_definition_apply_to (apply_to_name);
CREATE INDEX ix_class_definition_apply_to_class_definition_name ON class_definition_apply_to (class_definition_name);

CREATE TABLE class_definition_values_from (
	class_definition_name TEXT,
	values_from TEXT,
	PRIMARY KEY (class_definition_name, values_from),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_values_from_values_from ON class_definition_values_from (values_from);
CREATE INDEX ix_class_definition_values_from_class_definition_name ON class_definition_values_from (class_definition_name);

CREATE TABLE class_definition_id_prefixes (
	class_definition_name TEXT,
	id_prefixes TEXT,
	PRIMARY KEY (class_definition_name, id_prefixes),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_id_prefixes_id_prefixes ON class_definition_id_prefixes (id_prefixes);
CREATE INDEX ix_class_definition_id_prefixes_class_definition_name ON class_definition_id_prefixes (class_definition_name);

CREATE TABLE class_definition_implements (
	class_definition_name TEXT,
	implements TEXT,
	PRIMARY KEY (class_definition_name, implements),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_implements_class_definition_name ON class_definition_implements (class_definition_name);
CREATE INDEX ix_class_definition_implements_implements ON class_definition_implements (implements);

CREATE TABLE class_definition_instantiates (
	class_definition_name TEXT,
	instantiates TEXT,
	PRIMARY KEY (class_definition_name, instantiates),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_instantiates_instantiates ON class_definition_instantiates (instantiates);
CREATE INDEX ix_class_definition_instantiates_class_definition_name ON class_definition_instantiates (class_definition_name);

CREATE TABLE class_definition_todos (
	class_definition_name TEXT,
	todos TEXT,
	PRIMARY KEY (class_definition_name, todos),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_todos_class_definition_name ON class_definition_todos (class_definition_name);
CREATE INDEX ix_class_definition_todos_todos ON class_definition_todos (todos);

CREATE TABLE class_definition_notes (
	class_definition_name TEXT,
	notes TEXT,
	PRIMARY KEY (class_definition_name, notes),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_notes_notes ON class_definition_notes (notes);
CREATE INDEX ix_class_definition_notes_class_definition_name ON class_definition_notes (class_definition_name);

CREATE TABLE class_definition_comments (
	class_definition_name TEXT,
	comments TEXT,
	PRIMARY KEY (class_definition_name, comments),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_comments_comments ON class_definition_comments (comments);
CREATE INDEX ix_class_definition_comments_class_definition_name ON class_definition_comments (class_definition_name);

CREATE TABLE class_definition_see_also (
	class_definition_name TEXT,
	see_also TEXT,
	PRIMARY KEY (class_definition_name, see_also),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_see_also_see_also ON class_definition_see_also (see_also);
CREATE INDEX ix_class_definition_see_also_class_definition_name ON class_definition_see_also (class_definition_name);

CREATE TABLE class_definition_aliases (
	class_definition_name TEXT,
	aliases TEXT,
	PRIMARY KEY (class_definition_name, aliases),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_aliases_aliases ON class_definition_aliases (aliases);
CREATE INDEX ix_class_definition_aliases_class_definition_name ON class_definition_aliases (class_definition_name);

CREATE TABLE class_definition_mappings (
	class_definition_name TEXT,
	mappings TEXT,
	PRIMARY KEY (class_definition_name, mappings),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_mappings_class_definition_name ON class_definition_mappings (class_definition_name);
CREATE INDEX ix_class_definition_mappings_mappings ON class_definition_mappings (mappings);

CREATE TABLE class_definition_exact_mappings (
	class_definition_name TEXT,
	exact_mappings TEXT,
	PRIMARY KEY (class_definition_name, exact_mappings),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_exact_mappings_exact_mappings ON class_definition_exact_mappings (exact_mappings);
CREATE INDEX ix_class_definition_exact_mappings_class_definition_name ON class_definition_exact_mappings (class_definition_name);

CREATE TABLE class_definition_close_mappings (
	class_definition_name TEXT,
	close_mappings TEXT,
	PRIMARY KEY (class_definition_name, close_mappings),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_close_mappings_close_mappings ON class_definition_close_mappings (close_mappings);
CREATE INDEX ix_class_definition_close_mappings_class_definition_name ON class_definition_close_mappings (class_definition_name);

CREATE TABLE class_definition_related_mappings (
	class_definition_name TEXT,
	related_mappings TEXT,
	PRIMARY KEY (class_definition_name, related_mappings),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_related_mappings_related_mappings ON class_definition_related_mappings (related_mappings);
CREATE INDEX ix_class_definition_related_mappings_class_definition_name ON class_definition_related_mappings (class_definition_name);

CREATE TABLE class_definition_narrow_mappings (
	class_definition_name TEXT,
	narrow_mappings TEXT,
	PRIMARY KEY (class_definition_name, narrow_mappings),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_narrow_mappings_class_definition_name ON class_definition_narrow_mappings (class_definition_name);
CREATE INDEX ix_class_definition_narrow_mappings_narrow_mappings ON class_definition_narrow_mappings (narrow_mappings);

CREATE TABLE class_definition_broad_mappings (
	class_definition_name TEXT,
	broad_mappings TEXT,
	PRIMARY KEY (class_definition_name, broad_mappings),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_broad_mappings_class_definition_name ON class_definition_broad_mappings (class_definition_name);
CREATE INDEX ix_class_definition_broad_mappings_broad_mappings ON class_definition_broad_mappings (broad_mappings);

CREATE TABLE class_definition_contributors (
	class_definition_name TEXT,
	contributors TEXT,
	PRIMARY KEY (class_definition_name, contributors),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_contributors_class_definition_name ON class_definition_contributors (class_definition_name);
CREATE INDEX ix_class_definition_contributors_contributors ON class_definition_contributors (contributors);

CREATE TABLE class_definition_category (
	class_definition_name TEXT,
	category TEXT,
	PRIMARY KEY (class_definition_name, category),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_category_category ON class_definition_category (category);
CREATE INDEX ix_class_definition_category_class_definition_name ON class_definition_category (class_definition_name);

CREATE TABLE class_definition_keyword (
	class_definition_name TEXT,
	keyword TEXT,
	PRIMARY KEY (class_definition_name, keyword),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_class_definition_keyword_keyword ON class_definition_keyword (keyword);
CREATE INDEX ix_class_definition_keyword_class_definition_name ON class_definition_keyword (class_definition_name);

CREATE TABLE dimension_expression_todos (
	dimension_expression_id INTEGER,
	todos TEXT,
	PRIMARY KEY (dimension_expression_id, todos),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_todos_todos ON dimension_expression_todos (todos);
CREATE INDEX ix_dimension_expression_todos_dimension_expression_id ON dimension_expression_todos (dimension_expression_id);

CREATE TABLE dimension_expression_notes (
	dimension_expression_id INTEGER,
	notes TEXT,
	PRIMARY KEY (dimension_expression_id, notes),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_notes_dimension_expression_id ON dimension_expression_notes (dimension_expression_id);
CREATE INDEX ix_dimension_expression_notes_notes ON dimension_expression_notes (notes);

CREATE TABLE dimension_expression_comments (
	dimension_expression_id INTEGER,
	comments TEXT,
	PRIMARY KEY (dimension_expression_id, comments),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_comments_dimension_expression_id ON dimension_expression_comments (dimension_expression_id);
CREATE INDEX ix_dimension_expression_comments_comments ON dimension_expression_comments (comments);

CREATE TABLE dimension_expression_see_also (
	dimension_expression_id INTEGER,
	see_also TEXT,
	PRIMARY KEY (dimension_expression_id, see_also),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_see_also_dimension_expression_id ON dimension_expression_see_also (dimension_expression_id);
CREATE INDEX ix_dimension_expression_see_also_see_also ON dimension_expression_see_also (see_also);

CREATE TABLE dimension_expression_aliases (
	dimension_expression_id INTEGER,
	aliases TEXT,
	PRIMARY KEY (dimension_expression_id, aliases),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_aliases_dimension_expression_id ON dimension_expression_aliases (dimension_expression_id);
CREATE INDEX ix_dimension_expression_aliases_aliases ON dimension_expression_aliases (aliases);

CREATE TABLE dimension_expression_mappings (
	dimension_expression_id INTEGER,
	mappings TEXT,
	PRIMARY KEY (dimension_expression_id, mappings),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_mappings_mappings ON dimension_expression_mappings (mappings);
CREATE INDEX ix_dimension_expression_mappings_dimension_expression_id ON dimension_expression_mappings (dimension_expression_id);

CREATE TABLE dimension_expression_exact_mappings (
	dimension_expression_id INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY (dimension_expression_id, exact_mappings),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_exact_mappings_dimension_expression_id ON dimension_expression_exact_mappings (dimension_expression_id);
CREATE INDEX ix_dimension_expression_exact_mappings_exact_mappings ON dimension_expression_exact_mappings (exact_mappings);

CREATE TABLE dimension_expression_close_mappings (
	dimension_expression_id INTEGER,
	close_mappings TEXT,
	PRIMARY KEY (dimension_expression_id, close_mappings),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_close_mappings_close_mappings ON dimension_expression_close_mappings (close_mappings);
CREATE INDEX ix_dimension_expression_close_mappings_dimension_expression_id ON dimension_expression_close_mappings (dimension_expression_id);

CREATE TABLE dimension_expression_related_mappings (
	dimension_expression_id INTEGER,
	related_mappings TEXT,
	PRIMARY KEY (dimension_expression_id, related_mappings),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_related_mappings_related_mappings ON dimension_expression_related_mappings (related_mappings);
CREATE INDEX ix_dimension_expression_related_mappings_dimension_expression_id ON dimension_expression_related_mappings (dimension_expression_id);

CREATE TABLE dimension_expression_narrow_mappings (
	dimension_expression_id INTEGER,
	narrow_mappings TEXT,
	PRIMARY KEY (dimension_expression_id, narrow_mappings),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_narrow_mappings_dimension_expression_id ON dimension_expression_narrow_mappings (dimension_expression_id);
CREATE INDEX ix_dimension_expression_narrow_mappings_narrow_mappings ON dimension_expression_narrow_mappings (narrow_mappings);

CREATE TABLE dimension_expression_broad_mappings (
	dimension_expression_id INTEGER,
	broad_mappings TEXT,
	PRIMARY KEY (dimension_expression_id, broad_mappings),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_broad_mappings_broad_mappings ON dimension_expression_broad_mappings (broad_mappings);
CREATE INDEX ix_dimension_expression_broad_mappings_dimension_expression_id ON dimension_expression_broad_mappings (dimension_expression_id);

CREATE TABLE dimension_expression_contributors (
	dimension_expression_id INTEGER,
	contributors TEXT,
	PRIMARY KEY (dimension_expression_id, contributors),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_contributors_contributors ON dimension_expression_contributors (contributors);
CREATE INDEX ix_dimension_expression_contributors_dimension_expression_id ON dimension_expression_contributors (dimension_expression_id);

CREATE TABLE dimension_expression_category (
	dimension_expression_id INTEGER,
	category TEXT,
	PRIMARY KEY (dimension_expression_id, category),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_category_dimension_expression_id ON dimension_expression_category (dimension_expression_id);
CREATE INDEX ix_dimension_expression_category_category ON dimension_expression_category (category);

CREATE TABLE dimension_expression_keyword (
	dimension_expression_id INTEGER,
	keyword TEXT,
	PRIMARY KEY (dimension_expression_id, keyword),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_dimension_expression_keyword_keyword ON dimension_expression_keyword (keyword);
CREATE INDEX ix_dimension_expression_keyword_dimension_expression_id ON dimension_expression_keyword (dimension_expression_id);

CREATE TABLE pattern_expression_todos (
	pattern_expression_id INTEGER,
	todos TEXT,
	PRIMARY KEY (pattern_expression_id, todos),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_todos_pattern_expression_id ON pattern_expression_todos (pattern_expression_id);
CREATE INDEX ix_pattern_expression_todos_todos ON pattern_expression_todos (todos);

CREATE TABLE pattern_expression_notes (
	pattern_expression_id INTEGER,
	notes TEXT,
	PRIMARY KEY (pattern_expression_id, notes),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_notes_pattern_expression_id ON pattern_expression_notes (pattern_expression_id);
CREATE INDEX ix_pattern_expression_notes_notes ON pattern_expression_notes (notes);

CREATE TABLE pattern_expression_comments (
	pattern_expression_id INTEGER,
	comments TEXT,
	PRIMARY KEY (pattern_expression_id, comments),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_comments_comments ON pattern_expression_comments (comments);
CREATE INDEX ix_pattern_expression_comments_pattern_expression_id ON pattern_expression_comments (pattern_expression_id);

CREATE TABLE pattern_expression_see_also (
	pattern_expression_id INTEGER,
	see_also TEXT,
	PRIMARY KEY (pattern_expression_id, see_also),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_see_also_see_also ON pattern_expression_see_also (see_also);
CREATE INDEX ix_pattern_expression_see_also_pattern_expression_id ON pattern_expression_see_also (pattern_expression_id);

CREATE TABLE pattern_expression_aliases (
	pattern_expression_id INTEGER,
	aliases TEXT,
	PRIMARY KEY (pattern_expression_id, aliases),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_aliases_pattern_expression_id ON pattern_expression_aliases (pattern_expression_id);
CREATE INDEX ix_pattern_expression_aliases_aliases ON pattern_expression_aliases (aliases);

CREATE TABLE pattern_expression_mappings (
	pattern_expression_id INTEGER,
	mappings TEXT,
	PRIMARY KEY (pattern_expression_id, mappings),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_mappings_pattern_expression_id ON pattern_expression_mappings (pattern_expression_id);
CREATE INDEX ix_pattern_expression_mappings_mappings ON pattern_expression_mappings (mappings);

CREATE TABLE pattern_expression_exact_mappings (
	pattern_expression_id INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY (pattern_expression_id, exact_mappings),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_exact_mappings_exact_mappings ON pattern_expression_exact_mappings (exact_mappings);
CREATE INDEX ix_pattern_expression_exact_mappings_pattern_expression_id ON pattern_expression_exact_mappings (pattern_expression_id);

CREATE TABLE pattern_expression_close_mappings (
	pattern_expression_id INTEGER,
	close_mappings TEXT,
	PRIMARY KEY (pattern_expression_id, close_mappings),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_close_mappings_close_mappings ON pattern_expression_close_mappings (close_mappings);
CREATE INDEX ix_pattern_expression_close_mappings_pattern_expression_id ON pattern_expression_close_mappings (pattern_expression_id);

CREATE TABLE pattern_expression_related_mappings (
	pattern_expression_id INTEGER,
	related_mappings TEXT,
	PRIMARY KEY (pattern_expression_id, related_mappings),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_related_mappings_pattern_expression_id ON pattern_expression_related_mappings (pattern_expression_id);
CREATE INDEX ix_pattern_expression_related_mappings_related_mappings ON pattern_expression_related_mappings (related_mappings);

CREATE TABLE pattern_expression_narrow_mappings (
	pattern_expression_id INTEGER,
	narrow_mappings TEXT,
	PRIMARY KEY (pattern_expression_id, narrow_mappings),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_narrow_mappings_pattern_expression_id ON pattern_expression_narrow_mappings (pattern_expression_id);
CREATE INDEX ix_pattern_expression_narrow_mappings_narrow_mappings ON pattern_expression_narrow_mappings (narrow_mappings);

CREATE TABLE pattern_expression_broad_mappings (
	pattern_expression_id INTEGER,
	broad_mappings TEXT,
	PRIMARY KEY (pattern_expression_id, broad_mappings),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_broad_mappings_pattern_expression_id ON pattern_expression_broad_mappings (pattern_expression_id);
CREATE INDEX ix_pattern_expression_broad_mappings_broad_mappings ON pattern_expression_broad_mappings (broad_mappings);

CREATE TABLE pattern_expression_contributors (
	pattern_expression_id INTEGER,
	contributors TEXT,
	PRIMARY KEY (pattern_expression_id, contributors),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_contributors_contributors ON pattern_expression_contributors (contributors);
CREATE INDEX ix_pattern_expression_contributors_pattern_expression_id ON pattern_expression_contributors (pattern_expression_id);

CREATE TABLE pattern_expression_category (
	pattern_expression_id INTEGER,
	category TEXT,
	PRIMARY KEY (pattern_expression_id, category),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_category_pattern_expression_id ON pattern_expression_category (pattern_expression_id);
CREATE INDEX ix_pattern_expression_category_category ON pattern_expression_category (category);

CREATE TABLE pattern_expression_keyword (
	pattern_expression_id INTEGER,
	keyword TEXT,
	PRIMARY KEY (pattern_expression_id, keyword),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE INDEX ix_pattern_expression_keyword_keyword ON pattern_expression_keyword (keyword);
CREATE INDEX ix_pattern_expression_keyword_pattern_expression_id ON pattern_expression_keyword (pattern_expression_id);

CREATE TABLE import_expression_todos (
	import_expression_id INTEGER,
	todos TEXT,
	PRIMARY KEY (import_expression_id, todos),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_todos_todos ON import_expression_todos (todos);
CREATE INDEX ix_import_expression_todos_import_expression_id ON import_expression_todos (import_expression_id);

CREATE TABLE import_expression_notes (
	import_expression_id INTEGER,
	notes TEXT,
	PRIMARY KEY (import_expression_id, notes),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_notes_notes ON import_expression_notes (notes);
CREATE INDEX ix_import_expression_notes_import_expression_id ON import_expression_notes (import_expression_id);

CREATE TABLE import_expression_comments (
	import_expression_id INTEGER,
	comments TEXT,
	PRIMARY KEY (import_expression_id, comments),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_comments_comments ON import_expression_comments (comments);
CREATE INDEX ix_import_expression_comments_import_expression_id ON import_expression_comments (import_expression_id);

CREATE TABLE import_expression_see_also (
	import_expression_id INTEGER,
	see_also TEXT,
	PRIMARY KEY (import_expression_id, see_also),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_see_also_import_expression_id ON import_expression_see_also (import_expression_id);
CREATE INDEX ix_import_expression_see_also_see_also ON import_expression_see_also (see_also);

CREATE TABLE import_expression_aliases (
	import_expression_id INTEGER,
	aliases TEXT,
	PRIMARY KEY (import_expression_id, aliases),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_aliases_aliases ON import_expression_aliases (aliases);
CREATE INDEX ix_import_expression_aliases_import_expression_id ON import_expression_aliases (import_expression_id);

CREATE TABLE import_expression_mappings (
	import_expression_id INTEGER,
	mappings TEXT,
	PRIMARY KEY (import_expression_id, mappings),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_mappings_mappings ON import_expression_mappings (mappings);
CREATE INDEX ix_import_expression_mappings_import_expression_id ON import_expression_mappings (import_expression_id);

CREATE TABLE import_expression_exact_mappings (
	import_expression_id INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY (import_expression_id, exact_mappings),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_exact_mappings_import_expression_id ON import_expression_exact_mappings (import_expression_id);
CREATE INDEX ix_import_expression_exact_mappings_exact_mappings ON import_expression_exact_mappings (exact_mappings);

CREATE TABLE import_expression_close_mappings (
	import_expression_id INTEGER,
	close_mappings TEXT,
	PRIMARY KEY (import_expression_id, close_mappings),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_close_mappings_close_mappings ON import_expression_close_mappings (close_mappings);
CREATE INDEX ix_import_expression_close_mappings_import_expression_id ON import_expression_close_mappings (import_expression_id);

CREATE TABLE import_expression_related_mappings (
	import_expression_id INTEGER,
	related_mappings TEXT,
	PRIMARY KEY (import_expression_id, related_mappings),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_related_mappings_related_mappings ON import_expression_related_mappings (related_mappings);
CREATE INDEX ix_import_expression_related_mappings_import_expression_id ON import_expression_related_mappings (import_expression_id);

CREATE TABLE import_expression_narrow_mappings (
	import_expression_id INTEGER,
	narrow_mappings TEXT,
	PRIMARY KEY (import_expression_id, narrow_mappings),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_narrow_mappings_import_expression_id ON import_expression_narrow_mappings (import_expression_id);
CREATE INDEX ix_import_expression_narrow_mappings_narrow_mappings ON import_expression_narrow_mappings (narrow_mappings);

CREATE TABLE import_expression_broad_mappings (
	import_expression_id INTEGER,
	broad_mappings TEXT,
	PRIMARY KEY (import_expression_id, broad_mappings),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_broad_mappings_broad_mappings ON import_expression_broad_mappings (broad_mappings);
CREATE INDEX ix_import_expression_broad_mappings_import_expression_id ON import_expression_broad_mappings (import_expression_id);

CREATE TABLE import_expression_contributors (
	import_expression_id INTEGER,
	contributors TEXT,
	PRIMARY KEY (import_expression_id, contributors),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_contributors_import_expression_id ON import_expression_contributors (import_expression_id);
CREATE INDEX ix_import_expression_contributors_contributors ON import_expression_contributors (contributors);

CREATE TABLE import_expression_category (
	import_expression_id INTEGER,
	category TEXT,
	PRIMARY KEY (import_expression_id, category),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_category_import_expression_id ON import_expression_category (import_expression_id);
CREATE INDEX ix_import_expression_category_category ON import_expression_category (category);

CREATE TABLE import_expression_keyword (
	import_expression_id INTEGER,
	keyword TEXT,
	PRIMARY KEY (import_expression_id, keyword),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE INDEX ix_import_expression_keyword_keyword ON import_expression_keyword (keyword);
CREATE INDEX ix_import_expression_keyword_import_expression_id ON import_expression_keyword (import_expression_id);

CREATE TABLE "UnitOfMeasure_exact_mappings" (
	"UnitOfMeasure_id" INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY ("UnitOfMeasure_id", exact_mappings),
	FOREIGN KEY("UnitOfMeasure_id") REFERENCES "UnitOfMeasure" (id)
);
CREATE INDEX "ix_UnitOfMeasure_exact_mappings_UnitOfMeasure_id" ON "UnitOfMeasure_exact_mappings" ("UnitOfMeasure_id");
CREATE INDEX "ix_UnitOfMeasure_exact_mappings_exact_mappings" ON "UnitOfMeasure_exact_mappings" (exact_mappings);

CREATE TABLE anonymous_slot_expression (
	id INTEGER NOT NULL,
	range TEXT,
	required BOOLEAN,
	recommended BOOLEAN,
	multivalued BOOLEAN,
	inlined BOOLEAN,
	inlined_as_list BOOLEAN,
	pattern TEXT,
	implicit_prefix TEXT,
	value_presence VARCHAR(11),
	equals_string TEXT,
	equals_number INTEGER,
	equals_expression TEXT,
	exact_cardinality INTEGER,
	minimum_cardinality INTEGER,
	maximum_cardinality INTEGER,
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	range_expression_id INTEGER,
	enum_range_id INTEGER,
	minimum_value_id INTEGER,
	maximum_value_id INTEGER,
	structured_pattern_id INTEGER,
	unit_id INTEGER,
	has_member_id INTEGER,
	all_members_id INTEGER,
	array_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(range) REFERENCES element (name),
	FOREIGN KEY(range_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(enum_range_id) REFERENCES enum_expression (id),
	FOREIGN KEY(minimum_value_id) REFERENCES "Anything" (id),
	FOREIGN KEY(maximum_value_id) REFERENCES "Anything" (id),
	FOREIGN KEY(structured_pattern_id) REFERENCES pattern_expression (id),
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id),
	FOREIGN KEY(has_member_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(all_members_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(array_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_id ON anonymous_slot_expression (id);

CREATE TABLE local_name (
	local_name_source TEXT NOT NULL,
	local_name_value TEXT NOT NULL,
	element_name TEXT,
	schema_definition_name TEXT,
	type_definition_name TEXT,
	subset_definition_name TEXT,
	definition_name TEXT,
	enum_definition_name TEXT,
	slot_definition_name TEXT,
	class_definition_name TEXT,
	PRIMARY KEY (local_name_source, local_name_value, element_name, schema_definition_name, type_definition_name, subset_definition_name, definition_name, enum_definition_name, slot_definition_name, class_definition_name),
	UNIQUE (element_name, local_name_source),
	UNIQUE (schema_definition_name, local_name_source),
	UNIQUE (type_definition_name, local_name_source),
	UNIQUE (subset_definition_name, local_name_source),
	UNIQUE (definition_name, local_name_source),
	UNIQUE (enum_definition_name, local_name_source),
	UNIQUE (slot_definition_name, local_name_source),
	UNIQUE (class_definition_name, local_name_source),
	FOREIGN KEY(element_name) REFERENCES element (name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name),
	FOREIGN KEY(definition_name) REFERENCES definition (name),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE INDEX ix_local_name_local_name_source ON local_name (local_name_source);
CREATE INDEX ix_local_name_slot_definition_name ON local_name (slot_definition_name);
CREATE INDEX local_name_class_definition_name_local_name_source_idx ON local_name (class_definition_name, local_name_source);
CREATE INDEX ix_local_name_enum_definition_name ON local_name (enum_definition_name);
CREATE INDEX local_name_schema_definition_name_local_name_source_idx ON local_name (schema_definition_name, local_name_source);
CREATE INDEX local_name_type_definition_name_local_name_source_idx ON local_name (type_definition_name, local_name_source);
CREATE INDEX local_name_subset_definition_name_local_name_source_idx ON local_name (subset_definition_name, local_name_source);
CREATE INDEX ix_local_name_schema_definition_name ON local_name (schema_definition_name);
CREATE INDEX local_name_definition_name_local_name_source_idx ON local_name (definition_name, local_name_source);
CREATE INDEX ix_local_name_subset_definition_name ON local_name (subset_definition_name);
CREATE INDEX local_name_element_name_local_name_source_idx ON local_name (element_name, local_name_source);
CREATE INDEX local_name_enum_definition_name_local_name_source_idx ON local_name (enum_definition_name, local_name_source);
CREATE INDEX local_name_slot_definition_name_local_name_source_idx ON local_name (slot_definition_name, local_name_source);
CREATE INDEX ix_local_name_local_name_value ON local_name (local_name_value);
CREATE INDEX ix_local_name_class_definition_name ON local_name (class_definition_name);
CREATE INDEX ix_local_name_definition_name ON local_name (definition_name);
CREATE INDEX ix_local_name_type_definition_name ON local_name (type_definition_name);
CREATE INDEX ix_local_name_element_name ON local_name (element_name);

CREATE TABLE permissible_value (
	text TEXT NOT NULL,
	description TEXT,
	meaning TEXT,
	is_a TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	enum_expression_id INTEGER,
	anonymous_enum_expression_id INTEGER,
	enum_definition_name TEXT,
	unit_id INTEGER,
	PRIMARY KEY (text),
	FOREIGN KEY(is_a) REFERENCES permissible_value (text),
	FOREIGN KEY(enum_expression_id) REFERENCES enum_expression (id),
	FOREIGN KEY(anonymous_enum_expression_id) REFERENCES anonymous_enum_expression (id),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id)
);
CREATE INDEX ix_permissible_value_text ON permissible_value (text);

CREATE TABLE common_metadata_in_subset (
	common_metadata_id INTEGER,
	in_subset_name TEXT,
	PRIMARY KEY (common_metadata_id, in_subset_name),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_common_metadata_in_subset_common_metadata_id ON common_metadata_in_subset (common_metadata_id);
CREATE INDEX ix_common_metadata_in_subset_in_subset_name ON common_metadata_in_subset (in_subset_name);

CREATE TABLE element_in_subset (
	element_name TEXT,
	in_subset_name TEXT,
	PRIMARY KEY (element_name, in_subset_name),
	FOREIGN KEY(element_name) REFERENCES element (name),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_element_in_subset_in_subset_name ON element_in_subset (in_subset_name);
CREATE INDEX ix_element_in_subset_element_name ON element_in_subset (element_name);

CREATE TABLE schema_definition_in_subset (
	schema_definition_name TEXT,
	in_subset_name TEXT,
	PRIMARY KEY (schema_definition_name, in_subset_name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_schema_definition_in_subset_schema_definition_name ON schema_definition_in_subset (schema_definition_name);
CREATE INDEX ix_schema_definition_in_subset_in_subset_name ON schema_definition_in_subset (in_subset_name);

CREATE TABLE type_expression_equals_string_in (
	type_expression_id INTEGER,
	equals_string_in TEXT,
	PRIMARY KEY (type_expression_id, equals_string_in),
	FOREIGN KEY(type_expression_id) REFERENCES type_expression (id)
);
CREATE INDEX ix_type_expression_equals_string_in_type_expression_id ON type_expression_equals_string_in (type_expression_id);
CREATE INDEX ix_type_expression_equals_string_in_equals_string_in ON type_expression_equals_string_in (equals_string_in);

CREATE TABLE type_expression_none_of (
	type_expression_id INTEGER,
	none_of_id INTEGER,
	PRIMARY KEY (type_expression_id, none_of_id),
	FOREIGN KEY(type_expression_id) REFERENCES type_expression (id),
	FOREIGN KEY(none_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_type_expression_none_of_none_of_id ON type_expression_none_of (none_of_id);
CREATE INDEX ix_type_expression_none_of_type_expression_id ON type_expression_none_of (type_expression_id);

CREATE TABLE type_expression_exactly_one_of (
	type_expression_id INTEGER,
	exactly_one_of_id INTEGER,
	PRIMARY KEY (type_expression_id, exactly_one_of_id),
	FOREIGN KEY(type_expression_id) REFERENCES type_expression (id),
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_type_expression_exactly_one_of_type_expression_id ON type_expression_exactly_one_of (type_expression_id);
CREATE INDEX ix_type_expression_exactly_one_of_exactly_one_of_id ON type_expression_exactly_one_of (exactly_one_of_id);

CREATE TABLE type_expression_any_of (
	type_expression_id INTEGER,
	any_of_id INTEGER,
	PRIMARY KEY (type_expression_id, any_of_id),
	FOREIGN KEY(type_expression_id) REFERENCES type_expression (id),
	FOREIGN KEY(any_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_type_expression_any_of_type_expression_id ON type_expression_any_of (type_expression_id);
CREATE INDEX ix_type_expression_any_of_any_of_id ON type_expression_any_of (any_of_id);

CREATE TABLE type_expression_all_of (
	type_expression_id INTEGER,
	all_of_id INTEGER,
	PRIMARY KEY (type_expression_id, all_of_id),
	FOREIGN KEY(type_expression_id) REFERENCES type_expression (id),
	FOREIGN KEY(all_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_type_expression_all_of_type_expression_id ON type_expression_all_of (type_expression_id);
CREATE INDEX ix_type_expression_all_of_all_of_id ON type_expression_all_of (all_of_id);

CREATE TABLE anonymous_type_expression_equals_string_in (
	anonymous_type_expression_id INTEGER,
	equals_string_in TEXT,
	PRIMARY KEY (anonymous_type_expression_id, equals_string_in),
	FOREIGN KEY(anonymous_type_expression_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_anonymous_type_expression_equals_string_in_equals_string_in ON anonymous_type_expression_equals_string_in (equals_string_in);
CREATE INDEX ix_anonymous_type_expression_equals_string_in_anonymous_type_expression_id ON anonymous_type_expression_equals_string_in (anonymous_type_expression_id);

CREATE TABLE anonymous_type_expression_none_of (
	anonymous_type_expression_id INTEGER,
	none_of_id INTEGER,
	PRIMARY KEY (anonymous_type_expression_id, none_of_id),
	FOREIGN KEY(anonymous_type_expression_id) REFERENCES anonymous_type_expression (id),
	FOREIGN KEY(none_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_anonymous_type_expression_none_of_anonymous_type_expression_id ON anonymous_type_expression_none_of (anonymous_type_expression_id);
CREATE INDEX ix_anonymous_type_expression_none_of_none_of_id ON anonymous_type_expression_none_of (none_of_id);

CREATE TABLE anonymous_type_expression_exactly_one_of (
	anonymous_type_expression_id INTEGER,
	exactly_one_of_id INTEGER,
	PRIMARY KEY (anonymous_type_expression_id, exactly_one_of_id),
	FOREIGN KEY(anonymous_type_expression_id) REFERENCES anonymous_type_expression (id),
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_anonymous_type_expression_exactly_one_of_anonymous_type_expression_id ON anonymous_type_expression_exactly_one_of (anonymous_type_expression_id);
CREATE INDEX ix_anonymous_type_expression_exactly_one_of_exactly_one_of_id ON anonymous_type_expression_exactly_one_of (exactly_one_of_id);

CREATE TABLE anonymous_type_expression_any_of (
	anonymous_type_expression_id INTEGER,
	any_of_id INTEGER,
	PRIMARY KEY (anonymous_type_expression_id, any_of_id),
	FOREIGN KEY(anonymous_type_expression_id) REFERENCES anonymous_type_expression (id),
	FOREIGN KEY(any_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_anonymous_type_expression_any_of_anonymous_type_expression_id ON anonymous_type_expression_any_of (anonymous_type_expression_id);
CREATE INDEX ix_anonymous_type_expression_any_of_any_of_id ON anonymous_type_expression_any_of (any_of_id);

CREATE TABLE anonymous_type_expression_all_of (
	anonymous_type_expression_id INTEGER,
	all_of_id INTEGER,
	PRIMARY KEY (anonymous_type_expression_id, all_of_id),
	FOREIGN KEY(anonymous_type_expression_id) REFERENCES anonymous_type_expression (id),
	FOREIGN KEY(all_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_anonymous_type_expression_all_of_anonymous_type_expression_id ON anonymous_type_expression_all_of (anonymous_type_expression_id);
CREATE INDEX ix_anonymous_type_expression_all_of_all_of_id ON anonymous_type_expression_all_of (all_of_id);

CREATE TABLE type_definition_none_of (
	type_definition_name TEXT,
	none_of_id INTEGER,
	PRIMARY KEY (type_definition_name, none_of_id),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name),
	FOREIGN KEY(none_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_type_definition_none_of_type_definition_name ON type_definition_none_of (type_definition_name);
CREATE INDEX ix_type_definition_none_of_none_of_id ON type_definition_none_of (none_of_id);

CREATE TABLE type_definition_exactly_one_of (
	type_definition_name TEXT,
	exactly_one_of_id INTEGER,
	PRIMARY KEY (type_definition_name, exactly_one_of_id),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name),
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_type_definition_exactly_one_of_exactly_one_of_id ON type_definition_exactly_one_of (exactly_one_of_id);
CREATE INDEX ix_type_definition_exactly_one_of_type_definition_name ON type_definition_exactly_one_of (type_definition_name);

CREATE TABLE type_definition_any_of (
	type_definition_name TEXT,
	any_of_id INTEGER,
	PRIMARY KEY (type_definition_name, any_of_id),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name),
	FOREIGN KEY(any_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_type_definition_any_of_type_definition_name ON type_definition_any_of (type_definition_name);
CREATE INDEX ix_type_definition_any_of_any_of_id ON type_definition_any_of (any_of_id);

CREATE TABLE type_definition_all_of (
	type_definition_name TEXT,
	all_of_id INTEGER,
	PRIMARY KEY (type_definition_name, all_of_id),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name),
	FOREIGN KEY(all_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE INDEX ix_type_definition_all_of_all_of_id ON type_definition_all_of (all_of_id);
CREATE INDEX ix_type_definition_all_of_type_definition_name ON type_definition_all_of (type_definition_name);

CREATE TABLE type_definition_in_subset (
	type_definition_name TEXT,
	in_subset_name TEXT,
	PRIMARY KEY (type_definition_name, in_subset_name),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_type_definition_in_subset_type_definition_name ON type_definition_in_subset (type_definition_name);
CREATE INDEX ix_type_definition_in_subset_in_subset_name ON type_definition_in_subset (in_subset_name);

CREATE TABLE subset_definition_id_prefixes (
	subset_definition_name TEXT,
	id_prefixes TEXT,
	PRIMARY KEY (subset_definition_name, id_prefixes),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_id_prefixes_subset_definition_name ON subset_definition_id_prefixes (subset_definition_name);
CREATE INDEX ix_subset_definition_id_prefixes_id_prefixes ON subset_definition_id_prefixes (id_prefixes);

CREATE TABLE subset_definition_implements (
	subset_definition_name TEXT,
	implements TEXT,
	PRIMARY KEY (subset_definition_name, implements),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_implements_subset_definition_name ON subset_definition_implements (subset_definition_name);
CREATE INDEX ix_subset_definition_implements_implements ON subset_definition_implements (implements);

CREATE TABLE subset_definition_instantiates (
	subset_definition_name TEXT,
	instantiates TEXT,
	PRIMARY KEY (subset_definition_name, instantiates),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_instantiates_subset_definition_name ON subset_definition_instantiates (subset_definition_name);
CREATE INDEX ix_subset_definition_instantiates_instantiates ON subset_definition_instantiates (instantiates);

CREATE TABLE subset_definition_todos (
	subset_definition_name TEXT,
	todos TEXT,
	PRIMARY KEY (subset_definition_name, todos),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_todos_todos ON subset_definition_todos (todos);
CREATE INDEX ix_subset_definition_todos_subset_definition_name ON subset_definition_todos (subset_definition_name);

CREATE TABLE subset_definition_notes (
	subset_definition_name TEXT,
	notes TEXT,
	PRIMARY KEY (subset_definition_name, notes),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_notes_notes ON subset_definition_notes (notes);
CREATE INDEX ix_subset_definition_notes_subset_definition_name ON subset_definition_notes (subset_definition_name);

CREATE TABLE subset_definition_comments (
	subset_definition_name TEXT,
	comments TEXT,
	PRIMARY KEY (subset_definition_name, comments),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_comments_subset_definition_name ON subset_definition_comments (subset_definition_name);
CREATE INDEX ix_subset_definition_comments_comments ON subset_definition_comments (comments);

CREATE TABLE subset_definition_in_subset (
	subset_definition_name TEXT,
	in_subset_name TEXT,
	PRIMARY KEY (subset_definition_name, in_subset_name),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_in_subset_subset_definition_name ON subset_definition_in_subset (subset_definition_name);
CREATE INDEX ix_subset_definition_in_subset_in_subset_name ON subset_definition_in_subset (in_subset_name);

CREATE TABLE subset_definition_see_also (
	subset_definition_name TEXT,
	see_also TEXT,
	PRIMARY KEY (subset_definition_name, see_also),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_see_also_see_also ON subset_definition_see_also (see_also);
CREATE INDEX ix_subset_definition_see_also_subset_definition_name ON subset_definition_see_also (subset_definition_name);

CREATE TABLE subset_definition_aliases (
	subset_definition_name TEXT,
	aliases TEXT,
	PRIMARY KEY (subset_definition_name, aliases),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_aliases_subset_definition_name ON subset_definition_aliases (subset_definition_name);
CREATE INDEX ix_subset_definition_aliases_aliases ON subset_definition_aliases (aliases);

CREATE TABLE subset_definition_mappings (
	subset_definition_name TEXT,
	mappings TEXT,
	PRIMARY KEY (subset_definition_name, mappings),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_mappings_subset_definition_name ON subset_definition_mappings (subset_definition_name);
CREATE INDEX ix_subset_definition_mappings_mappings ON subset_definition_mappings (mappings);

CREATE TABLE subset_definition_exact_mappings (
	subset_definition_name TEXT,
	exact_mappings TEXT,
	PRIMARY KEY (subset_definition_name, exact_mappings),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_exact_mappings_exact_mappings ON subset_definition_exact_mappings (exact_mappings);
CREATE INDEX ix_subset_definition_exact_mappings_subset_definition_name ON subset_definition_exact_mappings (subset_definition_name);

CREATE TABLE subset_definition_close_mappings (
	subset_definition_name TEXT,
	close_mappings TEXT,
	PRIMARY KEY (subset_definition_name, close_mappings),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_close_mappings_close_mappings ON subset_definition_close_mappings (close_mappings);
CREATE INDEX ix_subset_definition_close_mappings_subset_definition_name ON subset_definition_close_mappings (subset_definition_name);

CREATE TABLE subset_definition_related_mappings (
	subset_definition_name TEXT,
	related_mappings TEXT,
	PRIMARY KEY (subset_definition_name, related_mappings),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_related_mappings_subset_definition_name ON subset_definition_related_mappings (subset_definition_name);
CREATE INDEX ix_subset_definition_related_mappings_related_mappings ON subset_definition_related_mappings (related_mappings);

CREATE TABLE subset_definition_narrow_mappings (
	subset_definition_name TEXT,
	narrow_mappings TEXT,
	PRIMARY KEY (subset_definition_name, narrow_mappings),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_narrow_mappings_subset_definition_name ON subset_definition_narrow_mappings (subset_definition_name);
CREATE INDEX ix_subset_definition_narrow_mappings_narrow_mappings ON subset_definition_narrow_mappings (narrow_mappings);

CREATE TABLE subset_definition_broad_mappings (
	subset_definition_name TEXT,
	broad_mappings TEXT,
	PRIMARY KEY (subset_definition_name, broad_mappings),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_broad_mappings_subset_definition_name ON subset_definition_broad_mappings (subset_definition_name);
CREATE INDEX ix_subset_definition_broad_mappings_broad_mappings ON subset_definition_broad_mappings (broad_mappings);

CREATE TABLE subset_definition_contributors (
	subset_definition_name TEXT,
	contributors TEXT,
	PRIMARY KEY (subset_definition_name, contributors),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_contributors_subset_definition_name ON subset_definition_contributors (subset_definition_name);
CREATE INDEX ix_subset_definition_contributors_contributors ON subset_definition_contributors (contributors);

CREATE TABLE subset_definition_category (
	subset_definition_name TEXT,
	category TEXT,
	PRIMARY KEY (subset_definition_name, category),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_category_subset_definition_name ON subset_definition_category (subset_definition_name);
CREATE INDEX ix_subset_definition_category_category ON subset_definition_category (category);

CREATE TABLE subset_definition_keyword (
	subset_definition_name TEXT,
	keyword TEXT,
	PRIMARY KEY (subset_definition_name, keyword),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_subset_definition_keyword_subset_definition_name ON subset_definition_keyword (subset_definition_name);
CREATE INDEX ix_subset_definition_keyword_keyword ON subset_definition_keyword (keyword);

CREATE TABLE definition_in_subset (
	definition_name TEXT,
	in_subset_name TEXT,
	PRIMARY KEY (definition_name, in_subset_name),
	FOREIGN KEY(definition_name) REFERENCES definition (name),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_definition_in_subset_in_subset_name ON definition_in_subset (in_subset_name);
CREATE INDEX ix_definition_in_subset_definition_name ON definition_in_subset (definition_name);

CREATE TABLE enum_expression_include (
	enum_expression_id INTEGER,
	include_id INTEGER,
	PRIMARY KEY (enum_expression_id, include_id),
	FOREIGN KEY(enum_expression_id) REFERENCES enum_expression (id),
	FOREIGN KEY(include_id) REFERENCES anonymous_enum_expression (id)
);
CREATE INDEX ix_enum_expression_include_include_id ON enum_expression_include (include_id);
CREATE INDEX ix_enum_expression_include_enum_expression_id ON enum_expression_include (enum_expression_id);

CREATE TABLE enum_expression_minus (
	enum_expression_id INTEGER,
	minus_id INTEGER,
	PRIMARY KEY (enum_expression_id, minus_id),
	FOREIGN KEY(enum_expression_id) REFERENCES enum_expression (id),
	FOREIGN KEY(minus_id) REFERENCES anonymous_enum_expression (id)
);
CREATE INDEX ix_enum_expression_minus_enum_expression_id ON enum_expression_minus (enum_expression_id);
CREATE INDEX ix_enum_expression_minus_minus_id ON enum_expression_minus (minus_id);

CREATE TABLE enum_expression_inherits (
	enum_expression_id INTEGER,
	inherits_name TEXT,
	PRIMARY KEY (enum_expression_id, inherits_name),
	FOREIGN KEY(enum_expression_id) REFERENCES enum_expression (id),
	FOREIGN KEY(inherits_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_expression_inherits_inherits_name ON enum_expression_inherits (inherits_name);
CREATE INDEX ix_enum_expression_inherits_enum_expression_id ON enum_expression_inherits (enum_expression_id);

CREATE TABLE enum_expression_concepts (
	enum_expression_id INTEGER,
	concepts TEXT,
	PRIMARY KEY (enum_expression_id, concepts),
	FOREIGN KEY(enum_expression_id) REFERENCES enum_expression (id)
);
CREATE INDEX ix_enum_expression_concepts_enum_expression_id ON enum_expression_concepts (enum_expression_id);
CREATE INDEX ix_enum_expression_concepts_concepts ON enum_expression_concepts (concepts);

CREATE TABLE anonymous_enum_expression_include (
	anonymous_enum_expression_id INTEGER,
	include_id INTEGER,
	PRIMARY KEY (anonymous_enum_expression_id, include_id),
	FOREIGN KEY(anonymous_enum_expression_id) REFERENCES anonymous_enum_expression (id),
	FOREIGN KEY(include_id) REFERENCES anonymous_enum_expression (id)
);
CREATE INDEX ix_anonymous_enum_expression_include_anonymous_enum_expression_id ON anonymous_enum_expression_include (anonymous_enum_expression_id);
CREATE INDEX ix_anonymous_enum_expression_include_include_id ON anonymous_enum_expression_include (include_id);

CREATE TABLE anonymous_enum_expression_minus (
	anonymous_enum_expression_id INTEGER,
	minus_id INTEGER,
	PRIMARY KEY (anonymous_enum_expression_id, minus_id),
	FOREIGN KEY(anonymous_enum_expression_id) REFERENCES anonymous_enum_expression (id),
	FOREIGN KEY(minus_id) REFERENCES anonymous_enum_expression (id)
);
CREATE INDEX ix_anonymous_enum_expression_minus_minus_id ON anonymous_enum_expression_minus (minus_id);
CREATE INDEX ix_anonymous_enum_expression_minus_anonymous_enum_expression_id ON anonymous_enum_expression_minus (anonymous_enum_expression_id);

CREATE TABLE anonymous_enum_expression_inherits (
	anonymous_enum_expression_id INTEGER,
	inherits_name TEXT,
	PRIMARY KEY (anonymous_enum_expression_id, inherits_name),
	FOREIGN KEY(anonymous_enum_expression_id) REFERENCES anonymous_enum_expression (id),
	FOREIGN KEY(inherits_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_anonymous_enum_expression_inherits_inherits_name ON anonymous_enum_expression_inherits (inherits_name);
CREATE INDEX ix_anonymous_enum_expression_inherits_anonymous_enum_expression_id ON anonymous_enum_expression_inherits (anonymous_enum_expression_id);

CREATE TABLE anonymous_enum_expression_concepts (
	anonymous_enum_expression_id INTEGER,
	concepts TEXT,
	PRIMARY KEY (anonymous_enum_expression_id, concepts),
	FOREIGN KEY(anonymous_enum_expression_id) REFERENCES anonymous_enum_expression (id)
);
CREATE INDEX ix_anonymous_enum_expression_concepts_concepts ON anonymous_enum_expression_concepts (concepts);
CREATE INDEX ix_anonymous_enum_expression_concepts_anonymous_enum_expression_id ON anonymous_enum_expression_concepts (anonymous_enum_expression_id);

CREATE TABLE enum_definition_include (
	enum_definition_name TEXT,
	include_id INTEGER,
	PRIMARY KEY (enum_definition_name, include_id),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(include_id) REFERENCES anonymous_enum_expression (id)
);
CREATE INDEX ix_enum_definition_include_include_id ON enum_definition_include (include_id);
CREATE INDEX ix_enum_definition_include_enum_definition_name ON enum_definition_include (enum_definition_name);

CREATE TABLE enum_definition_minus (
	enum_definition_name TEXT,
	minus_id INTEGER,
	PRIMARY KEY (enum_definition_name, minus_id),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(minus_id) REFERENCES anonymous_enum_expression (id)
);
CREATE INDEX ix_enum_definition_minus_minus_id ON enum_definition_minus (minus_id);
CREATE INDEX ix_enum_definition_minus_enum_definition_name ON enum_definition_minus (enum_definition_name);

CREATE TABLE enum_definition_inherits (
	enum_definition_name TEXT,
	inherits_name TEXT,
	PRIMARY KEY (enum_definition_name, inherits_name),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(inherits_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_inherits_enum_definition_name ON enum_definition_inherits (enum_definition_name);
CREATE INDEX ix_enum_definition_inherits_inherits_name ON enum_definition_inherits (inherits_name);

CREATE TABLE enum_definition_concepts (
	enum_definition_name TEXT,
	concepts TEXT,
	PRIMARY KEY (enum_definition_name, concepts),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_concepts_enum_definition_name ON enum_definition_concepts (enum_definition_name);
CREATE INDEX ix_enum_definition_concepts_concepts ON enum_definition_concepts (concepts);

CREATE TABLE enum_definition_mixins (
	enum_definition_name TEXT,
	mixins_name TEXT,
	PRIMARY KEY (enum_definition_name, mixins_name),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(mixins_name) REFERENCES definition (name)
);
CREATE INDEX ix_enum_definition_mixins_mixins_name ON enum_definition_mixins (mixins_name);
CREATE INDEX ix_enum_definition_mixins_enum_definition_name ON enum_definition_mixins (enum_definition_name);

CREATE TABLE enum_definition_apply_to (
	enum_definition_name TEXT,
	apply_to_name TEXT,
	PRIMARY KEY (enum_definition_name, apply_to_name),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(apply_to_name) REFERENCES definition (name)
);
CREATE INDEX ix_enum_definition_apply_to_apply_to_name ON enum_definition_apply_to (apply_to_name);
CREATE INDEX ix_enum_definition_apply_to_enum_definition_name ON enum_definition_apply_to (enum_definition_name);

CREATE TABLE enum_definition_values_from (
	enum_definition_name TEXT,
	values_from TEXT,
	PRIMARY KEY (enum_definition_name, values_from),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_values_from_values_from ON enum_definition_values_from (values_from);
CREATE INDEX ix_enum_definition_values_from_enum_definition_name ON enum_definition_values_from (enum_definition_name);

CREATE TABLE enum_definition_id_prefixes (
	enum_definition_name TEXT,
	id_prefixes TEXT,
	PRIMARY KEY (enum_definition_name, id_prefixes),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_id_prefixes_id_prefixes ON enum_definition_id_prefixes (id_prefixes);
CREATE INDEX ix_enum_definition_id_prefixes_enum_definition_name ON enum_definition_id_prefixes (enum_definition_name);

CREATE TABLE enum_definition_implements (
	enum_definition_name TEXT,
	implements TEXT,
	PRIMARY KEY (enum_definition_name, implements),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_implements_implements ON enum_definition_implements (implements);
CREATE INDEX ix_enum_definition_implements_enum_definition_name ON enum_definition_implements (enum_definition_name);

CREATE TABLE enum_definition_instantiates (
	enum_definition_name TEXT,
	instantiates TEXT,
	PRIMARY KEY (enum_definition_name, instantiates),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_instantiates_enum_definition_name ON enum_definition_instantiates (enum_definition_name);
CREATE INDEX ix_enum_definition_instantiates_instantiates ON enum_definition_instantiates (instantiates);

CREATE TABLE enum_definition_todos (
	enum_definition_name TEXT,
	todos TEXT,
	PRIMARY KEY (enum_definition_name, todos),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_todos_enum_definition_name ON enum_definition_todos (enum_definition_name);
CREATE INDEX ix_enum_definition_todos_todos ON enum_definition_todos (todos);

CREATE TABLE enum_definition_notes (
	enum_definition_name TEXT,
	notes TEXT,
	PRIMARY KEY (enum_definition_name, notes),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_notes_enum_definition_name ON enum_definition_notes (enum_definition_name);
CREATE INDEX ix_enum_definition_notes_notes ON enum_definition_notes (notes);

CREATE TABLE enum_definition_comments (
	enum_definition_name TEXT,
	comments TEXT,
	PRIMARY KEY (enum_definition_name, comments),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_comments_comments ON enum_definition_comments (comments);
CREATE INDEX ix_enum_definition_comments_enum_definition_name ON enum_definition_comments (enum_definition_name);

CREATE TABLE enum_definition_in_subset (
	enum_definition_name TEXT,
	in_subset_name TEXT,
	PRIMARY KEY (enum_definition_name, in_subset_name),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_enum_definition_in_subset_in_subset_name ON enum_definition_in_subset (in_subset_name);
CREATE INDEX ix_enum_definition_in_subset_enum_definition_name ON enum_definition_in_subset (enum_definition_name);

CREATE TABLE enum_definition_see_also (
	enum_definition_name TEXT,
	see_also TEXT,
	PRIMARY KEY (enum_definition_name, see_also),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_see_also_see_also ON enum_definition_see_also (see_also);
CREATE INDEX ix_enum_definition_see_also_enum_definition_name ON enum_definition_see_also (enum_definition_name);

CREATE TABLE enum_definition_aliases (
	enum_definition_name TEXT,
	aliases TEXT,
	PRIMARY KEY (enum_definition_name, aliases),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_aliases_enum_definition_name ON enum_definition_aliases (enum_definition_name);
CREATE INDEX ix_enum_definition_aliases_aliases ON enum_definition_aliases (aliases);

CREATE TABLE enum_definition_mappings (
	enum_definition_name TEXT,
	mappings TEXT,
	PRIMARY KEY (enum_definition_name, mappings),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_mappings_enum_definition_name ON enum_definition_mappings (enum_definition_name);
CREATE INDEX ix_enum_definition_mappings_mappings ON enum_definition_mappings (mappings);

CREATE TABLE enum_definition_exact_mappings (
	enum_definition_name TEXT,
	exact_mappings TEXT,
	PRIMARY KEY (enum_definition_name, exact_mappings),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_exact_mappings_exact_mappings ON enum_definition_exact_mappings (exact_mappings);
CREATE INDEX ix_enum_definition_exact_mappings_enum_definition_name ON enum_definition_exact_mappings (enum_definition_name);

CREATE TABLE enum_definition_close_mappings (
	enum_definition_name TEXT,
	close_mappings TEXT,
	PRIMARY KEY (enum_definition_name, close_mappings),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_close_mappings_enum_definition_name ON enum_definition_close_mappings (enum_definition_name);
CREATE INDEX ix_enum_definition_close_mappings_close_mappings ON enum_definition_close_mappings (close_mappings);

CREATE TABLE enum_definition_related_mappings (
	enum_definition_name TEXT,
	related_mappings TEXT,
	PRIMARY KEY (enum_definition_name, related_mappings),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_related_mappings_related_mappings ON enum_definition_related_mappings (related_mappings);
CREATE INDEX ix_enum_definition_related_mappings_enum_definition_name ON enum_definition_related_mappings (enum_definition_name);

CREATE TABLE enum_definition_narrow_mappings (
	enum_definition_name TEXT,
	narrow_mappings TEXT,
	PRIMARY KEY (enum_definition_name, narrow_mappings),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_narrow_mappings_enum_definition_name ON enum_definition_narrow_mappings (enum_definition_name);
CREATE INDEX ix_enum_definition_narrow_mappings_narrow_mappings ON enum_definition_narrow_mappings (narrow_mappings);

CREATE TABLE enum_definition_broad_mappings (
	enum_definition_name TEXT,
	broad_mappings TEXT,
	PRIMARY KEY (enum_definition_name, broad_mappings),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_broad_mappings_enum_definition_name ON enum_definition_broad_mappings (enum_definition_name);
CREATE INDEX ix_enum_definition_broad_mappings_broad_mappings ON enum_definition_broad_mappings (broad_mappings);

CREATE TABLE enum_definition_contributors (
	enum_definition_name TEXT,
	contributors TEXT,
	PRIMARY KEY (enum_definition_name, contributors),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_contributors_contributors ON enum_definition_contributors (contributors);
CREATE INDEX ix_enum_definition_contributors_enum_definition_name ON enum_definition_contributors (enum_definition_name);

CREATE TABLE enum_definition_category (
	enum_definition_name TEXT,
	category TEXT,
	PRIMARY KEY (enum_definition_name, category),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_category_category ON enum_definition_category (category);
CREATE INDEX ix_enum_definition_category_enum_definition_name ON enum_definition_category (enum_definition_name);

CREATE TABLE enum_definition_keyword (
	enum_definition_name TEXT,
	keyword TEXT,
	PRIMARY KEY (enum_definition_name, keyword),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE INDEX ix_enum_definition_keyword_keyword ON enum_definition_keyword (keyword);
CREATE INDEX ix_enum_definition_keyword_enum_definition_name ON enum_definition_keyword (enum_definition_name);

CREATE TABLE anonymous_expression_in_subset (
	anonymous_expression_id INTEGER,
	in_subset_name TEXT,
	PRIMARY KEY (anonymous_expression_id, in_subset_name),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_anonymous_expression_in_subset_anonymous_expression_id ON anonymous_expression_in_subset (anonymous_expression_id);
CREATE INDEX ix_anonymous_expression_in_subset_in_subset_name ON anonymous_expression_in_subset (in_subset_name);

CREATE TABLE path_expression_in_subset (
	path_expression_id INTEGER,
	in_subset_name TEXT,
	PRIMARY KEY (path_expression_id, in_subset_name),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_path_expression_in_subset_path_expression_id ON path_expression_in_subset (path_expression_id);
CREATE INDEX ix_path_expression_in_subset_in_subset_name ON path_expression_in_subset (in_subset_name);

CREATE TABLE slot_definition_type_mappings (
	slot_definition_name TEXT,
	type_mappings_framework TEXT,
	PRIMARY KEY (slot_definition_name, type_mappings_framework),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(type_mappings_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_slot_definition_type_mappings_slot_definition_name ON slot_definition_type_mappings (slot_definition_name);
CREATE INDEX ix_slot_definition_type_mappings_type_mappings_framework ON slot_definition_type_mappings (type_mappings_framework);

CREATE TABLE slot_definition_in_subset (
	slot_definition_name TEXT,
	in_subset_name TEXT,
	PRIMARY KEY (slot_definition_name, in_subset_name),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_slot_definition_in_subset_in_subset_name ON slot_definition_in_subset (in_subset_name);
CREATE INDEX ix_slot_definition_in_subset_slot_definition_name ON slot_definition_in_subset (slot_definition_name);

CREATE TABLE anonymous_class_expression_in_subset (
	anonymous_class_expression_id INTEGER,
	in_subset_name TEXT,
	PRIMARY KEY (anonymous_class_expression_id, in_subset_name),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_anonymous_class_expression_in_subset_anonymous_class_expression_id ON anonymous_class_expression_in_subset (anonymous_class_expression_id);
CREATE INDEX ix_anonymous_class_expression_in_subset_in_subset_name ON anonymous_class_expression_in_subset (in_subset_name);

CREATE TABLE class_definition_in_subset (
	class_definition_name TEXT,
	in_subset_name TEXT,
	PRIMARY KEY (class_definition_name, in_subset_name),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_class_definition_in_subset_in_subset_name ON class_definition_in_subset (in_subset_name);
CREATE INDEX ix_class_definition_in_subset_class_definition_name ON class_definition_in_subset (class_definition_name);

CREATE TABLE class_rule_todos (
	class_rule_id INTEGER,
	todos TEXT,
	PRIMARY KEY (class_rule_id, todos),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_todos_todos ON class_rule_todos (todos);
CREATE INDEX ix_class_rule_todos_class_rule_id ON class_rule_todos (class_rule_id);

CREATE TABLE class_rule_notes (
	class_rule_id INTEGER,
	notes TEXT,
	PRIMARY KEY (class_rule_id, notes),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_notes_class_rule_id ON class_rule_notes (class_rule_id);
CREATE INDEX ix_class_rule_notes_notes ON class_rule_notes (notes);

CREATE TABLE class_rule_comments (
	class_rule_id INTEGER,
	comments TEXT,
	PRIMARY KEY (class_rule_id, comments),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_comments_class_rule_id ON class_rule_comments (class_rule_id);
CREATE INDEX ix_class_rule_comments_comments ON class_rule_comments (comments);

CREATE TABLE class_rule_in_subset (
	class_rule_id INTEGER,
	in_subset_name TEXT,
	PRIMARY KEY (class_rule_id, in_subset_name),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_class_rule_in_subset_in_subset_name ON class_rule_in_subset (in_subset_name);
CREATE INDEX ix_class_rule_in_subset_class_rule_id ON class_rule_in_subset (class_rule_id);

CREATE TABLE class_rule_see_also (
	class_rule_id INTEGER,
	see_also TEXT,
	PRIMARY KEY (class_rule_id, see_also),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_see_also_see_also ON class_rule_see_also (see_also);
CREATE INDEX ix_class_rule_see_also_class_rule_id ON class_rule_see_also (class_rule_id);

CREATE TABLE class_rule_aliases (
	class_rule_id INTEGER,
	aliases TEXT,
	PRIMARY KEY (class_rule_id, aliases),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_aliases_aliases ON class_rule_aliases (aliases);
CREATE INDEX ix_class_rule_aliases_class_rule_id ON class_rule_aliases (class_rule_id);

CREATE TABLE class_rule_mappings (
	class_rule_id INTEGER,
	mappings TEXT,
	PRIMARY KEY (class_rule_id, mappings),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_mappings_class_rule_id ON class_rule_mappings (class_rule_id);
CREATE INDEX ix_class_rule_mappings_mappings ON class_rule_mappings (mappings);

CREATE TABLE class_rule_exact_mappings (
	class_rule_id INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY (class_rule_id, exact_mappings),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_exact_mappings_class_rule_id ON class_rule_exact_mappings (class_rule_id);
CREATE INDEX ix_class_rule_exact_mappings_exact_mappings ON class_rule_exact_mappings (exact_mappings);

CREATE TABLE class_rule_close_mappings (
	class_rule_id INTEGER,
	close_mappings TEXT,
	PRIMARY KEY (class_rule_id, close_mappings),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_close_mappings_class_rule_id ON class_rule_close_mappings (class_rule_id);
CREATE INDEX ix_class_rule_close_mappings_close_mappings ON class_rule_close_mappings (close_mappings);

CREATE TABLE class_rule_related_mappings (
	class_rule_id INTEGER,
	related_mappings TEXT,
	PRIMARY KEY (class_rule_id, related_mappings),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_related_mappings_class_rule_id ON class_rule_related_mappings (class_rule_id);
CREATE INDEX ix_class_rule_related_mappings_related_mappings ON class_rule_related_mappings (related_mappings);

CREATE TABLE class_rule_narrow_mappings (
	class_rule_id INTEGER,
	narrow_mappings TEXT,
	PRIMARY KEY (class_rule_id, narrow_mappings),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_narrow_mappings_narrow_mappings ON class_rule_narrow_mappings (narrow_mappings);
CREATE INDEX ix_class_rule_narrow_mappings_class_rule_id ON class_rule_narrow_mappings (class_rule_id);

CREATE TABLE class_rule_broad_mappings (
	class_rule_id INTEGER,
	broad_mappings TEXT,
	PRIMARY KEY (class_rule_id, broad_mappings),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_broad_mappings_class_rule_id ON class_rule_broad_mappings (class_rule_id);
CREATE INDEX ix_class_rule_broad_mappings_broad_mappings ON class_rule_broad_mappings (broad_mappings);

CREATE TABLE class_rule_contributors (
	class_rule_id INTEGER,
	contributors TEXT,
	PRIMARY KEY (class_rule_id, contributors),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_contributors_class_rule_id ON class_rule_contributors (class_rule_id);
CREATE INDEX ix_class_rule_contributors_contributors ON class_rule_contributors (contributors);

CREATE TABLE class_rule_category (
	class_rule_id INTEGER,
	category TEXT,
	PRIMARY KEY (class_rule_id, category),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_category_category ON class_rule_category (category);
CREATE INDEX ix_class_rule_category_class_rule_id ON class_rule_category (class_rule_id);

CREATE TABLE class_rule_keyword (
	class_rule_id INTEGER,
	keyword TEXT,
	PRIMARY KEY (class_rule_id, keyword),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE INDEX ix_class_rule_keyword_class_rule_id ON class_rule_keyword (class_rule_id);
CREATE INDEX ix_class_rule_keyword_keyword ON class_rule_keyword (keyword);

CREATE TABLE array_expression_dimensions (
	array_expression_id INTEGER,
	dimensions_id INTEGER,
	PRIMARY KEY (array_expression_id, dimensions_id),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id),
	FOREIGN KEY(dimensions_id) REFERENCES dimension_expression (id)
);
CREATE INDEX ix_array_expression_dimensions_dimensions_id ON array_expression_dimensions (dimensions_id);
CREATE INDEX ix_array_expression_dimensions_array_expression_id ON array_expression_dimensions (array_expression_id);

CREATE TABLE array_expression_todos (
	array_expression_id INTEGER,
	todos TEXT,
	PRIMARY KEY (array_expression_id, todos),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_todos_array_expression_id ON array_expression_todos (array_expression_id);
CREATE INDEX ix_array_expression_todos_todos ON array_expression_todos (todos);

CREATE TABLE array_expression_notes (
	array_expression_id INTEGER,
	notes TEXT,
	PRIMARY KEY (array_expression_id, notes),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_notes_notes ON array_expression_notes (notes);
CREATE INDEX ix_array_expression_notes_array_expression_id ON array_expression_notes (array_expression_id);

CREATE TABLE array_expression_comments (
	array_expression_id INTEGER,
	comments TEXT,
	PRIMARY KEY (array_expression_id, comments),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_comments_array_expression_id ON array_expression_comments (array_expression_id);
CREATE INDEX ix_array_expression_comments_comments ON array_expression_comments (comments);

CREATE TABLE array_expression_in_subset (
	array_expression_id INTEGER,
	in_subset_name TEXT,
	PRIMARY KEY (array_expression_id, in_subset_name),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_array_expression_in_subset_in_subset_name ON array_expression_in_subset (in_subset_name);
CREATE INDEX ix_array_expression_in_subset_array_expression_id ON array_expression_in_subset (array_expression_id);

CREATE TABLE array_expression_see_also (
	array_expression_id INTEGER,
	see_also TEXT,
	PRIMARY KEY (array_expression_id, see_also),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_see_also_see_also ON array_expression_see_also (see_also);
CREATE INDEX ix_array_expression_see_also_array_expression_id ON array_expression_see_also (array_expression_id);

CREATE TABLE array_expression_aliases (
	array_expression_id INTEGER,
	aliases TEXT,
	PRIMARY KEY (array_expression_id, aliases),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_aliases_aliases ON array_expression_aliases (aliases);
CREATE INDEX ix_array_expression_aliases_array_expression_id ON array_expression_aliases (array_expression_id);

CREATE TABLE array_expression_mappings (
	array_expression_id INTEGER,
	mappings TEXT,
	PRIMARY KEY (array_expression_id, mappings),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_mappings_mappings ON array_expression_mappings (mappings);
CREATE INDEX ix_array_expression_mappings_array_expression_id ON array_expression_mappings (array_expression_id);

CREATE TABLE array_expression_exact_mappings (
	array_expression_id INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY (array_expression_id, exact_mappings),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_exact_mappings_array_expression_id ON array_expression_exact_mappings (array_expression_id);
CREATE INDEX ix_array_expression_exact_mappings_exact_mappings ON array_expression_exact_mappings (exact_mappings);

CREATE TABLE array_expression_close_mappings (
	array_expression_id INTEGER,
	close_mappings TEXT,
	PRIMARY KEY (array_expression_id, close_mappings),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_close_mappings_array_expression_id ON array_expression_close_mappings (array_expression_id);
CREATE INDEX ix_array_expression_close_mappings_close_mappings ON array_expression_close_mappings (close_mappings);

CREATE TABLE array_expression_related_mappings (
	array_expression_id INTEGER,
	related_mappings TEXT,
	PRIMARY KEY (array_expression_id, related_mappings),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_related_mappings_related_mappings ON array_expression_related_mappings (related_mappings);
CREATE INDEX ix_array_expression_related_mappings_array_expression_id ON array_expression_related_mappings (array_expression_id);

CREATE TABLE array_expression_narrow_mappings (
	array_expression_id INTEGER,
	narrow_mappings TEXT,
	PRIMARY KEY (array_expression_id, narrow_mappings),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_narrow_mappings_narrow_mappings ON array_expression_narrow_mappings (narrow_mappings);
CREATE INDEX ix_array_expression_narrow_mappings_array_expression_id ON array_expression_narrow_mappings (array_expression_id);

CREATE TABLE array_expression_broad_mappings (
	array_expression_id INTEGER,
	broad_mappings TEXT,
	PRIMARY KEY (array_expression_id, broad_mappings),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_broad_mappings_array_expression_id ON array_expression_broad_mappings (array_expression_id);
CREATE INDEX ix_array_expression_broad_mappings_broad_mappings ON array_expression_broad_mappings (broad_mappings);

CREATE TABLE array_expression_contributors (
	array_expression_id INTEGER,
	contributors TEXT,
	PRIMARY KEY (array_expression_id, contributors),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_contributors_array_expression_id ON array_expression_contributors (array_expression_id);
CREATE INDEX ix_array_expression_contributors_contributors ON array_expression_contributors (contributors);

CREATE TABLE array_expression_category (
	array_expression_id INTEGER,
	category TEXT,
	PRIMARY KEY (array_expression_id, category),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_category_category ON array_expression_category (category);
CREATE INDEX ix_array_expression_category_array_expression_id ON array_expression_category (array_expression_id);

CREATE TABLE array_expression_keyword (
	array_expression_id INTEGER,
	keyword TEXT,
	PRIMARY KEY (array_expression_id, keyword),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_array_expression_keyword_keyword ON array_expression_keyword (keyword);
CREATE INDEX ix_array_expression_keyword_array_expression_id ON array_expression_keyword (array_expression_id);

CREATE TABLE dimension_expression_in_subset (
	dimension_expression_id INTEGER,
	in_subset_name TEXT,
	PRIMARY KEY (dimension_expression_id, in_subset_name),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_dimension_expression_in_subset_in_subset_name ON dimension_expression_in_subset (in_subset_name);
CREATE INDEX ix_dimension_expression_in_subset_dimension_expression_id ON dimension_expression_in_subset (dimension_expression_id);

CREATE TABLE pattern_expression_in_subset (
	pattern_expression_id INTEGER,
	in_subset_name TEXT,
	PRIMARY KEY (pattern_expression_id, in_subset_name),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_pattern_expression_in_subset_in_subset_name ON pattern_expression_in_subset (in_subset_name);
CREATE INDEX ix_pattern_expression_in_subset_pattern_expression_id ON pattern_expression_in_subset (pattern_expression_id);

CREATE TABLE import_expression_in_subset (
	import_expression_id INTEGER,
	in_subset_name TEXT,
	PRIMARY KEY (import_expression_id, in_subset_name),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_import_expression_in_subset_import_expression_id ON import_expression_in_subset (import_expression_id);
CREATE INDEX ix_import_expression_in_subset_in_subset_name ON import_expression_in_subset (in_subset_name);

CREATE TABLE unique_key_unique_key_slots (
	unique_key_unique_key_name TEXT,
	unique_key_slots_name TEXT NOT NULL,
	PRIMARY KEY (unique_key_unique_key_name, unique_key_slots_name),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name),
	FOREIGN KEY(unique_key_slots_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_unique_key_unique_key_slots_unique_key_slots_name ON unique_key_unique_key_slots (unique_key_slots_name);
CREATE INDEX ix_unique_key_unique_key_slots_unique_key_unique_key_name ON unique_key_unique_key_slots (unique_key_unique_key_name);

CREATE TABLE unique_key_todos (
	unique_key_unique_key_name TEXT,
	todos TEXT,
	PRIMARY KEY (unique_key_unique_key_name, todos),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_todos_todos ON unique_key_todos (todos);
CREATE INDEX ix_unique_key_todos_unique_key_unique_key_name ON unique_key_todos (unique_key_unique_key_name);

CREATE TABLE unique_key_notes (
	unique_key_unique_key_name TEXT,
	notes TEXT,
	PRIMARY KEY (unique_key_unique_key_name, notes),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_notes_notes ON unique_key_notes (notes);
CREATE INDEX ix_unique_key_notes_unique_key_unique_key_name ON unique_key_notes (unique_key_unique_key_name);

CREATE TABLE unique_key_comments (
	unique_key_unique_key_name TEXT,
	comments TEXT,
	PRIMARY KEY (unique_key_unique_key_name, comments),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_comments_comments ON unique_key_comments (comments);
CREATE INDEX ix_unique_key_comments_unique_key_unique_key_name ON unique_key_comments (unique_key_unique_key_name);

CREATE TABLE unique_key_in_subset (
	unique_key_unique_key_name TEXT,
	in_subset_name TEXT,
	PRIMARY KEY (unique_key_unique_key_name, in_subset_name),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_unique_key_in_subset_in_subset_name ON unique_key_in_subset (in_subset_name);
CREATE INDEX ix_unique_key_in_subset_unique_key_unique_key_name ON unique_key_in_subset (unique_key_unique_key_name);

CREATE TABLE unique_key_see_also (
	unique_key_unique_key_name TEXT,
	see_also TEXT,
	PRIMARY KEY (unique_key_unique_key_name, see_also),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_see_also_see_also ON unique_key_see_also (see_also);
CREATE INDEX ix_unique_key_see_also_unique_key_unique_key_name ON unique_key_see_also (unique_key_unique_key_name);

CREATE TABLE unique_key_aliases (
	unique_key_unique_key_name TEXT,
	aliases TEXT,
	PRIMARY KEY (unique_key_unique_key_name, aliases),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_aliases_aliases ON unique_key_aliases (aliases);
CREATE INDEX ix_unique_key_aliases_unique_key_unique_key_name ON unique_key_aliases (unique_key_unique_key_name);

CREATE TABLE unique_key_mappings (
	unique_key_unique_key_name TEXT,
	mappings TEXT,
	PRIMARY KEY (unique_key_unique_key_name, mappings),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_mappings_unique_key_unique_key_name ON unique_key_mappings (unique_key_unique_key_name);
CREATE INDEX ix_unique_key_mappings_mappings ON unique_key_mappings (mappings);

CREATE TABLE unique_key_exact_mappings (
	unique_key_unique_key_name TEXT,
	exact_mappings TEXT,
	PRIMARY KEY (unique_key_unique_key_name, exact_mappings),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_exact_mappings_exact_mappings ON unique_key_exact_mappings (exact_mappings);
CREATE INDEX ix_unique_key_exact_mappings_unique_key_unique_key_name ON unique_key_exact_mappings (unique_key_unique_key_name);

CREATE TABLE unique_key_close_mappings (
	unique_key_unique_key_name TEXT,
	close_mappings TEXT,
	PRIMARY KEY (unique_key_unique_key_name, close_mappings),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_close_mappings_unique_key_unique_key_name ON unique_key_close_mappings (unique_key_unique_key_name);
CREATE INDEX ix_unique_key_close_mappings_close_mappings ON unique_key_close_mappings (close_mappings);

CREATE TABLE unique_key_related_mappings (
	unique_key_unique_key_name TEXT,
	related_mappings TEXT,
	PRIMARY KEY (unique_key_unique_key_name, related_mappings),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_related_mappings_unique_key_unique_key_name ON unique_key_related_mappings (unique_key_unique_key_name);
CREATE INDEX ix_unique_key_related_mappings_related_mappings ON unique_key_related_mappings (related_mappings);

CREATE TABLE unique_key_narrow_mappings (
	unique_key_unique_key_name TEXT,
	narrow_mappings TEXT,
	PRIMARY KEY (unique_key_unique_key_name, narrow_mappings),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_narrow_mappings_narrow_mappings ON unique_key_narrow_mappings (narrow_mappings);
CREATE INDEX ix_unique_key_narrow_mappings_unique_key_unique_key_name ON unique_key_narrow_mappings (unique_key_unique_key_name);

CREATE TABLE unique_key_broad_mappings (
	unique_key_unique_key_name TEXT,
	broad_mappings TEXT,
	PRIMARY KEY (unique_key_unique_key_name, broad_mappings),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_broad_mappings_unique_key_unique_key_name ON unique_key_broad_mappings (unique_key_unique_key_name);
CREATE INDEX ix_unique_key_broad_mappings_broad_mappings ON unique_key_broad_mappings (broad_mappings);

CREATE TABLE unique_key_contributors (
	unique_key_unique_key_name TEXT,
	contributors TEXT,
	PRIMARY KEY (unique_key_unique_key_name, contributors),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_contributors_contributors ON unique_key_contributors (contributors);
CREATE INDEX ix_unique_key_contributors_unique_key_unique_key_name ON unique_key_contributors (unique_key_unique_key_name);

CREATE TABLE unique_key_category (
	unique_key_unique_key_name TEXT,
	category TEXT,
	PRIMARY KEY (unique_key_unique_key_name, category),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_category_category ON unique_key_category (category);
CREATE INDEX ix_unique_key_category_unique_key_unique_key_name ON unique_key_category (unique_key_unique_key_name);

CREATE TABLE unique_key_keyword (
	unique_key_unique_key_name TEXT,
	keyword TEXT,
	PRIMARY KEY (unique_key_unique_key_name, keyword),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE INDEX ix_unique_key_keyword_unique_key_unique_key_name ON unique_key_keyword (unique_key_unique_key_name);
CREATE INDEX ix_unique_key_keyword_keyword ON unique_key_keyword (keyword);

CREATE TABLE type_mapping_todos (
	type_mapping_framework TEXT,
	todos TEXT,
	PRIMARY KEY (type_mapping_framework, todos),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_todos_todos ON type_mapping_todos (todos);
CREATE INDEX ix_type_mapping_todos_type_mapping_framework ON type_mapping_todos (type_mapping_framework);

CREATE TABLE type_mapping_notes (
	type_mapping_framework TEXT,
	notes TEXT,
	PRIMARY KEY (type_mapping_framework, notes),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_notes_notes ON type_mapping_notes (notes);
CREATE INDEX ix_type_mapping_notes_type_mapping_framework ON type_mapping_notes (type_mapping_framework);

CREATE TABLE type_mapping_comments (
	type_mapping_framework TEXT,
	comments TEXT,
	PRIMARY KEY (type_mapping_framework, comments),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_comments_type_mapping_framework ON type_mapping_comments (type_mapping_framework);
CREATE INDEX ix_type_mapping_comments_comments ON type_mapping_comments (comments);

CREATE TABLE type_mapping_in_subset (
	type_mapping_framework TEXT,
	in_subset_name TEXT,
	PRIMARY KEY (type_mapping_framework, in_subset_name),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_type_mapping_in_subset_type_mapping_framework ON type_mapping_in_subset (type_mapping_framework);
CREATE INDEX ix_type_mapping_in_subset_in_subset_name ON type_mapping_in_subset (in_subset_name);

CREATE TABLE type_mapping_see_also (
	type_mapping_framework TEXT,
	see_also TEXT,
	PRIMARY KEY (type_mapping_framework, see_also),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_see_also_type_mapping_framework ON type_mapping_see_also (type_mapping_framework);
CREATE INDEX ix_type_mapping_see_also_see_also ON type_mapping_see_also (see_also);

CREATE TABLE type_mapping_aliases (
	type_mapping_framework TEXT,
	aliases TEXT,
	PRIMARY KEY (type_mapping_framework, aliases),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_aliases_type_mapping_framework ON type_mapping_aliases (type_mapping_framework);
CREATE INDEX ix_type_mapping_aliases_aliases ON type_mapping_aliases (aliases);

CREATE TABLE type_mapping_mappings (
	type_mapping_framework TEXT,
	mappings TEXT,
	PRIMARY KEY (type_mapping_framework, mappings),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_mappings_type_mapping_framework ON type_mapping_mappings (type_mapping_framework);
CREATE INDEX ix_type_mapping_mappings_mappings ON type_mapping_mappings (mappings);

CREATE TABLE type_mapping_exact_mappings (
	type_mapping_framework TEXT,
	exact_mappings TEXT,
	PRIMARY KEY (type_mapping_framework, exact_mappings),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_exact_mappings_exact_mappings ON type_mapping_exact_mappings (exact_mappings);
CREATE INDEX ix_type_mapping_exact_mappings_type_mapping_framework ON type_mapping_exact_mappings (type_mapping_framework);

CREATE TABLE type_mapping_close_mappings (
	type_mapping_framework TEXT,
	close_mappings TEXT,
	PRIMARY KEY (type_mapping_framework, close_mappings),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_close_mappings_type_mapping_framework ON type_mapping_close_mappings (type_mapping_framework);
CREATE INDEX ix_type_mapping_close_mappings_close_mappings ON type_mapping_close_mappings (close_mappings);

CREATE TABLE type_mapping_related_mappings (
	type_mapping_framework TEXT,
	related_mappings TEXT,
	PRIMARY KEY (type_mapping_framework, related_mappings),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_related_mappings_related_mappings ON type_mapping_related_mappings (related_mappings);
CREATE INDEX ix_type_mapping_related_mappings_type_mapping_framework ON type_mapping_related_mappings (type_mapping_framework);

CREATE TABLE type_mapping_narrow_mappings (
	type_mapping_framework TEXT,
	narrow_mappings TEXT,
	PRIMARY KEY (type_mapping_framework, narrow_mappings),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_narrow_mappings_narrow_mappings ON type_mapping_narrow_mappings (narrow_mappings);
CREATE INDEX ix_type_mapping_narrow_mappings_type_mapping_framework ON type_mapping_narrow_mappings (type_mapping_framework);

CREATE TABLE type_mapping_broad_mappings (
	type_mapping_framework TEXT,
	broad_mappings TEXT,
	PRIMARY KEY (type_mapping_framework, broad_mappings),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_broad_mappings_broad_mappings ON type_mapping_broad_mappings (broad_mappings);
CREATE INDEX ix_type_mapping_broad_mappings_type_mapping_framework ON type_mapping_broad_mappings (type_mapping_framework);

CREATE TABLE type_mapping_contributors (
	type_mapping_framework TEXT,
	contributors TEXT,
	PRIMARY KEY (type_mapping_framework, contributors),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_contributors_type_mapping_framework ON type_mapping_contributors (type_mapping_framework);
CREATE INDEX ix_type_mapping_contributors_contributors ON type_mapping_contributors (contributors);

CREATE TABLE type_mapping_category (
	type_mapping_framework TEXT,
	category TEXT,
	PRIMARY KEY (type_mapping_framework, category),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_category_type_mapping_framework ON type_mapping_category (type_mapping_framework);
CREATE INDEX ix_type_mapping_category_category ON type_mapping_category (category);

CREATE TABLE type_mapping_keyword (
	type_mapping_framework TEXT,
	keyword TEXT,
	PRIMARY KEY (type_mapping_framework, keyword),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_type_mapping_keyword_type_mapping_framework ON type_mapping_keyword (type_mapping_framework);
CREATE INDEX ix_type_mapping_keyword_keyword ON type_mapping_keyword (keyword);

CREATE TABLE slot_expression (
	id INTEGER NOT NULL,
	range TEXT,
	required BOOLEAN,
	recommended BOOLEAN,
	multivalued BOOLEAN,
	inlined BOOLEAN,
	inlined_as_list BOOLEAN,
	pattern TEXT,
	implicit_prefix TEXT,
	value_presence VARCHAR(11),
	equals_string TEXT,
	equals_number INTEGER,
	equals_expression TEXT,
	exact_cardinality INTEGER,
	minimum_cardinality INTEGER,
	maximum_cardinality INTEGER,
	range_expression_id INTEGER,
	enum_range_id INTEGER,
	minimum_value_id INTEGER,
	maximum_value_id INTEGER,
	structured_pattern_id INTEGER,
	unit_id INTEGER,
	has_member_id INTEGER,
	all_members_id INTEGER,
	array_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(range) REFERENCES element (name),
	FOREIGN KEY(range_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(enum_range_id) REFERENCES enum_expression (id),
	FOREIGN KEY(minimum_value_id) REFERENCES "Anything" (id),
	FOREIGN KEY(maximum_value_id) REFERENCES "Anything" (id),
	FOREIGN KEY(structured_pattern_id) REFERENCES pattern_expression (id),
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id),
	FOREIGN KEY(has_member_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(all_members_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(array_id) REFERENCES array_expression (id)
);
CREATE INDEX ix_slot_expression_id ON slot_expression (id);

CREATE TABLE anonymous_slot_expression_equals_string_in (
	anonymous_slot_expression_id INTEGER,
	equals_string_in TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, equals_string_in),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_equals_string_in_anonymous_slot_expression_id ON anonymous_slot_expression_equals_string_in (anonymous_slot_expression_id);
CREATE INDEX ix_anonymous_slot_expression_equals_string_in_equals_string_in ON anonymous_slot_expression_equals_string_in (equals_string_in);

CREATE TABLE anonymous_slot_expression_none_of (
	anonymous_slot_expression_id INTEGER,
	none_of_id INTEGER,
	PRIMARY KEY (anonymous_slot_expression_id, none_of_id),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(none_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_none_of_anonymous_slot_expression_id ON anonymous_slot_expression_none_of (anonymous_slot_expression_id);
CREATE INDEX ix_anonymous_slot_expression_none_of_none_of_id ON anonymous_slot_expression_none_of (none_of_id);

CREATE TABLE anonymous_slot_expression_exactly_one_of (
	anonymous_slot_expression_id INTEGER,
	exactly_one_of_id INTEGER,
	PRIMARY KEY (anonymous_slot_expression_id, exactly_one_of_id),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_exactly_one_of_anonymous_slot_expression_id ON anonymous_slot_expression_exactly_one_of (anonymous_slot_expression_id);
CREATE INDEX ix_anonymous_slot_expression_exactly_one_of_exactly_one_of_id ON anonymous_slot_expression_exactly_one_of (exactly_one_of_id);

CREATE TABLE anonymous_slot_expression_any_of (
	anonymous_slot_expression_id INTEGER,
	any_of_id INTEGER,
	PRIMARY KEY (anonymous_slot_expression_id, any_of_id),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(any_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_any_of_any_of_id ON anonymous_slot_expression_any_of (any_of_id);
CREATE INDEX ix_anonymous_slot_expression_any_of_anonymous_slot_expression_id ON anonymous_slot_expression_any_of (anonymous_slot_expression_id);

CREATE TABLE anonymous_slot_expression_all_of (
	anonymous_slot_expression_id INTEGER,
	all_of_id INTEGER,
	PRIMARY KEY (anonymous_slot_expression_id, all_of_id),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(all_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_all_of_all_of_id ON anonymous_slot_expression_all_of (all_of_id);
CREATE INDEX ix_anonymous_slot_expression_all_of_anonymous_slot_expression_id ON anonymous_slot_expression_all_of (anonymous_slot_expression_id);

CREATE TABLE anonymous_slot_expression_todos (
	anonymous_slot_expression_id INTEGER,
	todos TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, todos),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_todos_todos ON anonymous_slot_expression_todos (todos);
CREATE INDEX ix_anonymous_slot_expression_todos_anonymous_slot_expression_id ON anonymous_slot_expression_todos (anonymous_slot_expression_id);

CREATE TABLE anonymous_slot_expression_notes (
	anonymous_slot_expression_id INTEGER,
	notes TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, notes),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_notes_notes ON anonymous_slot_expression_notes (notes);
CREATE INDEX ix_anonymous_slot_expression_notes_anonymous_slot_expression_id ON anonymous_slot_expression_notes (anonymous_slot_expression_id);

CREATE TABLE anonymous_slot_expression_comments (
	anonymous_slot_expression_id INTEGER,
	comments TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, comments),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_comments_anonymous_slot_expression_id ON anonymous_slot_expression_comments (anonymous_slot_expression_id);
CREATE INDEX ix_anonymous_slot_expression_comments_comments ON anonymous_slot_expression_comments (comments);

CREATE TABLE anonymous_slot_expression_in_subset (
	anonymous_slot_expression_id INTEGER,
	in_subset_name TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, in_subset_name),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_anonymous_slot_expression_in_subset_anonymous_slot_expression_id ON anonymous_slot_expression_in_subset (anonymous_slot_expression_id);
CREATE INDEX ix_anonymous_slot_expression_in_subset_in_subset_name ON anonymous_slot_expression_in_subset (in_subset_name);

CREATE TABLE anonymous_slot_expression_see_also (
	anonymous_slot_expression_id INTEGER,
	see_also TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, see_also),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_see_also_see_also ON anonymous_slot_expression_see_also (see_also);
CREATE INDEX ix_anonymous_slot_expression_see_also_anonymous_slot_expression_id ON anonymous_slot_expression_see_also (anonymous_slot_expression_id);

CREATE TABLE anonymous_slot_expression_aliases (
	anonymous_slot_expression_id INTEGER,
	aliases TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, aliases),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_aliases_anonymous_slot_expression_id ON anonymous_slot_expression_aliases (anonymous_slot_expression_id);
CREATE INDEX ix_anonymous_slot_expression_aliases_aliases ON anonymous_slot_expression_aliases (aliases);

CREATE TABLE anonymous_slot_expression_mappings (
	anonymous_slot_expression_id INTEGER,
	mappings TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, mappings),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_mappings_anonymous_slot_expression_id ON anonymous_slot_expression_mappings (anonymous_slot_expression_id);
CREATE INDEX ix_anonymous_slot_expression_mappings_mappings ON anonymous_slot_expression_mappings (mappings);

CREATE TABLE anonymous_slot_expression_exact_mappings (
	anonymous_slot_expression_id INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, exact_mappings),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_exact_mappings_exact_mappings ON anonymous_slot_expression_exact_mappings (exact_mappings);
CREATE INDEX ix_anonymous_slot_expression_exact_mappings_anonymous_slot_expression_id ON anonymous_slot_expression_exact_mappings (anonymous_slot_expression_id);

CREATE TABLE anonymous_slot_expression_close_mappings (
	anonymous_slot_expression_id INTEGER,
	close_mappings TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, close_mappings),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_close_mappings_close_mappings ON anonymous_slot_expression_close_mappings (close_mappings);
CREATE INDEX ix_anonymous_slot_expression_close_mappings_anonymous_slot_expression_id ON anonymous_slot_expression_close_mappings (anonymous_slot_expression_id);

CREATE TABLE anonymous_slot_expression_related_mappings (
	anonymous_slot_expression_id INTEGER,
	related_mappings TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, related_mappings),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_related_mappings_anonymous_slot_expression_id ON anonymous_slot_expression_related_mappings (anonymous_slot_expression_id);
CREATE INDEX ix_anonymous_slot_expression_related_mappings_related_mappings ON anonymous_slot_expression_related_mappings (related_mappings);

CREATE TABLE anonymous_slot_expression_narrow_mappings (
	anonymous_slot_expression_id INTEGER,
	narrow_mappings TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, narrow_mappings),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_narrow_mappings_anonymous_slot_expression_id ON anonymous_slot_expression_narrow_mappings (anonymous_slot_expression_id);
CREATE INDEX ix_anonymous_slot_expression_narrow_mappings_narrow_mappings ON anonymous_slot_expression_narrow_mappings (narrow_mappings);

CREATE TABLE anonymous_slot_expression_broad_mappings (
	anonymous_slot_expression_id INTEGER,
	broad_mappings TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, broad_mappings),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_broad_mappings_anonymous_slot_expression_id ON anonymous_slot_expression_broad_mappings (anonymous_slot_expression_id);
CREATE INDEX ix_anonymous_slot_expression_broad_mappings_broad_mappings ON anonymous_slot_expression_broad_mappings (broad_mappings);

CREATE TABLE anonymous_slot_expression_contributors (
	anonymous_slot_expression_id INTEGER,
	contributors TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, contributors),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_contributors_contributors ON anonymous_slot_expression_contributors (contributors);
CREATE INDEX ix_anonymous_slot_expression_contributors_anonymous_slot_expression_id ON anonymous_slot_expression_contributors (anonymous_slot_expression_id);

CREATE TABLE anonymous_slot_expression_category (
	anonymous_slot_expression_id INTEGER,
	category TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, category),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_category_category ON anonymous_slot_expression_category (category);
CREATE INDEX ix_anonymous_slot_expression_category_anonymous_slot_expression_id ON anonymous_slot_expression_category (anonymous_slot_expression_id);

CREATE TABLE anonymous_slot_expression_keyword (
	anonymous_slot_expression_id INTEGER,
	keyword TEXT,
	PRIMARY KEY (anonymous_slot_expression_id, keyword),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_anonymous_slot_expression_keyword_anonymous_slot_expression_id ON anonymous_slot_expression_keyword (anonymous_slot_expression_id);
CREATE INDEX ix_anonymous_slot_expression_keyword_keyword ON anonymous_slot_expression_keyword (keyword);

CREATE TABLE slot_definition_none_of (
	slot_definition_name TEXT,
	none_of_id INTEGER,
	PRIMARY KEY (slot_definition_name, none_of_id),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(none_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_slot_definition_none_of_slot_definition_name ON slot_definition_none_of (slot_definition_name);
CREATE INDEX ix_slot_definition_none_of_none_of_id ON slot_definition_none_of (none_of_id);

CREATE TABLE slot_definition_exactly_one_of (
	slot_definition_name TEXT,
	exactly_one_of_id INTEGER,
	PRIMARY KEY (slot_definition_name, exactly_one_of_id),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_slot_definition_exactly_one_of_exactly_one_of_id ON slot_definition_exactly_one_of (exactly_one_of_id);
CREATE INDEX ix_slot_definition_exactly_one_of_slot_definition_name ON slot_definition_exactly_one_of (slot_definition_name);

CREATE TABLE slot_definition_any_of (
	slot_definition_name TEXT,
	any_of_id INTEGER,
	PRIMARY KEY (slot_definition_name, any_of_id),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(any_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_slot_definition_any_of_slot_definition_name ON slot_definition_any_of (slot_definition_name);
CREATE INDEX ix_slot_definition_any_of_any_of_id ON slot_definition_any_of (any_of_id);

CREATE TABLE slot_definition_all_of (
	slot_definition_name TEXT,
	all_of_id INTEGER,
	PRIMARY KEY (slot_definition_name, all_of_id),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(all_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_slot_definition_all_of_slot_definition_name ON slot_definition_all_of (slot_definition_name);
CREATE INDEX ix_slot_definition_all_of_all_of_id ON slot_definition_all_of (all_of_id);

CREATE TABLE permissible_value_instantiates (
	permissible_value_text TEXT,
	instantiates TEXT,
	PRIMARY KEY (permissible_value_text, instantiates),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_instantiates_permissible_value_text ON permissible_value_instantiates (permissible_value_text);
CREATE INDEX ix_permissible_value_instantiates_instantiates ON permissible_value_instantiates (instantiates);

CREATE TABLE permissible_value_implements (
	permissible_value_text TEXT,
	implements TEXT,
	PRIMARY KEY (permissible_value_text, implements),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_implements_permissible_value_text ON permissible_value_implements (permissible_value_text);
CREATE INDEX ix_permissible_value_implements_implements ON permissible_value_implements (implements);

CREATE TABLE permissible_value_mixins (
	permissible_value_text TEXT,
	mixins_text TEXT,
	PRIMARY KEY (permissible_value_text, mixins_text),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text),
	FOREIGN KEY(mixins_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_mixins_permissible_value_text ON permissible_value_mixins (permissible_value_text);
CREATE INDEX ix_permissible_value_mixins_mixins_text ON permissible_value_mixins (mixins_text);

CREATE TABLE permissible_value_todos (
	permissible_value_text TEXT,
	todos TEXT,
	PRIMARY KEY (permissible_value_text, todos),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_todos_permissible_value_text ON permissible_value_todos (permissible_value_text);
CREATE INDEX ix_permissible_value_todos_todos ON permissible_value_todos (todos);

CREATE TABLE permissible_value_notes (
	permissible_value_text TEXT,
	notes TEXT,
	PRIMARY KEY (permissible_value_text, notes),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_notes_notes ON permissible_value_notes (notes);
CREATE INDEX ix_permissible_value_notes_permissible_value_text ON permissible_value_notes (permissible_value_text);

CREATE TABLE permissible_value_comments (
	permissible_value_text TEXT,
	comments TEXT,
	PRIMARY KEY (permissible_value_text, comments),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_comments_permissible_value_text ON permissible_value_comments (permissible_value_text);
CREATE INDEX ix_permissible_value_comments_comments ON permissible_value_comments (comments);

CREATE TABLE permissible_value_in_subset (
	permissible_value_text TEXT,
	in_subset_name TEXT,
	PRIMARY KEY (permissible_value_text, in_subset_name),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_permissible_value_in_subset_permissible_value_text ON permissible_value_in_subset (permissible_value_text);
CREATE INDEX ix_permissible_value_in_subset_in_subset_name ON permissible_value_in_subset (in_subset_name);

CREATE TABLE permissible_value_see_also (
	permissible_value_text TEXT,
	see_also TEXT,
	PRIMARY KEY (permissible_value_text, see_also),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_see_also_see_also ON permissible_value_see_also (see_also);
CREATE INDEX ix_permissible_value_see_also_permissible_value_text ON permissible_value_see_also (permissible_value_text);

CREATE TABLE permissible_value_aliases (
	permissible_value_text TEXT,
	aliases TEXT,
	PRIMARY KEY (permissible_value_text, aliases),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_aliases_aliases ON permissible_value_aliases (aliases);
CREATE INDEX ix_permissible_value_aliases_permissible_value_text ON permissible_value_aliases (permissible_value_text);

CREATE TABLE permissible_value_mappings (
	permissible_value_text TEXT,
	mappings TEXT,
	PRIMARY KEY (permissible_value_text, mappings),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_mappings_permissible_value_text ON permissible_value_mappings (permissible_value_text);
CREATE INDEX ix_permissible_value_mappings_mappings ON permissible_value_mappings (mappings);

CREATE TABLE permissible_value_exact_mappings (
	permissible_value_text TEXT,
	exact_mappings TEXT,
	PRIMARY KEY (permissible_value_text, exact_mappings),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_exact_mappings_exact_mappings ON permissible_value_exact_mappings (exact_mappings);
CREATE INDEX ix_permissible_value_exact_mappings_permissible_value_text ON permissible_value_exact_mappings (permissible_value_text);

CREATE TABLE permissible_value_close_mappings (
	permissible_value_text TEXT,
	close_mappings TEXT,
	PRIMARY KEY (permissible_value_text, close_mappings),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_close_mappings_permissible_value_text ON permissible_value_close_mappings (permissible_value_text);
CREATE INDEX ix_permissible_value_close_mappings_close_mappings ON permissible_value_close_mappings (close_mappings);

CREATE TABLE permissible_value_related_mappings (
	permissible_value_text TEXT,
	related_mappings TEXT,
	PRIMARY KEY (permissible_value_text, related_mappings),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_related_mappings_permissible_value_text ON permissible_value_related_mappings (permissible_value_text);
CREATE INDEX ix_permissible_value_related_mappings_related_mappings ON permissible_value_related_mappings (related_mappings);

CREATE TABLE permissible_value_narrow_mappings (
	permissible_value_text TEXT,
	narrow_mappings TEXT,
	PRIMARY KEY (permissible_value_text, narrow_mappings),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_narrow_mappings_narrow_mappings ON permissible_value_narrow_mappings (narrow_mappings);
CREATE INDEX ix_permissible_value_narrow_mappings_permissible_value_text ON permissible_value_narrow_mappings (permissible_value_text);

CREATE TABLE permissible_value_broad_mappings (
	permissible_value_text TEXT,
	broad_mappings TEXT,
	PRIMARY KEY (permissible_value_text, broad_mappings),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_broad_mappings_permissible_value_text ON permissible_value_broad_mappings (permissible_value_text);
CREATE INDEX ix_permissible_value_broad_mappings_broad_mappings ON permissible_value_broad_mappings (broad_mappings);

CREATE TABLE permissible_value_contributors (
	permissible_value_text TEXT,
	contributors TEXT,
	PRIMARY KEY (permissible_value_text, contributors),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_contributors_contributors ON permissible_value_contributors (contributors);
CREATE INDEX ix_permissible_value_contributors_permissible_value_text ON permissible_value_contributors (permissible_value_text);

CREATE TABLE permissible_value_category (
	permissible_value_text TEXT,
	category TEXT,
	PRIMARY KEY (permissible_value_text, category),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_category_permissible_value_text ON permissible_value_category (permissible_value_text);
CREATE INDEX ix_permissible_value_category_category ON permissible_value_category (category);

CREATE TABLE permissible_value_keyword (
	permissible_value_text TEXT,
	keyword TEXT,
	PRIMARY KEY (permissible_value_text, keyword),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE INDEX ix_permissible_value_keyword_keyword ON permissible_value_keyword (keyword);
CREATE INDEX ix_permissible_value_keyword_permissible_value_text ON permissible_value_keyword (permissible_value_text);

CREATE TABLE enum_binding (
	id INTEGER NOT NULL,
	range TEXT,
	obligation_level VARCHAR(11),
	binds_value_of TEXT,
	pv_formula VARCHAR(11),
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	schema_definition_name TEXT,
	slot_expression_id INTEGER,
	anonymous_slot_expression_id INTEGER,
	slot_definition_name TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(range) REFERENCES enum_definition (name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE INDEX ix_enum_binding_id ON enum_binding (id);

CREATE TABLE slot_expression_equals_string_in (
	slot_expression_id INTEGER,
	equals_string_in TEXT,
	PRIMARY KEY (slot_expression_id, equals_string_in),
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id)
);
CREATE INDEX ix_slot_expression_equals_string_in_equals_string_in ON slot_expression_equals_string_in (equals_string_in);
CREATE INDEX ix_slot_expression_equals_string_in_slot_expression_id ON slot_expression_equals_string_in (slot_expression_id);

CREATE TABLE slot_expression_none_of (
	slot_expression_id INTEGER,
	none_of_id INTEGER,
	PRIMARY KEY (slot_expression_id, none_of_id),
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id),
	FOREIGN KEY(none_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_slot_expression_none_of_slot_expression_id ON slot_expression_none_of (slot_expression_id);
CREATE INDEX ix_slot_expression_none_of_none_of_id ON slot_expression_none_of (none_of_id);

CREATE TABLE slot_expression_exactly_one_of (
	slot_expression_id INTEGER,
	exactly_one_of_id INTEGER,
	PRIMARY KEY (slot_expression_id, exactly_one_of_id),
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id),
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_slot_expression_exactly_one_of_slot_expression_id ON slot_expression_exactly_one_of (slot_expression_id);
CREATE INDEX ix_slot_expression_exactly_one_of_exactly_one_of_id ON slot_expression_exactly_one_of (exactly_one_of_id);

CREATE TABLE slot_expression_any_of (
	slot_expression_id INTEGER,
	any_of_id INTEGER,
	PRIMARY KEY (slot_expression_id, any_of_id),
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id),
	FOREIGN KEY(any_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_slot_expression_any_of_any_of_id ON slot_expression_any_of (any_of_id);
CREATE INDEX ix_slot_expression_any_of_slot_expression_id ON slot_expression_any_of (slot_expression_id);

CREATE TABLE slot_expression_all_of (
	slot_expression_id INTEGER,
	all_of_id INTEGER,
	PRIMARY KEY (slot_expression_id, all_of_id),
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id),
	FOREIGN KEY(all_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE INDEX ix_slot_expression_all_of_all_of_id ON slot_expression_all_of (all_of_id);
CREATE INDEX ix_slot_expression_all_of_slot_expression_id ON slot_expression_all_of (slot_expression_id);

CREATE TABLE structured_alias (
	id INTEGER NOT NULL,
	literal_form TEXT NOT NULL,
	predicate VARCHAR(15),
	description TEXT,
	title TEXT,
	deprecated TEXT,
	from_schema TEXT,
	imported_from TEXT,
	source TEXT,
	in_language TEXT,
	deprecated_element_has_exact_replacement TEXT,
	deprecated_element_has_possible_replacement TEXT,
	created_by TEXT,
	created_on DATETIME,
	last_updated_on DATETIME,
	modified_by TEXT,
	status TEXT,
	rank INTEGER,
	common_metadata_id INTEGER,
	element_name TEXT,
	schema_definition_name TEXT,
	type_definition_name TEXT,
	subset_definition_name TEXT,
	definition_name TEXT,
	enum_definition_name TEXT,
	enum_binding_id INTEGER,
	structured_alias_id INTEGER,
	anonymous_expression_id INTEGER,
	path_expression_id INTEGER,
	anonymous_slot_expression_id INTEGER,
	slot_definition_name TEXT,
	anonymous_class_expression_id INTEGER,
	class_definition_name TEXT,
	class_rule_id INTEGER,
	array_expression_id INTEGER,
	dimension_expression_id INTEGER,
	pattern_expression_id INTEGER,
	import_expression_id INTEGER,
	permissible_value_text TEXT,
	unique_key_unique_key_name TEXT,
	type_mapping_framework TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id),
	FOREIGN KEY(element_name) REFERENCES element (name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name),
	FOREIGN KEY(definition_name) REFERENCES definition (name),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_structured_alias_id ON structured_alias (id);

CREATE TABLE enum_binding_todos (
	enum_binding_id INTEGER,
	todos TEXT,
	PRIMARY KEY (enum_binding_id, todos),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_todos_enum_binding_id ON enum_binding_todos (enum_binding_id);
CREATE INDEX ix_enum_binding_todos_todos ON enum_binding_todos (todos);

CREATE TABLE enum_binding_notes (
	enum_binding_id INTEGER,
	notes TEXT,
	PRIMARY KEY (enum_binding_id, notes),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_notes_notes ON enum_binding_notes (notes);
CREATE INDEX ix_enum_binding_notes_enum_binding_id ON enum_binding_notes (enum_binding_id);

CREATE TABLE enum_binding_comments (
	enum_binding_id INTEGER,
	comments TEXT,
	PRIMARY KEY (enum_binding_id, comments),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_comments_comments ON enum_binding_comments (comments);
CREATE INDEX ix_enum_binding_comments_enum_binding_id ON enum_binding_comments (enum_binding_id);

CREATE TABLE enum_binding_in_subset (
	enum_binding_id INTEGER,
	in_subset_name TEXT,
	PRIMARY KEY (enum_binding_id, in_subset_name),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_enum_binding_in_subset_in_subset_name ON enum_binding_in_subset (in_subset_name);
CREATE INDEX ix_enum_binding_in_subset_enum_binding_id ON enum_binding_in_subset (enum_binding_id);

CREATE TABLE enum_binding_see_also (
	enum_binding_id INTEGER,
	see_also TEXT,
	PRIMARY KEY (enum_binding_id, see_also),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_see_also_enum_binding_id ON enum_binding_see_also (enum_binding_id);
CREATE INDEX ix_enum_binding_see_also_see_also ON enum_binding_see_also (see_also);

CREATE TABLE enum_binding_aliases (
	enum_binding_id INTEGER,
	aliases TEXT,
	PRIMARY KEY (enum_binding_id, aliases),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_aliases_aliases ON enum_binding_aliases (aliases);
CREATE INDEX ix_enum_binding_aliases_enum_binding_id ON enum_binding_aliases (enum_binding_id);

CREATE TABLE enum_binding_mappings (
	enum_binding_id INTEGER,
	mappings TEXT,
	PRIMARY KEY (enum_binding_id, mappings),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_mappings_mappings ON enum_binding_mappings (mappings);
CREATE INDEX ix_enum_binding_mappings_enum_binding_id ON enum_binding_mappings (enum_binding_id);

CREATE TABLE enum_binding_exact_mappings (
	enum_binding_id INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY (enum_binding_id, exact_mappings),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_exact_mappings_enum_binding_id ON enum_binding_exact_mappings (enum_binding_id);
CREATE INDEX ix_enum_binding_exact_mappings_exact_mappings ON enum_binding_exact_mappings (exact_mappings);

CREATE TABLE enum_binding_close_mappings (
	enum_binding_id INTEGER,
	close_mappings TEXT,
	PRIMARY KEY (enum_binding_id, close_mappings),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_close_mappings_enum_binding_id ON enum_binding_close_mappings (enum_binding_id);
CREATE INDEX ix_enum_binding_close_mappings_close_mappings ON enum_binding_close_mappings (close_mappings);

CREATE TABLE enum_binding_related_mappings (
	enum_binding_id INTEGER,
	related_mappings TEXT,
	PRIMARY KEY (enum_binding_id, related_mappings),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_related_mappings_enum_binding_id ON enum_binding_related_mappings (enum_binding_id);
CREATE INDEX ix_enum_binding_related_mappings_related_mappings ON enum_binding_related_mappings (related_mappings);

CREATE TABLE enum_binding_narrow_mappings (
	enum_binding_id INTEGER,
	narrow_mappings TEXT,
	PRIMARY KEY (enum_binding_id, narrow_mappings),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_narrow_mappings_enum_binding_id ON enum_binding_narrow_mappings (enum_binding_id);
CREATE INDEX ix_enum_binding_narrow_mappings_narrow_mappings ON enum_binding_narrow_mappings (narrow_mappings);

CREATE TABLE enum_binding_broad_mappings (
	enum_binding_id INTEGER,
	broad_mappings TEXT,
	PRIMARY KEY (enum_binding_id, broad_mappings),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_broad_mappings_broad_mappings ON enum_binding_broad_mappings (broad_mappings);
CREATE INDEX ix_enum_binding_broad_mappings_enum_binding_id ON enum_binding_broad_mappings (enum_binding_id);

CREATE TABLE enum_binding_contributors (
	enum_binding_id INTEGER,
	contributors TEXT,
	PRIMARY KEY (enum_binding_id, contributors),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_contributors_enum_binding_id ON enum_binding_contributors (enum_binding_id);
CREATE INDEX ix_enum_binding_contributors_contributors ON enum_binding_contributors (contributors);

CREATE TABLE enum_binding_category (
	enum_binding_id INTEGER,
	category TEXT,
	PRIMARY KEY (enum_binding_id, category),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_category_enum_binding_id ON enum_binding_category (enum_binding_id);
CREATE INDEX ix_enum_binding_category_category ON enum_binding_category (category);

CREATE TABLE enum_binding_keyword (
	enum_binding_id INTEGER,
	keyword TEXT,
	PRIMARY KEY (enum_binding_id, keyword),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id)
);
CREATE INDEX ix_enum_binding_keyword_keyword ON enum_binding_keyword (keyword);
CREATE INDEX ix_enum_binding_keyword_enum_binding_id ON enum_binding_keyword (enum_binding_id);

CREATE TABLE example (
	id INTEGER NOT NULL,
	value TEXT,
	description TEXT,
	common_metadata_id INTEGER,
	element_name TEXT,
	schema_definition_name TEXT,
	type_definition_name TEXT,
	subset_definition_name TEXT,
	definition_name TEXT,
	enum_definition_name TEXT,
	enum_binding_id INTEGER,
	structured_alias_id INTEGER,
	anonymous_expression_id INTEGER,
	path_expression_id INTEGER,
	anonymous_slot_expression_id INTEGER,
	slot_definition_name TEXT,
	anonymous_class_expression_id INTEGER,
	class_definition_name TEXT,
	class_rule_id INTEGER,
	array_expression_id INTEGER,
	dimension_expression_id INTEGER,
	pattern_expression_id INTEGER,
	import_expression_id INTEGER,
	permissible_value_text TEXT,
	unique_key_unique_key_name TEXT,
	type_mapping_framework TEXT,
	object_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id),
	FOREIGN KEY(element_name) REFERENCES element (name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name),
	FOREIGN KEY(definition_name) REFERENCES definition (name),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework),
	FOREIGN KEY(object_id) REFERENCES "Anything" (id)
);
CREATE INDEX ix_example_id ON example (id);

CREATE TABLE alt_description (
	source TEXT NOT NULL,
	description TEXT NOT NULL,
	common_metadata_id INTEGER,
	element_name TEXT,
	schema_definition_name TEXT,
	type_definition_name TEXT,
	subset_definition_name TEXT,
	definition_name TEXT,
	enum_definition_name TEXT,
	enum_binding_id INTEGER,
	structured_alias_id INTEGER,
	anonymous_expression_id INTEGER,
	path_expression_id INTEGER,
	anonymous_slot_expression_id INTEGER,
	slot_definition_name TEXT,
	anonymous_class_expression_id INTEGER,
	class_definition_name TEXT,
	class_rule_id INTEGER,
	array_expression_id INTEGER,
	dimension_expression_id INTEGER,
	pattern_expression_id INTEGER,
	import_expression_id INTEGER,
	permissible_value_text TEXT,
	unique_key_unique_key_name TEXT,
	type_mapping_framework TEXT,
	PRIMARY KEY (source, description, common_metadata_id, element_name, schema_definition_name, type_definition_name, subset_definition_name, definition_name, enum_definition_name, enum_binding_id, structured_alias_id, anonymous_expression_id, path_expression_id, anonymous_slot_expression_id, slot_definition_name, anonymous_class_expression_id, class_definition_name, class_rule_id, array_expression_id, dimension_expression_id, pattern_expression_id, import_expression_id, permissible_value_text, unique_key_unique_key_name, type_mapping_framework),
	UNIQUE (common_metadata_id, source),
	UNIQUE (element_name, source),
	UNIQUE (schema_definition_name, source),
	UNIQUE (type_definition_name, source),
	UNIQUE (subset_definition_name, source),
	UNIQUE (definition_name, source),
	UNIQUE (enum_definition_name, source),
	UNIQUE (enum_binding_id, source),
	UNIQUE (structured_alias_id, source),
	UNIQUE (anonymous_expression_id, source),
	UNIQUE (path_expression_id, source),
	UNIQUE (anonymous_slot_expression_id, source),
	UNIQUE (slot_definition_name, source),
	UNIQUE (anonymous_class_expression_id, source),
	UNIQUE (class_definition_name, source),
	UNIQUE (class_rule_id, source),
	UNIQUE (array_expression_id, source),
	UNIQUE (dimension_expression_id, source),
	UNIQUE (pattern_expression_id, source),
	UNIQUE (import_expression_id, source),
	UNIQUE (permissible_value_text, source),
	UNIQUE (unique_key_unique_key_name, source),
	UNIQUE (type_mapping_framework, source),
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id),
	FOREIGN KEY(element_name) REFERENCES element (name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name),
	FOREIGN KEY(definition_name) REFERENCES definition (name),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework)
);
CREATE INDEX ix_alt_description_array_expression_id ON alt_description (array_expression_id);
CREATE INDEX alt_description_enum_binding_id_source_idx ON alt_description (enum_binding_id, source);
CREATE INDEX ix_alt_description_enum_binding_id ON alt_description (enum_binding_id);
CREATE INDEX alt_description_class_definition_name_source_idx ON alt_description (class_definition_name, source);
CREATE INDEX ix_alt_description_class_rule_id ON alt_description (class_rule_id);
CREATE INDEX alt_description_subset_definition_name_source_idx ON alt_description (subset_definition_name, source);
CREATE INDEX alt_description_anonymous_slot_expression_id_source_idx ON alt_description (anonymous_slot_expression_id, source);
CREATE INDEX ix_alt_description_definition_name ON alt_description (definition_name);
CREATE INDEX alt_description_unique_key_unique_key_name_source_idx ON alt_description (unique_key_unique_key_name, source);
CREATE INDEX ix_alt_description_type_mapping_framework ON alt_description (type_mapping_framework);
CREATE INDEX ix_alt_description_class_definition_name ON alt_description (class_definition_name);
CREATE INDEX alt_description_common_metadata_id_source_idx ON alt_description (common_metadata_id, source);
CREATE INDEX alt_description_structured_alias_id_source_idx ON alt_description (structured_alias_id, source);
CREATE INDEX alt_description_pattern_expression_id_source_idx ON alt_description (pattern_expression_id, source);
CREATE INDEX ix_alt_description_unique_key_unique_key_name ON alt_description (unique_key_unique_key_name);
CREATE INDEX ix_alt_description_subset_definition_name ON alt_description (subset_definition_name);
CREATE INDEX ix_alt_description_anonymous_class_expression_id ON alt_description (anonymous_class_expression_id);
CREATE INDEX ix_alt_description_description ON alt_description (description);
CREATE INDEX alt_description_class_rule_id_source_idx ON alt_description (class_rule_id, source);
CREATE INDEX alt_description_element_name_source_idx ON alt_description (element_name, source);
CREATE INDEX ix_alt_description_slot_definition_name ON alt_description (slot_definition_name);
CREATE INDEX ix_alt_description_permissible_value_text ON alt_description (permissible_value_text);
CREATE INDEX alt_description_definition_name_source_idx ON alt_description (definition_name, source);
CREATE INDEX ix_alt_description_type_definition_name ON alt_description (type_definition_name);
CREATE INDEX alt_description_slot_definition_name_source_idx ON alt_description (slot_definition_name, source);
CREATE INDEX alt_description_type_mapping_framework_source_idx ON alt_description (type_mapping_framework, source);
CREATE INDEX ix_alt_description_anonymous_slot_expression_id ON alt_description (anonymous_slot_expression_id);
CREATE INDEX ix_alt_description_import_expression_id ON alt_description (import_expression_id);
CREATE INDEX alt_description_anonymous_expression_id_source_idx ON alt_description (anonymous_expression_id, source);
CREATE INDEX alt_description_dimension_expression_id_source_idx ON alt_description (dimension_expression_id, source);
CREATE INDEX alt_description_import_expression_id_source_idx ON alt_description (import_expression_id, source);
CREATE INDEX alt_description_schema_definition_name_source_idx ON alt_description (schema_definition_name, source);
CREATE INDEX ix_alt_description_path_expression_id ON alt_description (path_expression_id);
CREATE INDEX ix_alt_description_schema_definition_name ON alt_description (schema_definition_name);
CREATE INDEX alt_description_array_expression_id_source_idx ON alt_description (array_expression_id, source);
CREATE INDEX ix_alt_description_enum_definition_name ON alt_description (enum_definition_name);
CREATE INDEX ix_alt_description_element_name ON alt_description (element_name);
CREATE INDEX ix_alt_description_pattern_expression_id ON alt_description (pattern_expression_id);
CREATE INDEX alt_description_enum_definition_name_source_idx ON alt_description (enum_definition_name, source);
CREATE INDEX ix_alt_description_source ON alt_description (source);
CREATE INDEX alt_description_anonymous_class_expression_id_source_idx ON alt_description (anonymous_class_expression_id, source);
CREATE INDEX ix_alt_description_anonymous_expression_id ON alt_description (anonymous_expression_id);
CREATE INDEX ix_alt_description_dimension_expression_id ON alt_description (dimension_expression_id);
CREATE INDEX alt_description_type_definition_name_source_idx ON alt_description (type_definition_name, source);
CREATE INDEX alt_description_path_expression_id_source_idx ON alt_description (path_expression_id, source);
CREATE INDEX alt_description_permissible_value_text_source_idx ON alt_description (permissible_value_text, source);
CREATE INDEX ix_alt_description_common_metadata_id ON alt_description (common_metadata_id);
CREATE INDEX ix_alt_description_structured_alias_id ON alt_description (structured_alias_id);

CREATE TABLE annotation (
	tag TEXT NOT NULL,
	element_name TEXT,
	schema_definition_name TEXT,
	type_definition_name TEXT,
	subset_definition_name TEXT,
	definition_name TEXT,
	enum_definition_name TEXT,
	enum_binding_id INTEGER,
	structured_alias_id INTEGER,
	anonymous_expression_id INTEGER,
	path_expression_id INTEGER,
	anonymous_slot_expression_id INTEGER,
	slot_definition_name TEXT,
	anonymous_class_expression_id INTEGER,
	class_definition_name TEXT,
	class_rule_id INTEGER,
	array_expression_id INTEGER,
	dimension_expression_id INTEGER,
	pattern_expression_id INTEGER,
	import_expression_id INTEGER,
	permissible_value_text TEXT,
	unique_key_unique_key_name TEXT,
	type_mapping_framework TEXT,
	annotatable_id INTEGER,
	annotation_tag TEXT,
	value_id INTEGER NOT NULL,
	PRIMARY KEY (tag, element_name, schema_definition_name, type_definition_name, subset_definition_name, definition_name, enum_definition_name, enum_binding_id, structured_alias_id, anonymous_expression_id, path_expression_id, anonymous_slot_expression_id, slot_definition_name, anonymous_class_expression_id, class_definition_name, class_rule_id, array_expression_id, dimension_expression_id, pattern_expression_id, import_expression_id, permissible_value_text, unique_key_unique_key_name, type_mapping_framework, annotatable_id, annotation_tag, value_id),
	UNIQUE (element_name, tag),
	UNIQUE (schema_definition_name, tag),
	UNIQUE (type_definition_name, tag),
	UNIQUE (subset_definition_name, tag),
	UNIQUE (definition_name, tag),
	UNIQUE (enum_definition_name, tag),
	UNIQUE (enum_binding_id, tag),
	UNIQUE (structured_alias_id, tag),
	UNIQUE (anonymous_expression_id, tag),
	UNIQUE (path_expression_id, tag),
	UNIQUE (anonymous_slot_expression_id, tag),
	UNIQUE (slot_definition_name, tag),
	UNIQUE (anonymous_class_expression_id, tag),
	UNIQUE (class_definition_name, tag),
	UNIQUE (class_rule_id, tag),
	UNIQUE (array_expression_id, tag),
	UNIQUE (dimension_expression_id, tag),
	UNIQUE (pattern_expression_id, tag),
	UNIQUE (import_expression_id, tag),
	UNIQUE (permissible_value_text, tag),
	UNIQUE (unique_key_unique_key_name, tag),
	UNIQUE (type_mapping_framework, tag),
	UNIQUE (annotatable_id, tag),
	UNIQUE (annotation_tag, tag),
	FOREIGN KEY(element_name) REFERENCES element (name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name),
	FOREIGN KEY(definition_name) REFERENCES definition (name),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework),
	FOREIGN KEY(annotatable_id) REFERENCES annotatable (id),
	FOREIGN KEY(annotation_tag) REFERENCES annotation (tag),
	FOREIGN KEY(value_id) REFERENCES "AnyValue" (id)
);
CREATE INDEX annotation_enum_binding_id_tag_idx ON annotation (enum_binding_id, tag);
CREATE INDEX annotation_class_definition_name_tag_idx ON annotation (class_definition_name, tag);
CREATE INDEX annotation_unique_key_unique_key_name_tag_idx ON annotation (unique_key_unique_key_name, tag);
CREATE INDEX ix_annotation_enum_definition_name ON annotation (enum_definition_name);
CREATE INDEX ix_annotation_tag ON annotation (tag);
CREATE INDEX ix_annotation_array_expression_id ON annotation (array_expression_id);
CREATE INDEX ix_annotation_definition_name ON annotation (definition_name);
CREATE INDEX annotation_anonymous_slot_expression_id_tag_idx ON annotation (anonymous_slot_expression_id, tag);
CREATE INDEX ix_annotation_class_rule_id ON annotation (class_rule_id);
CREATE INDEX annotation_pattern_expression_id_tag_idx ON annotation (pattern_expression_id, tag);
CREATE INDEX annotation_subset_definition_name_tag_idx ON annotation (subset_definition_name, tag);
CREATE INDEX ix_annotation_value_id ON annotation (value_id);
CREATE INDEX ix_annotation_subset_definition_name ON annotation (subset_definition_name);
CREATE INDEX ix_annotation_class_definition_name ON annotation (class_definition_name);
CREATE INDEX annotation_structured_alias_id_tag_idx ON annotation (structured_alias_id, tag);
CREATE INDEX annotation_class_rule_id_tag_idx ON annotation (class_rule_id, tag);
CREATE INDEX ix_annotation_structured_alias_id ON annotation (structured_alias_id);
CREATE INDEX annotation_element_name_tag_idx ON annotation (element_name, tag);
CREATE INDEX annotation_type_mapping_framework_tag_idx ON annotation (type_mapping_framework, tag);
CREATE INDEX ix_annotation_annotatable_id ON annotation (annotatable_id);
CREATE INDEX ix_annotation_annotation_tag ON annotation (annotation_tag);
CREATE INDEX ix_annotation_type_definition_name ON annotation (type_definition_name);
CREATE INDEX ix_annotation_anonymous_class_expression_id ON annotation (anonymous_class_expression_id);
CREATE INDEX annotation_slot_definition_name_tag_idx ON annotation (slot_definition_name, tag);
CREATE INDEX ix_annotation_type_mapping_framework ON annotation (type_mapping_framework);
CREATE INDEX annotation_definition_name_tag_idx ON annotation (definition_name, tag);
CREATE INDEX annotation_import_expression_id_tag_idx ON annotation (import_expression_id, tag);
CREATE INDEX ix_annotation_schema_definition_name ON annotation (schema_definition_name);
CREATE INDEX ix_annotation_slot_definition_name ON annotation (slot_definition_name);
CREATE INDEX ix_annotation_unique_key_unique_key_name ON annotation (unique_key_unique_key_name);
CREATE INDEX annotation_anonymous_expression_id_tag_idx ON annotation (anonymous_expression_id, tag);
CREATE INDEX annotation_array_expression_id_tag_idx ON annotation (array_expression_id, tag);
CREATE INDEX annotation_annotatable_id_tag_idx ON annotation (annotatable_id, tag);
CREATE INDEX ix_annotation_anonymous_slot_expression_id ON annotation (anonymous_slot_expression_id);
CREATE INDEX ix_annotation_permissible_value_text ON annotation (permissible_value_text);
CREATE INDEX annotation_anonymous_class_expression_id_tag_idx ON annotation (anonymous_class_expression_id, tag);
CREATE INDEX ix_annotation_path_expression_id ON annotation (path_expression_id);
CREATE INDEX annotation_enum_definition_name_tag_idx ON annotation (enum_definition_name, tag);
CREATE INDEX annotation_permissible_value_text_tag_idx ON annotation (permissible_value_text, tag);
CREATE INDEX ix_annotation_import_expression_id ON annotation (import_expression_id);
CREATE INDEX annotation_schema_definition_name_tag_idx ON annotation (schema_definition_name, tag);
CREATE INDEX annotation_type_definition_name_tag_idx ON annotation (type_definition_name, tag);
CREATE INDEX ix_annotation_element_name ON annotation (element_name);
CREATE INDEX ix_annotation_anonymous_expression_id ON annotation (anonymous_expression_id);
CREATE INDEX annotation_path_expression_id_tag_idx ON annotation (path_expression_id, tag);
CREATE INDEX annotation_dimension_expression_id_tag_idx ON annotation (dimension_expression_id, tag);
CREATE INDEX annotation_annotation_tag_tag_idx ON annotation (annotation_tag, tag);
CREATE INDEX ix_annotation_pattern_expression_id ON annotation (pattern_expression_id);
CREATE INDEX ix_annotation_enum_binding_id ON annotation (enum_binding_id);
CREATE INDEX ix_annotation_dimension_expression_id ON annotation (dimension_expression_id);

CREATE TABLE structured_alias_category (
	structured_alias_id INTEGER,
	category TEXT,
	PRIMARY KEY (structured_alias_id, category),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_category_category ON structured_alias_category (category);
CREATE INDEX ix_structured_alias_category_structured_alias_id ON structured_alias_category (structured_alias_id);

CREATE TABLE structured_alias_contexts (
	structured_alias_id INTEGER,
	contexts TEXT,
	PRIMARY KEY (structured_alias_id, contexts),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_contexts_structured_alias_id ON structured_alias_contexts (structured_alias_id);
CREATE INDEX ix_structured_alias_contexts_contexts ON structured_alias_contexts (contexts);

CREATE TABLE structured_alias_todos (
	structured_alias_id INTEGER,
	todos TEXT,
	PRIMARY KEY (structured_alias_id, todos),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_todos_structured_alias_id ON structured_alias_todos (structured_alias_id);
CREATE INDEX ix_structured_alias_todos_todos ON structured_alias_todos (todos);

CREATE TABLE structured_alias_notes (
	structured_alias_id INTEGER,
	notes TEXT,
	PRIMARY KEY (structured_alias_id, notes),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_notes_structured_alias_id ON structured_alias_notes (structured_alias_id);
CREATE INDEX ix_structured_alias_notes_notes ON structured_alias_notes (notes);

CREATE TABLE structured_alias_comments (
	structured_alias_id INTEGER,
	comments TEXT,
	PRIMARY KEY (structured_alias_id, comments),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_comments_comments ON structured_alias_comments (comments);
CREATE INDEX ix_structured_alias_comments_structured_alias_id ON structured_alias_comments (structured_alias_id);

CREATE TABLE structured_alias_in_subset (
	structured_alias_id INTEGER,
	in_subset_name TEXT,
	PRIMARY KEY (structured_alias_id, in_subset_name),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id),
	FOREIGN KEY(in_subset_name) REFERENCES subset_definition (name)
);
CREATE INDEX ix_structured_alias_in_subset_structured_alias_id ON structured_alias_in_subset (structured_alias_id);
CREATE INDEX ix_structured_alias_in_subset_in_subset_name ON structured_alias_in_subset (in_subset_name);

CREATE TABLE structured_alias_see_also (
	structured_alias_id INTEGER,
	see_also TEXT,
	PRIMARY KEY (structured_alias_id, see_also),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_see_also_structured_alias_id ON structured_alias_see_also (structured_alias_id);
CREATE INDEX ix_structured_alias_see_also_see_also ON structured_alias_see_also (see_also);

CREATE TABLE structured_alias_aliases (
	structured_alias_id INTEGER,
	aliases TEXT,
	PRIMARY KEY (structured_alias_id, aliases),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_aliases_aliases ON structured_alias_aliases (aliases);
CREATE INDEX ix_structured_alias_aliases_structured_alias_id ON structured_alias_aliases (structured_alias_id);

CREATE TABLE structured_alias_mappings (
	structured_alias_id INTEGER,
	mappings TEXT,
	PRIMARY KEY (structured_alias_id, mappings),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_mappings_structured_alias_id ON structured_alias_mappings (structured_alias_id);
CREATE INDEX ix_structured_alias_mappings_mappings ON structured_alias_mappings (mappings);

CREATE TABLE structured_alias_exact_mappings (
	structured_alias_id INTEGER,
	exact_mappings TEXT,
	PRIMARY KEY (structured_alias_id, exact_mappings),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_exact_mappings_exact_mappings ON structured_alias_exact_mappings (exact_mappings);
CREATE INDEX ix_structured_alias_exact_mappings_structured_alias_id ON structured_alias_exact_mappings (structured_alias_id);

CREATE TABLE structured_alias_close_mappings (
	structured_alias_id INTEGER,
	close_mappings TEXT,
	PRIMARY KEY (structured_alias_id, close_mappings),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_close_mappings_close_mappings ON structured_alias_close_mappings (close_mappings);
CREATE INDEX ix_structured_alias_close_mappings_structured_alias_id ON structured_alias_close_mappings (structured_alias_id);

CREATE TABLE structured_alias_related_mappings (
	structured_alias_id INTEGER,
	related_mappings TEXT,
	PRIMARY KEY (structured_alias_id, related_mappings),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_related_mappings_structured_alias_id ON structured_alias_related_mappings (structured_alias_id);
CREATE INDEX ix_structured_alias_related_mappings_related_mappings ON structured_alias_related_mappings (related_mappings);

CREATE TABLE structured_alias_narrow_mappings (
	structured_alias_id INTEGER,
	narrow_mappings TEXT,
	PRIMARY KEY (structured_alias_id, narrow_mappings),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_narrow_mappings_structured_alias_id ON structured_alias_narrow_mappings (structured_alias_id);
CREATE INDEX ix_structured_alias_narrow_mappings_narrow_mappings ON structured_alias_narrow_mappings (narrow_mappings);

CREATE TABLE structured_alias_broad_mappings (
	structured_alias_id INTEGER,
	broad_mappings TEXT,
	PRIMARY KEY (structured_alias_id, broad_mappings),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_broad_mappings_structured_alias_id ON structured_alias_broad_mappings (structured_alias_id);
CREATE INDEX ix_structured_alias_broad_mappings_broad_mappings ON structured_alias_broad_mappings (broad_mappings);

CREATE TABLE structured_alias_contributors (
	structured_alias_id INTEGER,
	contributors TEXT,
	PRIMARY KEY (structured_alias_id, contributors),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_contributors_structured_alias_id ON structured_alias_contributors (structured_alias_id);
CREATE INDEX ix_structured_alias_contributors_contributors ON structured_alias_contributors (contributors);

CREATE TABLE structured_alias_keyword (
	structured_alias_id INTEGER,
	keyword TEXT,
	PRIMARY KEY (structured_alias_id, keyword),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE INDEX ix_structured_alias_keyword_structured_alias_id ON structured_alias_keyword (structured_alias_id);
CREATE INDEX ix_structured_alias_keyword_keyword ON structured_alias_keyword (keyword);

CREATE TABLE extension (
	tag TEXT NOT NULL,
	element_name TEXT,
	schema_definition_name TEXT,
	type_definition_name TEXT,
	subset_definition_name TEXT,
	definition_name TEXT,
	enum_definition_name TEXT,
	enum_binding_id INTEGER,
	structured_alias_id INTEGER,
	anonymous_expression_id INTEGER,
	path_expression_id INTEGER,
	anonymous_slot_expression_id INTEGER,
	slot_definition_name TEXT,
	anonymous_class_expression_id INTEGER,
	class_definition_name TEXT,
	class_rule_id INTEGER,
	array_expression_id INTEGER,
	dimension_expression_id INTEGER,
	pattern_expression_id INTEGER,
	import_expression_id INTEGER,
	permissible_value_text TEXT,
	unique_key_unique_key_name TEXT,
	type_mapping_framework TEXT,
	extension_tag TEXT,
	extensible_id INTEGER,
	annotation_tag TEXT,
	value_id INTEGER NOT NULL,
	PRIMARY KEY (tag, element_name, schema_definition_name, type_definition_name, subset_definition_name, definition_name, enum_definition_name, enum_binding_id, structured_alias_id, anonymous_expression_id, path_expression_id, anonymous_slot_expression_id, slot_definition_name, anonymous_class_expression_id, class_definition_name, class_rule_id, array_expression_id, dimension_expression_id, pattern_expression_id, import_expression_id, permissible_value_text, unique_key_unique_key_name, type_mapping_framework, extension_tag, extensible_id, annotation_tag, value_id),
	UNIQUE (element_name, tag),
	UNIQUE (schema_definition_name, tag),
	UNIQUE (type_definition_name, tag),
	UNIQUE (subset_definition_name, tag),
	UNIQUE (definition_name, tag),
	UNIQUE (enum_definition_name, tag),
	UNIQUE (enum_binding_id, tag),
	UNIQUE (structured_alias_id, tag),
	UNIQUE (anonymous_expression_id, tag),
	UNIQUE (path_expression_id, tag),
	UNIQUE (anonymous_slot_expression_id, tag),
	UNIQUE (slot_definition_name, tag),
	UNIQUE (anonymous_class_expression_id, tag),
	UNIQUE (class_definition_name, tag),
	UNIQUE (class_rule_id, tag),
	UNIQUE (array_expression_id, tag),
	UNIQUE (dimension_expression_id, tag),
	UNIQUE (pattern_expression_id, tag),
	UNIQUE (import_expression_id, tag),
	UNIQUE (permissible_value_text, tag),
	UNIQUE (unique_key_unique_key_name, tag),
	UNIQUE (type_mapping_framework, tag),
	UNIQUE (extension_tag, tag),
	UNIQUE (extensible_id, tag),
	UNIQUE (annotation_tag, tag),
	FOREIGN KEY(element_name) REFERENCES element (name),
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name),
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name),
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name),
	FOREIGN KEY(definition_name) REFERENCES definition (name),
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name),
	FOREIGN KEY(enum_binding_id) REFERENCES enum_binding (id),
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id),
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id),
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id),
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id),
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name),
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id),
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name),
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id),
	FOREIGN KEY(array_expression_id) REFERENCES array_expression (id),
	FOREIGN KEY(dimension_expression_id) REFERENCES dimension_expression (id),
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id),
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id),
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text),
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name),
	FOREIGN KEY(type_mapping_framework) REFERENCES type_mapping (framework),
	FOREIGN KEY(extension_tag) REFERENCES extension (tag),
	FOREIGN KEY(extensible_id) REFERENCES extensible (id),
	FOREIGN KEY(annotation_tag) REFERENCES annotation (tag),
	FOREIGN KEY(value_id) REFERENCES "AnyValue" (id)
);
CREATE INDEX extension_type_mapping_framework_tag_idx ON extension (type_mapping_framework, tag);
CREATE INDEX ix_extension_array_expression_id ON extension (array_expression_id);
CREATE INDEX extension_class_rule_id_tag_idx ON extension (class_rule_id, tag);
CREATE INDEX ix_extension_tag ON extension (tag);
CREATE INDEX ix_extension_enum_definition_name ON extension (enum_definition_name);
CREATE INDEX extension_element_name_tag_idx ON extension (element_name, tag);
CREATE INDEX extension_structured_alias_id_tag_idx ON extension (structured_alias_id, tag);
CREATE INDEX ix_extension_class_rule_id ON extension (class_rule_id);
CREATE INDEX extension_import_expression_id_tag_idx ON extension (import_expression_id, tag);
CREATE INDEX ix_extension_value_id ON extension (value_id);
CREATE INDEX extension_definition_name_tag_idx ON extension (definition_name, tag);
CREATE INDEX extension_slot_definition_name_tag_idx ON extension (slot_definition_name, tag);
CREATE INDEX ix_extension_definition_name ON extension (definition_name);
CREATE INDEX ix_extension_annotation_tag ON extension (annotation_tag);
CREATE INDEX ix_extension_class_definition_name ON extension (class_definition_name);
CREATE INDEX ix_extension_extensible_id ON extension (extensible_id);
CREATE INDEX ix_extension_extension_tag ON extension (extension_tag);
CREATE INDEX extension_extension_tag_tag_idx ON extension (extension_tag, tag);
CREATE INDEX extension_array_expression_id_tag_idx ON extension (array_expression_id, tag);
CREATE INDEX extension_anonymous_expression_id_tag_idx ON extension (anonymous_expression_id, tag);
CREATE INDEX ix_extension_subset_definition_name ON extension (subset_definition_name);
CREATE INDEX ix_extension_anonymous_class_expression_id ON extension (anonymous_class_expression_id);
CREATE INDEX ix_extension_type_mapping_framework ON extension (type_mapping_framework);
CREATE INDEX ix_extension_structured_alias_id ON extension (structured_alias_id);
CREATE INDEX ix_extension_type_definition_name ON extension (type_definition_name);
CREATE INDEX extension_permissible_value_text_tag_idx ON extension (permissible_value_text, tag);
CREATE INDEX ix_extension_slot_definition_name ON extension (slot_definition_name);
CREATE INDEX extension_enum_definition_name_tag_idx ON extension (enum_definition_name, tag);
CREATE INDEX extension_anonymous_slot_expression_id_tag_idx ON extension (anonymous_slot_expression_id, tag);
CREATE INDEX extension_anonymous_class_expression_id_tag_idx ON extension (anonymous_class_expression_id, tag);
CREATE INDEX ix_extension_unique_key_unique_key_name ON extension (unique_key_unique_key_name);
CREATE INDEX extension_schema_definition_name_tag_idx ON extension (schema_definition_name, tag);
CREATE INDEX ix_extension_schema_definition_name ON extension (schema_definition_name);
CREATE INDEX ix_extension_anonymous_slot_expression_id ON extension (anonymous_slot_expression_id);
CREATE INDEX ix_extension_permissible_value_text ON extension (permissible_value_text);
CREATE INDEX extension_subset_definition_name_tag_idx ON extension (subset_definition_name, tag);
CREATE INDEX extension_extensible_id_tag_idx ON extension (extensible_id, tag);
CREATE INDEX extension_dimension_expression_id_tag_idx ON extension (dimension_expression_id, tag);
CREATE INDEX extension_path_expression_id_tag_idx ON extension (path_expression_id, tag);
CREATE INDEX ix_extension_path_expression_id ON extension (path_expression_id);
CREATE INDEX ix_extension_import_expression_id ON extension (import_expression_id);
CREATE INDEX ix_extension_element_name ON extension (element_name);
CREATE INDEX extension_type_definition_name_tag_idx ON extension (type_definition_name, tag);
CREATE INDEX extension_unique_key_unique_key_name_tag_idx ON extension (unique_key_unique_key_name, tag);
CREATE INDEX extension_enum_binding_id_tag_idx ON extension (enum_binding_id, tag);
CREATE INDEX extension_class_definition_name_tag_idx ON extension (class_definition_name, tag);
CREATE INDEX ix_extension_anonymous_expression_id ON extension (anonymous_expression_id);
CREATE INDEX ix_extension_pattern_expression_id ON extension (pattern_expression_id);
CREATE INDEX extension_annotation_tag_tag_idx ON extension (annotation_tag, tag);
CREATE INDEX extension_pattern_expression_id_tag_idx ON extension (pattern_expression_id, tag);
CREATE INDEX ix_extension_dimension_expression_id ON extension (dimension_expression_id);
CREATE INDEX ix_extension_enum_binding_id ON extension (enum_binding_id);
