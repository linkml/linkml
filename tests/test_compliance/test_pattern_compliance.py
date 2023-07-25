"""Tests for pattern slots and use of regular expressions as constraints."""
import re

import pytest

from tests.test_compliance.helper import (
    PYDANTIC,
    PYTHON_DATACLASSES,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CORE_FRAMEWORKS, SLOT_S1


@pytest.mark.parametrize(
    "schema_name,pattern,data_name,value",
    [
        ("complete_match", r"^\S+$", "no_ws", "ab"),
        ("complete_match", r"^\S+$", "ws", "a b"),
        ("partial_match", r"ab", "partial_ab", "abcd"),
        ("partial_match", r"ab", "complete_ab", "ab"),
        ("partial_match", r"ab", "ws", "a b"),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_pattern(framework, schema_name, pattern, data_name, value):
    """
    Tests behavior of pattern slots.

    Pattern slots allow for regular expression constraints.
    Currently not supported for validation by python frameworks.

    :param framework: not supported by python frameworks
    :param schema_name: the name reflects which constraints are implementd
    :param pattern: regular expression
    :param value: value to check
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "pattern": pattern,
                },
            }
        }
    }
    schema = validated_schema(test_pattern, schema_name, framework, classes=classes)
    implementation_status = ValidationBehavior.IMPLEMENTS
    is_valid = bool(re.match(pattern, value))
    if framework in [PYDANTIC, PYTHON_DATACLASSES, SQL_DDL_SQLITE]:
        if not is_valid:
            implementation_status = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: value},
        is_valid,
        expected_behavior=implementation_status,
        target_class=CLASS_C,
        description=f"matching {value} to {pattern} expected={is_valid}",
    )
