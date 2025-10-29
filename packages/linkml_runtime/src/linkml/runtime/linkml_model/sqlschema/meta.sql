

CREATE TABLE alt_description (
	source TEXT NOT NULL, 
	description TEXT NOT NULL, 
	PRIMARY KEY (source, description)
);

CREATE TABLE annotation (
	tag TEXT NOT NULL, 
	value TEXT NOT NULL, 
	extensions TEXT, 
	annotations TEXT, 
	PRIMARY KEY (tag, value, extensions, annotations)
);

CREATE TABLE anonymous_class_expression (
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	todos TEXT, 
	notes TEXT, 
	comments TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	see_also TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	aliases TEXT, 
	structured_aliases TEXT, 
	mappings TEXT, 
	exact_mappings TEXT, 
	close_mappings TEXT, 
	related_mappings TEXT, 
	narrow_mappings TEXT, 
	broad_mappings TEXT, 
	created_by TEXT, 
	contributors TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	categories TEXT, 
	keywords TEXT, 
	is_a TEXT, 
	any_of TEXT, 
	exactly_one_of TEXT, 
	none_of TEXT, 
	all_of TEXT, 
	slot_conditions TEXT, 
	PRIMARY KEY (extensions, annotations, description, alt_descriptions, title, deprecated, todos, notes, comments, examples, in_subset, from_schema, imported_from, source, in_language, see_also, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, aliases, structured_aliases, mappings, exact_mappings, close_mappings, related_mappings, narrow_mappings, broad_mappings, created_by, contributors, created_on, last_updated_on, modified_by, status, rank, categories, keywords, is_a, any_of, exactly_one_of, none_of, all_of, slot_conditions)
);

CREATE TABLE anonymous_enum_expression (
	code_set TEXT, 
	code_set_tag TEXT, 
	code_set_version TEXT, 
	pv_formula VARCHAR(11), 
	permissible_values TEXT, 
	include TEXT, 
	minus TEXT, 
	inherits TEXT, 
	reachable_from TEXT, 
	matches TEXT, 
	concepts TEXT, 
	PRIMARY KEY (code_set, code_set_tag, code_set_version, pv_formula, permissible_values, include, minus, inherits, reachable_from, matches, concepts)
);

CREATE TABLE anonymous_slot_expression (
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	todos TEXT, 
	notes TEXT, 
	comments TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	see_also TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	aliases TEXT, 
	structured_aliases TEXT, 
	mappings TEXT, 
	exact_mappings TEXT, 
	close_mappings TEXT, 
	related_mappings TEXT, 
	narrow_mappings TEXT, 
	broad_mappings TEXT, 
	created_by TEXT, 
	contributors TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	categories TEXT, 
	keywords TEXT, 
	range TEXT, 
	range_expression TEXT, 
	enum_range TEXT, 
	bindings TEXT, 
	required BOOLEAN, 
	recommended BOOLEAN, 
	multivalued BOOLEAN, 
	inlined BOOLEAN, 
	inlined_as_list BOOLEAN, 
	minimum_value TEXT, 
	maximum_value TEXT, 
	pattern TEXT, 
	structured_pattern TEXT, 
	unit TEXT, 
	implicit_prefix TEXT, 
	value_presence VARCHAR(11), 
	equals_string TEXT, 
	equals_string_in TEXT, 
	equals_number INTEGER, 
	equals_expression TEXT, 
	exact_cardinality INTEGER, 
	minimum_cardinality INTEGER, 
	maximum_cardinality INTEGER, 
	has_member TEXT, 
	all_members TEXT, 
	none_of TEXT, 
	exactly_one_of TEXT, 
	any_of TEXT, 
	all_of TEXT, 
	PRIMARY KEY (extensions, annotations, description, alt_descriptions, title, deprecated, todos, notes, comments, examples, in_subset, from_schema, imported_from, source, in_language, see_also, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, aliases, structured_aliases, mappings, exact_mappings, close_mappings, related_mappings, narrow_mappings, broad_mappings, created_by, contributors, created_on, last_updated_on, modified_by, status, rank, categories, keywords, range, range_expression, enum_range, bindings, required, recommended, multivalued, inlined, inlined_as_list, minimum_value, maximum_value, pattern, structured_pattern, unit, implicit_prefix, value_presence, equals_string, equals_string_in, equals_number, equals_expression, exact_cardinality, minimum_cardinality, maximum_cardinality, has_member, all_members, none_of, exactly_one_of, any_of, all_of)
);

