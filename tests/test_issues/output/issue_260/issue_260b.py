# Auto generated from issue_260b.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-03-26 14:21
# Schema: issue_260b
#
# id: http://example.org/tests/issue_260b
# description: Another small file to be imported
# license:

import dataclasses
import sys
import re
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml.utils.slot import Slot
from linkml.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml.utils.formatutils import camelcase, underscore, sfx
from linkml.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml.utils.curienamespace import CurieNamespace
from . issue_260a import C260a, String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
DEFAULT_ = CurieNamespace('', 'http://example.org/tests/issue_260b/')


# Types

# Class references



class C260b(C260a):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/issue_260b/C260b")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "C260b"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/issue_260b/C260b")


# Enumerations


# Slots
class slots:
    pass

