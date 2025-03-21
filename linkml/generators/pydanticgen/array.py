import sys
from abc import ABC, abstractmethod
from enum import Enum
from typing import (
    ClassVar,
    Optional,
    TypeVar,
    Union,
)

from linkml_runtime.linkml_model import Element
from linkml_runtime.linkml_model.meta import ArrayExpression, DimensionExpression
from pydantic import VERSION as PYDANTIC_VERSION

from linkml.utils.deprecation import deprecation_warning

if int(PYDANTIC_VERSION[0]) < 2:
    # Support for having pydantic 1 installed in the same environment will be dropped in 1.9.0
    deprecation_warning("pydantic-v1")

if sys.version_info.minor < 12:
    from typing_extensions import TypeAliasType
else:
    from typing import TypeAliasType


from linkml.generators.pydanticgen.build import RangeResult
from linkml.generators.pydanticgen.template import ConditionalImport, Import, Imports, ObjectImport
from linkml.utils.exceptions import ValidationError


class ArrayRepresentation(Enum):
    LIST = "list"
    NUMPYDANTIC = "numpydantic"  # numpydantic must be installed to use this


_BOUNDED_ARRAY_FIELDS = ("exact_number_dimensions", "minimum_number_dimensions", "maximum_number_dimensions")

_T = TypeVar("_T")
AnyShapeArray = TypeAliasType("AnyShapeArray", list[Union[_T, "AnyShapeArray[_T]"]], type_params=(_T,))

_AnyShapeArrayImports = (
    Imports()
    + Import(
        module="typing",
        objects=[
            ObjectImport(name="TypeVar"),
            ObjectImport(name="Union"),
        ],
    )
    + ConditionalImport(
        condition="sys.version_info.minor >= 12",
        module="typing",
        objects=[ObjectImport(name="TypeAliasType")],
        alternative=Import(module="typing_extensions", objects=[ObjectImport(name="TypeAliasType")]),
    )
)

# annotated types are special and inspect.getsource() can't stringify them
_AnyShapeArrayInjects = [
    '_T = TypeVar("_T")',
    """AnyShapeArray = TypeAliasType(
    "AnyShapeArray", list[Union[_T, "AnyShapeArray[_T]"]], type_params=(_T,)
)""",
]

_ConListImports = Imports() + Import(module="pydantic", objects=[ObjectImport(name="conlist")])


