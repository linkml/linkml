# Auto generated from was_associated_with_generated.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-11-11T13:06:33
# Schema: was_associated_with
#
# id: http://example.org/was_associated_with
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import re
from dataclasses import dataclass
from typing import Any, ClassVar, Optional, Union

from jsonasobj2 import as_dict
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.metamodelcore import empty_dict, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from rdflib import URIRef

metamodel_version = "1.7.0"
version = None

# Namespaces
DCTERMS = CurieNamespace("dcterms", "http://purl.org/dc/terms/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
NMDC = CurieNamespace("nmdc", "https://w3id.org/nmdc/")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = NMDC


# Types


# Class references
class NamedThingId(extended_str):
    pass


class ConcreteThingId(NamedThingId):
    pass


class ActivityId(extended_str):
    pass


class WorkflowExecutionActivityId(ActivityId):
    pass


class MetatranscriptomeAssemblyId(WorkflowExecutionActivityId):
    pass


class MetatranscriptomeActivityId(WorkflowExecutionActivityId):
    pass


@dataclass
class NamedThing(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.NamedThing
    class_class_curie: ClassVar[str] = "nmdc:NamedThing"
    class_name: ClassVar[str] = "NamedThing"
    class_model_uri: ClassVar[URIRef] = NMDC.NamedThing

    id: Union[str, NamedThingId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    alternative_identifiers: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.alternative_identifiers, list):
            self.alternative_identifiers = (
                [self.alternative_identifiers] if self.alternative_identifiers is not None else []
            )
        self.alternative_identifiers = [v if isinstance(v, str) else str(v) for v in self.alternative_identifiers]

        super().__post_init__(**kwargs)


@dataclass
class ConcreteThing(NamedThing):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.ConcreteThing
    class_class_curie: ClassVar[str] = "nmdc:ConcreteThing"
    class_name: ClassVar[str] = "ConcreteThing"
    class_model_uri: ClassVar[URIRef] = NMDC.ConcreteThing

    id: Union[str, ConcreteThingId] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ConcreteThingId):
            self.id = ConcreteThingId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Agent(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.Agent
    class_class_curie: ClassVar[str] = "nmdc:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = NMDC.Agent

    acted_on_behalf_of: Optional[Union[dict, "Agent"]] = None
    was_informed_by: Optional[Union[str, ActivityId]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.acted_on_behalf_of is not None and not isinstance(self.acted_on_behalf_of, Agent):
            self.acted_on_behalf_of = Agent(**as_dict(self.acted_on_behalf_of))

        if self.was_informed_by is not None and not isinstance(self.was_informed_by, ActivityId):
            self.was_informed_by = ActivityId(self.was_informed_by)

        super().__post_init__(**kwargs)


@dataclass
class Activity(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.Activity
    class_class_curie: ClassVar[str] = "nmdc:Activity"
    class_name: ClassVar[str] = "Activity"
    class_model_uri: ClassVar[URIRef] = NMDC.Activity

    id: Union[str, ActivityId] = None
    name: Optional[str] = None
    was_informed_by: Optional[Union[str, ActivityId]] = None
    was_associated_with: Optional[Union[dict, Agent]] = None
    used: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ActivityId):
            self.id = ActivityId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.was_informed_by is not None and not isinstance(self.was_informed_by, ActivityId):
            self.was_informed_by = ActivityId(self.was_informed_by)

        if self.was_associated_with is not None and not isinstance(self.was_associated_with, Agent):
            self.was_associated_with = Agent(**as_dict(self.was_associated_with))

        if self.used is not None and not isinstance(self.used, str):
            self.used = str(self.used)

        super().__post_init__(**kwargs)


@dataclass
class WorkflowExecutionActivity(Activity):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.WorkflowExecutionActivity
    class_class_curie: ClassVar[str] = "nmdc:WorkflowExecutionActivity"
    class_name: ClassVar[str] = "WorkflowExecutionActivity"
    class_model_uri: ClassVar[URIRef] = NMDC.WorkflowExecutionActivity

    id: Union[str, WorkflowExecutionActivityId] = None
    execution_resource: str = None
    has_input: Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]] = None
    has_output: Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]] = None
    was_informed_by: Union[str, ActivityId] = None
    raw_type: Optional[str] = None
    part_of: Optional[Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]]] = empty_list()
    type: Optional[str] = None
    was_associated_with: Optional[Union[str, WorkflowExecutionActivityId]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, WorkflowExecutionActivityId):
            self.id = WorkflowExecutionActivityId(self.id)

        if self._is_empty(self.execution_resource):
            self.MissingRequiredField("execution_resource")
        if not isinstance(self.execution_resource, str):
            self.execution_resource = str(self.execution_resource)

        if self._is_empty(self.has_input):
            self.MissingRequiredField("has_input")
        if not isinstance(self.has_input, list):
            self.has_input = [self.has_input] if self.has_input is not None else []
        self.has_input = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.has_input]

        if self._is_empty(self.has_output):
            self.MissingRequiredField("has_output")
        if not isinstance(self.has_output, list):
            self.has_output = [self.has_output] if self.has_output is not None else []
        self.has_output = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.has_output]

        if self._is_empty(self.was_informed_by):
            self.MissingRequiredField("was_informed_by")
        if not isinstance(self.was_informed_by, ActivityId):
            self.was_informed_by = ActivityId(self.was_informed_by)

        if self.raw_type is not None and not isinstance(self.raw_type, str):
            self.raw_type = str(self.raw_type)

        if not isinstance(self.part_of, list):
            self.part_of = [self.part_of] if self.part_of is not None else []
        self.part_of = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.part_of]

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.was_associated_with is not None and not isinstance(
            self.was_associated_with, WorkflowExecutionActivityId
        ):
            self.was_associated_with = WorkflowExecutionActivityId(self.was_associated_with)

        super().__post_init__(**kwargs)


