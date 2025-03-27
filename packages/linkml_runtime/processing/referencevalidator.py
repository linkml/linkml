"""Reference implementation for validations and normalization.

See:

- `Part 5<https://w3id.org/linkml/specification/05validation>`_ of LinkML specification
- `Part 6<https://w3id.org/linkml/specification/06mapping>`_ of LinkML specification
"""
import decimal
import re
import sys
from copy import copy
from dataclasses import dataclass, field
import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Optional, Union, TextIO
from collections.abc import Iterator

import click
import yaml

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import (
    SlotDefinition,
    ClassDefinition,
    EnumDefinition,
    TypeDefinition,
    Element,
    SchemaDefinition,
    SlotDefinitionName,
)
from linkml_runtime.linkml_model.meta import (
    AnonymousClassExpression,
    AnonymousSlotExpression,
    ClassRule,
    ClassDefinitionName,
)
from linkml_runtime.processing.validation_datamodel import (
    ConstraintType,
    ValidationResult, ValidationConfiguration,
)
from linkml_runtime.utils import yamlutils
from linkml_runtime.utils.eval_utils import eval_expr
from linkml_runtime.utils.metamodelcore import (
    XSDTime,
    Bool,
    XSDDate,
    URIorCURIE,
    URI,
    NCName,
    ElementIdentifier,
    NodeIdentifier,
)


# Mapping from either XSD types or LinkML type.base fields to Python types;
# (the coerced type is the last element of the tuple, the others are
# acceptable types)
XSD_OR_BASE_TO_PYTHON = {
    # Base type mapping (first)
    "URIorCURIE": (str, yamlutils.extended_str, URIorCURIE),
    "URI": (str, yamlutils.extended_str, URI),
    "NCName": (str, yamlutils.extended_str, NCName),
    "ElementIdentifier": (str, yamlutils.extended_str, ElementIdentifier),
    "NodeIdentifier": (str, yamlutils.extended_str, NodeIdentifier),
    # XSD type mapping (second)
    "xsd:string": str,
    "xsd:integer": int,
    "xsd:float": float,
    "xsd:boolean": (bool, Bool),
    "xsd:double": float,
    "xsd:decimal": Decimal,
    "xsd:dateTime": (str, datetime.datetime, datetime.time, XSDTime),
    "xsd:date": (str, datetime.date, XSDDate),
    "xsd:time": (str, datetime.time, XSDTime),
}


def _is_list_of_lists(x: Any) -> bool:
    """
    True x is of the form `[[...`

    >>> _is_list_of_lists([1])
    False
    >>> _is_list_of_lists([[1,2],[3,4]])
    True
    >>> _is_list_of_lists([[]])
    True

    :param x: element to be tested
    :return: True if LoL
    """
    return x and isinstance(x, list) and isinstance(x[0], list)


def linearize_nested_lists(nested_list: list, is_row_ordered=True):
    """
    Returns a linear sequence of elements corresponding to a nested list array representation

    >>> linearize_nested_lists([[11,12,13],[21,22,23],[31,32,33]], is_row_ordered=True)
    [11, 12, 13, 21, 22, 23, 31, 32, 33]

    >>> linearize_nested_lists([[11,12,13],[21,22,23],[31,32,33]], is_row_ordered=False)
    [11, 21, 31, 12, 22, 32, 13, 23, 33]

    :param nested_list:
    :param is_row_ordered:
    :return:
    """
    if not is_row_ordered:
        return _linearize_nested_list_column_order(nested_list)
    # row-ordered
    result = []
    stack = [iter(nested_list)]
    while stack:
        try:
            item = next(stack[-1])
            if isinstance(item, list):
                stack.append(iter(item))
            else:
                result.append(item)
        except StopIteration:
            stack.pop()
    return result


def _linearize_nested_list_column_order(nested_list):
    result = []
    if not nested_list:
        return result

    num_rows = len(nested_list)
    max_row_len = max(len(row) for row in nested_list)

    for col in range(max_row_len):
        for row in range(num_rows):
            if col < len(nested_list[row]):
                result.append(nested_list[row][col])

    return result

class CollectionForm(Enum):
    """Form of a schema element.
    See Part 6 of the LinkML specification"""

    NonCollection = "NonCollection"
    ExpandedDict = "ExpandedDict"
    CompactDict = "CompactDict"
    SimpleDict = "SimpleDict"
    List = "List"
    ListOfLists = "ListOfLists"


COLLECTION_FORM_NORMALIZATION = tuple[CollectionForm, CollectionForm]
COLLECTION_FORM_ANNOTATION_KEY = "collection_form"


