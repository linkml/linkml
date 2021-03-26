
# id: http://example.org/tests/types
# description:
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
from linkml.utils.metamodelcore import Bool

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
METATYPE = CurieNamespace('metatype', 'https://w3id.org/linkml/types/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = CurieNamespace('', 'http://example.org/tests/types/')


# Types
class String(str):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = URIRef("http://example.org/tests/types/String")


class Boolean(Bool):
    type_class_uri = XSD.boolean
    type_class_curie = "xsd:boolean"
    type_name = "boolean"
    type_model_uri = URIRef("http://example.org/tests/types/Boolean")


class BooleanType(Boolean):
    type_class_uri = XSD.boolean
    type_class_curie = "xsd:boolean"
    type_name = "boolean type"
    type_model_uri = URIRef("http://example.org/tests/types/BooleanType")


class StringType(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string type"
    type_model_uri = URIRef("http://example.org/tests/types/StringType")


# Class references




# Enumerations


# Slots
class slots:
    pass


