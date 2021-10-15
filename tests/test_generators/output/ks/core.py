# Auto generated from core.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-10-15 19:59
# Schema: core
#
# id: https://w3id.org/linkml/tests/core
# description: core schema imported by kitchen_sink
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
from linkml_runtime.linkml_model.types import Date, String
from linkml_runtime.utils.metamodelcore import XSDDate

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
BIOLINK = CurieNamespace('biolink', 'https://w3id.org/biolink/')
CORE = CurieNamespace('core', 'https://w3id.org/linkml/tests/core/')
DCE = CurieNamespace('dce', 'http://purl.org/dc/elements/1.1/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
DEFAULT_ = CORE


# Types

# Class references
class ActivityId(extended_str):
    pass


class AgentId(extended_str):
    pass


@dataclass
class Activity(YAMLRoot):
    """
    a provence-generating activity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CORE.Activity
    class_class_curie: ClassVar[str] = "core:Activity"
    class_name: ClassVar[str] = "activity"
    class_model_uri: ClassVar[URIRef] = CORE.Activity

    id: Union[str, ActivityId] = None
    started_at_time: Optional[Union[str, XSDDate]] = None
    ended_at_time: Optional[Union[str, XSDDate]] = None
    was_informed_by: Optional[Union[str, ActivityId]] = None
    was_associated_with: Optional[Union[str, AgentId]] = None
    used: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ActivityId):
            self.id = ActivityId(self.id)

        if self.started_at_time is not None and not isinstance(self.started_at_time, XSDDate):
            self.started_at_time = XSDDate(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, XSDDate):
            self.ended_at_time = XSDDate(self.ended_at_time)

        if self.was_informed_by is not None and not isinstance(self.was_informed_by, ActivityId):
            self.was_informed_by = ActivityId(self.was_informed_by)

        if self.was_associated_with is not None and not isinstance(self.was_associated_with, AgentId):
            self.was_associated_with = AgentId(self.was_associated_with)

        if self.used is not None and not isinstance(self.used, str):
            self.used = str(self.used)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass
class Agent(YAMLRoot):
    """
    a provence-generating agent
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV.Agent
    class_class_curie: ClassVar[str] = "prov:Agent"
    class_name: ClassVar[str] = "agent"
    class_model_uri: ClassVar[URIRef] = CORE.Agent

    id: Union[str, AgentId] = None
    acted_on_behalf_of: Optional[Union[str, AgentId]] = None
    was_informed_by: Optional[Union[str, ActivityId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AgentId):
            self.id = AgentId(self.id)

        if self.acted_on_behalf_of is not None and not isinstance(self.acted_on_behalf_of, AgentId):
            self.acted_on_behalf_of = AgentId(self.acted_on_behalf_of)

        if self.was_informed_by is not None and not isinstance(self.was_informed_by, ActivityId):
            self.was_informed_by = ActivityId(self.was_informed_by)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=CORE.id, name="id", curie=CORE.curie('id'),
                   model_uri=CORE.id, domain=None, range=URIRef)

slots.name = Slot(uri=CORE.name, name="name", curie=CORE.curie('name'),
                   model_uri=CORE.name, domain=None, range=Optional[str])

slots.description = Slot(uri=CORE.description, name="description", curie=CORE.curie('description'),
                   model_uri=CORE.description, domain=None, range=Optional[str])

slots.started_at_time = Slot(uri=PROV.startedAtTime, name="started at time", curie=PROV.curie('startedAtTime'),
                   model_uri=CORE.started_at_time, domain=None, range=Optional[Union[str, XSDDate]])

slots.ended_at_time = Slot(uri=PROV.endedAtTime, name="ended at time", curie=PROV.curie('endedAtTime'),
                   model_uri=CORE.ended_at_time, domain=None, range=Optional[Union[str, XSDDate]])

slots.was_informed_by = Slot(uri=PROV.wasInformedBy, name="was informed by", curie=PROV.curie('wasInformedBy'),
                   model_uri=CORE.was_informed_by, domain=None, range=Optional[Union[str, ActivityId]])

slots.was_associated_with = Slot(uri=PROV.wasAssociatedWith, name="was associated with", curie=PROV.curie('wasAssociatedWith'),
                   model_uri=CORE.was_associated_with, domain=None, range=Optional[Union[str, AgentId]])

slots.acted_on_behalf_of = Slot(uri=PROV.actedOnBehalfOf, name="acted on behalf of", curie=PROV.curie('actedOnBehalfOf'),
                   model_uri=CORE.acted_on_behalf_of, domain=None, range=Optional[Union[str, AgentId]])

slots.was_generated_by = Slot(uri=PROV.wasGeneratedBy, name="was generated by", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=CORE.was_generated_by, domain=None, range=Optional[Union[str, ActivityId]])

slots.used = Slot(uri=PROV.used, name="used", curie=PROV.curie('used'),
                   model_uri=CORE.used, domain=Activity, range=Optional[str])

slots.activity_set = Slot(uri=CORE.activity_set, name="activity set", curie=CORE.curie('activity_set'),
                   model_uri=CORE.activity_set, domain=None, range=Optional[Union[Dict[Union[str, ActivityId], Union[dict, Activity]], List[Union[dict, Activity]]]])

slots.agent_set = Slot(uri=CORE.agent_set, name="agent set", curie=CORE.curie('agent_set'),
                   model_uri=CORE.agent_set, domain=None, range=Optional[Union[Dict[Union[str, AgentId], Union[dict, Agent]], List[Union[dict, Agent]]]])