@dataclass
class Normalization:
    """A transformation of a schema element"""


@dataclass
class CollectionFormNormalization(Normalization):
    """A normalization that maps from one collection form to another"""
    input_form: CollectionForm = None
    output_form: CollectionForm = None


@dataclass
class TypeNormalization(Normalization):
    input_form: str = None
    output_form: str = None


@dataclass
class Report:
    """A report of validation results"""

    configuration: ValidationConfiguration = None
    """Customization of reporting."""

    results: list[ValidationResult] = field(default_factory=lambda: [])
    """All results, including normalized"""

    normalizations: list[Normalization] = field(default_factory=lambda: [])
    """All normalizations and repairs applied"""

    def combine(self, other: "Report") -> "Report":
        self.results.extend(other.results)
        return self

    def add_collection_form_normalization(
        self,
        problem_type: ConstraintType,
        before: CollectionForm,
        after: CollectionForm,
    ):
        """
        Add a collection form normalization to the report.

        :param problem_type:
        :param before:
        :param after:
        :return:
        """
        result = ValidationResult(type=ConstraintType.SlotConstraint)
        norm = CollectionFormNormalization(input_form=before, output_form=after)
        # result.repairs.append(norm)
        result.normalized = True
        result.repaired = True
        self.results.append(result)
        self.normalizations.append(norm)

    def add_type_normalization(self, before: str, after: str):
        result = ValidationResult(type=ConstraintType.TypeConstraint)
        norm = TypeNormalization(input_form=before, output_form=after)
        # result.repairs.append(norm)
        result.normalized = True
        result.repaired = True
        self.results.append(result)
        self.normalizations.append(norm)

    def add_problem(
        self,
        problem_type: ConstraintType,
        instantiates: str,
        subject: Any,
        predicate: Optional[str] = None,
        **kwargs,
    ):
        result = ValidationResult(
            type=problem_type,
            instantiates=instantiates,
            subject=str(subject),
            predicate=predicate,
            **kwargs,
        )
        locator = None
        if isinstance(subject, yamlutils.TypedNode):
            locator = subject
        elif isinstance(predicate, yamlutils.TypedNode):
            locator = predicate
        if locator and locator._s:
            result.source_line_number = locator._s.line
            result.source_column_number = locator._s.column
            result.source_location = locator.yaml_loc()
        self.results.append(result)

    def _is_error(self, result: ValidationResult) -> bool:
        return result.type != ConstraintType(ConstraintType.RecommendedConstraint)

    def errors(self) -> list[ValidationResult]:
        """
        Return a list of all results that are not normalized and do not have ERROR severity
        """
        # TODO: use severity
        return [r for r in self.results_excluding_normalized() if self._is_error(r)]

    def warnings(self) -> list[ValidationResult]:
        """
        Return a list of all results that are not normalized and do not have ERROR severity
        """
        # TODO: use severity
        return [r for r in self.results_excluding_normalized() if not self._is_error(r)]

    def results_excluding_normalized(self) -> list[ValidationResult]:
        return [r for r in self.results if not r.normalized]

    def unrepaired_problem_types(self) -> list[ConstraintType]:
        return [r.type for r in self.results_excluding_normalized()]

    def normalized_results(self) -> list[ValidationResult]:
        return [r for r in self.results if r.normalized]

    def collection_form_normalizations(
        self,
    ) -> Iterator[tuple[CollectionForm, CollectionForm]]:
        for norm in self.normalizations:
            if isinstance(norm, CollectionFormNormalization):
                yield norm.input_form, norm.output_form


def _remove_pk(obj: dict, pk_slot_name: str) -> dict:
    """Make a new CompactDict ready copy of a dict, removing the pk_slot_name"""
    if pk_slot_name in obj:
        obj = copy(obj)
        del obj[pk_slot_name]
    return obj


def _add_pk(obj: dict, pk_slot_name: str, pk_val: Any) -> dict:
    """Make a new ExpandedDict ready copy of a dict, adding the pk_slot_name"""
    if obj is None:
        return {pk_slot_name: pk_val}
    if pk_slot_name not in obj:
        obj = copy(obj)
        obj[pk_slot_name] = pk_val
    return obj


def _simple_to_dict(obj: Union[dict, Any], simple_value_slot_name: str) -> dict:
    """Make a new Dict from a simple value"""
    if isinstance(obj, dict):
        return obj
    return {simple_value_slot_name: obj}


