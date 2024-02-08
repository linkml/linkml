"""Constants for boolean slots tests (any_of, all_of, etc)."""

from typing import Optional

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
    CLASS_ANY,
    CLASS_C,
    CLASS_D,
    CLASS_U1,
    CLASS_U2,
    CORE_FRAMEWORKS,
    ENUM_E,
    ENUM_F,
    PV_1,
    PV_2,
    PV_3,
    SLOT_ID,
    SLOT_S1,
    SLOT_S2,
    SLOT_S3,
    CLASS_C1a,
    CLASS_C1b,
    SLOT_S1a,
    SLOT_S1b,
)


@pytest.mark.parametrize("use_default_range", [False, True])
@pytest.mark.parametrize("use_any_type", [False, True])
@pytest.mark.parametrize(
    "data_name,value,is_valid",
    [
        ("none", None, True),
        ("int", 1, True),
        ("str", "abc", False),
        ("obj", {SLOT_S2: "abc"}, True),
        ("bad_obj", {SLOT_S1: "abc"}, False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_slot_any_of(framework, data_name, value, is_valid, use_any_type, use_default_range):
    """
    Tests behavior of any_of at the slot level.

    This test creates a test schema with a slot S1 whose values
    are either an integer or an inlined instance of class D.

    any_of is a special case of boolean metaslot,
    as it cleanly maps to many language constructs (e.g. Union in Python),
    and it is often possible to normalize complex combinations to any_of form.

    TODO: resolve issues around combining any_of with default ranges or
    asserted ranges, see https://github.com/linkml/linkml/issues/1483

    :param framework: generator to test
    :param data_name: unique identifier for the test data instance
    :param value: data value to use in the instance
    :param is_valid: whether the test instance is expected to be valid
    :param use_any_type: if True, assert additional range using linkml:Any
    :param use_default_range: if True, the default range will be included in addition to any_of.
    :return:
    """
    expected_json_schema = {"s1": {"anyOf": [{"$ref": "#/$defs/D"}, {"type": "integer"}]}}
    if use_default_range and not use_any_type:
        # TODO: undesired behavior, see https://github.com/linkml/linkml/issues/1483
        expected_json_schema["s1"]["type"] = "string"
    if use_any_type:
        # TODO: undesired behavior, see https://github.com/linkml/linkml/issues/1483
        expected_json_schema["s1"]["$ref"] = "#/$defs/Any"
    classes = {
        CLASS_D: {
            "attributes": {
                SLOT_S2: {
                    "range": "string",
                },
            },
        },
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "any_of": [
                        {
                            "range": CLASS_D,
                        },
                        {"range": "integer"},
                    ],
                    "_mappings": {
                        PYDANTIC: f"{SLOT_S1}: Optional[Union[D, int]]",
                        JSON_SCHEMA: expected_json_schema,
                    },
                },
            },
        },
    }
    if use_default_range:
        default_range = "string"
    else:
        default_range = None
    if use_any_type:
        classes[CLASS_ANY] = {
            "class_uri": "linkml:Any",
        }
        classes[CLASS_C]["attributes"][SLOT_S1]["range"] = CLASS_ANY

    schema = validated_schema(
        test_slot_any_of,
        f"DefaultRangeEQ_{default_range}_AnyTypeEQ_{use_any_type}",
        framework,
        classes=classes,
        default_range=default_range,
        core_elements=["any_of", "range"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework in [PYTHON_DATACLASSES, SQL_DDL_SQLITE]:
        expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == JSON_SCHEMA:
        if use_default_range and not is_valid:
            # https://github.com/linkml/linkml/issues/1483
            expected_behavior = ValidationBehavior.INCOMPLETE
        if data_name == "bad_obj":
            expected_behavior = ValidationBehavior.INCOMPLETE
        if is_valid and (use_any_type or use_default_range):
            expected_behavior = ValidationBehavior.FALSE_POSITIVE
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: value},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {value}",
        exclude_rdf=True,
    )


