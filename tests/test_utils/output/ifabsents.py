# Auto generated from ifabsents.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:26
# Schema: ifabsent
#
# id: http://example.org/tests/ifabsent
# description:
# license:

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
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
TEST = CurieNamespace('test', 'http://example.org/test/')
XSD = CurieNamespace('xsd', 'http://example.org/UNKNOWN/xsd/')
DEFAULT_ = TEST


# Types
class String(str):
    """ A character string """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = TEST.String


# Class references



@dataclass
class C1(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.C1
    class_class_curie: ClassVar[str] = "test:C1"
    class_name: ClassVar[str] = "c1"
    class_model_uri: ClassVar[URIRef] = TEST.C1

    s1: Optional[str] = True
    s1p: Optional[str] = True
    s2: Optional[str] = False
    s2p: Optional[str] = False
    slot_uri: Optional[str] = None
    slot_curie: Optional[str] = None
    class_uri: Optional[str] = None
    class_curie: Optional[str] = None
    bnode: Optional[str] = bnode()
    txt: Optional[str] = "penguins\"doves"
    int: Optional[str] = -1403
    dfltrange: Optional[str] = None
    dfltns: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.s1 is not None and not isinstance(self.s1, str):
            self.s1 = str(self.s1)

        if self.s1p is not None and not isinstance(self.s1p, str):
            self.s1p = str(self.s1p)

        if self.s2 is not None and not isinstance(self.s2, str):
            self.s2 = str(self.s2)

        if self.s2p is not None and not isinstance(self.s2p, str):
            self.s2p = str(self.s2p)

        if self.slot_uri is not None and not isinstance(self.slot_uri, str):
            self.slot_uri = str(self.slot_uri)

        if self.slot_curie is not None and not isinstance(self.slot_curie, str):
            self.slot_curie = str(self.slot_curie)

        if self.class_uri is not None and not isinstance(self.class_uri, str):
            self.class_uri = str(self.class_uri)

        if self.class_curie is not None and not isinstance(self.class_curie, str):
            self.class_curie = str(self.class_curie)

        if self.bnode is not None and not isinstance(self.bnode, str):
            self.bnode = str(self.bnode)

        if self.txt is not None and not isinstance(self.txt, str):
            self.txt = str(self.txt)

        if self.int is not None and not isinstance(self.int, str):
            self.int = str(self.int)

        if self.dfltrange is not None and not isinstance(self.dfltrange, str):
            self.dfltrange = str(self.dfltrange)

        if self.dfltns is not None and not isinstance(self.dfltns, str):
            self.dfltns = str(self.dfltns)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.s1 = Slot(uri=TEST.s1, name="s1", curie=TEST.curie('s1'),
                   model_uri=TEST.s1, domain=None, range=Optional[str])

slots.s1p = Slot(uri=TEST.s1p, name="s1p", curie=TEST.curie('s1p'),
                   model_uri=TEST.s1p, domain=None, range=Optional[str])

slots.s2 = Slot(uri=TEST.s2, name="s2", curie=TEST.curie('s2'),
                   model_uri=TEST.s2, domain=None, range=Optional[str])

slots.s2p = Slot(uri=TEST.s2p, name="s2p", curie=TEST.curie('s2p'),
                   model_uri=TEST.s2p, domain=None, range=Optional[str])

slots.slot_uri = Slot(uri=TEST.slot_uri, name="slot_uri", curie=TEST.curie('slot_uri'),
                   model_uri=TEST.slot_uri, domain=None, range=Optional[str])

slots.slot_curie = Slot(uri=TEST.slot_curie, name="slot_curie", curie=TEST.curie('slot_curie'),
                   model_uri=TEST.slot_curie, domain=None, range=Optional[str])

slots.class_uri = Slot(uri=TEST.class_uri, name="class_uri", curie=TEST.curie('class_uri'),
                   model_uri=TEST.class_uri, domain=None, range=Optional[str])

slots.class_curie = Slot(uri=TEST.class_curie, name="class_curie", curie=TEST.curie('class_curie'),
                   model_uri=TEST.class_curie, domain=None, range=Optional[str])

slots.bnode = Slot(uri=TEST.bnode, name="bnode", curie=TEST.curie('bnode'),
                   model_uri=TEST.bnode, domain=None, range=Optional[str])

slots.txt = Slot(uri=TEST.txt, name="txt", curie=TEST.curie('txt'),
                   model_uri=TEST.txt, domain=None, range=Optional[str])

slots.int = Slot(uri=TEST.int, name="int", curie=TEST.curie('int'),
                   model_uri=TEST.int, domain=None, range=Optional[str])

slots.dfltrange = Slot(uri=TEST.dfltrange, name="dfltrange", curie=TEST.curie('dfltrange'),
                   model_uri=TEST.dfltrange, domain=None, range=Optional[str])

slots.dfltns = Slot(uri=TEST.dfltns, name="dfltns", curie=TEST.curie('dfltns'),
                   model_uri=TEST.dfltns, domain=None, range=Optional[str])