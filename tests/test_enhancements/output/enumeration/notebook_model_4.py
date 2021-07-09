# Auto generated from notebook_model_4.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: simple
#
# id: http://example.org/test/simple
# description: Very simple enumeration
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
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
CS = CurieNamespace('CS', 'http://ontologies-r.us/codesystem/')
SCT = CurieNamespace('SCT', 'http://snomed.info/id/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PLAY = CurieNamespace('play', 'http://example.org/test/play/')
DEFAULT_ = PLAY


# Types

# Class references
class FavoriteColorId(extended_str):
    pass


@dataclass
class FavoriteColor(YAMLRoot):
    id: Union[str, FavoriteColorId] = None
    position: Union[str, "Colors"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, FavoriteColorId):
            self.id = FavoriteColorId(self.id)

        if self._is_empty(self.position):
            self.MissingRequiredField("position")
        if not isinstance(self.position, Colors):
            self.position = Colors(self.position)

        super().__post_init__(**kwargs)


# Enumerations
class Colors(EnumDefinitionImpl):
    """
    Color values, mapped to SNOMED CT
    """
    _defn = EnumDefinition(
        name="Colors",
        description="Color values, mapped to SNOMED CT",
        code_set=CS.SCT,
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "1",
                PermissibleValue(text="1",
                                 description="Red",
                                 meaning=SCT["371240000"]) )
        setattr(cls, "2",
                PermissibleValue(text="2",
                                 description="Yellow",
                                 meaning=SCT["371244009"]) )
        setattr(cls, "3",
                PermissibleValue(text="3",
                                 meaning=SCT["405738005"]) )
        setattr(cls, "4",
                PermissibleValue(text="4",
                                 description="Muted",
                                 meaning=SCT.abcde) )
        setattr(cls, "9",
                PermissibleValue(text="9",
                                 description="Muddy") )

# Slots
