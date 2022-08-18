import re
from typing import Iterable

from linkml_runtime import SchemaView

from ..linter import LinterProblem, LinterRule

PATTERNS = {
    "snake": "[a-z][_a-z0-9]+",
    "uppersnake": "[A-Z][_A-Z0-9]+",
    "camel": "[a-z][a-zA-Z0-9]+",
    "kebab": "[a-z][\-a-z0-9]+",
}


class PermissibleValuesFormatRule(LinterRule):
    id = "permissible_values_format"

    def check(
        self, schema_view: SchemaView, fix: bool = False
    ) -> Iterable[LinterProblem]:
        pattern = PATTERNS.get(self.config.format, self.config.format)
        for enum_name, enum_def in schema_view.all_enums(imports=False).items():
            for value in enum_def.permissible_values.keys():
                if re.fullmatch(pattern, value) is None:
                    yield LinterProblem(
                        f"Enum '{enum_name}' has permissible value '{value}'"
                    )