@dataclass
class ReferenceValidator:
    """
    An engine that performs combined normalization and validation of instances according to a schema.

    See:

    - `Part 5<https://w3id.org/linkml/specification/05validation>`_ of LinkML specification
    - `Part 6<https://w3id.org/linkml/specification/06mapping>`_ of LinkML specification

    The ReferenceValidator works by first retrieving the *derived* schema given an input asserted
    schema, using :ref:`SchemaView`.

    The input data object is in dictionary form, isomorphic to a JSON document. The ReferenceValidator will
    descendant into the input object, first applying *normalization* rules (part 6), then applying *validation* rules
    (part 5).

    The output is (1) a new *normalized* object, and (2) a :ref:`Report` of validation results.
    """

    schemaview: SchemaView
    """View over source schema"""

    derived_schema: SchemaDefinition = None
    """Schema derived following part 4 of LinkML specification"""

    filter_invalid_objects: bool = False
    """If True, then remove any invalid objects from the tree"""

    auto_type_designator: Optional[str] = None
    """Set to equal "@type" for JSON-LD serialization"""

    skip_validation: bool = None
    """If True, then only perform normalization, not validation"""

    skip_normalization: bool = None
    """If True, then only perform validation, not normalization"""

    expand_all: bool = None
    """If True, then expand all SimpleDict and CompactDict objects to ExpandedDicts"""

    def __post_init__(self):
        self.derived_schema = self.schemaview.materialize_derived_schema()

    def validate(self, input_object: Any, target: Optional[str] = None) -> Report:
        """
        Validate an instance according to the schema

        :param input_object:
        :param target:
        :return:
        """
        parent_slot = self._create_index_slot(target, input_object)
        report = Report()
        self.normalize_slot_value(input_object, parent_slot, report)
        return report

    def normalize(
        self,
        input_object: Any,
        target: Optional[str] = None,
        report: Optional[Report] = None,
    ) -> Any:
        """
        Normalize an instance according to the schema

        :param input_object:
        :param target:
        :param report:
        :return:
        """
        parent_slot = self._create_index_slot(target, input_object)
        if report is None:
            report = Report()
        return self.normalize_slot_value(input_object, parent_slot, report)

    def _create_index_slot(
        self, target: Optional[str] = None, input_object: Any = None
    ) -> SlotDefinition:
        """
        Create a parent slot that points at the target element.

        :param target:
        :param input_object:
        :return:
        """
        target = self._schema_root(target)
        slot = SlotDefinition(name="temp", range=target, inlined=True)
        if input_object is None or isinstance(input_object, dict):
            slot.inlined = True
        elif isinstance(input_object, list):
            slot.inlined = True
            slot.inlined_as_list = True
            slot.multivalued = True
        return slot

    def _schema_root(
        self, target: Optional[str] = None
    ) -> Optional[ClassDefinitionName]:
        if target is not None:
            return ClassDefinitionName(target)
        roots = [r.name for r in self.derived_schema.classes.values() if r.tree_root]
        if len(roots) != 1:
            raise ValueError(f"Cannot normalize: {len(roots)} roots found")
        return roots[0]

    def normalize_slot_value(
        self, input_object: Any, parent_slot: SlotDefinition, report: Report
    ) -> Any:
        pk_slot_name = None
        range_element = self._slot_range_element(parent_slot)
        # Infer collection form, and normalize to this form, if necessary
        form = self.infer_slot_collection_form(parent_slot)
        normalized_object = copy(input_object)
        if isinstance(range_element, ClassDefinition):
            pk_slot_name = self._identifier_slot_name(range_element)
        normalized_object = self.normalize_to_collection_form(
            form, normalized_object, parent_slot, pk_slot_name, report
        )
        # Validate
        new_report = Report()
        if parent_slot.required and not normalized_object:
            report.add_problem(
                ConstraintType.RequiredConstraint, parent_slot.range, str(input_object)
            )
        if parent_slot.recommended and not normalized_object:
            report.add_problem(
                ConstraintType.RecommendedConstraint,
                parent_slot.range,
                str(input_object),
            )
        simple_dict_value_slot = self._slot_as_simple_dict_value_slot(parent_slot)
        if isinstance(normalized_object, dict) and parent_slot.multivalued:
            if not simple_dict_value_slot:
                output_object = {
                    k: self.normalize_instance(v, parent_slot, new_report)
                    for k, v in normalized_object.items()
                }
            else:
                output_object = {
                    k: self.normalize_instance(v, simple_dict_value_slot, new_report)
                    for k, v in normalized_object.items()
                }
        elif _is_list_of_lists(normalized_object):
            raise NotImplementedError(f"List of Lists: {normalized_object}")
        elif isinstance(normalized_object, list):
            output_object = [
                self.normalize_instance(v, parent_slot, new_report)
                for v in normalized_object
            ]
        else:
            # normalize an instance
            output_object = self.normalize_instance(
                normalized_object, parent_slot, new_report
            )
        report.combine(new_report)
        return output_object

    def _is_dict_collection(
        self, input_object: Any, parent_slot: SlotDefinition
    ) -> bool:
        if not isinstance(input_object, dict):
            return False
        if not parent_slot.multivalued:
            return False
        if parent_slot.inlined:
            return False
        if self.auto_type_designator and self.auto_type_designator in input_object:
            return False
        return True

    def infer_slot_collection_form(self, parent_slot: SlotDefinition) -> CollectionForm:
        if COLLECTION_FORM_ANNOTATION_KEY in parent_slot.annotations:
            v = parent_slot.annotations[COLLECTION_FORM_ANNOTATION_KEY].value
            if v:
                return CollectionForm[v]
        if not parent_slot.multivalued:
            return CollectionForm.NonCollection
        if not parent_slot.inlined:
            return CollectionForm.List
        if parent_slot.inlined_as_list:
            return CollectionForm.List
        if self.expand_all:
            return CollectionForm.ExpandedDict
        simple_dict_value_slot = self._slot_as_simple_dict_value_slot(parent_slot)
        if simple_dict_value_slot:
            return CollectionForm.SimpleDict
        # TODO: provide direct metamodel method
        if (
            "expanded" in parent_slot.annotations
            and parent_slot.annotations["expanded"].value
        ):
            return CollectionForm.ExpandedDict
        return CollectionForm.CompactDict

    def normalize_to_collection_form(
        self,
        form: CollectionForm,
        input_object: Any,
        slot: SlotDefinition,
        pk_slot_name: SlotDefinitionName,
        report: Report,
    ) -> Any:
        """
        Normalizes the input object to a defined form

        :param form:
        :param input_object:
        :param slot:
        :param pk_slot_name:
        :param report:
        :return:
        """
        if _is_list_of_lists(input_object):
            if form != CollectionForm.List:
                return input_object
            if not any(impl for impl in slot.implements if impl == "linkml:elements"):
                return input_object
            is_row_ordered = not any(impl for impl in slot.implements if impl == "linkml:ColumnOrderedArray")
            input_object = linearize_nested_lists(input_object, is_row_ordered)
        if form == CollectionForm.NonCollection:
            return self.ensure_non_collection(input_object, slot, pk_slot_name, report)
        elif form == CollectionForm.List:
            return self.ensure_list(input_object, slot, pk_slot_name, report)
        elif form == CollectionForm.ExpandedDict:
            return self.ensure_expanded_dict(input_object, slot, pk_slot_name, report)
        elif form == CollectionForm.CompactDict:
            return self.ensure_compact_dict(input_object, slot, pk_slot_name, report)
        elif form == CollectionForm.SimpleDict:
            return self.ensure_simple_dict(input_object, slot, pk_slot_name, report)
        else:
            raise AssertionError(f"{form} unrecognized")

    def ensure_non_collection(
        self,
        input_object: Any,
        parent_slot: SlotDefinition,
        pk_slot_name: SlotDefinitionName,
        report: Report,
    ) -> Any:
        if isinstance(input_object, list):
            # List -> Atom
            report.add_collection_form_normalization(
                ConstraintType.SingleValuedConstraint,
                CollectionForm.List,
                CollectionForm.NonCollection,
            )
            if len(input_object) == 0:
                return None
            return input_object[0]
        if self._is_dict_collection(input_object, parent_slot):
            # Dict -> Atom
            report.add_collection_form_normalization(
                ConstraintType.SingleValuedConstraint,
                CollectionForm.ExpandedDict,
                CollectionForm.NonCollection,
            )
            return list(input_object.values())[0]
        return input_object

    def ensure_list(
        self,
        input_object: Any,
        parent_slot: SlotDefinition,
        pk_slot_name: SlotDefinitionName,
        report: Report,
    ) -> Any:
        if not isinstance(input_object, (list, dict)):
            # Atom -> List
            report.add_collection_form_normalization(
                ConstraintType.MultiValuedConstraint,
                CollectionForm.NonCollection,
                CollectionForm.List,
            )
            return [input_object]
        if isinstance(input_object, dict):
            # Dict -> List
            def _obj_from_item(k, v):
                if pk_slot_name:
                    v = copy(v)
                    if pk_slot_name in input_object and input_object[pk_slot_name] != k:
                        # TODO: account for this differently
                        report.add_collection_form_normalization(
                            ConstraintType.ListCollectionFormConstraint,
                            CollectionForm.ExpandedDict,
                            CollectionForm.ExpandedDict,
                        )
                    v[str(pk_slot_name)] = k
                return v

            report.add_collection_form_normalization(
                ConstraintType.ListCollectionFormConstraint,
                CollectionForm.ExpandedDict,
                CollectionForm.List,
            )
            return [_obj_from_item(k, v) for k, v in list(input_object.items())]
        return input_object

    def ensure_expanded_dict(
        self,
        input_object: Any,
        parent_slot: SlotDefinition,
        pk_slot_name: SlotDefinitionName,
        report: Report,
    ) -> Any:
        if isinstance(input_object, list):
            # List -> Dict
            report.add_collection_form_normalization(
                ConstraintType.DictCollectionFormConstraint,
                CollectionForm.List,
                CollectionForm.ExpandedDict,
            )
            return {v.get(pk_slot_name): v for v in input_object}
        if isinstance(input_object, dict):
            simple_dict_value_slot = self._slot_as_simple_dict_value_slot(parent_slot)
            if simple_dict_value_slot and any(
                v
                for v in input_object.values()
                if v is not None and not isinstance(v, dict)
            ):
                # SimpleDict -> ExpandedDict
                report.add_collection_form_normalization(
                    ConstraintType.DictCollectionFormConstraint,
                    CollectionForm.SimpleDict,
                    CollectionForm.ExpandedDict,
                )
                return {
                    k: _add_pk(
                        _simple_to_dict(v, simple_dict_value_slot.name), pk_slot_name, k
                    )
                    for k, v in input_object.items()
                }
            else:
                # {ExpandedDict, CompactDict} -> ExpandedDict
                return {k: _add_pk(v, pk_slot_name, k) for k, v in input_object.items()}

    def ensure_compact_dict(
        self,
        input_object: Any,
        parent_slot: SlotDefinition,
        pk_slot_name: SlotDefinitionName,
        report: Report,
    ) -> Any:
        if isinstance(input_object, list):
            # List -> Dict
            report.add_collection_form_normalization(
                ConstraintType.DictCollectionFormConstraint,
                CollectionForm.List,
                CollectionForm.CompactDict,
            )
            return {
                v.get(pk_slot_name): _remove_pk(v, pk_slot_name) for v in input_object
            }
        elif isinstance(input_object, dict):
            if pk_slot_name and any(
                v
                for k, v in input_object.items()
                if isinstance(v, dict) and v.get(pk_slot_name, None) is not None
            ):
                report.add_collection_form_normalization(
                    ConstraintType.DictCollectionFormConstraint,
                    CollectionForm.ExpandedDict,
                    CollectionForm.CompactDict,
                )
                return {k: _remove_pk(v, pk_slot_name) for k, v in input_object.items()}
            else:
                return input_object
        else:
            report.add_collection_form_normalization(
                ConstraintType.DictCollectionFormConstraint,
                CollectionForm.List,
                CollectionForm.CompactDict,
            )
            return input_object

    def ensure_simple_dict(
        self,
        input_object: Any,
        parent_slot: SlotDefinition,
        pk_slot_name: SlotDefinitionName,
        report: Report,
    ) -> Any:
        simple_dict_value_slot = self._slot_as_simple_dict_value_slot(parent_slot)
        if not simple_dict_value_slot:
            raise AssertionError(
                f"Should have simple dict slot valie: {parent_slot.name}"
            )
        normalized_object = input_object
        if isinstance(input_object, list):
            normalized_object = {v[pk_slot_name]: v for v in input_object}
            original_form = CollectionForm.List
        else:
            original_form = CollectionForm.ExpandedDict
        # Dict -> SimpleDict
        new_normalized_object = {}
        simplified = False
        for k, v in normalized_object.items():
            if isinstance(v, dict):
                v_as_simple = self.normalize_slot_value(
                    v.get(simple_dict_value_slot.name), simple_dict_value_slot, report
                )
                new_normalized_object[k] = v_as_simple
                simplified = True
        if simplified:
            report.add_collection_form_normalization(
                ConstraintType.SimpleDictCollectionFormConstraint,
                original_form,
                CollectionForm.SimpleDict,
            )
            normalized_object = new_normalized_object
        elif original_form == CollectionForm.List:
            report.add_collection_form_normalization(
                ConstraintType.SimpleDictCollectionFormConstraint,
                original_form,
                CollectionForm.SimpleDict,
            )
        return normalized_object

    def normalize_instance(
        self, input_object: Any, parent_slot: SlotDefinition, report: Report
    ) -> Any:
        range_element = self._slot_range_element(parent_slot)
        if input_object is None:
            return None
        if isinstance(range_element, ClassDefinition):
            if parent_slot.inlined:
                if isinstance(input_object, dict):
                    return self.normalize_object(input_object, range_element, report)
                else:
                    report.add_problem(
                        ConstraintType.DictCollectionFormConstraint,
                        parent_slot.range,
                        input_object,
                        predicate=parent_slot.name,
                    )
                    return input_object
            else:
                return self.normalize_reference(input_object, range_element, report)
        elif isinstance(range_element, EnumDefinition):
            return self.normalize_enum(input_object, range_element, report)
        elif isinstance(range_element, TypeDefinition):
            return self.normalize_type(input_object, range_element, report, parent_slot)
        else:
            return input_object

    def normalize_reference(
        self, input_object: dict, target: ClassDefinition, report: Report
    ) -> dict:
        pk_slot = self._identifier_slot(target)
        if pk_slot is None:
            raise AssertionError(f"Cannot normalize: no primary key for {target.name}")
        return self.normalize_type(
            input_object, self.derived_schema.types.get(pk_slot.range, None), report
        )

    def normalize_object(
        self, input_object: dict, target: ClassDefinition, report: Report
    ) -> dict:
        if not isinstance(input_object, dict):
            raise AssertionError(
                f"Cannot normalize: expected dict, got {type(input_object)} for {input_object}"
            )
        output_object = {}
        # Induced slot
        for slot in target.attributes.values():
            # TODO: required slots MUST be present UNLESS this is a CompactDict
            if (
                slot.required
                and slot.alias not in input_object
                and not (slot.identifier or slot.key)
            ):
                report.add_problem(
                    ConstraintType.RequiredConstraint,
                    slot.name,
                    input_object,
                    predicate=target.name,
                )
            if (
                slot.recommended
                and slot.alias not in input_object
                and not (slot.identifier or slot.key)
            ):
                report.add_problem(
                    ConstraintType.RecommendedConstraint,
                    slot.name,
                    input_object,
                    predicate=target.name,
                )
            if slot.designates_type and slot.name in input_object:
                induced_class_name = self._class_name_from_value(
                    input_object[slot.name], slot.range
                )
                new_target = self.derived_schema.classes[induced_class_name]
                if not self.subsumes(target, new_target):
                    report.add_problem(
                        ConstraintType.DesignatesTypeConstraint,
                        slot.name,
                        new_target.name,
                    )
                target = new_target
        # deepen using classification rules
        for desc_cn in self.schemaview.class_descendants(target.name, reflexive=False):
            desc = self.derived_schema.classes[desc_cn]
            for expr in desc.classification_rules:
                if self._matches_class_expression(input_object, target, expr):
                    target = desc
                    break
        # Descend into slot values
        for k, v in input_object.items():
            actual_k = None
            if k in target.attributes:
                actual_k = k
            else:
                for a in target.attributes.values():
                    if a.alias == k:
                        actual_k = a.name
                        break
            if actual_k is None:
                report.add_problem(
                    ConstraintType.ClosedClassConstraint,
                    instantiates=target.name,
                    subject=input_object,
                    predicate=k,
                )
                if not self.filter_invalid_objects:
                    output_object[k] = v
                continue
            slot = target.attributes[actual_k]
            output_object[k] = self.normalize_slot_value(v, slot, report)
            if not self._matches_slot_expression(output_object[k], slot, output_object):
                report.add_problem(
                    ConstraintType.ExpressionConstraint, target.name, output_object[k]
                )
        for rule in target.rules:
            self.evaluate_rule(output_object, rule, report)
        return output_object

    def normalize_enum(
        self, input_object: Any, target: EnumDefinition, report: Report
    ) -> Any:
        if input_object not in target.permissible_values:
            report.add_problem(
                ConstraintType.PermissibleValueConstraint, target.name, input_object
            )
        return input_object

    def normalize_type(
        self,
        input_object: Any,
        target: Optional[TypeDefinition],
        report: Report,
        parent_slot: SlotDefinition = None,
    ) -> Any:
        if input_object is None:
            return None
        if target is None:
           return input_object
        output_value = input_object
        if target.base in XSD_OR_BASE_TO_PYTHON:
            expected_python_type = XSD_OR_BASE_TO_PYTHON[target.base]
        elif target.uri in XSD_OR_BASE_TO_PYTHON:
            expected_python_type = XSD_OR_BASE_TO_PYTHON[target.uri]
        else:
            report.add_problem(
                ConstraintType.UnmappedTypeConstraint, target.name, input_object
            )
            return output_value
        current_python_type = type(input_object)
        if isinstance(expected_python_type, tuple):
            expected_python_types = list(expected_python_type)
            normalize_func = expected_python_types[-1]
            cast_func = expected_python_types[0]
            if current_python_type in expected_python_types[:-1]:
                try:
                    output_value = cast_func(normalize_func(input_object))
                except Exception as e:
                    report.add_problem(
                        ConstraintType.TypeConstraint,
                        target.name,
                        input_object,
                        info=f"Coercion failed for {normalize_func}: {e}",
                    )
        else:
            normalize_func = expected_python_type
            cast_func = None
            expected_python_types = [expected_python_type]
        if current_python_type == yamlutils.extended_str:
            current_python_type = str
        if current_python_type not in expected_python_types:
            try:
                output_value = normalize_func(input_object)
                if cast_func is not None:
                    output_value = cast_func(output_value)
                report.add_type_normalization(
                    current_python_type.__name__, expected_python_types[0].__name__
                )
            except (ValueError, decimal.InvalidOperation) as e:
                problem = ValidationResult(
                    ConstraintType.TypeConstraint,
                    instantiates=target.name,
                    subject=input_object,
                    info=f"unable to coerce {current_python_type.__name__} to {target.uri}: {e}",
                )
                report.results.append(problem)
        # validation
        if parent_slot:
            if (
                parent_slot.maximum_value is not None
                and output_value > parent_slot.maximum_value
            ):
                report.add_problem(
                    ConstraintType.MaximumValueConstraint, target.name, input_object
                )
            if (
                parent_slot.minimum_value is not None
                and output_value < parent_slot.minimum_value
            ):
                report.add_problem(
                    ConstraintType.MinimumValueConstraint, target.name, input_object
                )
            if parent_slot.pattern is not None:
                if not re.match(parent_slot.pattern, output_value):
                    report.add_problem(
                        ConstraintType.PatternConstraint, target.name, input_object
                    )
            if parent_slot.equals_string is not None:
                if output_value != parent_slot.equals_string:
                    report.add_problem(
                        ConstraintType.ExpressionConstraint, target.name, input_object
                    )
        return output_value

    def evaluate_rule(
        self, input_object: dict, rule: ClassRule, report: Report
    ) -> None:
        for cond in rule.preconditions:
            if not self._matches_class_expression(
                input_object.get(cond.slot, None), cond, input_object
            ):
                return
        for cond in rule.postconditions:
            if not self._matches_class_expression(
                input_object.get(cond.slot, None), cond, input_object
            ):
                report.add_problem(ConstraintType.RuleViolation, rule.name)
                return

    def subsumes(self, parent: ClassDefinition, child: ClassDefinition):
        return parent.name in self.schemaview.class_ancestors(
            child.name, reflexive=True
        )

    def _slot_range_element(self, slot: SlotDefinition) -> Optional[Element]:
        ds = self.derived_schema
        sr = slot.range
        if sr in ds.classes:
            return ds.classes[sr]
        elif sr in ds.enums:
            return ds.enums[sr]
        elif sr in ds.types:
            return ds.types[sr]
        else:
            return None

    def _slot_collection_form(self, slot: SlotDefinition) -> CollectionForm:
        if not slot.multivalued:
            return CollectionForm.NonCollection
        if slot.inlined_as_list:
            return CollectionForm.List
        if not slot.inlined:
            return CollectionForm.List
        range_element = self._slot_range_element(slot)
        if not isinstance(range_element, ClassDefinition):
            raise AssertionError(f"Should be non-inlined: {slot.name}")
        if self._slot_as_simple_dict_value_slot(slot):
            return CollectionForm.SimpleDict
        if self._slot_inlined_as_compact_dict(slot):
            return CollectionForm.CompactDict
        return CollectionForm.ExpandedDict

    def _slot_inlined_as_compact_dict(self, slot: SlotDefinition) -> bool:
        if not slot.inlined:
            return False
        if slot.inlined_as_list:
            return False
        if self._slot_as_simple_dict_value_slot(slot):
            return False
        # TODO: make this configurable
        return True

    def _slot_as_simple_dict_value_slot(
        self, slot: SlotDefinition
    ) -> Optional[SlotDefinition]:
        if not slot.inlined or slot.inlined_as_list:
            return False
        range_element = self._slot_range_element(slot)
        if isinstance(range_element, ClassDefinition):
            non_pk_atts = [
                s
                for s in range_element.attributes.values()
                if not s.identifier and not s.key
            ]
            if len(non_pk_atts) == 1:
                return non_pk_atts[0]

    def _identifier_slot_name(
        self, cls: ClassDefinition
    ) -> Optional[SlotDefinitionName]:
        for slot in cls.attributes.values():
            if slot.identifier:
                return slot.name
            if slot.key:
                return slot.name

    def _identifier_slot(self, cls: ClassDefinition) -> Optional[SlotDefinition]:
        for slot in cls.attributes.values():
            if slot.identifier:
                return slot
            if slot.key:
                return slot

    def _class_name_from_value(self, slot_value: Any, slot_range: str) -> str:
        if slot_range == "curie":
            return slot_value.split(":")[0]
        elif slot_range == "uriorcurie":
            raise NotImplementedError
        else:
            return str(slot_value)

    def _matches_class_expression(
        self,
        input_object: dict,
        target: ClassDefinition,
        expr: AnonymousClassExpression,
    ) -> bool:
        if expr.is_a:
            if expr.is_a not in self.schemaview.class_ancestors(
                target.name, reflexive=True
            ):
                return False
            for slot_name, slot_expression in expr.slot_conditions.items():
                v = input_object.get(slot_name, None)
                if not self._matches_slot_expression(v, slot_expression, input_object):
                    return False
        return True

    def _matches_slot_expression(
        self,
        slot_value: Any,
        expr: Union[SlotDefinition, AnonymousSlotExpression],
        input_object: dict,
    ) -> bool:
        for x in expr.none_of:
            if self._matches_slot_expression(slot_value, x, input_object):
                return False
        if expr.exactly_one_of:
            vals = [
                x
                for x in expr.exactly_one_of
                if self._matches_slot_expression(slot_value, x, input_object)
            ]
            if len(vals) != 1:
                return False
        if expr.any_of:
            vals = [
                x
                for x in expr.any_of
                if self._matches_slot_expression(slot_value, x, input_object)
            ]
            if not vals:
                return False
        for x in expr.all_of:
            if not self._matches_slot_expression(slot_value, x, input_object):
                return False
        if expr.equals_expression:
            if eval_expr(expr.equals_expression, **input_object) != slot_value:
                return False
        if expr.equals_string:
            if str(slot_value) != expr.equals_string:
                return False
        if expr.equals_number:
            if slot_value != x.equals_number:
                return False
        return True


