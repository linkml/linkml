
CREATE TABLE common_metadata (
	id INTEGER, 
	description TEXT, 
	title TEXT, 
	deprecated TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
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
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
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
	name TEXT, 
	definition_uri TEXT, 
	conforms_to TEXT, 
	description TEXT, 
	title TEXT, 
	deprecated TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(default_range) REFERENCES type_definition (name)
);
CREATE TABLE type_expression (
	id INTEGER, 
	pattern TEXT, 
	equals_string TEXT, 
	equals_number INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE anonymous_type_expression (
	id INTEGER, 
	pattern TEXT, 
	equals_string TEXT, 
	equals_number INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE type_definition (
	typeof TEXT, 
	base TEXT, 
	uri TEXT, 
	repr TEXT, 
	pattern TEXT, 
	equals_string TEXT, 
	equals_number INTEGER, 
	name TEXT, 
	definition_uri TEXT, 
	conforms_to TEXT, 
	description TEXT, 
	title TEXT, 
	deprecated TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	schema_definition_name TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(typeof) REFERENCES type_definition (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
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
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(is_a) REFERENCES definition (name)
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
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE class_expression (
	id INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE class_level_rule (
	id INTEGER, 
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
CREATE TABLE subset_definition (
	name TEXT, 
	definition_uri TEXT, 
	conforms_to TEXT, 
	description TEXT, 
	title TEXT, 
	deprecated TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	schema_definition_name TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE enum_definition (
	code_set TEXT, 
	code_set_tag TEXT, 
	code_set_version TEXT, 
	pv_formula VARCHAR(11), 
	name TEXT, 
	definition_uri TEXT, 
	conforms_to TEXT, 
	description TEXT, 
	title TEXT, 
	deprecated TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	schema_definition_name TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
);
CREATE TABLE class_definition (
	class_uri TEXT, 
	subclass_of TEXT, 
	tree_root BOOLEAN, 
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
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	schema_definition_name TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(is_a) REFERENCES class_definition (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id)
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
CREATE TABLE element_id_prefixes (
	element_name TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (element_name, id_prefixes), 
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
CREATE TABLE schema_definition_id_prefixes (
	schema_definition_name TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (schema_definition_name, id_prefixes), 
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
CREATE TABLE type_definition_equals_string_in (
	type_definition_name TEXT, 
	equals_string_in TEXT, 
	PRIMARY KEY (type_definition_name, equals_string_in), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name)
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
CREATE TABLE type_definition_id_prefixes (
	type_definition_name TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (type_definition_name, id_prefixes), 
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
CREATE TABLE anonymous_class_expression (
	id INTEGER, 
	is_a TEXT, 
	description TEXT, 
	title TEXT, 
	deprecated TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	class_definition_name TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(is_a) REFERENCES definition (name), 
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
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	enum_definition_name TEXT, 
	PRIMARY KEY (text), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name)
);
CREATE TABLE unique_key (
	id INTEGER, 
	description TEXT, 
	title TEXT, 
	deprecated TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	class_definition_name TEXT, 
	PRIMARY KEY (id), 
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
CREATE TABLE definition_in_subset (
	definition_name TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (definition_name, in_subset), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE enum_definition_id_prefixes (
	enum_definition_name TEXT, 
	id_prefixes TEXT, 
	PRIMARY KEY (enum_definition_name, id_prefixes), 
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
CREATE TABLE anonymous_expression_in_subset (
	anonymous_expression_id TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (anonymous_expression_id, in_subset), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE class_definition_union_of (
	class_definition_name TEXT, 
	union_of TEXT, 
	PRIMARY KEY (class_definition_name, union_of), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(union_of) REFERENCES class_definition (name)
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
CREATE TABLE anonymous_slot_expression (
	id INTEGER, 
	range TEXT, 
	required BOOLEAN, 
	recommended BOOLEAN, 
	minimum_value INTEGER, 
	maximum_value INTEGER, 
	pattern TEXT, 
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
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	range_expression_id TEXT, 
	has_member_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(range) REFERENCES element (name), 
	FOREIGN KEY(range_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(has_member_id) REFERENCES anonymous_slot_expression (id)
);
CREATE TABLE class_rule (
	id INTEGER, 
	bidirectional BOOLEAN, 
	open_world BOOLEAN, 
	precedence INTEGER, 
	deactivated BOOLEAN, 
	description TEXT, 
	title TEXT, 
	deprecated TEXT, 
	from_schema TEXT, 
	imported_from TEXT, 
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
CREATE TABLE unique_key_todos (
	unique_key_id TEXT, 
	todos TEXT, 
	PRIMARY KEY (unique_key_id, todos), 
	FOREIGN KEY(unique_key_id) REFERENCES unique_key (id)
);
CREATE TABLE unique_key_notes (
	unique_key_id TEXT, 
	notes TEXT, 
	PRIMARY KEY (unique_key_id, notes), 
	FOREIGN KEY(unique_key_id) REFERENCES unique_key (id)
);
CREATE TABLE unique_key_comments (
	unique_key_id TEXT, 
	comments TEXT, 
	PRIMARY KEY (unique_key_id, comments), 
	FOREIGN KEY(unique_key_id) REFERENCES unique_key (id)
);
CREATE TABLE unique_key_in_subset (
	unique_key_id TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (unique_key_id, in_subset), 
	FOREIGN KEY(unique_key_id) REFERENCES unique_key (id), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE unique_key_see_also (
	unique_key_id TEXT, 
	see_also TEXT, 
	PRIMARY KEY (unique_key_id, see_also), 
	FOREIGN KEY(unique_key_id) REFERENCES unique_key (id)
);
CREATE TABLE slot_expression (
	id INTEGER, 
	range TEXT, 
	required BOOLEAN, 
	recommended BOOLEAN, 
	minimum_value INTEGER, 
	maximum_value INTEGER, 
	pattern TEXT, 
	equals_string TEXT, 
	equals_number INTEGER, 
	equals_expression TEXT, 
	minimum_cardinality INTEGER, 
	maximum_cardinality INTEGER, 
	range_expression_id TEXT, 
	has_member_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(range) REFERENCES element (name), 
	FOREIGN KEY(range_expression_id) REFERENCES anonymous_class_expression (id), 
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
CREATE TABLE slot_definition (
	singular_name TEXT, 
	domain TEXT, 
	slot_uri TEXT, 
	multivalued BOOLEAN, 
	inherited BOOLEAN, 
	readonly TEXT, 
	ifabsent TEXT, 
	inlined BOOLEAN, 
	inlined_as_list BOOLEAN, 
	"key" BOOLEAN, 
	identifier BOOLEAN, 
	designates_type BOOLEAN, 
	alias TEXT, 
	owner TEXT, 
	subproperty_of TEXT, 
	symmetric BOOLEAN, 
	inverse TEXT, 
	is_class_field BOOLEAN, 
	role TEXT, 
	is_usage_slot BOOLEAN, 
	usage_slot_name TEXT, 
	range TEXT, 
	required BOOLEAN, 
	recommended BOOLEAN, 
	minimum_value INTEGER, 
	maximum_value INTEGER, 
	pattern TEXT, 
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
	deprecated_element_has_exact_replacement TEXT, 
	deprecated_element_has_possible_replacement TEXT, 
	schema_definition_name TEXT, 
	slot_expression_id TEXT, 
	anonymous_slot_expression_id TEXT, 
	slot_definition_name TEXT, 
	class_expression_id TEXT, 
	anonymous_class_expression_id TEXT, 
	class_definition_name TEXT, 
	range_expression_id TEXT, 
	has_member_id TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(domain) REFERENCES class_definition (name), 
	FOREIGN KEY(owner) REFERENCES definition (name), 
	FOREIGN KEY(subproperty_of) REFERENCES slot_definition (name), 
	FOREIGN KEY(inverse) REFERENCES slot_definition (name), 
	FOREIGN KEY(range) REFERENCES element (name), 
	FOREIGN KEY(is_a) REFERENCES slot_definition (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(slot_expression_id) REFERENCES slot_expression (id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(class_expression_id) REFERENCES class_expression (id), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(range_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(has_member_id) REFERENCES anonymous_slot_expression (id)
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
	anonymous_expression_id TEXT, 
	anonymous_slot_expression_id TEXT, 
	slot_definition_name TEXT, 
	anonymous_class_expression_id TEXT, 
	class_definition_name TEXT, 
	class_rule_id TEXT, 
	permissible_value_text TEXT, 
	unique_key_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id), 
	FOREIGN KEY(element_name) REFERENCES element (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text), 
	FOREIGN KEY(unique_key_id) REFERENCES unique_key (id)
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
	anonymous_expression_id TEXT, 
	anonymous_slot_expression_id TEXT, 
	slot_definition_name TEXT, 
	anonymous_class_expression_id TEXT, 
	class_definition_name TEXT, 
	class_rule_id TEXT, 
	permissible_value_text TEXT, 
	unique_key_id TEXT, 
	PRIMARY KEY (source, description, common_metadata_id, element_name, schema_definition_name, type_definition_name, subset_definition_name, definition_name, enum_definition_name, anonymous_expression_id, anonymous_slot_expression_id, slot_definition_name, anonymous_class_expression_id, class_definition_name, class_rule_id, permissible_value_text, unique_key_id), 
	FOREIGN KEY(common_metadata_id) REFERENCES common_metadata (id), 
	FOREIGN KEY(element_name) REFERENCES element (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text), 
	FOREIGN KEY(unique_key_id) REFERENCES unique_key (id)
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
	anonymous_expression_id TEXT, 
	anonymous_slot_expression_id TEXT, 
	slot_definition_name TEXT, 
	anonymous_class_expression_id TEXT, 
	class_definition_name TEXT, 
	class_rule_id TEXT, 
	permissible_value_text TEXT, 
	unique_key_id TEXT, 
	annotatable_id TEXT, 
	annotation_tag TEXT, 
	PRIMARY KEY (tag, value, element_name, schema_definition_name, type_definition_name, subset_definition_name, definition_name, enum_definition_name, anonymous_expression_id, anonymous_slot_expression_id, slot_definition_name, anonymous_class_expression_id, class_definition_name, class_rule_id, permissible_value_text, unique_key_id, annotatable_id, annotation_tag), 
	FOREIGN KEY(element_name) REFERENCES element (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text), 
	FOREIGN KEY(unique_key_id) REFERENCES unique_key (id), 
	FOREIGN KEY(annotatable_id) REFERENCES annotatable (id), 
	FOREIGN KEY(annotation_tag) REFERENCES annotation (tag)
);
CREATE TABLE slot_definition_domain_of (
	slot_definition_name TEXT, 
	domain_of TEXT, 
	PRIMARY KEY (slot_definition_name, domain_of), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(domain_of) REFERENCES class_definition (name)
);
CREATE TABLE slot_definition_equals_string_in (
	slot_definition_name TEXT, 
	equals_string_in TEXT, 
	PRIMARY KEY (slot_definition_name, equals_string_in), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
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
CREATE TABLE slot_definition_in_subset (
	slot_definition_name TEXT, 
	in_subset TEXT, 
	PRIMARY KEY (slot_definition_name, in_subset), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(in_subset) REFERENCES subset_definition (name)
);
CREATE TABLE slot_definition_see_also (
	slot_definition_name TEXT, 
	see_also TEXT, 
	PRIMARY KEY (slot_definition_name, see_also), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name)
);
CREATE TABLE class_definition_slots (
	class_definition_name TEXT, 
	slots TEXT, 
	PRIMARY KEY (class_definition_name, slots), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(slots) REFERENCES slot_definition (name)
);
CREATE TABLE class_definition_defining_slots (
	class_definition_name TEXT, 
	defining_slots TEXT, 
	PRIMARY KEY (class_definition_name, defining_slots), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(defining_slots) REFERENCES slot_definition (name)
);
CREATE TABLE unique_key_unique_key_slots (
	unique_key_id TEXT, 
	unique_key_slots TEXT NOT NULL, 
	PRIMARY KEY (unique_key_id, unique_key_slots), 
	FOREIGN KEY(unique_key_id) REFERENCES unique_key (id), 
	FOREIGN KEY(unique_key_slots) REFERENCES slot_definition (name)
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
	anonymous_expression_id TEXT, 
	anonymous_slot_expression_id TEXT, 
	slot_definition_name TEXT, 
	anonymous_class_expression_id TEXT, 
	class_definition_name TEXT, 
	class_rule_id TEXT, 
	permissible_value_text TEXT, 
	unique_key_id TEXT, 
	annotation_tag TEXT, 
	extension_tag TEXT, 
	extensible_id TEXT, 
	PRIMARY KEY (tag, value, element_name, schema_definition_name, type_definition_name, subset_definition_name, definition_name, enum_definition_name, anonymous_expression_id, anonymous_slot_expression_id, slot_definition_name, anonymous_class_expression_id, class_definition_name, class_rule_id, permissible_value_text, unique_key_id, annotation_tag, extension_tag, extensible_id), 
	FOREIGN KEY(element_name) REFERENCES element (name), 
	FOREIGN KEY(schema_definition_name) REFERENCES schema_definition (id), 
	FOREIGN KEY(type_definition_name) REFERENCES type_definition (name), 
	FOREIGN KEY(subset_definition_name) REFERENCES subset_definition (name), 
	FOREIGN KEY(definition_name) REFERENCES definition (name), 
	FOREIGN KEY(enum_definition_name) REFERENCES enum_definition (name), 
	FOREIGN KEY(anonymous_expression_id) REFERENCES anonymous_expression (id), 
	FOREIGN KEY(anonymous_slot_expression_id) REFERENCES anonymous_slot_expression (id), 
	FOREIGN KEY(slot_definition_name) REFERENCES slot_definition (name), 
	FOREIGN KEY(anonymous_class_expression_id) REFERENCES anonymous_class_expression (id), 
	FOREIGN KEY(class_definition_name) REFERENCES class_definition (name), 
	FOREIGN KEY(class_rule_id) REFERENCES class_rule (id), 
	FOREIGN KEY(permissible_value_text) REFERENCES permissible_value (text), 
	FOREIGN KEY(unique_key_id) REFERENCES unique_key (id), 
	FOREIGN KEY(annotation_tag) REFERENCES annotation (tag), 
	FOREIGN KEY(extension_tag) REFERENCES extension (tag), 
	FOREIGN KEY(extensible_id) REFERENCES extensible (id)
);