@dataclass
class MetatranscriptomeAssembly(WorkflowExecutionActivity):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.MetatranscriptomeAssembly
    class_class_curie: ClassVar[str] = "nmdc:MetatranscriptomeAssembly"
    class_name: ClassVar[str] = "MetatranscriptomeAssembly"
    class_model_uri: ClassVar[URIRef] = NMDC.MetatranscriptomeAssembly

    id: Union[str, MetatranscriptomeAssemblyId] = None
    execution_resource: str = None
    has_input: Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]] = None
    has_output: Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]] = None
    was_informed_by: Union[str, ActivityId] = None
    insdc_assembly_identifiers: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MetatranscriptomeAssemblyId):
            self.id = MetatranscriptomeAssemblyId(self.id)

        if self.insdc_assembly_identifiers is not None and not isinstance(self.insdc_assembly_identifiers, str):
            self.insdc_assembly_identifiers = str(self.insdc_assembly_identifiers)

        super().__post_init__(**kwargs)


@dataclass
class MetatranscriptomeActivity(WorkflowExecutionActivity):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.MetatranscriptomeActivity
    class_class_curie: ClassVar[str] = "nmdc:MetatranscriptomeActivity"
    class_name: ClassVar[str] = "MetatranscriptomeActivity"
    class_model_uri: ClassVar[URIRef] = NMDC.MetatranscriptomeActivity

    id: Union[str, MetatranscriptomeActivityId] = None
    execution_resource: str = None
    has_input: Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]] = None
    has_output: Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]] = None
    was_informed_by: Union[str, ActivityId] = None
    raw_type: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MetatranscriptomeActivityId):
            self.id = MetatranscriptomeActivityId(self.id)

        if self.raw_type is not None and not isinstance(self.raw_type, str):
            self.raw_type = str(self.raw_type)

        super().__post_init__(**kwargs)