@click.command
@click.option("--schema", "-s", required=True,
              help="Path to LinkML schema")
@click.option("--target", "-C",
              help="name of target class or element to normalize/validate against")
@click.option("--report-file", "-R", type=click.File("w"), default=sys.stderr,
              show_default=True,
              help="path to file for reports")
@click.option("--output", "-o", type=click.File("w"), default=sys.stdout)
@click.option("--expand-all/--no-expand-all",
              help="If True, expand all Dicts to ExpandedDicts")
@click.argument("input")
def cli(schema: str, target: str, input: str, report_file: TextIO, output: TextIO, **kwargs) -> None:
    """
    Normalizes and validates a YAML document against a schema.

    Normalization is a mix of casting types (e.g. "5" to 5), as well as
    LinkML *collection forms*, e.g. ExpandedDict to CompactDict.

    Validations is performed using a derived schema, as per part 5 of the specification.

    Note that in future this will be folded into the main linkml-validate command.

    Currently this CLI lacks features such as the ability to customize which
    severity rules to fail on.

    :param schema:
    :param target:
    :param input:
    :param output:
    :return:
    """
    sv = SchemaView(schema)
    normalizer = ReferenceValidator(sv, **kwargs)
    with open(input) as f:
        input_object = yaml.safe_load(f)
    report = Report()
    output_object = normalizer.normalize(input_object, target=target, report=report)
    if report.normalized_results():
        report_file.write("# Repaired:\n")
        for r in report.normalized_results():
            report_file.write(yaml_dumper.dumps(r))
    if report.warnings():
        report_file.write("# Warnings:\n")
        for r in report.warnings():
            report_file.write(yaml_dumper.dumps(r))
    if report.errors():
        report_file.write("# Errors:\n")
        for r in report.errors():
            report_file.write(yaml_dumper.dumps(r))
        sys.exit(1)
    # TODO: https://stackoverflow.com/questions/45004464/yaml-dump-adding-unwanted-newlines-in-multiline-strings
    output_str = yaml.dump(output_object, sort_keys=False)
    output.write(output_str)


if __name__ == "__main__":
    cli()
