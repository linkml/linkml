import sys
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, ClassVar, Generic, Iterable, List, Optional, Type, TypeVar, Union, get_args

from linkml_runtime.linkml_model import Element
from linkml_runtime.linkml_model.meta import ArrayExpression, DimensionExpression
from pydantic import VERSION as PYDANTIC_VERSION

if int(PYDANTIC_VERSION[0]) < 2:
    pass
else:
    from pydantic import GetCoreSchemaHandler
    from pydantic_core import CoreSchema, core_schema

if sys.version_info.minor <= 8:
    from typing_extensions import Annotated
else:
    from typing import Annotated

from linkml.generators.pydanticgen.build import SlotResult
from linkml.generators.pydanticgen.template import ConditionalImport, Import, Imports, ObjectImport


class ArrayRepresentation(Enum):
    LIST = "list"
    NPARRAY = "nparray"  # numpy and nptyping must be installed to use this


_BOUNDED_ARRAY_FIELDS = ("exact_number_dimensions", "minimum_number_dimensions", "maximum_number_dimensions")

_T = TypeVar("_T")
_RecursiveListType = Iterable[Union[_T, Iterable["_RecursiveListType"]]]
if int(PYDANTIC_VERSION[0]) >= 2:

    class AnyShapeArrayType(Generic[_T]):
        @classmethod
        def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
            # double-nested parameterized types here
            # source_type: List[Union[T,List[...]]]
            item_type = Any if get_args(get_args(source_type)[0])[0] is _T else get_args(get_args(source_type)[0])[0]

            item_schema = handler.generate_schema(item_type)
            if item_schema.get("type", "any") != "any":
                item_schema["strict"] = True

            if item_type is Any:
                # Before python 3.11, `Any` type was a special object without a __name__
                item_name = "Any"
            else:
                item_name = item_type.__name__

            array_ref = f"any-shape-array-{item_name}"

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
        + Import(
            module="typing",
            objects=[
                ObjectImport(name="Generic"),
                ObjectImport(name="Iterable"),
                ObjectImport(name="TypeVar"),
                ObjectImport(name="Union"),
                ObjectImport(name="get_args"),
            ],
        )
        + ConditionalImport(
            condition="sys.version_info.minor > 8",
            module="typing",
            objects=[ObjectImport(name="Annotated")],
            alternative=Import(module="typing_extensions", objects=[ObjectImport(name="Annotated")]),
        )
        + Import(module="pydantic", objects=[ObjectImport(name="GetCoreSchemaHandler")])
        + Import(module="pydantic_core", objects=[ObjectImport(name="CoreSchema"), ObjectImport(name="core_schema")])
    )

    # annotated types are special and inspect.getsource() can't stringify them
    _AnyShapeArrayInjects = [
        '_T = TypeVar("_T")',
        '_RecursiveListType = Iterable[Union[_T, Iterable["_RecursiveListType"]]]',
        AnyShapeArrayType,
        "AnyShapeArray = Annotated[_RecursiveListType, AnyShapeArrayType]",
    ]

