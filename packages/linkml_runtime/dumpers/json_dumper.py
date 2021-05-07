import json
from typing import Dict
from jsonasobj2 import items, JsonObj, as_dict

from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.utils.context_utils import CONTEXTS_PARAM_TYPE
from linkml_runtime.utils.yamlutils import YAMLRoot, as_json_object


class JSONDumper(Dumper):

    def dump(self, element: YAMLRoot, to_file: str, contexts: CONTEXTS_PARAM_TYPE = None) -> None:
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
        super().dump(element, to_file, contexts=contexts)

    def dumps(self, element: YAMLRoot, contexts: CONTEXTS_PARAM_TYPE = None) -> str:
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
        return json.dumps(as_json_object(element, contexts),
                          default=lambda o: self.remove_empty_items(o) if isinstance(o, YAMLRoot) else json.JSONDecoder().decode(o),
                          indent='  ')


    @staticmethod
    def remove_empty_items(obj: Dict) -> Dict:
        """
        Remove empty items from obj
        :param obj:
        :return: copy of dictionary with empty lists/dicts and Nones removed
        """
        return {k: as_dict(v) if isinstance(v, JsonObj) else v
                for k, v in items(obj) if not (v is None or v == [] or v == {})}
