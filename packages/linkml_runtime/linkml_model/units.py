# Auto generated from units.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-06-28T03:39:16
# Schema: units
#
# id: https://w3id.org/linkml/units
# description: Units datamodel
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from .types import String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
QUDT = CurieNamespace('qudt', 'http://qudt.org/schema/qudt/')
DEFAULT_ = LINKML


# Types

# Class references



@dataclass
class UnitOfMeasure(YAMLRoot):
    """
    A unit of measure, or unit, is a particular quantity value that has been chosen as a scale for measuring other
    quantities the same kind (more generally of equivalent dimension).
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = QUDT.Unit
    class_class_curie: ClassVar[str] = "qudt:Unit"
    class_name: ClassVar[str] = "UnitOfMeasure"
    class_model_uri: ClassVar[URIRef] = LINKML.UnitOfMeasure

    symbol: Optional[str] = None
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    ucum_code: Optional[str] = None
    derivation: Optional[str] = None
    has_quantity_kind: Optional[Union[str, URIorCURIE]] = None
    iec61360code: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.symbol is not None and not isinstance(self.symbol, str):
            self.symbol = str(self.symbol)

        if not isinstance(self.exact_mappings, list):
            self.exact_mappings = [self.exact_mappings] if self.exact_mappings is not None else []
        self.exact_mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.exact_mappings]

        if self.ucum_code is not None and not isinstance(self.ucum_code, str):
            self.ucum_code = str(self.ucum_code)

        if self.derivation is not None and not isinstance(self.derivation, str):
            self.derivation = str(self.derivation)

        if self.has_quantity_kind is not None and not isinstance(self.has_quantity_kind, URIorCURIE):
            self.has_quantity_kind = URIorCURIE(self.has_quantity_kind)

        if self.iec61360code is not None and not isinstance(self.iec61360code, str):
            self.iec61360code = str(self.iec61360code)

        super().__post_init__(**kwargs)


# Enumerations


# Slots

