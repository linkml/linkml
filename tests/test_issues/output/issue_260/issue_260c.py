# Auto generated from issue_260c.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-01-27T02:54:55
# Schema: issue_260c
#
# id: http://example.org/tests/issue_260c
# description: Another small file to be imported
# license:

import dataclasses
import re
import sys
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import JsonObj, as_dict
from linkml_runtime.linkml_model.meta import (EnumDefinition, PermissibleValue,
                                              PvFormulaOptions)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import \
    dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import bnode, empty_dict, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (YAMLRoot, extended_float,
                                            extended_int, extended_str)
from rdflib import Namespace, URIRef

from .issue_260a import String
from .issue_260b import C260b

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
DEFAULT_ = CurieNamespace('', 'http://example.org/tests/issue_260c/')


# Types

# Class references



class C260c(C260b):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/issue_260c/C260c")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "C260c"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/issue_260c/C260c")


# Enumerations


# Slots
class slots:
    pass