@dataclass
class Database(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.Database
    class_class_curie: ClassVar[str] = "nmdc:Database"
    class_name: ClassVar[str] = "Database"
    class_model_uri: ClassVar[URIRef] = NMDC.Database

    activity_set: Optional[
        Union[
            dict[Union[str, WorkflowExecutionActivityId], Union[dict, WorkflowExecutionActivity]],
            list[Union[dict, WorkflowExecutionActivity]],
        ]
    ] = empty_dict()
    metatranscriptome_activity_set: Optional[
        Union[
            dict[Union[str, MetatranscriptomeActivityId], Union[dict, MetatranscriptomeActivity]],
            list[Union[dict, MetatranscriptomeActivity]],
        ]
    ] = empty_dict()
    concrete_thing_set: Optional[
        Union[
            dict[Union[str, ConcreteThingId], Union[dict, ConcreteThing]],
            list[Union[dict, ConcreteThing]],
        ]
    ] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        self._normalize_inlined_as_list(
            slot_name="activity_set", slot_type=WorkflowExecutionActivity, key_name="id", keyed=True
        )

        self._normalize_inlined_as_list(
            slot_name="metatranscriptome_activity_set",
            slot_type=MetatranscriptomeActivity,
            key_name="id",
            keyed=True,
        )

        self._normalize_inlined_as_list(
            slot_name="concrete_thing_set", slot_type=ConcreteThing, key_name="id", keyed=True
        )

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.concrete_thing_set = Slot(
    uri=NMDC.concrete_thing_set,
    name="concrete_thing_set",
    curie=NMDC.curie("concrete_thing_set"),
    model_uri=NMDC.concrete_thing_set,
    domain=Database,
    range=Optional[
        Union[
            dict[Union[str, ConcreteThingId], Union[dict, ConcreteThing]],
            list[Union[dict, ConcreteThing]],
        ]
    ],
)

slots.was_informed_by = Slot(
    uri=NMDC.was_informed_by,
    name="was_informed_by",
    curie=NMDC.curie("was_informed_by"),
    model_uri=NMDC.was_informed_by,
    domain=None,
    range=Optional[Union[str, ActivityId]],
)

slots.was_associated_with = Slot(
    uri=NMDC.was_associated_with,
    name="was_associated_with",
    curie=NMDC.curie("was_associated_with"),
    model_uri=NMDC.was_associated_with,
    domain=None,
    range=Optional[Union[dict, Agent]],
)

slots.acted_on_behalf_of = Slot(
    uri=NMDC.acted_on_behalf_of,
    name="acted_on_behalf_of",
    curie=NMDC.curie("acted_on_behalf_of"),
    model_uri=NMDC.acted_on_behalf_of,
    domain=None,
    range=Optional[Union[dict, Agent]],
)

slots.was_generated_by = Slot(
    uri=NMDC.was_generated_by,
    name="was_generated_by",
    curie=NMDC.curie("was_generated_by"),
    model_uri=NMDC.was_generated_by,
    domain=None,
    range=Optional[Union[str, ActivityId]],
)

slots.used = Slot(
    uri=NMDC.used,
    name="used",
    curie=NMDC.curie("used"),
    model_uri=NMDC.used,
    domain=Activity,
    range=Optional[str],
)

slots.object_set = Slot(
    uri=NMDC.object_set,
    name="object_set",
    curie=NMDC.curie("object_set"),
    model_uri=NMDC.object_set,
    domain=Database,
    range=Optional[Union[str, list[str]]],
)

slots.activity_set = Slot(
    uri=NMDC.activity_set,
    name="activity_set",
    curie=NMDC.curie("activity_set"),
    model_uri=NMDC.activity_set,
    domain=Database,
    range=Optional[
        Union[
            dict[Union[str, WorkflowExecutionActivityId], Union[dict, WorkflowExecutionActivity]],
            list[Union[dict, WorkflowExecutionActivity]],
        ]
    ],
)

slots.metatranscriptome_activity_set = Slot(
    uri=NMDC.metatranscriptome_activity_set,
    name="metatranscriptome_activity_set",
    curie=NMDC.curie("metatranscriptome_activity_set"),
    model_uri=NMDC.metatranscriptome_activity_set,
    domain=Database,
    range=Optional[
        Union[
            dict[Union[str, MetatranscriptomeActivityId], Union[dict, MetatranscriptomeActivity]],
            list[Union[dict, MetatranscriptomeActivity]],
        ]
    ],
)

slots.id = Slot(uri=NMDC.id, name="id", curie=NMDC.curie("id"), model_uri=NMDC.id, domain=None, range=URIRef)

slots.name = Slot(
    uri=NMDC.name,
    name="name",
    curie=NMDC.curie("name"),
    model_uri=NMDC.name,
    domain=None,
    range=Optional[str],
)

slots.execution_resource = Slot(
    uri=NMDC.execution_resource,
    name="execution_resource",
    curie=NMDC.curie("execution_resource"),
    model_uri=NMDC.execution_resource,
    domain=None,
    range=Optional[str],
)

slots.has_input = Slot(
    uri=NMDC.has_input,
    name="has_input",
    curie=NMDC.curie("has_input"),
    model_uri=NMDC.has_input,
    domain=NamedThing,
    range=Optional[Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]]],
)

slots.has_output = Slot(
    uri=NMDC.has_output,
    name="has_output",
    curie=NMDC.curie("has_output"),
    model_uri=NMDC.has_output,
    domain=NamedThing,
    range=Optional[Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]]],
)

