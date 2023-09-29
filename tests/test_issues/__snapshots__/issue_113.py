# Auto generated from issue_113.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: schema
#
# id: https://microbiomedata/schema
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
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
DEFAULT_ = CurieNamespace('', 'https://microbiomedata/schema/')


# Types

# Class references



class NamedThing(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/NamedThing")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "named thing"
    class_model_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/NamedThing")


@dataclass
class TestClass(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/TestClass")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "test class"
    class_model_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/TestClass")

    test_attribute_1: Optional[str] = None
    test_attribute_2: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.test_attribute_1 is not None and not isinstance(self.test_attribute_1, str):
            self.test_attribute_1 = str(self.test_attribute_1)

        if self.test_attribute_2 is not None and not isinstance(self.test_attribute_2, str):
            self.test_attribute_2 = str(self.test_attribute_2)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.attribute = Slot(uri=DEFAULT_.attribute, name="attribute", curie=DEFAULT_.curie('attribute'),
                   model_uri=DEFAULT_.attribute, domain=NamedThing, range=Optional[str])

slots.test_attribute_1 = Slot(uri=DEFAULT_.test_attribute_1, name="test attribute 1", curie=DEFAULT_.curie('test_attribute_1'),
                   model_uri=DEFAULT_.test_attribute_1, domain=NamedThing, range=Optional[str])

slots.test_attribute_2 = Slot(uri=DEFAULT_.test_attribute_2, name="test attribute 2", curie=DEFAULT_.curie('test_attribute_2'),
                   model_uri=DEFAULT_.test_attribute_2, domain=None, range=Optional[str])