import io
import yaml
import json
from typing import Dict, List, Any

from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.dumpers.json_dumper import JSONDumper
from linkml_runtime.utils.yamlutils import YAMLRoot
from linkml_runtime.linkml_model.meta import SlotDefinitionName, SchemaDefinition
from linkml_runtime.utils.schemaview import SchemaView

from linkml_runtime.utils.csvutils import GlobalConfig, get_configmap
from json_flattener import flatten_to_csv


class CSVDumper(Dumper):

    def dumps(self, element: YAMLRoot,
              index_slot: SlotDefinitionName = None,
              schema: SchemaDefinition = None,
              schemaview: SchemaView = None,
              **kwargs) -> str:
        """ Return element formatted as CSV lines """
        json_dumper = JSONDumper()
        element_j = json.loads(json_dumper.dumps(element))
        objs = element_j[index_slot]
        if schemaview is None:
            schemaview = SchemaView(schema)
        configmap = get_configmap(schemaview, index_slot)
        config = GlobalConfig(key_configs=configmap)
        output = io.StringIO()
        flatten_to_csv(objs, output, config=config, **kwargs)
        return output.getvalue()
