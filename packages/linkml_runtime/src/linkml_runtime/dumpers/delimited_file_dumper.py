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
        **kwargs,
    ) -> str:
        """Return element formatted as CSV lines"""
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