class ArrayValidator:
    """
    Validate the specification of a LinkML Array

    .. todo::

        It looks like :mod:`linkml.validator` is for validating instances against schema, rather
        than validating the schema itself, so am not subclassing/writing as a plugin.
        Unsure if there is a more general means of validating schema, but for now this is
        an independent class
    """

    @classmethod
    def validate(cls, array: ArrayExpression):
        """
        Validate an array expression.

        Raises:
            :class:`.ValidationError` if invalid
        """
        cls.array_exact_dimensions(array)
        cls.array_consistent_n_dimensions(array)
        cls.array_explicitly_unbounded(array)
        cls.array_dimensions_ordinal(array)

        if array.dimensions:
            for dimension in array.dimensions:
                cls.validate_dimension(dimension)

    @classmethod
    def validate_dimension(cls, dimension: DimensionExpression):
        """
        Validate a single array dimension

        Raises:
            :class:`.ValidationError` if invalid
        """
        cls.dimension_exact_cardinality(dimension)
        cls.dimension_ordinal(dimension)

    @staticmethod
    def array_exact_dimensions(array: ArrayExpression):
        """Arrays can have exact_number_dimensions OR min/max_number_dimensions, but not both"""
        if array.exact_number_dimensions is not None and (
            array.minimum_number_dimensions is not None or array.maximum_number_dimensions is not None
        ):
            raise ValidationError(
                f"Can only specify EITHER exact_number_dimensions OR minimum/maximum dimensions, got: {array}"
            )

    @staticmethod
    def array_consistent_n_dimensions(array: ArrayExpression):
        """
        Complex arrays with both exact/min/max_number_dimensions and parameterized dimensions
        need to have the exact/min/max_number_dimensions greater than the number of parameterized dimensions!
        """
        if not array.dimensions:
            return

        for field_name in _BOUNDED_ARRAY_FIELDS:
            field = getattr(array, field_name, None)
            if field and field < len(array.dimensions):
                raise ValidationError(
                    "if exact/minimum/maximum_number_dimensions is provided, "
                    "it must be greater than the parameterized dimensions. "
                    f"got\n- {field_name}: {field}\n- dimensions: {array.dimensions}"
                )

    @staticmethod
    def array_dimensions_ordinal(array: ArrayExpression):
        """
        minimum_number_dimensions needs to be less than maximum_number_dimensions when both are set
        """
        if array.minimum_number_dimensions is not None and array.maximum_number_dimensions:
            if array.minimum_number_dimensions > array.maximum_number_dimensions:
                raise ValidationError(
                    "minimum_number_dimensions must be lesser than maximum_number_dimensions when both are set. "
                    f"got minimum: {array.minimum_number_dimensions}, maximum: {array.maximum_number_dimensions}"
                )

    @staticmethod
    def array_explicitly_unbounded(array: ArrayExpression):
        """
        Complex arrays with a minimum_number_dimensions and parameterized dimensions
        need to either use exact_number_dimensions to specify extra anonymous dimensions
        or set maximum_number_dimensions to ``False`` to specify unbounded extra anonymous
        dimensions to avoid ambiguity.
        """
        if array.minimum_number_dimensions is not None and array.maximum_number_dimensions is None and array.dimensions:
            raise ValidationError(
                "Cannot specify a minimum_number_dimensions while maximum is None while using labeled dimensions - "
                "either use exact_number_dimensions > len(dimensions) for extra parameterized dimensions or set "
                "maximum_number_dimensions explicitly to False for unbounded dimensions"
            )

    @staticmethod
    def dimension_exact_cardinality(dimension: DimensionExpression):
        """Dimensions can only have exact_cardinality OR min/max_cardinality, but not both"""
        if dimension.exact_cardinality is not None and (
            dimension.minimum_cardinality is not None or dimension.maximum_cardinality is not None
        ):
            raise ValidationError(
                f"Can only specify EITHER exact_cardinality OR minimum/maximum cardinality, got: {dimension}"
            )

    @staticmethod
    def dimension_ordinal(dimension: DimensionExpression):
        """minimum_cardinality must be less than maximum_cardinality when both are set"""
        if dimension.minimum_cardinality is not None and dimension.maximum_cardinality is not None:
            if dimension.minimum_cardinality > dimension.maximum_cardinality:
                raise ValidationError(
                    "minimum_cardinality must be lesser than maximum_cardinality when both are set. "
                    f"got minimum: {dimension.minimum_cardinality}, maximum: {dimension.maximum_cardinality}"
                )


