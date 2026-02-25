import io
import json
from abc import ABC, abstractmethod

from json_flattener import GlobalConfig, flatten_to_csv
from pydantic import BaseModel

from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.dumpers.json_dumper import JSONDumper
from linkml_runtime.linkml_model.meta import SchemaDefinition, SlotDefinitionName
from linkml_runtime.utils.csvutils import get_configmap
from linkml_runtime.utils.list_utils import (
    WRAPPER_STYLES,
    check_data_for_delimiter,
    enhance_configmap_for_multivalued_primitives,
    get_list_config_from_annotations,
    strip_whitespace_from_lists,
)
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot


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
        list_wrapper: str = None,
        list_delimiter: str = None,
        list_strip_whitespace: bool = None,
        refuse_delimiter_in_data: bool = None,
        **kwargs,
    ) -> str:
        """Return element formatted as CSV lines"""
        json_dumper = JSONDumper()
        element_j = json.loads(json_dumper.dumps(element))
        objs = element_j[index_slot]
        if schemaview is None:
            schemaview = SchemaView(schema)

        # Read list configuration from schema annotations
        list_markers, inner_delimiter, strip_whitespace, refuse_delim = get_list_config_from_annotations(
            schemaview
        )

        # CLI options override schema annotations
        if list_wrapper is not None:
            list_markers = WRAPPER_STYLES.get(list_wrapper, ("[", "]"))
        if list_delimiter is not None:
            inner_delimiter = list_delimiter
        if list_strip_whitespace is not None:
            strip_whitespace = list_strip_whitespace
        if refuse_delimiter_in_data is not None:
            refuse_delim = refuse_delimiter_in_data

        # Check for delimiter-in-data conflicts before serializing
        if refuse_delim:
            check_data_for_delimiter(objs, inner_delimiter, schemaview, index_slot)

        # Strip whitespace from string values in lists if enabled (default)
        if strip_whitespace:
            objs = [strip_whitespace_from_lists(obj) for obj in objs]

        # Unwrapped mode means no brackets around lists (e.g., a|b|c instead of [a|b|c])
        unwrapped_mode = list_markers == ("", "")

        # Get base configmap and enhance with multivalued primitive slots
        configmap = get_configmap(schemaview, index_slot)
        configmap = enhance_configmap_for_multivalued_primitives(
            schemaview, index_slot, configmap, unwrapped_mode=unwrapped_mode
        )

        config = GlobalConfig(
            key_configs=configmap,
            csv_delimiter=self.delimiter,
            csv_list_markers=list_markers,
            csv_inner_delimiter=inner_delimiter,
        )
        output = io.StringIO()
        flatten_to_csv(objs, output, config=config, **kwargs)
        return output.getvalue()
