import logging
from dataclasses import dataclass
from enum import Enum

from linkml_runtime.linkml_model.meta import TypeDefinition

from ..class_generator_mixin import ClassGeneratorMixin
from ..dataframe_generator import DataframeGenerator
from ..enum_generator_mixin import EnumGeneratorMixin
from .name_handler_pandera_schema import PanderaSchemaNameHandler
from .slot_generator_mixin_pandera import SlotGeneratorMixinPandera

logger = logging.getLogger(__name__)


# Pandera-specific type mapping
TYPE_MAP = {
    "panderagen_class_based": {
        "xsd:string": "str",
        "xsd:integer": "int",
        "xsd:int": "int",
        "xsd:float": "float",
        "xsd:double": "float",
        "xsd:boolean": "bool",
        "xsd:dateTime": "DateTime",
        "xsd:date": "Date",
        "xsd:time": "Time",
        "xsd:anyURI": "str",
        "xsd:decimal": "float",
    },
}

# Backward compatibility
TYPEMAP = TYPE_MAP.copy()


class TemplateEnum(Enum):
    CLASS_BASED = "panderagen_class_based"
    OBJECT_BASED = "panderagen_object_based"
    POLARS_SCHEMA = "polars_schema"
    PYARROW_SCHEMA = "pyarrow_schema"


@dataclass
class PanderaDataframeGenerator(
    DataframeGenerator, EnumGeneratorMixin, ClassGeneratorMixin, SlotGeneratorMixinPandera, PanderaSchemaNameHandler
):
    """
    Generates Pandera python classes from a LinkML schema.

    Status: incompletely implemented

    Two styles are supported:

    - class-based
    - schema-based (not implemented)
    """

    TEMPLATE_DIRECTORY = "panderagen_class_based"

    # ObjectVars
    inline_validator_mixin: bool = False
    coerce: bool = False

    @staticmethod
    def make_multivalued(range: str) -> str:
        if range == "Struct":
            return "pl.List"  # WOW
        return f"List[{range}]"

    def uri_type_map(self, xsd_uri: str, template: str = None):
        if template is None:
            template = "panderagen_class_based"
        return TYPE_MAP[template].get(xsd_uri)

    def get_type_map(self) -> dict:
        """Get the type map for this generator."""
        return TYPE_MAP

    def map_type(self, t: TypeDefinition) -> str:
        logger.info(f"type_map definition: {t}")

        typ = None

        if t.uri:
            typ = self.uri_type_map(t.uri)
            if typ is None:
                typ = self.map_type(self.schemaview.get_type(t.typeof))
        elif t.typeof:
            typ = self.map_type(self.schemaview.get_type(t.typeof))

        if typ is None:
            raise ValueError(f"{t} cannot be mapped to a type")

        return typ
