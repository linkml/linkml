# Auto generated from table.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-10-10T16:55:54
# Schema: table
#
# id: https://w3id.org/linkml/examples/table
# description: Represent a table in linkml
# license: https://creativecommons.org/publicdomain/zero/1.0/

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
from linkml_runtime.linkml_model.types import String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
TABLE = CurieNamespace('table', 'https://w3id.org/linkml/examples/table/')
DEFAULT_ = TABLE


# Types

# Class references
class RowColumnA(URIorCURIE):
    pass


@dataclass
class Object(YAMLRoot):
    """
    An object (bnode) which needs embedding in a single row
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TABLE.Object
    class_class_curie: ClassVar[str] = "table:Object"
    class_name: ClassVar[str] = "Object"
    class_model_uri: ClassVar[URIRef] = TABLE.Object

    name: Optional[str] = None
    value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass
class Row(YAMLRoot):
    """
    A single data point made up of columns.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TABLE.Row
    class_class_curie: ClassVar[str] = "table:Row"
    class_name: ClassVar[str] = "Row"
    class_model_uri: ClassVar[URIRef] = TABLE.Row

    columnA: Union[str, RowColumnA] = None
    objectB: Optional[Union[dict, Object]] = None
    columnC: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.columnA):
            self.MissingRequiredField("columnA")
        if not isinstance(self.columnA, RowColumnA):
            self.columnA = RowColumnA(self.columnA)

        if self.objectB is not None and not isinstance(self.objectB, Object):
            self.objectB = Object(**as_dict(self.objectB))

        if self.columnC is not None and not isinstance(self.columnC, str):
            self.columnC = str(self.columnC)

        super().__post_init__(**kwargs)


@dataclass
class Table(YAMLRoot):
    """
    Container of rows.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TABLE.Table
    class_class_curie: ClassVar[str] = "table:Table"
    class_name: ClassVar[str] = "Table"
    class_model_uri: ClassVar[URIRef] = TABLE.Table

    rows: Optional[Union[Dict[Union[str, RowColumnA], Union[dict, Row]], List[Union[dict, Row]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="rows", slot_type=Row, key_name="columnA", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.rows = Slot(uri=TABLE.rows, name="rows", curie=TABLE.curie('rows'),
                   model_uri=TABLE.rows, domain=None, range=Optional[Union[Dict[Union[str, RowColumnA], Union[dict, Row]], List[Union[dict, Row]]]])

slots.columnA = Slot(uri=TABLE.columnA, name="columnA", curie=TABLE.curie('columnA'),
                   model_uri=TABLE.columnA, domain=None, range=URIRef)

slots.objectB = Slot(uri=TABLE.objectB, name="objectB", curie=TABLE.curie('objectB'),
                   model_uri=TABLE.objectB, domain=None, range=Optional[Union[dict, Object]])

slots.columnC = Slot(uri=TABLE.columnC, name="columnC", curie=TABLE.curie('columnC'),
                   model_uri=TABLE.columnC, domain=None, range=Optional[str])

slots.name = Slot(uri=TABLE.name, name="name", curie=TABLE.curie('name'),
                   model_uri=TABLE.name, domain=None, range=Optional[str])

slots.value = Slot(uri=TABLE.value, name="value", curie=TABLE.curie('value'),
                   model_uri=TABLE.value, domain=None, range=Optional[str])
