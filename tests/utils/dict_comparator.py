import os
from types import ModuleType
from typing import Optional, Tuple, Dict, Any, Union

import jsonpatch
import yaml
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot


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


def compare_yaml(expected: Union[str, Dict], actual: Union[str, Dict]) -> Optional[str]:
    if isinstance(expected, str):
        with open(expected) as expected_stream:
            expected_obj = yaml.load(expected_stream)
    else:
        expected_obj = expected
    if isinstance(actual, str):
        with open(actual) as actual_stream:
            actual_obj = yaml.load(actual_stream)
    else:
        actual_obj = actual
    return compare_dicts(expected_obj, actual_obj)

def compare_objs(expected: YAMLRoot, actual: YAMLRoot) -> Optional[str]:
    expected_obj = yaml.load(yaml_dumper.dumps(expected))
    actual_obj = yaml.load(yaml_dumper.dumps(actual))
    return compare_dicts(expected_obj, actual_obj)
