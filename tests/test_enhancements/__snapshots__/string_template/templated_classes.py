# Auto generated from templated_classes.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: string_templates
#
# id: http://examples.org/linkml/test/string_templates
# description: Test cases for the string_template model
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from datetime import date, datetime, time
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Integer, String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = LINKML


# Types

# Class references



@dataclass(repr=False)
class FirstClass(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["FirstClass"]
    class_class_curie: ClassVar[str] = "linkml:FirstClass"
    class_name: ClassVar[str] = "first class"
    class_model_uri: ClassVar[URIRef] = LINKML.FirstClass

    name: str = None
    age: Optional[int] = None
    gender: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.age is not None and not isinstance(self.age, int):
            self.age = int(self.age)

        if self.gender is not None and not isinstance(self.gender, str):
            self.gender = str(self.gender)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.firstClass__name = Slot(uri=LINKML.name, name="firstClass__name", curie=LINKML.curie('name'),
                   model_uri=LINKML.firstClass__name, domain=None, range=str)

slots.firstClass__age = Slot(uri=LINKML.age, name="firstClass__age", curie=LINKML.curie('age'),
                   model_uri=LINKML.firstClass__age, domain=None, range=Optional[int])

slots.firstClass__gender = Slot(uri=LINKML.gender, name="firstClass__gender", curie=LINKML.curie('gender'),
                   model_uri=LINKML.firstClass__gender, domain=None, range=Optional[str])