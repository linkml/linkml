-- # Class: "common_metadata" Description: "Generic metadata shared across definitions"
--     * Slot: id Description: 
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: "element" Description: "a named element in the model"
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: definition_uri Description: the "native" URI of the element
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: "schema_definition" Description: "a collection of subset, type, slot and class definitions"
--     * Slot: id Description: The official schema URI
--     * Slot: version Description: particular version of schema
--     * Slot: license Description: license for the schema
--     * Slot: default_prefix Description: default and base prefix -- used for ':' identifiers, @base and @vocab
--     * Slot: default_range Description: default slot range to be used if range element is omitted from a slot definition
--     * Slot: metamodel_version Description: Version of the metamodel used to load the schema
--     * Slot: source_file Description: name, uri or description of the source of the schema
--     * Slot: source_file_date Description: modification date of the source of the schema
--     * Slot: source_file_size Description: size in bytes of the source of the schema
--     * Slot: generation_date Description: date and time that the schema was loaded/generated
--     * Slot: slot_names_unique Description: if true then induced/mangled slot names are not created for class_usage and attributes
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: definition_uri Description: the "native" URI of the element
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: "type_expression" Description: ""
--     * Slot: id Description: 
--     * Slot: pattern Description: the string value of the slot must conform to this regular expression expressed in the string
--     * Slot: implicit_prefix Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
--     * Slot: equals_string Description: the slot must have range string and the value of the slot must equal the specified value
--     * Slot: equals_number Description: the slot must have range of a number and the value of the slot must equal the specified value
--     * Slot: minimum_value Description: for slots with ranges of type number, the value must be equal to or higher than this
--     * Slot: maximum_value Description: for slots with ranges of type number, the value must be equal to or lowe than this
--     * Slot: structured_pattern_id Description: the string value of the slot must conform to the regular expression in the pattern expression
--     * Slot: unit_id Description: an encoding of a unit
-- # Class: "anonymous_type_expression" Description: ""
--     * Slot: id Description: 
--     * Slot: pattern Description: the string value of the slot must conform to this regular expression expressed in the string
--     * Slot: implicit_prefix Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
--     * Slot: equals_string Description: the slot must have range string and the value of the slot must equal the specified value
--     * Slot: equals_number Description: the slot must have range of a number and the value of the slot must equal the specified value
--     * Slot: minimum_value Description: for slots with ranges of type number, the value must be equal to or higher than this
--     * Slot: maximum_value Description: for slots with ranges of type number, the value must be equal to or lowe than this
--     * Slot: structured_pattern_id Description: the string value of the slot must conform to the regular expression in the pattern expression
--     * Slot: unit_id Description: an encoding of a unit
-- # Class: "type_definition" Description: "A data type definition."
--     * Slot: typeof Description: Names a parent type
--     * Slot: base Description: python base type that implements this type definition
--     * Slot: uri Description: The uri that defines the possible values for the type definition
--     * Slot: repr Description: the name of the python object that implements this type definition
--     * Slot: pattern Description: the string value of the slot must conform to this regular expression expressed in the string
--     * Slot: implicit_prefix Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
--     * Slot: equals_string Description: the slot must have range string and the value of the slot must equal the specified value
--     * Slot: equals_number Description: the slot must have range of a number and the value of the slot must equal the specified value
--     * Slot: minimum_value Description: for slots with ranges of type number, the value must be equal to or higher than this
--     * Slot: maximum_value Description: for slots with ranges of type number, the value must be equal to or lowe than this
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: definition_uri Description: the "native" URI of the element
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: structured_pattern_id Description: the string value of the slot must conform to the regular expression in the pattern expression
--     * Slot: unit_id Description: an encoding of a unit
-- # Class: "subset_definition" Description: "the name and description of a subset"
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: definition_uri Description: the "native" URI of the element
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: schema_definition_name Description: Autocreated FK slot
-- # Class: "definition" Description: "base class for definitions"
--     * Slot: is_a Description: specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
--     * Slot: abstract Description: an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
--     * Slot: mixin Description: this slot or class can only be used as a mixin.
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: string_serialization Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objectsFor example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: definition_uri Description: the "native" URI of the element
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: "enum_expression" Description: "An expression that constrains the range of a slot"
--     * Slot: id Description: 
--     * Slot: code_set Description: the identifier of an enumeration code set.
--     * Slot: code_set_tag Description: the version tag of the enumeration code set
--     * Slot: code_set_version Description: the version identifier of the enumeration code set
--     * Slot: pv_formula Description: Defines the specific formula to be used to generate the permissible values.
--     * Slot: reachable_from_id Description: Specifies a query for obtaining a list of permissible values based on graph reachability
--     * Slot: matches_id Description: Specifies a match query that is used to calculate the list of permissible values
-- # Class: "anonymous_enum_expression" Description: "An enum_expression that is not named"
--     * Slot: id Description: 
--     * Slot: code_set Description: the identifier of an enumeration code set.
--     * Slot: code_set_tag Description: the version tag of the enumeration code set
--     * Slot: code_set_version Description: the version identifier of the enumeration code set
--     * Slot: pv_formula Description: Defines the specific formula to be used to generate the permissible values.
--     * Slot: reachable_from_id Description: Specifies a query for obtaining a list of permissible values based on graph reachability
--     * Slot: matches_id Description: Specifies a match query that is used to calculate the list of permissible values
-- # Class: "enum_definition" Description: "List of values that constrain the range of a slot"
--     * Slot: enum_uri Description: URI of the enum in an RDF environment
--     * Slot: code_set Description: the identifier of an enumeration code set.
--     * Slot: code_set_tag Description: the version tag of the enumeration code set
--     * Slot: code_set_version Description: the version identifier of the enumeration code set
--     * Slot: pv_formula Description: Defines the specific formula to be used to generate the permissible values.
--     * Slot: is_a Description: specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
--     * Slot: abstract Description: an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
--     * Slot: mixin Description: this slot or class can only be used as a mixin.
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: string_serialization Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objectsFor example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: definition_uri Description: the "native" URI of the element
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: reachable_from_id Description: Specifies a query for obtaining a list of permissible values based on graph reachability
--     * Slot: matches_id Description: Specifies a match query that is used to calculate the list of permissible values
-- # Class: "match_query" Description: "A query that is used on an enum expression to dynamically obtain a set of permissivle values via a query that matches on properties of the external concepts"
--     * Slot: id Description: 
--     * Slot: identifier_pattern Description: A regular expression that is used to obtain a set of identifiers from a source_ontology to construct a set of permissible values
--     * Slot: source_ontology Description: An ontology or vocabulary or terminology that is used in a query to obtain a set of permissible values
-- # Class: "reachability_query" Description: "A query that is used on an enum expression to dynamically obtain a set of permissible values via walking from a set of source nodes to a set of descendants or ancestors over a set of relationship types"
--     * Slot: id Description: 
--     * Slot: source_ontology Description: An ontology or vocabulary or terminology that is used in a query to obtain a set of permissible values
--     * Slot: is_direct Description: True if the reachability query should only include directly related nodes, if False then include also transitively connected
--     * Slot: include_self Description: True if the query is reflexive
--     * Slot: traverse_up Description: True if the direction of the reachability query is reversed and ancestors are retrieved
-- # Class: "structured_alias" Description: "object that contains meta data about a synonym or alias including where it came from (source) and its scope (narrow, broad, etc.)"
--     * Slot: id Description: 
--     * Slot: literal_form Description: The literal lexical form of a structured alias
--     * Slot: predicate Description: The relationship between an element and its alias 
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
-- # Class: "expression" Description: "general mixin for any class that can represent some form of expression"
--     * Slot: id Description: 
-- # Class: "anonymous_expression" Description: ""
--     * Slot: id Description: 
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: "path_expression" Description: "An expression that describes an abstract path from an object to another through a sequence of slot lookups"
--     * Slot: id Description: 
--     * Slot: reversed Description: true if the slot is to be inversed
--     * Slot: traverse Description: the slot to traverse
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: followed_by_id Description: in a sequential list, this indicates the next member
--     * Slot: range_expression_id Description: A range that is described as a boolean expression combining existing ranges
-- # Class: "slot_expression" Description: "an expression that constrains the range of values a slot can take"
--     * Slot: id Description: 
--     * Slot: range Description: defines the type of the object of the slot.  Given the following slot definition  S1:    domain: C1    range:  C2the declaration  X:    S1: Yimplicitly asserts Y is an instance of C2
--     * Slot: required Description: true means that the slot must be present in the loaded definition
--     * Slot: recommended Description: true means that the slot should be present in the loaded definition, but this is not required
--     * Slot: inlined Description: True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
--     * Slot: inlined_as_list Description: True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
--     * Slot: minimum_value Description: for slots with ranges of type number, the value must be equal to or higher than this
--     * Slot: maximum_value Description: for slots with ranges of type number, the value must be equal to or lowe than this
--     * Slot: pattern Description: the string value of the slot must conform to this regular expression expressed in the string
--     * Slot: implicit_prefix Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
--     * Slot: equals_string Description: the slot must have range string and the value of the slot must equal the specified value
--     * Slot: equals_number Description: the slot must have range of a number and the value of the slot must equal the specified value
--     * Slot: equals_expression Description: the value of the slot must equal the value of the evaluated expression
--     * Slot: minimum_cardinality Description: the minimum number of entries for a multivalued slot
--     * Slot: maximum_cardinality Description: the maximum number of entries for a multivalued slot
--     * Slot: range_expression_id Description: A range that is described as a boolean expression combining existing ranges
--     * Slot: enum_range_id Description: An inlined enumeration
--     * Slot: structured_pattern_id Description: the string value of the slot must conform to the regular expression in the pattern expression
--     * Slot: unit_id Description: an encoding of a unit
--     * Slot: has_member_id Description: the values of the slot is multivalued with at least one member satisfying the condition
-- # Class: "anonymous_slot_expression" Description: ""
--     * Slot: id Description: 
--     * Slot: range Description: defines the type of the object of the slot.  Given the following slot definition  S1:    domain: C1    range:  C2the declaration  X:    S1: Yimplicitly asserts Y is an instance of C2
--     * Slot: required Description: true means that the slot must be present in the loaded definition
--     * Slot: recommended Description: true means that the slot should be present in the loaded definition, but this is not required
--     * Slot: inlined Description: True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
--     * Slot: inlined_as_list Description: True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
--     * Slot: minimum_value Description: for slots with ranges of type number, the value must be equal to or higher than this
--     * Slot: maximum_value Description: for slots with ranges of type number, the value must be equal to or lowe than this
--     * Slot: pattern Description: the string value of the slot must conform to this regular expression expressed in the string
--     * Slot: implicit_prefix Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
--     * Slot: equals_string Description: the slot must have range string and the value of the slot must equal the specified value
--     * Slot: equals_number Description: the slot must have range of a number and the value of the slot must equal the specified value
--     * Slot: equals_expression Description: the value of the slot must equal the value of the evaluated expression
--     * Slot: minimum_cardinality Description: the minimum number of entries for a multivalued slot
--     * Slot: maximum_cardinality Description: the maximum number of entries for a multivalued slot
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: range_expression_id Description: A range that is described as a boolean expression combining existing ranges
--     * Slot: enum_range_id Description: An inlined enumeration
--     * Slot: structured_pattern_id Description: the string value of the slot must conform to the regular expression in the pattern expression
--     * Slot: unit_id Description: an encoding of a unit
--     * Slot: has_member_id Description: the values of the slot is multivalued with at least one member satisfying the condition
-- # Class: "slot_definition" Description: "the definition of a property or a slot"
--     * Slot: singular_name Description: a name that is used in the singular form
--     * Slot: domain Description: defines the type of the subject of the slot.  Given the following slot definition  S1:    domain: C1    range:  C2the declaration  X:    S1: Yimplicitly asserts that X is an instance of C1
--     * Slot: slot_uri Description: predicate of this slot for semantic web application
--     * Slot: multivalued Description: true means that slot can have more than one value
--     * Slot: inherited Description: true means that the *value* of a slot is inherited by subclasses
--     * Slot: readonly Description: If present, slot is read only.  Text explains why
--     * Slot: ifabsent Description: function that provides a default value for the slot. * [Tt]rue -- boolean True  * [Ff]alse -- boolean False  * int(value) -- integer value  * str(value) -- string value  * default_range -- schema default range  * bnode -- blank node identifier  * slot_uri -- URI for the slot  * class_curie -- CURIE for the containing class  * class_uri -- URI for the containing class
--     * Slot: list_elements_unique Description: If True, then there must be no duplicates in the elements of a multivalued slot
--     * Slot: list_elements_ordered Description: If True, then the order of elements of a multivalued slot is guaranteed to be preserved. If False, the order may still be preserved but this is not guaranteed
--     * Slot: shared Description: If True, then the relationship between the slot domain and range is many to one or many to many
--     * Slot: key Description: True means that the key slot(s) uniquely identify the container.
--     * Slot: identifier Description: True means that the key slot(s) uniquely identify the container. There can be at most one identifier or key per container
--     * Slot: designates_type Description: True means that the key slot(s) is used to determine the instantiation (types) relation between objects and a ClassDefinition
--     * Slot: alias Description: the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.
--     * Slot: owner Description: the "owner" of the slot. It is the class if it appears in the slots list, otherwise the declaring slot
--     * Slot: subproperty_of Description: Ontology property which this slot is a subproperty of.  Note: setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
--     * Slot: symmetric Description: If s is symmetric, and i.s=v, then v.s=i
--     * Slot: reflexive Description: If s is reflexive, then i.s=i for all instances i
--     * Slot: locally_reflexive Description: If s is locally_reflexive, then i.s=i for all instances i where s if a class slot for the type of i
--     * Slot: irreflexive Description: If s is irreflexive, then there exists no i such i.s=i
--     * Slot: asymmetric Description: If s is antisymmetric, and i.s=v where i is different from v, v.s cannot have value i
--     * Slot: transitive Description: If s is transitive, and i.s=z, and s.s=j, then i.s=j
--     * Slot: inverse Description: indicates that any instance of d s r implies that there is also an instance of r s' d
--     * Slot: is_class_field Description: indicates that any instance, i,  the domain of this slot will include an assert of i s range
--     * Slot: transitive_form_of Description: If s transitive_form_of d, then (1) s holds whenever d holds (2) s is transitive (3) d holds whenever s holds and there are no intermediates, and s is not reflexive
--     * Slot: reflexive_transitive_form_of Description: transitive_form_of including the reflexive case
--     * Slot: role Description: the role played by the slot range
--     * Slot: is_usage_slot Description: True means that this slot was defined in a slot_usage situation
--     * Slot: usage_slot_name Description: The name of the slot referenced in the slot_usage
--     * Slot: relational_role Description: the role a slot on a relationship class plays, for example, the subject, object or predicate roles
--     * Slot: slot_group Description: allows for grouping of related slots into a grouping slot that serves the role of a group
--     * Slot: is_grouping_slot Description: true if this slot is a grouping slot
--     * Slot: children_are_mutually_disjoint Description: If true then all direct is_a children are mutually disjoint and share no instances in common
--     * Slot: range Description: defines the type of the object of the slot.  Given the following slot definition  S1:    domain: C1    range:  C2the declaration  X:    S1: Yimplicitly asserts Y is an instance of C2
--     * Slot: required Description: true means that the slot must be present in the loaded definition
--     * Slot: recommended Description: true means that the slot should be present in the loaded definition, but this is not required
--     * Slot: inlined Description: True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
--     * Slot: inlined_as_list Description: True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
--     * Slot: minimum_value Description: for slots with ranges of type number, the value must be equal to or higher than this
--     * Slot: maximum_value Description: for slots with ranges of type number, the value must be equal to or lowe than this
--     * Slot: pattern Description: the string value of the slot must conform to this regular expression expressed in the string
--     * Slot: implicit_prefix Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
--     * Slot: equals_string Description: the slot must have range string and the value of the slot must equal the specified value
--     * Slot: equals_number Description: the slot must have range of a number and the value of the slot must equal the specified value
--     * Slot: equals_expression Description: the value of the slot must equal the value of the evaluated expression
--     * Slot: minimum_cardinality Description: the minimum number of entries for a multivalued slot
--     * Slot: maximum_cardinality Description: the maximum number of entries for a multivalued slot
--     * Slot: is_a Description: specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
--     * Slot: abstract Description: an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
--     * Slot: mixin Description: this slot or class can only be used as a mixin.
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: string_serialization Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objectsFor example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: definition_uri Description: the "native" URI of the element
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: slot_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: class_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: path_rule_id Description: a rule for inferring a slot assignment based on evaluating a path through a sequence of slot assignments
--     * Slot: range_expression_id Description: A range that is described as a boolean expression combining existing ranges
--     * Slot: enum_range_id Description: An inlined enumeration
--     * Slot: structured_pattern_id Description: the string value of the slot must conform to the regular expression in the pattern expression
--     * Slot: unit_id Description: an encoding of a unit
--     * Slot: has_member_id Description: the values of the slot is multivalued with at least one member satisfying the condition
-- # Class: "class_expression" Description: "A boolean expression that can be used to dynamically determine membership of a class"
--     * Slot: id Description: 
-- # Class: "anonymous_class_expression" Description: ""
--     * Slot: id Description: 
--     * Slot: is_a Description: specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: class_definition_name Description: Autocreated FK slot
-- # Class: "class_definition" Description: "the definition of a class or interface"
--     * Slot: class_uri Description: URI of the class in an RDF environment
--     * Slot: subclass_of Description: rdfs:subClassOf to be emitted in OWL generation
--     * Slot: tree_root Description: indicator that this is the root class in tree structures
--     * Slot: slot_names_unique Description: if true then induced/mangled slot names are not created for class_usage and attributes
--     * Slot: represents_relationship Description: true if this class represents a relationship rather than an entity
--     * Slot: children_are_mutually_disjoint Description: If true then all direct is_a children are mutually disjoint and share no instances in common
--     * Slot: is_a Description: specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
--     * Slot: abstract Description: an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
--     * Slot: mixin Description: this slot or class can only be used as a mixin.
--     * Slot: created_by Description: agent that created the element
--     * Slot: created_on Description: time at which the element was created
--     * Slot: last_updated_on Description: time at which the element was last updated
--     * Slot: modified_by Description: agent that modified the element
--     * Slot: status Description: status of the element
--     * Slot: string_serialization Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objectsFor example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
--     * Slot: name Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
--     * Slot: definition_uri Description: the "native" URI of the element
--     * Slot: conforms_to Description: An established standard to which the element conforms.
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: schema_definition_name Description: Autocreated FK slot
-- # Class: "class_level_rule" Description: "A rule that is applied to classes"
--     * Slot: id Description: 
-- # Class: "class_rule" Description: "A rule that applies to instances of a class"
--     * Slot: id Description: 
--     * Slot: bidirectional Description: in addition to preconditions entailing postconditions, the postconditions entail the preconditions
--     * Slot: open_world Description: if true, the the postconditions may be omitted in instance data, but it is valid for an inference engine to add these
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: deactivated Description: a deactivated rule is not executed by the rules engine
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: preconditions_id Description: an expression that must hold in order for the rule to be applicable to an instance
--     * Slot: postconditions_id Description: an expression that must hold for an instance of the class, if the preconditions hold
--     * Slot: elseconditions_id Description: an expression that must hold for an instance of the class, if the preconditions no not hold
-- # Class: "pattern_expression" Description: "a regular expression pattern used to evaluate conformance of a string"
--     * Slot: id Description: 
--     * Slot: syntax Description: the string value of the slot must conform to this regular expression expressed in the string. May be interpolated.
--     * Slot: interpolated Description: if true then the pattern is first string interpolated
--     * Slot: partial_match Description: if true then the pattern must match the whole string, as if enclosed in ^...$
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: "import_expression" Description: "an expression describing an import"
--     * Slot: id Description: 
--     * Slot: import_from Description: 
--     * Slot: import_as Description: 
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
-- # Class: "setting" Description: "assignment of a key to a value"
--     * Slot: setting_key Description: the variable name for a setting
--     * Slot: setting_value Description: The value assigned for a setting
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: import_expression_id Description: Autocreated FK slot
-- # Class: "prefix" Description: "prefix URI tuple"
--     * Slot: prefix_prefix Description: the nsname (sans ':' for a given prefix)
--     * Slot: prefix_reference Description: A URI associated with a given prefix
--     * Slot: schema_definition_name Description: Autocreated FK slot
-- # Class: "local_name" Description: "an attributed label"
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
-- # Class: "example" Description: "usage example and description"
--     * Slot: id Description: 
--     * Slot: value Description: example value
--     * Slot: description Description: description of what the value is doing
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
-- # Class: "alt_description" Description: "an attributed description"
--     * Slot: source Description: the source of an attributed description
--     * Slot: description Description: text of an attributed description
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
-- # Class: "permissible_value" Description: "a permissible value, accompanied by intended text and an optional mapping to a concept URI"
--     * Slot: text Description: 
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: meaning Description: the value meaning of a permissible value
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: enum_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_enum_expression_id Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: unit_id Description: an encoding of a unit
-- # Class: "unique_key" Description: "a collection of slots whose values uniquely identify an instance of a class"
--     * Slot: unique_key_name Description: name of the unique key
--     * Slot: description Description: a description of the element's purpose and use
--     * Slot: title Description: the official title of the element
--     * Slot: deprecated Description: Description of why and when this element will no longer be used
--     * Slot: from_schema Description: id of the schema that defined the element
--     * Slot: imported_from Description: the imports entry that this element was derived from.  Empty means primary source
--     * Slot: source Description: A related resource from which the element is derived.
--     * Slot: in_language Description: 
--     * Slot: deprecated_element_has_exact_replacement Description: When an element is deprecated, it can be automatically replaced by this uri or curie
--     * Slot: deprecated_element_has_possible_replacement Description: When an element is deprecated, it can be potentially replaced by this uri or curie
--     * Slot: rank Description: the relative order in which the element occurs, lower values are given precedence
--     * Slot: class_definition_name Description: Autocreated FK slot
-- # Class: "UnitOfMeasure" Description: "A unit of measure, or unit, is a particular quantity value that has been chosen as a scale for measuring other quantities the same kind (more generally of equivalent dimension)."
--     * Slot: id Description: 
--     * Slot: symbol Description: name of the unit encoded as a symbol
--     * Slot: ucum_code Description: associates a QUDT unit with its UCUM code (case-sensitive).
--     * Slot: derivation Description: Expression for deriving this unit from other units
--     * Slot: has_quantity_kind Description: Concept in a vocabulary or ontology that denotes the kind of quantity being measured, e.g. length
--     * Slot: iec61360code Description: 
-- # Class: "annotatable" Description: "mixin for classes that support annotations"
--     * Slot: id Description: 
-- # Class: "annotation" Description: "a tag/value pair with the semantics of OWL Annotation"
--     * Slot: tag Description: a tag associated with an extension
--     * Slot: value Description: the actual annotation
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: annotatable_id Description: Autocreated FK slot
--     * Slot: annotation_tag Description: Autocreated FK slot
-- # Class: "extension" Description: "a tag/value pair used to add non-model information to an entry"
--     * Slot: tag Description: a tag associated with an extension
--     * Slot: value Description: the actual annotation
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: annotation_tag Description: Autocreated FK slot
--     * Slot: extension_tag Description: Autocreated FK slot
--     * Slot: extensible_id Description: Autocreated FK slot
-- # Class: "extensible" Description: "mixin for classes that support extension"
--     * Slot: id Description: 
-- # Class: "common_metadata_todos" Description: ""
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "common_metadata_notes" Description: ""
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "common_metadata_comments" Description: ""
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "common_metadata_in_subset" Description: ""
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "common_metadata_see_also" Description: ""
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "common_metadata_aliases" Description: ""
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "common_metadata_mappings" Description: ""
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "common_metadata_exact_mappings" Description: ""
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "common_metadata_close_mappings" Description: ""
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "common_metadata_related_mappings" Description: ""
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "common_metadata_narrow_mappings" Description: ""
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "common_metadata_broad_mappings" Description: ""
--     * Slot: common_metadata_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "element_id_prefixes" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: "element_todos" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "element_notes" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "element_comments" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "element_in_subset" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "element_see_also" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "element_aliases" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "element_mappings" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "element_exact_mappings" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "element_close_mappings" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "element_related_mappings" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "element_narrow_mappings" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "element_broad_mappings" Description: ""
--     * Slot: element_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "schema_definition_imports" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: imports Description: other schemas that are included in this schema
-- # Class: "schema_definition_emit_prefixes" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: emit_prefixes Description: a list of Curie prefixes that are used in the representation of instances of the model.  All prefixes in this list are added to the prefix sections of the target models.
-- # Class: "schema_definition_default_curi_maps" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: default_curi_maps Description: ordered list of prefixcommon biocontexts to be fetched to resolve id prefixes and inline prefix variables
-- # Class: "schema_definition_category" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: category Description: controlled terms used to categorize an element
-- # Class: "schema_definition_keyword" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: keyword Description: Keywords or tags used to describe the element
-- # Class: "schema_definition_id_prefixes" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: "schema_definition_todos" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "schema_definition_notes" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "schema_definition_comments" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "schema_definition_in_subset" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "schema_definition_see_also" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "schema_definition_aliases" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "schema_definition_mappings" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "schema_definition_exact_mappings" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "schema_definition_close_mappings" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "schema_definition_related_mappings" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "schema_definition_narrow_mappings" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "schema_definition_broad_mappings" Description: ""
--     * Slot: schema_definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "type_expression_equals_string_in" Description: ""
--     * Slot: type_expression_id Description: Autocreated FK slot
--     * Slot: equals_string_in Description: the slot must have range string and the value of the slot must equal one of the specified values
-- # Class: "type_expression_none_of" Description: ""
--     * Slot: type_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: "type_expression_exactly_one_of" Description: ""
--     * Slot: type_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: "type_expression_any_of" Description: ""
--     * Slot: type_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: "type_expression_all_of" Description: ""
--     * Slot: type_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: "anonymous_type_expression_equals_string_in" Description: ""
--     * Slot: anonymous_type_expression_id Description: Autocreated FK slot
--     * Slot: equals_string_in Description: the slot must have range string and the value of the slot must equal one of the specified values
-- # Class: "anonymous_type_expression_none_of" Description: ""
--     * Slot: anonymous_type_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: "anonymous_type_expression_exactly_one_of" Description: ""
--     * Slot: anonymous_type_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: "anonymous_type_expression_any_of" Description: ""
--     * Slot: anonymous_type_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: "anonymous_type_expression_all_of" Description: ""
--     * Slot: anonymous_type_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: "type_definition_union_of" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: union_of Description: indicates that the domain element consists exactly of the members of the element in the range.
-- # Class: "type_definition_equals_string_in" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: equals_string_in Description: the slot must have range string and the value of the slot must equal one of the specified values
-- # Class: "type_definition_none_of" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: "type_definition_exactly_one_of" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: "type_definition_any_of" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: "type_definition_all_of" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: "type_definition_id_prefixes" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: "type_definition_todos" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "type_definition_notes" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "type_definition_comments" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "type_definition_in_subset" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "type_definition_see_also" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "type_definition_aliases" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "type_definition_mappings" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "type_definition_exact_mappings" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "type_definition_close_mappings" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "type_definition_related_mappings" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "type_definition_narrow_mappings" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "type_definition_broad_mappings" Description: ""
--     * Slot: type_definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "subset_definition_id_prefixes" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: "subset_definition_todos" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "subset_definition_notes" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "subset_definition_comments" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "subset_definition_in_subset" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "subset_definition_see_also" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "subset_definition_aliases" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "subset_definition_mappings" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "subset_definition_exact_mappings" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "subset_definition_close_mappings" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "subset_definition_related_mappings" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "subset_definition_narrow_mappings" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "subset_definition_broad_mappings" Description: ""
--     * Slot: subset_definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "definition_mixins" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: mixins Description: List of definitions to be mixed in. Targets may be any definition of the same type
-- # Class: "definition_apply_to" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: apply_to Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
-- # Class: "definition_values_from" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: values_from Description: The identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
-- # Class: "definition_id_prefixes" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: "definition_todos" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "definition_notes" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "definition_comments" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "definition_in_subset" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "definition_see_also" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "definition_aliases" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "definition_mappings" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "definition_exact_mappings" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "definition_close_mappings" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "definition_related_mappings" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "definition_narrow_mappings" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "definition_broad_mappings" Description: ""
--     * Slot: definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "enum_expression_include" Description: ""
--     * Slot: enum_expression_id Description: Autocreated FK slot
--     * Slot: include_id Description: An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set
-- # Class: "enum_expression_minus" Description: ""
--     * Slot: enum_expression_id Description: Autocreated FK slot
--     * Slot: minus_id Description: An enum expression that yields a list of permissible values that are to be subtracted from the enum
-- # Class: "enum_expression_inherits" Description: ""
--     * Slot: enum_expression_id Description: Autocreated FK slot
--     * Slot: inherits Description: An enum definition that is used as the basis to create a new enum
-- # Class: "enum_expression_concepts" Description: ""
--     * Slot: enum_expression_id Description: Autocreated FK slot
--     * Slot: concepts Description: A list of identifiers that are used to construct a set of permissible values
-- # Class: "anonymous_enum_expression_include" Description: ""
--     * Slot: anonymous_enum_expression_id Description: Autocreated FK slot
--     * Slot: include_id Description: An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set
-- # Class: "anonymous_enum_expression_minus" Description: ""
--     * Slot: anonymous_enum_expression_id Description: Autocreated FK slot
--     * Slot: minus_id Description: An enum expression that yields a list of permissible values that are to be subtracted from the enum
-- # Class: "anonymous_enum_expression_inherits" Description: ""
--     * Slot: anonymous_enum_expression_id Description: Autocreated FK slot
--     * Slot: inherits Description: An enum definition that is used as the basis to create a new enum
-- # Class: "anonymous_enum_expression_concepts" Description: ""
--     * Slot: anonymous_enum_expression_id Description: Autocreated FK slot
--     * Slot: concepts Description: A list of identifiers that are used to construct a set of permissible values
-- # Class: "enum_definition_include" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: include_id Description: An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set
-- # Class: "enum_definition_minus" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: minus_id Description: An enum expression that yields a list of permissible values that are to be subtracted from the enum
-- # Class: "enum_definition_inherits" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: inherits Description: An enum definition that is used as the basis to create a new enum
-- # Class: "enum_definition_concepts" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: concepts Description: A list of identifiers that are used to construct a set of permissible values
-- # Class: "enum_definition_mixins" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: mixins Description: List of definitions to be mixed in. Targets may be any definition of the same type
-- # Class: "enum_definition_apply_to" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: apply_to Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
-- # Class: "enum_definition_values_from" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: values_from Description: The identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
-- # Class: "enum_definition_id_prefixes" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: "enum_definition_todos" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "enum_definition_notes" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "enum_definition_comments" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "enum_definition_in_subset" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "enum_definition_see_also" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "enum_definition_aliases" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "enum_definition_mappings" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "enum_definition_exact_mappings" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "enum_definition_close_mappings" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "enum_definition_related_mappings" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "enum_definition_narrow_mappings" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "enum_definition_broad_mappings" Description: ""
--     * Slot: enum_definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "reachability_query_source_nodes" Description: ""
--     * Slot: reachability_query_id Description: Autocreated FK slot
--     * Slot: source_nodes Description: A list of nodes that are used in the reachability query
-- # Class: "reachability_query_relationship_types" Description: ""
--     * Slot: reachability_query_id Description: Autocreated FK slot
--     * Slot: relationship_types Description: A list of relationship types (properties) that are used in a reachability query
-- # Class: "structured_alias_category" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: category Description: The category or categories of an alias. This can be drawn from any relevant vocabulary
-- # Class: "structured_alias_todos" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "structured_alias_notes" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "structured_alias_comments" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "structured_alias_in_subset" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "structured_alias_see_also" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "structured_alias_aliases" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "structured_alias_mappings" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "structured_alias_exact_mappings" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "structured_alias_close_mappings" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "structured_alias_related_mappings" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "structured_alias_narrow_mappings" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "structured_alias_broad_mappings" Description: ""
--     * Slot: structured_alias_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "anonymous_expression_todos" Description: ""
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "anonymous_expression_notes" Description: ""
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "anonymous_expression_comments" Description: ""
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "anonymous_expression_in_subset" Description: ""
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "anonymous_expression_see_also" Description: ""
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "anonymous_expression_aliases" Description: ""
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "anonymous_expression_mappings" Description: ""
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "anonymous_expression_exact_mappings" Description: ""
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "anonymous_expression_close_mappings" Description: ""
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "anonymous_expression_related_mappings" Description: ""
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "anonymous_expression_narrow_mappings" Description: ""
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "anonymous_expression_broad_mappings" Description: ""
--     * Slot: anonymous_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "path_expression_none_of" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: "path_expression_any_of" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: "path_expression_all_of" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: "path_expression_exactly_one_of" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: "path_expression_todos" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "path_expression_notes" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "path_expression_comments" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "path_expression_in_subset" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "path_expression_see_also" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "path_expression_aliases" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "path_expression_mappings" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "path_expression_exact_mappings" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "path_expression_close_mappings" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "path_expression_related_mappings" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "path_expression_narrow_mappings" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "path_expression_broad_mappings" Description: ""
--     * Slot: path_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "slot_expression_equals_string_in" Description: ""
--     * Slot: slot_expression_id Description: Autocreated FK slot
--     * Slot: equals_string_in Description: the slot must have range string and the value of the slot must equal one of the specified values
-- # Class: "slot_expression_none_of" Description: ""
--     * Slot: slot_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: "slot_expression_exactly_one_of" Description: ""
--     * Slot: slot_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: "slot_expression_any_of" Description: ""
--     * Slot: slot_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: "slot_expression_all_of" Description: ""
--     * Slot: slot_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: "anonymous_slot_expression_equals_string_in" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: equals_string_in Description: the slot must have range string and the value of the slot must equal one of the specified values
-- # Class: "anonymous_slot_expression_none_of" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: "anonymous_slot_expression_exactly_one_of" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: "anonymous_slot_expression_any_of" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: "anonymous_slot_expression_all_of" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: "anonymous_slot_expression_todos" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "anonymous_slot_expression_notes" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "anonymous_slot_expression_comments" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "anonymous_slot_expression_in_subset" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "anonymous_slot_expression_see_also" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "anonymous_slot_expression_aliases" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "anonymous_slot_expression_mappings" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "anonymous_slot_expression_exact_mappings" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "anonymous_slot_expression_close_mappings" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "anonymous_slot_expression_related_mappings" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "anonymous_slot_expression_narrow_mappings" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "anonymous_slot_expression_broad_mappings" Description: ""
--     * Slot: anonymous_slot_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "slot_definition_domain_of" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: domain_of Description: the class(es) that reference the slot in a "slots" or "slot_usage" context
-- # Class: "slot_definition_disjoint_with" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: disjoint_with Description: Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances
-- # Class: "slot_definition_union_of" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: union_of Description: indicates that the domain element consists exactly of the members of the element in the range.
-- # Class: "slot_definition_equals_string_in" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: equals_string_in Description: the slot must have range string and the value of the slot must equal one of the specified values
-- # Class: "slot_definition_none_of" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: "slot_definition_exactly_one_of" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: "slot_definition_any_of" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: "slot_definition_all_of" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: "slot_definition_mixins" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: mixins Description: List of definitions to be mixed in. Targets may be any definition of the same type
-- # Class: "slot_definition_apply_to" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: apply_to Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
-- # Class: "slot_definition_values_from" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: values_from Description: The identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
-- # Class: "slot_definition_id_prefixes" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: "slot_definition_todos" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "slot_definition_notes" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "slot_definition_comments" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "slot_definition_in_subset" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "slot_definition_see_also" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "slot_definition_aliases" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "slot_definition_mappings" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "slot_definition_exact_mappings" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "slot_definition_close_mappings" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "slot_definition_related_mappings" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "slot_definition_narrow_mappings" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "slot_definition_broad_mappings" Description: ""
--     * Slot: slot_definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "class_expression_any_of" Description: ""
--     * Slot: class_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: "class_expression_exactly_one_of" Description: ""
--     * Slot: class_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: "class_expression_none_of" Description: ""
--     * Slot: class_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: "class_expression_all_of" Description: ""
--     * Slot: class_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: "anonymous_class_expression_any_of" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: "anonymous_class_expression_exactly_one_of" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: "anonymous_class_expression_none_of" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: "anonymous_class_expression_all_of" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: "anonymous_class_expression_todos" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "anonymous_class_expression_notes" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "anonymous_class_expression_comments" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "anonymous_class_expression_in_subset" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "anonymous_class_expression_see_also" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "anonymous_class_expression_aliases" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "anonymous_class_expression_mappings" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "anonymous_class_expression_exact_mappings" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "anonymous_class_expression_close_mappings" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "anonymous_class_expression_related_mappings" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "anonymous_class_expression_narrow_mappings" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "anonymous_class_expression_broad_mappings" Description: ""
--     * Slot: anonymous_class_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "class_definition_slots" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: slots Description: list of slot names that are applicable to a class
-- # Class: "class_definition_union_of" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: union_of Description: indicates that the domain element consists exactly of the members of the element in the range.
-- # Class: "class_definition_defining_slots" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: defining_slots Description: The combination of is a plus defining slots form a genus-differentia definition, or the set of necessary and sufficient conditions that can be transformed into an OWL equivalence axiom
-- # Class: "class_definition_disjoint_with" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: disjoint_with Description: Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances
-- # Class: "class_definition_any_of" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: any_of_id Description: holds if at least one of the expressions hold
-- # Class: "class_definition_exactly_one_of" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: exactly_one_of_id Description: holds if only one of the expressions hold
-- # Class: "class_definition_none_of" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: none_of_id Description: holds if none of the expressions hold
-- # Class: "class_definition_all_of" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: all_of_id Description: holds if all of the expressions hold
-- # Class: "class_definition_mixins" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: mixins Description: List of definitions to be mixed in. Targets may be any definition of the same type
-- # Class: "class_definition_apply_to" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: apply_to Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
-- # Class: "class_definition_values_from" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: values_from Description: The identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
-- # Class: "class_definition_id_prefixes" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: id_prefixes Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
-- # Class: "class_definition_todos" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "class_definition_notes" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "class_definition_comments" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "class_definition_in_subset" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "class_definition_see_also" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "class_definition_aliases" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "class_definition_mappings" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "class_definition_exact_mappings" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "class_definition_close_mappings" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "class_definition_related_mappings" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "class_definition_narrow_mappings" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "class_definition_broad_mappings" Description: ""
--     * Slot: class_definition_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "class_rule_todos" Description: ""
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "class_rule_notes" Description: ""
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "class_rule_comments" Description: ""
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "class_rule_in_subset" Description: ""
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "class_rule_see_also" Description: ""
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "class_rule_aliases" Description: ""
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "class_rule_mappings" Description: ""
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "class_rule_exact_mappings" Description: ""
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "class_rule_close_mappings" Description: ""
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "class_rule_related_mappings" Description: ""
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "class_rule_narrow_mappings" Description: ""
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "class_rule_broad_mappings" Description: ""
--     * Slot: class_rule_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "pattern_expression_todos" Description: ""
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "pattern_expression_notes" Description: ""
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "pattern_expression_comments" Description: ""
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "pattern_expression_in_subset" Description: ""
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "pattern_expression_see_also" Description: ""
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "pattern_expression_aliases" Description: ""
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "pattern_expression_mappings" Description: ""
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "pattern_expression_exact_mappings" Description: ""
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "pattern_expression_close_mappings" Description: ""
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "pattern_expression_related_mappings" Description: ""
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "pattern_expression_narrow_mappings" Description: ""
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "pattern_expression_broad_mappings" Description: ""
--     * Slot: pattern_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "import_expression_todos" Description: ""
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "import_expression_notes" Description: ""
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "import_expression_comments" Description: ""
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "import_expression_in_subset" Description: ""
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "import_expression_see_also" Description: ""
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "import_expression_aliases" Description: ""
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "import_expression_mappings" Description: ""
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "import_expression_exact_mappings" Description: ""
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "import_expression_close_mappings" Description: ""
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "import_expression_related_mappings" Description: ""
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "import_expression_narrow_mappings" Description: ""
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "import_expression_broad_mappings" Description: ""
--     * Slot: import_expression_id Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "permissible_value_todos" Description: ""
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "permissible_value_notes" Description: ""
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "permissible_value_comments" Description: ""
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "permissible_value_in_subset" Description: ""
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "permissible_value_see_also" Description: ""
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "permissible_value_aliases" Description: ""
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "permissible_value_mappings" Description: ""
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "permissible_value_exact_mappings" Description: ""
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "permissible_value_close_mappings" Description: ""
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "permissible_value_related_mappings" Description: ""
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "permissible_value_narrow_mappings" Description: ""
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "permissible_value_broad_mappings" Description: ""
--     * Slot: permissible_value_text Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "unique_key_unique_key_slots" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: unique_key_slots Description: list of slot names that form a key
-- # Class: "unique_key_todos" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: todos Description: Outstanding issue that needs resolution
-- # Class: "unique_key_notes" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: notes Description: editorial notes about an element intended for internal consumption
-- # Class: "unique_key_comments" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: comments Description: notes and comments about an element intended for external consumption
-- # Class: "unique_key_in_subset" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: in_subset Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
-- # Class: "unique_key_see_also" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: see_also Description: a reference
-- # Class: "unique_key_aliases" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: aliases Description: 
-- # Class: "unique_key_mappings" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: mappings Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
-- # Class: "unique_key_exact_mappings" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: exact_mappings Description: A list of terms from different schemas or terminology systems that have identical meaning.
-- # Class: "unique_key_close_mappings" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: close_mappings Description: A list of terms from different schemas or terminology systems that have close meaning.
-- # Class: "unique_key_related_mappings" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: related_mappings Description: A list of terms from different schemas or terminology systems that have related meaning.
-- # Class: "unique_key_narrow_mappings" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: narrow_mappings Description: A list of terms from different schemas or terminology systems that have narrower meaning.
-- # Class: "unique_key_broad_mappings" Description: ""
--     * Slot: unique_key_unique_key_name Description: Autocreated FK slot
--     * Slot: broad_mappings Description: A list of terms from different schemas or terminology systems that have broader meaning.
-- # Class: "UnitOfMeasure_exact_mappings" Description: ""
--     * Slot: UnitOfMeasure_id Description: Autocreated FK slot
--     * Slot: exact_mappings Description: Used to link a unit to equivalent concepts in ontologies such as UO, SNOMED, OEM, OBOE, NCIT

