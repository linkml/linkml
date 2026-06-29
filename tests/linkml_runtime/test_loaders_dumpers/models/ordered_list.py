# Auto generated from ordered_list.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-06-29T11:43:02
# Schema: ordered_list
#
# id: http://example.org/ordered_list
# description: Schema exercising ``list_elements_ordered`` on multivalued slots, which the RDF dumper/loader represent as an ``rdf:List`` so that element order is part of the RDF semantics. See https://github.com/linkml/linkml/issues/3531
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import JsonObj, as_dict
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import bnode, empty_dict, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_float, extended_int, extended_str
from rdflib import Namespace, URIRef

from linkml_runtime.linkml_model.types import String

metamodel_version = "1.11.0"
version = None

# Namespaces
EX = CurieNamespace("ex", "http://example.org/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
DEFAULT_ = EX


# Types


# Class references
class ItemName(extended_str):
    pass


class ColumnDescAtom(extended_str):
    pass


@dataclass(repr=False)
class Item(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["Item"]
    class_class_curie: ClassVar[str] = "ex:Item"
    class_name: ClassVar[str] = "Item"
    class_model_uri: ClassVar[URIRef] = EX.Item

    name: Union[str, ItemName] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, ItemName):
            self.name = ItemName(self.name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ColumnDesc(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["ColumnDesc"]
    class_class_curie: ClassVar[str] = "ex:ColumnDesc"
    class_name: ClassVar[str] = "ColumnDesc"
    class_model_uri: ClassVar[URIRef] = EX.ColumnDesc

    atom: Union[str, ColumnDescAtom] = None
    scope: Optional[Union[str, list[str]]] = empty_list()
    items: Optional[Union[list[Union[str, ItemName]], dict[Union[str, ItemName], Union[dict, Item]]]] = empty_dict()
    tags: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.atom):
            self.MissingRequiredField("atom")
        if not isinstance(self.atom, ColumnDescAtom):
            self.atom = ColumnDescAtom(self.atom)

        if not isinstance(self.scope, list):
            self.scope = [self.scope] if self.scope is not None else []
        self.scope = [v if isinstance(v, str) else str(v) for v in self.scope]

        self._normalize_inlined_as_list(slot_name="items", slot_type=Item, key_name="name", keyed=True)

        if not isinstance(self.tags, list):
            self.tags = [self.tags] if self.tags is not None else []
        self.tags = [v if isinstance(v, str) else str(v) for v in self.tags]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.item__name = Slot(
    uri=EX.name, name="item__name", curie=EX.curie("name"), model_uri=EX.item__name, domain=None, range=URIRef
)

slots.columnDesc__atom = Slot(
    uri=EX.atom,
    name="columnDesc__atom",
    curie=EX.curie("atom"),
    model_uri=EX.columnDesc__atom,
    domain=None,
    range=URIRef,
)

slots.columnDesc__scope = Slot(
    uri=EX.scope,
    name="columnDesc__scope",
    curie=EX.curie("scope"),
    model_uri=EX.columnDesc__scope,
    domain=None,
    range=Optional[Union[str, list[str]]],
)

slots.columnDesc__items = Slot(
    uri=EX.items,
    name="columnDesc__items",
    curie=EX.curie("items"),
    model_uri=EX.columnDesc__items,
    domain=None,
    range=Optional[Union[list[Union[str, ItemName]], dict[Union[str, ItemName], Union[dict, Item]]]],
)

slots.columnDesc__tags = Slot(
    uri=EX.tags,
    name="columnDesc__tags",
    curie=EX.curie("tags"),
    model_uri=EX.columnDesc__tags,
    domain=None,
    range=Optional[Union[str, list[str]]],
)
