import json
from datetime import datetime, date
from decimal import Decimal
from typing import Union
from pydantic import BaseModel

from deprecated.classic import deprecated

from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.utils import formatutils
from linkml_runtime.utils.context_utils import CONTEXTS_PARAM_TYPE
from linkml_runtime.utils.formatutils import remove_empty_items
from linkml_runtime.utils.yamlutils import YAMLRoot, as_json_object
from jsonasobj2 import JsonObj


class JSONDumper(Dumper):

    def dump(self, element: Union[BaseModel, YAMLRoot], to_file: str, contexts: CONTEXTS_PARAM_TYPE = None,
             **kwargs) -> None:
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
        if isinstance(element, BaseModel):
            element = element.model_dump()
        super().dump(element, to_file, contexts=contexts, **kwargs)

    def dumps(self, element: Union[BaseModel, YAMLRoot], contexts: CONTEXTS_PARAM_TYPE = None, inject_type=True) -> str:
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
        :param inject_type: if True (default), add a @type at the top level
        :return: JSON Object representing the element
        """

        def default(o):
            if isinstance(o, BaseModel):
                return remove_empty_items(o.model_dump(), hide_protected_keys=True)
            if isinstance(o, YAMLRoot):
                return remove_empty_items(o, hide_protected_keys=True)
            elif isinstance(o, Decimal):
                # https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object
                return str(o)
            elif isinstance(o, (datetime, date)):
                return str(o)
            else:
                return json.JSONDecoder().decode(o)
        if isinstance(element, BaseModel):
            element = element.model_dump()
        return json.dumps(as_json_object(element, contexts, inject_type=inject_type),
                          default=default,
                          ensure_ascii=False,
                          indent='  ')

    @staticmethod
    @deprecated("Use `utils/formatutils/remove_empty_items` instead")
    def remove_empty_items(obj: dict) -> dict:
        """
        Remove empty items from obj
        :param obj:
        :return: copy of dictionary with empty lists/dicts and Nones removed
        """
        return formatutils.remove_empty_items(obj, hide_protected_keys=True)

    def to_json_object(self, element: Union[BaseModel, YAMLRoot], contexts: CONTEXTS_PARAM_TYPE = None,
                       inject_type=True) -> JsonObj:
        """
        As dumps(), except returns a JsonObj, not a string

        :param element: LinkML object to be emitted
        :param contexts: JSON-LD context(s) in the form of:
            * file name
            * URL
            * JSON String
            * dict
            * JSON Object
            * A list containing elements of any type named above
        :param inject_type: if True (default), add a @type at the top level
        :return: JSON Object representing the element
        """
        return as_json_object(element, contexts, inject_type=inject_type)

    def to_dict(self, element: Union[BaseModel, YAMLRoot], **kwargs) -> JsonObj:
        """
        As dumps(), except returns a JsonObj, not a string

        :param element: LinkML object to be emitted
        :param contexts: JSON-LD context(s) in the form of:
            * file name
            * URL
            * JSON String
            * dict
            * JSON Object
            * A list containing elements of any type named above
        :param inject_type: if True (default), add a @type at the top level
        :return: JSON Object representing the element
        """
        return json.loads(self.dumps(element, inject_type=False, **kwargs))
