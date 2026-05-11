import logging
import re
from dataclasses import dataclass

from ..dataframe_generator import DataframeGenerator
from .slot_handler_polars import SlotHandlerPolars

logger = logging.getLogger(__name__)


@dataclass
class PolarsSchemaDataframeGenerator(DataframeGenerator):
    """
    Generates Polars schema classes from a LinkML schema.
    """

    TEMPLATE_DIRECTORY = "panderagen_polars_schema"
    TEMPLATE_PATH = "polars_schema.jinja2"

    def _default_type_map(self) -> dict:
        """Pandera-specific type mapping."""
        return {
            "xsd:string": "pl.Utf8",
            "xsd:normalizedString": "pl.Utf8",
            "xsd:int": "pl.Int32",
            "xsd:integer": "pl.Int64",
            "xsd:float": "pl.Float64",  # maybe architecture dependent?
            "xsd:double": "pl.Float64",
            "xsd:boolean": "pl.Boolean",
            "xsd:dateTime": 'pl.Datetime(time_unit="us", time_zone=None)',
            "xsd:date": "pl.Date",
            "xsd:time": "pl.Time",
            "xsd:anyURI": "pl.Utf8",
            "xsd:decimal": "pl.Float64",
            ## LinkML-specific types not in XSD namespace. Best matches!
            "linkml:DateOrDatetime": "pl.Utf8",  # No direct Polars equivalent
            "shex:iri": "pl.Utf8",  # objectidentifier
            "shex:nonLiteral": "pl.Utf8",  # nodeidentifier
        }

    def __post_init__(self):
        # Ensure template_path and template_file are set to defaults if not provided
        if self.template_path is None:
            self.template_path = PolarsSchemaDataframeGenerator.TEMPLATE_DIRECTORY
        if self.template_file is None:
            self.template_file = PolarsSchemaDataframeGenerator.TEMPLATE_PATH
        super().__post_init__()
        self.slot_handler = SlotHandlerPolars(self)

    @staticmethod
    def make_multivalued(range: str) -> str:
        return f"pl.List({range})"

    @staticmethod
    def dict_range(field_range: str) -> str:
        """Convert a Struct-reference range to its inline pl.Struct(XDict) form.

        This is used in the two-pass template to populate *Dict entries without
        forward-referencing unbound *Struct names.  Examples::

            "ChildStruct"          -> "pl.Struct(ChildDict)"
            "pl.List(ChildStruct)" -> "pl.List(pl.Struct(ChildDict))"

        Non-struct ranges (primitives, enums, Any) are returned unchanged.
        """
        return re.sub(r"(\w+)Struct\b", lambda m: f"pl.Struct({m.group(1)}Dict)", field_range)
