import json
from abc import ABC, abstractmethod

from json_flattener import GlobalConfig, unflatten_from_csv
from pydantic import BaseModel

from linkml_runtime.linkml_model.meta import SchemaDefinition, SlotDefinitionName
from linkml_runtime.loaders.json_loader import JSONLoader
from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.boolean_utils import coerce_boolean_values, get_boolean_config, get_boolean_slots
from linkml_runtime.utils.csvutils import get_configmap
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot


def _coerce_empty_to_none(obj: dict | list) -> dict | list:
    """
    Recursively coerce empty string values to None.

    Per Chris Mungall's guidance in Discussion #1996: ``""`` should be coerced to null.

    Args:
        obj: A dict or list from json-flattener unflatten

    Returns:
        The same structure with empty strings replaced by None
    """
    if isinstance(obj, dict):
        return {
            k: _coerce_empty_to_none(v) if isinstance(v, dict | list) else (None if v == "" else v)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [
            _coerce_empty_to_none(item) if isinstance(item, dict | list) else (None if item == "" else item)
            for item in obj
        ]
    return obj


class DelimitedFileLoader(Loader, ABC):
    @property
    @abstractmethod
    def delimiter(self):
        pass

    def load_as_dict(
        self,
        source: str,
        index_slot: SlotDefinitionName = None,
        schema: SchemaDefinition = None,
        schemaview: SchemaView = None,
        **kwargs,
    ) -> dict | list[dict]:
        json_str = self._get_json_str_to_load(source, index_slot, schema, schemaview, **kwargs)
        return JSONLoader().load_as_dict(json_str)

    def load_any(self, *args, **kwargs) -> YAMLRoot | list[YAMLRoot]:
        return self.load(*args, **kwargs)

    def loads(
        self,
        input,
        target_class: type[BaseModel | YAMLRoot],
        index_slot: SlotDefinitionName = None,
        schema: SchemaDefinition = None,
        schemaview: SchemaView = None,
        **kwargs,
    ) -> str:
        json_str = self._get_json_str_to_load(input, index_slot, schema, schemaview, **kwargs)
        return JSONLoader().loads(json_str, target_class=target_class)

    def load(
        self,
        source: str,
        target_class: type[BaseModel | YAMLRoot],
        index_slot: SlotDefinitionName = None,
        schema: SchemaDefinition = None,
        schemaview: SchemaView = None,
        **kwargs,
    ) -> str:
        json_str = self._get_json_str_to_load(source, index_slot, schema, schemaview, **kwargs)
        return JSONLoader().loads(json_str, target_class=target_class)

    def _get_json_str_to_load(
        self,
        input,
        index_slot: SlotDefinitionName = None,
        schema: SchemaDefinition = None,
        schemaview: SchemaView = None,
        boolean_truthy: frozenset[str] | None = None,
        boolean_falsy: frozenset[str] | None = None,
        **kwargs,
    ):
        if schemaview is None:
            schemaview = SchemaView(schema)
        configmap = get_configmap(schemaview, index_slot)
        config = GlobalConfig(key_configs=configmap, csv_delimiter=self.delimiter)
        objs = unflatten_from_csv(input, config=config, **kwargs)

        # Coerce empty strings to null (per Discussion #1996)
        objs = [_coerce_empty_to_none(obj) for obj in objs]

        # Schema-aware boolean coercion: only coerce for slots with range: boolean
        boolean_slots = get_boolean_slots(schemaview, index_slot)
        if boolean_slots:
            bc = get_boolean_config(schemaview, boolean_truthy=boolean_truthy, boolean_falsy=boolean_falsy)
            objs = [coerce_boolean_values(obj, boolean_slots, bc.truthy_values, bc.falsy_values) for obj in objs]

        return json.dumps({index_slot: objs})
