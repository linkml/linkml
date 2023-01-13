# Auto generated from None by pythongen.py version: 0.9.0
# Generation date: 2023-01-13T12:39:28
# Schema: test-schema
#
# id: http://example.org/test-schema
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
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
TEST_SCHEMA = CurieNamespace('test_schema', 'http://example.org/test-schema/')
DEFAULT_ = TEST_SCHEMA


# Types

# Class references
class PersonId(extended_str):
    pass


@dataclass
class Person(YAMLRoot):
    """
    A human being
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST_SCHEMA.Person
    class_class_curie: ClassVar[str] = "test_schema:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = TEST_SCHEMA.Person

    id: Union[str, PersonId] = None
    name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


@dataclass
class Database(YAMLRoot):
    """
    An outer collection of class-specific collections
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST_SCHEMA.Database
    class_class_curie: ClassVar[str] = "test_schema:Database"
    class_name: ClassVar[str] = "Database"
    class_model_uri: ClassVar[URIRef] = TEST_SCHEMA.Database

    person_set: Optional[Union[Dict[Union[str, PersonId], Union[dict, Person]], List[Union[dict, Person]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="person_set", slot_type=Person, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=TEST_SCHEMA.id, name="id", curie=TEST_SCHEMA.curie('id'),
                   model_uri=TEST_SCHEMA.id, domain=None, range=URIRef)

slots.name = Slot(uri=TEST_SCHEMA.name, name="name", curie=TEST_SCHEMA.curie('name'),
                   model_uri=TEST_SCHEMA.name, domain=None, range=Optional[str])

slots.person_set = Slot(uri=TEST_SCHEMA.person_set, name="person_set", curie=TEST_SCHEMA.curie('person_set'),
                   model_uri=TEST_SCHEMA.person_set, domain=None, range=Optional[Union[Dict[Union[str, PersonId], Union[dict, Person]], List[Union[dict, Person]]]])