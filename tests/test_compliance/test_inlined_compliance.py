"""Inlining tests.

Tests that make use of linkml:inlined and related constructs.

- TODO: dict normalization, SimpleDicts and CompactDicts
"""
import pytest

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    PYDANTIC,
    PYTHON_DATACLASSES,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import (
    CLASS_C,
    CLASS_D,
    CORE_FRAMEWORKS,
    EXAMPLE_STRING_VALUE_2,
    EXAMPLE_STRING_VALUE_3,
    SLOT_ID,
    SLOT_S1,
    SLOT_S2,
    SLOT_S3,
)


@pytest.mark.parametrize("data", ["inlined_list", "flat", "nested", "flat_list"])
@pytest.mark.parametrize("foreign_key", [0, "FK"])
@pytest.mark.parametrize("multivalued", [0, "MV"])
@pytest.mark.parametrize("inlined_as_list", [0, "IAL"])
@pytest.mark.parametrize("inlined", [0, "INL"])
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)  ## TODO: consider limiting this
def test_inlined(framework, inlined, inlined_as_list, multivalued, foreign_key, data):
    """
    Tests behavior of inlined slots.

    Inlining controls whether nested objects are inlined or referenced by id.

    This test performs combinatorial testing with different values of metamodel slots that
    affect inlining, as these all compose together in different ways.

    :param framework: all tree-based frameworks should support inlining
    :param inlined: corresponds to linkml:inlined
    :param inlined_as_list: corresponds to linkml:inlined_as_list
    :param multivalued: corresponds to linkml:multivalued
    :param foreign_key: corresponds to whether the referenced entity has an identifier
    :return:
    """
    inlined = bool(inlined)
    inlined_as_list = bool(inlined_as_list)
    multivalued = bool(multivalued)
    foreign_key = bool(foreign_key)
    schema_name = f"INL{inlined}_IAL{inlined_as_list}_MV{multivalued}_FK{foreign_key}"
    entailed_inlined = inlined or inlined_as_list or not foreign_key
    py_def_map = {
        (PYDANTIC, False, False, False, False): "D",
        (PYDANTIC, False, False, False, True): "str",
        (PYDANTIC, False, False, True, False): "List[D]",
        (PYDANTIC, False, False, True, True): "List[str]",
        (PYDANTIC, False, True, False, False): "D",  # odd but valid combo
        (PYDANTIC, False, True, False, True): "D",  # odd but valid combo
        (PYDANTIC, False, True, True, False): "List[D]",
        # (PYDANTIC, False, True, True, True): "List[str]", ## TODO check this one
        (PYDANTIC, True, False, False, False): "D",
        (PYDANTIC, True, False, False, True): "D",
        (PYDANTIC, True, False, True, False): "List[D]",
        (PYDANTIC, True, False, True, True): "Dict[str, D]",
        (PYDANTIC, True, True, False, False): "D",  # odd but valid combo
        # (PYDANTIC, True, True, False, True): "str",  ## TODO check this one
        (PYDANTIC, True, True, True, False): "List[D]",
        (PYDANTIC, True, True, True, True): "List[D]",
        (PYTHON_DATACLASSES, False, False, False, False): 'Union[dict, "D"]',
        (PYTHON_DATACLASSES, False, False, False, True): "Union[str, DId]",
        (
            PYTHON_DATACLASSES,
            False,
            False,
            True,
            False,
        ): 'Union[Union[dict, "D"], List[Union[dict, "D"]]]',
        (
            PYTHON_DATACLASSES,
            False,
            False,
            True,
            True,
        ): "Union[Union[str, DId], List[Union[str, DId]]]",
        (PYTHON_DATACLASSES, False, True, False, False): 'Union[dict, "D"]',  # odd but valid combo
        (PYTHON_DATACLASSES, False, True, False, True): 'Union[dict, "D"]',  # odd but valid combo
        (
            PYTHON_DATACLASSES,
            False,
            True,
            True,
            False,
        ): 'Union[Union[dict, "D"], List[Union[dict, "D"]]]',
        (
            PYTHON_DATACLASSES,
            False,
            True,
            True,
            True,
        ): 'Union[Dict[Union[str, DId], Union[dict, "D"]], List[Union[dict, "D"]]]',
        (PYTHON_DATACLASSES, True, False, False, False): 'Union[dict, "D"]',
        (PYTHON_DATACLASSES, True, False, False, True): 'Union[dict, "D"]',
        (
            PYTHON_DATACLASSES,
            True,
            False,
            True,
            False,
        ): 'Union[Union[dict, "D"], List[Union[dict, "D"]]]',
        (
            PYTHON_DATACLASSES,
            True,
            False,
            True,
            True,
        ): 'Union[Dict[Union[str, DId], Union[dict, "D"]], List[Union[dict, "D"]]]',
        (PYTHON_DATACLASSES, True, True, False, False): 'Union[dict, "D"]',  # odd but valid combo
        (PYTHON_DATACLASSES, True, True, False, True): 'Union[dict, "D"]',
        (
            PYTHON_DATACLASSES,
            True,
            True,
            True,
            False,
        ): 'Union[Union[dict, "D"], List[Union[dict, "D"]]]',
        (
            PYTHON_DATACLASSES,
            True,
            True,
            True,
            True,
        ): 'Union[Dict[Union[str, DId], Union[dict, "D"]], List[Union[dict, "D"]]]',
    }
    tpl = (framework, inlined, inlined_as_list, multivalued, foreign_key)
    if tpl in py_def_map:
        py_def = py_def_map[tpl]
        py_def = f"Optional[{py_def}]"
    else:
        py_def = "Optional"
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "inlined": inlined,
                    "inlined_as_list": inlined_as_list,
                    "multivalued": multivalued,
                    "range": CLASS_D,
                    "_mappings": {
                        PYDANTIC: f"{SLOT_S1}: {py_def}",
                        PYTHON_DATACLASSES: f"{SLOT_S1}: {py_def}",
                    },
                },
            },
        },
        CLASS_D: {
            "attributes": {
                SLOT_ID: {
                    "identifier": foreign_key,
                },
                SLOT_S2: {},
                SLOT_S3: {},
            },
        },
    }
    schema = validated_schema(
        test_inlined,
        schema_name,
        framework,
        classes=classes,
        core_elements=["inlined", "inlined_as_list", "multivalued", "identifier"],
    )
    implementation_status = ValidationBehavior.IMPLEMENTS
    coerced = None
    id_val = "X:1"
    id_val2 = "X:2"
    if data == "flat":
        inst = {
            SLOT_S1: id_val,
        }
        is_valid = False if entailed_inlined or multivalued else True
        if not is_valid:
            if entailed_inlined:
                if foreign_key and multivalued and not inlined_as_list:
                    coerced = {SLOT_S1: {id_val: {SLOT_ID: id_val}}}
                elif foreign_key and multivalued and inlined_as_list:
                    coerced = {SLOT_S1: [{SLOT_ID: id_val}]}
                elif foreign_key and not multivalued:
                    coerced = {SLOT_S1: {SLOT_ID: id_val}}
            else:
                if not multivalued:
                    raise AssertionError
                if foreign_key:
                    coerced = {SLOT_S1: [id_val]}
                else:
                    raise AssertionError
    elif data == "nested":
        inst = {
            SLOT_S1: {
                SLOT_ID: id_val,
                SLOT_S2: EXAMPLE_STRING_VALUE_2,
                SLOT_S3: EXAMPLE_STRING_VALUE_3,
            }
        }
        is_valid = entailed_inlined and not multivalued
        if framework == JSON_SCHEMA:
            if inlined and not inlined_as_list and multivalued and foreign_key:
                # TODO: json-schema generation appears incorrect here
                implementation_status = ValidationBehavior.INCOMPLETE
    elif data == "flat_list":
        inst = {
            SLOT_S1: [id_val, id_val2],
        }
        is_valid = not entailed_inlined and multivalued
        if framework == SQL_DDL_SQLITE and multivalued and foreign_key:
            # TODO: bug in SQLA for this case
            implementation_status = ValidationBehavior.INCOMPLETE
    elif data == "inlined_list":
        inst = {
            SLOT_S1: [
                {
                    SLOT_ID: id_val,
                    SLOT_S2: EXAMPLE_STRING_VALUE_2,
                    SLOT_S3: EXAMPLE_STRING_VALUE_3,
                },
                {
                    SLOT_ID: id_val2,
                    SLOT_S2: EXAMPLE_STRING_VALUE_2,
                    SLOT_S3: EXAMPLE_STRING_VALUE_3,
                },
            ],
        }
        is_valid = (inlined_as_list or not foreign_key) and multivalued
    else:
        raise AssertionError(f"Unknown data type {data}")
    if not is_valid and framework == PYTHON_DATACLASSES:
        implementation_status = ValidationBehavior.COERCES
    if framework == SQL_DDL_SQLITE and not is_valid:
        implementation_status = ValidationBehavior.NOT_APPLICABLE
    check_data(
        schema,
        data,
        framework,
        inst,
        is_valid,
        coerced=coerced,
        expected_behavior=implementation_status,
        target_class=CLASS_C,
        description=f"testing data shape {data} against schema",
        exclude_rdf=not is_valid,
    )
