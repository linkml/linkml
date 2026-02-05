import json
from abc import ABC, abstractmethod

from json_flattener import GlobalConfig, unflatten_from_csv
from pydantic import BaseModel

from linkml_runtime.linkml_model.meta import SchemaDefinition, SlotDefinitionName
from linkml_runtime.loaders.json_loader import JSONLoader
from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.csvutils import get_configmap
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot


# YAML 1.1 boolean values plus numeric 0/1 (case-insensitive for strings)
TRUTHY_VALUES = frozenset({"true", "yes", "on", "1"})
FALSY_VALUES = frozenset({"false", "no", "off", "0"})


def _get_boolean_slots(schemaview: SchemaView, index_slot: SlotDefinitionName) -> set[str]:
    """
    Get the names of slots with range: boolean for the class targeted by index_slot.

    Args:
        schemaview: The schema view
        index_slot: The slot that indexes the top-level objects

    Returns:
        Set of slot names that have boolean range
    """
    if schemaview is None or index_slot is None:
        return set()

    slot = schemaview.get_slot(index_slot)
    if slot is None or slot.range is None:
        return set()

    target_class = slot.range
    if target_class not in schemaview.all_classes():
        return set()

    boolean_slots = set()
    for slot_name in schemaview.class_slots(target_class):
        induced_slot = schemaview.induced_slot(slot_name, target_class)
        if induced_slot.range == "boolean":
            boolean_slots.add(slot_name)

    return boolean_slots


def _coerce_boolean_values(obj: Union[dict, list], boolean_slots: set[str]) -> Union[dict, list]:
    """
    Recursively coerce string values in boolean slots to actual booleans.

    Accepts YAML 1.1 boolean values plus numeric 0/1:
    - Truthy: true, yes, on (case-insensitive), 1
    - Falsy: false, no, off (case-insensitive), 0

    Args:
        obj: A dict or list from json-flattener unflatten
        boolean_slots: Set of slot names that should be coerced to boolean

    Returns:
        The same structure with boolean slots coerced to actual booleans
    """
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            if k in boolean_slots:
                result[k] = _coerce_single_boolean(v)
            elif isinstance(v, (dict, list)):
                result[k] = _coerce_boolean_values(v, boolean_slots)
            else:
                result[k] = v
        return result
    elif isinstance(obj, list):
        return [_coerce_boolean_values(item, boolean_slots) for item in obj]
    else:
        return obj


def _coerce_single_boolean(value):
    """Coerce a single value to boolean if it matches truthy/falsy patterns."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        if value == 1:
            return True
        if value == 0:
            return False
        return value
    if isinstance(value, str):
        lower = value.lower()
        if lower in TRUTHY_VALUES:
            return True
        if lower in FALSY_VALUES:
            return False
    return value


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
        **kwargs,
    ):
        if schemaview is None:
            schemaview = SchemaView(schema)
        configmap = get_configmap(schemaview, index_slot)
        config = GlobalConfig(key_configs=configmap, csv_delimiter=self.delimiter)
        objs = unflatten_from_csv(input, config=config, **kwargs)

        # Schema-aware boolean coercion: only coerce for slots with range: boolean
        boolean_slots = _get_boolean_slots(schemaview, index_slot)
        if boolean_slots:
            objs = [_coerce_boolean_values(obj, boolean_slots) for obj in objs]

        return json.dumps({index_slot: objs})
