"""Shared utilities for boolean value handling in CSV/TSV serialization.

These functions are used by both the delimited file loader and dumper to
configure and apply boolean coercion consistently.
"""

import logging
from dataclasses import dataclass, field

from linkml_runtime.linkml_model.meta import SlotDefinitionName
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)

# Default truthy/falsy values following pandas/R conventions (case-insensitive).
DEFAULT_TRUTHY_VALUES = frozenset({"true", "t"})
DEFAULT_FALSY_VALUES = frozenset({"false", "f"})

# Mapping from boolean_output annotation/CLI values to (true_str, false_str).
BOOLEAN_OUTPUT_FORMATS: dict[str, tuple[str, str]] = {
    "true": ("true", "false"),
    "True": ("True", "False"),
    "TRUE": ("TRUE", "FALSE"),
    "yes": ("yes", "no"),
    "Yes": ("Yes", "No"),
    "YES": ("YES", "NO"),
    "on": ("on", "off"),
    "On": ("On", "Off"),
    "ON": ("ON", "OFF"),
    "1": ("1", "0"),
}


@dataclass
class BooleanConfig:
    """Settled configuration for boolean value handling in CSV/TSV.

    Loading (Postel's law: liberal acceptance):
        ``truthy_values`` and ``falsy_values`` are the cumulative sets of
        strings recognized as True/False during CSV/TSV loading.  Defaults
        are *extended* (not replaced) by schema annotations and CLI options.

    Dumping (Postel's law: conservative output):
        ``output_true`` and ``output_false`` control how Python booleans
        are written when dumping to CSV/TSV.
    """

    truthy_values: frozenset[str] = field(default_factory=lambda: DEFAULT_TRUTHY_VALUES)
    falsy_values: frozenset[str] = field(default_factory=lambda: DEFAULT_FALSY_VALUES)
    output_true: str = "true"
    output_false: str = "false"


def get_boolean_config(
    schemaview: SchemaView | None = None,
    *,
    boolean_truthy: frozenset[str] | None = None,
    boolean_falsy: frozenset[str] | None = None,
    boolean_output: str | None = None,
) -> BooleanConfig:
    """Build a settled BooleanConfig from schema annotations and CLI overrides.

    Resolution order for truthy/falsy (cumulative — each layer extends):
        defaults -> schema annotations -> CLI keyword arguments.

    Resolution order for output format (last wins):
        default -> schema annotation -> CLI keyword argument.

    Schema-level annotations:

    - ``boolean_truthy``: comma-separated additional truthy values (e.g. ``yes,on,1``).
    - ``boolean_falsy``: comma-separated additional falsy values (e.g. ``no,off,0``).
    - ``boolean_output``: output format key (e.g. ``true``, ``TRUE``, ``yes``, ``1``).

    Args:
        schemaview: A SchemaView for reading annotations.
        boolean_truthy: CLI-provided additional truthy values (already lowercased).
        boolean_falsy: CLI-provided additional falsy values (already lowercased).
        boolean_output: CLI override for output format key.

    Returns:
        A settled BooleanConfig.
    """
    config = BooleanConfig()

    # Schema annotations extend the defaults
    if schemaview and schemaview.schema and schemaview.schema.annotations:
        ann = schemaview.schema.annotations
        if "boolean_truthy" in ann:
            extra = frozenset(v.strip().lower() for v in ann["boolean_truthy"].value.split(",") if v.strip())
            config.truthy_values = config.truthy_values | extra
        if "boolean_falsy" in ann:
            extra = frozenset(v.strip().lower() for v in ann["boolean_falsy"].value.split(",") if v.strip())
            config.falsy_values = config.falsy_values | extra
        if "boolean_output" in ann:
            format_key = ann["boolean_output"].value
            true_str, false_str = BOOLEAN_OUTPUT_FORMATS.get(format_key, ("true", "false"))
            config.output_true = true_str
            config.output_false = false_str

    # CLI arguments extend truthy/falsy, override output
    if boolean_truthy is not None:
        config.truthy_values = config.truthy_values | boolean_truthy
    if boolean_falsy is not None:
        config.falsy_values = config.falsy_values | boolean_falsy
    if boolean_output is not None:
        true_str, false_str = BOOLEAN_OUTPUT_FORMATS.get(boolean_output, ("true", "false"))
        config.output_true = true_str
        config.output_false = false_str

    return config


def get_boolean_slots(schemaview: SchemaView, index_slot: SlotDefinitionName) -> set[str]:
    """Get slot names with ``range: boolean`` for the class targeted by index_slot.

    Args:
        schemaview: The schema view.
        index_slot: The slot that indexes the top-level objects.

    Returns:
        Set of slot names that have boolean range.
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


def coerce_boolean_values(
    obj: dict | list,
    boolean_slots: set[str],
    truthy: frozenset[str] = DEFAULT_TRUTHY_VALUES,
    falsy: frozenset[str] = DEFAULT_FALSY_VALUES,
) -> dict | list:
    """Recursively coerce string values in boolean slots to actual booleans.

    Args:
        obj: A dict or list from json-flattener unflatten.
        boolean_slots: Set of slot names that should be coerced to boolean.
        truthy: Set of lowercase strings to treat as True.
        falsy: Set of lowercase strings to treat as False.

    Returns:
        The same structure with boolean slots coerced to actual booleans.
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
                result[k] = coerce_boolean_values(v, boolean_slots, truthy, falsy)
            else:
                result[k] = v
        return result
    elif isinstance(obj, list):
        return [coerce_boolean_values(item, boolean_slots, truthy, falsy) for item in obj]
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


def convert_booleans_for_output(obj: dict | list, true_str: str, false_str: str) -> dict | list:
    """Recursively convert boolean values to the specified string format.

    Args:
        obj: A dict or list to process.
        true_str: String to use for True values.
        false_str: String to use for False values.

    Returns:
        The same structure with booleans converted to strings.
    """
    if isinstance(obj, dict):
        return {k: convert_booleans_for_output(v, true_str, false_str) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_booleans_for_output(item, true_str, false_str) for item in obj]
    elif isinstance(obj, bool):
        return true_str if obj else false_str
    else:
        return obj