CREATE TABLE anonymous_type_expression (
	pattern TEXT, 
	structured_pattern TEXT, 
	unit TEXT, 
	implicit_prefix TEXT, 
	equals_string TEXT, 
	equals_string_in TEXT, 
	equals_number INTEGER, 
	minimum_value TEXT, 
	maximum_value TEXT, 
	none_of TEXT, 
	exactly_one_of TEXT, 
	any_of TEXT, 
	all_of TEXT, 
	PRIMARY KEY (pattern, structured_pattern, unit, implicit_prefix, equals_string, equals_string_in, equals_number, minimum_value, maximum_value, none_of, exactly_one_of, any_of, all_of)
);

CREATE TABLE array_expression (
	exact_number_dimensions INTEGER, 
	minimum_number_dimensions INTEGER, 
	maximum_number_dimensions TEXT, 
	dimensions TEXT, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	todos TEXT, 
	notes TEXT, 
	comments TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	see_also TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	aliases TEXT, 
	structured_aliases TEXT, 
	mappings TEXT, 
	exact_mappings TEXT, 
	close_mappings TEXT, 
	related_mappings TEXT, 
	narrow_mappings TEXT, 
	broad_mappings TEXT, 
	created_by TEXT, 
	contributors TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	categories TEXT, 
	keywords TEXT, 
	PRIMARY KEY (exact_number_dimensions, minimum_number_dimensions, maximum_number_dimensions, dimensions, extensions, annotations, description, alt_descriptions, title, deprecated, todos, notes, comments, examples, in_subset, from_schema, imported_from, source, in_language, see_also, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, aliases, structured_aliases, mappings, exact_mappings, close_mappings, related_mappings, narrow_mappings, broad_mappings, created_by, contributors, created_on, last_updated_on, modified_by, status, rank, categories, keywords)
);

CREATE TABLE class_definition (
	name TEXT NOT NULL, 
	id_prefixes_are_closed BOOLEAN, 
	definition_uri TEXT, 
	local_names TEXT, 
	conforms_to TEXT, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	structured_aliases TEXT, 
	created_by TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	abstract BOOLEAN, 
	mixin BOOLEAN, 
	string_serialization TEXT, 
	slots TEXT, 
	slot_usage TEXT, 
	attributes TEXT, 
	class_uri TEXT, 
	subclass_of TEXT, 
	union_of TEXT, 
	defining_slots TEXT, 
	tree_root BOOLEAN, 
	classification_rules TEXT, 
	slot_names_unique BOOLEAN, 
	represents_relationship BOOLEAN, 
	disjoint_with TEXT, 
	children_are_mutually_disjoint BOOLEAN, 
	is_a TEXT, 
	mixins TEXT, 
	apply_to TEXT, 
	any_of TEXT, 
	exactly_one_of TEXT, 
	none_of TEXT, 
	all_of TEXT, 
	slot_conditions TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(is_a) REFERENCES class_definition (name)
);

CREATE TABLE dimension_expression (
	alias TEXT, 
	maximum_cardinality INTEGER, 
	minimum_cardinality INTEGER, 
	exact_cardinality INTEGER, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	todos TEXT, 
	notes TEXT, 
	comments TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	see_also TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	aliases TEXT, 
	structured_aliases TEXT, 
	mappings TEXT, 
	exact_mappings TEXT, 
	close_mappings TEXT, 
	related_mappings TEXT, 
	narrow_mappings TEXT, 
	broad_mappings TEXT, 
	created_by TEXT, 
	contributors TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	categories TEXT, 
	keywords TEXT, 
	PRIMARY KEY (alias, maximum_cardinality, minimum_cardinality, exact_cardinality, extensions, annotations, description, alt_descriptions, title, deprecated, todos, notes, comments, examples, in_subset, from_schema, imported_from, source, in_language, see_also, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, aliases, structured_aliases, mappings, exact_mappings, close_mappings, related_mappings, narrow_mappings, broad_mappings, created_by, contributors, created_on, last_updated_on, modified_by, status, rank, categories, keywords)
);

CREATE TABLE enum_definition (
	name TEXT NOT NULL, 
	id_prefixes_are_closed BOOLEAN, 
	definition_uri TEXT, 
	local_names TEXT, 
	conforms_to TEXT, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	structured_aliases TEXT, 
	created_by TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	is_a TEXT, 
	abstract BOOLEAN, 
	mixin BOOLEAN, 
	string_serialization TEXT, 
	enum_uri TEXT, 
	code_set TEXT, 
	code_set_tag TEXT, 
	code_set_version TEXT, 
	pv_formula VARCHAR(11), 
	permissible_values TEXT, 
	include TEXT, 
	minus TEXT, 
	inherits TEXT, 
	reachable_from TEXT, 
	matches TEXT, 
	PRIMARY KEY (name)
);

