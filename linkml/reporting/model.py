# Auto generated from reporting.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-09-01 20:03
# Schema: reporting
#
# id: https://w3id.org/linkml/reporting
# description: A datamodel for reports on data
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
from linkml_runtime.linkml_model.types import Nodeidentifier, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import NodeIdentifier, URIorCURIE

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
REPORTING = CurieNamespace('reporting', 'https://w3id.org/linkml/report')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = REPORTING


# Types

# Class references



@dataclass
class Report(YAMLRoot):
    """
    A report object
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.Report
    class_class_curie: ClassVar[str] = "reporting:Report"
    class_name: ClassVar[str] = "report"
    class_model_uri: ClassVar[URIRef] = REPORTING.Report

    results: Optional[Union[Union[dict, "CheckResult"], List[Union[dict, "CheckResult"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [v if isinstance(v, CheckResult) else CheckResult(**as_dict(v)) for v in self.results]

        super().__post_init__(**kwargs)


@dataclass
class CheckResult(YAMLRoot):
    """
    An individual check
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.CheckResult
    class_class_curie: ClassVar[str] = "reporting:CheckResult"
    class_name: ClassVar[str] = "check_result"
    class_model_uri: ClassVar[URIRef] = REPORTING.CheckResult

    type: Optional[Union[str, URIorCURIE]] = None
    subject: Optional[Union[str, NodeIdentifier]] = None
    instantiates: Optional[Union[str, NodeIdentifier]] = None
    predicate: Optional[Union[str, NodeIdentifier]] = None
    object: Optional[Union[str, NodeIdentifier]] = None
    object_str: Optional[str] = None
    source: Optional[Union[str, NodeIdentifier]] = None
    info: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, URIorCURIE):
            self.type = URIorCURIE(self.type)

        if self.subject is not None and not isinstance(self.subject, NodeIdentifier):
            self.subject = NodeIdentifier(self.subject)

        if self.instantiates is not None and not isinstance(self.instantiates, NodeIdentifier):
            self.instantiates = NodeIdentifier(self.instantiates)

        if self.predicate is not None and not isinstance(self.predicate, NodeIdentifier):
            self.predicate = NodeIdentifier(self.predicate)

        if self.object is not None and not isinstance(self.object, NodeIdentifier):
            self.object = NodeIdentifier(self.object)

        if self.object_str is not None and not isinstance(self.object_str, str):
            self.object_str = str(self.object_str)

        if self.source is not None and not isinstance(self.source, NodeIdentifier):
            self.source = NodeIdentifier(self.source)

        if self.info is not None and not isinstance(self.info, str):
            self.info = str(self.info)

        super().__post_init__(**kwargs)


class Problem(CheckResult):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.Problem
    class_class_curie: ClassVar[str] = "reporting:Problem"
    class_name: ClassVar[str] = "problem"
    class_model_uri: ClassVar[URIRef] = REPORTING.Problem


class ProblemSlotUndeclared(Problem):
    """
    A problem in which an undeclared slot is used
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.ProblemSlotUndeclared
    class_class_curie: ClassVar[str] = "reporting:ProblemSlotUndeclared"
    class_name: ClassVar[str] = "problem_slot_undeclared"
    class_model_uri: ClassVar[URIRef] = REPORTING.ProblemSlotUndeclared


class ProblemSlotInapplicable(Problem):
    """
    A problem in which a slot is used in an instance of a class where the slot is not applicable for that class
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.ProblemSlotInapplicable
    class_class_curie: ClassVar[str] = "reporting:ProblemSlotInapplicable"
    class_name: ClassVar[str] = "problem_slot_inapplicable"
    class_model_uri: ClassVar[URIRef] = REPORTING.ProblemSlotInapplicable


class ProblemSlotMissing(Problem):
    """
    A problem in which an instance of a class has a required slot which is not filled in
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.ProblemSlotMissing
    class_class_curie: ClassVar[str] = "reporting:ProblemSlotMissing"
    class_name: ClassVar[str] = "problem_slot_missing"
    class_model_uri: ClassVar[URIRef] = REPORTING.ProblemSlotMissing


# Enumerations
class SeverityOptions(EnumDefinitionImpl):

    FATAL = PermissibleValue(text="FATAL")
    ERROR = PermissibleValue(text="ERROR")
    WARNING = PermissibleValue(text="WARNING")
    INFO = PermissibleValue(text="INFO")

    _defn = EnumDefinition(
        name="SeverityOptions",
    )

# Slots
class slots:
    pass

slots.type = Slot(uri=REPORTING.type, name="type", curie=REPORTING.curie('type'),
                   model_uri=REPORTING.type, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.subject = Slot(uri=REPORTING.subject, name="subject", curie=REPORTING.curie('subject'),
                   model_uri=REPORTING.subject, domain=None, range=Optional[Union[str, NodeIdentifier]])

slots.instantiates = Slot(uri=REPORTING.instantiates, name="instantiates", curie=REPORTING.curie('instantiates'),
                   model_uri=REPORTING.instantiates, domain=None, range=Optional[Union[str, NodeIdentifier]])

slots.predicate = Slot(uri=REPORTING.predicate, name="predicate", curie=REPORTING.curie('predicate'),
                   model_uri=REPORTING.predicate, domain=None, range=Optional[Union[str, NodeIdentifier]])

slots.object = Slot(uri=REPORTING.object, name="object", curie=REPORTING.curie('object'),
                   model_uri=REPORTING.object, domain=None, range=Optional[Union[str, NodeIdentifier]])

slots.object_str = Slot(uri=REPORTING.object_str, name="object_str", curie=REPORTING.curie('object_str'),
                   model_uri=REPORTING.object_str, domain=None, range=Optional[str])

slots.source = Slot(uri=REPORTING.source, name="source", curie=REPORTING.curie('source'),
                   model_uri=REPORTING.source, domain=None, range=Optional[Union[str, NodeIdentifier]])

slots.severity = Slot(uri=REPORTING.severity, name="severity", curie=REPORTING.curie('severity'),
                   model_uri=REPORTING.severity, domain=None, range=Optional[Union[str, "SeverityOptions"]])

slots.info = Slot(uri=REPORTING.info, name="info", curie=REPORTING.curie('info'),
                   model_uri=REPORTING.info, domain=None, range=Optional[str])

slots.report__results = Slot(uri=REPORTING.results, name="report__results", curie=REPORTING.curie('results'),
                   model_uri=REPORTING.report__results, domain=None, range=Optional[Union[Union[dict, CheckResult], List[Union[dict, CheckResult]]]])
