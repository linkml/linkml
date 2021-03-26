# Auto generated from issue_121.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-03-26 14:21
# Schema: schema
#
# id: https://microbiomedata/schema
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

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
from linkml_model.types import String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = CurieNamespace('', 'https://microbiomedata/schema/')


# Types

# Class references



@dataclass
class Biosample(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/Biosample")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "biosample"
    class_model_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/Biosample")

    depth: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.depth is not None and not isinstance(self.depth, str):
            self.depth = str(self.depth)

        super().__post_init__(**kwargs)


class ImportedClass(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/mixs/ImportedClass")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "imported class"
    class_model_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/ImportedClass")


# Enumerations


# Slots
class slots:
    pass

slots.depth = Slot(uri=DEFAULT_['mixs/depth'], name="depth", curie=DEFAULT_.curie('mixs/depth'),
                   model_uri=DEFAULT_.depth, domain=None, range=Optional[str])

slots.biosample_depth = Slot(uri=DEFAULT_.depth, name="biosample_depth", curie=DEFAULT_.curie('depth'),
                   model_uri=DEFAULT_.biosample_depth, domain=Biosample, range=Optional[str])