CREATE TABLE enum_expression (
	code_set TEXT, 
	code_set_tag TEXT, 
	code_set_version TEXT, 
	pv_formula VARCHAR(11), 
	permissible_values TEXT, 
	include TEXT, 
	minus TEXT, 
	inherits TEXT, 
	reachable_from TEXT, 
	matches TEXT, 
	concepts TEXT, 
	PRIMARY KEY (code_set, code_set_tag, code_set_version, pv_formula, permissible_values, include, minus, inherits, reachable_from, matches, concepts)
);

CREATE TABLE example (
	value TEXT, 
	description TEXT, 
	object TEXT, 
	PRIMARY KEY (value, description, object)
);

CREATE TABLE extension (
	tag TEXT NOT NULL, 
	value TEXT NOT NULL, 
	extensions TEXT, 
	PRIMARY KEY (tag, value, extensions)
);

CREATE TABLE import_expression (
	import_from TEXT NOT NULL, 
	import_as TEXT, 
	import_map TEXT, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	todos TEXT, 
	notes TEXT, 
	comments TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	see_also TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	aliases TEXT, 
	structured_aliases TEXT, 
	mappings TEXT, 
	exact_mappings TEXT, 
	close_mappings TEXT, 
	related_mappings TEXT, 
	narrow_mappings TEXT, 
	broad_mappings TEXT, 
	created_by TEXT, 
	contributors TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	categories TEXT, 
	keywords TEXT, 
	PRIMARY KEY (import_from, import_as, import_map, extensions, annotations, description, alt_descriptions, title, deprecated, todos, notes, comments, examples, in_subset, from_schema, imported_from, source, in_language, see_also, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, aliases, structured_aliases, mappings, exact_mappings, close_mappings, related_mappings, narrow_mappings, broad_mappings, created_by, contributors, created_on, last_updated_on, modified_by, status, rank, categories, keywords)
);

CREATE TABLE local_name (
	local_name_source TEXT NOT NULL, 
	local_name_value TEXT NOT NULL, 
	PRIMARY KEY (local_name_source, local_name_value)
);

CREATE TABLE match_query (
	identifier_pattern TEXT, 
	source_ontology TEXT, 
	PRIMARY KEY (identifier_pattern, source_ontology)
);

CREATE TABLE pattern_expression (
	syntax TEXT, 
	interpolated BOOLEAN, 
	partial_match BOOLEAN, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	todos TEXT, 
	notes TEXT, 
	comments TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	see_also TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	aliases TEXT, 
	structured_aliases TEXT, 
	mappings TEXT, 
	exact_mappings TEXT, 
	close_mappings TEXT, 
	related_mappings TEXT, 
	narrow_mappings TEXT, 
	broad_mappings TEXT, 
	created_by TEXT, 
	contributors TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	categories TEXT, 
	keywords TEXT, 
	PRIMARY KEY (syntax, interpolated, partial_match, extensions, annotations, description, alt_descriptions, title, deprecated, todos, notes, comments, examples, in_subset, from_schema, imported_from, source, in_language, see_also, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, aliases, structured_aliases, mappings, exact_mappings, close_mappings, related_mappings, narrow_mappings, broad_mappings, created_by, contributors, created_on, last_updated_on, modified_by, status, rank, categories, keywords)
);

CREATE TABLE permissible_value (
	text TEXT NOT NULL, 
	description TEXT, 
	meaning TEXT, 
	unit TEXT, 
	is_a TEXT, 
	mixins TEXT, 
	extensions TEXT, 
	annotations TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	structured_aliases TEXT, 
	created_by TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	PRIMARY KEY (text), 
	FOREIGN KEY(is_a) REFERENCES permissible_value (text)
);

CREATE TABLE reachability_query (
	source_ontology TEXT, 
	source_nodes TEXT, 
	relationship_types TEXT, 
	is_direct BOOLEAN, 
	include_self BOOLEAN, 
	traverse_up BOOLEAN, 
	PRIMARY KEY (source_ontology, source_nodes, relationship_types, is_direct, include_self, traverse_up)
);

CREATE TABLE setting (
	setting_key TEXT NOT NULL, 
	setting_value TEXT NOT NULL, 
	PRIMARY KEY (setting_key, setting_value)
);

CREATE TABLE structured_alias (
	literal_form TEXT NOT NULL, 
	predicate VARCHAR(15), 
	categories TEXT, 
	contexts TEXT, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	todos TEXT, 
	notes TEXT, 
	comments TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	see_also TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	aliases TEXT, 
	structured_aliases TEXT, 
	mappings TEXT, 
	exact_mappings TEXT, 
	close_mappings TEXT, 
	related_mappings TEXT, 
	narrow_mappings TEXT, 
	broad_mappings TEXT, 
	created_by TEXT, 
	contributors TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	keywords TEXT, 
	PRIMARY KEY (literal_form, predicate, categories, contexts, extensions, annotations, description, alt_descriptions, title, deprecated, todos, notes, comments, examples, in_subset, from_schema, imported_from, source, in_language, see_also, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, aliases, structured_aliases, mappings, exact_mappings, close_mappings, related_mappings, narrow_mappings, broad_mappings, created_by, contributors, created_on, last_updated_on, modified_by, status, rank, keywords)
);

