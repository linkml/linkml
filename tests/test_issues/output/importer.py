# Auto generated from importer.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: importer
#
# id: https://example.org/importer
# description: Test of local import with an identifier
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
from . importee import Base, BaseId, String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
EX = CurieNamespace('ex', 'https://example.org/importee/')
DEFAULT_ = EX


# Types

# Class references
class ChildId(BaseId):
    pass


@dataclass
class Child(Base):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Child
    class_class_curie: ClassVar[str] = "ex:Child"
    class_name: ClassVar[str] = "child"
    class_model_uri: ClassVar[URIRef] = EX.Child

    id: Union[str, ChildId] = None
    value: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ChildId):
            self.id = ChildId(self.id)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

