import logging
from typing import Any

from json_flattener import KeyConfig, Serializer
from json_flattener.flattener import CONFIGMAP

from linkml_runtime.linkml_model.meta import ClassDefinitionName, SlotDefinitionName
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)

# Bracket-free list markers for CSV/TSV (pipe delimiter only, no surrounding brackets)
# This aligns with schemasheets conventions and common spreadsheet data entry patterns
CSV_LIST_MARKERS = ("", "")


def clean_multivalued_nulls(data: Any, schemaview: SchemaView, index_slot: SlotDefinitionName) -> Any:
    """
    Clean up [null] or [None] values in multivalued slots after loading from CSV/TSV.

    json-flattener converts empty cells in list columns to [null]. This function
    converts those back to None (omitted) for a cleaner data structure.

    :param data: Data structure loaded from CSV/TSV (dict with index_slot key)
    :param schemaview: LinkML schema view
    :param index_slot: The index slot name containing the list of objects
    :return: Cleaned data structure
    """
    if not isinstance(data, dict) or index_slot not in data:
        return data

    slot = schemaview.get_slot(index_slot) if schemaview else None
    if slot is None or slot.range not in schemaview.all_classes():
        return data

    target_class = slot.range
    multivalued_slots = set()
    for sn in schemaview.class_slots(target_class):
        induced = schemaview.induced_slot(sn, target_class)
        if induced.multivalued:
            multivalued_slots.add(sn)

    items = data.get(index_slot, [])
    if not isinstance(items, list):
        return data

    for item in items:
        if not isinstance(item, dict):
            continue
        for slot_name in multivalued_slots:
            if slot_name in item:
                value = item[slot_name]
                # Convert [None] or [null] to None (omit the key)
                if isinstance(value, list) and len(value) == 1 and value[0] is None:
                    del item[slot_name]
                # Also clean up lists that contain only None values
                elif isinstance(value, list):
                    cleaned = [v for v in value if v is not None]
                    if not cleaned:
                        del item[slot_name]
                    elif cleaned != value:
                        item[slot_name] = cleaned

    return data


def get_configmap(schemaview: SchemaView, index_slot: SlotDefinitionName) -> CONFIGMAP:
    """
    Generates a configuration that specifies mapping between a CSV and a JSON structure

    See json_flattener docs for more details

    :param schemaview: LinkML schema view over schema
    :param index_slot: key that indexes the top level object
    :return: mapping between top level keys and denormalization configurations
    """
    slot = None
    if index_slot is not None and schemaview is not None:
        slot = schemaview.get_slot(index_slot)

    if slot is not None:
        if slot.range is not None and slot.range in schemaview.all_classes():
            cm = {}
            for sn in schemaview.class_slots(slot.range):
                config = _get_key_config(schemaview, slot.range, sn)
                if config is not None:
                    cm[sn] = config
            return cm
        else:
            logger.warning(f"Index slot range not to class: {slot.range}")
    else:
        logger.warning("Index slot or schema not specified")
    return {}


def _get_key_config(schemaview: SchemaView, tgt_cls: ClassDefinitionName, sn: SlotDefinitionName, sep="_"):
    """
    Generate a KeyConfig for a slot that tells json-flattener how to handle it.

    Returns KeyConfig for:
    - Class-ranged inlined slots (existing behavior)
    - Multivalued primitive slots (string[], integer[], etc.)

    :param schemaview: LinkML schema view
    :param tgt_cls: Target class containing the slot
    :param sn: Slot name
    :param sep: Separator for denormalized column names
    :return: KeyConfig or None
    """
    slot = schemaview.induced_slot(sn, tgt_cls)
    range = slot.range
    all_cls = schemaview.all_classes()
    if range in all_cls and schemaview.is_inlined(slot):
        # Class-ranged inlined slot - flatten nested structure
        mappings = {}
        has_nested_multivalued = False
        for inner_sn in schemaview.class_slots(range):
            denormalized_sn = f"{sn}{sep}{inner_sn}"
            mappings[inner_sn] = denormalized_sn
            inner_slot = schemaview.induced_slot(inner_sn, range)
            inner_slot_range = inner_slot.range
            if inner_slot.multivalued:
                # Nested multivalued fields can't be properly tracked in bracket-free format
                has_nested_multivalued = True
            elif inner_slot_range in all_cls and inner_slot.inlined:
                # Deeply nested inlined objects also require JSON serialization
                has_nested_multivalued = True
        if has_nested_multivalued:
            # Use JSON-only serialization for objects with nested multivalued fields
            # This avoids issues with bracket-free list parsing for nested fields
            serializers = [Serializer.json]
            return KeyConfig(
                is_list=slot.multivalued, delete=True, flatten=False, mappings={}, serializers=serializers
            )
        else:
            # Simple nested objects can be flattened
            return KeyConfig(
                is_list=slot.multivalued, delete=True, flatten=True, mappings=mappings, serializers=[]
            )
    elif slot.multivalued:
        # Multivalued primitive slot (string[], integer[], enum[], etc.)
        # Tell json-flattener this field is a list so it splits on pipe delimiter
        return KeyConfig(is_list=True)
    else:
        return None
