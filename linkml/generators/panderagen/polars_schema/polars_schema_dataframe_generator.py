import logging
from dataclasses import dataclass

from linkml_runtime.linkml_model.meta import TypeDefinition

# TODO: separate these all out for PolaRS
from ..dataframe_generator import DataframeGenerator
from .name_handler_polars_schema import PolarsSchemaNameHandler
from .slot_generator_mixin_polars_schema import SlotGeneratorMixinPolarsSchema

logger = logging.getLogger(__name__)


# Polars-specific type mapping
TYPE_MAP = {
    "panderagen_polars_schema": {
        "xsd:string": "pl.Utf8",
        "xsd:normalizedString": "pl.Utf8",
        "xsd:int": "pl:Int32",
        "xsd:integer": "pl.Int64",
        "xsd:float": "pl.Float32",
        "xsd:double": "pl.Float64",
        "xsd:boolean": "pl.Boolean",
        "xsd:dateTime": "pl.Datetime",
        "xsd:date": "pl.Date",
        "xsd:time": "pl.Time",
        "xsd:anyURI": "pl.Utf8",
        "xsd:decimal": "pl.Decimal",
    },
}

# Backward compatibility
POLARS_TYPEMAP = TYPE_MAP.copy()


@dataclass
class PolarsSchemaDataframeGenerator(DataframeGenerator, PolarsSchemaNameHandler, SlotGeneratorMixinPolarsSchema):
    """
    Generates Polars schema classes from a LinkML schema.
    """

    TEMPLATE_DIRECTORY = "panderagen_polars_schema"

    @staticmethod
    def make_multivalued(range: str) -> str:
        return f"pl.List({range})"

    def uri_type_map(self, xsd_uri: str, template: str = None):
        if template is None:
            template = "panderagen_polars_schema"
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
