"""Tests ifabsent constructs for adding default values."""

import pytest
import rdflib

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    OWL,
    PANDERA_POLARS_CLASS,
    PYDANTIC,
    PYTHON_DATACLASSES,
    SHACL,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CLASS_D, CORE_FRAMEWORKS, ENUM_E, PV_1, SLOT_ID, SLOT_S1

FUZZ_STR = "a b_c!@#$%^&*_+{}|:<>?[]()'\""


@pytest.mark.parametrize(
    "schema_name,range,ifabsent,data_name,initial_value,expected,schema_valid,valid,skip_for",
    [
        ("str", "string", "string(x)", "no_value", None, "x", True, True),
        ("str", "string", "string(x)", "has_value", "y", "y", True, True),
        ("int", "integer", "int(5)", "no_value", None, 5, True, True),
        ("boolT", "boolean", "true", "no_value", None, True, True, True),
        ("boolF", "boolean", "false", "no_value", None, False, True, True),
        ("class_curie", "uriorcurie", "class_curie", "no_value", None, "ex:C", True, True),
        ("bnode", "nodeidentifier", "bnode", "no_value", None, rdflib.BNode, True, True),
        ("D", CLASS_D, "string(p1)", "no_value", None, "p1", False, True),
        ("inconsistent", "integer", "string(x)", "has_value", None, "x", True, False),
        # Skip Python, Pydantic and Shacl frameworks because this incompatibility is not possible with the processor
        (
            "incompat_string",
            "integer",
            "string(x)",
            "has_value",
            None,
            None,
            True,
            False,
            [PYTHON_DATACLASSES, PYDANTIC, PANDERA_POLARS_CLASS],
        ),
        (
            "incompat_bool",
            "boolean",
            "string(x)",
            "has_value",
            None,
            None,
            True,
            False,
            [PYTHON_DATACLASSES, PYDANTIC, SHACL, PANDERA_POLARS_CLASS],
        ),
        (
            "incompat_float",
            "float",
            "string(x)",
            "has_value",
            None,
            None,
            True,
            False,
            [PYTHON_DATACLASSES, PYDANTIC, SHACL, PANDERA_POLARS_CLASS],
        ),
        ("fuzz_str", "string", f"string({FUZZ_STR})", "has_value", None, FUZZ_STR, True, True, []),
        # ("enum", ENUM_E, f"(EnumName({PV_1})", "has_value", None, PV_1, True, True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_ifabsent(
    framework, schema_name, range, ifabsent, data_name, initial_value, expected, schema_valid, valid, skip_for
):
    """
    Tests behavior of ifabsent (defaults).

    Ifabsent allows for default values.

    :param framework: not supported by python dataclasses
    :param schema_name: the name reflects which constraints are implemented
    :param ifabsent: default value
    :param initial_value: value to check
    :param expected: expected value (not used)
    :return:
    """

    if framework in skip_for:
        return

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
    enums = {}
    if range == ENUM_E:
        enums = {ENUM_E: {"permissible_values": {PV_1: {}}}}
    if range == CLASS_D:
        classes[CLASS_D] = {"attributes": {SLOT_ID: {"range": "string", "identifier": True}}}
    try:
        schema = validated_schema(
            test_ifabsent, schema_name, framework, classes=classes, enums=enums, core_elements=["ifabsent"]
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
    exclude_rdf = True
    def instance_check_call(obj):
        if ifabsent == "class_curie":
            return True
        if framework in [PYTHON_DATACLASSES, PYDANTIC]:
            if expected == rdflib.BNode:
                return getattr(obj, SLOT_S1).startswith("_:")
            return getattr(obj, SLOT_S1) == expected
        return True
    if ifabsent == "bnode":
        if framework in [PYTHON_DATACLASSES, SQL_DDL_SQLITE]:
            pytest.skip("TODO: fix bug in metamodelcore")
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: initial_value} if initial_value is not None else {},
        valid,
        expected_behavior=implementation_status,
        target_class=CLASS_C,
        exclude_rdf=exclude_rdf,
        instance_check_call=instance_check_call,
    )
