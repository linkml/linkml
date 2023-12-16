from __future__ import annotations
from datetime import datetime, date
from enum import Enum
import numpy as np
from typing import List, Dict, Optional, Any, Union, Literal
from pydantic import BaseModel as BaseModel, Field
from linkml_runtime.linkml_model import Decimal


from pydantic import ValidationError
from pydantic.fields import ModelField
from typing import Generic, TypeVar
from abc import ABC, abstractmethod
from numpy.lib import NumpyVersion
import sys

T = TypeVar("T", bound=np.generic)

if sys.version_info < (3, 9) or NumpyVersion(np.__version__) < "1.22.0":
    nd_array_type = np.ndarray
else:
    nd_array_type = np.ndarray[Any, T]


class _BaseDType:
    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update({"type": cls.__name__})

    @classmethod
    def __get_validators__(cls):  # TODO what is the return type?
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> "_BaseDType":
        if field.sub_fields:
            msg = f"{cls.__name__} has no subfields"
            raise ValidationError(msg)
        if not isinstance(val, cls):
            return cls(val)
        return val


class intc(np.intc, _BaseDType):
    pass


class np_int(np.int_, _BaseDType):  #
    pass


class _CommonNDArray(ABC):
    @classmethod
    @abstractmethod
    def validate(cls, val: Any, field: ModelField) -> nd_array_type:
        ...

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any], field: ModelField | None) -> None:
        if field and field.sub_fields:
            type_with_potential_subtype = f"np.ndarray[{field.sub_fields[0]}]"
        else:
            type_with_potential_subtype = "np.ndarray"
        field_schema.update({"type": type_with_potential_subtype})

    @classmethod
    def __get_validators__(cls):  # TODO what is the return type?
        yield cls.validate

    @staticmethod
    def _validate(val: Any, field: ModelField) -> nd_array_type:
        data = val
        if field.sub_fields is not None:
            dtype_field = field.sub_fields[0]
            return np.asarray(data, dtype=dtype_field.type_)
        return np.asarray(data)


class NDArray(Generic[T], nd_array_type, _CommonNDArray):
    @classmethod
    def validate(cls, val: Any, field: ModelField) -> nd_array_type:
        return cls._validate(val, field)


metamodel_version = "None"
version = "None"


class WeakRefShimBaseModel(BaseModel):
    __slots__ = "__weakref__"


class ConfiguredBaseModel(
    WeakRefShimBaseModel,
    validate_assignment=True,
    validate_all=True,
    underscore_attrs_are_private=True,
    extra="forbid",
    arbitrary_types_allowed=True,
    use_enum_values=True,
):
    pass


class TemperatureMatrix(ConfiguredBaseModel):
    x: LatitudeSeries = Field(None)
    y: LongitudeSeries = Field(None)
    time: DaySeries = Field(None)
    temperatures: np.ndarray = Field(None)


class LatitudeSeries(ConfiguredBaseModel):
    """
    A series whose values represent latitude
    """

    values: np.ndarray = Field(None)


class LongitudeSeries(ConfiguredBaseModel):
    """
    A series whose values represent longitude
    """

    values: np.ndarray = Field(None)


class DaySeries(ConfiguredBaseModel):
    """
    A series whose values represent the days since the start of the measurement period
    """

    values: NDArray[np_int]
    test: np.ndarray
    test2: int


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
TemperatureMatrix.update_forward_refs()
LatitudeSeries.update_forward_refs()
LongitudeSeries.update_forward_refs()
DaySeries.update_forward_refs()


lat = LatitudeSeries(values=np.array([1, 2, 3]))
lon = LongitudeSeries(values=np.array([4, 5, 6]))
day = DaySeries(values=np.array([7, 8, 9], dtype=np.int8), test=np.array([1, 2, 3]), test2=2.2)
temp = TemperatureMatrix(
    x=lat,
    y=lon,
    time=day,
    temperatures=np.ones((3, 3, 3)),
)
print(temp)
print(temp.time.values.dtype)
