from ..name_handler_mixin import NameHandlerBase


class PanderaSchemaNameHandler(NameHandlerBase):
    """
    A class that handles naming conventions for Polars schema in generated code.
    """

    _PREFIX = "pandera"

    def render_enum_name(self, enum_name: str) -> str:
        return enum_name

    def render_class_name(self, cls_name: str) -> str:
        return cls_name

    def render_slot_name(self, slot_name: str) -> str:
        return slot_name
