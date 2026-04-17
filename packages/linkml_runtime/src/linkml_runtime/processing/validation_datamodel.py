# Auto generated from validation_datamodel.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-04-15T15:13:14
# Schema: validaton-results
#
# id: https://w3id.org/linkml/validation_results
# description: A datamodel for data validation results.
# license: https://creativecommons.org/publicdomain/zero/1.0/

from dataclasses import dataclass
from typing import Any, ClassVar, Optional, Union

from jsonasobj2 import as_dict
from rdflib import URIRef

from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE, empty_dict, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot

metamodel_version = "1.7.0"
version = None

# Namespaces
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
OWL = CurieNamespace("owl", "http://www.w3.org/2002/07/owl#")
PAV = CurieNamespace("pav", "http://purl.org/pav/")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SH = CurieNamespace("sh", "http://www.w3.org/ns/shacl#")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
VM = CurieNamespace("vm", "https://w3id.org/linkml/validation-model/")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = VM


# Types


# Class references
class ConstraintCheckId(URIorCURIE):
    pass


class NodeId(URIorCURIE):
    pass


class TypeSeverityKeyValueType(URIorCURIE):
    pass


@dataclass(repr=False)
class ConstraintCheck(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ClassDefinition"]
    class_class_curie: ClassVar[str] = "linkml:ClassDefinition"
    class_name: ClassVar[str] = "ConstraintCheck"
    class_model_uri: ClassVar[URIRef] = VM.ConstraintCheck

    id: Union[str, ConstraintCheckId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ConstraintCheckId):
            self.id = ConstraintCheckId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Node(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ClassDefinition"]
    class_class_curie: ClassVar[str] = "linkml:ClassDefinition"
    class_name: ClassVar[str] = "Node"
    class_model_uri: ClassVar[URIRef] = VM.Node

    id: Union[str, NodeId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeId):
            self.id = NodeId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ValidationConfiguration(YAMLRoot):
    """
    Configuration parameters for execution of a validation report
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ClassDefinition"]
    class_class_curie: ClassVar[str] = "linkml:ClassDefinition"
    class_name: ClassVar[str] = "ValidationConfiguration"
    class_model_uri: ClassVar[URIRef] = VM.ValidationConfiguration

    max_number_results_per_type: Optional[int] = None
    type_severity_map: Optional[
        Union[
            dict[Union[str, TypeSeverityKeyValueType], Union[dict, "TypeSeverityKeyValue"]],
            list[Union[dict, "TypeSeverityKeyValue"]],
        ]
    ] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.max_number_results_per_type is not None and not isinstance(self.max_number_results_per_type, int):
            self.max_number_results_per_type = int(self.max_number_results_per_type)

        self._normalize_inlined_as_dict(
            slot_name="type_severity_map", slot_type=TypeSeverityKeyValue, key_name="type", keyed=True
        )

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RepairConfiguration(YAMLRoot):
    """
    Configuration parameters for execution of validation repairs
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ClassDefinition"]
    class_class_curie: ClassVar[str] = "linkml:ClassDefinition"
    class_name: ClassVar[str] = "RepairConfiguration"
    class_model_uri: ClassVar[URIRef] = VM.RepairConfiguration

    validation_configuration: Optional[Union[dict, ValidationConfiguration]] = None
    dry_run: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.validation_configuration is not None and not isinstance(
            self.validation_configuration, ValidationConfiguration
        ):
            self.validation_configuration = ValidationConfiguration(**as_dict(self.validation_configuration))

        if self.dry_run is not None and not isinstance(self.dry_run, Bool):
            self.dry_run = Bool(self.dry_run)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TypeSeverityKeyValue(YAMLRoot):
    """
    key-value pair that maps a validation result type to a severity setting, for overriding default severity
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ClassDefinition"]
    class_class_curie: ClassVar[str] = "linkml:ClassDefinition"
    class_name: ClassVar[str] = "TypeSeverityKeyValue"
    class_model_uri: ClassVar[URIRef] = VM.TypeSeverityKeyValue

    type: Union[str, TypeSeverityKeyValueType] = None
    severity: Optional[Union[str, "SeverityType"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, TypeSeverityKeyValueType):
            self.type = TypeSeverityKeyValueType(self.type)

        if self.severity is not None and not isinstance(self.severity, SeverityType):
            self.severity = SeverityType(self.severity)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Report(YAMLRoot):
    """
    A report object that is a holder to multiple report results
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ClassDefinition"]
    class_class_curie: ClassVar[str] = "linkml:ClassDefinition"
    class_name: ClassVar[str] = "Report"
    class_model_uri: ClassVar[URIRef] = VM.Report

    results: Optional[Union[Union[dict, "Result"], list[Union[dict, "Result"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [v if isinstance(v, Result) else Result(**as_dict(v)) for v in self.results]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ValidationReport(Report):
    """
    A report that consists of validation results
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SH["ValidationReport"]
    class_class_curie: ClassVar[str] = "sh:ValidationReport"
    class_name: ClassVar[str] = "ValidationReport"
    class_model_uri: ClassVar[URIRef] = VM.ValidationReport

    results: Optional[Union[Union[dict, "ValidationResult"], list[Union[dict, "ValidationResult"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="results", slot_type=ValidationResult, key_name="type", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RepairReport(Report):
    """
    A report that consists of repair operation results
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ClassDefinition"]
    class_class_curie: ClassVar[str] = "linkml:ClassDefinition"
    class_name: ClassVar[str] = "RepairReport"
    class_model_uri: ClassVar[URIRef] = VM.RepairReport

    results: Optional[Union[Union[dict, "RepairOperation"], list[Union[dict, "RepairOperation"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [v if isinstance(v, RepairOperation) else RepairOperation(**as_dict(v)) for v in self.results]

        super().__post_init__(**kwargs)


class Result(YAMLRoot):
    """
    Abstract base class for any individual report result
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ClassDefinition"]
    class_class_curie: ClassVar[str] = "linkml:ClassDefinition"
    class_name: ClassVar[str] = "Result"
    class_model_uri: ClassVar[URIRef] = VM.Result


@dataclass(repr=False)
class ValidationResult(Result):
    """
    An individual result arising from validation of a data instance using a particular rule
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SH["ValidationResult"]
    class_class_curie: ClassVar[str] = "sh:ValidationResult"
    class_name: ClassVar[str] = "ValidationResult"
    class_model_uri: ClassVar[URIRef] = VM.ValidationResult

    type: Union[str, "ConstraintType"] = None
    severity: Optional[Union[str, "SeverityType"]] = None
    subject: Optional[str] = None
    instantiates: Optional[Union[str, NodeId]] = None
    predicate: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    object_str: Optional[str] = None
    source: Optional[str] = None
    info: Optional[str] = None
    normalized: Optional[Union[bool, Bool]] = None
    repaired: Optional[Union[bool, Bool]] = None
    source_line_number: Optional[int] = None
    source_column_number: Optional[int] = None
    source_location: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, ConstraintType):
            self.type = ConstraintType(self.type)

        if self.severity is not None and not isinstance(self.severity, SeverityType):
            self.severity = SeverityType(self.severity)

        if self.subject is not None and not isinstance(self.subject, str):
            self.subject = str(self.subject)

        if self.instantiates is not None and not isinstance(self.instantiates, NodeId):
            self.instantiates = NodeId(self.instantiates)

        if self.predicate is not None and not isinstance(self.predicate, NodeId):
            self.predicate = NodeId(self.predicate)

        if self.object is not None and not isinstance(self.object, NodeId):
            self.object = NodeId(self.object)

        if self.object_str is not None and not isinstance(self.object_str, str):
            self.object_str = str(self.object_str)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        if self.info is not None and not isinstance(self.info, str):
            self.info = str(self.info)

        if self.normalized is not None and not isinstance(self.normalized, Bool):
            self.normalized = Bool(self.normalized)

        if self.repaired is not None and not isinstance(self.repaired, Bool):
            self.repaired = Bool(self.repaired)

        if self.source_line_number is not None and not isinstance(self.source_line_number, int):
            self.source_line_number = int(self.source_line_number)

        if self.source_column_number is not None and not isinstance(self.source_column_number, int):
            self.source_column_number = int(self.source_column_number)

        if self.source_location is not None and not isinstance(self.source_location, str):
            self.source_location = str(self.source_location)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RepairOperation(Result):
    """
    The result of performing an individual repair
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ClassDefinition"]
    class_class_curie: ClassVar[str] = "linkml:ClassDefinition"
    class_name: ClassVar[str] = "RepairOperation"
    class_model_uri: ClassVar[URIRef] = VM.RepairOperation

    repairs: Optional[Union[dict, ValidationResult]] = None
    modified: Optional[Union[bool, Bool]] = None
    successful: Optional[Union[bool, Bool]] = None
    info: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.repairs is not None and not isinstance(self.repairs, ValidationResult):
            self.repairs = ValidationResult(**as_dict(self.repairs))

        if self.modified is not None and not isinstance(self.modified, Bool):
            self.modified = Bool(self.modified)

        if self.successful is not None and not isinstance(self.successful, Bool):
            self.successful = Bool(self.successful)

        if self.info is not None and not isinstance(self.info, str):
            self.info = str(self.info)

        super().__post_init__(**kwargs)


# Enumerations
class SeverityType(EnumDefinitionImpl):
    FATAL = PermissibleValue(text="FATAL")
    ERROR = PermissibleValue(text="ERROR", meaning=SH["Violation"])
    WARNING = PermissibleValue(text="WARNING", meaning=SH["Warning"])
    INFO = PermissibleValue(text="INFO", meaning=SH["Info"])

    _defn = EnumDefinition(
        name="SeverityType",
    )


class ConstraintType(EnumDefinitionImpl):
    TypeConstraint = PermissibleValue(
        text="TypeConstraint",
        description="constraint in which the range is a type, and the slot value must conform to the type",
        meaning=SH["DatatypeConstraintComponent"],
    )
    MinCountConstraint = PermissibleValue(
        text="MinCountConstraint",
        description="""cardinality constraint where the number of values of the slot must be greater or equal to a specified minimum""",
        meaning=SH["MinCountConstraintComponent"],
    )
    RequiredConstraint = PermissibleValue(
        text="RequiredConstraint",
        description="cardinality constraint where there MUST be at least one value of the slot",
        meaning=SH["MinCountConstraintComponent"],
    )
    RecommendedConstraint = PermissibleValue(
        text="RecommendedConstraint",
        description="cardinality constraint where there SHOULD be at least one value of the slot",
        meaning=SH["MinCountConstraintComponent"],
    )
    MaxCountConstraint = PermissibleValue(
        text="MaxCountConstraint",
        description="""cardinality constraint where the number of values of the slot must be less than or equal to a specified maximum""",
        meaning=SH["MaxCountConstraintComponent"],
    )
    SingleValuedConstraint = PermissibleValue(
        text="SingleValuedConstraint", description="the value of the slot must be atomic and not a collection"
    )
    MultiValuedConstraint = PermissibleValue(
        text="MultiValuedConstraint", description="the value of the slot must be a collection and not atomic"
    )
    DeprecatedProperty = PermissibleValue(
        text="DeprecatedProperty",
        description="constraint where the instance slot should not be deprecated",
        meaning=VM["DeprecatedProperty"],
    )
    MaxLengthConstraint = PermissibleValue(
        text="MaxLengthConstraint",
        description="constraint where the slot value must have a length equal to or less than a specified maximum",
        meaning=SH["MaxLengthConstraintComponent"],
    )
    MinLengthConstraint = PermissibleValue(
        text="MinLengthConstraint",
        description="constraint where the slot value must have a length equal to or less than a specified maximum",
        meaning=SH["MinLengthConstraintComponent"],
    )
    PatternConstraint = PermissibleValue(
        text="PatternConstraint",
        description="constraint where the slot value must match a given regular expression pattern",
        meaning=SH["PatternConstraintComponent"],
    )
    ClosedClassConstraint = PermissibleValue(
        text="ClosedClassConstraint",
        description="constraint where the slot value must be allowable for the instantiated class",
        meaning=SH["ClosedConstraintComponent"],
    )
    DesignatesTypeConstraint = PermissibleValue(text="DesignatesTypeConstraint")
    InstanceConstraint = PermissibleValue(text="InstanceConstraint", meaning=SH["NodeConstraintComponent"])
    SlotConstraint = PermissibleValue(text="SlotConstraint", meaning=SH["PropertyConstraintComponent"])
    PermissibleValueConstraint = PermissibleValue(
        text="PermissibleValueConstraint",
        description="constraint where the slot value must be one of a set of permissible values",
        meaning=SH["InConstraintComponent"],
    )
    UndeclaredSlotConstraint = PermissibleValue(text="UndeclaredSlotConstraint")
    RuleConstraint = PermissibleValue(
        text="RuleConstraint",
        description="constraint where the structure of an object must conform to a specified rule",
    )
    ExpressionConstraint = PermissibleValue(text="ExpressionConstraint")
    EqualsExpressionConstraint = PermissibleValue(
        text="EqualsExpressionConstraint", meaning=SH["EqualsConstraintComponent"]
    )
    LessThanExpressionConstraint = PermissibleValue(
        text="LessThanExpressionConstraint", meaning=SH["LessThanConstraintComponent"]
    )
    LessThanOrEqualsExpressionConstraint = PermissibleValue(
        text="LessThanOrEqualsExpressionConstraint", meaning=SH["LessThanOrEqualsComponent"]
    )
    DisjointConstraint = PermissibleValue(text="DisjointConstraint", meaning=SH["DisjointConstraintComponent"])
    MinimumValueConstraint = PermissibleValue(
        text="MinimumValueConstraint", meaning=SH["MinInclusiveConstraintComponent"]
    )
    MaximumValueConstraint = PermissibleValue(
        text="MaximumValueConstraint", meaning=SH["MaxInclusiveConstraintComponent"]
    )
    MinimumExclusiveValueConstraint = PermissibleValue(
        text="MinimumExclusiveValueConstraint", meaning=SH["MinExclusiveInclusiveConstraintComponent"]
    )
    MaximumExclusiveValueConstraint = PermissibleValue(
        text="MaximumExclusiveValueConstraint", meaning=SH["MaxExclusiveInclusiveConstraintComponent"]
    )
    CollectionFormConstraint = PermissibleValue(text="CollectionFormConstraint")
    ListCollectionFormConstraint = PermissibleValue(text="ListCollectionFormConstraint")
    DictCollectionFormConstraint = PermissibleValue(text="DictCollectionFormConstraint")
    SimpleDictCollectionFormConstraint = PermissibleValue(text="SimpleDictCollectionFormConstraint")
    CompactDictCollectionFormConstraint = PermissibleValue(text="CompactDictCollectionFormConstraint")
    ExpandedDictCollectionFormConstraint = PermissibleValue(text="ExpandedDictCollectionFormConstraint")

    _defn = EnumDefinition(
        name="ConstraintType",
    )


# Slots
class slots:
    pass


slots.type = Slot(
    uri=SH.sourceConstraintComponent,
    name="type",
    curie=SH.curie("sourceConstraintComponent"),
    model_uri=VM.type,
    domain=None,
    range=Union[str, "ConstraintType"],
)

slots.subject = Slot(
    uri=SH.focusNode,
    name="subject",
    curie=SH.curie("focusNode"),
    model_uri=VM.subject,
    domain=None,
    range=Optional[str],
)

slots.instantiates = Slot(
    uri=LINKML.slot_uri,
    name="instantiates",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.instantiates,
    domain=None,
    range=Optional[Union[str, NodeId]],
)

slots.predicate = Slot(
    uri=LINKML.slot_uri,
    name="predicate",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.predicate,
    domain=None,
    range=Optional[Union[str, NodeId]],
)

slots.object = Slot(
    uri=SH.value,
    name="object",
    curie=SH.curie("value"),
    model_uri=VM.object,
    domain=None,
    range=Optional[Union[str, NodeId]],
)

slots.object_str = Slot(
    uri=LINKML.slot_uri,
    name="object_str",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.object_str,
    domain=None,
    range=Optional[str],
)

slots.source = Slot(
    uri=LINKML.slot_uri,
    name="source",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.source,
    domain=None,
    range=Optional[str],
)

slots.severity = Slot(
    uri=SH.resultSeverity,
    name="severity",
    curie=SH.curie("resultSeverity"),
    model_uri=VM.severity,
    domain=None,
    range=Optional[Union[str, "SeverityType"]],
)

slots.info = Slot(
    uri=SH.resultMessage,
    name="info",
    curie=SH.curie("resultMessage"),
    model_uri=VM.info,
    domain=None,
    range=Optional[str],
)

slots.results = Slot(
    uri=SH.result,
    name="results",
    curie=SH.curie("result"),
    model_uri=VM.results,
    domain=None,
    range=Optional[Union[Union[dict, Result], list[Union[dict, Result]]]],
)

slots.normalized = Slot(
    uri=LINKML.slot_uri,
    name="normalized",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.normalized,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.repaired = Slot(
    uri=LINKML.slot_uri,
    name="repaired",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.repaired,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.source_line_number = Slot(
    uri=LINKML.slot_uri,
    name="source_line_number",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.source_line_number,
    domain=None,
    range=Optional[int],
)

slots.source_column_number = Slot(
    uri=LINKML.slot_uri,
    name="source_column_number",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.source_column_number,
    domain=None,
    range=Optional[int],
)

slots.source_location = Slot(
    uri=LINKML.slot_uri,
    name="source_location",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.source_location,
    domain=None,
    range=Optional[str],
)

slots.constraintCheck__id = Slot(
    uri=LINKML.slot_uri,
    name="constraintCheck__id",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.constraintCheck__id,
    domain=None,
    range=URIRef,
)

slots.node__id = Slot(
    uri=LINKML.slot_uri,
    name="node__id",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.node__id,
    domain=None,
    range=URIRef,
)

slots.validationConfiguration__max_number_results_per_type = Slot(
    uri=LINKML.slot_uri,
    name="validationConfiguration__max_number_results_per_type",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.validationConfiguration__max_number_results_per_type,
    domain=None,
    range=Optional[int],
)

slots.validationConfiguration__type_severity_map = Slot(
    uri=LINKML.slot_uri,
    name="validationConfiguration__type_severity_map",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.validationConfiguration__type_severity_map,
    domain=None,
    range=Optional[
        Union[
            dict[Union[str, TypeSeverityKeyValueType], Union[dict, TypeSeverityKeyValue]],
            list[Union[dict, TypeSeverityKeyValue]],
        ]
    ],
)

slots.repairConfiguration__validation_configuration = Slot(
    uri=LINKML.slot_uri,
    name="repairConfiguration__validation_configuration",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.repairConfiguration__validation_configuration,
    domain=None,
    range=Optional[Union[dict, ValidationConfiguration]],
)

slots.repairConfiguration__dry_run = Slot(
    uri=LINKML.slot_uri,
    name="repairConfiguration__dry_run",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.repairConfiguration__dry_run,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.typeSeverityKeyValue__type = Slot(
    uri=LINKML.slot_uri,
    name="typeSeverityKeyValue__type",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.typeSeverityKeyValue__type,
    domain=None,
    range=URIRef,
)

slots.typeSeverityKeyValue__severity = Slot(
    uri=LINKML.slot_uri,
    name="typeSeverityKeyValue__severity",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.typeSeverityKeyValue__severity,
    domain=None,
    range=Optional[Union[str, "SeverityType"]],
)

slots.repairOperation__repairs = Slot(
    uri=LINKML.slot_uri,
    name="repairOperation__repairs",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.repairOperation__repairs,
    domain=None,
    range=Optional[Union[dict, ValidationResult]],
)

slots.repairOperation__modified = Slot(
    uri=LINKML.slot_uri,
    name="repairOperation__modified",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.repairOperation__modified,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.repairOperation__successful = Slot(
    uri=LINKML.slot_uri,
    name="repairOperation__successful",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.repairOperation__successful,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.repairOperation__info = Slot(
    uri=LINKML.slot_uri,
    name="repairOperation__info",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.repairOperation__info,
    domain=None,
    range=Optional[str],
)

slots.ValidationReport_results = Slot(
    uri=LINKML.slot_uri,
    name="ValidationReport_results",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.ValidationReport_results,
    domain=ValidationReport,
    range=Optional[Union[Union[dict, "ValidationResult"], list[Union[dict, "ValidationResult"]]]],
)

slots.RepairReport_results = Slot(
    uri=LINKML.slot_uri,
    name="RepairReport_results",
    curie=LINKML.curie("slot_uri"),
    model_uri=VM.RepairReport_results,
    domain=RepairReport,
    range=Optional[Union[Union[dict, "RepairOperation"], list[Union[dict, "RepairOperation"]]]],
)
