# Auto generated from timepoint.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-10-15 20:00
# Schema: timepoint
#
# id: http://example.org/tests/timepoint
# description:
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
from linkml_runtime.linkml_model.types import String, Time
from linkml_runtime.utils.metamodelcore import XSDTime

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = CurieNamespace('', 'http://example.org/tests/timepoint/')


# Types
class TimeType(Time):
    """ A time object represents a (local) time of day, independent of any particular day """
    type_class_uri = XSD.dateTime
    type_class_curie = "xsd:dateTime"
    type_name = "time type"
    type_model_uri = URIRef("http://example.org/tests/timepoint/TimeType")


# Class references
class GeographicLocationK(extended_str):
    pass


class GeographicLocationAtTimeK(GeographicLocationK):
    pass


@dataclass
class GeographicLocation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/timepoint/GeographicLocation")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "geographic location"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/timepoint/GeographicLocation")

    k: Union[str, GeographicLocationK] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.k):
            self.MissingRequiredField("k")
        if not isinstance(self.k, GeographicLocationK):
            self.k = GeographicLocationK(self.k)

        super().__post_init__(**kwargs)


@dataclass
class GeographicLocationAtTime(GeographicLocation):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/timepoint/GeographicLocationAtTime")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "geographic location at time"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/timepoint/GeographicLocationAtTime")

    k: Union[str, GeographicLocationAtTimeK] = None
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.k):
            self.MissingRequiredField("k")
        if not isinstance(self.k, GeographicLocationAtTimeK):
            self.k = GeographicLocationAtTimeK(self.k)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.k = Slot(uri=DEFAULT_.k, name="k", curie=DEFAULT_.curie('k'),
                   model_uri=DEFAULT_.k, domain=GeographicLocation, range=Union[str, GeographicLocationK])

slots.timepoint = Slot(uri=DEFAULT_.timepoint, name="timepoint", curie=DEFAULT_.curie('timepoint'),
                   model_uri=DEFAULT_.timepoint, domain=GeographicLocationAtTime, range=Optional[Union[str, TimeType]])
