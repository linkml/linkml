import os
from types import ModuleType
from typing import Optional, Tuple, Dict, Any

import jsonpatch
import yaml

def compare_dicts(expected: Dict[str, Any], actual: Dict[str, Any]) -> Optional[str]:
    """
    Compare two dicts
    :param expected: expected yaml -- can either be yaml text or a file name
    :param actual: generated yaml -- text or file name
    :param expected_path: path where expected will be stored
    :return: Differences or issues if any, else None
    """
    patches = jsonpatch.make_patch(expected, actual)
    return " ".join([str(p) for p in patches])


def compare_yaml(expected: str, actual: str) -> Optional[str]:
    with open(expected) as expected_stream:
        expected_obj = yaml.load(expected_stream)
    with open(actual) as actual_stream:
        actual_obj = yaml.load(actual_stream)
    return compare_dicts(expected_obj, actual_obj)
