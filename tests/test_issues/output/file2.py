# Auto generated from file2.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-01-27T02:55:04
# Schema: valuesetresolution
#
# id: https://hotecosystem.org/tccm/valuesetresolution
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
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
TCCM = CurieNamespace('tccm', 'https://hotecosystem.org/tccm/')
DEFAULT_ = TCCM


# Types

# Class references



@dataclass
class IterableResolvedValueSet(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.IterableResolvedValueSet
    class_class_curie: ClassVar[str] = "tccm:IterableResolvedValueSet"
    class_name: ClassVar[str] = "IterableResolvedValueSet"
    class_model_uri: ClassVar[URIRef] = TCCM.IterableResolvedValueSet

    complete: Union[str, "CompleteDirectory"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.complete):
            self.MissingRequiredField("complete")
        if not isinstance(self.complete, CompleteDirectory):
            self.complete = CompleteDirectory(self.complete)

        super().__post_init__(**kwargs)


@dataclass
class Directory(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM["directories_and_lists/Directory"]
    class_class_curie: ClassVar[str] = "tccm:directories_and_lists/Directory"
    class_name: ClassVar[str] = "Directory"
    class_model_uri: ClassVar[URIRef] = TCCM.Directory

    complete: Union[str, "CompleteDirectory"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.complete):
            self.MissingRequiredField("complete")
        if not isinstance(self.complete, CompleteDirectory):
            self.complete = CompleteDirectory(self.complete)

        super().__post_init__(**kwargs)


# Enumerations
class CompleteDirectory(EnumDefinitionImpl):

    COMPLETE = PermissibleValue(text="COMPLETE",
                                       description="The Directory contains all of the qualifying entries")
    PARTIAL = PermissibleValue(text="PARTIAL",
                                     description="The directory contains only a partial listing of the qualifying entries.")

    _defn = EnumDefinition(
        name="CompleteDirectory",
    )

# Slots
class slots:
    pass

slots.directory__complete = Slot(uri=TCCM.complete, name="directory__complete", curie=TCCM.curie('complete'),
                   model_uri=TCCM.directory__complete, domain=None, range=Union[str, "CompleteDirectory"])