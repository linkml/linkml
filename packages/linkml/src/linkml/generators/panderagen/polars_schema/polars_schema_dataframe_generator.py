import logging
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
            "xsd:int": "pl:Int32",
            "xsd:integer": "pl.Int64",
            "xsd:float": "pl.Float64",  # maybe architecture dependent?
            "xsd:double": "pl.Float64",
            "xsd:boolean": "pl.Boolean",
            "xsd:dateTime": 'pl.Datetime(time_unit="us", time_zone=None)',
            "xsd:date": "pl.Date",
            "xsd:time": "pl.Time",
            "xsd:anyURI": "pl.Utf8",
            "xsd:decimal": "pl.Float64",
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
