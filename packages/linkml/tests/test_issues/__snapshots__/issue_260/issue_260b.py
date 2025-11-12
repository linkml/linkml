# Auto generated from issue_260b.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: issue_260b
#
# id: http://example.org/tests/issue_260b
# description: Another small file to be imported
# license:

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from . issue_260a import C260a, String

metamodel_version = "1.7.0"
version = None

# Namespaces
DEFAULT_ = CurieNamespace('', 'http://example.org/tests/issue_260b/')


# Types

# Class references



class C260b(C260a):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/issue_260b/C260b")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "C260b"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/issue_260b/C260b")


# Enumerations


# Slots
class slots:
    pass
