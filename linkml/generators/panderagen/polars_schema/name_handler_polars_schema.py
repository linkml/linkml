import re

from ..name_handler_mixin import NameHandlerBase


class PolarsSchemaNameHandler(NameHandlerBase):
    """
    A class that handles naming conventions for Polars schema in generated code.
    """

    _PREFIX = "polars"

    def clean(self, name: str) -> str:
        return re.sub(r"\W+", "_", name)

    def render_enum_name(self, enum_name: str) -> str:
        return self.clean(enum_name)

    def render_class_name(self, class_name: str) -> str:
        return self.clean(class_name)

    def render_slot_name(self, slot_name: str) -> str:
        return self.clean(f"{PolarsSchemaNameHandler._PREFIX}_slot_{slot_name}")
