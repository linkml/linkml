import io
import json
from abc import ABC, abstractmethod

from json_flattener import GlobalConfig, flatten_to_csv
from pydantic import BaseModel

from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.dumpers.json_dumper import JSONDumper
from linkml_runtime.linkml_model.meta import SchemaDefinition, SlotDefinitionName
from linkml_runtime.utils.csvutils import get_configmap
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot

# Mapping from boolean_output annotation values to (true_str, false_str)
BOOLEAN_OUTPUT_FORMATS = {
    "true": ("true", "false"),
    "True": ("True", "False"),
    "TRUE": ("TRUE", "FALSE"),
    "yes": ("yes", "no"),
    "Yes": ("Yes", "No"),
    "YES": ("YES", "NO"),
    "on": ("on", "off"),
    "On": ("On", "Off"),
    "ON": ("ON", "OFF"),
    "1": ("1", "0"),
}


def _get_boolean_output_format(schemaview: SchemaView, boolean_output: str = None) -> tuple[str, str]:
    """
    Get the boolean output format from annotation or parameter.

    Args:
        schemaview: The schema view
        boolean_output: CLI override for boolean output format

    Returns:
        Tuple of (true_string, false_string)
    """
    # Default to lowercase true/false
    format_key = "true"

    # Check schema annotation
    if schemaview and schemaview.schema and schemaview.schema.annotations:
        if "boolean_output" in schemaview.schema.annotations:
            format_key = schemaview.schema.annotations["boolean_output"].value

    # CLI option overrides schema annotation
    if boolean_output is not None:
        format_key = boolean_output

    return BOOLEAN_OUTPUT_FORMATS.get(format_key, ("true", "false"))


def _convert_booleans_for_output(obj: dict | list, true_str: str, false_str: str) -> dict | list:
    """
    Recursively convert boolean values to the specified string format.

    Args:
        obj: A dict or list to process
        true_str: String to use for True values
        false_str: String to use for False values

    Returns:
        The same structure with booleans converted to strings
    """
    if isinstance(obj, dict):
        return {k: _convert_booleans_for_output(v, true_str, false_str) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_booleans_for_output(item, true_str, false_str) for item in obj]
    elif isinstance(obj, bool):
        return true_str if obj else false_str
    else:
        return obj


class DelimitedFileDumper(Dumper, ABC):
    @property
    @abstractmethod
    def delimiter(self):
        pass

    def dumps(
        self,
        element: BaseModel | YAMLRoot,
        index_slot: SlotDefinitionName = None,
        schema: SchemaDefinition = None,
        schemaview: SchemaView = None,
        boolean_output: str = None,
        **kwargs,
    ) -> str:
        """Return element formatted as CSV lines

        Args:
            element: The element to dump
            index_slot: The slot that indexes the top-level objects
            schema: The schema definition
            schemaview: The schema view
            boolean_output: Output format for booleans (true, yes, 1, on, etc.)
            **kwargs: Additional arguments passed to flatten_to_csv

        Returns:
            CSV/TSV formatted string
        """
        json_dumper = JSONDumper()
        element_j = json.loads(json_dumper.dumps(element))
        objs = element_j[index_slot]
        if schemaview is None:
            schemaview = SchemaView(schema)

        # Convert booleans to the specified output format
        true_str, false_str = _get_boolean_output_format(schemaview, boolean_output)
        objs = [_convert_booleans_for_output(obj, true_str, false_str) for obj in objs]

        configmap = get_configmap(schemaview, index_slot)
        config = GlobalConfig(key_configs=configmap, csv_delimiter=self.delimiter)
        output = io.StringIO()
        flatten_to_csv(objs, output, config=config, **kwargs)
        return output.getvalue()
