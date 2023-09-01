# Auto generated from array.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-09-01T13:21:12
# Schema: arrays
#
# id: https://w3id.org/linkml/lib/arrays
# description: LinkML templates for storing one-dimensional series, two-dimensional arrays, and arrays of higher dimensionality.
#   Status: Experimental
#   Note that this model is not intended to be imported directly. Instead, use `implements` to denote conformance.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
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
from .types import Integer, String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
GITHUB = CurieNamespace('github', 'https://github.com/')
GOM = CurieNamespace('gom', 'https://w3id.org/gom#')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = LINKML


# Types

# Class references
class OneDimensionalSeriesSeriesLabel(extended_str):
    pass


Any = Any

class DataStructure(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.DataStructure
    class_class_curie: ClassVar[str] = "linkml:DataStructure"
    class_name: ClassVar[str] = "DataStructure"
    class_model_uri: ClassVar[URIRef] = LINKML.DataStructure


@dataclass
class Array(DataStructure):
    """
    a data structure consisting of a collection of *elements*, each identified by at least one array index tuple.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.Array
    class_class_curie: ClassVar[str] = "linkml:Array"
    class_name: ClassVar[str] = "Array"
    class_model_uri: ClassVar[URIRef] = LINKML.Array

    elements: Union[Union[dict, Any], List[Union[dict, Any]]] = None
    dimensionality: Optional[int] = None
    array_linearization_order: Optional[Union[str, "ArrayLinearizationOrderOptions"]] = "ROW_MAJOR_ARRAY_ORDER"

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.dimensionality is not None and not isinstance(self.dimensionality, int):
            self.dimensionality = int(self.dimensionality)

        if self.array_linearization_order is not None and not isinstance(self.array_linearization_order, ArrayLinearizationOrderOptions):
            self.array_linearization_order = ArrayLinearizationOrderOptions(self.array_linearization_order)

        super().__post_init__(**kwargs)


@dataclass
class OneDimensionalSeries(Array):
    """
    An array that has one dimension
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.OneDimensionalSeries
    class_class_curie: ClassVar[str] = "linkml:OneDimensionalSeries"
    class_name: ClassVar[str] = "OneDimensionalSeries"
    class_model_uri: ClassVar[URIRef] = LINKML.OneDimensionalSeries

    series_label: Union[str, OneDimensionalSeriesSeriesLabel] = None
    elements: Union[Union[dict, Any], List[Union[dict, Any]]] = None
    length: Optional[int] = None
    dimensionality: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.series_label):
            self.MissingRequiredField("series_label")
        if not isinstance(self.series_label, OneDimensionalSeriesSeriesLabel):
            self.series_label = OneDimensionalSeriesSeriesLabel(self.series_label)

        if self.length is not None and not isinstance(self.length, int):
            self.length = int(self.length)

        if self.dimensionality is not None and not isinstance(self.dimensionality, int):
            self.dimensionality = int(self.dimensionality)

        super().__post_init__(**kwargs)


@dataclass
class TwoDimensionalArray(Array):
    """
    An array that has two dimensions
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.TwoDimensionalArray
    class_class_curie: ClassVar[str] = "linkml:TwoDimensionalArray"
    class_name: ClassVar[str] = "TwoDimensionalArray"
    class_model_uri: ClassVar[URIRef] = LINKML.TwoDimensionalArray

    axis0: Union[dict, OneDimensionalSeries] = None
    axis1: Union[dict, OneDimensionalSeries] = None
    elements: Union[Union[dict, Any], List[Union[dict, Any]]] = None
    dimensionality: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.axis0):
            self.MissingRequiredField("axis0")
        if not isinstance(self.axis0, OneDimensionalSeries):
            self.axis0 = OneDimensionalSeries(**as_dict(self.axis0))

        if self._is_empty(self.axis1):
            self.MissingRequiredField("axis1")
        if not isinstance(self.axis1, OneDimensionalSeries):
            self.axis1 = OneDimensionalSeries(**as_dict(self.axis1))

        if self.dimensionality is not None and not isinstance(self.dimensionality, int):
            self.dimensionality = int(self.dimensionality)

        super().__post_init__(**kwargs)


@dataclass
class ThreeDimensionalArray(Array):
    """
    An array that has two dimensions
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.ThreeDimensionalArray
    class_class_curie: ClassVar[str] = "linkml:ThreeDimensionalArray"
    class_name: ClassVar[str] = "ThreeDimensionalArray"
    class_model_uri: ClassVar[URIRef] = LINKML.ThreeDimensionalArray

    elements: Union[Union[dict, Any], List[Union[dict, Any]]] = None
    axis0: Union[dict, OneDimensionalSeries] = None
    axis1: Union[dict, OneDimensionalSeries] = None
    axis2: Union[dict, OneDimensionalSeries] = None
    dimensionality: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.axis0):
            self.MissingRequiredField("axis0")
        if not isinstance(self.axis0, OneDimensionalSeries):
            self.axis0 = OneDimensionalSeries(**as_dict(self.axis0))

        if self._is_empty(self.axis1):
            self.MissingRequiredField("axis1")
        if not isinstance(self.axis1, OneDimensionalSeries):
            self.axis1 = OneDimensionalSeries(**as_dict(self.axis1))

        if self._is_empty(self.axis2):
            self.MissingRequiredField("axis2")
        if not isinstance(self.axis2, OneDimensionalSeries):
            self.axis2 = OneDimensionalSeries(**as_dict(self.axis2))

        if self.dimensionality is not None and not isinstance(self.dimensionality, int):
            self.dimensionality = int(self.dimensionality)

        super().__post_init__(**kwargs)


