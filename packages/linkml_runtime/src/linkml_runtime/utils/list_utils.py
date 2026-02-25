"""Shared utilities for configuring multivalued field formatting in CSV/TSV serialization.

These functions are used by both the delimited file loader and dumper to read
list formatting configuration from schema annotations and apply it consistently.
"""

import logging

from json_flattener import KeyConfig

from linkml_runtime.linkml_model.meta import SlotDefinitionName
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)

# Maps list_wrapper annotation values to (open, close) marker tuples for json-flattener.
WRAPPER_STYLES: dict[str, tuple[str, str]] = {
    "square": ("[", "]"),
    "curly": ("{", "}"),
    "paren": ("(", ")"),
    "none": ("", ""),
}


def resolve_list_wrapper(wrapper: str) -> tuple[str, str]:
    """Resolve wrapper style to markers, warning and defaulting when invalid."""
    if wrapper in WRAPPER_STYLES:
        return WRAPPER_STYLES[wrapper]

    logger.warning(
        f"Invalid list_wrapper value '{wrapper}'. "
        f"Expected one of {list(WRAPPER_STYLES)}. "
        "Defaulting to 'square' (bracketed lists)."
    )
    return WRAPPER_STYLES["square"]


def get_list_config_from_annotations(
    schemaview: SchemaView,
) -> tuple[tuple[str, str], str, bool, bool]:
    """Read list formatting configuration from schema-level annotations.

    These annotations control how multivalued fields are serialized in CSV/TSV:

    - ``list_wrapper``: wrapper style around list items (default ``square``).
      Permissible values: ``square`` ``[a|b]``, ``curly`` ``{a|b}``,
      ``paren`` ``(a|b)``, ``none`` ``a|b``.
    - ``list_delimiter``: character between list items (default ``|``).
    - ``list_strip_whitespace``: strip whitespace around delimiter (default ``true``).
    - ``refuse_delimiter_in_data``: raise ValueError if a multivalued value
      contains the delimiter (default ``false``).

    Note: These are schema-level only because json-flattener's GlobalConfig
    applies the same markers/delimiter to ALL columns in the CSV/TSV.

    Args:
        schemaview: A SchemaView for reading annotations.

    Returns:
        Tuple of (csv_list_markers, csv_inner_delimiter, strip_whitespace,
        refuse_delimiter_in_data).
    """
    list_markers = ("[", "]")
    inner_delimiter = "|"
    strip_whitespace = True
    refuse_delimiter_in_data = False

    if not schemaview or not schemaview.schema:
        return list_markers, inner_delimiter, strip_whitespace, refuse_delimiter_in_data

    if schemaview.schema.annotations:
        annotations = schemaview.schema.annotations
        if "list_wrapper" in annotations:
            wrapper = annotations["list_wrapper"].value
            list_markers = resolve_list_wrapper(wrapper)
        if "list_delimiter" in annotations:
            inner_delimiter = annotations["list_delimiter"].value
        if "list_strip_whitespace" in annotations:
            value = str(annotations["list_strip_whitespace"].value).lower()
            if value not in ("true", "false"):
                logger.warning(
                    f"Invalid list_strip_whitespace value '{value}'. Expected 'true' or 'false'. Defaulting to true."
                )
            else:
                strip_whitespace = value == "true"
        if "refuse_delimiter_in_data" in annotations:
            value = str(annotations["refuse_delimiter_in_data"].value).lower()
            if value not in ("true", "false"):
                logger.warning(
                    f"Invalid refuse_delimiter_in_data value '{value}'. "
                    "Expected 'true' or 'false'. Defaulting to false."
                )
            else:
                refuse_delimiter_in_data = value == "true"

    return list_markers, inner_delimiter, strip_whitespace, refuse_delimiter_in_data