class ArrayRangeGenerator(ABC):
    """
    Metaclass for generating a given format of array range.

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
        array (:class:`.ArrayExpression` ): Array to create a range for
        dtype (Union[str, :class:`.Element` ): dtype of the entire array as a string

    """

    REPR: ClassVar[ArrayRepresentation]

    def __init__(self, array: Optional[ArrayExpression], dtype: Union[str, Element]):
        self.array = array
        self.dtype = dtype

    def make(self) -> RangeResult:
        """
        Create the string form of the array representation, validating first
        """
        self.validate()

        if not self.array.dimensions and not self.has_bounded_dimensions:
            return self._any_shape(self.array)
        elif not self.array.dimensions and self.has_bounded_dimensions:
            return self._bounded_dimensions(self.array)
        elif self.array.dimensions and not self.has_bounded_dimensions:
            return self._parameterized_dimensions(self.array)
        else:
            return self._complex_dimensions(self.array)

    def validate(self):
        """
        Ensure that the given ArrayExpression is valid using :class:`.ArrayValidator`

        .. todo::

            Integrate with more general schema validation that happens when a schema is loaded,
            rather than when an array is generated

        Raises:
            :class:`.ValidationError` if the schema is invalid
        """
        ArrayValidator.validate(self.array)

    @property
    def has_bounded_dimensions(self) -> bool:
        """Whether the :class:`.ArrayExpression` has some shape specification aside from ``dimensions``"""
        return any([getattr(self.array, arr_field, None) is not None for arr_field in _BOUNDED_ARRAY_FIELDS])

    @classmethod
    def get_generator(cls, repr: ArrayRepresentation) -> type["ArrayRangeGenerator"]:
        """Get the generator class for a given array representation"""
        for subclass in cls.__subclasses__():
            if repr in (subclass.REPR, subclass.REPR.value):
                return subclass
        raise ValueError(f"Generator for array representation {repr} not found!")

    @abstractmethod
    def _any_shape(self, array: Optional[ArrayRepresentation] = None) -> RangeResult:
        """Any shaped array!"""
        pass

    @abstractmethod
    def _bounded_dimensions(self, array: ArrayExpression) -> RangeResult:
        """Array shape specified numerically, without axis parameterization"""
        pass

    @abstractmethod
    def _parameterized_dimensions(self, array: ArrayExpression) -> RangeResult:
        """Array shape specified with ``dimensions`` without additional parameterized dimensions"""
        pass

    @abstractmethod
    def _complex_dimensions(self, array: ArrayExpression) -> RangeResult:
        """Array shape with both ``parameterized`` and ``bounded`` dimensions"""
        pass


