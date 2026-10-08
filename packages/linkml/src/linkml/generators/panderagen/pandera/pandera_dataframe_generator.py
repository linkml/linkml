import logging
from dataclasses import dataclass
from enum import Enum

from linkml.generators.common.naming import check_keyword_collisions
from linkml_runtime.linkml_model.meta import ClassDefinition

from ..dataframe_generator import DataframeGenerator
from ..render_adapters.dataframe_class import DataframeClass
from .slot_handler_pandera import SlotHandlerPandera

logger = logging.getLogger(__name__)


class TemplateEnum(Enum):
    CLASS_BASED = "panderagen_class_based"
    OBJECT_BASED = "panderagen_object_based"
    POLARS_SCHEMA = "polars_schema"


@dataclass
class PanderaDataframeGenerator(DataframeGenerator):
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

    def _default_type_map(self) -> dict:
        return {
            "xsd:string": "str",
            "xsd:integer": "int",
            "xsd:int": "int",
            "xsd:float": "float",
            "xsd:double": "float",
            "xsd:boolean": "bool",
            "xsd:dateTime": "DateTime()",
            "xsd:date": "Date",
            "xsd:time": "Time",
            "xsd:anyURI": "str",
            "xsd:decimal": "float",
        }

    def __post_init__(self):
        super().__post_init__()
        self.slot_handler = SlotHandlerPandera(self)

    @staticmethod
    def make_multivalued(range: str) -> str:
        return "List"

    def append_slots(self, schemaview_class: ClassDefinition, ooclass: DataframeClass) -> None:
        """
        Append slots to the class. A class cannot have both a column named after a Python keyword, such as from,
        and a column from_, because the class-based model gives both the attribute from_.
        """
        super().append_slots(schemaview_class, ooclass)
        check_keyword_collisions(schemaview_class.name, [field.name for field in ooclass.all_fields])
