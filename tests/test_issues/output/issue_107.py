# Auto generated from issue_107.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-01-27T02:54:45
# Schema: schema
#
# id: https://issue_test/107/schema
# description:
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

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ICD_9 = CurieNamespace('ICD-9', 'http://test.org/prefix/ICD9')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = CurieNamespace('', 'https://issue_test/107/schema/')


# Types
class String(str):
    """ A character string """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = URIRef("https://issue_test/107/schema/String")


# Class references




# Enumerations


# Slots
class slots:
    pass

