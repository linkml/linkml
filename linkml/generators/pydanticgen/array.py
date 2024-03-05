from abc import ABC, abstractmethod
from enum import Enum
from typing import (
    Annotated,
    Any,
    ClassVar,
    Generic,
    Iterable,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
)

from linkml_runtime.linkml_model import Element
from linkml_runtime.linkml_model.meta import ArrayExpression, DimensionExpression
from pydantic import VERSION as PYDANTIC_VERSION

if int(PYDANTIC_VERSION[0]) < 2:
    pass
else:
    from pydantic import GetCoreSchemaHandler
    from pydantic_core import CoreSchema, core_schema

from linkml.generators.pydanticgen.build import SlotResult
from linkml.generators.pydanticgen.template import Import, Imports, ObjectImport


class ArrayRepresentation(Enum):
    LIST = "list"
    NPARRAY = "nparray"  # numpy and nptyping must be installed to use this


_ANONYMOUS_ARRAY_FIELDS = ("exact_number_dimensions", "minimum_number_dimensions", "maximum_number_dimensions")

_T = TypeVar("_T")
_RecursiveListType = Iterable[_T | Iterable["_RecursiveListType"]]
if int(PYDANTIC_VERSION[0]) >= 2:

    class AnyShapeArrayType(Generic[_T]):
        @classmethod
        def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
            # double-nested parameterized types here
            # source_type: List[Union[T,List[...]]]
            item_type = Any if get_args(get_args(source_type)[0])[0] is _T else get_args(get_args(source_type)[0])[0]

            item_schema = handler.generate_schema(item_type)
            array_ref = f"any-shape-array-{item_type.__name__}"

            schema = core_schema.definitions_schema(
                core_schema.list_schema(core_schema.definition_reference_schema(array_ref)),
                [
                    core_schema.union_schema(
                        [
                            core_schema.list_schema(core_schema.definition_reference_schema(array_ref)),
                            item_schema,
                        ],
                        ref=array_ref,
                    )
                ],
            )

            return schema

    AnyShapeArray = Annotated[_RecursiveListType, AnyShapeArrayType]

    _AnyShapeArrayImports = (
        Imports()
        + Import(module="typing", objects=[ObjectImport(name="Generic"), ObjectImport(name="TypeVar")])
        + Import(module="pydantic", objects=[ObjectImport(name="GetCoreSchemaHandler")])
        + Import(module="pydantic_core", objects=[ObjectImport(name="CoreSchema"), ObjectImport(name="core_schema")])
    )
    _AnyShapeArrayInjects = [
        '_T = TypeVar("_T")',
        '_RecursiveListType = Iterable[_T | Iterable["_RecursiveListType"]]',
        AnyShapeArrayType,
        AnyShapeArray,
    ]

else:

    class AnyShapeArray(Generic[_T]):
        type_: Any

        def __class_getitem__(cls, item):
            alias = type(f"AnyShape_{str(item.__name__)}", (AnyShapeArray,), {"type_": item})
            return alias

        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def __modify_schema__(cls, field_schema):
            item_type = field_schema["allOf"][0]["type"]
            array_id = f"#any-shape-array-{item_type}"
            field_schema["anyOf"] = [
                {"type": item_type},
                {"type": "array", "items": {"$ref": array_id}},
            ]
            field_schema["$id"] = array_id
            del field_schema["allOf"]

        @classmethod
        def validate(cls, v: Union[List[_T], list]):
            if str(type(v)) == "<class 'numpy.ndarray'>":
                v = v.tolist()

            if not isinstance(v, list):
                raise TypeError(f"Must be a list of lists! got {v}")

            def _validate(_v: Union[List[_T], list]):
                for item in _v:
                    if isinstance(item, list):
                        _validate(item)
                    elif cls.type_.__name__ != "AnyType":
                        if not isinstance(item, cls.type_):
                            raise TypeError(
                                (
                                    f"List items must be list of lists, or the type used in "
                                    f"the subscript ({cls.type_}. Got item {item} and outer value {v}"
                                )
                            )
                return _v

            return _validate(v)

    _AnyShapeArrayImports = Imports() + Import(
        module="typing",
        objects=[ObjectImport(name="Generic"), ObjectImport(name="TypeVar"), ObjectImport(name="_GenericAlias")],
    )
    _AnyShapeArrayInjects = [
        '_T = TypeVar("_T")',
        AnyShapeArray,
    ]

