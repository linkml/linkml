# Auto generated from issue_260a.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: issue_260a
#
# id: http://example.org/tests/issue_260a
# description: Small file to be imported
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



metamodel_version = "1.7.0"
version = None

# Namespaces
XSD = CurieNamespace('xsd', 'http://example.org/UNKNOWN/xsd/')
DEFAULT_ = CurieNamespace('', 'http://example.org/tests/issue_260a/')


# Types
class String(str):
    """ A character string """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = URIRef("http://example.org/tests/issue_260a/String")


# Class references



@dataclass(repr=False)
class C260a(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/issue_260a/C260a")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "C260a"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/issue_260a/C260a")

    id: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=DEFAULT_.id, name="id", curie=DEFAULT_.curie('id'),
                   model_uri=DEFAULT_.id, domain=None, range=Optional[str])
