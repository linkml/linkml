from ..name_handler_mixin import NameHandlerBase


class PolarsSchemaNameHandler(NameHandlerBase):
    """
    A class that handles naming conventions for Polars schema in generated code.
    """

    _PREFIX = "polars"

    def render_enum_name(self, enum_name: str) -> str:
        return f"{PolarsSchemaNameHandler._PREFIX}_enum_{enum_name}"

    def render_class_name(self, cls_name: str) -> str:
        return f"{PolarsSchemaNameHandler._PREFIX}_{cls_name}"

    def render_slot_name(self, slot_name: str) -> str:
        return f"{PolarsSchemaNameHandler._PREFIX}_slot_{slot_name}"
