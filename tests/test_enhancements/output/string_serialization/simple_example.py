# Auto generated from simple_example.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: example.org
#
# id: http://example.org
# description:
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
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = CurieNamespace('', 'http://example.org/')


# Types

# Class references



@dataclass
class C(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/C")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "c"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/C")

    s: Optional[str] = None
    t: Optional[str] = None
    as_str: Optional[str] = None
    as_str2: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.s is not None and not isinstance(self.s, str):
            self.s = str(self.s)

        if self.t is not None and not isinstance(self.t, str):
            self.t = str(self.t)

        if self.as_str is not None and not isinstance(self.as_str, str):
            self.as_str = str(self.as_str)

        if self.as_str2 is not None and not isinstance(self.as_str2, str):
            self.as_str2 = str(self.as_str2)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.s = Slot(uri=DEFAULT_.s, name="s", curie=DEFAULT_.curie('s'),
                   model_uri=DEFAULT_.s, domain=None, range=Optional[str])

slots.t = Slot(uri=DEFAULT_.t, name="t", curie=DEFAULT_.curie('t'),
                   model_uri=DEFAULT_.t, domain=None, range=Optional[str])

slots.as_str = Slot(uri=DEFAULT_.as_str, name="as_str", curie=DEFAULT_.curie('as_str'),
                   model_uri=DEFAULT_.as_str, domain=None, range=Optional[str])

slots.as_str2 = Slot(uri=DEFAULT_.as_str2, name="as_str2", curie=DEFAULT_.curie('as_str2'),
                   model_uri=DEFAULT_.as_str2, domain=None, range=Optional[str])