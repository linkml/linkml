"""Inlining tests.

Tests that make use of linkml:inlined and related constructs.

See: `<https://linkml.io/linkml/schemas/inlining.html>`_

"""

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

    See: `<https://linkml.io/linkml/schemas/inlining.html>`_

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
    if framework == SHACL:
        pytest.skip("TODO: RDF has no concept of inlining")
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
        (PYDANTIC, False, True, True, True): "List[D]",
        (PYDANTIC, True, False, False, False): "D",
        (PYDANTIC, True, False, False, True): "D",
        (PYDANTIC, True, False, True, False): "List[D]",
        (PYDANTIC, True, False, True, True): "Dict[str, D]",  ## TODO: relax for CompactDict
        (PYDANTIC, True, True, False, False): "D",  # odd but valid combo
        (PYDANTIC, True, True, False, True): "D",
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
        if framework in (PYDANTIC, PYTHON_DATACLASSES):
            raise ValueError(f"No python annotation found for condition {tpl}")
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
    prefixes = {
        "X": "http://example.org/X/",
    }
    schema = validated_schema(
        test_inlined,
        schema_name,
        framework,
        classes=classes,
        prefixes=prefixes,
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
    elif data == "flat_list":
        inst = {
            SLOT_S1: [id_val, id_val2],
        }
        is_valid = not entailed_inlined and multivalued
        if framework == SQL_DDL_SQLITE and multivalued and foreign_key:
            # TODO: bug in SQLA for this case
            # AttributeError: 'DId' object has no attribute '_sa_instance_state'
            # https://github.com/linkml/linkml/issues/1160
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
    if framework in [SQL_DDL_SQLITE, SHACL] and not is_valid:
        # inlining has no cognate in relational and RDF
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


BASIC_ATTRS = {SLOT_ID: {"key": True}, SLOT_S1: {"range": "string"}}
EXTRA_ATTRS = {
    SLOT_ID: {"key": True},
    SLOT_S1: {"range": "string"},
    SLOT_S2: {"range": "string"},
}
IMPLICIT_ATTRS = {
    SLOT_ID: {"key": True},
    SLOT_S1: {"range": "string"},
    SLOT_S2: {"range": "string", "required": True},
}
ANNOTATED_ATTRS = {
    SLOT_ID: {"key": True},
    SLOT_S1: {"range": "string"},
    SLOT_S2: {"range": "string", "annotations": {"simple_dict_value": True}},
}


@pytest.mark.parametrize(
    "name,attrs,data_name,values,is_valid",
    [
        ("basic", BASIC_ATTRS, "t1", {"x": "y"}, True),
        ("basic", BASIC_ATTRS, "expanded", {"x": {SLOT_ID: "x", SLOT_S1: "y"}}, True),
        ("basic", BASIC_ATTRS, "expanded_nokey", {"x": {SLOT_S1: "y"}}, True),
        ("basic", BASIC_ATTRS, "expanded_noval", {"x": None}, True),
        ("basic", BASIC_ATTRS, "wrong_type", {"x": 5}, False),
        ("basic", BASIC_ATTRS, "empty", {}, True),
        ("extra", EXTRA_ATTRS, "t1", {"x": "y"}, False),
        ("extra", EXTRA_ATTRS, "expanded", {"x": {SLOT_ID: "x", SLOT_S1: "y"}}, True),
        ("extra", EXTRA_ATTRS, "empty", {}, True),
        ("implicit", IMPLICIT_ATTRS, "t1", {"x": "y"}, True),
        ("implicit", IMPLICIT_ATTRS, "expanded", {"x": {SLOT_ID: "x", SLOT_S2: "y"}}, True),
        ("implicit", IMPLICIT_ATTRS, "expanded2", {"x": {SLOT_ID: "x", SLOT_S1: "z", SLOT_S2: "y"}}, True),
        ("implicit", IMPLICIT_ATTRS, "expanded_noreqval", {"x": {}}, False),
        ("implicit", IMPLICIT_ATTRS, "empty", {}, True),
        ("annotated", ANNOTATED_ATTRS, "t1", {"x": "y"}, True),
        ("annotated", ANNOTATED_ATTRS, "expanded", {"x": {SLOT_ID: "x", SLOT_S2: "y"}}, True),
        ("annotated", ANNOTATED_ATTRS, "expanded2", {"x": {SLOT_ID: "x", SLOT_S1: "z", SLOT_S2: "y"}}, True),
        ("annotated", ANNOTATED_ATTRS, "empty", {}, True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_inlined_as_simple_dict(framework, name, attrs, data_name, values, is_valid):
    """
    Test inlined as simple dict.

    In some cases, a multivalued slot whose range is objects can be compacted to
    a SimpleDict, whose keys are the keys/identifiers of the object, and whose values
    are atomic and represent the "main value" for the object.

    An example of this is prefixes in the metamodel, where the value is the prefix_reference.

    A SimpleDict can be used in the following scenarios:

    1. The object is a tuple of two slots, the first being the key
    2. There is exactly one required non-key slot
    3. The main value slot is explicitly annotated

    This test sets up a schema where class C is a container for inlined class D objects,
    where the definition of class D is varied across different SimpleDict patterns.

    :param framework:
    :param name:
    :param attrs:
    :param data_name:
    :param values:
    :param is_valid:
    :return:
    """
    if framework in [SQL_DDL_SQLITE]:
        pytest.skip("TODO: SQLA do not support inlined as simple dict")
    if framework == PYDANTIC and name != "basic":
        pytest.skip("TODO: pydantic-based methods are permissive")
    if name == "extra" and data_name == "t1":
        if framework != JSON_SCHEMA:
            pytest.skip("TODO: dataclasses-based methods are permissive")
    if data_name == "expanded_noval" and framework != JSON_SCHEMA:
        pytest.skip("TODO: dataclasses-based methods dislike empty values for simpledict")
    coerced = None
    classes = {
        CLASS_D: {
            "attributes": attrs,
        },
        CLASS_C: {
            "attributes": {
                SLOT_S3: {
                    "range": CLASS_D,
                    "multivalued": True,
                    "inlined": True,
                },
            },
        },
    }
    schema = validated_schema(
        test_inlined_as_simple_dict, name, framework, classes=classes, description=name, core_elements=["inlined"]
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if data_name == "wrong_type":
        if framework in [PYTHON_DATACLASSES, PYDANTIC]:
            expected_behavior = ValidationBehavior.COERCES
        elif framework in [OWL, SHACL]:
            expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == PYDANTIC and data_name.startswith("expanded"):
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S3: values},
        is_valid,
        coerced=coerced,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        description=f"testing data shape {data_name} against schema {name}",
    )
