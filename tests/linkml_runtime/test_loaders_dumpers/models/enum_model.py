# Auto generated from enum_model.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-09-10 15:53
# Schema: enum_test
#
# id: https://example.org/enum_test
# description:
# license:

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
DEFAULT_ = CurieNamespace('', 'https://example.org/enum_test/')


# Types

# Class references



@dataclass
class Organism(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://example.org/enum_test/Organism")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Organism"
    class_model_uri: ClassVar[URIRef] = URIRef("https://example.org/enum_test/Organism")

    state: Optional[Union[str, "StateEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.state is not None and not isinstance(self.state, StateEnum):
            self.state = StateEnum(self.state)

        super().__post_init__(**kwargs)


# Enumerations
class StateEnum(EnumDefinitionImpl):

    LIVING = PermissibleValue(text="LIVING")
    DEAD = PermissibleValue(text="DEAD")

    _defn = EnumDefinition(
        name="StateEnum",
    )

# Slots
class slots:
    pass

slots.state = Slot(uri=DEFAULT_.state, name="state", curie=DEFAULT_.curie('state'),
                   model_uri=DEFAULT_.state, domain=None, range=Optional[Union[str, "StateEnum"]])
