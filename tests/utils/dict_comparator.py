from pathlib import Path
from typing import Any, Dict, Optional, Union

import jsonpatch
import yaml
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.formatutils import remove_empty_items
from linkml_runtime.utils.yamlutils import YAMLRoot


def compare_dicts(expected: Dict[str, Any], actual: Dict[str, Any]) -> Optional[str]:
    """
    Compare two dicts
    :param expected: expected yaml -- can either be yaml text or a file name
    :param actual: generated yaml -- text or file name
    :return: Differences or issues if any, else None
    """
    patches = jsonpatch.make_patch(expected, actual)
    return " ".join([str(p) for p in patches])


def compare_yaml(
    expected: Union[str, Dict, Path], actual: Union[str, Dict, Path], remove_empty: bool = False
) -> Optional[str]:
    if isinstance(expected, (str, Path)):
        with open(expected) as expected_stream:
            expected_obj = yaml.safe_load(expected_stream)
    else:
        expected_obj = expected
    if isinstance(actual, (str, Path)):
        with open(actual) as actual_stream:
            actual_obj = yaml.safe_load(actual_stream)
    else:
        actual_obj = actual

    if remove_empty:
        expected_obj = remove_empty_items(expected_obj)
        actual_obj = remove_empty_items(actual_obj)

    return compare_dicts(expected_obj, actual_obj)


def compare_objs(expected: YAMLRoot, actual: YAMLRoot) -> Optional[str]:
    expected_obj = yaml.safe_load(yaml_dumper.dumps(expected))
    actual_obj = yaml.safe_load(yaml_dumper.dumps(actual))
    return compare_dicts(expected_obj, actual_obj)
