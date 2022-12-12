# Auto generated from cleanroom_schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-12-12T11:33:46
# Schema: cleanroom-schema
#
# id: https://w3id.org/microbiomedata/cleanroom-schema
# description: Cleanroom reboot of NMDC schema
# license: MIT

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
GOLD = CurieNamespace('GOLD', 'http://identifiers.org/gold/')
OBI = CurieNamespace('OBI', 'https://purl.obolibrary.org/obo/OBI_')
CLEANROOM_SCHEMA = CurieNamespace('cleanroom_schema', 'https://example.com/cleanroom-schema/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
SCHEMA = CurieNamespace('schema', 'https://schema.org/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = CLEANROOM_SCHEMA


# Types

# Class references
class NamedThingId(URIorCURIE):
    pass


class MaterialEntityId(NamedThingId):
    pass


class BiosampleId(MaterialEntityId):
    pass


class AnalyticalSampleId(MaterialEntityId):
    pass


class SiteId(MaterialEntityId):
    pass


class FieldResearchSiteId(SiteId):
    pass


class PlannedProcessId(NamedThingId):
    pass


class CollectingBiosamplesFromSiteId(PlannedProcessId):
    pass


class AgentId(NamedThingId):
    pass


@dataclass
class NamedThing(YAMLRoot):
    """
    A generic grouping for any identifiable entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA.Thing
    class_class_curie: ClassVar[str] = "schema:Thing"
    class_name: ClassVar[str] = "NamedThing"
    class_model_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.NamedThing

    id: Union[str, NamedThingId] = None
    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass
class MaterialEntity(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.MaterialEntity
    class_class_curie: ClassVar[str] = "cleanroom_schema:MaterialEntity"
    class_name: ClassVar[str] = "MaterialEntity"
    class_model_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.MaterialEntity

    id: Union[str, MaterialEntityId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MaterialEntityId):
            self.id = MaterialEntityId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Biosample(MaterialEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.Biosample
    class_class_curie: ClassVar[str] = "cleanroom_schema:Biosample"
    class_name: ClassVar[str] = "Biosample"
    class_model_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.Biosample

    id: Union[str, BiosampleId] = None
    collected_from: Optional[Union[str, FieldResearchSiteId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BiosampleId):
            self.id = BiosampleId(self.id)

        if self.collected_from is not None and not isinstance(self.collected_from, FieldResearchSiteId):
            self.collected_from = FieldResearchSiteId(self.collected_from)

        super().__post_init__(**kwargs)


@dataclass
class AnalyticalSample(MaterialEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.AnalyticalSample
    class_class_curie: ClassVar[str] = "cleanroom_schema:AnalyticalSample"
    class_name: ClassVar[str] = "AnalyticalSample"
    class_model_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.AnalyticalSample

    id: Union[str, AnalyticalSampleId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AnalyticalSampleId):
            self.id = AnalyticalSampleId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Site(MaterialEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.Site
    class_class_curie: ClassVar[str] = "cleanroom_schema:Site"
    class_name: ClassVar[str] = "Site"
    class_model_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.Site

    id: Union[str, SiteId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SiteId):
            self.id = SiteId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class FieldResearchSite(Site):
    """
    A site, outside of a laboratory, from which biosamples may be collected.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.FieldResearchSite
    class_class_curie: ClassVar[str] = "cleanroom_schema:FieldResearchSite"
    class_name: ClassVar[str] = "FieldResearchSite"
    class_model_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.FieldResearchSite

    id: Union[str, FieldResearchSiteId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, FieldResearchSiteId):
            self.id = FieldResearchSiteId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class PlannedProcess(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBI["0000011"]
    class_class_curie: ClassVar[str] = "OBI:0000011"
    class_name: ClassVar[str] = "PlannedProcess"
    class_model_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.PlannedProcess

    id: Union[str, PlannedProcessId] = None
    has_inputs: Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]] = empty_list()
    has_outputs: Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]] = empty_list()
    participating_agent: Optional[Union[str, AgentId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PlannedProcessId):
            self.id = PlannedProcessId(self.id)

        if not isinstance(self.has_inputs, list):
            self.has_inputs = [self.has_inputs] if self.has_inputs is not None else []
        self.has_inputs = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.has_inputs]

        if not isinstance(self.has_outputs, list):
            self.has_outputs = [self.has_outputs] if self.has_outputs is not None else []
        self.has_outputs = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.has_outputs]

        if self.participating_agent is not None and not isinstance(self.participating_agent, AgentId):
            self.participating_agent = AgentId(self.participating_agent)

        super().__post_init__(**kwargs)


