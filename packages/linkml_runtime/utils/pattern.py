import re
from typing import Dict


def generate_patterns(schema_view) -> Dict[str, str]:
    """Generates a dictionary of slot patterns corresponding to
    the structured patterns in the settings.

    :param schema_view: SchemaView object with LinkML YAML
        already loaded
    :return generated_patterns: dictionary with the 
        expanded structured patterns 
    """

    # fetch settings from schema_view
    settings_dict = schema_view.schema.settings

    # dictionary of key and string value of settings dict
    format_spec = {}

    for k, setting in settings_dict.items():

        # create spec dictionary with keys that will replace
        # substrings in the structured pattern syntax
        format_spec[k] = setting.setting_value

    # dictionary with structured patterns in the key and
    # expanded, or materialized patterns as values
    generated_patterns = {}

    # regular expression capturing the various use cases
    # for the optionally dot separated, curly braces bound, pattern syntax
    var_name = re.compile("{([a-z0-9_-]+([\.-_ ][a-z0-9]+)*)}", re.IGNORECASE)

    for _, slot_defn in schema_view.all_slots().items():
        if slot_defn.structured_pattern:
            struct_pat = slot_defn.structured_pattern

            pattern = struct_pat.syntax

            # compute pattern from structured patterns
            # and format_spec dictionary


            # apply the regex to the pattern and look for matches
            matches = var_name.finditer(pattern)

            reversed = []
            for item in matches:
                # Detect double set brackets
                match_string = None
                if (
                    item.start() > 0
                    and item.end() < len(pattern)
                    and pattern[item.start() - 1] == "{"
                    and pattern[item.end()] == "}"
                ):
                    match_string = item.group(1)

                elif item.group(1) in format_spec:
                    match_string = str(format_spec[item.group(1)])

                if match_string:
                    reversed.insert(
                        0,
                        {
                            "string": match_string,
                            "start": item.start(),
                            "end": item.end(),
                        },
                    )

            converted = pattern
            for item in reversed:
                converted = (
                    converted[: item["start"]]
                    + item["string"]
                    + converted[item["end"] :]
                )

            generated_patterns[pattern] = converted

    return generated_patterns