class ListOfListsArray(ArrayRangeGenerator):
    """
    Represent arrays as lists of lists!
    """

    REPR = ArrayRepresentation.LIST

    @staticmethod
    def _list_of_lists(dimensions: int, dtype: str) -> str:
        return ("list[" * dimensions) + dtype + ("]" * dimensions)

    @staticmethod
    def _parameterized_dimension(dimension: DimensionExpression, dtype: str) -> RangeResult:
        # TODO: Preserve label representation in some readable way! doing the MVP now of using conlist
        if dimension.exact_cardinality:
            dmin = dimension.exact_cardinality
            dmax = dimension.exact_cardinality
        elif dimension.minimum_cardinality or dimension.maximum_cardinality:
            dmin = dimension.minimum_cardinality
            dmax = dimension.maximum_cardinality
        else:
            # TODO: handle labels for labeled but unshaped arrays
            return RangeResult(range="list[" + dtype + "]")

        items = []
        if dmin is not None:
            items.append(f"min_length={dmin}")
        if dmax is not None:
            items.append(f"max_length={dmax}")

        items.append(f"item_type={dtype}")
        items = ", ".join(items)
        range = f"conlist({items})"

        return RangeResult(range=range, imports=_ConListImports)

    def _any_shape(self, array: Optional[ArrayExpression] = None, with_inner_union: bool = False) -> RangeResult:
        """
        An AnyShaped array (using :class:`.AnyShapeArray` )

        Args:
            array (:class:`.ArrayExpression`): The array expression (not used)
            with_inner_union (bool): If ``True`` , the innermost type is a ``Union`` of the ``AnyShapeArray`` class
                and ``dtype`` (default: ``False`` )

        """
        if self.dtype in ("Any", "AnyType"):
            range = "AnyShapeArray"
        else:
            range = f"AnyShapeArray[{self.dtype}]"

        if with_inner_union:
            range = f"Union[{range}, {self.dtype}]"
        return RangeResult(range=range, injected_classes=_AnyShapeArrayInjects, imports=_AnyShapeArrayImports)

    def _bounded_dimensions(self, array: ArrayExpression) -> RangeResult:
        """
        A nested series of ``list[]`` ranges with :attr:`.dtype` at the center.

        When an array expression allows for a range of dimensions, each set of ``List`` s is joined by a ``Union`` .
        """
        if array.exact_number_dimensions or (
            array.minimum_number_dimensions
            and array.maximum_number_dimensions
            and array.minimum_number_dimensions == array.maximum_number_dimensions
        ):
            exact_dims = array.exact_number_dimensions or array.minimum_number_dimensions
            return RangeResult(range=self._list_of_lists(exact_dims, self.dtype))
        elif not array.maximum_number_dimensions and (
            array.minimum_number_dimensions is None or array.minimum_number_dimensions == 1
        ):
            return self._any_shape()
        elif array.maximum_number_dimensions:
            # e.g., if min = 2, max = 3, range = Union[list[list[dtype]], list[list[list[dtype]]]]
            min_dims = array.minimum_number_dimensions if array.minimum_number_dimensions is not None else 1
            ranges = [self._list_of_lists(i, self.dtype) for i in range(min_dims, array.maximum_number_dimensions + 1)]
            return RangeResult(range="Union[" + ", ".join(ranges) + "]")
        else:
            # min specified with no max
            # e.g., if min = 3, range = list[list[AnyShapeArray[dtype]]]
            return RangeResult(
                range=self._list_of_lists(array.minimum_number_dimensions - 1, self._any_shape().range),
                injected_classes=_AnyShapeArrayInjects,
                imports=_AnyShapeArrayImports,
            )

    def _parameterized_dimensions(self, array: ArrayExpression) -> RangeResult:
        """
        Constrained shapes using :func:`pydantic.conlist`

        TODO:
        - preservation of aliases
        - (what other metadata is allowable on labeled dimensions?)
        """
        # generate dimensions from inside out and then format
        # e.g., if dimensions = [{min_card: 3}, {min_card: 2}],
        # range = conlist(min_length=3, item_type=conlist(min_length=2, item_type=dtype))
        range = self.dtype
        for dimension in reversed(array.dimensions):
            range = self._parameterized_dimension(dimension, range).range

        return RangeResult(range=range, imports=_ConListImports)

    def _complex_dimensions(self, array: ArrayExpression) -> RangeResult:
        """
        Mixture of parameterized dimensions with a max or min (or both) shape for anonymous dimensions.

        A mixture of ``List`` , :class:`.conlist` , and :class:`.AnyShapeArray` .
        """
        res = None
        # first process any unlabeled dimensions which must be the innermost level of the range,
        # then wrap that with labeled dimensions
        if array.exact_number_dimensions or (
            array.minimum_number_dimensions
            and array.maximum_number_dimensions
            and array.minimum_number_dimensions == array.maximum_number_dimensions
        ):
            exact_dims = array.exact_number_dimensions or array.minimum_number_dimensions
            if exact_dims > len(array.dimensions):
                res = RangeResult(range=self._list_of_lists(exact_dims - len(array.dimensions), self.dtype))
            elif exact_dims == len(array.dimensions):
                # equivalent to labeled shape
                return self._parameterized_dimensions(array)
            # else is invalid, see: ArrayValidator.array_consistent_n_dimensions

        elif array.maximum_number_dimensions is not None and not array.maximum_number_dimensions:
            # unlimited n dimensions, so innermost is AnyShape with dtype
            res = self._any_shape(with_inner_union=True)

            if array.minimum_number_dimensions:
                # some minimum anonymous dimensions but unlimited max dimensions
                # e.g., if min = 3, len(dim) = 2, then res.range = list[Union[AnyShapeArray[dtype], dtype]]
                # res.range will be wrapped with the 2 labeled dimensions later
                res.range = self._list_of_lists(array.minimum_number_dimensions - len(array.dimensions), res.range)

        elif array.maximum_number_dimensions:
            initial_min = array.minimum_number_dimensions if array.minimum_number_dimensions is not None else 0
            dmin = max(len(array.dimensions), initial_min) - len(array.dimensions)
            dmax = array.maximum_number_dimensions - len(array.dimensions)

            res = self._bounded_dimensions(
                ArrayExpression(minimum_number_dimensions=dmin, maximum_number_dimensions=dmax)
            )

        if res is None:
            raise ValueError("Unsupported array specification! this is almost certainly a bug!")  # pragma: no cover

        # Wrap inner dimension with labeled dimension
        # e.g., if dimensions = [{min_card: 3}, {min_card: 2}]
        # and res.range = list[Union[AnyShapeArray[dtype], dtype]]
        # (min 3 dims, no max dims)
        # then the final range = conlist(
        #     min_length=3,
        #     item_type=conlist(
        #         min_length=2,
        #         item_type=list[Union[AnyShapeArray[dtype], dtype]]
        #     )
        # )
        for dim in reversed(array.dimensions):
            res = res.merge(self._parameterized_dimension(dim, dtype=res.range))

        return res


