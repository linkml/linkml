slot(abstract).
domain(abstract, definition).
range(abstract, boolean).
has_uri(abstract, 'http://w3id.org/biolink/vocab/abstract').
slot(alias).
domain(alias, slot_definition).
range(alias, string).
has_uri(alias, 'http://w3id.org/biolink/vocab/alias').
slot(aliases).
domain(aliases, element).
range(aliases, string).
has_uri(aliases, 'http://w3id.org/biolink/vocab/aliases').
multivalued(aliases).
slot(source).
domain(source, alt_description).
range(source, string).
has_uri(source, 'http://w3id.org/biolink/vocab/source').
required(source).
slot(description).
domain(description, alt_description).
range(description, string).
has_uri(description, 'http://w3id.org/biolink/vocab/description').
required(description).
slot(alt_descriptions).
domain(alt_descriptions, element).
range(alt_descriptions, alt_description).
has_uri(alt_descriptions, 'http://w3id.org/biolink/vocab/alt_descriptions').
multivalued(alt_descriptions).
slot(annotations).
domain(annotations, annotatable).
range(annotations, annotation).
has_uri(annotations, 'http://w3id.org/biolink/vocab/annotations').
multivalued(annotations).
slot(apply_to).
domain(apply_to, definition).
range(apply_to, definition).
has_uri(apply_to, 'http://w3id.org/biolink/vocab/apply_to').
multivalued(apply_to).
slot(attributes).
domain(attributes, class_definition).
range(attributes, slot_definition).
has_uri(attributes, 'http://w3id.org/biolink/vocab/attributes').
multivalued(attributes).
slot(base).
domain(base, type_definition).
range(base, string).
has_uri(base, 'http://w3id.org/biolink/vocab/base').
slot(broad_mappings).
range(broad_mappings, uriorcurie).
has_uri(broad_mappings, 'http://w3id.org/biolink/vocab/broad_mappings').
multivalued(broad_mappings).
slot(apply_to).
domain(apply_to, class_definition).
range(apply_to, class_definition).
has_uri(apply_to, 'http://w3id.org/biolink/vocab/apply_to').
multivalued(apply_to).
slot(is_a).
domain(is_a, class_definition).
range(is_a, class_definition).
has_uri(is_a, 'http://w3id.org/biolink/vocab/is_a').
slot(mixins).
domain(mixins, class_definition).
range(mixins, class_definition).
has_uri(mixins, 'http://w3id.org/biolink/vocab/mixins').
multivalued(mixins).
slot(class_uri).
domain(class_uri, class_definition).
range(class_uri, uriorcurie).
has_uri(class_uri, 'http://w3id.org/biolink/vocab/class_uri').
slot(classes).
domain(classes, schema_definition).
range(classes, class_definition).
has_uri(classes, 'http://w3id.org/biolink/vocab/classes').
multivalued(classes).
slot(close_mappings).
range(close_mappings, uriorcurie).
has_uri(close_mappings, 'http://w3id.org/biolink/vocab/close_mappings').
multivalued(close_mappings).
slot(code_set).
domain(code_set, enum_definition).
range(code_set, uriorcurie).
has_uri(code_set, 'http://w3id.org/biolink/vocab/code_set').
slot(code_set_tag).
domain(code_set_tag, enum_definition).
range(code_set_tag, string).
has_uri(code_set_tag, 'http://w3id.org/biolink/vocab/code_set_tag').
slot(code_set_version).
domain(code_set_version, enum_definition).
range(code_set_version, string).
has_uri(code_set_version, 'http://w3id.org/biolink/vocab/code_set_version').
slot(comments).
domain(comments, element).
range(comments, string).
has_uri(comments, 'http://w3id.org/biolink/vocab/comments').
multivalued(comments).
slot(created_by).
domain(created_by, element).
range(created_by, uriorcurie).
has_uri(created_by, 'http://w3id.org/biolink/vocab/created_by').
slot(created_on).
domain(created_on, element).
range(created_on, datetime).
has_uri(created_on, 'http://w3id.org/biolink/vocab/created_on').
slot(default_curi_maps).
domain(default_curi_maps, schema_definition).
range(default_curi_maps, string).
has_uri(default_curi_maps, 'http://w3id.org/biolink/vocab/default_curi_maps').
multivalued(default_curi_maps).
slot(default_prefix).
domain(default_prefix, schema_definition).
range(default_prefix, string).
has_uri(default_prefix, 'http://w3id.org/biolink/vocab/default_prefix').
slot(default_range).
domain(default_range, schema_definition).
range(default_range, type_definition).
has_uri(default_range, 'http://w3id.org/biolink/vocab/default_range').
slot(defining_slots).
domain(defining_slots, class_definition).
range(defining_slots, slot_definition).
has_uri(defining_slots, 'http://w3id.org/biolink/vocab/defining_slots').
multivalued(defining_slots).
slot(definition_uri).
domain(definition_uri, element).
range(definition_uri, uriorcurie).
has_uri(definition_uri, 'http://w3id.org/biolink/vocab/definition_uri').
slot(deprecated).
domain(deprecated, element).
range(deprecated, string).
has_uri(deprecated, 'http://w3id.org/biolink/vocab/deprecated').
slot(deprecated_element_has_exact_replacement).
range(deprecated_element_has_exact_replacement, uriorcurie).
has_uri(deprecated_element_has_exact_replacement, 'http://w3id.org/biolink/vocab/deprecated_element_has_exact_replacement').
slot(deprecated_element_has_possible_replacement).
range(deprecated_element_has_possible_replacement, uriorcurie).
has_uri(deprecated_element_has_possible_replacement, 'http://w3id.org/biolink/vocab/deprecated_element_has_possible_replacement').
slot(description).
domain(description, element).
range(description, string).
has_uri(description, 'http://w3id.org/biolink/vocab/description').
slot(designates_type).
domain(designates_type, slot_definition).
range(designates_type, boolean).
has_uri(designates_type, 'http://w3id.org/biolink/vocab/designates_type').
slot(domain).
domain(domain, slot_definition).
range(domain, class_definition).
has_uri(domain, 'http://w3id.org/biolink/vocab/domain').
slot(domain_of).
domain(domain_of, slot_definition).
range(domain_of, class_definition).
has_uri(domain_of, 'http://w3id.org/biolink/vocab/domain_of').
multivalued(domain_of).
slot(emit_prefixes).
domain(emit_prefixes, schema_definition).
range(emit_prefixes, ncname).
has_uri(emit_prefixes, 'http://w3id.org/biolink/vocab/emit_prefixes').
multivalued(emit_prefixes).
slot(enums).
domain(enums, schema_definition).
range(enums, enum_definition).
has_uri(enums, 'http://w3id.org/biolink/vocab/enums').
multivalued(enums).
slot(exact_mappings).
range(exact_mappings, uriorcurie).
has_uri(exact_mappings, 'http://w3id.org/biolink/vocab/exact_mappings').
multivalued(exact_mappings).
slot(examples).
domain(examples, element).
range(examples, example).
has_uri(examples, 'http://w3id.org/biolink/vocab/examples').
multivalued(examples).
slot(tag).
domain(tag, extension).
range(tag, uriorcurie).
has_uri(tag, 'http://w3id.org/biolink/vocab/tag').
required(tag).
slot(value).
domain(value, extension).
range(value, string).
has_uri(value, 'http://w3id.org/biolink/vocab/value').
required(value).
slot(extensions).
domain(extensions, extensible).
range(extensions, extension).
has_uri(extensions, 'http://w3id.org/biolink/vocab/extensions').
multivalued(extensions).
slot(from_schema).
domain(from_schema, element).
range(from_schema, uri).
has_uri(from_schema, 'http://w3id.org/biolink/vocab/from_schema').
slot(generation_date).
domain(generation_date, schema_definition).
range(generation_date, datetime).
has_uri(generation_date, 'http://w3id.org/biolink/vocab/generation_date').
slot(id).
domain(id, schema_definition).
range(id, uri).
has_uri(id, 'http://w3id.org/biolink/vocab/id').
required(id).
slot(id_prefixes).
domain(id_prefixes, element).
range(id_prefixes, ncname).
has_uri(id_prefixes, 'http://w3id.org/biolink/vocab/id_prefixes').
multivalued(id_prefixes).
slot(identifier).
domain(identifier, slot_definition).
range(identifier, boolean).
has_uri(identifier, 'http://w3id.org/biolink/vocab/identifier').
slot(ifabsent).
domain(ifabsent, slot_definition).
range(ifabsent, string).
has_uri(ifabsent, 'http://w3id.org/biolink/vocab/ifabsent').
slot(imported_from).
domain(imported_from, element).
range(imported_from, string).
has_uri(imported_from, 'http://w3id.org/biolink/vocab/imported_from').
slot(imports).
domain(imports, schema_definition).
range(imports, uriorcurie).
has_uri(imports, 'http://w3id.org/biolink/vocab/imports').
multivalued(imports).
slot(in_subset).
domain(in_subset, element).
range(in_subset, subset_definition).
has_uri(in_subset, 'http://w3id.org/biolink/vocab/in_subset').
multivalued(in_subset).
slot(inherited).
domain(inherited, slot_definition).
range(inherited, boolean).
has_uri(inherited, 'http://w3id.org/biolink/vocab/inherited').
slot(inlined).
domain(inlined, slot_definition).
range(inlined, boolean).
has_uri(inlined, 'http://w3id.org/biolink/vocab/inlined').
slot(inlined_as_list).
domain(inlined_as_list, slot_definition).
range(inlined_as_list, boolean).
has_uri(inlined_as_list, 'http://w3id.org/biolink/vocab/inlined_as_list').
slot(inverse).
domain(inverse, slot_definition).
range(inverse, slot_definition).
has_uri(inverse, 'http://w3id.org/biolink/vocab/inverse').
slot(is_a).
domain(is_a, definition).
range(is_a, definition).
has_uri(is_a, 'http://w3id.org/biolink/vocab/is_a').
slot(is_class_field).
domain(is_class_field, slot_definition).
range(is_class_field, boolean).
has_uri(is_class_field, 'http://w3id.org/biolink/vocab/is_class_field').
slot(is_usage_slot).
domain(is_usage_slot, slot_definition).
range(is_usage_slot, boolean).
has_uri(is_usage_slot, 'http://w3id.org/biolink/vocab/is_usage_slot').
slot(key).
domain(key, slot_definition).
range(key, boolean).
has_uri(key, 'http://w3id.org/biolink/vocab/key').
slot(last_updated_on).
domain(last_updated_on, element).
range(last_updated_on, datetime).
has_uri(last_updated_on, 'http://w3id.org/biolink/vocab/last_updated_on').
slot(license).
domain(license, schema_definition).
range(license, string).
has_uri(license, 'http://w3id.org/biolink/vocab/license').
slot(local_name_source).
domain(local_name_source, local_name).
range(local_name_source, ncname).
has_uri(local_name_source, 'http://w3id.org/biolink/vocab/local_name_source').
required(local_name_source).
slot(local_name_value).
domain(local_name_value, local_name).
range(local_name_value, string).
has_uri(local_name_value, 'http://w3id.org/biolink/vocab/local_name_value').
required(local_name_value).
slot(local_names).
domain(local_names, element).
range(local_names, local_name).
has_uri(local_names, 'http://w3id.org/biolink/vocab/local_names').
multivalued(local_names).
slot(mappings).
range(mappings, uriorcurie).
has_uri(mappings, 'http://w3id.org/biolink/vocab/mappings').
multivalued(mappings).
slot(maximum_value).
domain(maximum_value, slot_definition).
range(maximum_value, integer).
has_uri(maximum_value, 'http://w3id.org/biolink/vocab/maximum_value').
slot(meaning).
domain(meaning, permissible_value).
range(meaning, uriorcurie).
has_uri(meaning, 'http://w3id.org/biolink/vocab/meaning').
slot(metamodel_version).
domain(metamodel_version, schema_definition).
range(metamodel_version, string).
has_uri(metamodel_version, 'http://w3id.org/biolink/vocab/metamodel_version').
slot(minimum_value).
domain(minimum_value, slot_definition).
range(minimum_value, integer).
has_uri(minimum_value, 'http://w3id.org/biolink/vocab/minimum_value').
slot(mixin).
domain(mixin, definition).
range(mixin, boolean).
has_uri(mixin, 'http://w3id.org/biolink/vocab/mixin').
slot(mixins).
domain(mixins, definition).
range(mixins, definition).
has_uri(mixins, 'http://w3id.org/biolink/vocab/mixins').
multivalued(mixins).
slot(modified_by).
domain(modified_by, element).
range(modified_by, uriorcurie).
has_uri(modified_by, 'http://w3id.org/biolink/vocab/modified_by').
slot(multivalued).
domain(multivalued, slot_definition).
range(multivalued, boolean).
has_uri(multivalued, 'http://w3id.org/biolink/vocab/multivalued').
slot(name).
domain(name, element).
range(name, string).
has_uri(name, 'http://w3id.org/biolink/vocab/name').
required(name).
slot(narrow_mappings).
range(narrow_mappings, uriorcurie).
has_uri(narrow_mappings, 'http://w3id.org/biolink/vocab/narrow_mappings').
multivalued(narrow_mappings).
slot(notes).
domain(notes, element).
range(notes, string).
has_uri(notes, 'http://w3id.org/biolink/vocab/notes').
multivalued(notes).
slot(owner).
domain(owner, slot_definition).
range(owner, definition).
has_uri(owner, 'http://w3id.org/biolink/vocab/owner').
slot(pattern).
domain(pattern, definition).
range(pattern, string).
has_uri(pattern, 'http://w3id.org/biolink/vocab/pattern').
slot(is_a).
domain(is_a, permissible_value).
range(is_a, permissible_value).
has_uri(is_a, 'http://w3id.org/biolink/vocab/is_a').
slot(mixins).
domain(mixins, permissible_value).
range(mixins, permissible_value).
has_uri(mixins, 'http://w3id.org/biolink/vocab/mixins').
multivalued(mixins).
slot(permissible_values).
domain(permissible_values, enum_definition).
range(permissible_values, permissible_value).
has_uri(permissible_values, 'http://w3id.org/biolink/vocab/permissible_values').
multivalued(permissible_values).
slot(prefix_prefix).
domain(prefix_prefix, prefix).
range(prefix_prefix, ncname).
has_uri(prefix_prefix, 'http://w3id.org/biolink/vocab/prefix_prefix').
required(prefix_prefix).
slot(prefix_reference).
domain(prefix_reference, prefix).
range(prefix_reference, uri).
has_uri(prefix_reference, 'http://w3id.org/biolink/vocab/prefix_reference').
required(prefix_reference).
slot(prefixes).
domain(prefixes, schema_definition).
range(prefixes, prefix).
has_uri(prefixes, 'http://w3id.org/biolink/vocab/prefixes').
multivalued(prefixes).
slot(pv_formula).
domain(pv_formula, enum_definition).
range(pv_formula, pv_formula_options).
has_uri(pv_formula, 'http://w3id.org/biolink/vocab/pv_formula').
slot(range).
domain(range, slot_definition).
range(range, element).
has_uri(range, 'http://w3id.org/biolink/vocab/range').
slot(readonly).
domain(readonly, slot_definition).
range(readonly, string).
has_uri(readonly, 'http://w3id.org/biolink/vocab/readonly').
slot(recommended).
domain(recommended, slot_definition).
range(recommended, boolean).
has_uri(recommended, 'http://w3id.org/biolink/vocab/recommended').
slot(related_mappings).
range(related_mappings, uriorcurie).
has_uri(related_mappings, 'http://w3id.org/biolink/vocab/related_mappings').
multivalued(related_mappings).
slot(repr).
domain(repr, type_definition).
range(repr, string).
has_uri(repr, 'http://w3id.org/biolink/vocab/repr').
slot(required).
domain(required, slot_definition).
range(required, boolean).
has_uri(required, 'http://w3id.org/biolink/vocab/required').
slot(role).
domain(role, slot_definition).
range(role, string).
has_uri(role, 'http://w3id.org/biolink/vocab/role').
slot(name).
domain(name, schema_definition).
range(name, ncname).
has_uri(name, 'http://w3id.org/biolink/vocab/name').
required(name).
slot(see_also).
domain(see_also, element).
range(see_also, uriorcurie).
has_uri(see_also, 'http://w3id.org/biolink/vocab/see_also').
multivalued(see_also).
slot(singular_name).
domain(singular_name, slot_definition).
range(singular_name, string).
has_uri(singular_name, 'http://w3id.org/biolink/vocab/singular_name').
slot(apply_to).
domain(apply_to, slot_definition).
range(apply_to, slot_definition).
has_uri(apply_to, 'http://w3id.org/biolink/vocab/apply_to').
multivalued(apply_to).
slot(is_a).
domain(is_a, slot_definition).
range(is_a, slot_definition).
has_uri(is_a, 'http://w3id.org/biolink/vocab/is_a').
slot(mixins).
domain(mixins, slot_definition).
range(mixins, slot_definition).
has_uri(mixins, 'http://w3id.org/biolink/vocab/mixins').
multivalued(mixins).
slot(slots).
domain(slots, schema_definition).
range(slots, slot_definition).
has_uri(slots, 'http://w3id.org/biolink/vocab/slots').
multivalued(slots).
slot(slot_uri).
domain(slot_uri, slot_definition).
range(slot_uri, uriorcurie).
has_uri(slot_uri, 'http://w3id.org/biolink/vocab/slot_uri').
slot(slot_usage).
domain(slot_usage, class_definition).
range(slot_usage, slot_definition).
has_uri(slot_usage, 'http://w3id.org/biolink/vocab/slot_usage').
multivalued(slot_usage).
slot(slots).
domain(slots, class_definition).
range(slots, slot_definition).
has_uri(slots, 'http://w3id.org/biolink/vocab/slots').
multivalued(slots).
slot(source_file).
domain(source_file, schema_definition).
range(source_file, string).
has_uri(source_file, 'http://w3id.org/biolink/vocab/source_file').
slot(source_file_date).
domain(source_file_date, schema_definition).
range(source_file_date, datetime).
has_uri(source_file_date, 'http://w3id.org/biolink/vocab/source_file_date').
slot(source_file_size).
domain(source_file_size, schema_definition).
range(source_file_size, integer).
has_uri(source_file_size, 'http://w3id.org/biolink/vocab/source_file_size').
slot(status).
domain(status, element).
range(status, uriorcurie).
has_uri(status, 'http://w3id.org/biolink/vocab/status').
slot(string_serialization).
domain(string_serialization, definition).
range(string_serialization, string).
has_uri(string_serialization, 'http://w3id.org/biolink/vocab/string_serialization').
slot(subclass_of).
domain(subclass_of, class_definition).
range(subclass_of, uriorcurie).
has_uri(subclass_of, 'http://w3id.org/biolink/vocab/subclass_of').
slot(subproperty_of).
domain(subproperty_of, slot_definition).
range(subproperty_of, slot_definition).
has_uri(subproperty_of, 'http://w3id.org/biolink/vocab/subproperty_of').
slot(subsets).
domain(subsets, schema_definition).
range(subsets, subset_definition).
has_uri(subsets, 'http://w3id.org/biolink/vocab/subsets').
multivalued(subsets).
slot(symmetric).
domain(symmetric, slot_definition).
range(symmetric, boolean).
has_uri(symmetric, 'http://w3id.org/biolink/vocab/symmetric').
slot(text).
domain(text, permissible_value).
range(text, string).
has_uri(text, 'http://w3id.org/biolink/vocab/text').
required(text).
slot(title).
domain(title, element).
range(title, string).
has_uri(title, 'http://w3id.org/biolink/vocab/title').
slot(todos).
domain(todos, element).
range(todos, string).
has_uri(todos, 'http://w3id.org/biolink/vocab/todos').
multivalued(todos).
slot(tree_root).
domain(tree_root, class_definition).
range(tree_root, boolean).
has_uri(tree_root, 'http://w3id.org/biolink/vocab/tree_root').
slot(uri).
domain(uri, type_definition).
range(uri, uriorcurie).
has_uri(uri, 'http://w3id.org/biolink/vocab/uri').
slot(typeof).
domain(typeof, type_definition).
range(typeof, type_definition).
has_uri(typeof, 'http://w3id.org/biolink/vocab/typeof').
slot(types).
domain(types, schema_definition).
range(types, type_definition).
has_uri(types, 'http://w3id.org/biolink/vocab/types').
multivalued(types).
slot(union_of).
domain(union_of, class_definition).
range(union_of, class_definition).
has_uri(union_of, 'http://w3id.org/biolink/vocab/union_of').
multivalued(union_of).
slot(unique_key_slots).
domain(unique_key_slots, unique_key).
range(unique_key_slots, slot_definition).
has_uri(unique_key_slots, 'http://w3id.org/biolink/vocab/unique_key_slots').
multivalued(unique_key_slots).
required(unique_key_slots).
slot(unique_keys).
domain(unique_keys, class_definition).
range(unique_keys, unique_key).
has_uri(unique_keys, 'http://w3id.org/biolink/vocab/unique_keys').
multivalued(unique_keys).
slot(usage_slot_name).
domain(usage_slot_name, slot_definition).
range(usage_slot_name, string).
has_uri(usage_slot_name, 'http://w3id.org/biolink/vocab/usage_slot_name').
slot(value).
domain(value, example).
range(value, string).
has_uri(value, 'http://w3id.org/biolink/vocab/value').
slot(description).
domain(description, example).
range(description, string).
has_uri(description, 'http://w3id.org/biolink/vocab/description').
slot(values_from).
domain(values_from, definition).
range(values_from, uriorcurie).
has_uri(values_from, 'http://w3id.org/biolink/vocab/values_from').
multivalued(values_from).
slot(version).
domain(version, schema_definition).
range(version, string).
has_uri(version, 'http://w3id.org/biolink/vocab/version').
class(alt_description).
has_uri(alt_description, 'http://w3id.org/biolink/vocab/AltDescription').
class_slot(alt_description, source).
required(source).
slotrange(string).
required_in(source, alt_description).
range_in(source, string, alt_description).
class_slot(alt_description, description).
required(description).
slotrange(string).
required_in(description, alt_description).
range_in(description, string, alt_description).
class(annotatable).
has_uri(annotatable, 'http://w3id.org/biolink/vocab/Annotatable').
class_slot(annotatable, annotations).
required(annotations).
slotrange(annotation).
multivalued_in(annotations, annotatable).
range_in(annotations, annotation, annotatable).
class(annotation).
mixin(annotation, annotatable).
is_a(annotation, extension).
has_uri(annotation, 'http://w3id.org/biolink/vocab/Annotation').
class_slot(annotation, tag).
required(tag).
slotrange(uriorcurie).
required_in(tag, annotation).
range_in(tag, uriorcurie, annotation).
class_slot(annotation, value).
required(value).
slotrange(string).
required_in(value, annotation).
range_in(value, string, annotation).
class_slot(annotation, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, annotation).
range_in(extensions, extension, annotation).
class_slot(annotation, annotations).
required(annotations).
slotrange(annotation).
multivalued_in(annotations, annotation).
range_in(annotations, annotation, annotation).
class(class_definition).
is_a(class_definition, definition).
has_uri(class_definition, 'http://w3id.org/biolink/vocab/ClassDefinition').
class_slot(class_definition, name).
required(name).
slotrange(string).
required_in(name, class_definition).
range_in(name, string, class_definition).
class_slot(class_definition, title).
required(title).
slotrange(string).
range_in(title, string, class_definition).
class_slot(class_definition, id_prefixes).
required(id_prefixes).
slotrange(ncname).
multivalued_in(id_prefixes, class_definition).
range_in(id_prefixes, ncname, class_definition).
class_slot(class_definition, definition_uri).
required(definition_uri).
slotrange(uriorcurie).
range_in(definition_uri, uriorcurie, class_definition).
class_slot(class_definition, aliases).
required(aliases).
slotrange(string).
multivalued_in(aliases, class_definition).
range_in(aliases, string, class_definition).
class_slot(class_definition, local_names).
required(local_names).
slotrange(local_name).
multivalued_in(local_names, class_definition).
range_in(local_names, local_name, class_definition).
class_slot(class_definition, mappings).
required(mappings).
slotrange(uriorcurie).
multivalued_in(mappings, class_definition).
range_in(mappings, uriorcurie, class_definition).
class_slot(class_definition, exact_mappings).
required(exact_mappings).
slotrange(uriorcurie).
multivalued_in(exact_mappings, class_definition).
range_in(exact_mappings, uriorcurie, class_definition).
class_slot(class_definition, close_mappings).
required(close_mappings).
slotrange(uriorcurie).
multivalued_in(close_mappings, class_definition).
range_in(close_mappings, uriorcurie, class_definition).
class_slot(class_definition, related_mappings).
required(related_mappings).
slotrange(uriorcurie).
multivalued_in(related_mappings, class_definition).
range_in(related_mappings, uriorcurie, class_definition).
class_slot(class_definition, narrow_mappings).
required(narrow_mappings).
slotrange(uriorcurie).
multivalued_in(narrow_mappings, class_definition).
range_in(narrow_mappings, uriorcurie, class_definition).
class_slot(class_definition, broad_mappings).
required(broad_mappings).
slotrange(uriorcurie).
multivalued_in(broad_mappings, class_definition).
range_in(broad_mappings, uriorcurie, class_definition).
class_slot(class_definition, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, class_definition).
range_in(extensions, extension, class_definition).
class_slot(class_definition, annotations).
required(annotations).
slotrange(annotation).
multivalued_in(annotations, class_definition).
range_in(annotations, annotation, class_definition).
class_slot(class_definition, description).
required(description).
slotrange(string).
range_in(description, string, class_definition).
class_slot(class_definition, alt_descriptions).
required(alt_descriptions).
slotrange(alt_description).
multivalued_in(alt_descriptions, class_definition).
range_in(alt_descriptions, alt_description, class_definition).
class_slot(class_definition, deprecated).
required(deprecated).
slotrange(string).
range_in(deprecated, string, class_definition).
class_slot(class_definition, todos).
required(todos).
slotrange(string).
multivalued_in(todos, class_definition).
range_in(todos, string, class_definition).
class_slot(class_definition, notes).
required(notes).
slotrange(string).
multivalued_in(notes, class_definition).
range_in(notes, string, class_definition).
class_slot(class_definition, comments).
required(comments).
slotrange(string).
multivalued_in(comments, class_definition).
range_in(comments, string, class_definition).
class_slot(class_definition, examples).
required(examples).
slotrange(example).
multivalued_in(examples, class_definition).
range_in(examples, example, class_definition).
class_slot(class_definition, in_subset).
required(in_subset).
slotrange(subset_definition).
multivalued_in(in_subset, class_definition).
range_in(in_subset, subset_definition, class_definition).
class_slot(class_definition, from_schema).
required(from_schema).
slotrange(uri).
range_in(from_schema, uri, class_definition).
class_slot(class_definition, imported_from).
required(imported_from).
slotrange(string).
range_in(imported_from, string, class_definition).
class_slot(class_definition, see_also).
required(see_also).
slotrange(uriorcurie).
multivalued_in(see_also, class_definition).
range_in(see_also, uriorcurie, class_definition).
class_slot(class_definition, deprecated_element_has_exact_replacement).
required(deprecated_element_has_exact_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_exact_replacement, uriorcurie, class_definition).
class_slot(class_definition, deprecated_element_has_possible_replacement).
required(deprecated_element_has_possible_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_possible_replacement, uriorcurie, class_definition).
class_slot(class_definition, abstract).
required(abstract).
slotrange(boolean).
range_in(abstract, boolean, class_definition).
class_slot(class_definition, mixin).
required(mixin).
slotrange(boolean).
range_in(mixin, boolean, class_definition).
class_slot(class_definition, values_from).
required(values_from).
slotrange(uriorcurie).
multivalued_in(values_from, class_definition).
range_in(values_from, uriorcurie, class_definition).
class_slot(class_definition, created_by).
required(created_by).
slotrange(uriorcurie).
range_in(created_by, uriorcurie, class_definition).
class_slot(class_definition, created_on).
required(created_on).
slotrange(datetime).
range_in(created_on, datetime, class_definition).
class_slot(class_definition, last_updated_on).
required(last_updated_on).
slotrange(datetime).
range_in(last_updated_on, datetime, class_definition).
class_slot(class_definition, modified_by).
required(modified_by).
slotrange(uriorcurie).
range_in(modified_by, uriorcurie, class_definition).
class_slot(class_definition, status).
required(status).
slotrange(uriorcurie).
range_in(status, uriorcurie, class_definition).
class_slot(class_definition, string_serialization).
required(string_serialization).
slotrange(string).
range_in(string_serialization, string, class_definition).
class_slot(class_definition, slots).
required(slots).
slotrange(slot_definition).
multivalued_in(slots, class_definition).
range_in(slots, slot_definition, class_definition).
class_slot(class_definition, slot_usage).
required(slot_usage).
slotrange(slot_definition).
multivalued_in(slot_usage, class_definition).
range_in(slot_usage, slot_definition, class_definition).
class_slot(class_definition, attributes).
required(attributes).
slotrange(slot_definition).
multivalued_in(attributes, class_definition).
range_in(attributes, slot_definition, class_definition).
class_slot(class_definition, class_uri).
required(class_uri).
slotrange(uriorcurie).
range_in(class_uri, uriorcurie, class_definition).
class_slot(class_definition, subclass_of).
required(subclass_of).
slotrange(uriorcurie).
range_in(subclass_of, uriorcurie, class_definition).
class_slot(class_definition, union_of).
required(union_of).
slotrange(class_definition).
multivalued_in(union_of, class_definition).
range_in(union_of, class_definition, class_definition).
class_slot(class_definition, defining_slots).
required(defining_slots).
slotrange(slot_definition).
multivalued_in(defining_slots, class_definition).
range_in(defining_slots, slot_definition, class_definition).
class_slot(class_definition, tree_root).
required(tree_root).
slotrange(boolean).
range_in(tree_root, boolean, class_definition).
class_slot(class_definition, is_a).
required(is_a).
slotrange(class_definition).
range_in(is_a, class_definition, class_definition).
class_slot(class_definition, mixins).
required(mixins).
slotrange(class_definition).
multivalued_in(mixins, class_definition).
range_in(mixins, class_definition, class_definition).
class_slot(class_definition, apply_to).
required(apply_to).
slotrange(class_definition).
multivalued_in(apply_to, class_definition).
range_in(apply_to, class_definition, class_definition).
class(common_metadata).
has_uri(common_metadata, 'http://w3id.org/biolink/vocab/CommonMetadata').
class_slot(common_metadata, description).
required(description).
slotrange(string).
range_in(description, string, common_metadata).
class_slot(common_metadata, alt_descriptions).
required(alt_descriptions).
slotrange(alt_description).
multivalued_in(alt_descriptions, common_metadata).
range_in(alt_descriptions, alt_description, common_metadata).
class_slot(common_metadata, deprecated).
required(deprecated).
slotrange(string).
range_in(deprecated, string, common_metadata).
class_slot(common_metadata, todos).
required(todos).
slotrange(string).
multivalued_in(todos, common_metadata).
range_in(todos, string, common_metadata).
class_slot(common_metadata, notes).
required(notes).
slotrange(string).
multivalued_in(notes, common_metadata).
range_in(notes, string, common_metadata).
class_slot(common_metadata, comments).
required(comments).
slotrange(string).
multivalued_in(comments, common_metadata).
range_in(comments, string, common_metadata).
class_slot(common_metadata, examples).
required(examples).
slotrange(example).
multivalued_in(examples, common_metadata).
range_in(examples, example, common_metadata).
class_slot(common_metadata, in_subset).
required(in_subset).
slotrange(subset_definition).
multivalued_in(in_subset, common_metadata).
range_in(in_subset, subset_definition, common_metadata).
class_slot(common_metadata, from_schema).
required(from_schema).
slotrange(uri).
range_in(from_schema, uri, common_metadata).
class_slot(common_metadata, imported_from).
required(imported_from).
slotrange(string).
range_in(imported_from, string, common_metadata).
class_slot(common_metadata, see_also).
required(see_also).
slotrange(uriorcurie).
multivalued_in(see_also, common_metadata).
range_in(see_also, uriorcurie, common_metadata).
class_slot(common_metadata, deprecated_element_has_exact_replacement).
required(deprecated_element_has_exact_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_exact_replacement, uriorcurie, common_metadata).
class_slot(common_metadata, deprecated_element_has_possible_replacement).
required(deprecated_element_has_possible_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_possible_replacement, uriorcurie, common_metadata).
class(definition).
is_a(definition, element).
has_uri(definition, 'http://w3id.org/biolink/vocab/Definition').
class_slot(definition, name).
required(name).
slotrange(string).
required_in(name, definition).
range_in(name, string, definition).
class_slot(definition, title).
required(title).
slotrange(string).
range_in(title, string, definition).
class_slot(definition, id_prefixes).
required(id_prefixes).
slotrange(ncname).
multivalued_in(id_prefixes, definition).
range_in(id_prefixes, ncname, definition).
class_slot(definition, definition_uri).
required(definition_uri).
slotrange(uriorcurie).
range_in(definition_uri, uriorcurie, definition).
class_slot(definition, aliases).
required(aliases).
slotrange(string).
multivalued_in(aliases, definition).
range_in(aliases, string, definition).
class_slot(definition, local_names).
required(local_names).
slotrange(local_name).
multivalued_in(local_names, definition).
range_in(local_names, local_name, definition).
class_slot(definition, mappings).
required(mappings).
slotrange(uriorcurie).
multivalued_in(mappings, definition).
range_in(mappings, uriorcurie, definition).
class_slot(definition, exact_mappings).
required(exact_mappings).
slotrange(uriorcurie).
multivalued_in(exact_mappings, definition).
range_in(exact_mappings, uriorcurie, definition).
class_slot(definition, close_mappings).
required(close_mappings).
slotrange(uriorcurie).
multivalued_in(close_mappings, definition).
range_in(close_mappings, uriorcurie, definition).
class_slot(definition, related_mappings).
required(related_mappings).
slotrange(uriorcurie).
multivalued_in(related_mappings, definition).
range_in(related_mappings, uriorcurie, definition).
class_slot(definition, narrow_mappings).
required(narrow_mappings).
slotrange(uriorcurie).
multivalued_in(narrow_mappings, definition).
range_in(narrow_mappings, uriorcurie, definition).
class_slot(definition, broad_mappings).
required(broad_mappings).
slotrange(uriorcurie).
multivalued_in(broad_mappings, definition).
range_in(broad_mappings, uriorcurie, definition).
class_slot(definition, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, definition).
range_in(extensions, extension, definition).
class_slot(definition, annotations).
required(annotations).
slotrange(annotation).
multivalued_in(annotations, definition).
range_in(annotations, annotation, definition).
class_slot(definition, description).
required(description).
slotrange(string).
range_in(description, string, definition).
class_slot(definition, alt_descriptions).
required(alt_descriptions).
slotrange(alt_description).
multivalued_in(alt_descriptions, definition).
range_in(alt_descriptions, alt_description, definition).
class_slot(definition, deprecated).
required(deprecated).
slotrange(string).
range_in(deprecated, string, definition).
class_slot(definition, todos).
required(todos).
slotrange(string).
multivalued_in(todos, definition).
range_in(todos, string, definition).
class_slot(definition, notes).
required(notes).
slotrange(string).
multivalued_in(notes, definition).
range_in(notes, string, definition).
class_slot(definition, comments).
required(comments).
slotrange(string).
multivalued_in(comments, definition).
range_in(comments, string, definition).
class_slot(definition, examples).
required(examples).
slotrange(example).
multivalued_in(examples, definition).
range_in(examples, example, definition).
class_slot(definition, in_subset).
required(in_subset).
slotrange(subset_definition).
multivalued_in(in_subset, definition).
range_in(in_subset, subset_definition, definition).
class_slot(definition, from_schema).
required(from_schema).
slotrange(uri).
range_in(from_schema, uri, definition).
class_slot(definition, imported_from).
required(imported_from).
slotrange(string).
range_in(imported_from, string, definition).
class_slot(definition, see_also).
required(see_also).
slotrange(uriorcurie).
multivalued_in(see_also, definition).
range_in(see_also, uriorcurie, definition).
class_slot(definition, deprecated_element_has_exact_replacement).
required(deprecated_element_has_exact_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_exact_replacement, uriorcurie, definition).
class_slot(definition, deprecated_element_has_possible_replacement).
required(deprecated_element_has_possible_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_possible_replacement, uriorcurie, definition).
class_slot(definition, is_a).
required(is_a).
slotrange(definition).
range_in(is_a, definition, definition).
class_slot(definition, abstract).
required(abstract).
slotrange(boolean).
range_in(abstract, boolean, definition).
class_slot(definition, mixin).
required(mixin).
slotrange(boolean).
range_in(mixin, boolean, definition).
class_slot(definition, mixins).
required(mixins).
slotrange(definition).
multivalued_in(mixins, definition).
range_in(mixins, definition, definition).
class_slot(definition, apply_to).
required(apply_to).
slotrange(definition).
multivalued_in(apply_to, definition).
range_in(apply_to, definition, definition).
class_slot(definition, values_from).
required(values_from).
slotrange(uriorcurie).
multivalued_in(values_from, definition).
range_in(values_from, uriorcurie, definition).
class_slot(definition, created_by).
required(created_by).
slotrange(uriorcurie).
range_in(created_by, uriorcurie, definition).
class_slot(definition, created_on).
required(created_on).
slotrange(datetime).
range_in(created_on, datetime, definition).
class_slot(definition, last_updated_on).
required(last_updated_on).
slotrange(datetime).
range_in(last_updated_on, datetime, definition).
class_slot(definition, modified_by).
required(modified_by).
slotrange(uriorcurie).
range_in(modified_by, uriorcurie, definition).
class_slot(definition, status).
required(status).
slotrange(uriorcurie).
range_in(status, uriorcurie, definition).
class_slot(definition, string_serialization).
required(string_serialization).
slotrange(string).
range_in(string_serialization, string, definition).
class(element).
mixin(element, extensible).
mixin(element, annotatable).
mixin(element, common_metadata).
has_uri(element, 'http://w3id.org/biolink/vocab/Element').
class_slot(element, name).
required(name).
slotrange(string).
required_in(name, element).
range_in(name, string, element).
class_slot(element, title).
required(title).
slotrange(string).
range_in(title, string, element).
class_slot(element, id_prefixes).
required(id_prefixes).
slotrange(ncname).
multivalued_in(id_prefixes, element).
range_in(id_prefixes, ncname, element).
class_slot(element, definition_uri).
required(definition_uri).
slotrange(uriorcurie).
range_in(definition_uri, uriorcurie, element).
class_slot(element, aliases).
required(aliases).
slotrange(string).
multivalued_in(aliases, element).
range_in(aliases, string, element).
class_slot(element, local_names).
required(local_names).
slotrange(local_name).
multivalued_in(local_names, element).
range_in(local_names, local_name, element).
class_slot(element, mappings).
required(mappings).
slotrange(uriorcurie).
multivalued_in(mappings, element).
range_in(mappings, uriorcurie, element).
class_slot(element, exact_mappings).
required(exact_mappings).
slotrange(uriorcurie).
multivalued_in(exact_mappings, element).
range_in(exact_mappings, uriorcurie, element).
class_slot(element, close_mappings).
required(close_mappings).
slotrange(uriorcurie).
multivalued_in(close_mappings, element).
range_in(close_mappings, uriorcurie, element).
class_slot(element, related_mappings).
required(related_mappings).
slotrange(uriorcurie).
multivalued_in(related_mappings, element).
range_in(related_mappings, uriorcurie, element).
class_slot(element, narrow_mappings).
required(narrow_mappings).
slotrange(uriorcurie).
multivalued_in(narrow_mappings, element).
range_in(narrow_mappings, uriorcurie, element).
class_slot(element, broad_mappings).
required(broad_mappings).
slotrange(uriorcurie).
multivalued_in(broad_mappings, element).
range_in(broad_mappings, uriorcurie, element).
class_slot(element, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, element).
range_in(extensions, extension, element).
class_slot(element, annotations).
required(annotations).
slotrange(annotation).
multivalued_in(annotations, element).
range_in(annotations, annotation, element).
class_slot(element, description).
required(description).
slotrange(string).
range_in(description, string, element).
class_slot(element, alt_descriptions).
required(alt_descriptions).
slotrange(alt_description).
multivalued_in(alt_descriptions, element).
range_in(alt_descriptions, alt_description, element).
class_slot(element, deprecated).
required(deprecated).
slotrange(string).
range_in(deprecated, string, element).
class_slot(element, todos).
required(todos).
slotrange(string).
multivalued_in(todos, element).
range_in(todos, string, element).
class_slot(element, notes).
required(notes).
slotrange(string).
multivalued_in(notes, element).
range_in(notes, string, element).
class_slot(element, comments).
required(comments).
slotrange(string).
multivalued_in(comments, element).
range_in(comments, string, element).
class_slot(element, examples).
required(examples).
slotrange(example).
multivalued_in(examples, element).
range_in(examples, example, element).
class_slot(element, in_subset).
required(in_subset).
slotrange(subset_definition).
multivalued_in(in_subset, element).
range_in(in_subset, subset_definition, element).
class_slot(element, from_schema).
required(from_schema).
slotrange(uri).
range_in(from_schema, uri, element).
class_slot(element, imported_from).
required(imported_from).
slotrange(string).
range_in(imported_from, string, element).
class_slot(element, see_also).
required(see_also).
slotrange(uriorcurie).
multivalued_in(see_also, element).
range_in(see_also, uriorcurie, element).
class_slot(element, deprecated_element_has_exact_replacement).
required(deprecated_element_has_exact_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_exact_replacement, uriorcurie, element).
class_slot(element, deprecated_element_has_possible_replacement).
required(deprecated_element_has_possible_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_possible_replacement, uriorcurie, element).
class(enum_definition).
is_a(enum_definition, element).
has_uri(enum_definition, 'http://w3id.org/biolink/vocab/EnumDefinition').
class_slot(enum_definition, name).
required(name).
slotrange(string).
required_in(name, enum_definition).
range_in(name, string, enum_definition).
class_slot(enum_definition, title).
required(title).
slotrange(string).
range_in(title, string, enum_definition).
class_slot(enum_definition, id_prefixes).
required(id_prefixes).
slotrange(ncname).
multivalued_in(id_prefixes, enum_definition).
range_in(id_prefixes, ncname, enum_definition).
class_slot(enum_definition, definition_uri).
required(definition_uri).
slotrange(uriorcurie).
range_in(definition_uri, uriorcurie, enum_definition).
class_slot(enum_definition, aliases).
required(aliases).
slotrange(string).
multivalued_in(aliases, enum_definition).
range_in(aliases, string, enum_definition).
class_slot(enum_definition, local_names).
required(local_names).
slotrange(local_name).
multivalued_in(local_names, enum_definition).
range_in(local_names, local_name, enum_definition).
class_slot(enum_definition, mappings).
required(mappings).
slotrange(uriorcurie).
multivalued_in(mappings, enum_definition).
range_in(mappings, uriorcurie, enum_definition).
class_slot(enum_definition, exact_mappings).
required(exact_mappings).
slotrange(uriorcurie).
multivalued_in(exact_mappings, enum_definition).
range_in(exact_mappings, uriorcurie, enum_definition).
class_slot(enum_definition, close_mappings).
required(close_mappings).
slotrange(uriorcurie).
multivalued_in(close_mappings, enum_definition).
range_in(close_mappings, uriorcurie, enum_definition).
class_slot(enum_definition, related_mappings).
required(related_mappings).
slotrange(uriorcurie).
multivalued_in(related_mappings, enum_definition).
range_in(related_mappings, uriorcurie, enum_definition).
class_slot(enum_definition, narrow_mappings).
required(narrow_mappings).
slotrange(uriorcurie).
multivalued_in(narrow_mappings, enum_definition).
range_in(narrow_mappings, uriorcurie, enum_definition).
class_slot(enum_definition, broad_mappings).
required(broad_mappings).
slotrange(uriorcurie).
multivalued_in(broad_mappings, enum_definition).
range_in(broad_mappings, uriorcurie, enum_definition).
class_slot(enum_definition, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, enum_definition).
range_in(extensions, extension, enum_definition).
class_slot(enum_definition, annotations).
required(annotations).
slotrange(annotation).
multivalued_in(annotations, enum_definition).
range_in(annotations, annotation, enum_definition).
class_slot(enum_definition, description).
required(description).
slotrange(string).
range_in(description, string, enum_definition).
class_slot(enum_definition, alt_descriptions).
required(alt_descriptions).
slotrange(alt_description).
multivalued_in(alt_descriptions, enum_definition).
range_in(alt_descriptions, alt_description, enum_definition).
class_slot(enum_definition, deprecated).
required(deprecated).
slotrange(string).
range_in(deprecated, string, enum_definition).
class_slot(enum_definition, todos).
required(todos).
slotrange(string).
multivalued_in(todos, enum_definition).
range_in(todos, string, enum_definition).
class_slot(enum_definition, notes).
required(notes).
slotrange(string).
multivalued_in(notes, enum_definition).
range_in(notes, string, enum_definition).
class_slot(enum_definition, comments).
required(comments).
slotrange(string).
multivalued_in(comments, enum_definition).
range_in(comments, string, enum_definition).
class_slot(enum_definition, examples).
required(examples).
slotrange(example).
multivalued_in(examples, enum_definition).
range_in(examples, example, enum_definition).
class_slot(enum_definition, in_subset).
required(in_subset).
slotrange(subset_definition).
multivalued_in(in_subset, enum_definition).
range_in(in_subset, subset_definition, enum_definition).
class_slot(enum_definition, from_schema).
required(from_schema).
slotrange(uri).
range_in(from_schema, uri, enum_definition).
class_slot(enum_definition, imported_from).
required(imported_from).
slotrange(string).
range_in(imported_from, string, enum_definition).
class_slot(enum_definition, see_also).
required(see_also).
slotrange(uriorcurie).
multivalued_in(see_also, enum_definition).
range_in(see_also, uriorcurie, enum_definition).
class_slot(enum_definition, deprecated_element_has_exact_replacement).
required(deprecated_element_has_exact_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_exact_replacement, uriorcurie, enum_definition).
class_slot(enum_definition, deprecated_element_has_possible_replacement).
required(deprecated_element_has_possible_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_possible_replacement, uriorcurie, enum_definition).
class_slot(enum_definition, code_set).
required(code_set).
slotrange(uriorcurie).
range_in(code_set, uriorcurie, enum_definition).
class_slot(enum_definition, code_set_tag).
required(code_set_tag).
slotrange(string).
range_in(code_set_tag, string, enum_definition).
class_slot(enum_definition, code_set_version).
required(code_set_version).
slotrange(string).
range_in(code_set_version, string, enum_definition).
class_slot(enum_definition, pv_formula).
required(pv_formula).
slotrange(pv_formula_options).
range_in(pv_formula, pv_formula_options, enum_definition).
class_slot(enum_definition, permissible_values).
required(permissible_values).
slotrange(permissible_value).
multivalued_in(permissible_values, enum_definition).
range_in(permissible_values, permissible_value, enum_definition).
class(example).
has_uri(example, 'http://w3id.org/biolink/vocab/Example').
class_slot(example, value).
required(value).
slotrange(string).
range_in(value, string, example).
class_slot(example, description).
required(description).
slotrange(string).
range_in(description, string, example).
class(extensible).
has_uri(extensible, 'http://w3id.org/biolink/vocab/Extensible').
class_slot(extensible, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, extensible).
range_in(extensions, extension, extensible).
class(extension).
has_uri(extension, 'http://w3id.org/biolink/vocab/Extension').
class_slot(extension, tag).
required(tag).
slotrange(uriorcurie).
required_in(tag, extension).
range_in(tag, uriorcurie, extension).
class_slot(extension, value).
required(value).
slotrange(string).
required_in(value, extension).
range_in(value, string, extension).
class_slot(extension, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, extension).
range_in(extensions, extension, extension).
class(local_name).
has_uri(local_name, 'http://w3id.org/biolink/vocab/LocalName').
class_slot(local_name, local_name_source).
required(local_name_source).
slotrange(ncname).
required_in(local_name_source, local_name).
range_in(local_name_source, ncname, local_name).
class_slot(local_name, local_name_value).
required(local_name_value).
slotrange(string).
required_in(local_name_value, local_name).
range_in(local_name_value, string, local_name).
class(permissible_value).
mixin(permissible_value, extensible).
mixin(permissible_value, annotatable).
mixin(permissible_value, common_metadata).
has_uri(permissible_value, 'http://w3id.org/biolink/vocab/PermissibleValue').
class_slot(permissible_value, text).
required(text).
slotrange(string).
required_in(text, permissible_value).
range_in(text, string, permissible_value).
class_slot(permissible_value, description).
required(description).
slotrange(string).
range_in(description, string, permissible_value).
class_slot(permissible_value, meaning).
required(meaning).
slotrange(uriorcurie).
range_in(meaning, uriorcurie, permissible_value).
class_slot(permissible_value, is_a).
required(is_a).
slotrange(permissible_value).
range_in(is_a, permissible_value, permissible_value).
class_slot(permissible_value, mixins).
required(mixins).
slotrange(permissible_value).
multivalued_in(mixins, permissible_value).
range_in(mixins, permissible_value, permissible_value).
class_slot(permissible_value, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, permissible_value).
range_in(extensions, extension, permissible_value).
class_slot(permissible_value, annotations).
required(annotations).
slotrange(annotation).
multivalued_in(annotations, permissible_value).
range_in(annotations, annotation, permissible_value).
class_slot(permissible_value, alt_descriptions).
required(alt_descriptions).
slotrange(alt_description).
multivalued_in(alt_descriptions, permissible_value).
range_in(alt_descriptions, alt_description, permissible_value).
class_slot(permissible_value, deprecated).
required(deprecated).
slotrange(string).
range_in(deprecated, string, permissible_value).
class_slot(permissible_value, todos).
required(todos).
slotrange(string).
multivalued_in(todos, permissible_value).
range_in(todos, string, permissible_value).
class_slot(permissible_value, notes).
required(notes).
slotrange(string).
multivalued_in(notes, permissible_value).
range_in(notes, string, permissible_value).
class_slot(permissible_value, comments).
required(comments).
slotrange(string).
multivalued_in(comments, permissible_value).
range_in(comments, string, permissible_value).
class_slot(permissible_value, examples).
required(examples).
slotrange(example).
multivalued_in(examples, permissible_value).
range_in(examples, example, permissible_value).
class_slot(permissible_value, in_subset).
required(in_subset).
slotrange(subset_definition).
multivalued_in(in_subset, permissible_value).
range_in(in_subset, subset_definition, permissible_value).
class_slot(permissible_value, from_schema).
required(from_schema).
slotrange(uri).
range_in(from_schema, uri, permissible_value).
class_slot(permissible_value, imported_from).
required(imported_from).
slotrange(string).
range_in(imported_from, string, permissible_value).
class_slot(permissible_value, see_also).
required(see_also).
slotrange(uriorcurie).
multivalued_in(see_also, permissible_value).
range_in(see_also, uriorcurie, permissible_value).
class_slot(permissible_value, deprecated_element_has_exact_replacement).
required(deprecated_element_has_exact_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_exact_replacement, uriorcurie, permissible_value).
class_slot(permissible_value, deprecated_element_has_possible_replacement).
required(deprecated_element_has_possible_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_possible_replacement, uriorcurie, permissible_value).
class(prefix).
has_uri(prefix, 'http://w3id.org/biolink/vocab/Prefix').
class_slot(prefix, prefix_prefix).
required(prefix_prefix).
slotrange(ncname).
required_in(prefix_prefix, prefix).
range_in(prefix_prefix, ncname, prefix).
class_slot(prefix, prefix_reference).
required(prefix_reference).
slotrange(uri).
required_in(prefix_reference, prefix).
range_in(prefix_reference, uri, prefix).
class(schema_definition).
is_a(schema_definition, element).
has_uri(schema_definition, 'http://w3id.org/biolink/vocab/SchemaDefinition').
class_slot(schema_definition, title).
required(title).
slotrange(string).
range_in(title, string, schema_definition).
class_slot(schema_definition, id_prefixes).
required(id_prefixes).
slotrange(ncname).
multivalued_in(id_prefixes, schema_definition).
range_in(id_prefixes, ncname, schema_definition).
class_slot(schema_definition, definition_uri).
required(definition_uri).
slotrange(uriorcurie).
range_in(definition_uri, uriorcurie, schema_definition).
class_slot(schema_definition, aliases).
required(aliases).
slotrange(string).
multivalued_in(aliases, schema_definition).
range_in(aliases, string, schema_definition).
class_slot(schema_definition, local_names).
required(local_names).
slotrange(local_name).
multivalued_in(local_names, schema_definition).
range_in(local_names, local_name, schema_definition).
class_slot(schema_definition, mappings).
required(mappings).
slotrange(uriorcurie).
multivalued_in(mappings, schema_definition).
range_in(mappings, uriorcurie, schema_definition).
class_slot(schema_definition, exact_mappings).
required(exact_mappings).
slotrange(uriorcurie).
multivalued_in(exact_mappings, schema_definition).
range_in(exact_mappings, uriorcurie, schema_definition).
class_slot(schema_definition, close_mappings).
required(close_mappings).
slotrange(uriorcurie).
multivalued_in(close_mappings, schema_definition).
range_in(close_mappings, uriorcurie, schema_definition).
class_slot(schema_definition, related_mappings).
required(related_mappings).
slotrange(uriorcurie).
multivalued_in(related_mappings, schema_definition).
range_in(related_mappings, uriorcurie, schema_definition).
class_slot(schema_definition, narrow_mappings).
required(narrow_mappings).
slotrange(uriorcurie).
multivalued_in(narrow_mappings, schema_definition).
range_in(narrow_mappings, uriorcurie, schema_definition).
class_slot(schema_definition, broad_mappings).
required(broad_mappings).
slotrange(uriorcurie).
multivalued_in(broad_mappings, schema_definition).
range_in(broad_mappings, uriorcurie, schema_definition).
class_slot(schema_definition, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, schema_definition).
range_in(extensions, extension, schema_definition).
class_slot(schema_definition, annotations).
required(annotations).
slotrange(annotation).
multivalued_in(annotations, schema_definition).
range_in(annotations, annotation, schema_definition).
class_slot(schema_definition, description).
required(description).
slotrange(string).
range_in(description, string, schema_definition).
class_slot(schema_definition, alt_descriptions).
required(alt_descriptions).
slotrange(alt_description).
multivalued_in(alt_descriptions, schema_definition).
range_in(alt_descriptions, alt_description, schema_definition).
class_slot(schema_definition, deprecated).
required(deprecated).
slotrange(string).
range_in(deprecated, string, schema_definition).
class_slot(schema_definition, todos).
required(todos).
slotrange(string).
multivalued_in(todos, schema_definition).
range_in(todos, string, schema_definition).
class_slot(schema_definition, notes).
required(notes).
slotrange(string).
multivalued_in(notes, schema_definition).
range_in(notes, string, schema_definition).
class_slot(schema_definition, comments).
required(comments).
slotrange(string).
multivalued_in(comments, schema_definition).
range_in(comments, string, schema_definition).
class_slot(schema_definition, examples).
required(examples).
slotrange(example).
multivalued_in(examples, schema_definition).
range_in(examples, example, schema_definition).
class_slot(schema_definition, in_subset).
required(in_subset).
slotrange(subset_definition).
multivalued_in(in_subset, schema_definition).
range_in(in_subset, subset_definition, schema_definition).
class_slot(schema_definition, from_schema).
required(from_schema).
slotrange(uri).
range_in(from_schema, uri, schema_definition).
class_slot(schema_definition, imported_from).
required(imported_from).
slotrange(string).
range_in(imported_from, string, schema_definition).
class_slot(schema_definition, see_also).
required(see_also).
slotrange(uriorcurie).
multivalued_in(see_also, schema_definition).
range_in(see_also, uriorcurie, schema_definition).
class_slot(schema_definition, deprecated_element_has_exact_replacement).
required(deprecated_element_has_exact_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_exact_replacement, uriorcurie, schema_definition).
class_slot(schema_definition, deprecated_element_has_possible_replacement).
required(deprecated_element_has_possible_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_possible_replacement, uriorcurie, schema_definition).
class_slot(schema_definition, id).
required(id).
slotrange(uri).
required_in(id, schema_definition).
range_in(id, uri, schema_definition).
class_slot(schema_definition, version).
required(version).
slotrange(string).
range_in(version, string, schema_definition).
class_slot(schema_definition, imports).
required(imports).
slotrange(uriorcurie).
multivalued_in(imports, schema_definition).
range_in(imports, uriorcurie, schema_definition).
class_slot(schema_definition, license).
required(license).
slotrange(string).
range_in(license, string, schema_definition).
class_slot(schema_definition, prefixes).
required(prefixes).
slotrange(prefix).
multivalued_in(prefixes, schema_definition).
range_in(prefixes, prefix, schema_definition).
class_slot(schema_definition, emit_prefixes).
required(emit_prefixes).
slotrange(ncname).
multivalued_in(emit_prefixes, schema_definition).
range_in(emit_prefixes, ncname, schema_definition).
class_slot(schema_definition, default_curi_maps).
required(default_curi_maps).
slotrange(string).
multivalued_in(default_curi_maps, schema_definition).
range_in(default_curi_maps, string, schema_definition).
class_slot(schema_definition, default_prefix).
required(default_prefix).
slotrange(string).
range_in(default_prefix, string, schema_definition).
class_slot(schema_definition, default_range).
required(default_range).
slotrange(type_definition).
range_in(default_range, type_definition, schema_definition).
class_slot(schema_definition, subsets).
required(subsets).
slotrange(subset_definition).
multivalued_in(subsets, schema_definition).
range_in(subsets, subset_definition, schema_definition).
class_slot(schema_definition, types).
required(types).
slotrange(type_definition).
multivalued_in(types, schema_definition).
range_in(types, type_definition, schema_definition).
class_slot(schema_definition, enums).
required(enums).
slotrange(enum_definition).
multivalued_in(enums, schema_definition).
range_in(enums, enum_definition, schema_definition).
class_slot(schema_definition, slots).
required(slots).
slotrange(slot_definition).
multivalued_in(slots, schema_definition).
range_in(slots, slot_definition, schema_definition).
class_slot(schema_definition, classes).
required(classes).
slotrange(class_definition).
multivalued_in(classes, schema_definition).
range_in(classes, class_definition, schema_definition).
class_slot(schema_definition, metamodel_version).
required(metamodel_version).
slotrange(string).
range_in(metamodel_version, string, schema_definition).
class_slot(schema_definition, source_file).
required(source_file).
slotrange(string).
range_in(source_file, string, schema_definition).
class_slot(schema_definition, source_file_date).
required(source_file_date).
slotrange(datetime).
range_in(source_file_date, datetime, schema_definition).
class_slot(schema_definition, source_file_size).
required(source_file_size).
slotrange(integer).
range_in(source_file_size, integer, schema_definition).
class_slot(schema_definition, generation_date).
required(generation_date).
slotrange(datetime).
range_in(generation_date, datetime, schema_definition).
class_slot(schema_definition, name).
required(name).
slotrange(ncname).
required_in(name, schema_definition).
range_in(name, ncname, schema_definition).
class(slot_definition).
is_a(slot_definition, definition).
has_uri(slot_definition, 'http://w3id.org/biolink/vocab/SlotDefinition').
class_slot(slot_definition, name).
required(name).
slotrange(string).
required_in(name, slot_definition).
range_in(name, string, slot_definition).
class_slot(slot_definition, title).
required(title).
slotrange(string).
range_in(title, string, slot_definition).
class_slot(slot_definition, id_prefixes).
required(id_prefixes).
slotrange(ncname).
multivalued_in(id_prefixes, slot_definition).
range_in(id_prefixes, ncname, slot_definition).
class_slot(slot_definition, definition_uri).
required(definition_uri).
slotrange(uriorcurie).
range_in(definition_uri, uriorcurie, slot_definition).
class_slot(slot_definition, aliases).
required(aliases).
slotrange(string).
multivalued_in(aliases, slot_definition).
range_in(aliases, string, slot_definition).
class_slot(slot_definition, local_names).
required(local_names).
slotrange(local_name).
multivalued_in(local_names, slot_definition).
range_in(local_names, local_name, slot_definition).
class_slot(slot_definition, mappings).
required(mappings).
slotrange(uriorcurie).
multivalued_in(mappings, slot_definition).
range_in(mappings, uriorcurie, slot_definition).
class_slot(slot_definition, exact_mappings).
required(exact_mappings).
slotrange(uriorcurie).
multivalued_in(exact_mappings, slot_definition).
range_in(exact_mappings, uriorcurie, slot_definition).
class_slot(slot_definition, close_mappings).
required(close_mappings).
slotrange(uriorcurie).
multivalued_in(close_mappings, slot_definition).
range_in(close_mappings, uriorcurie, slot_definition).
class_slot(slot_definition, related_mappings).
required(related_mappings).
slotrange(uriorcurie).
multivalued_in(related_mappings, slot_definition).
range_in(related_mappings, uriorcurie, slot_definition).
class_slot(slot_definition, narrow_mappings).
required(narrow_mappings).
slotrange(uriorcurie).
multivalued_in(narrow_mappings, slot_definition).
range_in(narrow_mappings, uriorcurie, slot_definition).
class_slot(slot_definition, broad_mappings).
required(broad_mappings).
slotrange(uriorcurie).
multivalued_in(broad_mappings, slot_definition).
range_in(broad_mappings, uriorcurie, slot_definition).
class_slot(slot_definition, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, slot_definition).
range_in(extensions, extension, slot_definition).
class_slot(slot_definition, annotations).
required(annotations).
slotrange(annotation).
multivalued_in(annotations, slot_definition).
range_in(annotations, annotation, slot_definition).
class_slot(slot_definition, description).
required(description).
slotrange(string).
range_in(description, string, slot_definition).
class_slot(slot_definition, alt_descriptions).
required(alt_descriptions).
slotrange(alt_description).
multivalued_in(alt_descriptions, slot_definition).
range_in(alt_descriptions, alt_description, slot_definition).
class_slot(slot_definition, deprecated).
required(deprecated).
slotrange(string).
range_in(deprecated, string, slot_definition).
class_slot(slot_definition, todos).
required(todos).
slotrange(string).
multivalued_in(todos, slot_definition).
range_in(todos, string, slot_definition).
class_slot(slot_definition, notes).
required(notes).
slotrange(string).
multivalued_in(notes, slot_definition).
range_in(notes, string, slot_definition).
class_slot(slot_definition, comments).
required(comments).
slotrange(string).
multivalued_in(comments, slot_definition).
range_in(comments, string, slot_definition).
class_slot(slot_definition, examples).
required(examples).
slotrange(example).
multivalued_in(examples, slot_definition).
range_in(examples, example, slot_definition).
class_slot(slot_definition, in_subset).
required(in_subset).
slotrange(subset_definition).
multivalued_in(in_subset, slot_definition).
range_in(in_subset, subset_definition, slot_definition).
class_slot(slot_definition, from_schema).
required(from_schema).
slotrange(uri).
range_in(from_schema, uri, slot_definition).
class_slot(slot_definition, imported_from).
required(imported_from).
slotrange(string).
range_in(imported_from, string, slot_definition).
class_slot(slot_definition, see_also).
required(see_also).
slotrange(uriorcurie).
multivalued_in(see_also, slot_definition).
range_in(see_also, uriorcurie, slot_definition).
class_slot(slot_definition, deprecated_element_has_exact_replacement).
required(deprecated_element_has_exact_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_exact_replacement, uriorcurie, slot_definition).
class_slot(slot_definition, deprecated_element_has_possible_replacement).
required(deprecated_element_has_possible_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_possible_replacement, uriorcurie, slot_definition).
class_slot(slot_definition, abstract).
required(abstract).
slotrange(boolean).
range_in(abstract, boolean, slot_definition).
class_slot(slot_definition, mixin).
required(mixin).
slotrange(boolean).
range_in(mixin, boolean, slot_definition).
class_slot(slot_definition, values_from).
required(values_from).
slotrange(uriorcurie).
multivalued_in(values_from, slot_definition).
range_in(values_from, uriorcurie, slot_definition).
class_slot(slot_definition, created_by).
required(created_by).
slotrange(uriorcurie).
range_in(created_by, uriorcurie, slot_definition).
class_slot(slot_definition, created_on).
required(created_on).
slotrange(datetime).
range_in(created_on, datetime, slot_definition).
class_slot(slot_definition, last_updated_on).
required(last_updated_on).
slotrange(datetime).
range_in(last_updated_on, datetime, slot_definition).
class_slot(slot_definition, modified_by).
required(modified_by).
slotrange(uriorcurie).
range_in(modified_by, uriorcurie, slot_definition).
class_slot(slot_definition, status).
required(status).
slotrange(uriorcurie).
range_in(status, uriorcurie, slot_definition).
class_slot(slot_definition, string_serialization).
required(string_serialization).
slotrange(string).
range_in(string_serialization, string, slot_definition).
class_slot(slot_definition, singular_name).
required(singular_name).
slotrange(string).
range_in(singular_name, string, slot_definition).
class_slot(slot_definition, domain).
required(domain).
slotrange(class_definition).
range_in(domain, class_definition, slot_definition).
class_slot(slot_definition, range).
required(range).
slotrange(element).
range_in(range, element, slot_definition).
class_slot(slot_definition, slot_uri).
required(slot_uri).
slotrange(uriorcurie).
range_in(slot_uri, uriorcurie, slot_definition).
class_slot(slot_definition, multivalued).
required(multivalued).
slotrange(boolean).
range_in(multivalued, boolean, slot_definition).
class_slot(slot_definition, inherited).
required(inherited).
slotrange(boolean).
range_in(inherited, boolean, slot_definition).
class_slot(slot_definition, readonly).
required(readonly).
slotrange(string).
range_in(readonly, string, slot_definition).
class_slot(slot_definition, ifabsent).
required(ifabsent).
slotrange(string).
range_in(ifabsent, string, slot_definition).
class_slot(slot_definition, required).
required(required).
slotrange(boolean).
range_in(required, boolean, slot_definition).
class_slot(slot_definition, recommended).
required(recommended).
slotrange(boolean).
range_in(recommended, boolean, slot_definition).
class_slot(slot_definition, inlined).
required(inlined).
slotrange(boolean).
range_in(inlined, boolean, slot_definition).
class_slot(slot_definition, inlined_as_list).
required(inlined_as_list).
slotrange(boolean).
range_in(inlined_as_list, boolean, slot_definition).
class_slot(slot_definition, key).
required(key).
slotrange(boolean).
range_in(key, boolean, slot_definition).
class_slot(slot_definition, identifier).
required(identifier).
slotrange(boolean).
range_in(identifier, boolean, slot_definition).
class_slot(slot_definition, designates_type).
required(designates_type).
slotrange(boolean).
range_in(designates_type, boolean, slot_definition).
class_slot(slot_definition, alias).
required(alias).
slotrange(string).
range_in(alias, string, slot_definition).
class_slot(slot_definition, owner).
required(owner).
slotrange(definition).
range_in(owner, definition, slot_definition).
class_slot(slot_definition, domain_of).
required(domain_of).
slotrange(class_definition).
multivalued_in(domain_of, slot_definition).
range_in(domain_of, class_definition, slot_definition).
class_slot(slot_definition, subproperty_of).
required(subproperty_of).
slotrange(slot_definition).
range_in(subproperty_of, slot_definition, slot_definition).
class_slot(slot_definition, symmetric).
required(symmetric).
slotrange(boolean).
range_in(symmetric, boolean, slot_definition).
class_slot(slot_definition, inverse).
required(inverse).
slotrange(slot_definition).
range_in(inverse, slot_definition, slot_definition).
class_slot(slot_definition, is_class_field).
required(is_class_field).
slotrange(boolean).
range_in(is_class_field, boolean, slot_definition).
class_slot(slot_definition, role).
required(role).
slotrange(string).
range_in(role, string, slot_definition).
class_slot(slot_definition, is_usage_slot).
required(is_usage_slot).
slotrange(boolean).
range_in(is_usage_slot, boolean, slot_definition).
class_slot(slot_definition, usage_slot_name).
required(usage_slot_name).
slotrange(string).
range_in(usage_slot_name, string, slot_definition).
class_slot(slot_definition, minimum_value).
required(minimum_value).
slotrange(integer).
range_in(minimum_value, integer, slot_definition).
class_slot(slot_definition, maximum_value).
required(maximum_value).
slotrange(integer).
range_in(maximum_value, integer, slot_definition).
class_slot(slot_definition, pattern).
required(pattern).
slotrange(string).
range_in(pattern, string, slot_definition).
class_slot(slot_definition, is_a).
required(is_a).
slotrange(slot_definition).
range_in(is_a, slot_definition, slot_definition).
class_slot(slot_definition, mixins).
required(mixins).
slotrange(slot_definition).
multivalued_in(mixins, slot_definition).
range_in(mixins, slot_definition, slot_definition).
class_slot(slot_definition, apply_to).
required(apply_to).
slotrange(slot_definition).
multivalued_in(apply_to, slot_definition).
range_in(apply_to, slot_definition, slot_definition).
class(subset_definition).
is_a(subset_definition, element).
has_uri(subset_definition, 'http://w3id.org/biolink/vocab/SubsetDefinition').
class_slot(subset_definition, name).
required(name).
slotrange(string).
required_in(name, subset_definition).
range_in(name, string, subset_definition).
class_slot(subset_definition, title).
required(title).
slotrange(string).
range_in(title, string, subset_definition).
class_slot(subset_definition, id_prefixes).
required(id_prefixes).
slotrange(ncname).
multivalued_in(id_prefixes, subset_definition).
range_in(id_prefixes, ncname, subset_definition).
class_slot(subset_definition, definition_uri).
required(definition_uri).
slotrange(uriorcurie).
range_in(definition_uri, uriorcurie, subset_definition).
class_slot(subset_definition, aliases).
required(aliases).
slotrange(string).
multivalued_in(aliases, subset_definition).
range_in(aliases, string, subset_definition).
class_slot(subset_definition, local_names).
required(local_names).
slotrange(local_name).
multivalued_in(local_names, subset_definition).
range_in(local_names, local_name, subset_definition).
class_slot(subset_definition, mappings).
required(mappings).
slotrange(uriorcurie).
multivalued_in(mappings, subset_definition).
range_in(mappings, uriorcurie, subset_definition).
class_slot(subset_definition, exact_mappings).
required(exact_mappings).
slotrange(uriorcurie).
multivalued_in(exact_mappings, subset_definition).
range_in(exact_mappings, uriorcurie, subset_definition).
class_slot(subset_definition, close_mappings).
required(close_mappings).
slotrange(uriorcurie).
multivalued_in(close_mappings, subset_definition).
range_in(close_mappings, uriorcurie, subset_definition).
class_slot(subset_definition, related_mappings).
required(related_mappings).
slotrange(uriorcurie).
multivalued_in(related_mappings, subset_definition).
range_in(related_mappings, uriorcurie, subset_definition).
class_slot(subset_definition, narrow_mappings).
required(narrow_mappings).
slotrange(uriorcurie).
multivalued_in(narrow_mappings, subset_definition).
range_in(narrow_mappings, uriorcurie, subset_definition).
class_slot(subset_definition, broad_mappings).
required(broad_mappings).
slotrange(uriorcurie).
multivalued_in(broad_mappings, subset_definition).
range_in(broad_mappings, uriorcurie, subset_definition).
class_slot(subset_definition, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, subset_definition).
range_in(extensions, extension, subset_definition).
class_slot(subset_definition, annotations).
required(annotations).
slotrange(annotation).
multivalued_in(annotations, subset_definition).
range_in(annotations, annotation, subset_definition).
class_slot(subset_definition, description).
required(description).
slotrange(string).
range_in(description, string, subset_definition).
class_slot(subset_definition, alt_descriptions).
required(alt_descriptions).
slotrange(alt_description).
multivalued_in(alt_descriptions, subset_definition).
range_in(alt_descriptions, alt_description, subset_definition).
class_slot(subset_definition, deprecated).
required(deprecated).
slotrange(string).
range_in(deprecated, string, subset_definition).
class_slot(subset_definition, todos).
required(todos).
slotrange(string).
multivalued_in(todos, subset_definition).
range_in(todos, string, subset_definition).
class_slot(subset_definition, notes).
required(notes).
slotrange(string).
multivalued_in(notes, subset_definition).
range_in(notes, string, subset_definition).
class_slot(subset_definition, comments).
required(comments).
slotrange(string).
multivalued_in(comments, subset_definition).
range_in(comments, string, subset_definition).
class_slot(subset_definition, examples).
required(examples).
slotrange(example).
multivalued_in(examples, subset_definition).
range_in(examples, example, subset_definition).
class_slot(subset_definition, in_subset).
required(in_subset).
slotrange(subset_definition).
multivalued_in(in_subset, subset_definition).
range_in(in_subset, subset_definition, subset_definition).
class_slot(subset_definition, from_schema).
required(from_schema).
slotrange(uri).
range_in(from_schema, uri, subset_definition).
class_slot(subset_definition, imported_from).
required(imported_from).
slotrange(string).
range_in(imported_from, string, subset_definition).
class_slot(subset_definition, see_also).
required(see_also).
slotrange(uriorcurie).
multivalued_in(see_also, subset_definition).
range_in(see_also, uriorcurie, subset_definition).
class_slot(subset_definition, deprecated_element_has_exact_replacement).
required(deprecated_element_has_exact_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_exact_replacement, uriorcurie, subset_definition).
class_slot(subset_definition, deprecated_element_has_possible_replacement).
required(deprecated_element_has_possible_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_possible_replacement, uriorcurie, subset_definition).
class(type_definition).
is_a(type_definition, element).
has_uri(type_definition, 'http://w3id.org/biolink/vocab/TypeDefinition').
class_slot(type_definition, name).
required(name).
slotrange(string).
required_in(name, type_definition).
range_in(name, string, type_definition).
class_slot(type_definition, title).
required(title).
slotrange(string).
range_in(title, string, type_definition).
class_slot(type_definition, id_prefixes).
required(id_prefixes).
slotrange(ncname).
multivalued_in(id_prefixes, type_definition).
range_in(id_prefixes, ncname, type_definition).
class_slot(type_definition, definition_uri).
required(definition_uri).
slotrange(uriorcurie).
range_in(definition_uri, uriorcurie, type_definition).
class_slot(type_definition, aliases).
required(aliases).
slotrange(string).
multivalued_in(aliases, type_definition).
range_in(aliases, string, type_definition).
class_slot(type_definition, local_names).
required(local_names).
slotrange(local_name).
multivalued_in(local_names, type_definition).
range_in(local_names, local_name, type_definition).
class_slot(type_definition, mappings).
required(mappings).
slotrange(uriorcurie).
multivalued_in(mappings, type_definition).
range_in(mappings, uriorcurie, type_definition).
class_slot(type_definition, exact_mappings).
required(exact_mappings).
slotrange(uriorcurie).
multivalued_in(exact_mappings, type_definition).
range_in(exact_mappings, uriorcurie, type_definition).
class_slot(type_definition, close_mappings).
required(close_mappings).
slotrange(uriorcurie).
multivalued_in(close_mappings, type_definition).
range_in(close_mappings, uriorcurie, type_definition).
class_slot(type_definition, related_mappings).
required(related_mappings).
slotrange(uriorcurie).
multivalued_in(related_mappings, type_definition).
range_in(related_mappings, uriorcurie, type_definition).
class_slot(type_definition, narrow_mappings).
required(narrow_mappings).
slotrange(uriorcurie).
multivalued_in(narrow_mappings, type_definition).
range_in(narrow_mappings, uriorcurie, type_definition).
class_slot(type_definition, broad_mappings).
required(broad_mappings).
slotrange(uriorcurie).
multivalued_in(broad_mappings, type_definition).
range_in(broad_mappings, uriorcurie, type_definition).
class_slot(type_definition, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, type_definition).
range_in(extensions, extension, type_definition).
class_slot(type_definition, annotations).
required(annotations).
slotrange(annotation).
multivalued_in(annotations, type_definition).
range_in(annotations, annotation, type_definition).
class_slot(type_definition, description).
required(description).
slotrange(string).
range_in(description, string, type_definition).
class_slot(type_definition, alt_descriptions).
required(alt_descriptions).
slotrange(alt_description).
multivalued_in(alt_descriptions, type_definition).
range_in(alt_descriptions, alt_description, type_definition).
class_slot(type_definition, deprecated).
required(deprecated).
slotrange(string).
range_in(deprecated, string, type_definition).
class_slot(type_definition, todos).
required(todos).
slotrange(string).
multivalued_in(todos, type_definition).
range_in(todos, string, type_definition).
class_slot(type_definition, notes).
required(notes).
slotrange(string).
multivalued_in(notes, type_definition).
range_in(notes, string, type_definition).
class_slot(type_definition, comments).
required(comments).
slotrange(string).
multivalued_in(comments, type_definition).
range_in(comments, string, type_definition).
class_slot(type_definition, examples).
required(examples).
slotrange(example).
multivalued_in(examples, type_definition).
range_in(examples, example, type_definition).
class_slot(type_definition, in_subset).
required(in_subset).
slotrange(subset_definition).
multivalued_in(in_subset, type_definition).
range_in(in_subset, subset_definition, type_definition).
class_slot(type_definition, from_schema).
required(from_schema).
slotrange(uri).
range_in(from_schema, uri, type_definition).
class_slot(type_definition, imported_from).
required(imported_from).
slotrange(string).
range_in(imported_from, string, type_definition).
class_slot(type_definition, see_also).
required(see_also).
slotrange(uriorcurie).
multivalued_in(see_also, type_definition).
range_in(see_also, uriorcurie, type_definition).
class_slot(type_definition, deprecated_element_has_exact_replacement).
required(deprecated_element_has_exact_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_exact_replacement, uriorcurie, type_definition).
class_slot(type_definition, deprecated_element_has_possible_replacement).
required(deprecated_element_has_possible_replacement).
slotrange(uriorcurie).
range_in(deprecated_element_has_possible_replacement, uriorcurie, type_definition).
class_slot(type_definition, typeof).
required(typeof).
slotrange(type_definition).
range_in(typeof, type_definition, type_definition).
class_slot(type_definition, base).
required(base).
slotrange(string).
range_in(base, string, type_definition).
class_slot(type_definition, uri).
required(uri).
slotrange(uriorcurie).
range_in(uri, uriorcurie, type_definition).
class_slot(type_definition, repr).
required(repr).
slotrange(string).
range_in(repr, string, type_definition).
class_slot(type_definition, pattern).
required(pattern).
slotrange(string).
range_in(pattern, string, type_definition).
class(unique_key).
mixin(unique_key, extensible).
mixin(unique_key, annotatable).
has_uri(unique_key, 'http://w3id.org/biolink/vocab/UniqueKey').
class_slot(unique_key, unique_key_slots).
required(unique_key_slots).
slotrange(slot_definition).
multivalued_in(unique_key_slots, unique_key).
required_in(unique_key_slots, unique_key).
range_in(unique_key_slots, slot_definition, unique_key).
class_slot(unique_key, extensions).
required(extensions).
slotrange(extension).
multivalued_in(extensions, unique_key).
range_in(extensions, extension, unique_key).
class_slot(unique_key, annotations).
required(annotations).
slotrange(annotation).
multivalued_in(annotations, unique_key).
range_in(annotations, annotation, unique_key).