else:

    class AnyShapeArray(Generic[_T]):
        type_: Type[Any] = Any

        def __class_getitem__(cls, item):
            alias = type(f"AnyShape_{str(item.__name__)}", (AnyShapeArray,), {"type_": item})
            alias.type_ = item
            return alias

        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def __modify_schema__(cls, field_schema):
            try:
                item_type = field_schema["allOf"][0]["type"]
                type_schema = {"type": item_type}
                del field_schema["allOf"]
            except KeyError as e:
                if "allOf" in str(e):
                    item_type = "Any"
                    type_schema = {}
                else:
                    raise e

            array_id = f"#any-shape-array-{item_type}"
            field_schema["anyOf"] = [
                type_schema,
                {"type": "array", "items": {"$ref": array_id}},
            ]
            field_schema["$id"] = array_id

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
                    else:
                        try:
                            anytype = cls.type_.__name__ in ("AnyType", "Any")
                        except AttributeError:
                            # in python 3.8 and 3.9, `typing.Any` has no __name__
                            anytype = str(cls.type_).split(".")[-1] in ("AnyType", "Any")

                        if not anytype and not isinstance(item, cls.type_):
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

    See :ref:`array-forms` for more details on array range forms.

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

    Attributes:
        array (:class:`.ArrayExpression` ): Array to create an annotation for
        dtype (Union[str, :class:`.Element` ): dtype of the entire array as a string
        pydantic_ver (str): Pydantic version to generate array form for -
            currently only pydantic 1 and 2 are differentiated, and pydantic 1 will be deprecated soon.

    """

    REPR: ClassVar[ArrayRepresentation]

    def __init__(
        self, array: Optional[ArrayExpression], dtype: Union[str, Element], pydantic_ver: str = PYDANTIC_VERSION
    ):
        self.array = array
        self.dtype = dtype
        self.pydantic_ver = pydantic_ver

    def make(self) -> SlotResult:
        """Create the string form of the array representation"""
        if not self.array.dimensions and not self.has_bounded_dimensions:
            # any-shaped array
            return self.any_shape(self.array)
        elif not self.array.dimensions and self.has_bounded_dimensions:
            return self.bounded_dimensions(self.array)
        elif self.array.dimensions and not self.has_bounded_dimensions:
            return self.parameterized_dimensions(self.array)
        else:
            return self.complex_dimensions(self.array)

    @property
    def has_bounded_dimensions(self) -> bool:
        """Whether the :class:`.ArrayExpression` has some shape specification aside from ``dimensions``"""
        return any([getattr(self.array, arr_field, None) is not None for arr_field in _BOUNDED_ARRAY_FIELDS])

    @classmethod
    def get_generator(cls, repr: ArrayRepresentation) -> Type["ArrayRangeGenerator"]:
        """Get the generator class for a given array representation"""
        for subclass in cls.__subclasses__():
            if repr in (subclass.REPR, subclass.REPR.value):
                return subclass
        raise ValueError(f"Generator for array representation {repr} not found!")

    @abstractmethod
    def any_shape(self, array: Optional[ArrayRepresentation] = None) -> SlotResult:
        """Any shaped array!"""
        pass

    @abstractmethod
    def bounded_dimensions(self, array: ArrayExpression) -> SlotResult:
        """Array shape specified numerically, without axis parameterization"""
        pass

    @abstractmethod
    def parameterized_dimensions(self, array: ArrayExpression) -> SlotResult:
        """Array shape specified with ``dimensions`` without additional parameterized dimensions"""
        pass

    @abstractmethod
    def complex_dimensions(self, array: ArrayExpression) -> SlotResult:
        """Array shape with both ``parameterized`` and ``bounded`` dimensions"""
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
    def _parameterized_dimension(dimension: DimensionExpression, dtype: str) -> SlotResult:
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
        if int(PYDANTIC_VERSION[0]) >= 2:
            if dmin is not None:
                items.append(f"min_length={dmin}")
            if dmax is not None:
                items.append(f"max_length={dmax}")
        else:
            if dmin is not None:
                items.append(f"min_items={dmin}")
            if dmax is not None:
                items.append(f"max_items={dmax}")
        items.append(f"item_type={dtype}")
        items = ", ".join(items)
        annotation = f"conlist({items})"

        return SlotResult(annotation=annotation, imports=_ConListImports)

    def any_shape(self, array: Optional[ArrayExpression] = None, with_inner_union: bool = False) -> SlotResult:
        """
        An AnyShaped array (using :class:`.AnyShapeArray` )

        Args:
            array (:class:`.ArrayExpression`): The array expression (not used)
            with_inner_union (bool): If ``True`` , the innermost type is a ``Union`` of the ``AnyShapeArray`` class
                and ``dtype`` (default: ``False`` )

        """
        if self.dtype in ("Any", "AnyType"):
            annotation = "AnyShapeArray"
        else:
            annotation = f"AnyShapeArray[{self.dtype}]"

        if with_inner_union:
            annotation = f"Union[{annotation}, {self.dtype}]"
        return SlotResult(annotation=annotation, injected_classes=_AnyShapeArrayInjects, imports=_AnyShapeArrayImports)

    def bounded_dimensions(self, array: ArrayExpression) -> SlotResult:
        """
        A nested series of ``List[]`` annotations with :attr:`.dtype` at the center.

        When an array expression allows for a range of dimensions, each set of ``List`` s is joined by a ``Union`` .
        """
        if array.exact_number_dimensions or (
            array.minimum_number_dimensions
            and array.maximum_number_dimensions
            and array.minimum_number_dimensions == array.maximum_number_dimensions
        ):
            exact_dims = array.exact_number_dimensions or array.minimum_number_dimensions
            return SlotResult(annotation=self._list_of_lists(exact_dims, self.dtype))
        elif not array.maximum_number_dimensions and (
            array.minimum_number_dimensions is None or array.minimum_number_dimensions == 1
        ):
            return self.any_shape()
        elif array.maximum_number_dimensions:
            # e.g., if min = 2, max = 3, annotation = Union[List[List[dtype]], List[List[List[dtype]]]]
            min_dims = array.minimum_number_dimensions if array.minimum_number_dimensions is not None else 1
            annotations = [
                self._list_of_lists(i, self.dtype) for i in range(min_dims, array.maximum_number_dimensions + 1)
            ]
            # TODO: Format this nicely!
            return SlotResult(annotation="Union[" + ", ".join(annotations) + "]")
        else:
            # min specified with no max
            # e.g., if min = 3, annotation = List[List[AnyShapeArray[dtype]]]
            return SlotResult(
                annotation=self._list_of_lists(array.minimum_number_dimensions - 1, self.any_shape().annotation),
                injected_classes=_AnyShapeArrayInjects,
                imports=_AnyShapeArrayImports,
            )

    def parameterized_dimensions(self, array: ArrayExpression) -> SlotResult:
        """
        Constrained shapes using :func:`pydantic.conlist`

        TODO:
        - preservation of aliases
        - (what other metadata is allowable on labeled dimensions?)
        """
        # generate dimensions from inside out and then format
        # e.g., if dimensions = [{min_card: 3}, {min_card: 2}],
        # annotation = conlist(min_length=3, item_type=conlist(min_length=2, item_type=dtype))
        range = self.dtype
        for dimension in reversed(array.dimensions):
            range = self._parameterized_dimension(dimension, range).annotation

        return SlotResult(annotation=range, imports=_ConListImports)

    def complex_dimensions(self, array: ArrayExpression) -> SlotResult:
        """
        Mixture of parameterized dimensions with a max or min (or both) shape for anonymous dimensions.

        A mixture of ``List`` , :class:`.conlist` , and :class:`.AnyShapeArray` .
        """
        # first process any unlabeled dimensions which must be the innermost level of the annotation,
        # then wrap that with labeled dimensions
        if array.exact_number_dimensions or (
            array.minimum_number_dimensions
            and array.maximum_number_dimensions
            and array.minimum_number_dimensions == array.maximum_number_dimensions
        ):
            exact_dims = array.exact_number_dimensions or array.minimum_number_dimensions
            if exact_dims > len(array.dimensions):
                res = SlotResult(annotation=self._list_of_lists(exact_dims - len(array.dimensions), self.dtype))
            elif exact_dims == len(array.dimensions):
                # equivalent to labeled shape
                return self.parameterized_dimensions(array)
            else:
                raise ValueError(
                    "if exact_number_dimensions is provided, it must be greater than the parameterized dimensions"
                )

        elif array.maximum_number_dimensions is not None and not array.maximum_number_dimensions:
            # unlimited n dimensions, so innermost is AnyShape with dtype
            res = self.any_shape(with_inner_union=True)

            if array.minimum_number_dimensions and array.minimum_number_dimensions > len(array.dimensions):
                # some minimum anonymous dimensions but unlimited max dimensions
                # e.g., if min = 3, len(dim) = 2, then res.annotation = List[Union[AnyShapeArray[dtype], dtype]]
                # res.annotation will be wrapped with the 2 labeled dimensions later
                res.annotation = self._list_of_lists(
                    array.minimum_number_dimensions - len(array.dimensions), res.annotation
                )

        elif array.minimum_number_dimensions and array.maximum_number_dimensions is None:
            raise ValueError(
                (
                    "Cannot specify a minimum_number_dimensions while maximum is None while using labeled dimensions - "
                    "either use exact_number_dimensions > len(dimensions) for extra parameterized dimensions or set "
                    "maximum_number_dimensions explicitly to False for unbounded dimensions"
                )
            )
        elif array.maximum_number_dimensions:
            initial_min = array.minimum_number_dimensions if array.minimum_number_dimensions is not None else 0
            dmin = max(len(array.dimensions), initial_min) - len(array.dimensions)
            dmax = array.maximum_number_dimensions - len(array.dimensions)

            res = self.bounded_dimensions(
                ArrayExpression(minimum_number_dimensions=dmin, maximum_number_dimensions=dmax)
            )
        else:
            raise ValueError("Unsupported array specification! this is almost certainly a bug!")  # pragma: no cover

        # Wrap inner dimension with labeled dimension
        # e.g., if dimensions = [{min_card: 3}, {min_card: 2}]
        # and res.annotation = List[Union[AnyShapeArray[dtype], dtype]]
        # (min 3 dims, no max dims)
        # then the final annotation = conlist(
        #     min_length=3,
        #     item_type=conlist(
        #         min_length=2,
        #         item_type=List[Union[AnyShapeArray[dtype], dtype]]
        #     )
        # )
        for dim in reversed(array.dimensions):
            res = res.merge(self._parameterized_dimension(dim, dtype=res.annotation))

        return res


class NPTypingArray(ArrayRangeGenerator):
    """
    Represent array range with nptyping, and serialization/loading with an ArrayProxy
    """

    REPR = ArrayRepresentation.NPARRAY

    def __init__(self, **kwargs):
        super(self).__init__(**kwargs)
        raise NotImplementedError("NPTyping array ranges are not implemented yet :(")
