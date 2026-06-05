# Auto generated from file2.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: valuesetresolution
#
# id: https://hotecosystem.org/tccm/valuesetresolution
# description:
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



metamodel_version = "1.11.0"
version = None

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
TCCM = CurieNamespace('tccm', 'https://hotecosystem.org/tccm/')
DEFAULT_ = TCCM


# Types

# Class references



@dataclass(repr=False)
class IterableResolvedValueSet(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM["IterableResolvedValueSet"]
    class_class_curie: ClassVar[str] = "tccm:IterableResolvedValueSet"
    class_name: ClassVar[str] = "IterableResolvedValueSet"
    class_model_uri: ClassVar[URIRef] = TCCM.IterableResolvedValueSet

    complete: Union[str, "CompleteDirectory"] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.complete):
            self.MissingRequiredField("complete")
        if not isinstance(self.complete, CompleteDirectory):
            self.complete = CompleteDirectory(self.complete)

        super().__post_init__(**kwargs)

    _enum_slots: ClassVar[dict[str, tuple[str, bool]]] = {"complete": ("CompleteDirectory", False)}

    def __setattr__(self, name: str, value: Any) -> None:
        spec = type(self)._enum_slots.get(name)
        if spec is not None and value is not None:
            enum_name, multivalued = spec
            enum_cls = globals().get(enum_name)
            if enum_cls is not None:
                if multivalued:
                    if not isinstance(value, list):
                        value = [value] if value is not None else []
                    value = [v if isinstance(v, enum_cls) else enum_cls(v) for v in value]
                elif not isinstance(value, enum_cls):
                    value = enum_cls(value)
        object.__setattr__(self, name, value)


@dataclass(repr=False)
class Directory(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM["directories_and_lists/Directory"]
    class_class_curie: ClassVar[str] = "tccm:directories_and_lists/Directory"
    class_name: ClassVar[str] = "Directory"
    class_model_uri: ClassVar[URIRef] = TCCM.Directory

    complete: Union[str, "CompleteDirectory"] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.complete):
            self.MissingRequiredField("complete")
        if not isinstance(self.complete, CompleteDirectory):
            self.complete = CompleteDirectory(self.complete)

        super().__post_init__(**kwargs)

    _enum_slots: ClassVar[dict[str, tuple[str, bool]]] = {"complete": ("CompleteDirectory", False)}

    def __setattr__(self, name: str, value: Any) -> None:
        spec = type(self)._enum_slots.get(name)
        if spec is not None and value is not None:
            enum_name, multivalued = spec
            enum_cls = globals().get(enum_name)
            if enum_cls is not None:
                if multivalued:
                    if not isinstance(value, list):
                        value = [value] if value is not None else []
                    value = [v if isinstance(v, enum_cls) else enum_cls(v) for v in value]
                elif not isinstance(value, enum_cls):
                    value = enum_cls(value)
        object.__setattr__(self, name, value)


# Enumerations
class CompleteDirectory(EnumDefinitionImpl):

    COMPLETE = PermissibleValue(
        text="COMPLETE",
        description="The Directory contains all of the qualifying entries")
    PARTIAL = PermissibleValue(
        text="PARTIAL",
        description="The directory contains only a partial listing of the qualifying entries.")

    _defn = EnumDefinition(
        name="CompleteDirectory",
    )

# Slots
class slots:
    pass

slots.directory__complete = Slot(uri=TCCM['directories_and_lists/complete'], name="directory__complete", curie=TCCM.curie('directories_and_lists/complete'),
                   model_uri=TCCM.directory__complete, domain=None, range=Union[str, "CompleteDirectory"])
