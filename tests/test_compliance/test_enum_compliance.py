"""
Tests for enum compliance.

 - TODO: dynamic enums
"""
import re
from copy import deepcopy

import pytest

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    PYDANTIC,
    PYTHON_DATACLASSES,
    SQL_DDL_POSTGRES,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    generate_tree,
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
        ("EMPTY_ENUM", "empty", []),
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
            # "meaning": pv_meaning,
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
                PYDANTIC: f"class {safe_enum_name}(str, Enum)"
                if pvs
                else f"class {safe_enum_name}(str)",
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
    is_valid = value in [pv[0] for pv in pvs] or pvs == []
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework == SQL_DDL_SQLITE and not is_valid:
        # SQLite does not support enums
        expected_behavior = ValidationBehavior.INCOMPLETE
    if pvs == [] and framework not in [JSON_SCHEMA, PYDANTIC]:
        # only JSON Schema supports empty enums
        expected_behavior = ValidationBehavior.FALSE_POSITIVE
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


@pytest.mark.parametrize("include_meaning", [True, False])
@pytest.mark.parametrize("use_mixins", [False, True])
@pytest.mark.parametrize("propagate_down", [False, True])
@pytest.mark.parametrize(
    "data_name,data,is_valid",
    [
        ("empty", {}, True),
        ("1", {"slot_Enum0": "Enum0_1"}, True),
        ("2", {"slot_Enum0": "Enum01_1"}, False),
        ("3", {"slot_Enum0222": "Enum0222_1"}, True),
        ("4", {"slot_Enum0222": "Enum022_1"}, True),
        ("5", {"slot_Enum022": "Enum0222_1"}, False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_enum_hierarchy(
    framework, use_mixins, include_meaning, propagate_down, data_name, data, is_valid
):
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

    def _make_pv(_pv_name, pv_meaning=None, pv_description=None):
        pv = {}
        if pv_description:
            pv["description"] = pv_description
        if include_meaning and pv_meaning:
            pv["meaning"] = pv_meaning
        # E.g. Enum012_1 -> Enum01_1
        ix = _pv_name[-1]
        base = _pv_name[:-3]
        if base[-1] in ["0", "1"]:
            parent = f"{base}_{ix}"
            if use_mixins:
                pv["mixins"] = [parent]
            else:
                pv["is_a"] = parent
        return pv

    # remove non-alphanumeric from name

    tree = list(generate_tree(3, 2, "Enum"))
    enums = {}
    atts = {}
    for enum_name, parents in tree:
        pvs = {f"{enum_name}_{i}": _make_pv(f"{enum_name}_{i}") for i in range(1, 3)}
        enums[enum_name] = {"permissible_values": pvs}
        if parents:
            if use_mixins:
                enums[enum_name]["mixins"] = parents
            else:
                enums[enum_name]["is_a"] = parents[0]
                assert len(parents) == 1
        slot_name = f"slot_{enum_name}"
        atts[slot_name] = {
            "range": enum_name,
        }
    if propagate_down:
        # Note: assumes tree is ordered
        for child, parents in tree:
            for parent in parents:
                enums[child]["permissible_values"].update(
                    deepcopy(enums[parent]["permissible_values"])
                )
    else:
        pytest.skip("validation of inference of permissible values not yet implemented")

    classes = {
        CLASS_C: {"attributes": atts},
    }

    schema = validated_schema(
        test_enum_hierarchy,
        f"MeaningEQ_{include_meaning}__PropagateEQ_{propagate_down}__MixinsEQ_{use_mixins}",
        framework,
        classes=classes,
        enums=enums,
        prefixes={"schema": "http://schema.org/"},
        core_elements=["enum_definitions", "permissible_values", "meaning"],
    )

    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework == SQL_DDL_SQLITE and not is_valid:
        # SQLite does not support enums
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        data,
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=data_name,
    )
