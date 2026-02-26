import io
import json
from abc import ABC, abstractmethod

from json_flattener import GlobalConfig, flatten_to_csv
from pydantic import BaseModel

from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.dumpers.json_dumper import JSONDumper
from linkml_runtime.linkml_model.meta import SchemaDefinition, SlotDefinitionName
from linkml_runtime.utils.boolean_utils import convert_booleans_for_output, get_boolean_config
from linkml_runtime.utils.csvutils import get_configmap
from linkml_runtime.utils.list_utils import (
    check_data_for_delimiter,
    enhance_configmap_for_multivalued_primitives,
    get_list_config,
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
        boolean_output: str = None,
        **kwargs,
    ) -> str:
        """Return element formatted as CSV lines

        Args:
            element: The element to dump
            index_slot: The slot that indexes the top-level objects
            schema: The schema definition
            schemaview: The schema view
            list_wrapper: Override wrapper style for lists (square, curly, paren, none)
            list_delimiter: Override delimiter character between list items
            list_strip_whitespace: Override whether to strip whitespace around delimiters
            refuse_delimiter_in_data: Override whether to raise on delimiter-in-data conflicts
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

        lc = get_list_config(
            schemaview,
            list_wrapper=list_wrapper,
            list_delimiter=list_delimiter,
            list_strip_whitespace=list_strip_whitespace,
            refuse_delimiter_in_data=refuse_delimiter_in_data,
        )

        if lc.refuse_delimiter_in_data:
            check_data_for_delimiter(objs, lc.inner_delimiter, schemaview, index_slot)

        if lc.strip_whitespace:
            objs = [strip_whitespace_from_lists(obj) for obj in objs]

        # Convert booleans to the specified output format
        bc = get_boolean_config(schemaview, boolean_output=boolean_output)
        objs = [convert_booleans_for_output(obj, bc.output_true, bc.output_false) for obj in objs]

        configmap = get_configmap(schemaview, index_slot)
        configmap = enhance_configmap_for_multivalued_primitives(
            schemaview, index_slot, configmap, unwrapped_mode=lc.unwrapped
        )

        config = GlobalConfig(
            key_configs=configmap,
            csv_delimiter=self.delimiter,
            csv_list_markers=lc.list_markers,
            csv_inner_delimiter=lc.inner_delimiter,
        )
        output = io.StringIO()
        flatten_to_csv(objs, output, config=config, **kwargs)
        return output.getvalue()
