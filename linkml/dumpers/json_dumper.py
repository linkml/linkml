from typing import Dict

from linkml.utils.context_utils import CONTEXTS_PARAM_TYPE
from linkml.utils.yamlutils import YAMLRoot, as_json_object
from jsonasobj import as_json


def remove_empty_items(obj: Dict) -> Dict:
    """
    Remove empty items from obj
    :param obj:
    :return: copy of dictionary with empty lists/dicts and Nones removed
    """
    return {k: v for k, v in obj.items() if not (v is None or v == [] or v == {})}


def dump(element: YAMLRoot, to_file: str, contexts: CONTEXTS_PARAM_TYPE = None) -> None:
    """
    Write element as json to to_file
    :param element: LinkML object to be serialized as YAML
    :param to_file: file to write to
    :param contexts: JSON-LD context(s) in the form of:
        * file name
        * URL
        * JSON String
        * dict
        * JSON Object
        * A list containing elements of any type named above
    """
    with open(to_file, 'w') as outf:
        outf.write(dumps(element, contexts))


def dumps(element: YAMLRoot, contexts: CONTEXTS_PARAM_TYPE = None) -> str:
    """
    Return element as a JSON or a JSON-LD string
    :param element: LinkML object to be emitted
    :param contexts: JSON-LD context(s) in the form of:
        * file name
        * URL
        * JSON String
        * dict
        * JSON Object
        * A list containing elements of any type named above
    :return: JSON Object representing the element
    """
    return as_json(as_json_object(element, contexts), filtr=remove_empty_items, indent='  ')
