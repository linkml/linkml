"""Tests for pattern slots and use of regular expressions as constraints."""

# TODO: structured patterns

import re

import pytest

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    OWL,
    PYDANTIC,
    PYTHON_DATACLASSES,
    SHACL,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CLASS_D, CORE_FRAMEWORKS, SLOT_ID, SLOT_S1


@pytest.mark.parametrize(
    "schema_name,range,ifabsent,data_name,initial_value,expected,schema_valid,valid",
    [
        ("str", "string", "string(x)", "no_value", None, "x", True, True),
        ("str", "string", "string(x)", "has_value", "y", "x", True, True),
        ("int", "integer", "int(5)", "no_value", None, 5, True, True),
        ("boolT", "boolean", "true", "no_value", None, True, True, True),
        ("boolF", "boolean", "false", "no_value", None, False, True, True),
        ("class_curie", "uriorcurie", "class_curie", "no_value", None, "ex:C", True, True),
        ("D", CLASS_D, "string(p1)", "no_value", None, "p1", False, True),
        ("incompat", "integer", "string(x)", "has_value", None, "x", True, False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_ifabsent(framework, schema_name, range, ifabsent, data_name, initial_value, expected, schema_valid, valid):
    """
    Tests behavior of ifabsent (defaults).

    Ifabsent allows for default values.

    :param framework: not supported by python dataclasses
    :param schema_name: the name reflects which constraints are implemented
    :param ifabsent: default value
    :param initial_value: value to check
    :param expected: expected value
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "ifabsent": ifabsent,
                    "range": range,
                },
            }
        }
    }
    if range == CLASS_D:
        classes[CLASS_D] = {"attributes": {SLOT_ID: {"range": "string", "identifier": True}}}
    try:
        schema = validated_schema(
            test_ifabsent, schema_name, framework, classes=classes, core_elements=["ifabsent"]
        )
    except ValueError as e:
        if schema_valid:
            raise e
    if not schema_valid:
        return
    implementation_status = ValidationBehavior.IMPLEMENTS
    if not valid:
        if framework in [JSON_SCHEMA, SQL_DDL_SQLITE]:
            implementation_status = ValidationBehavior.INCOMPLETE
        if framework == PYDANTIC:
            implementation_status = ValidationBehavior.COERCES
        if framework == PYTHON_DATACLASSES:
            # validation in dataclasses only happens at the time of assignment
            implementation_status = ValidationBehavior.COERCES
        if framework == OWL:
            pytest.skip("this fails at the RDF generation stage, due to incompatible types")
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: initial_value},
        valid,
        expected_behavior=implementation_status,
        target_class=CLASS_C,
    )