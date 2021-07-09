# Auto generated from issue_80.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: Issue_80_test_case
#
# id: http://example.org/issues/80
# description: Example identifier
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
from linkml_runtime.linkml_model.types import Integer, Objectidentifier, String
from linkml_runtime.utils.metamodelcore import ElementIdentifier

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
BIOLINK = CurieNamespace('biolink', 'https://w3id.org/biolink/vocab/')
EX = CurieNamespace('ex', 'http://example.org/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
MODEL = CurieNamespace('model', 'https://w3id.org/biolink/')
DEFAULT_ = BIOLINK


# Types

# Class references
class PersonId(ElementIdentifier):
    pass


@dataclass
class Person(YAMLRoot):
    """
    A person, living or dead
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.PERSON
    class_class_curie: ClassVar[str] = "ex:PERSON"
    class_name: ClassVar[str] = "person"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Person

    id: Union[str, PersonId] = None
    name: str = None
    age: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.age is not None and not isinstance(self.age, int):
            self.age = int(self.age)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=BIOLINK.id, name="id", curie=BIOLINK.curie('id'),
                   model_uri=BIOLINK.id, domain=None, range=URIRef)

slots.name = Slot(uri=BIOLINK.name, name="name", curie=BIOLINK.curie('name'),
                   model_uri=BIOLINK.name, domain=None, range=str)

slots.age = Slot(uri=BIOLINK.age, name="age", curie=BIOLINK.curie('age'),
                   model_uri=BIOLINK.age, domain=None, range=Optional[int])