def strip_whitespace_from_lists(obj: dict | list) -> dict | list:
    """Recursively strip whitespace from string items in lists.

    This post-processes the unflattened data to strip leading/trailing
    whitespace from list items, handling cases like ``"a | b | c"`` being
    parsed as ``['a ', ' b ', ' c']``.

    Args:
        obj: A dict or list from json-flattener unflatten.

    Returns:
        The same structure with whitespace stripped from list string items.
    """
    if isinstance(obj, dict):
        return {k: strip_whitespace_from_lists(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        result = []
        for item in obj:
            if isinstance(item, str):
                result.append(item.strip())
            elif isinstance(item, dict | list):
                result.append(strip_whitespace_from_lists(item))
            else:
                result.append(item)
        return result
    else:
        return obj


def enhance_configmap_for_multivalued_primitives(
    schemaview: SchemaView,
    index_slot: SlotDefinitionName,
    configmap: dict,
    unwrapped_mode: bool = False,
) -> dict:
    """Enhance configmap with KeyConfig entries for multivalued primitive slots.

    The base ``get_configmap()`` only creates KeyConfig for class-ranged inlined
    slots. This function adds ``KeyConfig(is_list=True)`` for multivalued
    primitive slots (like ``aliases: string*``) so json-flattener knows to
    split/join on the delimiter.

    Note: ``KeyConfig(is_list=True)`` is only added when *unwrapped_mode* is
    True because in wrapped mode (e.g. ``[a|b|c]``), json-flattener already
    parses brackets correctly.

    Args:
        schemaview: The schema view.
        index_slot: The slot that indexes the top-level objects.
        configmap: The existing configmap from ``get_configmap()``.
        unwrapped_mode: If True, add KeyConfig for unwrapped list parsing.

    Returns:
        Enhanced configmap with entries for multivalued primitive slots.
    """
    if not unwrapped_mode:
        return configmap

    if schemaview is None or index_slot is None:
        return configmap

    slot = schemaview.get_slot(index_slot)
    if slot is None or slot.range is None:
        return configmap

    target_class = slot.range
    if target_class not in schemaview.all_classes():
        return configmap

    all_classes = schemaview.all_classes()

    for slot_name in schemaview.class_slots(target_class):
        if slot_name in configmap:
            continue

        induced_slot = schemaview.induced_slot(slot_name, target_class)
        if induced_slot.multivalued:
            slot_range = induced_slot.range
            if slot_range not in all_classes:
                configmap[slot_name] = KeyConfig(is_list=True)

    return configmap


def check_data_for_delimiter(
    objs: list[dict],
    delimiter: str,
    schemaview: SchemaView,
    index_slot: SlotDefinitionName,
) -> None:
    """Check that no string value in a multivalued slot contains the list delimiter.

    When ``refuse_delimiter_in_data`` is enabled, this function is called before
    serialization to prevent silent data corruption during round-tripping.

    Args:
        objs: The list of dicts about to be serialized (one dict per row).
        delimiter: The list delimiter character (e.g. ``|``).
        schemaview: The schema view for looking up slot metadata.
        index_slot: The top-level index slot name.

    Raises:
        ValueError: If any string value in a multivalued slot contains the
            delimiter.
    """
    multivalued_slots: set[str] = set()
    if schemaview is not None and index_slot is not None:
        slot = schemaview.get_slot(index_slot)
        if slot is not None and slot.range is not None:
            target_class = slot.range
            all_classes = schemaview.all_classes()
            if target_class in all_classes:
                for slot_name in schemaview.class_slots(target_class):
                    induced_slot = schemaview.induced_slot(slot_name, target_class)
                    if induced_slot.multivalued:
                        slot_range = induced_slot.range
                        if slot_range not in all_classes:
                            multivalued_slots.add(slot_name)

    if not multivalued_slots:
        return

    for obj in objs:
        for slot_name in multivalued_slots:
            values = obj.get(slot_name)
            if not isinstance(values, list):
                continue
            for value in values:
                if isinstance(value, str) and delimiter in value:
                    raise ValueError(
                        f"Multivalued slot '{slot_name}' contains a value "
                        f"that includes the list delimiter '{delimiter}': "
                        f"'{value}'. This would cause silent data corruption "
                        f"during round-tripping. Either change the delimiter, "
                        f"remove the delimiter character from the data, or "
                        f"disable refuse_delimiter_in_data."
                    )
