from abc import ABC, abstractmethod
from json_flattener import unflatten_from_csv, GlobalConfig
import json
from typing import Union
from linkml_runtime.utils.yamlutils import YAMLRoot
from pydantic import BaseModel

from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.loaders.json_loader import JSONLoader
from linkml_runtime.linkml_model.meta import SlotDefinitionName, SchemaDefinition
from linkml_runtime.utils.yamlutils import YAMLRoot
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.csvutils import get_configmap

class DelimitedFileLoader(Loader, ABC):

    @property
    @abstractmethod
    def delimiter(self):
        pass

    def load_as_dict(self, 
                     source: str,
                     index_slot: SlotDefinitionName = None,
                     schema: SchemaDefinition = None,
                     schemaview: SchemaView = None,
                     **kwargs) -> Union[dict, list[dict]]:
        json_str = self._get_json_str_to_load(source, index_slot, schema, schemaview, **kwargs)
        return JSONLoader().load_as_dict(json_str)

    def load_any(self, *args, **kwargs) -> Union[YAMLRoot, list[YAMLRoot]]:
        return self.load(*args, **kwargs)

    def loads(self, input,
              target_class: type[Union[BaseModel, YAMLRoot]],
              index_slot: SlotDefinitionName = None,
              schema: SchemaDefinition = None,
              schemaview: SchemaView = None,
              **kwargs) -> str:
        json_str = self._get_json_str_to_load(input, index_slot, schema, schemaview, **kwargs)
        return JSONLoader().loads(json_str, target_class=target_class)

    def load(self, source: str,
             target_class: type[Union[BaseModel, YAMLRoot]],
             index_slot: SlotDefinitionName = None,
             schema: SchemaDefinition = None,
             schemaview: SchemaView = None,
             **kwargs) -> str:
        json_str = self._get_json_str_to_load(source, index_slot, schema, schemaview, **kwargs)
        return JSONLoader().loads(json_str, target_class=target_class)

    def _get_json_str_to_load(self,
                          input,
                          index_slot: SlotDefinitionName = None,
                          schema: SchemaDefinition = None,
                          schemaview: SchemaView = None,
                          **kwargs):
        if schemaview is None:
            schemaview = SchemaView(schema)
        configmap = get_configmap(schemaview, index_slot)
        config = GlobalConfig(key_configs=configmap, csv_delimiter=self.delimiter)
        objs = unflatten_from_csv(input, config=config, **kwargs)
        return json.dumps({index_slot: objs})