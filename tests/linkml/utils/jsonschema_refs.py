"""A helper for tests that check the ``$ref`` values of generated JSON Schema documents."""

from typing import Any


def all_refs(node: Any) -> list[str]:
    """Return every ``$ref`` value in a generated JSON Schema document, examples included."""
    if isinstance(node, dict):
        return [value for key, value in node.items() if key == "$ref"] + [
            ref for value in node.values() for ref in all_refs(value)
        ]
    if isinstance(node, list):
        return [ref for value in node for ref in all_refs(value)]
    return []
