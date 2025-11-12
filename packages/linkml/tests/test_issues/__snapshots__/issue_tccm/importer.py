# Auto generated from importer.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: importer
#
# id: https://example.org/importer
# description: Test of local import with an identifier
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

from . importee import Base, BaseId, String

metamodel_version = "1.7.0"
version = None

# Namespaces
EX = CurieNamespace('ex', 'https://example.org/importee/')
DEFAULT_ = EX


# Types

# Class references
class ChildId(BaseId):
    pass


@dataclass(repr=False)
class Child(Base):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["Child"]
    class_class_curie: ClassVar[str] = "ex:Child"
    class_name: ClassVar[str] = "child"
    class_model_uri: ClassVar[URIRef] = EX.Child

    id: Union[str, ChildId] = None
    value: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ChildId):
            self.id = ChildId(self.id)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass
