# Auto generated from importee.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-03-26 14:21
# Schema: importee
#
# id: https://example.org/importee
# description: A minimal element to import
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml.utils.slot import Slot
from linkml.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml.utils.formatutils import camelcase, underscore, sfx
from linkml.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml.utils.curienamespace import CurieNamespace


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
        if self.id is None:
            raise ValueError("id must be supplied")
        if not isinstance(self.id, BaseId):
            self.id = BaseId(self.id)

        if self.value is None:
            raise ValueError("value must be supplied")
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