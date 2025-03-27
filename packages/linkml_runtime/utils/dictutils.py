import json

from linkml_runtime.dumpers import json_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot

def as_simple_dict(element: YAMLRoot) -> dict:
    """
    Returns the representation of element as a python dictionary

    :param element: element to return
    :return: simple python dictionary
    """
    obj = json_dumper.dumps(element=element, inject_type=False)
    return json.loads(obj)
