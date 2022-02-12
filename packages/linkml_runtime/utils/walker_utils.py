"""
Utilities for walking object trees
"""

from copy import deepcopy
from typing import Callable, Union, List, Dict, Any

from linkml_runtime.utils.yamlutils import YAMLRoot


def traverse_object_tree(obj: YAMLRoot, func: Callable, mutate: bool = True) -> Any:
    """
    Recursively walk object tree, transforming each object using passed in function

    :param obj: input object
    :param func: function applies to each object returning transformed object
    :param mutate: if true (default), the object may be mutated
    :return: transformed object
    """
    return _traverse_object_tree_1(obj, func, mutate)


# implementation for traverse_object_tree, but also accepts lists, dicts
def _traverse_object_tree_1(obj: Union[YAMLRoot, List, Dict], func: Callable,
                            mutate: bool = True) -> Any:
    if isinstance(obj, list):
        return [_traverse_object_tree_1(x, func, mutate) for x in obj]
    elif isinstance(obj, dict):
        return {k: _traverse_object_tree_1(v, func, mutate) for k, v in obj.items()}
    elif isinstance(obj, YAMLRoot):
        if not mutate:
            # make a copy, this copy is intentionally mutated from here
            obj = deepcopy(obj)
        for v in vars(obj).values():
            if v is not None:
                _traverse_object_tree_1(v, func, True)
        obj = func(obj)
        return obj
    else:
        return obj
