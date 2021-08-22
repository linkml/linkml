from json_flattener import unflatten_from_csv, KeyConfig, GlobalConfig, Serializer
import json
from typing import Type
from linkml_runtime.utils.yamlutils import YAMLRoot

from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.loaders.json_loader import JSONLoader
from linkml_runtime.linkml_model.meta import SlotDefinitionName, SchemaDefinition, ClassDefinition
from linkml_runtime.utils.yamlutils import YAMLRoot
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.csvutils import get_configmap

class CSVLoader(Loader):

    def loads(self, input,
              target_class: Type[YAMLRoot],
              index_slot: SlotDefinitionName = None,
              schema: SchemaDefinition = None,
              schemaview: SchemaView = None,
              **kwargs) -> str:
        if schemaview is None:
            schemaview = SchemaView(schema)
        configmap = get_configmap(schemaview, index_slot)
        config = GlobalConfig(key_configs=configmap)
        objs = unflatten_from_csv(input, config=config, **kwargs)
        return JSONLoader().loads(json.dumps({index_slot: objs}), target_class=target_class)

    def load(self, source: str,
             target_class: Type[YAMLRoot],
             index_slot: SlotDefinitionName = None,
             schema: SchemaDefinition = None,
             schemaview: SchemaView = None,
             **kwargs) -> str:
        if schemaview is None:
            schemaview = SchemaView(schema)
        configmap = get_configmap(schemaview, index_slot)
        config = GlobalConfig(key_configs=configmap)
        print(f'Loading from {source}')
        objs = unflatten_from_csv(source, config=config, **kwargs)
        return JSONLoader().loads(json.dumps({index_slot: objs}), target_class=target_class)