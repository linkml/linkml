import logging
from dataclasses import dataclass

from linkml_runtime.linkml_model.meta import TypeDefinition

from ..dataframe_generator import DataframeGenerator

logger = logging.getLogger(__name__)


# Arrow-specific type mapping
TYPE_MAP = {
    "panderagen_arrow_schema": {
        "xsd:string": "pa.string",
        "xsd:integer": "pa.int64",
        "xsd:int": "pa.int32",
        "xsd:float": "pa.float32",
        "xsd:double": "pa.float64",
        "xsd:boolean": "pa.boolean",
        "xsd:dateTime": "pa.timestamp",
        "xsd:date": "pa.date64",
        "xsd:time": "pa.time64",
        "xsd:anyURI": "pa.string",
        "xsd:decimal": "pa.decimal128",
    },
}

# Backward compatibility
ARROW_TYPEMAP = TYPE_MAP.copy()


@dataclass
class ArrowSchemaDataframeGenerator(DataframeGenerator):
    """
    Generates PyArrow schema classes from a LinkML schema.
    """

    TEMPLATE_DIRECTORY = "panderagen_arrow_schema"

    @staticmethod
    def make_multivalued(range: str) -> str:
        if range == "Struct":
            return "pa.list_"
        return f"List[{range}]"

    def uri_type_map(self, xsd_uri: str, template: str = None):
        if template is None:
            template = "panderagen_arrow_schema"
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