_ConListImports = Imports() + Import(module="pydantic", objects=[ObjectImport(name="conlist")])


class ArrayRangeGenerator(ABC):
    """
    Metaclass for generating a given format of array annotation.

    These classes do only enough validation of the array specification to decide
    which kind of representation to generate. Proper value validation should
    happen elsewhere (ie. in the metamodel and generated :class:`.ArrayExpression` class.)

    Each of the array representation generation methods should be able to handle
    the supported pydantic versions (currently still 1 and 2).

    Notes:

        When checking for array specification, recall that there is a semantic difference between
        ``None`` and ``False`` , particularly for :attr:`.ArrayExpression.max_number_dimensions` -
        check for absence of specification with ``is None`` rather than checking for truthiness/falsiness
        (unless that's what you intend to do ofc ;)
    """

    REPR: ClassVar[ArrayRepresentation]

    def __init__(self, array: ArrayExpression | None, dtype: str | Element, pydantic_ver: str = PYDANTIC_VERSION):
        self.array = array
        self.dtype = dtype
        self.pydantic_ver = pydantic_ver

    def make(self) -> SlotResult:
        """Create the string form of the array representation"""
        if not self.array.dimensions and not self.has_anonymous_dimensions:
            # any-shaped array
            return self.any_shape(self.array)
        elif not self.array.dimensions and self.has_anonymous_dimensions:
            return self.anonymous_shape(self.array)
        elif self.array.dimensions and not self.has_anonymous_dimensions:
            return self.labeled_shape(self.array)
        else:
            return self.mixed_shape(self.array)

    @property
    def has_anonymous_dimensions(self) -> bool:
        """Whether the :class:`.ArrayExpression` has some shape specification aside from ``dimensions``"""
        return any([getattr(self.array, arr_field, None) is not None for arr_field in _ANONYMOUS_ARRAY_FIELDS])

    @classmethod
    def get_generator(cls, repr: ArrayRepresentation) -> Type["ArrayRangeGenerator"]:
        """Get the generator class for a given array representation"""
        for subclass in cls.__subclasses__():
            if subclass.REPR == repr:
                return subclass
        raise ValueError(f"Generator for array representation {repr} not found!")

    @abstractmethod
    def any_shape(self, array: Optional[ArrayRepresentation] = None) -> SlotResult:
        """Any shaped array!"""
        pass

    @abstractmethod
    def anonymous_shape(self, array: ArrayExpression) -> SlotResult:
        """Array shape specified numerically, without axis parameterization"""
        pass

    @abstractmethod
    def labeled_shape(self, array: ArrayExpression) -> SlotResult:
        """Array shape specified with ``dimensions`` without additional anonymous axes"""
        pass

    @abstractmethod
    def mixed_shape(self, array: ArrayExpression) -> SlotResult:
        """Array shape with both ``dimensions`` and a ``max_number_dimensions`` for anonymous axes"""
        pass