class NumpydanticArray(ArrayRangeGenerator):
    """
    Represent array range with :class:`numpydantic.NDArray` annotations,
    allowing an abstract array specification to be used with many different array
    libraries.
    """

    REPR = ArrayRepresentation.NUMPYDANTIC
    MIN_NUMPYDANTIC_VERSION = "1.6.1"
    """
    Minimum numpydantic version needed to be installed in the environment using
    the generated models
    """
    IMPORTS = Imports() + Import(
        module="numpydantic", objects=[ObjectImport(name="NDArray"), ObjectImport(name="Shape")]
    )
    INJECTS = [f'MIN_NUMPYDANTIC_VERSION = "{MIN_NUMPYDANTIC_VERSION}"']

    def make(self) -> RangeResult:
        result = super().make()
        result.imports = self.IMPORTS.model_copy()
        result.injected_classes = self.INJECTS.copy()
        return result

    @staticmethod
    def ndarray_annotation(shape: Optional[list[Union[int, str]]] = None, dtype: Optional[str] = None) -> str:
        """
        Make a stringified :class:`numpydantic.NDArray` annotation for a given shape
        and dtype.

        If either ``shape`` or ``dtype`` is ``None`` , use ``Any``
        """
        if shape is None:
            shape = "Any"
        else:
            shape_expression = ", ".join([str(i) for i in shape])
            shape = f'Shape["{shape_expression}"]'

        if dtype is None or dtype in ("Any", "AnyType"):
            dtype = "Any"

        if shape == "Any" and dtype == "Any":
            return "NDArray"
        else:
            return f"NDArray[{shape}, {dtype}]"

    @staticmethod
    def _dimension_shape(dimension: DimensionExpression) -> str:
        if dimension.exact_cardinality:
            shape = str(dimension.exact_cardinality)
        elif dimension.minimum_cardinality and not dimension.maximum_cardinality:
            shape = f"{dimension.minimum_cardinality}-*"
        elif dimension.maximum_cardinality and not dimension.minimum_cardinality:
            shape = f"*-{dimension.maximum_cardinality}"
        elif dimension.minimum_cardinality and dimension.maximum_cardinality:
            shape = f"{dimension.minimum_cardinality}-{dimension.maximum_cardinality}"
        else:
            shape = "*"

        return shape

    @classmethod
    def _parameterized_dimension(cls, dimension: DimensionExpression) -> str:
        shape = cls._dimension_shape(dimension)
        if dimension.alias is not None:
            return f"{shape} {dimension.alias}"
        else:
            return shape

    def _any_shape(self, array: Optional[ArrayRepresentation] = None) -> RangeResult:
        """
        Any shaped array, either an unparameterized :class:`numpydantic.NDArray`
        if dtype is :class:`typing.Any` , or like ``NDArray[Any, {self.dtype}]``
        otherwise.
        """
        if self.dtype in ("Any", "AnyType"):
            range = "NDArray"
        else:
            range = f"NDArray[Any, {self.dtype}]"

        return RangeResult(range=range)

    def _bounded_dimensions(self, array: ArrayExpression) -> RangeResult:
        """
        Number of dimensions specified without shape
        """
        if array.exact_number_dimensions or (
            array.minimum_number_dimensions
            and array.maximum_number_dimensions
            and array.minimum_number_dimensions == array.maximum_number_dimensions
        ):
            exact_dims = array.exact_number_dimensions or array.minimum_number_dimensions

            return RangeResult(range=self.ndarray_annotation(["*"] * exact_dims, self.dtype))
        elif not array.maximum_number_dimensions and (
            array.minimum_number_dimensions is None or array.minimum_number_dimensions == 1
        ):
            return self._any_shape()
        elif array.maximum_number_dimensions:
            # e.g., if min = 2, max = 3, range = Union[NDArray[Shape["*, *"], dtype], NDArray[Shape["*, *, *"], dtype]]
            min_dims = array.minimum_number_dimensions if array.minimum_number_dimensions is not None else 1
            ranges = [
                self.ndarray_annotation(["*"] * i, self.dtype)
                for i in range(min_dims, array.maximum_number_dimensions + 1)
            ]
            return RangeResult(range="Union[" + ", ".join(ranges) + "]")
        else:
            # min specified with no max
            # e.g., if min = 3, range = NDArray[Shape[*, *, *, ...], dtype]
            shape_inner = ["*"] * array.minimum_number_dimensions
            shape_inner.append("...")
            return RangeResult(range=self.ndarray_annotation(shape_inner, self.dtype))

    def _parameterized_dimensions(self, array: ArrayExpression) -> RangeResult:
        """
        Arrays with constrained shapes or labels
        """
        dims = [self._parameterized_dimension(d) for d in array.dimensions]
        range = self.ndarray_annotation(dims, self.dtype)
        return RangeResult(range=range)

    def _complex_dimensions(self, array: ArrayExpression) -> RangeResult:
        """
        Mixture of parameterized dimensions with a max or min (or both) shape for anonymous dimensions.
        """
        dims = [self._parameterized_dimension(d) for d in array.dimensions]
        res = None

        if array.exact_number_dimensions or (
            array.minimum_number_dimensions
            and array.maximum_number_dimensions
            and array.minimum_number_dimensions == array.maximum_number_dimensions
        ):
            exact_dims = array.exact_number_dimensions or array.minimum_number_dimensions
            if exact_dims > len(array.dimensions):
                dims.extend(["*"] * (exact_dims - len(dims)))
                res = self.ndarray_annotation(dims, self.dtype)
            elif exact_dims == len(array.dimensions):
                # equivalent to labeled shape
                return self._parameterized_dimensions(array)
            # else is invalid, see: ArrayValidator.array_consistent_n_dimensions(array)

        elif array.maximum_number_dimensions is not None and not array.maximum_number_dimensions:
            # unlimited n dimensions

            if array.minimum_number_dimensions:
                # some minimum anonymous dimensions but unlimited max dimensions
                dims.extend(["*"] * (array.minimum_number_dimensions - len(dims)))

            dims.append("...")
            res = self.ndarray_annotation(dims, self.dtype)

        elif array.maximum_number_dimensions:
            # some res of anonymous dimensions

            if array.minimum_number_dimensions:
                min_dim = array.minimum_number_dimensions
            else:
                min_dim = len(dims)

            dim_union = []
            for i in range(min_dim, array.maximum_number_dimensions + 1):
                this_dims = dims.copy()
                this_dims.extend(["*"] * (i - len(dims)))
                dim_union.append(self.ndarray_annotation(this_dims, self.dtype))
            dim_union = ", ".join(dim_union)
            res = f"Union[{dim_union}]"

        if res is None:
            raise ValueError(f"Unhandled range case! {array}")

        return RangeResult(range=res)