class OrderedArray(YAMLRoot):
    """
    A mixin that describes an array whose elements are mapped from a linear sequence to an array index via a specified
    mapping
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.OrderedArray
    class_class_curie: ClassVar[str] = "linkml:OrderedArray"
    class_name: ClassVar[str] = "OrderedArray"
    class_model_uri: ClassVar[URIRef] = LINKML.OrderedArray


@dataclass
class ColumnOrderedArray(YAMLRoot):
    """
    An array ordering that is column-order
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.ColumnOrderedArray
    class_class_curie: ClassVar[str] = "linkml:ColumnOrderedArray"
    class_name: ClassVar[str] = "ColumnOrderedArray"
    class_model_uri: ClassVar[URIRef] = LINKML.ColumnOrderedArray

    array_linearization_order: Optional[Union[str, "ArrayLinearizationOrderOptions"]] = "ROW_MAJOR_ARRAY_ORDER"

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.array_linearization_order is not None and not isinstance(self.array_linearization_order, ArrayLinearizationOrderOptions):
            self.array_linearization_order = ArrayLinearizationOrderOptions(self.array_linearization_order)

        super().__post_init__(**kwargs)


@dataclass
class RowOrderedArray(YAMLRoot):
    """
    An array ordering that is row-order or generalizations thereof
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.RowOrderedArray
    class_class_curie: ClassVar[str] = "linkml:RowOrderedArray"
    class_name: ClassVar[str] = "RowOrderedArray"
    class_model_uri: ClassVar[URIRef] = LINKML.RowOrderedArray

    array_linearization_order: Optional[Union[str, "ArrayLinearizationOrderOptions"]] = "ROW_MAJOR_ARRAY_ORDER"

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.array_linearization_order is not None and not isinstance(self.array_linearization_order, ArrayLinearizationOrderOptions):
            self.array_linearization_order = ArrayLinearizationOrderOptions(self.array_linearization_order)

        super().__post_init__(**kwargs)


@dataclass
class MultiDimensionalArray(Array):
    """
    An array that has more than two dimensions
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.MultiDimensionalArray
    class_class_curie: ClassVar[str] = "linkml:MultiDimensionalArray"
    class_name: ClassVar[str] = "MultiDimensionalArray"
    class_model_uri: ClassVar[URIRef] = LINKML.MultiDimensionalArray

    elements: Union[Union[dict, Any], List[Union[dict, Any]]] = None

