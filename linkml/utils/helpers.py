import re
from functools import lru_cache
from typing import Union

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ElementName,
    SlotDefinition,
)


def remove_duplicates(lst):
    """Remove duplicate tuples from a list of tuples."""
    return [t for t in (set(tuple(i) for i in lst))]


def write_to_file(file_path, data, mode="w", encoding="utf-8"):
    with open(file_path, mode, encoding=encoding) as f:
        f.write(data)


def convert_to_snake_case(str):
    str = re.sub(r"(?<=[a-z])(?=[A-Z])|[^a-zA-Z]", " ", str).strip().replace(" ", "_")
    return "".join(str.lower())


@lru_cache(None)
def get_range_associated_slots(
    schemaview: SchemaView, range_class: ClassDefinition
) -> tuple[Union[SlotDefinition, None], Union[SlotDefinition, None], Union[list[SlotDefinition], None]]:
    if isinstance(range_class, ElementName):
        range_class = schemaview.get_class(range_class)
    if range_class is None:
        return None, None, None

    range_class_id_slot = schemaview.get_identifier_slot(range_class.name, use_key=True)
    if range_class_id_slot is None:
        return None, None, None

    non_id_slots = [s for s in schemaview.class_induced_slots(range_class.name) if s.name != range_class_id_slot.name]
    non_id_required_slots = [s for s in non_id_slots if s.required]

    # Some lists of objects can be serialized as SimpleDicts.
    # A SimpleDict is serialized as simple key-value pairs where the value is atomic.
    # The key must be declared as a key, and the value must satisfy one of the following conditions:
    # 1. The value slot is the only other slot in the object other than the key
    # 2. The value slot is explicitly annotated as a simple_dict_value
    # 3. The value slot is the only non-key that is required
    # See also: https://github.com/linkml/linkml/issues/1250
    range_simple_dict_value_slot = None
    if len(non_id_slots) == 1:
        range_simple_dict_value_slot = non_id_slots[0]
    elif len(non_id_slots) > 1:
        candidate_non_id_slots = []
        for non_id_slot in non_id_slots:
            if isinstance(non_id_slot.annotations, dict):
                is_simple_dict_value = non_id_slot.annotations.get("simple_dict_value", False)
            else:
                is_simple_dict_value = getattr(non_id_slot.annotations, "simple_dict_value", False)
            if is_simple_dict_value:
                candidate_non_id_slots.append(non_id_slot)
        if len(candidate_non_id_slots) == 1:
            range_simple_dict_value_slot = candidate_non_id_slots[0]
        else:
            candidate_non_id_slots = []
            for non_id_slot in non_id_slots:
                if non_id_slot.required:
                    candidate_non_id_slots.append(non_id_slot)
            if len(candidate_non_id_slots) == 1:
                range_simple_dict_value_slot = candidate_non_id_slots[0]

    return range_class_id_slot, range_simple_dict_value_slot, non_id_required_slots


def is_simple_dict(schemaview: SchemaView, slot: SlotDefinition) -> bool:
    if not slot.multivalued or not slot.inlined or slot.inlined_as_list:
        return False
    else:
        _, range_simple_dict_value_slot, _ = get_range_associated_slots(schemaview, slot.range)
        return range_simple_dict_value_slot is not None