CREATE TABLE common_metadata (
	id INTEGER, 
	description TEXT, 
	title TEXT, 
	deprecated TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	rank INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE element (
	name TEXT, 
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
	rank INTEGER, 
	PRIMARY KEY (name)
);
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
	name TEXT, 
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
	rank INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(default_range) REFERENCES type_definition (name)
);
CREATE TABLE type_definition (
	typeof TEXT, 
	base TEXT, 
	uri TEXT, 
	repr TEXT, 
	pattern TEXT, 
	implicit_prefix TEXT, 
	equals_string TEXT, 
	equals_number INTEGER, 
	minimum_value INTEGER, 
	maximum_value INTEGER, 
	name TEXT, 
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
	rank INTEGER, 
	schema_definition_name TEXT, 
	structured_pattern_id TEXT, 
	unit_id TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(typeof) REFERENCES type_definition (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(structured_pattern_id) REFERENCES pattern_expression (id), 
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id)
);
CREATE TABLE definition (
	is_a TEXT, 
	abstract BOOLEAN, 
	mixin BOOLEAN, 
	created_by TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	string_serialization TEXT, 
	name TEXT, 
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
	rank INTEGER, 
	PRIMARY KEY (name), 
	FOREIGN KEY(is_a) REFERENCES definition (name)
);
CREATE TABLE match_query (
	id INTEGER, 
	identifier_pattern TEXT, 
	source_ontology TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE reachability_query (
	id INTEGER, 
	source_ontology TEXT, 
	is_direct BOOLEAN, 
	include_self BOOLEAN, 
	traverse_up BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE TABLE expression (
	id INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE anonymous_expression (
	id INTEGER, 
	description TEXT, 
	title TEXT, 
	deprecated TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	rank INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE path_expression (
	id INTEGER, 
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
	rank INTEGER, 
	followed_by_id TEXT, 
	range_expression_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(traverse) REFERENCES slot_definition (name), 
	FOREIGN KEY(followed_by_id) REFERENCES path_expression (id), 
	FOREIGN KEY(range_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE slot_definition (
	singular_name TEXT, 
	domain TEXT, 
	slot_uri TEXT, 
	multivalued BOOLEAN, 
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
	inlined BOOLEAN, 
	inlined_as_list BOOLEAN, 
	minimum_value INTEGER, 
	maximum_value INTEGER, 
	pattern TEXT, 
	implicit_prefix TEXT, 
	equals_string TEXT, 
	equals_number INTEGER, 
	equals_expression TEXT, 
	minimum_cardinality INTEGER, 
	maximum_cardinality INTEGER, 
	is_a TEXT, 
	abstract BOOLEAN, 
	mixin BOOLEAN, 
	created_by TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	string_serialization TEXT, 
	name TEXT, 
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
	rank INTEGER, 
	schema_definition_name TEXT, 
	slot_expression_id TEXT, 
	anonymous_slot_expression_id TEXT, 
	slot_definition_name TEXT, 
	class_expression_id TEXT, 
	anonymous_class_expression_id TEXT, 
	class_definition_name TEXT, 
	path_rule_id TEXT, 
	range_expression_id TEXT, 
	enum_range_id TEXT, 
	structured_pattern_id TEXT, 
	unit_id TEXT, 
	has_member_id TEXT, 
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
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(class_expression_id) REFERENCES class_expression (id), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(path_rule_id) REFERENCES path_expression (id), 
	FOREIGN KEY(range_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(enum_range_id) REFERENCES enum_expression (id), 
	FOREIGN KEY(structured_pattern_id) REFERENCES pattern_expression (id), 
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id), 
	FOREIGN KEY(has_member_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE class_expression (
	id INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE class_level_rule (
	id INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE pattern_expression (
	id INTEGER, 
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
	rank INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE import_expression (
	id INTEGER, 
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
	rank INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE "UnitOfMeasure" (
	id INTEGER, 
	symbol TEXT, 
	ucum_code TEXT, 
	derivation TEXT, 
	has_quantity_kind TEXT, 
	iec61360code TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE annotatable (
	id INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE extensible (
	id INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE type_expression (
	id INTEGER, 
	pattern TEXT, 
	implicit_prefix TEXT, 
	equals_string TEXT, 
	equals_number INTEGER, 
	minimum_value INTEGER, 
	maximum_value INTEGER, 
	structured_pattern_id TEXT, 
	unit_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(structured_pattern_id) REFERENCES pattern_expression (id), 
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id)
);
CREATE TABLE anonymous_type_expression (
	id INTEGER, 
	pattern TEXT, 
	implicit_prefix TEXT, 
	equals_string TEXT, 
	equals_number INTEGER, 
	minimum_value INTEGER, 
	maximum_value INTEGER, 
	structured_pattern_id TEXT, 
	unit_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(structured_pattern_id) REFERENCES pattern_expression (id), 
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id)
);
CREATE TABLE subset_definition (
	name TEXT, 
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
	rank INTEGER, 
	schema_definition_name TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE enum_expression (
	id INTEGER, 
	code_set TEXT, 
	code_set_tag TEXT, 
	code_set_version TEXT, 
	pv_formula VARCHAR(11), 
	reachable_from_id TEXT, 
	matches_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(reachable_from_id) REFERENCES reachability_query (id), 
	FOREIGN KEY(matches_id) REFERENCES match_query (id)
);
CREATE TABLE anonymous_enum_expression (
	id INTEGER, 
	code_set TEXT, 
	code_set_tag TEXT, 
	code_set_version TEXT, 
	pv_formula VARCHAR(11), 
	reachable_from_id TEXT, 
	matches_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(reachable_from_id) REFERENCES reachability_query (id), 
	FOREIGN KEY(matches_id) REFERENCES match_query (id)
);
CREATE TABLE enum_definition (
	enum_uri TEXT, 
	code_set TEXT, 
	code_set_tag TEXT, 
	code_set_version TEXT, 
	pv_formula VARCHAR(11), 
	is_a TEXT, 
	abstract BOOLEAN, 
	mixin BOOLEAN, 
	created_by TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	string_serialization TEXT, 
	name TEXT, 
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
	rank INTEGER, 
	schema_definition_name TEXT, 
	reachable_from_id TEXT, 
	matches_id TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(is_a) REFERENCES definition (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(reachable_from_id) REFERENCES reachability_query (id), 
	FOREIGN KEY(matches_id) REFERENCES match_query (id)
);
CREATE TABLE class_definition (
	class_uri TEXT, 
	subclass_of TEXT, 
	tree_root BOOLEAN, 
	slot_names_unique BOOLEAN, 
	represents_relationship BOOLEAN, 
	children_are_mutually_disjoint BOOLEAN, 
	is_a TEXT, 
	abstract BOOLEAN, 
	mixin BOOLEAN, 
	created_by TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	string_serialization TEXT, 
	name TEXT, 
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
	rank INTEGER, 
	schema_definition_name TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(is_a) REFERENCES class_definition (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE setting (
	setting_key TEXT, 
	setting_value TEXT NOT NULL, 
	schema_definition_name TEXT, 
	import_expression_id TEXT, 
	PRIMARY KEY (setting_key, setting_value, schema_definition_name, import_expression_id), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE TABLE prefix (
	prefix_prefix TEXT, 
	prefix_reference TEXT NOT NULL, 
	schema_definition_name TEXT, 
	PRIMARY KEY (prefix_prefix, prefix_reference, schema_definition_name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE common_metadata_todos (
	common_metadata_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (common_metadata_id, todos), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE TABLE common_metadata_notes (
	common_metadata_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (common_metadata_id, notes), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE TABLE common_metadata_comments (
	common_metadata_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (common_metadata_id, comments), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE TABLE common_metadata_see_also (
	common_metadata_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (common_metadata_id, see_also), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE TABLE common_metadata_aliases (
	common_metadata_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (common_metadata_id, aliases), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE TABLE common_metadata_mappings (
	common_metadata_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (common_metadata_id, mappings), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE TABLE common_metadata_exact_mappings (
	common_metadata_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (common_metadata_id, exact_mappings), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE TABLE common_metadata_close_mappings (
	common_metadata_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (common_metadata_id, close_mappings), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE TABLE common_metadata_related_mappings (
	common_metadata_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (common_metadata_id, related_mappings), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE TABLE common_metadata_narrow_mappings (
	common_metadata_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (common_metadata_id, narrow_mappings), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE TABLE common_metadata_broad_mappings (
	common_metadata_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (common_metadata_id, broad_mappings), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id)
);
CREATE TABLE element_id_prefixes (
	element_name TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (element_name, id_prefixes), 
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE TABLE element_todos (
	element_name TEXT, 
	todos TEXT, 
	PRIMARY KEY (element_name, todos), 
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE TABLE element_notes (
	element_name TEXT, 
	notes TEXT, 
	PRIMARY KEY (element_name, notes), 
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE TABLE element_comments (
	element_name TEXT, 
	comments TEXT, 
	PRIMARY KEY (element_name, comments), 
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE TABLE element_see_also (
	element_name TEXT, 
	see_also TEXT, 
	PRIMARY KEY (element_name, see_also), 
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE TABLE element_aliases (
	element_name TEXT, 
	aliases TEXT, 
	PRIMARY KEY (element_name, aliases), 
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE TABLE element_mappings (
	element_name TEXT, 
	mappings TEXT, 
	PRIMARY KEY (element_name, mappings), 
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE TABLE element_exact_mappings (
	element_name TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (element_name, exact_mappings), 
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE TABLE element_close_mappings (
	element_name TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (element_name, close_mappings), 
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE TABLE element_related_mappings (
	element_name TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (element_name, related_mappings), 
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE TABLE element_narrow_mappings (
	element_name TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (element_name, narrow_mappings), 
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE TABLE element_broad_mappings (
	element_name TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (element_name, broad_mappings), 
	FOREIGN KEY(element_name) REFERENCES element (name)
);
CREATE TABLE schema_definition_imports (
	schema_definition_name TEXT, 
	imports TEXT, 
	PRIMARY KEY (schema_definition_name, imports), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_emit_prefixes (
	schema_definition_name TEXT, 
	emit_prefixes TEXT, 
	PRIMARY KEY (schema_definition_name, emit_prefixes), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_default_curi_maps (
	schema_definition_name TEXT, 
	default_curi_maps TEXT, 
	PRIMARY KEY (schema_definition_name, default_curi_maps), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_category (
	schema_definition_name TEXT, 
	category TEXT, 
	PRIMARY KEY (schema_definition_name, category), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_keyword (
	schema_definition_name TEXT, 
	keyword TEXT, 
	PRIMARY KEY (schema_definition_name, keyword), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_id_prefixes (
	schema_definition_name TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (schema_definition_name, id_prefixes), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_todos (
	schema_definition_name TEXT, 
	todos TEXT, 
	PRIMARY KEY (schema_definition_name, todos), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_notes (
	schema_definition_name TEXT, 
	notes TEXT, 
	PRIMARY KEY (schema_definition_name, notes), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_comments (
	schema_definition_name TEXT, 
	comments TEXT, 
	PRIMARY KEY (schema_definition_name, comments), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_see_also (
	schema_definition_name TEXT, 
	see_also TEXT, 
	PRIMARY KEY (schema_definition_name, see_also), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_aliases (
	schema_definition_name TEXT, 
	aliases TEXT, 
	PRIMARY KEY (schema_definition_name, aliases), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_mappings (
	schema_definition_name TEXT, 
	mappings TEXT, 
	PRIMARY KEY (schema_definition_name, mappings), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_exact_mappings (
	schema_definition_name TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (schema_definition_name, exact_mappings), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_close_mappings (
	schema_definition_name TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (schema_definition_name, close_mappings), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_related_mappings (
	schema_definition_name TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (schema_definition_name, related_mappings), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_narrow_mappings (
	schema_definition_name TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (schema_definition_name, narrow_mappings), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE schema_definition_broad_mappings (
	schema_definition_name TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (schema_definition_name, broad_mappings), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE type_definition_union_of (
	type_definition_name TEXT, 
	union_of TEXT, 
	PRIMARY KEY (type_definition_name, union_of), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(union_of) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_equals_string_in (
	type_definition_name TEXT, 
	equals_string_in TEXT, 
	PRIMARY KEY (type_definition_name, equals_string_in), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_id_prefixes (
	type_definition_name TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (type_definition_name, id_prefixes), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_todos (
	type_definition_name TEXT, 
	todos TEXT, 
	PRIMARY KEY (type_definition_name, todos), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_notes (
	type_definition_name TEXT, 
	notes TEXT, 
	PRIMARY KEY (type_definition_name, notes), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_comments (
	type_definition_name TEXT, 
	comments TEXT, 
	PRIMARY KEY (type_definition_name, comments), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_see_also (
	type_definition_name TEXT, 
	see_also TEXT, 
	PRIMARY KEY (type_definition_name, see_also), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_aliases (
	type_definition_name TEXT, 
	aliases TEXT, 
	PRIMARY KEY (type_definition_name, aliases), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_mappings (
	type_definition_name TEXT, 
	mappings TEXT, 
	PRIMARY KEY (type_definition_name, mappings), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_exact_mappings (
	type_definition_name TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (type_definition_name, exact_mappings), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_close_mappings (
	type_definition_name TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (type_definition_name, close_mappings), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_related_mappings (
	type_definition_name TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (type_definition_name, related_mappings), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_narrow_mappings (
	type_definition_name TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (type_definition_name, narrow_mappings), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE type_definition_broad_mappings (
	type_definition_name TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (type_definition_name, broad_mappings), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
);
CREATE TABLE definition_mixins (
	definition_name TEXT, 
	mixins TEXT, 
	PRIMARY KEY (definition_name, mixins), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(mixins) REFERENCES definition (name)
);
CREATE TABLE definition_apply_to (
	definition_name TEXT, 
	apply_to TEXT, 
	PRIMARY KEY (definition_name, apply_to), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(apply_to) REFERENCES definition (name)
);
CREATE TABLE definition_values_from (
	definition_name TEXT, 
	values_from TEXT, 
	PRIMARY KEY (definition_name, values_from), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE definition_id_prefixes (
	definition_name TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (definition_name, id_prefixes), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE definition_todos (
	definition_name TEXT, 
	todos TEXT, 
	PRIMARY KEY (definition_name, todos), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE definition_notes (
	definition_name TEXT, 
	notes TEXT, 
	PRIMARY KEY (definition_name, notes), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE definition_comments (
	definition_name TEXT, 
	comments TEXT, 
	PRIMARY KEY (definition_name, comments), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE definition_see_also (
	definition_name TEXT, 
	see_also TEXT, 
	PRIMARY KEY (definition_name, see_also), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE definition_aliases (
	definition_name TEXT, 
	aliases TEXT, 
	PRIMARY KEY (definition_name, aliases), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE definition_mappings (
	definition_name TEXT, 
	mappings TEXT, 
	PRIMARY KEY (definition_name, mappings), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE definition_exact_mappings (
	definition_name TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (definition_name, exact_mappings), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE definition_close_mappings (
	definition_name TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (definition_name, close_mappings), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE definition_related_mappings (
	definition_name TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (definition_name, related_mappings), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE definition_narrow_mappings (
	definition_name TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (definition_name, narrow_mappings), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE definition_broad_mappings (
	definition_name TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (definition_name, broad_mappings), 
	FOREIGN KEY(definition_name) REFERENCES definition (name)
);
CREATE TABLE reachability_query_source_nodes (
	reachability_query_id TEXT, 
	source_nodes TEXT, 
	PRIMARY KEY (reachability_query_id, source_nodes), 
	FOREIGN KEY(reachability_query_id) REFERENCES reachability_query (id)
);
CREATE TABLE reachability_query_relationship_types (
	reachability_query_id TEXT, 
	relationship_types TEXT, 
	PRIMARY KEY (reachability_query_id, relationship_types), 
	FOREIGN KEY(reachability_query_id) REFERENCES reachability_query (id)
);
CREATE TABLE anonymous_expression_todos (
	anonymous_expression_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (anonymous_expression_id, todos), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE TABLE anonymous_expression_notes (
	anonymous_expression_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (anonymous_expression_id, notes), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE TABLE anonymous_expression_comments (
	anonymous_expression_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (anonymous_expression_id, comments), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE TABLE anonymous_expression_see_also (
	anonymous_expression_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (anonymous_expression_id, see_also), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE TABLE anonymous_expression_aliases (
	anonymous_expression_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (anonymous_expression_id, aliases), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE TABLE anonymous_expression_mappings (
	anonymous_expression_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (anonymous_expression_id, mappings), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE TABLE anonymous_expression_exact_mappings (
	anonymous_expression_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (anonymous_expression_id, exact_mappings), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE TABLE anonymous_expression_close_mappings (
	anonymous_expression_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (anonymous_expression_id, close_mappings), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE TABLE anonymous_expression_related_mappings (
	anonymous_expression_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (anonymous_expression_id, related_mappings), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE TABLE anonymous_expression_narrow_mappings (
	anonymous_expression_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (anonymous_expression_id, narrow_mappings), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE TABLE anonymous_expression_broad_mappings (
	anonymous_expression_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (anonymous_expression_id, broad_mappings), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id)
);
CREATE TABLE path_expression_none_of (
	path_expression_id TEXT, 
	none_of_id TEXT, 
	PRIMARY KEY (path_expression_id, none_of_id), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id), 
	FOREIGN KEY(none_of_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_any_of (
	path_expression_id TEXT, 
	any_of_id TEXT, 
	PRIMARY KEY (path_expression_id, any_of_id), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id), 
	FOREIGN KEY(any_of_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_all_of (
	path_expression_id TEXT, 
	all_of_id TEXT, 
	PRIMARY KEY (path_expression_id, all_of_id), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id), 
	FOREIGN KEY(all_of_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_exactly_one_of (
	path_expression_id TEXT, 
	exactly_one_of_id TEXT, 
	PRIMARY KEY (path_expression_id, exactly_one_of_id), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id), 
	FOREIGN KEY(exactly_one_of_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_todos (
	path_expression_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (path_expression_id, todos), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_notes (
	path_expression_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (path_expression_id, notes), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_comments (
	path_expression_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (path_expression_id, comments), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_see_also (
	path_expression_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (path_expression_id, see_also), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_aliases (
	path_expression_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (path_expression_id, aliases), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_mappings (
	path_expression_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (path_expression_id, mappings), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_exact_mappings (
	path_expression_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (path_expression_id, exact_mappings), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_close_mappings (
	path_expression_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (path_expression_id, close_mappings), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_related_mappings (
	path_expression_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (path_expression_id, related_mappings), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_narrow_mappings (
	path_expression_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (path_expression_id, narrow_mappings), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE TABLE path_expression_broad_mappings (
	path_expression_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (path_expression_id, broad_mappings), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id)
);
CREATE TABLE slot_definition_disjoint_with (
	slot_definition_name TEXT, 
	disjoint_with TEXT, 
	PRIMARY KEY (slot_definition_name, disjoint_with), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(disjoint_with) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_union_of (
	slot_definition_name TEXT, 
	union_of TEXT, 
	PRIMARY KEY (slot_definition_name, union_of), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(union_of) REFERENCES type_definition (name)
);
CREATE TABLE slot_definition_equals_string_in (
	slot_definition_name TEXT, 
	equals_string_in TEXT, 
	PRIMARY KEY (slot_definition_name, equals_string_in), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_mixins (
	slot_definition_name TEXT, 
	mixins TEXT, 
	PRIMARY KEY (slot_definition_name, mixins), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(mixins) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_apply_to (
	slot_definition_name TEXT, 
	apply_to TEXT, 
	PRIMARY KEY (slot_definition_name, apply_to), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(apply_to) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_values_from (
	slot_definition_name TEXT, 
	values_from TEXT, 
	PRIMARY KEY (slot_definition_name, values_from), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_id_prefixes (
	slot_definition_name TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (slot_definition_name, id_prefixes), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_todos (
	slot_definition_name TEXT, 
	todos TEXT, 
	PRIMARY KEY (slot_definition_name, todos), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_notes (
	slot_definition_name TEXT, 
	notes TEXT, 
	PRIMARY KEY (slot_definition_name, notes), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_comments (
	slot_definition_name TEXT, 
	comments TEXT, 
	PRIMARY KEY (slot_definition_name, comments), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_see_also (
	slot_definition_name TEXT, 
	see_also TEXT, 
	PRIMARY KEY (slot_definition_name, see_also), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_aliases (
	slot_definition_name TEXT, 
	aliases TEXT, 
	PRIMARY KEY (slot_definition_name, aliases), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_mappings (
	slot_definition_name TEXT, 
	mappings TEXT, 
	PRIMARY KEY (slot_definition_name, mappings), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_exact_mappings (
	slot_definition_name TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (slot_definition_name, exact_mappings), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_close_mappings (
	slot_definition_name TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (slot_definition_name, close_mappings), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_related_mappings (
	slot_definition_name TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (slot_definition_name, related_mappings), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_narrow_mappings (
	slot_definition_name TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (slot_definition_name, narrow_mappings), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE slot_definition_broad_mappings (
	slot_definition_name TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (slot_definition_name, broad_mappings), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE pattern_expression_todos (
	pattern_expression_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (pattern_expression_id, todos), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE TABLE pattern_expression_notes (
	pattern_expression_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (pattern_expression_id, notes), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE TABLE pattern_expression_comments (
	pattern_expression_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (pattern_expression_id, comments), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE TABLE pattern_expression_see_also (
	pattern_expression_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (pattern_expression_id, see_also), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE TABLE pattern_expression_aliases (
	pattern_expression_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (pattern_expression_id, aliases), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE TABLE pattern_expression_mappings (
	pattern_expression_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (pattern_expression_id, mappings), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE TABLE pattern_expression_exact_mappings (
	pattern_expression_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (pattern_expression_id, exact_mappings), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE TABLE pattern_expression_close_mappings (
	pattern_expression_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (pattern_expression_id, close_mappings), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE TABLE pattern_expression_related_mappings (
	pattern_expression_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (pattern_expression_id, related_mappings), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE TABLE pattern_expression_narrow_mappings (
	pattern_expression_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (pattern_expression_id, narrow_mappings), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE TABLE pattern_expression_broad_mappings (
	pattern_expression_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (pattern_expression_id, broad_mappings), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id)
);
CREATE TABLE import_expression_todos (
	import_expression_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (import_expression_id, todos), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE TABLE import_expression_notes (
	import_expression_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (import_expression_id, notes), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE TABLE import_expression_comments (
	import_expression_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (import_expression_id, comments), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE TABLE import_expression_see_also (
	import_expression_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (import_expression_id, see_also), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE TABLE import_expression_aliases (
	import_expression_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (import_expression_id, aliases), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE TABLE import_expression_mappings (
	import_expression_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (import_expression_id, mappings), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE TABLE import_expression_exact_mappings (
	import_expression_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (import_expression_id, exact_mappings), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE TABLE import_expression_close_mappings (
	import_expression_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (import_expression_id, close_mappings), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE TABLE import_expression_related_mappings (
	import_expression_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (import_expression_id, related_mappings), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE TABLE import_expression_narrow_mappings (
	import_expression_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (import_expression_id, narrow_mappings), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE TABLE import_expression_broad_mappings (
	import_expression_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (import_expression_id, broad_mappings), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id)
);
CREATE TABLE "UnitOfMeasure_exact_mappings" (
	"UnitOfMeasure_id" TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY ("UnitOfMeasure_id", exact_mappings), 
	FOREIGN KEY("UnitOfMeasure_id") REFERENCES "UnitOfMeasure" (id)
);
CREATE TABLE anonymous_class_expression (
	id INTEGER, 
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
	rank INTEGER, 
	class_definition_name TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(is_a) REFERENCES definition (name), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE local_name (
	local_name_source TEXT, 
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
	FOREIGN KEY(element_name) REFERENCES element (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE permissible_value (
	text TEXT, 
	description TEXT, 
	meaning TEXT, 
	title TEXT, 
	deprecated TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	rank INTEGER, 
	enum_expression_id TEXT, 
	anonymous_enum_expression_id TEXT, 
	enum_definition_name TEXT, 
	unit_id TEXT, 
	PRIMARY KEY (text), 
	FOREIGN KEY(enum_expression_id) REFERENCES enum_expression (id), 
	FOREIGN KEY(anonymous_enum_expression_id) REFERENCES anonymous_enum_expression (id), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id)
);
CREATE TABLE unique_key (
	unique_key_name TEXT NOT NULL, 
	description TEXT, 
	title TEXT, 
	deprecated TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	rank INTEGER, 
	class_definition_name TEXT, 
	PRIMARY KEY (unique_key_name, description, title, deprecated, from_schema, imported_from, source, in_language, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, rank, class_definition_name), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE common_metadata_in_subset (
	common_metadata_id TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (common_metadata_id, in_subset), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE element_in_subset (
	element_name TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (element_name, in_subset), 
	FOREIGN KEY(element_name) REFERENCES element (name), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE schema_definition_in_subset (
	schema_definition_name TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (schema_definition_name, in_subset), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE type_expression_equals_string_in (
	type_expression_id TEXT, 
	equals_string_in TEXT, 
	PRIMARY KEY (type_expression_id, equals_string_in), 
	FOREIGN KEY(type_expression_id) REFERENCES type_expression (id)
);
CREATE TABLE type_expression_none_of (
	type_expression_id TEXT, 
	none_of_id TEXT, 
	PRIMARY KEY (type_expression_id, none_of_id), 
	FOREIGN KEY(type_expression_id) REFERENCES type_expression (id), 
	FOREIGN KEY(none_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE type_expression_exactly_one_of (
	type_expression_id TEXT, 
	exactly_one_of_id TEXT, 
	PRIMARY KEY (type_expression_id, exactly_one_of_id), 
	FOREIGN KEY(type_expression_id) REFERENCES type_expression (id), 
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE type_expression_any_of (
	type_expression_id TEXT, 
	any_of_id TEXT, 
	PRIMARY KEY (type_expression_id, any_of_id), 
	FOREIGN KEY(type_expression_id) REFERENCES type_expression (id), 
	FOREIGN KEY(any_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE type_expression_all_of (
	type_expression_id TEXT, 
	all_of_id TEXT, 
	PRIMARY KEY (type_expression_id, all_of_id), 
	FOREIGN KEY(type_expression_id) REFERENCES type_expression (id), 
	FOREIGN KEY(all_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE anonymous_type_expression_equals_string_in (
	anonymous_type_expression_id TEXT, 
	equals_string_in TEXT, 
	PRIMARY KEY (anonymous_type_expression_id, equals_string_in), 
	FOREIGN KEY(anonymous_type_expression_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE anonymous_type_expression_none_of (
	anonymous_type_expression_id TEXT, 
	none_of_id TEXT, 
	PRIMARY KEY (anonymous_type_expression_id, none_of_id), 
	FOREIGN KEY(anonymous_type_expression_id) REFERENCES anonymous_type_expression (id), 
	FOREIGN KEY(none_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE anonymous_type_expression_exactly_one_of (
	anonymous_type_expression_id TEXT, 
	exactly_one_of_id TEXT, 
	PRIMARY KEY (anonymous_type_expression_id, exactly_one_of_id), 
	FOREIGN KEY(anonymous_type_expression_id) REFERENCES anonymous_type_expression (id), 
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE anonymous_type_expression_any_of (
	anonymous_type_expression_id TEXT, 
	any_of_id TEXT, 
	PRIMARY KEY (anonymous_type_expression_id, any_of_id), 
	FOREIGN KEY(anonymous_type_expression_id) REFERENCES anonymous_type_expression (id), 
	FOREIGN KEY(any_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE anonymous_type_expression_all_of (
	anonymous_type_expression_id TEXT, 
	all_of_id TEXT, 
	PRIMARY KEY (anonymous_type_expression_id, all_of_id), 
	FOREIGN KEY(anonymous_type_expression_id) REFERENCES anonymous_type_expression (id), 
	FOREIGN KEY(all_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE type_definition_none_of (
	type_definition_name TEXT, 
	none_of_id TEXT, 
	PRIMARY KEY (type_definition_name, none_of_id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(none_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE type_definition_exactly_one_of (
	type_definition_name TEXT, 
	exactly_one_of_id TEXT, 
	PRIMARY KEY (type_definition_name, exactly_one_of_id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE type_definition_any_of (
	type_definition_name TEXT, 
	any_of_id TEXT, 
	PRIMARY KEY (type_definition_name, any_of_id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(any_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE type_definition_all_of (
	type_definition_name TEXT, 
	all_of_id TEXT, 
	PRIMARY KEY (type_definition_name, all_of_id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(all_of_id) REFERENCES anonymous_type_expression (id)
);
CREATE TABLE type_definition_in_subset (
	type_definition_name TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (type_definition_name, in_subset), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_id_prefixes (
	subset_definition_name TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (subset_definition_name, id_prefixes), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_todos (
	subset_definition_name TEXT, 
	todos TEXT, 
	PRIMARY KEY (subset_definition_name, todos), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_notes (
	subset_definition_name TEXT, 
	notes TEXT, 
	PRIMARY KEY (subset_definition_name, notes), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_comments (
	subset_definition_name TEXT, 
	comments TEXT, 
	PRIMARY KEY (subset_definition_name, comments), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_in_subset (
	subset_definition_name TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (subset_definition_name, in_subset), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_see_also (
	subset_definition_name TEXT, 
	see_also TEXT, 
	PRIMARY KEY (subset_definition_name, see_also), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_aliases (
	subset_definition_name TEXT, 
	aliases TEXT, 
	PRIMARY KEY (subset_definition_name, aliases), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_mappings (
	subset_definition_name TEXT, 
	mappings TEXT, 
	PRIMARY KEY (subset_definition_name, mappings), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_exact_mappings (
	subset_definition_name TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (subset_definition_name, exact_mappings), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_close_mappings (
	subset_definition_name TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (subset_definition_name, close_mappings), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_related_mappings (
	subset_definition_name TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (subset_definition_name, related_mappings), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_narrow_mappings (
	subset_definition_name TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (subset_definition_name, narrow_mappings), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE TABLE subset_definition_broad_mappings (
	subset_definition_name TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (subset_definition_name, broad_mappings), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name)
);
CREATE TABLE definition_in_subset (
	definition_name TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (definition_name, in_subset), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE enum_expression_include (
	enum_expression_id TEXT, 
	include_id TEXT, 
	PRIMARY KEY (enum_expression_id, include_id), 
	FOREIGN KEY(enum_expression_id) REFERENCES enum_expression (id), 
	FOREIGN KEY(include_id) REFERENCES anonymous_enum_expression (id)
);
CREATE TABLE enum_expression_minus (
	enum_expression_id TEXT, 
	minus_id TEXT, 
	PRIMARY KEY (enum_expression_id, minus_id), 
	FOREIGN KEY(enum_expression_id) REFERENCES enum_expression (id), 
	FOREIGN KEY(minus_id) REFERENCES anonymous_enum_expression (id)
);
CREATE TABLE enum_expression_inherits (
	enum_expression_id TEXT, 
	inherits TEXT, 
	PRIMARY KEY (enum_expression_id, inherits), 
	FOREIGN KEY(enum_expression_id) REFERENCES enum_expression (id), 
	FOREIGN KEY(inherits) REFERENCES enum_definition (name)
);
CREATE TABLE enum_expression_concepts (
	enum_expression_id TEXT, 
	concepts TEXT, 
	PRIMARY KEY (enum_expression_id, concepts), 
	FOREIGN KEY(enum_expression_id) REFERENCES enum_expression (id)
);
CREATE TABLE anonymous_enum_expression_include (
	anonymous_enum_expression_id TEXT, 
	include_id TEXT, 
	PRIMARY KEY (anonymous_enum_expression_id, include_id), 
	FOREIGN KEY(anonymous_enum_expression_id) REFERENCES anonymous_enum_expression (id), 
	FOREIGN KEY(include_id) REFERENCES anonymous_enum_expression (id)
);
CREATE TABLE anonymous_enum_expression_minus (
	anonymous_enum_expression_id TEXT, 
	minus_id TEXT, 
	PRIMARY KEY (anonymous_enum_expression_id, minus_id), 
	FOREIGN KEY(anonymous_enum_expression_id) REFERENCES anonymous_enum_expression (id), 
	FOREIGN KEY(minus_id) REFERENCES anonymous_enum_expression (id)
);
CREATE TABLE anonymous_enum_expression_inherits (
	anonymous_enum_expression_id TEXT, 
	inherits TEXT, 
	PRIMARY KEY (anonymous_enum_expression_id, inherits), 
	FOREIGN KEY(anonymous_enum_expression_id) REFERENCES anonymous_enum_expression (id), 
	FOREIGN KEY(inherits) REFERENCES enum_definition (name)
);
CREATE TABLE anonymous_enum_expression_concepts (
	anonymous_enum_expression_id TEXT, 
	concepts TEXT, 
	PRIMARY KEY (anonymous_enum_expression_id, concepts), 
	FOREIGN KEY(anonymous_enum_expression_id) REFERENCES anonymous_enum_expression (id)
);
CREATE TABLE enum_definition_include (
	enum_definition_name TEXT, 
	include_id TEXT, 
	PRIMARY KEY (enum_definition_name, include_id), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(include_id) REFERENCES anonymous_enum_expression (id)
);
CREATE TABLE enum_definition_minus (
	enum_definition_name TEXT, 
	minus_id TEXT, 
	PRIMARY KEY (enum_definition_name, minus_id), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(minus_id) REFERENCES anonymous_enum_expression (id)
);
CREATE TABLE enum_definition_inherits (
	enum_definition_name TEXT, 
	inherits TEXT, 
	PRIMARY KEY (enum_definition_name, inherits), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(inherits) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_concepts (
	enum_definition_name TEXT, 
	concepts TEXT, 
	PRIMARY KEY (enum_definition_name, concepts), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_mixins (
	enum_definition_name TEXT, 
	mixins TEXT, 
	PRIMARY KEY (enum_definition_name, mixins), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(mixins) REFERENCES definition (name)
);
CREATE TABLE enum_definition_apply_to (
	enum_definition_name TEXT, 
	apply_to TEXT, 
	PRIMARY KEY (enum_definition_name, apply_to), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(apply_to) REFERENCES definition (name)
);
CREATE TABLE enum_definition_values_from (
	enum_definition_name TEXT, 
	values_from TEXT, 
	PRIMARY KEY (enum_definition_name, values_from), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_id_prefixes (
	enum_definition_name TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (enum_definition_name, id_prefixes), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_todos (
	enum_definition_name TEXT, 
	todos TEXT, 
	PRIMARY KEY (enum_definition_name, todos), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_notes (
	enum_definition_name TEXT, 
	notes TEXT, 
	PRIMARY KEY (enum_definition_name, notes), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_comments (
	enum_definition_name TEXT, 
	comments TEXT, 
	PRIMARY KEY (enum_definition_name, comments), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_in_subset (
	enum_definition_name TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (enum_definition_name, in_subset), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE enum_definition_see_also (
	enum_definition_name TEXT, 
	see_also TEXT, 
	PRIMARY KEY (enum_definition_name, see_also), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_aliases (
	enum_definition_name TEXT, 
	aliases TEXT, 
	PRIMARY KEY (enum_definition_name, aliases), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_mappings (
	enum_definition_name TEXT, 
	mappings TEXT, 
	PRIMARY KEY (enum_definition_name, mappings), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_exact_mappings (
	enum_definition_name TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (enum_definition_name, exact_mappings), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_close_mappings (
	enum_definition_name TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (enum_definition_name, close_mappings), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_related_mappings (
	enum_definition_name TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (enum_definition_name, related_mappings), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_narrow_mappings (
	enum_definition_name TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (enum_definition_name, narrow_mappings), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE enum_definition_broad_mappings (
	enum_definition_name TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (enum_definition_name, broad_mappings), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE anonymous_expression_in_subset (
	anonymous_expression_id TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (anonymous_expression_id, in_subset), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE path_expression_in_subset (
	path_expression_id TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (path_expression_id, in_subset), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE slot_definition_domain_of (
	slot_definition_name TEXT, 
	domain_of TEXT, 
	PRIMARY KEY (slot_definition_name, domain_of), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(domain_of) REFERENCES class_definition (name)
);
CREATE TABLE slot_definition_in_subset (
	slot_definition_name TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (slot_definition_name, in_subset), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE class_definition_slots (
	class_definition_name TEXT, 
	slots TEXT, 
	PRIMARY KEY (class_definition_name, slots), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(slots) REFERENCES slot_definition (name)
);
CREATE TABLE class_definition_union_of (
	class_definition_name TEXT, 
	union_of TEXT, 
	PRIMARY KEY (class_definition_name, union_of), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(union_of) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_defining_slots (
	class_definition_name TEXT, 
	defining_slots TEXT, 
	PRIMARY KEY (class_definition_name, defining_slots), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(defining_slots) REFERENCES slot_definition (name)
);
CREATE TABLE class_definition_disjoint_with (
	class_definition_name TEXT, 
	disjoint_with TEXT, 
	PRIMARY KEY (class_definition_name, disjoint_with), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(disjoint_with) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_mixins (
	class_definition_name TEXT, 
	mixins TEXT, 
	PRIMARY KEY (class_definition_name, mixins), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(mixins) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_apply_to (
	class_definition_name TEXT, 
	apply_to TEXT, 
	PRIMARY KEY (class_definition_name, apply_to), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(apply_to) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_values_from (
	class_definition_name TEXT, 
	values_from TEXT, 
	PRIMARY KEY (class_definition_name, values_from), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_id_prefixes (
	class_definition_name TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (class_definition_name, id_prefixes), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_todos (
	class_definition_name TEXT, 
	todos TEXT, 
	PRIMARY KEY (class_definition_name, todos), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_notes (
	class_definition_name TEXT, 
	notes TEXT, 
	PRIMARY KEY (class_definition_name, notes), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_comments (
	class_definition_name TEXT, 
	comments TEXT, 
	PRIMARY KEY (class_definition_name, comments), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_in_subset (
	class_definition_name TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (class_definition_name, in_subset), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE class_definition_see_also (
	class_definition_name TEXT, 
	see_also TEXT, 
	PRIMARY KEY (class_definition_name, see_also), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_aliases (
	class_definition_name TEXT, 
	aliases TEXT, 
	PRIMARY KEY (class_definition_name, aliases), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_mappings (
	class_definition_name TEXT, 
	mappings TEXT, 
	PRIMARY KEY (class_definition_name, mappings), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_exact_mappings (
	class_definition_name TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (class_definition_name, exact_mappings), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_close_mappings (
	class_definition_name TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (class_definition_name, close_mappings), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_related_mappings (
	class_definition_name TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (class_definition_name, related_mappings), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_narrow_mappings (
	class_definition_name TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (class_definition_name, narrow_mappings), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE class_definition_broad_mappings (
	class_definition_name TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (class_definition_name, broad_mappings), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);
CREATE TABLE pattern_expression_in_subset (
	pattern_expression_id TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (pattern_expression_id, in_subset), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE import_expression_in_subset (
	import_expression_id TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (import_expression_id, in_subset), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE anonymous_slot_expression (
	id INTEGER, 
	range TEXT, 
	required BOOLEAN, 
	recommended BOOLEAN, 
	inlined BOOLEAN, 
	inlined_as_list BOOLEAN, 
	minimum_value INTEGER, 
	maximum_value INTEGER, 
	pattern TEXT, 
	implicit_prefix TEXT, 
	equals_string TEXT, 
	equals_number INTEGER, 
	equals_expression TEXT, 
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
	rank INTEGER, 
	range_expression_id TEXT, 
	enum_range_id TEXT, 
	structured_pattern_id TEXT, 
	unit_id TEXT, 
	has_member_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(range) REFERENCES element (name), 
	FOREIGN KEY(range_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(enum_range_id) REFERENCES enum_expression (id), 
	FOREIGN KEY(structured_pattern_id) REFERENCES pattern_expression (id), 
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id), 
	FOREIGN KEY(has_member_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE class_rule (
	id INTEGER, 
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
	class_definition_name TEXT, 
	preconditions_id TEXT, 
	postconditions_id TEXT, 
	elseconditions_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(preconditions_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(postconditions_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(elseconditions_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE class_expression_any_of (
	class_expression_id TEXT, 
	any_of_id TEXT, 
	PRIMARY KEY (class_expression_id, any_of_id), 
	FOREIGN KEY(class_expression_id) REFERENCES class_expression (id), 
	FOREIGN KEY(any_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE class_expression_exactly_one_of (
	class_expression_id TEXT, 
	exactly_one_of_id TEXT, 
	PRIMARY KEY (class_expression_id, exactly_one_of_id), 
	FOREIGN KEY(class_expression_id) REFERENCES class_expression (id), 
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE class_expression_none_of (
	class_expression_id TEXT, 
	none_of_id TEXT, 
	PRIMARY KEY (class_expression_id, none_of_id), 
	FOREIGN KEY(class_expression_id) REFERENCES class_expression (id), 
	FOREIGN KEY(none_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE class_expression_all_of (
	class_expression_id TEXT, 
	all_of_id TEXT, 
	PRIMARY KEY (class_expression_id, all_of_id), 
	FOREIGN KEY(class_expression_id) REFERENCES class_expression (id), 
	FOREIGN KEY(all_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_any_of (
	anonymous_class_expression_id TEXT, 
	any_of_id TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, any_of_id), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(any_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_exactly_one_of (
	anonymous_class_expression_id TEXT, 
	exactly_one_of_id TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, exactly_one_of_id), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_none_of (
	anonymous_class_expression_id TEXT, 
	none_of_id TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, none_of_id), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(none_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_all_of (
	anonymous_class_expression_id TEXT, 
	all_of_id TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, all_of_id), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(all_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_todos (
	anonymous_class_expression_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, todos), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_notes (
	anonymous_class_expression_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, notes), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_comments (
	anonymous_class_expression_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, comments), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_in_subset (
	anonymous_class_expression_id TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, in_subset), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE anonymous_class_expression_see_also (
	anonymous_class_expression_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, see_also), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_aliases (
	anonymous_class_expression_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, aliases), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_mappings (
	anonymous_class_expression_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, mappings), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_exact_mappings (
	anonymous_class_expression_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, exact_mappings), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_close_mappings (
	anonymous_class_expression_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, close_mappings), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_related_mappings (
	anonymous_class_expression_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, related_mappings), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_narrow_mappings (
	anonymous_class_expression_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, narrow_mappings), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE anonymous_class_expression_broad_mappings (
	anonymous_class_expression_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (anonymous_class_expression_id, broad_mappings), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE class_definition_any_of (
	class_definition_name TEXT, 
	any_of_id TEXT, 
	PRIMARY KEY (class_definition_name, any_of_id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(any_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE class_definition_exactly_one_of (
	class_definition_name TEXT, 
	exactly_one_of_id TEXT, 
	PRIMARY KEY (class_definition_name, exactly_one_of_id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE class_definition_none_of (
	class_definition_name TEXT, 
	none_of_id TEXT, 
	PRIMARY KEY (class_definition_name, none_of_id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(none_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE class_definition_all_of (
	class_definition_name TEXT, 
	all_of_id TEXT, 
	PRIMARY KEY (class_definition_name, all_of_id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(all_of_id) REFERENCES anonymous_class_expression (id)
);
CREATE TABLE permissible_value_todos (
	permissible_value_text TEXT, 
	todos TEXT, 
	PRIMARY KEY (permissible_value_text, todos), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE TABLE permissible_value_notes (
	permissible_value_text TEXT, 
	notes TEXT, 
	PRIMARY KEY (permissible_value_text, notes), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE TABLE permissible_value_comments (
	permissible_value_text TEXT, 
	comments TEXT, 
	PRIMARY KEY (permissible_value_text, comments), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE TABLE permissible_value_in_subset (
	permissible_value_text TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (permissible_value_text, in_subset), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE permissible_value_see_also (
	permissible_value_text TEXT, 
	see_also TEXT, 
	PRIMARY KEY (permissible_value_text, see_also), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE TABLE permissible_value_aliases (
	permissible_value_text TEXT, 
	aliases TEXT, 
	PRIMARY KEY (permissible_value_text, aliases), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE TABLE permissible_value_mappings (
	permissible_value_text TEXT, 
	mappings TEXT, 
	PRIMARY KEY (permissible_value_text, mappings), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE TABLE permissible_value_exact_mappings (
	permissible_value_text TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (permissible_value_text, exact_mappings), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE TABLE permissible_value_close_mappings (
	permissible_value_text TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (permissible_value_text, close_mappings), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE TABLE permissible_value_related_mappings (
	permissible_value_text TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (permissible_value_text, related_mappings), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE TABLE permissible_value_narrow_mappings (
	permissible_value_text TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (permissible_value_text, narrow_mappings), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE TABLE permissible_value_broad_mappings (
	permissible_value_text TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (permissible_value_text, broad_mappings), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text)
);
CREATE TABLE unique_key_unique_key_slots (
	unique_key_unique_key_name TEXT, 
	unique_key_slots TEXT NOT NULL, 
	PRIMARY KEY (unique_key_unique_key_name, unique_key_slots), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name), 
	FOREIGN KEY(unique_key_slots) REFERENCES slot_definition (name)
);
CREATE TABLE unique_key_todos (
	unique_key_unique_key_name TEXT, 
	todos TEXT, 
	PRIMARY KEY (unique_key_unique_key_name, todos), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE unique_key_notes (
	unique_key_unique_key_name TEXT, 
	notes TEXT, 
	PRIMARY KEY (unique_key_unique_key_name, notes), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE unique_key_comments (
	unique_key_unique_key_name TEXT, 
	comments TEXT, 
	PRIMARY KEY (unique_key_unique_key_name, comments), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE unique_key_in_subset (
	unique_key_unique_key_name TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (unique_key_unique_key_name, in_subset), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE unique_key_see_also (
	unique_key_unique_key_name TEXT, 
	see_also TEXT, 
	PRIMARY KEY (unique_key_unique_key_name, see_also), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE unique_key_aliases (
	unique_key_unique_key_name TEXT, 
	aliases TEXT, 
	PRIMARY KEY (unique_key_unique_key_name, aliases), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE unique_key_mappings (
	unique_key_unique_key_name TEXT, 
	mappings TEXT, 
	PRIMARY KEY (unique_key_unique_key_name, mappings), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE unique_key_exact_mappings (
	unique_key_unique_key_name TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (unique_key_unique_key_name, exact_mappings), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE unique_key_close_mappings (
	unique_key_unique_key_name TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (unique_key_unique_key_name, close_mappings), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE unique_key_related_mappings (
	unique_key_unique_key_name TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (unique_key_unique_key_name, related_mappings), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE unique_key_narrow_mappings (
	unique_key_unique_key_name TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (unique_key_unique_key_name, narrow_mappings), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE unique_key_broad_mappings (
	unique_key_unique_key_name TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (unique_key_unique_key_name, broad_mappings), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE structured_alias (
	id INTEGER, 
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
	rank INTEGER, 
	common_metadata_id TEXT, 
	element_name TEXT, 
	schema_definition_name TEXT, 
	type_definition_name TEXT, 
	subset_definition_name TEXT, 
	definition_name TEXT, 
	enum_definition_name TEXT, 
	structured_alias_id TEXT, 
	anonymous_expression_id TEXT, 
	path_expression_id TEXT, 
	anonymous_slot_expression_id TEXT, 
	slot_definition_name TEXT, 
	anonymous_class_expression_id TEXT, 
	class_definition_name TEXT, 
	class_rule_id TEXT, 
	pattern_expression_id TEXT, 
	import_expression_id TEXT, 
	permissible_value_text TEXT, 
	unique_key_unique_key_name TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id), 
	FOREIGN KEY(element_name) REFERENCES element (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE slot_expression (
	id INTEGER, 
	range TEXT, 
	required BOOLEAN, 
	recommended BOOLEAN, 
	inlined BOOLEAN, 
	inlined_as_list BOOLEAN, 
	minimum_value INTEGER, 
	maximum_value INTEGER, 
	pattern TEXT, 
	implicit_prefix TEXT, 
	equals_string TEXT, 
	equals_number INTEGER, 
	equals_expression TEXT, 
	minimum_cardinality INTEGER, 
	maximum_cardinality INTEGER, 
	range_expression_id TEXT, 
	enum_range_id TEXT, 
	structured_pattern_id TEXT, 
	unit_id TEXT, 
	has_member_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(range) REFERENCES element (name), 
	FOREIGN KEY(range_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(enum_range_id) REFERENCES enum_expression (id), 
	FOREIGN KEY(structured_pattern_id) REFERENCES pattern_expression (id), 
	FOREIGN KEY(unit_id) REFERENCES "UnitOfMeasure" (id), 
	FOREIGN KEY(has_member_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_equals_string_in (
	anonymous_slot_expression_id TEXT, 
	equals_string_in TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, equals_string_in), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_none_of (
	anonymous_slot_expression_id TEXT, 
	none_of_id TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, none_of_id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(none_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_exactly_one_of (
	anonymous_slot_expression_id TEXT, 
	exactly_one_of_id TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, exactly_one_of_id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_any_of (
	anonymous_slot_expression_id TEXT, 
	any_of_id TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, any_of_id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(any_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_all_of (
	anonymous_slot_expression_id TEXT, 
	all_of_id TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, all_of_id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(all_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_todos (
	anonymous_slot_expression_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, todos), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_notes (
	anonymous_slot_expression_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, notes), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_comments (
	anonymous_slot_expression_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, comments), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_in_subset (
	anonymous_slot_expression_id TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, in_subset), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE anonymous_slot_expression_see_also (
	anonymous_slot_expression_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, see_also), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_aliases (
	anonymous_slot_expression_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, aliases), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_mappings (
	anonymous_slot_expression_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, mappings), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_exact_mappings (
	anonymous_slot_expression_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, exact_mappings), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_close_mappings (
	anonymous_slot_expression_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, close_mappings), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_related_mappings (
	anonymous_slot_expression_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, related_mappings), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_narrow_mappings (
	anonymous_slot_expression_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, narrow_mappings), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE anonymous_slot_expression_broad_mappings (
	anonymous_slot_expression_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (anonymous_slot_expression_id, broad_mappings), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE slot_definition_none_of (
	slot_definition_name TEXT, 
	none_of_id TEXT, 
	PRIMARY KEY (slot_definition_name, none_of_id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(none_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE slot_definition_exactly_one_of (
	slot_definition_name TEXT, 
	exactly_one_of_id TEXT, 
	PRIMARY KEY (slot_definition_name, exactly_one_of_id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE slot_definition_any_of (
	slot_definition_name TEXT, 
	any_of_id TEXT, 
	PRIMARY KEY (slot_definition_name, any_of_id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(any_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE slot_definition_all_of (
	slot_definition_name TEXT, 
	all_of_id TEXT, 
	PRIMARY KEY (slot_definition_name, all_of_id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(all_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE class_rule_todos (
	class_rule_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (class_rule_id, todos), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE TABLE class_rule_notes (
	class_rule_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (class_rule_id, notes), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE TABLE class_rule_comments (
	class_rule_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (class_rule_id, comments), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE TABLE class_rule_in_subset (
	class_rule_id TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (class_rule_id, in_subset), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE class_rule_see_also (
	class_rule_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (class_rule_id, see_also), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE TABLE class_rule_aliases (
	class_rule_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (class_rule_id, aliases), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE TABLE class_rule_mappings (
	class_rule_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (class_rule_id, mappings), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE TABLE class_rule_exact_mappings (
	class_rule_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (class_rule_id, exact_mappings), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE TABLE class_rule_close_mappings (
	class_rule_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (class_rule_id, close_mappings), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE TABLE class_rule_related_mappings (
	class_rule_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (class_rule_id, related_mappings), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE TABLE class_rule_narrow_mappings (
	class_rule_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (class_rule_id, narrow_mappings), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE TABLE class_rule_broad_mappings (
	class_rule_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (class_rule_id, broad_mappings), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id)
);
CREATE TABLE example (
	id INTEGER, 
	value TEXT, 
	description TEXT, 
	common_metadata_id TEXT, 
	element_name TEXT, 
	schema_definition_name TEXT, 
	type_definition_name TEXT, 
	subset_definition_name TEXT, 
	definition_name TEXT, 
	enum_definition_name TEXT, 
	structured_alias_id TEXT, 
	anonymous_expression_id TEXT, 
	path_expression_id TEXT, 
	anonymous_slot_expression_id TEXT, 
	slot_definition_name TEXT, 
	anonymous_class_expression_id TEXT, 
	class_definition_name TEXT, 
	class_rule_id TEXT, 
	pattern_expression_id TEXT, 
	import_expression_id TEXT, 
	permissible_value_text TEXT, 
	unique_key_unique_key_name TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id), 
	FOREIGN KEY(element_name) REFERENCES element (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE alt_description (
	source TEXT, 
	description TEXT NOT NULL, 
	common_metadata_id TEXT, 
	element_name TEXT, 
	schema_definition_name TEXT, 
	type_definition_name TEXT, 
	subset_definition_name TEXT, 
	definition_name TEXT, 
	enum_definition_name TEXT, 
	structured_alias_id TEXT, 
	anonymous_expression_id TEXT, 
	path_expression_id TEXT, 
	anonymous_slot_expression_id TEXT, 
	slot_definition_name TEXT, 
	anonymous_class_expression_id TEXT, 
	class_definition_name TEXT, 
	class_rule_id TEXT, 
	pattern_expression_id TEXT, 
	import_expression_id TEXT, 
	permissible_value_text TEXT, 
	unique_key_unique_key_name TEXT, 
	PRIMARY KEY (source, description, common_metadata_id, element_name, schema_definition_name, type_definition_name, subset_definition_name, definition_name, enum_definition_name, structured_alias_id, anonymous_expression_id, path_expression_id, anonymous_slot_expression_id, slot_definition_name, anonymous_class_expression_id, class_definition_name, class_rule_id, pattern_expression_id, import_expression_id, permissible_value_text, unique_key_unique_key_name), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id), 
	FOREIGN KEY(element_name) REFERENCES element (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name)
);
CREATE TABLE annotation (
	tag TEXT NOT NULL, 
	value TEXT NOT NULL, 
	element_name TEXT, 
	schema_definition_name TEXT, 
	type_definition_name TEXT, 
	subset_definition_name TEXT, 
	definition_name TEXT, 
	enum_definition_name TEXT, 
	structured_alias_id TEXT, 
	anonymous_expression_id TEXT, 
	path_expression_id TEXT, 
	anonymous_slot_expression_id TEXT, 
	slot_definition_name TEXT, 
	anonymous_class_expression_id TEXT, 
	class_definition_name TEXT, 
	class_rule_id TEXT, 
	pattern_expression_id TEXT, 
	import_expression_id TEXT, 
	permissible_value_text TEXT, 
	unique_key_unique_key_name TEXT, 
	annotatable_id TEXT, 
	annotation_tag TEXT, 
	PRIMARY KEY (tag, value, element_name, schema_definition_name, type_definition_name, subset_definition_name, definition_name, enum_definition_name, structured_alias_id, anonymous_expression_id, path_expression_id, anonymous_slot_expression_id, slot_definition_name, anonymous_class_expression_id, class_definition_name, class_rule_id, pattern_expression_id, import_expression_id, permissible_value_text, unique_key_unique_key_name, annotatable_id, annotation_tag), 
	FOREIGN KEY(element_name) REFERENCES element (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name), 
	FOREIGN KEY(annotatable_id) REFERENCES annotatable (id), 
	FOREIGN KEY(annotation_tag) REFERENCES annotation (tag)
);
CREATE TABLE structured_alias_category (
	structured_alias_id TEXT, 
	category TEXT, 
	PRIMARY KEY (structured_alias_id, category), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE TABLE structured_alias_todos (
	structured_alias_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (structured_alias_id, todos), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE TABLE structured_alias_notes (
	structured_alias_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (structured_alias_id, notes), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE TABLE structured_alias_comments (
	structured_alias_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (structured_alias_id, comments), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE TABLE structured_alias_in_subset (
	structured_alias_id TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (structured_alias_id, in_subset), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE structured_alias_see_also (
	structured_alias_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (structured_alias_id, see_also), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE TABLE structured_alias_aliases (
	structured_alias_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (structured_alias_id, aliases), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE TABLE structured_alias_mappings (
	structured_alias_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (structured_alias_id, mappings), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE TABLE structured_alias_exact_mappings (
	structured_alias_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (structured_alias_id, exact_mappings), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE TABLE structured_alias_close_mappings (
	structured_alias_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (structured_alias_id, close_mappings), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE TABLE structured_alias_related_mappings (
	structured_alias_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (structured_alias_id, related_mappings), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE TABLE structured_alias_narrow_mappings (
	structured_alias_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (structured_alias_id, narrow_mappings), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE TABLE structured_alias_broad_mappings (
	structured_alias_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (structured_alias_id, broad_mappings), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id)
);
CREATE TABLE slot_expression_equals_string_in (
	slot_expression_id TEXT, 
	equals_string_in TEXT, 
	PRIMARY KEY (slot_expression_id, equals_string_in), 
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id)
);
CREATE TABLE slot_expression_none_of (
	slot_expression_id TEXT, 
	none_of_id TEXT, 
	PRIMARY KEY (slot_expression_id, none_of_id), 
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id), 
	FOREIGN KEY(none_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE slot_expression_exactly_one_of (
	slot_expression_id TEXT, 
	exactly_one_of_id TEXT, 
	PRIMARY KEY (slot_expression_id, exactly_one_of_id), 
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id), 
	FOREIGN KEY(exactly_one_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE slot_expression_any_of (
	slot_expression_id TEXT, 
	any_of_id TEXT, 
	PRIMARY KEY (slot_expression_id, any_of_id), 
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id), 
	FOREIGN KEY(any_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE slot_expression_all_of (
	slot_expression_id TEXT, 
	all_of_id TEXT, 
	PRIMARY KEY (slot_expression_id, all_of_id), 
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id), 
	FOREIGN KEY(all_of_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE extension (
	tag TEXT NOT NULL, 
	value TEXT NOT NULL, 
	element_name TEXT, 
	schema_definition_name TEXT, 
	type_definition_name TEXT, 
	subset_definition_name TEXT, 
	definition_name TEXT, 
	enum_definition_name TEXT, 
	structured_alias_id TEXT, 
	anonymous_expression_id TEXT, 
	path_expression_id TEXT, 
	anonymous_slot_expression_id TEXT, 
	slot_definition_name TEXT, 
	anonymous_class_expression_id TEXT, 
	class_definition_name TEXT, 
	class_rule_id TEXT, 
	pattern_expression_id TEXT, 
	import_expression_id TEXT, 
	permissible_value_text TEXT, 
	unique_key_unique_key_name TEXT, 
	annotation_tag TEXT, 
	extension_tag TEXT, 
	extensible_id TEXT, 
	PRIMARY KEY (tag, value, element_name, schema_definition_name, type_definition_name, subset_definition_name, definition_name, enum_definition_name, structured_alias_id, anonymous_expression_id, path_expression_id, anonymous_slot_expression_id, slot_definition_name, anonymous_class_expression_id, class_definition_name, class_rule_id, pattern_expression_id, import_expression_id, permissible_value_text, unique_key_unique_key_name, annotation_tag, extension_tag, extensible_id), 
	FOREIGN KEY(element_name) REFERENCES element (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(structured_alias_id) REFERENCES structured_alias (id), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id), 
	FOREIGN KEY(path_expression_id) REFERENCES path_expression (id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id), 
	FOREIGN KEY(pattern_expression_id) REFERENCES pattern_expression (id), 
	FOREIGN KEY(import_expression_id) REFERENCES import_expression (id), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text), 
	FOREIGN KEY(unique_key_unique_key_name) REFERENCES unique_key (unique_key_name), 
	FOREIGN KEY(annotation_tag) REFERENCES annotation (tag), 
	FOREIGN KEY(extension_tag) REFERENCES extension (tag), 
	FOREIGN KEY(extensible_id) REFERENCES extensible (id)
);