CREATE TABLE subset_definition (
	name TEXT NOT NULL, 
	id_prefixes_are_closed BOOLEAN, 
	definition_uri TEXT, 
	local_names TEXT, 
	conforms_to TEXT, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	structured_aliases TEXT, 
	created_by TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	PRIMARY KEY (name)
);

CREATE TABLE type_definition (
	name TEXT NOT NULL, 
	id_prefixes_are_closed BOOLEAN, 
	definition_uri TEXT, 
	local_names TEXT, 
	conforms_to TEXT, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	structured_aliases TEXT, 
	created_by TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	typeof TEXT, 
	base TEXT, 
	uri TEXT, 
	repr TEXT, 
	union_of TEXT, 
	pattern TEXT, 
	structured_pattern TEXT, 
	unit TEXT, 
	implicit_prefix TEXT, 
	equals_string TEXT, 
	equals_number INTEGER, 
	minimum_value TEXT, 
	maximum_value TEXT, 
	none_of TEXT, 
	exactly_one_of TEXT, 
	any_of TEXT, 
	all_of TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(typeof) REFERENCES type_definition (name)
);

CREATE TABLE "UnitOfMeasure" (
	symbol TEXT, 
	abbreviation TEXT, 
	descriptive_name TEXT, 
	exact_mappings TEXT, 
	ucum_code TEXT, 
	derivation TEXT, 
	has_quantity_kind TEXT, 
	iec61360code TEXT, 
	PRIMARY KEY (symbol, abbreviation, descriptive_name, exact_mappings, ucum_code, derivation, has_quantity_kind, iec61360code)
);

CREATE TABLE class_rule (
	preconditions TEXT, 
	postconditions TEXT, 
	elseconditions TEXT, 
	bidirectional BOOLEAN, 
	open_world BOOLEAN, 
	rank INTEGER, 
	deactivated BOOLEAN, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	todos TEXT, 
	notes TEXT, 
	comments TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	see_also TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	aliases TEXT, 
	structured_aliases TEXT, 
	mappings TEXT, 
	exact_mappings TEXT, 
	close_mappings TEXT, 
	related_mappings TEXT, 
	narrow_mappings TEXT, 
	broad_mappings TEXT, 
	created_by TEXT, 
	contributors TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	categories TEXT, 
	keywords TEXT, 
	class_definition_name TEXT, 
	PRIMARY KEY (preconditions, postconditions, elseconditions, bidirectional, open_world, rank, deactivated, extensions, annotations, description, alt_descriptions, title, deprecated, todos, notes, comments, examples, in_subset, from_schema, imported_from, source, in_language, see_also, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, aliases, structured_aliases, mappings, exact_mappings, close_mappings, related_mappings, narrow_mappings, broad_mappings, created_by, contributors, created_on, last_updated_on, modified_by, status, categories, keywords, class_definition_name), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);

CREATE TABLE enum_binding (
	range TEXT, 
	obligation_level VARCHAR(11), 
	binds_value_of TEXT, 
	pv_formula VARCHAR(11), 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	todos TEXT, 
	notes TEXT, 
	comments TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	see_also TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	aliases TEXT, 
	structured_aliases TEXT, 
	mappings TEXT, 
	exact_mappings TEXT, 
	close_mappings TEXT, 
	related_mappings TEXT, 
	narrow_mappings TEXT, 
	broad_mappings TEXT, 
	created_by TEXT, 
	contributors TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	categories TEXT, 
	keywords TEXT, 
	PRIMARY KEY (range, obligation_level, binds_value_of, pv_formula, extensions, annotations, description, alt_descriptions, title, deprecated, todos, notes, comments, examples, in_subset, from_schema, imported_from, source, in_language, see_also, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, aliases, structured_aliases, mappings, exact_mappings, close_mappings, related_mappings, narrow_mappings, broad_mappings, created_by, contributors, created_on, last_updated_on, modified_by, status, rank, categories, keywords), 
	FOREIGN KEY(range) REFERENCES enum_definition (name)
);

CREATE TABLE schema_definition (
	id_prefixes_are_closed BOOLEAN, 
	definition_uri TEXT, 
	local_names TEXT, 
	conforms_to TEXT, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	structured_aliases TEXT, 
	created_by TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	id TEXT NOT NULL, 
	version TEXT, 
	license TEXT, 
	default_prefix TEXT, 
	default_range TEXT, 
	subsets TEXT, 
	types TEXT, 
	enums TEXT, 
	slots TEXT, 
	classes TEXT, 
	metamodel_version TEXT, 
	source_file TEXT, 
	source_file_date DATETIME, 
	source_file_size INTEGER, 
	generation_date DATETIME, 
	slot_names_unique BOOLEAN, 
	settings TEXT, 
	bindings TEXT, 
	name TEXT NOT NULL, 
	PRIMARY KEY (name), 
	FOREIGN KEY(default_range) REFERENCES type_definition (name)
);

