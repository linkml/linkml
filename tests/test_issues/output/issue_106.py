# Auto generated from issue_106.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: test_106
#
# id: https://issue_test/106/schema
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
XSD = CurieNamespace('xsd', 'http://example.org/UNKNOWN/xsd/')
DEFAULT_ = CurieNamespace('', 'https://issue_test/106/schema/')


# Types
class String(str):
    """ A character string """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = URIRef("https://issue_test/106/schema/String")


# Class references



@dataclass
class C1(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://issue_test/106/schema/C1")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "c1"
    class_model_uri: ClassVar[URIRef] = URIRef("https://issue_test/106/schema/C1")

    s1: Optional[str] = None
    s2: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.s1 is not None and not isinstance(self.s1, str):
            self.s1 = str(self.s1)

        if self.s2 is not None and not isinstance(self.s2, str):
            self.s2 = str(self.s2)

        super().__post_init__(**kwargs)


@dataclass
class C2(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://issue_test/106/schema/C2")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "c2"
    class_model_uri: ClassVar[URIRef] = URIRef("https://issue_test/106/schema/C2")

    s1: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.s1 is not None and not isinstance(self.s1, str):
            self.s1 = str(self.s1)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.s1 = Slot(uri=DEFAULT_.s1, name="s1", curie=DEFAULT_.curie('s1'),
                   model_uri=DEFAULT_.s1, domain=None, range=Optional[str])

slots.s2 = Slot(uri=DEFAULT_.s2, name="s2", curie=DEFAULT_.curie('s2'),
                   model_uri=DEFAULT_.s2, domain=None, range=Optional[str])