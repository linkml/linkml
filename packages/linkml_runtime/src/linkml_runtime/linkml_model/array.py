# Auto generated from array.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-05-05T18:49:10
# Schema: arrays
#
# id: https://w3id.org/linkml/lib/arrays
# description: LinkML templates for storing one-dimensional series, two-dimensional arrays, and arrays of higher dimensionality.
#   Status: Experimental
#   Note that this model is not intended to be imported directly. Instead, use `implements` to denote conformance.
# license: https://creativecommons.org/publicdomain/zero/1.0/

from dataclasses import dataclass
from typing import Any, ClassVar, Optional, Union

from jsonasobj2 import as_dict
from rdflib import URIRef

from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot

metamodel_version = "1.7.0"
version = None

# Namespaces
GITHUB = CurieNamespace("github", "https://github.com/")
GOM = CurieNamespace("gom", "https://w3id.org/gom#")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
DEFAULT_ = LINKML


# Types

# Class references


Any = Any


class DataStructure(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["DataStructure"]
    class_class_curie: ClassVar[str] = "linkml:DataStructure"
    class_name: ClassVar[str] = "DataStructure"
    class_model_uri: ClassVar[URIRef] = LINKML.DataStructure


@dataclass(repr=False)
class NDArray(DataStructure):
    """
    a data structure consisting of a collection of *elements*, each identified by at least one array index tuple.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["NDArray"]
    class_class_curie: ClassVar[str] = "linkml:NDArray"
    class_name: ClassVar[str] = "NDArray"
    class_model_uri: ClassVar[URIRef] = LINKML.NDArray

    elements: Union[Union[dict, Any], list[Union[dict, Any]]] = None
    dimensions: Optional[int] = None
    array_linearization_order: Optional[Union[str, "ArrayLinearizationOrderOptions"]] = "ROW_MAJOR_ARRAY_ORDER"

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.dimensions is not None and not isinstance(self.dimensions, int):
            self.dimensions = int(self.dimensions)

        if self.array_linearization_order is not None and not isinstance(
            self.array_linearization_order, ArrayLinearizationOrderOptions
        ):
            self.array_linearization_order = ArrayLinearizationOrderOptions(self.array_linearization_order)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OneDimensionalSeries(NDArray):
    """
    an NDArray whose dimensionality is constrained to 1
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["OneDimensionalSeries"]
    class_class_curie: ClassVar[str] = "linkml:OneDimensionalSeries"
    class_name: ClassVar[str] = "OneDimensionalSeries"
    class_model_uri: ClassVar[URIRef] = LINKML.OneDimensionalSeries

    elements: Union[Union[dict, Any], list[Union[dict, Any]]] = None
    dimensions: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.dimensions is not None and not isinstance(self.dimensions, int):
            self.dimensions = int(self.dimensions)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataArray(DataStructure):
    """
    a data structure containing an NDArray and a set of one-dimensional series that are used to label the elements of
    the array
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["DataArray"]
    class_class_curie: ClassVar[str] = "linkml:DataArray"
    class_name: ClassVar[str] = "DataArray"
    class_model_uri: ClassVar[URIRef] = LINKML.DataArray

    axis: Union[dict, OneDimensionalSeries] = None
    array: Union[dict, NDArray] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.axis):
            self.MissingRequiredField("axis")
        if not isinstance(self.axis, OneDimensionalSeries):
            self.axis = OneDimensionalSeries(**as_dict(self.axis))

        if self._is_empty(self.array):
            self.MissingRequiredField("array")
        if not isinstance(self.array, NDArray):
            self.array = NDArray(**as_dict(self.array))

        super().__post_init__(**kwargs)


class GroupingByArrayOrder(YAMLRoot):
    """
    A mixin that describes an array whose elements are mapped from a linear sequence to an array index via a specified
    mapping
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["GroupingByArrayOrder"]
    class_class_curie: ClassVar[str] = "linkml:GroupingByArrayOrder"
    class_name: ClassVar[str] = "GroupingByArrayOrder"
    class_model_uri: ClassVar[URIRef] = LINKML.GroupingByArrayOrder


@dataclass(repr=False)
class ColumnOrderedArray(GroupingByArrayOrder):
    """
    An array ordering that is column-order
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ColumnOrderedArray"]
    class_class_curie: ClassVar[str] = "linkml:ColumnOrderedArray"
    class_name: ClassVar[str] = "ColumnOrderedArray"
    class_model_uri: ClassVar[URIRef] = LINKML.ColumnOrderedArray

    array_linearization_order: Optional[Union[str, "ArrayLinearizationOrderOptions"]] = "COLUMN_MAJOR_ARRAY_ORDER"

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.array_linearization_order is not None and not isinstance(
            self.array_linearization_order, ArrayLinearizationOrderOptions
        ):
            self.array_linearization_order = ArrayLinearizationOrderOptions(self.array_linearization_order)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RowOrderedArray(GroupingByArrayOrder):
    """
    An array ordering that is row-order or generalizations thereof
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["RowOrderedArray"]
    class_class_curie: ClassVar[str] = "linkml:RowOrderedArray"
    class_name: ClassVar[str] = "RowOrderedArray"
    class_model_uri: ClassVar[URIRef] = LINKML.RowOrderedArray

    array_linearization_order: Optional[Union[str, "ArrayLinearizationOrderOptions"]] = "ROW_MAJOR_ARRAY_ORDER"

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.array_linearization_order is not None and not isinstance(
            self.array_linearization_order, ArrayLinearizationOrderOptions
        ):
            self.array_linearization_order = ArrayLinearizationOrderOptions(self.array_linearization_order)

        super().__post_init__(**kwargs)


# Enumerations
class ArrayLinearizationOrderOptions(EnumDefinitionImpl):
    """
    Determines how a linear contiguous representation of the elements of an array map to array indices
    """

    COLUMN_MAJOR_ARRAY_ORDER = PermissibleValue(
        text="COLUMN_MAJOR_ARRAY_ORDER",
        description="""An array layout option in which the elements in each column is stored in consecutive positions, or any generalization thereof to dimensionality greater than 2""",
        meaning=GOM["columnMajorArray"],
    )
    ROW_MAJOR_ARRAY_ORDER = PermissibleValue(
        text="ROW_MAJOR_ARRAY_ORDER",
        description="""An array layout option in which the elements in each row is stored in consecutive positions, or any generalization thereof to dimensionality greater than 2""",
        meaning=GOM["rowMajorArray"],
    )

    _defn = EnumDefinition(
        name="ArrayLinearizationOrderOptions",
        description="Determines how a linear contiguous representation of the elements of an array map to array indices",
    )


# Slots
class slots:
    pass


slots.dimensions = Slot(
    uri=LINKML.dimensions,
    name="dimensions",
    curie=LINKML.curie("dimensions"),
    model_uri=LINKML.dimensions,
    domain=None,
    range=Optional[int],
)

slots.axis = Slot(
    uri=LINKML.axis,
    name="axis",
    curie=LINKML.curie("axis"),
    model_uri=LINKML.axis,
    domain=None,
    range=Union[dict, OneDimensionalSeries],
)

slots.axis_index = Slot(
    uri=LINKML.axis_index,
    name="axis_index",
    curie=LINKML.curie("axis_index"),
    model_uri=LINKML.axis_index,
    domain=None,
    range=Optional[int],
)

slots.array = Slot(
    uri=LINKML.array,
    name="array",
    curie=LINKML.curie("array"),
    model_uri=LINKML.array,
    domain=None,
    range=Union[dict, NDArray],
)

slots.elements = Slot(
    uri=LINKML.elements,
    name="elements",
    curie=LINKML.curie("elements"),
    model_uri=LINKML.elements,
    domain=None,
    range=Union[Union[dict, Any], list[Union[dict, Any]]],
)

slots.series_label = Slot(
    uri=LINKML.series_label,
    name="series_label",
    curie=LINKML.curie("series_label"),
    model_uri=LINKML.series_label,
    domain=None,
    range=URIRef,
)

slots.length = Slot(
    uri=LINKML.length,
    name="length",
    curie=LINKML.curie("length"),
    model_uri=LINKML.length,
    domain=None,
    range=Optional[int],
)

slots.array_linearization_order = Slot(
    uri=LINKML.array_linearization_order,
    name="array_linearization_order",
    curie=LINKML.curie("array_linearization_order"),
    model_uri=LINKML.array_linearization_order,
    domain=None,
    range=Optional[Union[str, "ArrayLinearizationOrderOptions"]],
)

slots.specified_input = Slot(
    uri=LINKML.specified_input,
    name="specified_input",
    curie=LINKML.curie("specified_input"),
    model_uri=LINKML.specified_input,
    domain=None,
    range=Optional[Union[Union[dict, DataStructure], list[Union[dict, DataStructure]]]],
)

slots.specified_output = Slot(
    uri=LINKML.specified_output,
    name="specified_output",
    curie=LINKML.curie("specified_output"),
    model_uri=LINKML.specified_output,
    domain=None,
    range=Optional[Union[Union[dict, DataStructure], list[Union[dict, DataStructure]]]],
)

slots.operation_parameters = Slot(
    uri=LINKML.operation_parameters,
    name="operation_parameters",
    curie=LINKML.curie("operation_parameters"),
    model_uri=LINKML.operation_parameters,
    domain=None,
    range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]],
)

