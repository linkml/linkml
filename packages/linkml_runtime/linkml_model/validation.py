# Auto generated from validation.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-05-19T21:54:12
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

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from .types import Nodeidentifier, String
from linkml_runtime.utils.metamodelcore import NodeIdentifier

metamodel_version = "1.7.0"
version = None

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
SH = CurieNamespace('sh', 'https://w3id.org/shacl/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = REPORTING


# Types

# Class references



@dataclass
class ValidationReport(YAMLRoot):
    """
    A report object
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SH.ValidationReport
    class_class_curie: ClassVar[str] = "sh:ValidationReport"
    class_name: ClassVar[str] = "ValidationReport"
    class_model_uri: ClassVar[URIRef] = REPORTING.ValidationReport

    results: Optional[Union[Union[dict, "ValidationResult"], List[Union[dict, "ValidationResult"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [v if isinstance(v, ValidationResult) else ValidationResult(**as_dict(v)) for v in self.results]

        super().__post_init__(**kwargs)


@dataclass
class ValidationResult(YAMLRoot):
    """
    An individual result arising from validation of a data instance using a particular rule
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SH.ValidationResult
    class_class_curie: ClassVar[str] = "sh:ValidationResult"
    class_name: ClassVar[str] = "ValidationResult"
    class_model_uri: ClassVar[URIRef] = REPORTING.ValidationResult

    type: Optional[Union[str, NodeIdentifier]] = None
    severity: Optional[Union[str, "SeverityOptions"]] = None
    subject: Optional[Union[str, NodeIdentifier]] = None
    instantiates: Optional[Union[str, NodeIdentifier]] = None
    predicate: Optional[Union[str, NodeIdentifier]] = None
    object: Optional[Union[str, NodeIdentifier]] = None
    object_str: Optional[str] = None
    source: Optional[Union[str, NodeIdentifier]] = None
    info: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, NodeIdentifier):
            self.type = NodeIdentifier(self.type)

        if self.severity is not None and not isinstance(self.severity, SeverityOptions):
            self.severity = SeverityOptions(self.severity)

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


# Enumerations
class ProblemType(EnumDefinitionImpl):

    undeclared_slot = PermissibleValue(text="undeclared_slot",
                                                     description="Applies when a slot is used in data but the slot is undeclared in the datamodel")
    inapplicable_slot = PermissibleValue(text="inapplicable_slot",
                                                         description="Applies when a slot is used in an instance of a class where the slot is not applicable for that class")
    missing_slot_value = PermissibleValue(text="missing_slot_value",
                                                           description="Applies when an instance of a class has a required slot which is not filled in")
    slot_range_violation = PermissibleValue(text="slot_range_violation",
                                                               description="Applies when the value of a slot is inconsistent with the declared range")
    max_count_violation = PermissibleValue(text="max_count_violation",
                                                             meaning=SH.MaxCountConstraintComponent)
    parsing_error = PermissibleValue(text="parsing_error",
                                                 description="The data could not be parsed")

    _defn = EnumDefinition(
        name="ProblemType",
    )

class SeverityOptions(EnumDefinitionImpl):

    FATAL = PermissibleValue(text="FATAL")
    ERROR = PermissibleValue(text="ERROR",
                                 meaning=SH.Violation)
    WARNING = PermissibleValue(text="WARNING",
                                     meaning=SH.Warning)
    INFO = PermissibleValue(text="INFO",
                               meaning=SH.Info)

    _defn = EnumDefinition(
        name="SeverityOptions",
    )

# Slots

