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

# Default boolean sentinels following pandas/R conventions (case-insensitive).
# Only {T, TRUE} / {F, FALSE} per Chris Mungall's guidance in Discussion #1996.
# Additional sentinels like yes/no or 0/1 can be added via boolean_truthy/boolean_falsy
# schema annotations or CLI options.
DEFAULT_TRUTHY_VALUES = frozenset({"true", "t"})
DEFAULT_FALSY_VALUES = frozenset({"false", "f"})


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


def _get_boolean_sentinels(
    schemaview: SchemaView | None,
    truthy_override: frozenset[str] | None = None,
    falsy_override: frozenset[str] | None = None,
) -> tuple[frozenset[str], frozenset[str]]:
    """
    Determine the truthy and falsy sentinel sets for boolean coercion.

    Cumulative: defaults are extended by schema annotations, which are
    further extended by CLI options. All values are stored and compared
    case-insensitively.

    Schema annotations ``boolean_truthy`` and ``boolean_falsy`` are comma-separated
    strings, e.g. ``boolean_truthy: "yes,on,1"``.

    Args:
        schemaview: The schema view (may be None)
        truthy_override: CLI-provided truthy values (already lowercased)
        falsy_override: CLI-provided falsy values (already lowercased)

    Returns:
        Tuple of (truthy_set, falsy_set) with all values lowercased
    """
    truthy = DEFAULT_TRUTHY_VALUES
    falsy = DEFAULT_FALSY_VALUES

    # Schema annotations extend the defaults
    if schemaview and schemaview.schema and schemaview.schema.annotations:
        ann = schemaview.schema.annotations
        if "boolean_truthy" in ann:
            extra = frozenset(v.strip().lower() for v in ann["boolean_truthy"].value.split(",") if v.strip())
            truthy = truthy | extra
        if "boolean_falsy" in ann:
            extra = frozenset(v.strip().lower() for v in ann["boolean_falsy"].value.split(",") if v.strip())
            falsy = falsy | extra

    # CLI overrides extend further
    if truthy_override is not None:
        truthy = truthy | truthy_override
    if falsy_override is not None:
        falsy = falsy | falsy_override

    return truthy, falsy


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


def _coerce_boolean_values(
    obj: dict | list,
    boolean_slots: set[str],
    truthy: frozenset[str] = DEFAULT_TRUTHY_VALUES,
    falsy: frozenset[str] = DEFAULT_FALSY_VALUES,
) -> dict | list:
    """
    Recursively coerce string values in boolean slots to actual booleans.

    Default sentinels follow pandas/R conventions (case-insensitive):
    - Truthy: T, TRUE
    - Falsy: F, FALSE

    Additional sentinels can be provided via the truthy/falsy parameters,
    which are populated from schema annotations or CLI options.

    Args:
        obj: A dict or list from json-flattener unflatten
        boolean_slots: Set of slot names that should be coerced to boolean
        truthy: Set of lowercase strings to treat as True
        falsy: Set of lowercase strings to treat as False

    Returns:
        The same structure with boolean slots coerced to actual booleans
    """
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            if k in boolean_slots:
                if isinstance(v, list):
                    result[k] = [_coerce_single_boolean(item, truthy, falsy) for item in v]
                else:
                    result[k] = _coerce_single_boolean(v, truthy, falsy)
            elif isinstance(v, dict | list):
                result[k] = _coerce_boolean_values(v, boolean_slots, truthy, falsy)
            else:
                result[k] = v
        return result
    elif isinstance(obj, list):
        return [_coerce_boolean_values(item, boolean_slots, truthy, falsy) for item in obj]
    else:
        return obj


def _coerce_single_boolean(
    value,
    truthy: frozenset[str] = DEFAULT_TRUTHY_VALUES,
    falsy: frozenset[str] = DEFAULT_FALSY_VALUES,
):
    """Coerce a single value to boolean if it matches truthy/falsy patterns.

    Handles both str and int values — CSV parsers may deliver numeric values
    like ``1``/``0`` as int rather than str.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        str_value = str(value)
        if str_value in truthy:
            return True
        if str_value in falsy:
            return False
        return value
    if isinstance(value, str):
        lower = value.lower()
        if lower in truthy:
            return True
        if lower in falsy:
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
        boolean_slots = _get_boolean_slots(schemaview, index_slot)
        if boolean_slots:
            truthy, falsy = _get_boolean_sentinels(schemaview, boolean_truthy, boolean_falsy)
            objs = [_coerce_boolean_values(obj, boolean_slots, truthy, falsy) for obj in objs]

        return json.dumps({index_slot: objs})