slots.part_of = Slot(
    uri=DCTERMS.isPartOf,
    name="part_of",
    curie=DCTERMS.curie("isPartOf"),
    model_uri=NMDC.part_of,
    domain=NamedThing,
    range=Optional[Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]]],
)

slots.type = Slot(
    uri=NMDC.type,
    name="type",
    curie=NMDC.curie("type"),
    model_uri=NMDC.type,
    domain=None,
    range=Optional[str],
)

slots.insdc_assembly_identifiers = Slot(
    uri=NMDC.insdc_assembly_identifiers,
    name="insdc_assembly_identifiers",
    curie=NMDC.curie("insdc_assembly_identifiers"),
    model_uri=NMDC.insdc_assembly_identifiers,
    domain=None,
    range=Optional[str],
    pattern=re.compile(r"^insdc.sra:[A-Z]+[0-9]+(\.[0-9]+)?$"),
)

slots.description = Slot(
    uri=DCTERMS.description,
    name="description",
    curie=DCTERMS.curie("description"),
    model_uri=NMDC.description,
    domain=None,
    range=Optional[str],
)

slots.alternative_identifiers = Slot(
    uri=NMDC.alternative_identifiers,
    name="alternative_identifiers",
    curie=NMDC.curie("alternative_identifiers"),
    model_uri=NMDC.alternative_identifiers,
    domain=None,
    range=Optional[Union[str, list[str]]],
)

slots.attribute = Slot(
    uri=NMDC.attribute,
    name="attribute",
    curie=NMDC.curie("attribute"),
    model_uri=NMDC.attribute,
    domain=None,
    range=Optional[str],
)

slots.assembly_identifiers = Slot(
    uri=NMDC.assembly_identifiers,
    name="assembly_identifiers",
    curie=NMDC.curie("assembly_identifiers"),
    model_uri=NMDC.assembly_identifiers,
    domain=None,
    range=Optional[str],
)

slots.insdc_identifiers = Slot(
    uri=NMDC.insdc_identifiers,
    name="insdc_identifiers",
    curie=NMDC.curie("insdc_identifiers"),
    model_uri=NMDC.insdc_identifiers,
    domain=None,
    range=Optional[str],
)

slots.raw_type = Slot(
    uri=NMDC.raw_type,
    name="raw_type",
    curie=NMDC.curie("raw_type"),
    model_uri=NMDC.raw_type,
    domain=None,
    range=Optional[str],
)

slots.WorkflowExecutionActivity_was_associated_with = Slot(
    uri=NMDC.was_associated_with,
    name="WorkflowExecutionActivity_was_associated_with",
    curie=NMDC.curie("was_associated_with"),
    model_uri=NMDC.WorkflowExecutionActivity_was_associated_with,
    domain=WorkflowExecutionActivity,
    range=Optional[Union[str, WorkflowExecutionActivityId]],
)

slots.WorkflowExecutionActivity_has_input = Slot(
    uri=NMDC.has_input,
    name="WorkflowExecutionActivity_has_input",
    curie=NMDC.curie("has_input"),
    model_uri=NMDC.WorkflowExecutionActivity_has_input,
    domain=WorkflowExecutionActivity,
    range=Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]],
)

slots.WorkflowExecutionActivity_has_output = Slot(
    uri=NMDC.has_output,
    name="WorkflowExecutionActivity_has_output",
    curie=NMDC.curie("has_output"),
    model_uri=NMDC.WorkflowExecutionActivity_has_output,
    domain=WorkflowExecutionActivity,
    range=Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]],
)

slots.WorkflowExecutionActivity_was_informed_by = Slot(
    uri=NMDC.was_informed_by,
    name="WorkflowExecutionActivity_was_informed_by",
    curie=NMDC.curie("was_informed_by"),
    model_uri=NMDC.WorkflowExecutionActivity_was_informed_by,
    domain=WorkflowExecutionActivity,
    range=Union[str, ActivityId],
)

slots.WorkflowExecutionActivity_execution_resource = Slot(
    uri=NMDC.execution_resource,
    name="WorkflowExecutionActivity_execution_resource",
    curie=NMDC.curie("execution_resource"),
    model_uri=NMDC.WorkflowExecutionActivity_execution_resource,
    domain=WorkflowExecutionActivity,
    range=str,
)
