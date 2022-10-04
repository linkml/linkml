from functools import lru_cache
import re
from typing import Dict


class PatternResolver():

    # regular expression capturing the various use cases
    # for the optionally dot separated, curly braces bound, pattern syntax
    var_name = re.compile("{([a-z0-9_-]+([\.-_ ][a-z0-9]+)*)}", re.IGNORECASE)

    def __init__(self, schema_view):
        # fetch settings from schema_view
        settings_dict = schema_view.schema.settings

        # dictionary of key and string value of settings dict
        self.format_spec = {}

        for k, setting in settings_dict.items():

            # create spec dictionary with keys that will replace
            # substrings in the structured pattern syntax
            self.format_spec[k] = setting.setting_value

    @lru_cache()
    def resolve(self, pattern: str) -> str:
        # apply the regex to the pattern and look for matches
        matches = self.var_name.finditer(pattern)

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

            elif item.group(1) in self.format_spec:
                match_string = str(self.format_spec[item.group(1)])

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

        return converted