@pytest.mark.parametrize(
    "data_name,value,is_valid",
    [
        ("v0", None, True),
        ("v1", 0, False),
        ("v2", 1, True),
        ("v3", 12, False),
        ("v4", 22, True),
        ("v5", 33, False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_slot_exactly_one_of(framework, data_name, value, is_valid):
    """
    Tests behavior of exactly_one_of at the slot level.

    This test creates a test schema with a slot S1 whose values
    are either an integer in the range [1, 15] or an integer in the range [10, 30].

    :param framework: generator to test
    :param data_name: unique identifier for the test data instance
    :param value: data value to use in the instance
    :param is_valid: whether the test instance is expected to be valid
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": "integer",
                    "exactly_one_of": [
                        {
                            "minimum_value": 1,
                            "maximum_value": 15,
                        },
                        {
                            "minimum_value": 10,
                            "maximum_value": 30,
                        },
                    ],
                },
            },
        },
    }
    schema = validated_schema(
        test_slot_exactly_one_of,
        "default",
        framework,
        classes=classes,
        core_elements=["exactly_one_of", "minimum_value", "maximum_value"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework != JSON_SCHEMA:
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: value},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {value}",
    )


@pytest.mark.parametrize(
    "data_name,value,is_valid",
    [
        ("v0", None, True),
        ("v1", 0, False),
        ("v2", 1, False),
        ("v3", 12, True),
        ("v4", 22, False),
        ("v5", 33, False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_slot_all_of(framework, data_name, value, is_valid):
    """
    Tests behavior of all_of at the slot level.

    This test creates a test schema with a slot S1 whose values
    are an integer in the range [1, 15] AND an integer in the range [10, 30].
    (This is an artificial example, a simpler schema would be to express directly
    in the range [10, 15] without using all_of.)

    :param framework: generator to test
    :param data_name: unique identifier for the test data instance
    :param value: data value to use in the instance
    :param is_valid: whether the test instance is expected to be valid
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": "integer",
                    "all_of": [
                        {
                            "minimum_value": 1,
                            "maximum_value": 15,
                        },
                        {
                            "minimum_value": 10,
                            "maximum_value": 30,
                        },
                    ],
                },
                "_mappings": {
                    JSON_SCHEMA: {
                        "s1": {
                            "allOf": [
                                {"maximum": 15, "minimum": 1},
                                {"maximum": 30, "minimum": 10},
                            ],
                            "type": "integer",
                        }
                    }
                },
            },
        },
    }
    schema = validated_schema(
        test_slot_all_of,
        "default",
        framework,
        classes=classes,
        core_elements=["all_of", "minimum_value", "maximum_value"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework != JSON_SCHEMA:
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: value},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {value}",
    )


@pytest.mark.parametrize(
    "data_name,value,is_valid",
    [
        ("v0", None, True),
        ("v1", 0, True),
        ("v2", 1, False),
        ("v3", 15, True),
        ("v4", 22, False),
        ("v5", 33, True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_slot_none_of(framework, data_name, value, is_valid):
    """
    Tests behavior of none_of at the slot level.

    This test creates a test schema with a slot S1 whose values
    are NOT an integer in the range [1, 10] AND NOT an integer in the range [21, 30].

    :param framework: generator to test
    :param data_name: unique identifier for the test data instance
    :param value: data value to use in the instance
    :param is_valid: whether the test instance is expected to be valid
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": "integer",
                    "none_of": [
                        {
                            "minimum_value": 1,
                            "maximum_value": 10,
                        },
                        {
                            "minimum_value": 21,
                            "maximum_value": 30,
                        },
                    ],
                },
            },
        },
    }
    schema = validated_schema(
        test_slot_none_of,
        "default",
        framework,
        classes=classes,
        core_elements=["none_of", "minimum_value", "maximum_value"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework != JSON_SCHEMA:
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: value},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {value}",
    )


@pytest.mark.parametrize(
    "data_name,instance,is_valid",
    [
        ("v0", {}, False),
        ("v1", {SLOT_S1: "x"}, True),
        ("v2", {SLOT_S2: "x"}, True),
        ("v3", {SLOT_S1: "x", SLOT_S2: "x"}, False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_cardinality_in_exactly_one_of(framework, data_name, instance, is_valid):
    """
    Tests intersection of cardinality and exactly_one_of.

    :param framework:
    :param data_name:
    :param instance:
    :param is_valid:
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {},
                SLOT_S2: {},
            },
            "exactly_one_of": [
                {
                    "slot_conditions": {
                        SLOT_S1: {
                            "required": True,
                        },
                    },
                },
                {
                    "slot_conditions": {
                        SLOT_S2: {
                            "required": True,
                        },
                    },
                },
            ],
        },
    }
    schema = validated_schema(
        test_cardinality_in_exactly_one_of,
        "default",
        framework,
        classes=classes,
        core_elements=["exactly_one_of", "minimum_value", "maximum_value"],
    )
    expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == JSON_SCHEMA:
        # TODO: this should be possible in json schema
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        instance,
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {instance}",
    )


