# Auto generated from issue_368.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: bms
#
# id: https://microbiomedata/schema
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

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
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
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

from . issue_368_imports import ParentClass, SampleEnum

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = CurieNamespace('', 'https://microbiomedata/schema/')


# Types

# Class references



@dataclass(repr=False)
class SampleClass(ParentClass):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/SampleClass")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "SampleClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/SampleClass")

    slot_1: Optional[Union[str, "SampleEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.slot_1 is not None and self.slot_1 not in SampleEnum:
            self.slot_1 = SampleEnum(self.slot_1)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.slot_1 = Slot(uri=DEFAULT_.slot_1, name="slot_1", curie=DEFAULT_.curie('slot_1'),
                   model_uri=DEFAULT_.slot_1, domain=None, range=Optional[Union[str, "SampleEnum"]])