@dataclass
class CollectingBiosamplesFromSite(PlannedProcess):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.CollectingBiosamplesFromSite
    class_class_curie: ClassVar[str] = "cleanroom_schema:CollectingBiosamplesFromSite"
    class_name: ClassVar[str] = "CollectingBiosamplesFromSite"
    class_model_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.CollectingBiosamplesFromSite

    id: Union[str, CollectingBiosamplesFromSiteId] = None
    has_inputs: Union[Union[str, SiteId], List[Union[str, SiteId]]] = None
    has_outputs: Union[Union[str, BiosampleId], List[Union[str, BiosampleId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CollectingBiosamplesFromSiteId):
            self.id = CollectingBiosamplesFromSiteId(self.id)

        if self._is_empty(self.has_inputs):
            self.MissingRequiredField("has_inputs")
        if not isinstance(self.has_inputs, list):
            self.has_inputs = [self.has_inputs] if self.has_inputs is not None else []
        self.has_inputs = [v if isinstance(v, SiteId) else SiteId(v) for v in self.has_inputs]

        if self._is_empty(self.has_outputs):
            self.MissingRequiredField("has_outputs")
        if not isinstance(self.has_outputs, list):
            self.has_outputs = [self.has_outputs] if self.has_outputs is not None else []
        self.has_outputs = [v if isinstance(v, BiosampleId) else BiosampleId(v) for v in self.has_outputs]

        super().__post_init__(**kwargs)


@dataclass
class Agent(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.Agent
    class_class_curie: ClassVar[str] = "cleanroom_schema:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.Agent

    id: Union[str, AgentId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AgentId):
            self.id = AgentId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class DataListCollection(YAMLRoot):
    """
    A datastructure that can contain lists of instances from any selected classes in the schema
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.DataListCollection
    class_class_curie: ClassVar[str] = "cleanroom_schema:DataListCollection"
    class_name: ClassVar[str] = "DataListCollection"
    class_model_uri: ClassVar[URIRef] = CLEANROOM_SCHEMA.DataListCollection

    biosample_list: Optional[Union[Dict[Union[str, BiosampleId], Union[dict, Biosample]], List[Union[dict, Biosample]]]] = empty_dict()
    frs_list: Optional[Union[Dict[Union[str, FieldResearchSiteId], Union[dict, FieldResearchSite]], List[Union[dict, FieldResearchSite]]]] = empty_dict()
    cbfs_list: Optional[Union[Dict[Union[str, CollectingBiosamplesFromSiteId], Union[dict, CollectingBiosamplesFromSite]], List[Union[dict, CollectingBiosamplesFromSite]]]] = empty_dict()
    nt_list: Optional[Union[Dict[Union[str, NamedThingId], Union[dict, NamedThing]], List[Union[dict, NamedThing]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="biosample_list", slot_type=Biosample, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="frs_list", slot_type=FieldResearchSite, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="cbfs_list", slot_type=CollectingBiosamplesFromSite, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="nt_list", slot_type=NamedThing, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=CLEANROOM_SCHEMA.id, name="id", curie=CLEANROOM_SCHEMA.curie('id'),
                   model_uri=CLEANROOM_SCHEMA.id, domain=None, range=URIRef)

slots.name = Slot(uri=CLEANROOM_SCHEMA.name, name="name", curie=CLEANROOM_SCHEMA.curie('name'),
                   model_uri=CLEANROOM_SCHEMA.name, domain=None, range=Optional[str])

slots.description = Slot(uri=CLEANROOM_SCHEMA.description, name="description", curie=CLEANROOM_SCHEMA.curie('description'),
                   model_uri=CLEANROOM_SCHEMA.description, domain=None, range=Optional[str])

slots.type = Slot(uri=CLEANROOM_SCHEMA.type, name="type", curie=CLEANROOM_SCHEMA.curie('type'),
                   model_uri=CLEANROOM_SCHEMA.type, domain=None, range=Optional[str])

slots.collected_from = Slot(uri=CLEANROOM_SCHEMA.collected_from, name="collected_from", curie=CLEANROOM_SCHEMA.curie('collected_from'),
                   model_uri=CLEANROOM_SCHEMA.collected_from, domain=Biosample, range=Optional[Union[str, FieldResearchSiteId]])

slots.has_inputs = Slot(uri=CLEANROOM_SCHEMA.has_inputs, name="has_inputs", curie=CLEANROOM_SCHEMA.curie('has_inputs'),
                   model_uri=CLEANROOM_SCHEMA.has_inputs, domain=None, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.has_outputs = Slot(uri=CLEANROOM_SCHEMA.has_outputs, name="has_outputs", curie=CLEANROOM_SCHEMA.curie('has_outputs'),
                   model_uri=CLEANROOM_SCHEMA.has_outputs, domain=None, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.participating_agent = Slot(uri=CLEANROOM_SCHEMA.participating_agent, name="participating_agent", curie=CLEANROOM_SCHEMA.curie('participating_agent'),
                   model_uri=CLEANROOM_SCHEMA.participating_agent, domain=None, range=Optional[Union[str, AgentId]])

slots.dataListCollection__biosample_list = Slot(uri=CLEANROOM_SCHEMA.biosample_list, name="dataListCollection__biosample_list", curie=CLEANROOM_SCHEMA.curie('biosample_list'),
                   model_uri=CLEANROOM_SCHEMA.dataListCollection__biosample_list, domain=None, range=Optional[Union[Dict[Union[str, BiosampleId], Union[dict, Biosample]], List[Union[dict, Biosample]]]])

slots.dataListCollection__frs_list = Slot(uri=CLEANROOM_SCHEMA.frs_list, name="dataListCollection__frs_list", curie=CLEANROOM_SCHEMA.curie('frs_list'),
                   model_uri=CLEANROOM_SCHEMA.dataListCollection__frs_list, domain=None, range=Optional[Union[Dict[Union[str, FieldResearchSiteId], Union[dict, FieldResearchSite]], List[Union[dict, FieldResearchSite]]]])

slots.dataListCollection__cbfs_list = Slot(uri=CLEANROOM_SCHEMA.cbfs_list, name="dataListCollection__cbfs_list", curie=CLEANROOM_SCHEMA.curie('cbfs_list'),
                   model_uri=CLEANROOM_SCHEMA.dataListCollection__cbfs_list, domain=None, range=Optional[Union[Dict[Union[str, CollectingBiosamplesFromSiteId], Union[dict, CollectingBiosamplesFromSite]], List[Union[dict, CollectingBiosamplesFromSite]]]])

slots.dataListCollection__nt_list = Slot(uri=CLEANROOM_SCHEMA.nt_list, name="dataListCollection__nt_list", curie=CLEANROOM_SCHEMA.curie('nt_list'),
                   model_uri=CLEANROOM_SCHEMA.dataListCollection__nt_list, domain=None, range=Optional[Union[Dict[Union[str, NamedThingId], Union[dict, NamedThing]], List[Union[dict, NamedThing]]]])

slots.CollectingBiosamplesFromSite_has_inputs = Slot(uri=CLEANROOM_SCHEMA.has_inputs, name="CollectingBiosamplesFromSite_has_inputs", curie=CLEANROOM_SCHEMA.curie('has_inputs'),
                   model_uri=CLEANROOM_SCHEMA.CollectingBiosamplesFromSite_has_inputs, domain=CollectingBiosamplesFromSite, range=Union[Union[str, SiteId], List[Union[str, SiteId]]])

slots.CollectingBiosamplesFromSite_has_outputs = Slot(uri=CLEANROOM_SCHEMA.has_outputs, name="CollectingBiosamplesFromSite_has_outputs", curie=CLEANROOM_SCHEMA.curie('has_outputs'),
                   model_uri=CLEANROOM_SCHEMA.CollectingBiosamplesFromSite_has_outputs, domain=CollectingBiosamplesFromSite, range=Union[Union[str, BiosampleId], List[Union[str, BiosampleId]]])