slots.NDArray_elements = Slot(
    uri=LINKML.elements,
    name="NDArray_elements",
    curie=LINKML.curie("elements"),
    model_uri=LINKML.NDArray_elements,
    domain=NDArray,
    range=Union[Union[dict, Any], list[Union[dict, Any]]],
)

slots.OneDimensionalSeries_dimensions = Slot(
    uri=LINKML.dimensions,
    name="OneDimensionalSeries_dimensions",
    curie=LINKML.curie("dimensions"),
    model_uri=LINKML.OneDimensionalSeries_dimensions,
    domain=OneDimensionalSeries,
    range=Optional[int],
)

slots.ColumnOrderedArray_array_linearization_order = Slot(
    uri=LINKML.array_linearization_order,
    name="ColumnOrderedArray_array_linearization_order",
    curie=LINKML.curie("array_linearization_order"),
    model_uri=LINKML.ColumnOrderedArray_array_linearization_order,
    domain=None,
    range=Optional[Union[str, "ArrayLinearizationOrderOptions"]],
)

slots.RowOrderedArray_array_linearization_order = Slot(
    uri=LINKML.array_linearization_order,
    name="RowOrderedArray_array_linearization_order",
    curie=LINKML.curie("array_linearization_order"),
    model_uri=LINKML.RowOrderedArray_array_linearization_order,
    domain=None,
    range=Optional[Union[str, "ArrayLinearizationOrderOptions"]],
)
