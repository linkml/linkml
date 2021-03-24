from typing import Any

from biolinkml.utils.yamlutils import YAMLRoot as BLYAMLRoot, TypedNode as BLTypedNode


def is_YAMLROOT(node: Any) -> bool:
    return isinstance(node, BLYAMLRoot)

def is_TypedNode(node: Any) -> bool:
    return isinstance(node, BLTypedNode)
