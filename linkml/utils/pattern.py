from linkml_runtime.utils.schemaview import SchemaView


def materialize_patterns(schema_view: SchemaView):
    """Materializes slot patterns based on structured
    patterns in the settings.

    Note: Changes the schema in place.

    :param schema_view: SchemaView object with LinkML YAML
        already loaded
    """

    # fetch settings from schema_view
    settings_dict = schema_view.schema.settings

    # dictionary of key and string value of settings dict
    format_spec = {}

    for k, setting in settings_dict.items():

        # TODO: handle keys with "."
        if "." in k:
            continue

        format_spec[k] = setting.setting_value

    for _, slot_defn in schema_view.all_slots().items():
        if slot_defn.structured_pattern:
            struct_pat = slot_defn.structured_pattern

            # TODO: handle keys with "."
            if "." in struct_pat.syntax:
                continue

            # computer pattern from structured patterns
            # and settings dictionary
            slot_defn.pattern = struct_pat.syntax.format(**format_spec)
