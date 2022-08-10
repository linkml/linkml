# Auto generated from ifabsent_uri.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-01-27T02:56:37
# Schema: ifabsent
#
# id: http://example.org/tests/ifabsent
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
import sys
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import JsonObj, as_dict
from linkml_runtime.linkml_model.meta import (EnumDefinition, PermissibleValue,
                                              PvFormulaOptions)
from linkml_runtime.linkml_model.types import String
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import \
    dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import bnode, empty_dict, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (YAMLRoot, extended_float,
                                            extended_int, extended_str)
from rdflib import Namespace, URIRef

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
TEST = CurieNamespace('test', 'http://example.org/tests/ifabsent/')
DEFAULT_ = TEST


# Types

# Class references



@dataclass
class C1(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.C1
    class_class_curie: ClassVar[str] = "test:C1"
    class_name: ClassVar[str] = "c1"
    class_model_uri: ClassVar[URIRef] = TEST.C1

    s1: Optional[str] = SKOS.label
    s2: Optional[str] = SKOS.definition

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.s1 is not None and not isinstance(self.s1, str):
            self.s1 = str(self.s1)

        if self.s2 is not None and not isinstance(self.s2, str):
            self.s2 = str(self.s2)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.s1 = Slot(uri=TEST.s1, name="s1", curie=TEST.curie('s1'),
                   model_uri=TEST.s1, domain=None, range=Optional[str])

slots.s2 = Slot(uri=TEST.s2, name="s2", curie=TEST.curie('s2'),
                   model_uri=TEST.s2, domain=None, range=Optional[str])