class ListOfListsArray(ArrayRangeGenerator):
    """
    Represent arrays as lists of lists!

    TODO: Move all validation of values (eg. anywhere we raise a ValueError) to the ArrayExpression
    dataclass and out of the generator class
    """

    REPR = ArrayRepresentation.LIST

    @staticmethod
    def _list_of_lists(dimensions: int, dtype: str) -> str:
        return ("List[" * dimensions) + dtype + ("]" * dimensions)

    @staticmethod
    def _labeled_dimension(dimension: DimensionExpression, dtype: str) -> SlotResult:
        # TODO: Preserve label representation in some readable way! doing the MVP now of using conlist
        if dimension.exact_cardinality and (dimension.minimum_cardinality or dimension.maximum_cardinality):
            raise ValueError("Can only specify EITHER exact_cardinality OR minimum/maximum cardinality")
        elif dimension.exact_cardinality:
            dmin = dimension.exact_cardinality
            dmax = dimension.exact_cardinality
        elif dimension.minimum_cardinality or dimension.maximum_cardinality:
            dmin = dimension.minimum_cardinality
            dmax = dimension.maximum_cardinality
        else:
            # TODO: handle labels for labeled but unshaped arrays
            return SlotResult(annotation="List[" + dtype + "]")

        items = []
        if dmin is not None:
            items.append(f"min_items={dmin}")
        if dmax is not None:
            items.append(f"max_items={dmax}")
        items.append(f"item_type={dtype}")
        items = ", ".join(items)
        annotation = f"conlist({items})"

        return SlotResult(annotation=annotation, imports=_ConListImports)

    def any_shape(self, array: Optional[ArrayExpression] = None) -> SlotResult:
        if self.dtype == "Any":
            annotation = "AnyShapeArray"
        else:
            annotation = f"AnyShapeArray[{self.dtype}]"
        return SlotResult(annotation=annotation, injected_classes=_AnyShapeArrayInjects, imports=_AnyShapeArrayImports)

    def anonymous_shape(self, array: ArrayExpression) -> SlotResult:
        if array.exact_number_dimensions:
            return SlotResult(annotation=self._list_of_lists(array.exact_number_dimensions, self.dtype))
        elif not array.maximum_number_dimensions and (
            array.minimum_number_dimensions is None or array.minimum_number_dimensions == 1
        ):
            return self.any_shape()
        elif array.maximum_number_dimensions:
            min_dims = array.minimum_number_dimensions if array.minimum_number_dimensions else 1
            annotations = [
                self._list_of_lists(i, self.dtype) for i in range(min_dims, array.maximum_number_dimensions + 1)
            ]
            # TODO: Format this nicely!
            return SlotResult(annotation="Union[" + ", ".join(annotations) + "]")
        else:
            return SlotResult(
                annotation=self._list_of_lists(array.minimum_number_dimensions, self.any_shape().annotation),
                injected_classes=_AnyShapeArrayInjects,
                imports=_AnyShapeArrayImports,
            )

    def labeled_shape(self, array: ArrayExpression) -> SlotResult:
        """
        Constrained shapes using :func:`pydantic.conlist`

        TODO:
        - preservation of aliases
        - (what other metadata is allowable on labeled dimensions?)
        """
        # generate dimensions from inside out and then format
        range = self.dtype
        for dimension in reversed(array.dimensions):
            range = self._labeled_dimension(dimension, range).annotation

        return SlotResult(annotation=range, imports=_ConListImports)

    def mixed_shape(self, array: ArrayExpression) -> SlotResult:
        """
        Mixture of labeled dimensions with a max or min (or both) shape for anonymous dimensions
        """
        if array.exact_number_dimensions is not None:
            if array.exact_number_dimensions > len(array.dimensions):
                res = SlotResult(
                    annotation=self._list_of_lists(array.exact_number_dimensions - len(array.dimensions), self.dtype)
                )
            elif array.exact_number_dimensions == len(array.dimensions):
                # equivalent to labeled shape
                return self.labeled_shape(array)
            else:
                raise ValueError(
                    "if exact_number_dimensions is provided, it must be greater than the parameterized dimensions"
                )

        elif array.maximum_number_dimensions is not None and not array.maximum_number_dimensions:
            # unlimited n dimensions, so innermost is AnyShape with dtype
            res = self.any_shape()

            if array.minimum_number_dimensions and array.minimum_number_dimensions > len(array.dimensions):
                # some minimum anonymous dimensions but unlimited max dimensions
                res += self._list_of_lists(array.minimum_number_dimensions - len(array.dimensions), res.annotation)

        elif array.minimum_number_dimensions and array.maximum_number_dimensions is None:
            raise ValueError(
                (
                    "Cannot specify a minimum_number_dimensions while maximum is None while using labeled dimensions - "
                    "either use exact_number_dimensions > len(dimensions) for extra anonymous dimensions or set "
                    "maximum_number_dimensions explicitly to False for unbounded dimensions"
                )
            )
        elif array.maximum_number_dimensions:
            initial_min = array.minimum_number_dimensions if array.minimum_number_dimensions is not None else 0
            dmin = max(len(array.dimensions), initial_min) - len(array.dimensions)
            dmax = array.maximum_number_dimensions - len(array.dimensions)

            res = self.anonymous_shape(ArrayExpression(minimum_number_dimensions=dmin, maximum_number_dimensions=dmax))
        else:
            raise ValueError("Unsupported array specification! this is almost certainly a bug!")

        # Wrap inner dimension with labeled dimension
        for dim in array.dimensions:
            res += self._labeled_dimension(dim, dtype=res.annotation)

        return res


class NPTypingArray(ArrayRangeGenerator):
    """
    Represent array range with nptyping, and serialization/loading with an ArrayProxy
    """

    REPR = ArrayRepresentation.NPARRAY

    def __init__(self, **kwargs):
        super(self).__init__(**kwargs)
        raise NotImplementedError("NPTyping array ranges are not implemented yet :(")
