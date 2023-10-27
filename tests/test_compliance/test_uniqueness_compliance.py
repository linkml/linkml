import pytest

from tests.test_compliance.helper import (
    PYTHON_DATACLASSES,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import (
    CLASS_C,
    CLASS_CONTAINER,
    CORE_FRAMEWORKS,
    SLOT_ID,
    SLOT_S1,
    SLOT_S2,
    SLOT_S3,
)


@pytest.mark.parametrize("additional_slot_values", [None, "v1"])
@pytest.mark.parametrize(
    "description,ids,is_valid",
    [
        ("no_duplicates", ["P:1", "P:2"], True),
        ("duplicates", ["P:1", "P:1"], False),
        ("empty", [], True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_identifier(framework, description, ids, is_valid, additional_slot_values):
    """
    Tests basic behavior of identifiers.

    :param framework: all should support attributes
    :param description: description of the test data
    :param object: object to check
    :param is_valid: whether the object is valid
    :return:
    """
    classes = {
        CLASS_CONTAINER: {
            "attributes": {
                "entities": {
                    "range": CLASS_C,
                    "multivalued": True,
                    "inlined": True,
                    "inlined_as_list": True,
                },
            },
        },
        CLASS_C: {
            "attributes": {
                SLOT_ID: {
                    "identifier": True,
                },
                SLOT_S1: {},
            },
        },
    }
    schema = validated_schema(test_identifier, "default", framework, classes=classes, core_elements=["identifier"])
    obj = {"entities": [{"id": id, SLOT_S1: additional_slot_values} for id in ids]}
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if not is_valid and framework != PYTHON_DATACLASSES:
        expected_behavior = ValidationBehavior.INCOMPLETE
    if not additional_slot_values:
        pytest.skip("issues with dataclasses where object is empty except for plain id")
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        obj,
        is_valid,
        target_class=CLASS_CONTAINER,
        expected_behavior=expected_behavior,
        description=description,
    )


@pytest.mark.parametrize("consider_nulls_inequal", [False, True])
@pytest.mark.parametrize(
    "description,objects,is_valid,is_valid_if_nulls_inequal",
    [
        ("trivial", [], True, True),
        (
            "neq",
            [
                (None, None, None),
                (None, None, None),
            ],
            True,
            False,
        ),
        (
            "neq2",
            [
                ("x1", None, None),
                ("x1", None, None),
            ],
            True,
            False,
        ),
        (
            "no_duplicates",
            [
                ("x1", "y1", "z1"),
                ("x2", "y2", "z2"),
                ("x3", "y3", "z3"),
            ],
            True,
            True,
        ),
        (
            "duplicates_main",
            [
                ("x1", "y1", "z1"),
                ("x1", "y1", "z2"),
                ("x3", "y3", "z3"),
            ],
            False,
            False,
        ),
        (
            "duplicates_secondary",
            [
                ("x1", "y1", "z1"),
                ("x1", "y2", "z1"),
                ("x3", "y3", "z3"),
            ],
            False,
            False,
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_unique_keys(framework, description, objects, is_valid, is_valid_if_nulls_inequal, consider_nulls_inequal):
    """
    Tests unique keys

    """
    classes = {
        CLASS_CONTAINER: {
            "attributes": {
                "entities": {
                    "range": CLASS_C,
                    "multivalued": True,
                    "inlined": True,
                    "inlined_as_list": True,
                },
            },
        },
        CLASS_C: {
            "attributes": {
                SLOT_S1: {},
                SLOT_S2: {},
                SLOT_S3: {},
            },
            "unique_keys": {
                "main": {
                    "unique_key_slots": [SLOT_S1, SLOT_S2],
                    "consider_nulls_inequal": consider_nulls_inequal,
                },
                "secondary": {
                    "unique_key_slots": [SLOT_S1, SLOT_S3],
                    "consider_nulls_inequal": consider_nulls_inequal,
                },
            },
            "_mappings": {
                SQL_DDL_SQLITE: f"UNIQUE ({SLOT_S1}, {SLOT_S2})",
            },
        },
    }
    schema = validated_schema(
        test_unique_keys,
        f"NIE{consider_nulls_inequal}",
        framework,
        classes=classes,
        core_elements=["identifier"],
    )
    obj = {"entities": [{SLOT_S1: s1, SLOT_S2: s2, SLOT_S3: s3} for s1, s2, s3 in objects]}
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if not is_valid:
        if framework == SQL_DDL_SQLITE:
            # SQLite and most RDBMSs treats nulls as inequal
            if not consider_nulls_inequal:
                expected_behavior = ValidationBehavior.IMPLEMENTS
            else:
                expected_behavior = ValidationBehavior.INCOMPLETE
        else:
            # only supported in SQL backends
            expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        obj,
        is_valid,
        target_class=CLASS_CONTAINER,
        expected_behavior=expected_behavior,
        description=description,
    )
