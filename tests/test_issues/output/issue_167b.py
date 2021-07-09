# Auto generated from issue_167b.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: annotations_test
#
# id: http://example.org/tests/issue167b
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


metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
EX = CurieNamespace('ex', 'http://example.org/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = EX


# Types

# Class references



class MyClass(YAMLRoot):
    """
    Annotations as tag value pairs. Note that altLabel is defined in the default namespace, not in the SKOS namespace
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.MyClass
    class_class_curie: ClassVar[str] = "ex:MyClass"
    class_name: ClassVar[str] = "my class"
    class_model_uri: ClassVar[URIRef] = EX.MyClass


class MyClass2(YAMLRoot):
    """
    -> This form of annotations is a tag/value format, which allows annotations to be annotated. Note, however, that
    the annotation source is NOT a CURIE, rather just a string.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.MyClass2
    class_class_curie: ClassVar[str] = "ex:MyClass2"
    class_name: ClassVar[str] = "my class 2"
    class_model_uri: ClassVar[URIRef] = EX.MyClass2


# Enumerations


# Slots
class slots:
    pass