class ObjectAsTuple(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.ObjectAsTuple
    class_class_curie: ClassVar[str] = "linkml:ObjectAsTuple"
    class_name: ClassVar[str] = "ObjectAsTuple"
    class_model_uri: ClassVar[URIRef] = LINKML.ObjectAsTuple


class ArrayIndex(ObjectAsTuple):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.ArrayIndex
    class_class_curie: ClassVar[str] = "linkml:ArrayIndex"
    class_name: ClassVar[str] = "ArrayIndex"
    class_model_uri: ClassVar[URIRef] = LINKML.ArrayIndex


@dataclass
class Operation(YAMLRoot):
    """
    Represents the transformation of one or more inputs to one or more outputs determined by zero to many operation
    parameters
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.Operation
    class_class_curie: ClassVar[str] = "linkml:Operation"
    class_name: ClassVar[str] = "Operation"
    class_model_uri: ClassVar[URIRef] = LINKML.Operation

    specified_input: Optional[Union[Union[dict, DataStructure], List[Union[dict, DataStructure]]]] = empty_list()
    specified_output: Optional[Union[Union[dict, DataStructure], List[Union[dict, DataStructure]]]] = empty_list()
    operation_parameters: Optional[Union[Union[dict, Any], List[Union[dict, Any]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.specified_input, list):
            self.specified_input = [self.specified_input] if self.specified_input is not None else []
        self.specified_input = [v if isinstance(v, DataStructure) else DataStructure(**as_dict(v)) for v in self.specified_input]

        if not isinstance(self.specified_output, list):
            self.specified_output = [self.specified_output] if self.specified_output is not None else []
        self.specified_output = [v if isinstance(v, DataStructure) else DataStructure(**as_dict(v)) for v in self.specified_output]

        super().__post_init__(**kwargs)


@dataclass
class ArrayIndexOperation(YAMLRoot):
    """
    An operation that takes as input an Array and is parameterized by an array index tuple and yields an array element
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.ArrayIndexOperation
    class_class_curie: ClassVar[str] = "linkml:ArrayIndexOperation"
    class_name: ClassVar[str] = "ArrayIndexOperation"
    class_model_uri: ClassVar[URIRef] = LINKML.ArrayIndexOperation

    specified_input: Optional[Union[Union[dict, Array], List[Union[dict, Array]]]] = empty_list()
    specified_output: Optional[Union[Union[dict, Any], List[Union[dict, Any]]]] = empty_list()
    operation_parameters: Optional[Union[Union[dict, ArrayIndex], List[Union[dict, ArrayIndex]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="specified_input", slot_type=Array, key_name="elements", keyed=False)

        if not isinstance(self.operation_parameters, list):
            self.operation_parameters = [self.operation_parameters] if self.operation_parameters is not None else []
        self.operation_parameters = [v if isinstance(v, ArrayIndex) else ArrayIndex(**as_dict(v)) for v in self.operation_parameters]

        super().__post_init__(**kwargs)


# Enumerations
class ArrayLinearizationOrderOptions(EnumDefinitionImpl):
    """
    Determines how a linear contiguous representation of the elements of an array map to array indices
    """
    COLUMN_MAJOR_ARRAY_ORDER = PermissibleValue(
        text="COLUMN_MAJOR_ARRAY_ORDER",
        description="""An array layout option in which the elements in each column is stored in consecutive positions, or any generalization thereof to dimensionality greater than 2""",
        meaning=GOM.columnMajorArray)
    ROW_MAJOR_ARRAY_ORDER = PermissibleValue(
        text="ROW_MAJOR_ARRAY_ORDER",
        description="""An array layout option in which the elements in each row is stored in consecutive positions, or any generalization thereof to dimensionality greater than 2""",
        meaning=GOM.rowMajorArray)

    _defn = EnumDefinition(
        name="ArrayLinearizationOrderOptions",
        description="Determines how a linear contiguous representation of the elements of an array map to array indices",
    )

# Slots
class slots:
    pass

slots.dimensionality = Slot(uri=LINKML.dimensionality, name="dimensionality", curie=LINKML.curie('dimensionality'),
                   model_uri=LINKML.dimensionality, domain=None, range=Optional[int])

slots.axis = Slot(uri=LINKML.axis, name="axis", curie=LINKML.curie('axis'),
                   model_uri=LINKML.axis, domain=None, range=Optional[Union[str, OneDimensionalSeriesSeriesLabel]])

slots.axis0 = Slot(uri=LINKML.axis0, name="axis0", curie=LINKML.curie('axis0'),
                   model_uri=LINKML.axis0, domain=None, range=Union[dict, OneDimensionalSeries])

slots.axis1 = Slot(uri=LINKML.axis1, name="axis1", curie=LINKML.curie('axis1'),
                   model_uri=LINKML.axis1, domain=None, range=Union[dict, OneDimensionalSeries])

slots.axis2 = Slot(uri=LINKML.axis2, name="axis2", curie=LINKML.curie('axis2'),
                   model_uri=LINKML.axis2, domain=None, range=Union[dict, OneDimensionalSeries])

slots.elements = Slot(uri=LINKML.elements, name="elements", curie=LINKML.curie('elements'),
                   model_uri=LINKML.elements, domain=None, range=Union[Union[dict, Any], List[Union[dict, Any]]])

slots.series_label = Slot(uri=LINKML.series_label, name="series_label", curie=LINKML.curie('series_label'),
                   model_uri=LINKML.series_label, domain=None, range=URIRef)

slots.length = Slot(uri=LINKML.length, name="length", curie=LINKML.curie('length'),
                   model_uri=LINKML.length, domain=None, range=Optional[int])

slots.array_linearization_order = Slot(uri=LINKML.array_linearization_order, name="array_linearization_order", curie=LINKML.curie('array_linearization_order'),
                   model_uri=LINKML.array_linearization_order, domain=None, range=Optional[Union[str, "ArrayLinearizationOrderOptions"]])

slots.specified_input = Slot(uri=LINKML.specified_input, name="specified_input", curie=LINKML.curie('specified_input'),
                   model_uri=LINKML.specified_input, domain=None, range=Optional[Union[Union[dict, DataStructure], List[Union[dict, DataStructure]]]])

slots.specified_output = Slot(uri=LINKML.specified_output, name="specified_output", curie=LINKML.curie('specified_output'),
                   model_uri=LINKML.specified_output, domain=None, range=Optional[Union[Union[dict, DataStructure], List[Union[dict, DataStructure]]]])

slots.operation_parameters = Slot(uri=LINKML.operation_parameters, name="operation_parameters", curie=LINKML.curie('operation_parameters'),
                   model_uri=LINKML.operation_parameters, domain=None, range=Optional[Union[Union[dict, Any], List[Union[dict, Any]]]])

slots.Array_elements = Slot(uri=LINKML.elements, name="Array_elements", curie=LINKML.curie('elements'),
                   model_uri=LINKML.Array_elements, domain=Array, range=Union[Union[dict, Any], List[Union[dict, Any]]])

slots.OneDimensionalSeries_dimensionality = Slot(uri=LINKML.dimensionality, name="OneDimensionalSeries_dimensionality", curie=LINKML.curie('dimensionality'),
                   model_uri=LINKML.OneDimensionalSeries_dimensionality, domain=OneDimensionalSeries, range=Optional[int])

slots.TwoDimensionalArray_dimensionality = Slot(uri=LINKML.dimensionality, name="TwoDimensionalArray_dimensionality", curie=LINKML.curie('dimensionality'),
                   model_uri=LINKML.TwoDimensionalArray_dimensionality, domain=TwoDimensionalArray, range=Optional[int])

slots.TwoDimensionalArray_elements = Slot(uri=LINKML.elements, name="TwoDimensionalArray_elements", curie=LINKML.curie('elements'),
                   model_uri=LINKML.TwoDimensionalArray_elements, domain=TwoDimensionalArray, range=Union[Union[dict, Any], List[Union[dict, Any]]])

slots.ThreeDimensionalArray_dimensionality = Slot(uri=LINKML.dimensionality, name="ThreeDimensionalArray_dimensionality", curie=LINKML.curie('dimensionality'),
                   model_uri=LINKML.ThreeDimensionalArray_dimensionality, domain=ThreeDimensionalArray, range=Optional[int])

slots.ColumnOrderedArray_array_linearization_order = Slot(uri=LINKML.array_linearization_order, name="ColumnOrderedArray_array_linearization_order", curie=LINKML.curie('array_linearization_order'),
                   model_uri=LINKML.ColumnOrderedArray_array_linearization_order, domain=None, range=Optional[Union[str, "ArrayLinearizationOrderOptions"]])

slots.RowOrderedArray_array_linearization_order = Slot(uri=LINKML.array_linearization_order, name="RowOrderedArray_array_linearization_order", curie=LINKML.curie('array_linearization_order'),
                   model_uri=LINKML.RowOrderedArray_array_linearization_order, domain=None, range=Optional[Union[str, "ArrayLinearizationOrderOptions"]])

slots.ArrayIndexOperation_specified_input = Slot(uri=LINKML.specified_input, name="ArrayIndexOperation_specified_input", curie=LINKML.curie('specified_input'),
                   model_uri=LINKML.ArrayIndexOperation_specified_input, domain=ArrayIndexOperation, range=Optional[Union[Union[dict, Array], List[Union[dict, Array]]]])

slots.ArrayIndexOperation_specified_output = Slot(uri=LINKML.specified_output, name="ArrayIndexOperation_specified_output", curie=LINKML.curie('specified_output'),
                   model_uri=LINKML.ArrayIndexOperation_specified_output, domain=ArrayIndexOperation, range=Optional[Union[Union[dict, Any], List[Union[dict, Any]]]])

slots.ArrayIndexOperation_operation_parameters = Slot(uri=LINKML.operation_parameters, name="ArrayIndexOperation_operation_parameters", curie=LINKML.curie('operation_parameters'),
                   model_uri=LINKML.ArrayIndexOperation_operation_parameters, domain=ArrayIndexOperation, range=Optional[Union[Union[dict, ArrayIndex], List[Union[dict, ArrayIndex]]]])
