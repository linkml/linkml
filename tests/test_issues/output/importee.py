# Auto generated from importee.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: importee
#
# id: https://example.org/importee
# description: A minimal element to import
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace


metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
EX = CurieNamespace('ex', 'https://example.org/importee/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = EX


# Types
class String(str):
    """ A character string """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = EX.String


# Class references
class BaseId(extended_str):
    pass


@dataclass
class Base(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Base
    class_class_curie: ClassVar[str] = "ex:Base"
    class_name: ClassVar[str] = "base"
    class_model_uri: ClassVar[URIRef] = EX.Base

    id: Union[str, BaseId] = None
    value: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BaseId):
            self.id = BaseId(self.id)

        if self._is_empty(self.value):
            self.MissingRequiredField("value")
        if not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=EX.id, name="id", curie=EX.curie('id'),
                   model_uri=EX.id, domain=None, range=URIRef)

slots.value = Slot(uri=EX.value, name="value", curie=EX.curie('value'),
                   model_uri=EX.value, domain=None, range=str)