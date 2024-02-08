"""Compliance tests for core constructs."""

import unicodedata

import pytest
from _decimal import Decimal
from linkml_runtime.utils.formatutils import underscore
from pydantic.version import VERSION as PYDANTIC_VERSION

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    OWL,
    PYDANTIC,
    PYDANTIC_ROOT_CLASS,
    PYTHON_DATACLASSES,
    PYTHON_DATACLASSES_ROOT_CLASS,
    SHACL,
    SHEX,
    SQL_DDL_POSTGRES,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    metamodel_schemaview,
    validated_schema,
)
from tests.test_compliance.test_compliance import (
    CLASS_ANY,
    CLASS_C,
    CORE_FRAMEWORKS,
    EXAMPLE_STRING_VALUE_1,
    EXAMPLE_STRING_VALUE_2,
    EXAMPLE_STRING_VALUE_3,
    SLOT_ID,
    SLOT_S1,
    SLOT_S2,
    SLOT_S3,
)

IS_PYDANTIC_V1 = PYDANTIC_VERSION[0] == "1"


@pytest.mark.parametrize(
    "description,ndim,object,is_valid",
    [
        ("object may be empty", 3, {}, True),
        (
            "1D array with float against 1D array float schema",
            1,
            {
                SLOT_S1: [2.0],
            },
            True,
        ),
        (
            "2D array with float against 1D array float schema",
            1,
            {
                SLOT_S1: [[2.0]],
            },
            False,
        ),
        (
            "1D array with string against 1D array float schema",
            1,
            {
                SLOT_S1: ["foo"],
            },
            False,
        ),
        (
            "3D array with float against 3D array float schema",
            3,
            {
                SLOT_S1: [[[2.0]]],
            },
            True,
        ),
        (
            "2D array with float against 3D array float schema",
            3,
            {
                SLOT_S1: [[2.0]],
            },
            False,
        ),
        (
            "3D array with string against 3D array float schema",
            3,
            {
                SLOT_S1: [[["foo"]]],
            },
            False,
        ),
        (
            "3D array with float against 3D array float schema",
            3,
            {
                SLOT_S1: [[[2.0, 3.0], [4.0, 5.0]], [[6.0, 7.0], [8.0, 9.0]]],
            },
            True,
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_array(framework, description, ndim, object, is_valid):
    """
    Tests basic behavior of arrays.

    Known issues:

    - None. This is core behavior all frameworks MAY support.

    :param framework: all may support arrays
    :param description: description of the test data
    :param ndim: number of dimensions in the array
    :param object: object to check
    :param is_valid: whether the object is valid
    :return:
    """
    if framework != PYDANTIC:
        pytest.skip("Not implemented yet")

    expected_range = {
        1: "List[float]",
        3: "List[List[List[float]]]",
    }
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": "float",
                    "array": {
                        "exact_number_dimensions": ndim,
                    },
                    "_mappings": {
                        PYDANTIC: f"s1: Optional[{expected_range[ndim]}] = Field(None)",
                    }
                },
            },
        },
    }
    schema = validated_schema(test_array, f"array-ndim{ndim}", framework, classes=classes, core_elements=["array"])
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        object,
        is_valid,
        target_class=CLASS_C,
        description="pattern",
    )