@pytest.mark.parametrize(
    "data_name,s1value,s2value,is_valid",
    [
        ("none", None, None, True),
        ("both", 20, 20, True),
        ("first", 20, 0, True),
        ("second", 0, 20, True),
        ("neither", 0, 0, False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_class_any_of(framework, data_name, s1value, s2value, is_valid):
    """
    Tests behavior of any_of for classes.

    :param framework: generator to test
    :param data_name: unique identifier for the test data instance
    :param s1value: value for slot S1
    :param s2value: value for slot S2
    :param is_valid: whether the test instance is expected to be valid
    :return:
    """
    slots = {
        SLOT_S1: {
            "range": "integer",
        },
        SLOT_S2: {
            "range": "integer",
        },
    }
    classes = {
        CLASS_C: {
            "slots": [SLOT_S1, SLOT_S2],
            "any_of": [
                {
                    "slot_conditions": {
                        SLOT_S1: {
                            "minimum_value": 10,
                        },
                    },
                },
                {
                    "slot_conditions": {
                        SLOT_S2: {
                            "minimum_value": 20,
                        },
                    },
                },
            ],
        },
    }
    schema = validated_schema(
        test_class_any_of,
        "default",
        framework,
        classes=classes,
        slots=slots,
        core_elements=["any_of", "ClassDefinition"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework != OWL:
        expected_behavior = ValidationBehavior.INCOMPLETE
    # TODO: rdflib transformer has issues around ranges
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: s1value, SLOT_S2: s2value},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {s1value}, {s2value}",
        # exclude_rdf=True,
    )


@pytest.mark.parametrize(
    "schema_name,s1_range,s2_range,op,s1_expression,s2_expression,data_name,s1value,s2value,is_valid",
    [
        # strings
        (
            "any_of_streq",
            "string",
            "string",
            "any_of",
            {"equals_string": "x"},
            {"equals_string": "y"},
            "none",
            None,
            None,
            True,
        ),
        (
            "any_of_streq",
            "string",
            "string",
            "any_of",
            {"equals_string": "x"},
            {"equals_string": "y"},
            "both",
            "x",
            "y",
            True,
        ),
        (
            "any_of_streq",
            "string",
            "string",
            "any_of",
            {"equals_string": "x"},
            {"equals_string": "y"},
            "first",
            "x",
            "z",
            True,
        ),
        (
            "any_of_streq",
            "string",
            "string",
            "any_of",
            {"equals_string": "x"},
            {"equals_string": "y"},
            "second",
            "z",
            "y",
            True,
        ),
        (
            "any_of_streq",
            "string",
            "string",
            "any_of",
            {"equals_string": "x"},
            {"equals_string": "y"},
            "neither",
            "z",
            "z",
            False,
        ),
        # list of strings
        (
            "any_of_streq_MV",
            "string*",
            "string*",
            "any_of",
            {"equals_string_in": ["x"]},
            {"equals_string_in": ["y"]},
            "none",
            None,
            None,
            True,
        ),
        (
            "any_of_streq_MV",
            "string*",
            "string*",
            "any_of",
            {"equals_string_in": ["x", "a"]},
            {"equals_string_in": ["y", "a"]},
            "both",
            ["x"],
            ["y"],
            True,
        ),
        (
            "any_of_streq_MV",
            "string*",
            "string*",
            "any_of",
            {"equals_string_in": ["x", "a"]},
            {"equals_string_in": ["y", "a"]},
            "first",
            ["x"],
            ["z"],
            True,
        ),
        (
            "any_of_streq_MV",
            "string*",
            "string*",
            "any_of",
            {"equals_string_in": ["x", "a"]},
            {"equals_string_in": ["y", "a"]},
            "second",
            ["z"],
            ["y"],
            True,
        ),
        (
            "any_of_streq_MV",
            "string*",
            "string*",
            "any_of",
            {"equals_string_in": ["x", "a"]},
            {"equals_string_in": ["y", "a"]},
            "neither",
            ["x", "z"],
            ["y", "z"],
            False,
        ),
        # strings, object reference
        (
            "any_of_streq_ref",
            "D",
            "D",
            "any_of",
            {"equals_string": "TEST:x"},
            {"equals_string": "TEST:y"},
            "none",
            None,
            None,
            True,
        ),
        (
            "any_of_streq_ref",
            "D",
            "D",
            "any_of",
            {"equals_string": "TEST:x"},
            {"equals_string": "TEST:y"},
            "both",
            "TEST:x",
            "TEST:y",
            True,
        ),
        (
            "any_of_streq_ref",
            "D",
            "D",
            "any_of",
            {"equals_string": "TEST:x"},
            {"equals_string": "TEST:y"},
            "first",
            "TEST:x",
            "TEST:z",
            True,
        ),
        (
            "any_of_streq_ref",
            "D",
            "D",
            "any_of",
            {"equals_string": "TEST:x"},
            {"equals_string": "TEST:y"},
            "second",
            "TEST:z",
            "TEST:y",
            True,
        ),
        (
            "any_of_streq_ref",
            "D",
            "D",
            "any_of",
            {"equals_string": "TEST:x"},
            {"equals_string": "TEST:y"},
            "neither",
            "TEST:z",
            "TEST:z",
            False,
        ),
        # ints, all_of
        (
            "all_of_min_min_INT",
            "integer",
            "integer",
            "all_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "none",
            None,
            None,
            True,
        ),
        (
            "all_of_min_min_INT",
            "integer",
            "integer",
            "all_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "both",
            20,
            20,
            True,
        ),
        (
            "all_of_min_min_INT",
            "integer",
            "integer",
            "all_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "first",
            20,
            0,
            False,
        ),
        (
            "all_of_min_min_INT",
            "integer",
            "integer",
            "all_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "second",
            0,
            20,
            False,
        ),
        (
            "all_of_min_min_INT",
            "integer",
            "integer",
            "all_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "neither",
            0,
            0,
            False,
        ),
        # ints, none_of
        (
            "none_of_min_min_INT",
            "integer",
            "integer",
            "none_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "none",
            None,
            None,
            True,
        ),
        (
            "none_of_min_min_INT",
            "integer",
            "integer",
            "none_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "both",
            20,
            20,
            False,
        ),
        (
            "none_of_min_min_INT",
            "integer",
            "integer",
            "none_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "first",
            20,
            0,
            False,
        ),
        (
            "none_of_min_min_INT",
            "integer",
            "integer",
            "none_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "second",
            0,
            20,
            False,
        ),
        (
            "none_of_min_min_INT",
            "integer",
            "integer",
            "none_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "neither",
            0,
            0,
            True,
        ),
        # ints, any_of
        (
            "any_of_min_min_INT",
            "integer",
            "integer",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "none",
            None,
            None,
            True,
        ),
        (
            "any_of_min_min_INT",
            "integer",
            "integer",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "both",
            20,
            20,
            True,
        ),
        (
            "any_of_min_min_INT",
            "integer",
            "integer",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "first",
            20,
            0,
            True,
        ),
        (
            "any_of_min_min_INT",
            "integer",
            "integer",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "second",
            0,
            20,
            True,
        ),
        (
            "any_of_min_min_INT",
            "integer",
            "integer",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "neither",
            0,
            0,
            False,
        ),
        # floats, any_of
        (
            "any_of_min_min_FLOAT",
            "float",
            "float",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "none",
            None,
            None,
            True,
        ),
        (
            "any_of_min_min_FLOAT",
            "float",
            "float",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "both",
            20.0,
            20.0,
            True,
        ),
        (
            "any_of_min_min_FLOAT",
            "float",
            "float",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "first",
            20.0,
            0.0,
            True,
        ),
        (
            "any_of_min_min_FLOAT",
            "float",
            "float",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "second",
            0.0,
            20.0,
            True,
        ),
        (
            "any_of_min_min_FLOAT",
            "float",
            "float",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "neither",
            0.0,
            0.0,
            False,
        ),
        # Any type, any_of
        (
            "any_of_min_min_ANY",
            "Any",
            "integer",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "none",
            None,
            None,
            True,
        ),
        (
            "any_of_min_min_ANY",
            "Any",
            "integer",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "both",
            20,
            20,
            True,
        ),
        (
            "any_of_min_min_ANY",
            "Any",
            "integer",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "first",
            20,
            0,
            True,
        ),
        (
            "any_of_min_min_ANY",
            "Any",
            "integer",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "second",
            0,
            20,
            True,
        ),
        (
            "any_of_min_min_ANY",
            "Any",
            "integer",
            "any_of",
            {"minimum_value": 10},
            {"minimum_value": 20},
            "neither",
            0,
            0,
            False,
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_class_boolean_with_expressions(
    framework, schema_name, s1_range, s2_range, op, s1_expression, s2_expression, data_name, s1value, s2value, is_valid
):
    """
    Tests behavior of any_of for class expressions.

    :param framework: generator to test
    :param schema_name: unique name of generated schema
    :param s1_range: range of slot 1
    :param s2_range: range of slot 2
    :param op: linkml boolean operation to use
    :param s1_expression: expression for slot 1
    :param s2_expression: expression for slot 2
    :param data_name: name of data to generate
    :param s1value: value for slot 1
    :param s2value: value for slot 2
    :param is_valid: whether the data should be valid
    :return:
    """
    if (s1_range == CLASS_ANY or s2_range == CLASS_ANY) and framework not in [PYDANTIC]:
        pytest.skip("Class Any not supported in this test")
    if framework == SHACL:
        pytest.skip("shaclgen does not support boolean expressions yet")
    if s1_range.endswith("*"):
        s1_multivalued = True
        s1_range = s1_range[:-1]
    else:
        s1_multivalued = False
    if s2_range.endswith("*"):
        s2_multivalued = True
        s2_range = s2_range[:-1]
    else:
        s2_multivalued = False
    slots = {
        SLOT_S1: {
            "range": s1_range,
            "multivalued": s1_multivalued,
        },
        SLOT_S2: {
            "range": s2_range,
            "multivalued": s2_multivalued,
        },
        SLOT_S3: {
            "range": "string",
        },
        SLOT_ID: {
            "range": "string",
            "identifier": True,
        },
    }
    classes = {
        CLASS_ANY: {
            "class_uri": "linkml:Any",
        },
        CLASS_D: {
            "slots": [SLOT_ID, SLOT_S3],
        },
        CLASS_C: {
            "slots": [SLOT_S1, SLOT_S2],
            op: [
                {
                    "slot_conditions": {
                        SLOT_S1: s1_expression,
                    },
                },
                {
                    "slot_conditions": {
                        SLOT_S2: s2_expression,
                    },
                },
            ],
        },
    }
    schema = validated_schema(
        test_class_boolean_with_expressions,
        schema_name,
        framework,
        prefixes={
            "TEST": "https://example.org/TEST/",
        },
        classes=classes,
        slots=slots,
        core_elements=["any_of", "ClassDefinition"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if not is_valid and framework not in [OWL]:
        expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == OWL:
        if s1_range == "float" or s2_range == "float":
            # TODO: investigate this
            expected_behavior = ValidationBehavior.FALSE_POSITIVE
        if s1_range == "D" or s2_range == "D":
            # expected: OWL is open world
            expected_behavior = ValidationBehavior.INCOMPLETE

    check_data(
        schema,
        f"{schema_name}-{data_name}",
        framework,
        {SLOT_S1: s1value, SLOT_S2: s2value},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {s1value}, {s2value}",
        # exclude_rdf=True,
    )


@pytest.mark.parametrize(
    "schema_name,range,op,expression1,expression2,data_name,value,is_valid",
    [
        # any-type
        (
            "any_of_anytype",
            "Any",
            "any_of",
            {"range": "string", "equals_string": "x"},
            {"range": "string", "equals_string": "y"},
            "matches_one",
            "x",
            True,
        ),
        (
            "any_of_anytype",
            "Any",
            "any_of",
            {"range": "string", "equals_string": "x"},
            {"range": "string", "equals_string": "y"},
            "matches_none",
            "z",
            False,
        ),
        (
            "mixed",
            "Any",
            "any_of",
            {"range": "integer", "minimum_value": 5},
            {"range": "string", "equals_string": "y"},
            "matches_str",
            "x",
            True,
        ),
        (
            "mixed",
            "Any",
            "any_of",
            {"range": "integer", "minimum_value": 5},
            {"range": "string", "equals_string": "y"},
            "matches_int",
            8,
            True,
        ),
        (
            "mixed",
            "Any",
            "any_of",
            {"range": "integer", "minimum_value": 5},
            {"range": "string", "equals_string": "y"},
            "matches_none",
            1,
            False,
        ),
        ("mixed_cls_int", "Any", "any_of", {"range": CLASS_D}, {"range": "integer"}, "matches_int", 1, True),
        ("mixed_cls_int", "Any", "any_of", {"range": CLASS_D}, {"range": "integer"}, "matches_obj", "test:x", True),
        ("mixed_enum_int", "Any", "any_of", {"range": ENUM_E}, {"range": "integer"}, "matches_int", 1, True),
        ("mixed_enum_int", "Any", "any_of", {"range": ENUM_E}, {"range": "integer"}, "matches_pv", PV_1, True),
        ("mixed_enum_int", "Any", "any_of", {"range": ENUM_E}, {"range": "integer"}, "matches_none", "z", False),
        ("mixed_all_of_enum_enum", "Any", "all_of", {"range": ENUM_E}, {"range": ENUM_F}, "matches_pv", PV_2, True),
        ("mixed_all_of_enum_enum", "Any", "all_of", {"range": ENUM_E}, {"range": ENUM_F}, "matches_pv", PV_1, False),
        ("mixed_all_of_enum_enum", "Any", "all_of", {"range": ENUM_E}, {"range": ENUM_F}, "matches_pv", PV_3, False),
        ("mixed_all_of_enum_enum", "Any", "all_of", {"range": ENUM_E}, {"range": ENUM_F}, "matches_pv", "z", False),
        # mixed cardinality; not yet allowed at expression level
        # ("todo, "string", "any_of", {"multivalued": True}, {"multivalued": False}, "match_sv", "x", True),
        # ("todo", "string", "any_of", {"multivalued": True}, {"multivalued": False}, "match_mv", ["x"], True),
        # strings
        ("any_of_streq", "string", "any_of", {"equals_string": "x"}, {"equals_string": "y"}, "none", None, True),
        ("any_of_streq", "string", "any_of", {"equals_string": "x"}, {"equals_string": "y"}, "matches", "x", True),
        ("any_of_streq", "string", "any_of", {"equals_string": "x"}, {"equals_string": "y"}, "no_matches", "z", False),
        # list of strings
        (
            "any_of_streq_MV",
            "string*",
            "any_of",
            {"equals_string_in": ["x"]},
            {"equals_string_in": ["y"]},
            "none",
            None,
            True,
        ),
        (
            "any_of_streq_MV",
            "string*",
            "any_of",
            {"equals_string_in": ["x", "a"]},
            {"equals_string_in": ["y", "a"]},
            "one",
            ["y", "z"],
            False,
        ),
        (
            "any_of_streq_MV",
            "string*",
            "any_of",
            {"equals_string_in": ["x", "a"]},
            {"equals_string_in": ["y", "a"]},
            "neither",
            ["z"],
            False,
        ),
        # strings, object reference
        (
            "any_of_streq_ref",
            CLASS_D,
            "any_of",
            {"equals_string": "TEST:x"},
            {"equals_string": "TEST:y"},
            "none",
            None,
            True,
        ),
        (
            "any_of_streq_ref",
            CLASS_D,
            "any_of",
            {"equals_string": "TEST:x"},
            {"equals_string": "TEST:y"},
            "match",
            "TEST:x",
            True,
        ),
        (
            "any_of_streq_ref",
            CLASS_D,
            "any_of",
            {"equals_string": "TEST:x"},
            {"equals_string": "TEST:y"},
            "neither",
            "TEST:z",
            False,
        ),
        # ints, all_of
        ("all_of_min_min_INT", "integer", "all_of", {"minimum_value": 10}, {"minimum_value": 20}, "none", None, True),
        ("all_of_min_min_INT", "integer", "all_of", {"minimum_value": 10}, {"minimum_value": 20}, "both", 20, True),
        ("all_of_min_min_INT", "integer", "all_of", {"minimum_value": 10}, {"minimum_value": 20}, "one", 10, False),
        ("all_of_min_min_INT", "integer", "all_of", {"minimum_value": 10}, {"minimum_value": 20}, "neither", 0, False),
        # ints, none_of
        ("none_of_min_min_INT", "integer", "none_of", {"minimum_value": 10}, {"minimum_value": 20}, "none", None, True),
        ("none_of_min_min_INT", "integer", "none_of", {"minimum_value": 10}, {"minimum_value": 20}, "both", 20, False),
        ("none_of_min_min_INT", "integer", "none_of", {"minimum_value": 10}, {"minimum_value": 20}, "first", 10, False),
        ("none_of_min_min_INT", "integer", "none_of", {"minimum_value": 10}, {"minimum_value": 20}, "neither", 0, True),
        # ints, any_of
        ("any_of_min_min_INT", "integer", "any_of", {"minimum_value": 10}, {"minimum_value": 20}, "none", None, True),
        ("any_of_min_min_INT", "integer", "any_of", {"minimum_value": 10}, {"minimum_value": 20}, "both", 20, True),
        ("any_of_min_min_INT", "integer", "any_of", {"minimum_value": 10}, {"minimum_value": 20}, "first", 10, True),
        ("any_of_min_min_INT", "integer", "any_of", {"minimum_value": 10}, {"minimum_value": 20}, "neither", 0, False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_slot_boolean_with_expressions(
    framework, schema_name, range, op, expression1, expression2, data_name, value, is_valid
):
    """
    Tests behavior of any_of for slot expressions.

    :param framework: generator to test
    :param schema_name: unique name of generated schema
    :param range: range of slot; a "*" indicates multivalued
    :param op: linkml boolean operation to use (combines expression1 and expression2)
    :param expression1: first expression
    :param expression2: second expression
    :param data_name: unique name of generated data
    :param value: value to test
    :param is_valid: expected validity of value
    :return:
    """
    if framework == SHACL:
        pytest.skip("shaclgen does not support boolean expressions yet")
    if range.endswith("*"):
        multivalued = True
        range = range[:-1]
    else:
        multivalued = False
    slots = {
        SLOT_S1: {
            "range": range,
            "multivalued": multivalued,
        },
        SLOT_S3: {
            "range": "string",
        },
        SLOT_ID: {
            "range": "string",
            "identifier": True,
        },
    }
    classes = {
        CLASS_ANY: {
            "class_uri": "linkml:Any",
        },
        CLASS_D: {
            "slots": [SLOT_ID, SLOT_S3],
        },
        CLASS_C: {
            "slots": [SLOT_S1],
            "slot_usage": {
                SLOT_S1: {
                    op: [expression1, expression2],
                },
            },
        },
    }
    enums = {}
    if expression1.get("range", None) == ENUM_E or expression2.get("range", None) == ENUM_E:
        enums[ENUM_E] = {
            "permissible_values": {PV_1: {}, PV_2: {}},
        }
    if expression1.get("range", None) == ENUM_F or expression2.get("range", None) == ENUM_F:
        enums[ENUM_F] = {
            "permissible_values": {PV_2: {}, PV_3: {}},
        }
    schema = validated_schema(
        test_slot_boolean_with_expressions,
        schema_name,
        framework,
        prefixes={
            "TEST": "https://example.org/TEST/",
        },
        classes=classes,
        slots=slots,
        enums=enums,
        core_elements=["any_of", "ClassDefinition"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if not is_valid and framework not in [OWL, JSON_SCHEMA]:
        expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == JSON_SCHEMA:
        if multivalued and not is_valid:
            # https://github.com/linkml/linkml/issues/1677
            expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == OWL:
        if range == "float":
            # TODO: investigate this
            expected_behavior = ValidationBehavior.FALSE_POSITIVE
        if range == CLASS_D:
            # expected: OWL is open world
            expected_behavior = ValidationBehavior.INCOMPLETE

    exclude_rdf = False
    if range == "Any":
        exclude_rdf = True
        if framework in [JSON_SCHEMA, SQL_DDL_SQLITE]:
            expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        f"{schema_name}-{data_name}",
        framework,
        {SLOT_S1: value},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {value}",
        exclude_rdf=exclude_rdf,
    )


@pytest.mark.parametrize(
    "value",
    [1, 10, 15, 20, 21],
)
@pytest.mark.parametrize(
    "min_val,max_val,equals_number",
    [(10, 20, None), (10, 10, None), (20, 10, None), (10, 20, 15), (None, None, 1)],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_min_max(framework, min_val, max_val, equals_number: Optional[int], value):
    """
    Tests behavior of minimum and maximum value.

    This test creates a test schema with a slot S1 whose values
    are an integer in the range [min_val, max_val], where min_val and max_val
    are parameters to the test.

    :param framework: generator to test
    :param min_val: minimum value for slot in schema
    :param max_val: maximum value for slot in schema
    :param equals_number: equals_number in schema
    :param value: value of slot in data to test with
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "required": True,
                    "range": "integer",
                    "minimum_value": min_val,
                    "maximum_value": max_val,
                    "equals_number": equals_number,
                    "_mappings": {
                        PYDANTIC: (
                            f"{SLOT_S1}: int = Field(..., ge={min_val}, le={max_val})" if not equals_number else ""
                        )
                    },
                },
            },
        },
    }

    def between(x, low, high) -> bool:
        if x is None:
            return True
        if low is not None and x < low:
            return False
        if high is not None and x > high:
            return False
        return True

    satisfiable = between(equals_number, min_val, max_val)
    if min_val is not None and max_val is not None:
        satisfiable = min_val <= max_val
    is_valid = between(value, min_val, max_val)
    comments = []
    if not satisfiable:
        comments.append("not satisfiable min {min_val} > max {max_val}")
    schema = validated_schema(
        test_min_max,
        f"min{min_val}_max{max_val}_eq{equals_number}",
        framework,
        classes=classes,
        core_elements=["minimum_value", "maximum_value", "range"],
        comments=comments,
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if equals_number is not None and is_valid:
        is_valid = equals_number == value
    if framework in [PYTHON_DATACLASSES, SQL_DDL_SQLITE]:
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        f"v{value}",
        framework,
        {SLOT_S1: value},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {value}",
    )


@pytest.mark.parametrize(
    "s1,s2,is_valid",
    [
        (0, 0, False),
        (0, 1, True),
        (1, 0, True),
        (1, 1, True),
        (0, 10, False),
        (10, 10, False),
        (10, 11, True),
        (11, 10, True),
        (11, 11, True),
        (10, 0, False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_preconditions(framework, s1, s2, is_valid):
    """
    Tests behavior of rules (preconditions and postconditions).

    This test creates a test schema with a slot S1 and S2 whose values
    are integers, where there is also a rule stating that if S1 is either 0 or 10,
    S2 cannot be either 0 or 10. The test then checks the validity of the data.

    :param framework: generator to test
    :param s1: value of slot S1
    :param s2: value of slot S2
    :param is_valid: whether the data is valid
    :return:
    """
    if framework == SHACL:
        pytest.skip("shaclgen does not support rules yet")
    classes = {
        CLASS_C: {
            "description": "if s1 is either 0 or 10, s2 cannot be either 0 or 10",
            "attributes": {
                SLOT_S1: {
                    "range": "integer",
                },
                SLOT_S2: {
                    "range": "integer",
                },
            },
            "rules": [
                {
                    "preconditions": {
                        "slot_conditions": {
                            SLOT_S1: {
                                "any_of": [
                                    {"equals_number": 0},
                                    {"equals_number": 10},
                                ]
                            }
                        },
                    },
                    "postconditions": {
                        "slot_conditions": {
                            SLOT_S2: {
                                "none_of": [
                                    {"equals_number": 0},
                                    {"equals_number": 10},
                                ],
                            },
                        },
                    },
                },
            ],
        },
    }
    schema = validated_schema(
        test_preconditions,
        "default",
        framework,
        classes=classes,
        core_elements=[
            "preconditions",
            "postconditions",
            "slot_conditions",
            "any_of",
            "none_of",
            "equals_number",
        ],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework not in [JSON_SCHEMA, OWL]:
        # only JSON Schema supports rules
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        f"v{s1}_{s2}",
        framework,
        {SLOT_S1: s1, SLOT_S2: s2},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {s1} {s2}",
    )


@pytest.mark.parametrize(
    "s1,s1a,s1b,is_valid",
    [
        (None, None, None, True),
        (15, "t", None, True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_classification_rules(framework, s1, s1a, s1b, is_valid):
    """
    Tests behavior of classification rules.

    :param framework: generator to test
    :param s1: value of slot S1
    :param s1a: value of slot S1a
    :param s1b: value of slot S1b
    :param is_valid: whether the data is valid
    :return:
    """
    if framework == SHACL:
        pytest.skip("shaclgen does not support boolean expressions yet")
    classes = {
        CLASS_C: {
            "description": "parent",
            "attributes": {
                SLOT_S1: {
                    "range": "integer",
                },
            },
        },
        CLASS_C1a: {
            "is_a": CLASS_C,
            "attributes": {
                SLOT_S1a: {
                    "range": "string",
                }
            },
            "classification_rules": [
                {
                    "is_a": CLASS_C,
                    "slot_conditions": {
                        SLOT_S1: {
                            "minimum_value": 10,
                            "maximum_value": 20,
                        },
                    },
                },
            ],
        },
        CLASS_C1b: {
            "is_a": CLASS_C,
            "attributes": {
                SLOT_S1b: {
                    "range": "string",
                }
            },
            "classification_rules": [
                {
                    "is_a": CLASS_C,
                    "slot_conditions": {
                        SLOT_S1: {
                            "minimum_value": 20,
                            "maximum_value": 30,
                        },
                    },
                },
            ],
        },
    }
    schema = validated_schema(
        test_classification_rules,
        "default",
        framework,
        classes=classes,
        core_elements=[
            "classification_rules",
            "slot_conditions",
        ],
    )
    expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == OWL:
        # The OWL works, however, currently the conversion requires
        # going via python objects, which cannot be instantiated as
        # they don't implement this inference
        expected_behavior = ValidationBehavior.INCOMPLETE
    inst = {SLOT_S1: s1, SLOT_S1a: s1a, SLOT_S1b: s1b}
    inst = {k: v for k, v in inst.items() if v is not None}
    check_data(
        schema,
        f"v{s1}_{s1a}_{s1b}",
        framework,
        inst,
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {s1a} {s1b}",
    )


@pytest.mark.parametrize(
    "data_name,value,is_valid",
    [
        ("none", None, True),
        ("int", 1, True),
        ("str", "abc", False),
        ("obj", {SLOT_S2: "abc"}, True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
@pytest.mark.skip(reason="not implemented")
def test_union_of(framework, data_name, value, is_valid):
    """
    Tests behavior of union_of.

    :param framework:
    :param data_name:
    :param value:
    :param is_valid:
    :return:
    """
    if framework == SHACL:
        pytest.skip("shaclgen does not support boolean expressions yet")
    classes = {
        CLASS_D: {
            "attributes": {
                SLOT_S2: {
                    "range": "string",
                },
            },
        },
        CLASS_C: {
            "union_of": [
                CLASS_U1,
                CLASS_U2,
            ],
        },
        CLASS_U1: {
            "attributes": {
                SLOT_S1: {
                    "range": CLASS_D,
                },
            },
        },
        CLASS_U2: {
            "attributes": {
                SLOT_S1: {
                    "range": "integer",
                },
            },
        },
    }
    schema = validated_schema(
        test_union_of,
        "default",
        framework,
        classes=classes,
        core_elements=["union_of", "range"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework in [PYTHON_DATACLASSES, SQL_DDL_SQLITE]:
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: value},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {value}",
    )


@pytest.mark.parametrize(
    "data_name,instance,is_valid",
    [
        ("v0", {}, False),
        ("v1", {SLOT_S1: "x"}, True),
        ("v2", {SLOT_S2: "x"}, True),
        ("v3", {SLOT_S1: "x", SLOT_S2: "x"}, False),
    ],
)
@pytest.mark.parametrize("multivalued", [False, True])
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_value_presence_in_rules(framework, multivalued, data_name, instance, is_valid):
    """
    Tests intersection of value_presence and rules.

    This test creates a test schema with a class C with two slots, S1 and S2,
    where either S1 or S2 is set, but not both. The test then checks the validity
    of the data specified by the instance parameter.

    :param framework: generator to test
    :param multivalued: whether the slots are multivalued or not
    :param data_name: name of data to test with
    :param instance: data object to test with
    :param is_valid: whether the data is valid or not
    :return:
    """
    if framework == SHACL:
        pytest.skip("shaclgen does not support boolean expressions yet")
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "multivalued": multivalued,
                },
                SLOT_S2: {
                    "multivalued": multivalued,
                },
            },
            "rules": [
                {
                    "preconditions": {
                        "slot_conditions": {
                            SLOT_S1: {
                                "value_presence": "PRESENT",
                            },
                        },
                    },
                    "postconditions": {
                        "slot_conditions": {
                            SLOT_S2: {
                                "value_presence": "ABSENT",
                            },
                        },
                    },
                },
                {
                    "preconditions": {
                        "slot_conditions": {
                            SLOT_S1: {
                                "value_presence": "ABSENT",
                            },
                        },
                    },
                    "postconditions": {
                        "slot_conditions": {
                            SLOT_S2: {
                                "value_presence": "PRESENT",
                            },
                        },
                    },
                },
            ],
        },
    }
    schema = validated_schema(
        test_value_presence_in_rules,
        f"MV{multivalued}",
        framework,
        classes=classes,
        core_elements=["preconditions", "postconditions", "slot_conditions", "value_presence"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework != JSON_SCHEMA:
        if not is_valid:
            expected_behavior = ValidationBehavior.INCOMPLETE
    if multivalued:
        instance = {k: [v] for k, v in instance.items()}
    check_data(
        schema,
        data_name,
        framework,
        instance,
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {instance}",
    )


@pytest.mark.parametrize(
    "name,quantification,expression,instance,is_valid",
    [
        ("all_members_min_10", "all_members", {"range": "integer", "minimum_value": 10}, [10, 11, 12], True),
        ("all_members_min_10", "all_members", {"range": "integer", "minimum_value": 10}, [9, 10], False),
        ("all_members_min_10", "all_members", {"range": "integer", "minimum_value": 10}, [9], False),
        ("all_members_min_10", "all_members", {"range": "integer", "minimum_value": 10}, [10], True),
        ("all_members_min_10", "all_members", {"range": "integer", "minimum_value": 10}, [], True),
        ("has_member_min_10", "has_member", {"range": "integer", "minimum_value": 10}, [10, 11, 12], True),
        ("has_member_min_10", "has_member", {"range": "integer", "minimum_value": 10}, [9, 10], True),
        ("has_member_min_10", "has_member", {"range": "integer", "minimum_value": 10}, [8, 9], False),
        ("has_member_min_10", "has_member", {"range": "integer", "minimum_value": 10}, [9], False),
        ("has_member_min_10", "has_member", {"range": "integer", "minimum_value": 10}, [10], True),
        ("has_member_min_10", "has_member", {"range": "integer", "minimum_value": 10}, [], False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_membership(framework, name, quantification, expression, instance, is_valid):
    """
    Tests behavior of membership.

    :param framework:
    :param name:
    :param quantification:
    :param expression:
    :param instance:
    :param is_valid:
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": "integer",
                    "multivalued": True,
                    quantification: expression,
                },
            },
        },
    }
    schema = validated_schema(
        test_membership,
        name,
        framework,
        classes=classes,
        core_elements=[quantification],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework not in [JSON_SCHEMA, OWL]:
        if not is_valid:
            expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == OWL and quantification == "has_member" and not is_valid:
        # OWL is open world, existential checks succeed without closure axioms
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        "_".join([str(x) for x in instance]),
        framework,
        {SLOT_S1: instance},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {instance}",
    )
