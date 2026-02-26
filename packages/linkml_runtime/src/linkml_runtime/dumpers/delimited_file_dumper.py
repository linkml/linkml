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

        bc = get_boolean_config(schemaview, boolean_output=boolean_output)
        objs = [convert_booleans_for_output(obj, bc.output_true, bc.output_false) for obj in objs]

        configmap = get_configmap(schemaview, index_slot)
        config = GlobalConfig(key_configs=configmap, csv_delimiter=self.delimiter)
        output = io.StringIO()
        flatten_to_csv(objs, output, config=config, **kwargs)
        return output.getvalue()