CREATE TABLE slot_definition (
	name TEXT NOT NULL, 
	id_prefixes_are_closed BOOLEAN, 
	definition_uri TEXT, 
	local_names TEXT, 
	conforms_to TEXT, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	structured_aliases TEXT, 
	created_by TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	abstract BOOLEAN, 
	mixin BOOLEAN, 
	string_serialization TEXT, 
	singular_name TEXT, 
	domain TEXT, 
	slot_uri TEXT, 
	array TEXT, 
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
	domain_of TEXT, 
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
	path_rule TEXT, 
	disjoint_with TEXT, 
	children_are_mutually_disjoint BOOLEAN, 
	union_of TEXT, 
	is_a TEXT, 
	mixins TEXT, 
	apply_to TEXT, 
	range TEXT, 
	range_expression TEXT, 
	enum_range TEXT, 
	bindings TEXT, 
	required BOOLEAN, 
	recommended BOOLEAN, 
	multivalued BOOLEAN, 
	inlined BOOLEAN, 
	inlined_as_list BOOLEAN, 
	minimum_value TEXT, 
	maximum_value TEXT, 
	pattern TEXT, 
	structured_pattern TEXT, 
	unit TEXT, 
	implicit_prefix TEXT, 
	value_presence VARCHAR(11), 
	equals_string TEXT, 
	equals_number INTEGER, 
	equals_expression TEXT, 
	exact_cardinality INTEGER, 
	minimum_cardinality INTEGER, 
	maximum_cardinality INTEGER, 
	has_member TEXT, 
	all_members TEXT, 
	none_of TEXT, 
	exactly_one_of TEXT, 
	any_of TEXT, 
	all_of TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(domain) REFERENCES class_definition (name), 
	FOREIGN KEY(subproperty_of) REFERENCES slot_definition (name), 
	FOREIGN KEY(inverse) REFERENCES slot_definition (name), 
	FOREIGN KEY(transitive_form_of) REFERENCES slot_definition (name), 
	FOREIGN KEY(reflexive_transitive_form_of) REFERENCES slot_definition (name), 
	FOREIGN KEY(slot_group) REFERENCES slot_definition (name), 
	FOREIGN KEY(is_a) REFERENCES slot_definition (name)
);

