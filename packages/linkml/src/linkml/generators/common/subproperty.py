"""Utilities for handling subproperty_of constraints in generators.

The `subproperty_of` metamodel property constrains slot values to descendants
of a specified parent slot. These utilities provide shared logic for:
- Detecting URI-like range types (uri, uriorcurie, curie)
- Formatting slot values according to range type
- Collecting and deduplicating slot hierarchy values
"""

from typing import Optional

from linkml_runtime.linkml_model.meta import SlotDefinition
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.schemaview import SchemaView

# Standard type sets for URI-like ranges
CURIE_TYPES: frozenset[str] = frozenset({"uriorcurie", "curie"})
URI_TYPES: frozenset[str] = frozenset({"uri"})


def is_uri_range(sv: SchemaView, range_type: Optional[str]) -> bool:
    """
    Check if range type is URI-like (uri, uriorcurie, curie, or descendant).

    :param sv: SchemaView for type ancestry lookup
    :param range_type: The range type to check
    :return: True if range type is URI-like
    """
    if range_type is None:
        return False

    if range_type in CURIE_TYPES or range_type in URI_TYPES:
        return True

    if range_type in sv.all_types():
        type_ancestors = set(sv.type_ancestors(range_type))
        if type_ancestors & CURIE_TYPES or type_ancestors & URI_TYPES:
            return True

    return False


def is_curie_range(sv: SchemaView, range_type: Optional[str]) -> bool:
    """
    Check if range type is specifically CURIE-like (not full URI).

    Returns True for uriorcurie, curie, or types that inherit from them.
    Returns False for uri types (which should expand to full URIs).

    :param sv: SchemaView for type ancestry lookup
    :param range_type: The range type to check
    :return: True if range type is CURIE-like
    """
    if range_type is None:
        return False

    if range_type in CURIE_TYPES:
        return True

    if range_type in sv.all_types():
        type_ancestors = set(sv.type_ancestors(range_type))
        if type_ancestors & CURIE_TYPES:
            return True

    return False


def format_slot_value_for_range(sv: SchemaView, slot_name: str, range_type: Optional[str]) -> str:
    """
    Format slot value according to the declared range type.

    Uses slot_uri to generate proper CURIEs (e.g., biolink:related_to)
    rather than just slot names.

    :param sv: SchemaView for slot and type lookup
    :param slot_name: Name of the slot
    :param range_type: The range type (string, uriorcurie, uri, or None)
    :return: Formatted slot value
    """
    slot = sv.get_slot(slot_name)

    if range_type is None:
        return underscore(slot_name)

    # Check if range_type itself is a URI-like type
    if range_type in CURIE_TYPES:
        # Return as CURIE using slot_uri: biolink:related_to
        return sv.get_uri(slot, expand=False)
    elif range_type in URI_TYPES:
        # Return as full URI: https://w3id.org/biolink/vocab/related_to
        return sv.get_uri(slot, expand=True)

    # Check if range_type inherits from a URI-like type (when linkml:types is imported)
    if range_type in sv.all_types():
        type_ancestors = set(sv.type_ancestors(range_type))

        if type_ancestors & CURIE_TYPES:
            # Return as CURIE using slot_uri: biolink:related_to
            return sv.get_uri(slot, expand=False)
        elif type_ancestors & URI_TYPES:
            # Return as full URI: https://w3id.org/biolink/vocab/related_to
            return sv.get_uri(slot, expand=True)

    # Return as snake_case string: related_to
    return underscore(slot_name)


def get_subproperty_values(
    sv: SchemaView,
    slot: SlotDefinition,
    expand_uri: Optional[bool] = None,
) -> list[str]:
    """
    Get all valid string values from slot hierarchy for subproperty_of constraint.

    Following metamodel semantics: "any ontological child (related to X via
    an is_a relationship), is a valid value for the slot"

    :param sv: SchemaView for slot hierarchy lookup
    :param slot: SlotDefinition with subproperty_of set
    :param expand_uri: If True, return full URIs; if False, return CURIEs;
                       if None, determine from range type
    :return: Sorted, deduplicated list of formatted values
    """
    if not slot.subproperty_of:
        return []

    root_slot_name = slot.subproperty_of
    descendants = sv.slot_descendants(root_slot_name, reflexive=True)

    values = []
    for slot_name in descendants:
        if expand_uri is not None:
            descendant_slot = sv.get_slot(slot_name)
            value = sv.get_uri(descendant_slot, expand=expand_uri)
        else:
            value = format_slot_value_for_range(sv, slot_name, slot.range)
        values.append(value)

    # Remove duplicates while preserving order, then sort
    return sorted(list(dict.fromkeys(values)))
