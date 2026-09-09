from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, ClassVar

from linkml.generators.common.build import RangeResult
from linkml.utils.exceptions import SchemaValidationError
from linkml_runtime.linkml_model import Element
from linkml_runtime.linkml_model.meta import ArrayExpression, DimensionExpression

_BOUNDED_ARRAY_FIELDS = ("exact_number_dimensions", "minimum_number_dimensions", "maximum_number_dimensions")


class ArrayRepresentation(Enum):
    LIST = "list"
    NUMPYDANTIC = "numpydantic"  # numpydantic must be installed to use this
    JSON_SCHEMA = "json_schema"


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
            :class:`.SchemaValidationError` if invalid
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
            :class:`.SchemaValidationError` if invalid
        """
        cls.dimension_exact_cardinality(dimension)
        cls.dimension_ordinal(dimension)

    @staticmethod
    def array_exact_dimensions(array: ArrayExpression):
        """Arrays can have exact_number_dimensions OR min/max_number_dimensions, but not both"""
        if array.exact_number_dimensions is not None and (
            array.minimum_number_dimensions is not None or array.maximum_number_dimensions is not None
        ):
            raise SchemaValidationError(
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
                raise SchemaValidationError(
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
                raise SchemaValidationError(
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
            raise SchemaValidationError(
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
            raise SchemaValidationError(
                f"Can only specify EITHER exact_cardinality OR minimum/maximum cardinality, got: {dimension}"
            )

    @staticmethod
    def dimension_ordinal(dimension: DimensionExpression):
        """minimum_cardinality must be less than maximum_cardinality when both are set"""
        if dimension.minimum_cardinality is not None and dimension.maximum_cardinality is not None:
            if dimension.minimum_cardinality > dimension.maximum_cardinality:
                raise SchemaValidationError(
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

    def __init__(self, array: ArrayExpression | None, dtype: str | Element | dict):
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
            :class:`.SchemaValidationError` if the schema is invalid
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
    def _any_shape(self, array: ArrayRepresentation | None = None) -> Any:
        """Any shaped array!"""
        pass

    @abstractmethod
    def _bounded_dimensions(self, array: ArrayExpression) -> Any:
        """Array shape specified numerically, without axis parameterization"""
        pass

    @abstractmethod
    def _parameterized_dimensions(self, array: ArrayExpression) -> Any:
        """Array shape specified with ``dimensions`` without additional parameterized dimensions"""
        pass

    @abstractmethod
    def _complex_dimensions(self, array: ArrayExpression) -> Any:
        """Array shape with both ``parameterized`` and ``bounded`` dimensions"""
        pass