CREATE TABLE unique_key (
	unique_key_name TEXT NOT NULL, 
	unique_key_slots TEXT NOT NULL, 
	consider_nulls_inequal BOOLEAN, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	todos TEXT, 
	notes TEXT, 
	comments TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	see_also TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	aliases TEXT, 
	structured_aliases TEXT, 
	mappings TEXT, 
	exact_mappings TEXT, 
	close_mappings TEXT, 
	related_mappings TEXT, 
	narrow_mappings TEXT, 
	broad_mappings TEXT, 
	created_by TEXT, 
	contributors TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	categories TEXT, 
	keywords TEXT, 
	class_definition_name TEXT, 
	PRIMARY KEY (unique_key_name, unique_key_slots, consider_nulls_inequal, extensions, annotations, description, alt_descriptions, title, deprecated, todos, notes, comments, examples, in_subset, from_schema, imported_from, source, in_language, see_also, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, aliases, structured_aliases, mappings, exact_mappings, close_mappings, related_mappings, narrow_mappings, broad_mappings, created_by, contributors, created_on, last_updated_on, modified_by, status, rank, categories, keywords, class_definition_name), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_id_prefixes (
	backref_id TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (backref_id, id_prefixes), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_implements (
	backref_id TEXT, 
	implements TEXT, 
	PRIMARY KEY (backref_id, implements), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_instantiates (
	backref_id TEXT, 
	instantiates TEXT, 
	PRIMARY KEY (backref_id, instantiates), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_todos (
	backref_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (backref_id, todos), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_notes (
	backref_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (backref_id, notes), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_comments (
	backref_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (backref_id, comments), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_see_also (
	backref_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (backref_id, see_also), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_aliases (
	backref_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_mappings (
	backref_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (backref_id, mappings), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_exact_mappings (
	backref_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (backref_id, exact_mappings), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_close_mappings (
	backref_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (backref_id, close_mappings), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_related_mappings (
	backref_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (backref_id, related_mappings), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_narrow_mappings (
	backref_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (backref_id, narrow_mappings), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_broad_mappings (
	backref_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (backref_id, broad_mappings), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_contributors (
	backref_id TEXT, 
	contributors TEXT, 
	PRIMARY KEY (backref_id, contributors), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_categories (
	backref_id TEXT, 
	categories TEXT, 
	PRIMARY KEY (backref_id, categories), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_keywords (
	backref_id TEXT, 
	keywords TEXT, 
	PRIMARY KEY (backref_id, keywords), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE class_definition_values_from (
	backref_id TEXT, 
	values_from TEXT, 
	PRIMARY KEY (backref_id, values_from), 
	FOREIGN KEY(backref_id) REFERENCES class_definition (name)
);

CREATE TABLE enum_definition_id_prefixes (
	backref_id TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (backref_id, id_prefixes), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_implements (
	backref_id TEXT, 
	implements TEXT, 
	PRIMARY KEY (backref_id, implements), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_instantiates (
	backref_id TEXT, 
	instantiates TEXT, 
	PRIMARY KEY (backref_id, instantiates), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_todos (
	backref_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (backref_id, todos), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_notes (
	backref_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (backref_id, notes), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_comments (
	backref_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (backref_id, comments), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_see_also (
	backref_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (backref_id, see_also), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_aliases (
	backref_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_mappings (
	backref_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (backref_id, mappings), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_exact_mappings (
	backref_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (backref_id, exact_mappings), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_close_mappings (
	backref_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (backref_id, close_mappings), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_related_mappings (
	backref_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (backref_id, related_mappings), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_narrow_mappings (
	backref_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (backref_id, narrow_mappings), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_broad_mappings (
	backref_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (backref_id, broad_mappings), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_contributors (
	backref_id TEXT, 
	contributors TEXT, 
	PRIMARY KEY (backref_id, contributors), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_categories (
	backref_id TEXT, 
	categories TEXT, 
	PRIMARY KEY (backref_id, categories), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_keywords (
	backref_id TEXT, 
	keywords TEXT, 
	PRIMARY KEY (backref_id, keywords), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_mixins (
	backref_id TEXT, 
	mixins TEXT, 
	PRIMARY KEY (backref_id, mixins), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_apply_to (
	backref_id TEXT, 
	apply_to TEXT, 
	PRIMARY KEY (backref_id, apply_to), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_values_from (
	backref_id TEXT, 
	values_from TEXT, 
	PRIMARY KEY (backref_id, values_from), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE enum_definition_concepts (
	backref_id TEXT, 
	concepts TEXT, 
	PRIMARY KEY (backref_id, concepts), 
	FOREIGN KEY(backref_id) REFERENCES enum_definition (name)
);

CREATE TABLE permissible_value_instantiates (
	backref_id TEXT, 
	instantiates TEXT, 
	PRIMARY KEY (backref_id, instantiates), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_implements (
	backref_id TEXT, 
	implements TEXT, 
	PRIMARY KEY (backref_id, implements), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_todos (
	backref_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (backref_id, todos), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_notes (
	backref_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (backref_id, notes), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_comments (
	backref_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (backref_id, comments), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_see_also (
	backref_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (backref_id, see_also), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_aliases (
	backref_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_mappings (
	backref_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (backref_id, mappings), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_exact_mappings (
	backref_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (backref_id, exact_mappings), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_close_mappings (
	backref_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (backref_id, close_mappings), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_related_mappings (
	backref_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (backref_id, related_mappings), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_narrow_mappings (
	backref_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (backref_id, narrow_mappings), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_broad_mappings (
	backref_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (backref_id, broad_mappings), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_contributors (
	backref_id TEXT, 
	contributors TEXT, 
	PRIMARY KEY (backref_id, contributors), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_categories (
	backref_id TEXT, 
	categories TEXT, 
	PRIMARY KEY (backref_id, categories), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE permissible_value_keywords (
	backref_id TEXT, 
	keywords TEXT, 
	PRIMARY KEY (backref_id, keywords), 
	FOREIGN KEY(backref_id) REFERENCES permissible_value (text)
);

CREATE TABLE subset_definition_id_prefixes (
	backref_id TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (backref_id, id_prefixes), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_implements (
	backref_id TEXT, 
	implements TEXT, 
	PRIMARY KEY (backref_id, implements), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_instantiates (
	backref_id TEXT, 
	instantiates TEXT, 
	PRIMARY KEY (backref_id, instantiates), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_todos (
	backref_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (backref_id, todos), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_notes (
	backref_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (backref_id, notes), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_comments (
	backref_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (backref_id, comments), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_see_also (
	backref_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (backref_id, see_also), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_aliases (
	backref_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_mappings (
	backref_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (backref_id, mappings), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_exact_mappings (
	backref_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (backref_id, exact_mappings), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_close_mappings (
	backref_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (backref_id, close_mappings), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_related_mappings (
	backref_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (backref_id, related_mappings), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_narrow_mappings (
	backref_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (backref_id, narrow_mappings), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_broad_mappings (
	backref_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (backref_id, broad_mappings), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_contributors (
	backref_id TEXT, 
	contributors TEXT, 
	PRIMARY KEY (backref_id, contributors), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_categories (
	backref_id TEXT, 
	categories TEXT, 
	PRIMARY KEY (backref_id, categories), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE subset_definition_keywords (
	backref_id TEXT, 
	keywords TEXT, 
	PRIMARY KEY (backref_id, keywords), 
	FOREIGN KEY(backref_id) REFERENCES subset_definition (name)
);

CREATE TABLE type_definition_id_prefixes (
	backref_id TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (backref_id, id_prefixes), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_implements (
	backref_id TEXT, 
	implements TEXT, 
	PRIMARY KEY (backref_id, implements), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_instantiates (
	backref_id TEXT, 
	instantiates TEXT, 
	PRIMARY KEY (backref_id, instantiates), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_todos (
	backref_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (backref_id, todos), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_notes (
	backref_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (backref_id, notes), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_comments (
	backref_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (backref_id, comments), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_see_also (
	backref_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (backref_id, see_also), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_aliases (
	backref_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_mappings (
	backref_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (backref_id, mappings), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_exact_mappings (
	backref_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (backref_id, exact_mappings), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_close_mappings (
	backref_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (backref_id, close_mappings), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_related_mappings (
	backref_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (backref_id, related_mappings), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_narrow_mappings (
	backref_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (backref_id, narrow_mappings), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_broad_mappings (
	backref_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (backref_id, broad_mappings), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_contributors (
	backref_id TEXT, 
	contributors TEXT, 
	PRIMARY KEY (backref_id, contributors), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_categories (
	backref_id TEXT, 
	categories TEXT, 
	PRIMARY KEY (backref_id, categories), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_keywords (
	backref_id TEXT, 
	keywords TEXT, 
	PRIMARY KEY (backref_id, keywords), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE type_definition_equals_string_in (
	backref_id TEXT, 
	equals_string_in TEXT, 
	PRIMARY KEY (backref_id, equals_string_in), 
	FOREIGN KEY(backref_id) REFERENCES type_definition (name)
);

CREATE TABLE path_expression (
	followed_by TEXT, 
	none_of TEXT, 
	any_of TEXT, 
	all_of TEXT, 
	exactly_one_of TEXT, 
	reversed BOOLEAN, 
	traverse TEXT, 
	range_expression TEXT, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	todos TEXT, 
	notes TEXT, 
	comments TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	see_also TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	aliases TEXT, 
	structured_aliases TEXT, 
	mappings TEXT, 
	exact_mappings TEXT, 
	close_mappings TEXT, 
	related_mappings TEXT, 
	narrow_mappings TEXT, 
	broad_mappings TEXT, 
	created_by TEXT, 
	contributors TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	categories TEXT, 
	keywords TEXT, 
	PRIMARY KEY (followed_by, none_of, any_of, all_of, exactly_one_of, reversed, traverse, range_expression, extensions, annotations, description, alt_descriptions, title, deprecated, todos, notes, comments, examples, in_subset, from_schema, imported_from, source, in_language, see_also, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, aliases, structured_aliases, mappings, exact_mappings, close_mappings, related_mappings, narrow_mappings, broad_mappings, created_by, contributors, created_on, last_updated_on, modified_by, status, rank, categories, keywords), 
	FOREIGN KEY(traverse) REFERENCES slot_definition (name)
);

CREATE TABLE prefix (
	prefix_prefix TEXT NOT NULL, 
	prefix_reference TEXT NOT NULL, 
	schema_definition_name TEXT, 
	PRIMARY KEY (prefix_prefix, prefix_reference, schema_definition_name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (name)
);

CREATE TABLE type_mapping (
	framework TEXT NOT NULL, 
	type TEXT, 
	string_serialization TEXT, 
	extensions TEXT, 
	annotations TEXT, 
	description TEXT, 
	alt_descriptions TEXT, 
	title TEXT, 
	deprecated TEXT, 
	todos TEXT, 
	notes TEXT, 
	comments TEXT, 
	examples TEXT, 
	in_subset TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	source TEXT, 
	in_language TEXT, 
	see_also TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	aliases TEXT, 
	structured_aliases TEXT, 
	mappings TEXT, 
	exact_mappings TEXT, 
	close_mappings TEXT, 
	related_mappings TEXT, 
	narrow_mappings TEXT, 
	broad_mappings TEXT, 
	created_by TEXT, 
	contributors TEXT, 
	created_on DATETIME, 
	last_updated_on DATETIME, 
	modified_by TEXT, 
	status TEXT, 
	rank INTEGER, 
	categories TEXT, 
	keywords TEXT, 
	slot_definition_name TEXT, 
	PRIMARY KEY (framework, type, string_serialization, extensions, annotations, description, alt_descriptions, title, deprecated, todos, notes, comments, examples, in_subset, from_schema, imported_from, source, in_language, see_also, deprecated_element_has_exact_replacement, deprecated_element_has_possible_replacement, aliases, structured_aliases, mappings, exact_mappings, close_mappings, related_mappings, narrow_mappings, broad_mappings, created_by, contributors, created_on, last_updated_on, modified_by, status, rank, categories, keywords, slot_definition_name), 
	FOREIGN KEY(type) REFERENCES type_definition (name), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);

CREATE TABLE schema_definition_id_prefixes (
	backref_id TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (backref_id, id_prefixes), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_implements (
	backref_id TEXT, 
	implements TEXT, 
	PRIMARY KEY (backref_id, implements), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_instantiates (
	backref_id TEXT, 
	instantiates TEXT, 
	PRIMARY KEY (backref_id, instantiates), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_todos (
	backref_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (backref_id, todos), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_notes (
	backref_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (backref_id, notes), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_comments (
	backref_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (backref_id, comments), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_see_also (
	backref_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (backref_id, see_also), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_aliases (
	backref_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_mappings (
	backref_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (backref_id, mappings), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_exact_mappings (
	backref_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (backref_id, exact_mappings), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_close_mappings (
	backref_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (backref_id, close_mappings), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_related_mappings (
	backref_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (backref_id, related_mappings), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_narrow_mappings (
	backref_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (backref_id, narrow_mappings), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_broad_mappings (
	backref_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (backref_id, broad_mappings), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_contributors (
	backref_id TEXT, 
	contributors TEXT, 
	PRIMARY KEY (backref_id, contributors), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_categories (
	backref_id TEXT, 
	categories TEXT, 
	PRIMARY KEY (backref_id, categories), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_keywords (
	backref_id TEXT, 
	keywords TEXT, 
	PRIMARY KEY (backref_id, keywords), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_imports (
	backref_id TEXT, 
	imports TEXT, 
	PRIMARY KEY (backref_id, imports), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_emit_prefixes (
	backref_id TEXT, 
	emit_prefixes TEXT, 
	PRIMARY KEY (backref_id, emit_prefixes), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE schema_definition_default_curi_maps (
	backref_id TEXT, 
	default_curi_maps TEXT, 
	PRIMARY KEY (backref_id, default_curi_maps), 
	FOREIGN KEY(backref_id) REFERENCES schema_definition (name)
);

CREATE TABLE slot_definition_id_prefixes (
	backref_id TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (backref_id, id_prefixes), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_implements (
	backref_id TEXT, 
	implements TEXT, 
	PRIMARY KEY (backref_id, implements), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_instantiates (
	backref_id TEXT, 
	instantiates TEXT, 
	PRIMARY KEY (backref_id, instantiates), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_todos (
	backref_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (backref_id, todos), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_notes (
	backref_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (backref_id, notes), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_comments (
	backref_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (backref_id, comments), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_see_also (
	backref_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (backref_id, see_also), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_aliases (
	backref_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_mappings (
	backref_id TEXT, 
	mappings TEXT, 
	PRIMARY KEY (backref_id, mappings), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_exact_mappings (
	backref_id TEXT, 
	exact_mappings TEXT, 
	PRIMARY KEY (backref_id, exact_mappings), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_close_mappings (
	backref_id TEXT, 
	close_mappings TEXT, 
	PRIMARY KEY (backref_id, close_mappings), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_related_mappings (
	backref_id TEXT, 
	related_mappings TEXT, 
	PRIMARY KEY (backref_id, related_mappings), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_narrow_mappings (
	backref_id TEXT, 
	narrow_mappings TEXT, 
	PRIMARY KEY (backref_id, narrow_mappings), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_broad_mappings (
	backref_id TEXT, 
	broad_mappings TEXT, 
	PRIMARY KEY (backref_id, broad_mappings), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_contributors (
	backref_id TEXT, 
	contributors TEXT, 
	PRIMARY KEY (backref_id, contributors), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_categories (
	backref_id TEXT, 
	categories TEXT, 
	PRIMARY KEY (backref_id, categories), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_keywords (
	backref_id TEXT, 
	keywords TEXT, 
	PRIMARY KEY (backref_id, keywords), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_values_from (
	backref_id TEXT, 
	values_from TEXT, 
	PRIMARY KEY (backref_id, values_from), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);

CREATE TABLE slot_definition_equals_string_in (
	backref_id TEXT, 
	equals_string_in TEXT, 
	PRIMARY KEY (backref_id, equals_string_in), 
	FOREIGN KEY(backref_id) REFERENCES slot_definition (name)
);
