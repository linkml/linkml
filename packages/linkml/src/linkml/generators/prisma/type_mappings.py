"""
Type mapping utilities for LinkML to Prisma schema generation.

Maps LinkML types to Prisma scalar types and generates field modifiers.
"""

from typing import Optional

from linkml_runtime.linkml_model.meta import SlotDefinition

PRISMA_RANGEMAP = {
    "string": "String",
    "integer": "Int",
    "boolean": "Boolean",
    "float": "Float",
    "double": "Float",
    "decimal": "Decimal",
    "date": "DateTime",
    "datetime": "DateTime",
    "time": "String",
    "json": "Json",
    "uri": "String",
    "uriorcurie": "String",
    "ncname": "String",
    "bytes": "Bytes",
}


def get_prisma_type(linkml_range: str, is_multivalued: bool = False, use_scalar_arrays: bool = True) -> str:
    """
    Map LinkML range to Prisma type.

    Args:
        linkml_range: LinkML type or class name
        is_multivalued: Whether the slot is multivalued
        use_scalar_arrays: Whether to use Prisma scalar arrays (String[]) for multivalued scalars

    Returns:
        Prisma type string (e.g., "String", "Int", "String[]")
    """
    base_type = PRISMA_RANGEMAP.get(linkml_range, linkml_range)

    if is_multivalued and use_scalar_arrays:
        return f"{base_type}[]"
    return base_type


def get_prisma_modifiers(slot: SlotDefinition, is_identifier: bool = False, is_required: bool = False) -> str:
    """
    Generate Prisma field modifiers for a slot.

    Args:
        slot: LinkML slot definition
        is_identifier: Whether this slot is an identifier/primary key
        is_required: Whether this slot is required

    Returns:
        Space-separated string of Prisma modifiers (e.g., "@id @default(autoincrement())")
    """
    modifiers = []

    if is_identifier:
        modifiers.append("@id")

    # Add unique modifier if slot is marked as unique
    if getattr(slot, "identifier", False) and not is_identifier:
        modifiers.append("@unique")

    # Add default value modifiers
    # Note: This is a simplified implementation
    # Full implementation would handle default values from slot.ifabsent

    return " ".join(modifiers)


def is_optional_field(slot: SlotDefinition, is_required: bool = False) -> bool:
    """
    Determine if a field should be optional in Prisma (marked with ?).

    Args:
        slot: LinkML slot definition
        is_required: Whether the slot is explicitly required

    Returns:
        True if the field should be optional (?) in Prisma
    """
    # In Prisma, fields are required by default
    # We add ? for optional fields
    return not is_required and not slot.required
