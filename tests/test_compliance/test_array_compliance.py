"""Compliance tests for core constructs."""

import pytest

from tests.test_compliance.helper import (
    OWL,
    PYDANTIC,
    PYTHON_DATACLASSES,
    SHACL,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import (
    CLASS_C,
    CORE_FRAMEWORKS,
    SLOT_S1,
)


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
                        PYDANTIC: f"s1: Optional[{expected_range[ndim]}] = Field(None",
                    },
                },
            },
        },
    }
    schema = validated_schema(test_array, f"array-ndim{ndim}", framework, classes=classes, core_elements=["array"])
    if framework in [PYTHON_DATACLASSES, SQL_DDL_SQLITE, SHACL, OWL]:
        pytest.skip("Not implemented yet")
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework != PYDANTIC and not is_valid:
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        object,
        is_valid,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        description="pattern",
    )
