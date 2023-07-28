"""
Tests for enum compliance.

 - TODO: dynamic enums
"""
import re

import pytest

from tests.test_compliance.helper import (
    PYDANTIC,
    PYTHON_DATACLASSES,
    SQL_DDL_POSTGRES,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CORE_FRAMEWORKS, SLOT_S1


@pytest.mark.parametrize("include_meaning", [True, False])
@pytest.mark.parametrize("value", ["A", "C", "schema:A"])
@pytest.mark.parametrize(
    "enum_name,enum_desc,pvs",
    [
        ("ENUM_A", "basic_enum", [("A", "schema:A", "An A"), ("B", "schema:B", "A B")]),
        (
            "ENUM_B",
            "curies_enum",
            [("schema:A", "schema:A", "An A"), ("schema:B", "schema:B", "A B")],
        ),
        ("ENUM_C", "ws_enum", [("A B", "schema:AB", "An A B"), ("B-%", "schema:Bpct", "A B%")]),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_enum(framework, enum_name, enum_desc, pvs, value, include_meaning):
    """
    Tests behavior of enums.

    :param framework: some frameworks like sqlite do not support enums
    :param enum_name: name of the enum
    :param enum_desc: description of the enum
    :param pvs: permissible values
    :param value: value to check
    :param include_meaning: whether to include the meaning in the enum
    :return:
    """

    def _make_pv(_pv_name, pv_meaning, pv_description):
        pv = {
            "meaning": pv_meaning,
            "description": pv_description,
        }
        if include_meaning:
            pv["meaning"] = pv_meaning
        return pv

    # remove non-alphanumeric from name
    safe_enum_name = re.sub(r"\W+", "", enum_name).replace("_", "")

    enums = {
        enum_name: {
            "description": enum_desc,
            "permissible_values": {pv[0]: _make_pv(*pv) for pv in pvs},
            "_mappings": {
                PYDANTIC: f"class {safe_enum_name}(str, Enum)",
                PYTHON_DATACLASSES: f"class {safe_enum_name}(EnumDefinitionImpl)",
                SQL_DDL_POSTGRES: f'CREATE TYPE "{enum_name}" AS ENUM',
            },
        }
    }
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": enum_name,
                    "_mappings": {
                        PYDANTIC: f"{SLOT_S1}: Optional[{safe_enum_name}]",
                        PYTHON_DATACLASSES: f'{SLOT_S1}: Optional[Union[str, "{safe_enum_name}"]]',
                        SQL_DDL_SQLITE: f"{SLOT_S1} VARCHAR",  ## sqlite does not support enums
                        # PYTHON_DATACLASSES: f"{SLOT_S1}: Optional[{typ_py_name}]",
                    },
                },
            }
        },
    }

    schema = validated_schema(
        test_enum,
        f"{enum_name}_M{include_meaning}",
        framework,
        classes=classes,
        enums=enums,
        prefixes={"schema": "http://schema.org/"},
        core_elements=["enum_definitions", "permissible_values", "meaning"],
    )
    is_valid = value in [pv[0] for pv in pvs]
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework == SQL_DDL_SQLITE and not is_valid:
        # SQLite does not support enums
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        value.replace(":", "_").replace(" ", "_"),
        framework,
        {SLOT_S1: value},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description="enum",
    )
