# Auto generated from linkml_issue_463.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-03-02T04:15:57
# Schema: test
#
# id: https://w3id.org/linkml/examples/test
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
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
EX = CurieNamespace('ex', 'http://example.org/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = EX


# Types

# Class references



@dataclass
class Contained(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Contained
    class_class_curie: ClassVar[str] = "ex:Contained"
    class_name: ClassVar[str] = "Contained"
    class_model_uri: ClassVar[URIRef] = EX.Contained

    type: Union[dict, "TypeObj"] = None
    label: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, TypeObj):
            self.type = TypeObj(**as_dict(self.type))

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass
class Container(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Container
    class_class_curie: ClassVar[str] = "ex:Container"
    class_name: ClassVar[str] = "Container"
    class_model_uri: ClassVar[URIRef] = EX.Container

    contains: Optional[Union[Union[dict, Contained], List[Union[dict, Contained]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.contains, list):
            self.contains = [self.contains] if self.contains is not None else []
        self.contains = [v if isinstance(v, Contained) else Contained(**as_dict(v)) for v in self.contains]

        super().__post_init__(**kwargs)


@dataclass
class TypeObj(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.TypeObj
    class_class_curie: ClassVar[str] = "ex:TypeObj"
    class_name: ClassVar[str] = "TypeObj"
    class_model_uri: ClassVar[URIRef] = EX.TypeObj

    label: Optional[str] = None
    system: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.system is not None and not isinstance(self.system, str):
            self.system = str(self.system)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.type = Slot(uri=EX.type, name="type", curie=EX.curie('type'),
                   model_uri=EX.type, domain=None, range=Union[dict, TypeObj])

slots.label = Slot(uri=EX.label, name="label", curie=EX.curie('label'),
                   model_uri=EX.label, domain=None, range=Optional[str])

slots.system = Slot(uri=EX.system, name="system", curie=EX.curie('system'),
                   model_uri=EX.system, domain=None, range=Optional[str])

slots.contains = Slot(uri=EX.contains, name="contains", curie=EX.curie('contains'),
                   model_uri=EX.contains, domain=None, range=Optional[Union[Union[dict, Contained], List[Union[dict, Contained]]]])