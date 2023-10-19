"""Constants for boolean slots tests (any_of, all_of, etc)."""
from typing import Optional

import pytest

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    OWL,
    PYDANTIC,
    PYTHON_DATACLASSES,
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
    SLOT_S1,
    SLOT_S2,
    CLASS_C1a,
    CLASS_C1b,
    SLOT_S1a,
    SLOT_S1b,
)


@pytest.mark.parametrize("use_default_range", [False, True])
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
def test_any_of(framework, data_name, value, is_valid, use_default_range):
    """
    Tests behavior of any_of.

    This test creates a test schema with a slot S1 whose values
    are either an integer or an inlined instance of class D.

    any_of is a special case of boolean metaslot,
    as it cleanly maps to many language constructs (e.g. Union in Python),
    and it is often possible to normalize complex combinations to any_of form.

    :param framework: generator to test
    :param data_name: unique identifier for the test data instance
    :param value: data value to use in the instance
    :param is_valid: whether the test instance is expected to be valid
    :param use_default_range: if True, the default range will be included in addition to any_of.
    :return:
    """
    expected_json_schema = {
        "s1": {
            # "$ref": "#/$defs/Any",
            "anyOf": [{"$ref": "#/$defs/D"}, {"type": "integer"}]
        }
    }
    if use_default_range:
        # Note: this is redundant and may be removed in the future
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
        classes[CLASS_ANY] = {
            "class_uri": "linkml:Any",
        }
        classes[CLASS_C]["attributes"][SLOT_S1]["range"] = CLASS_ANY
    else:
        default_range = None
    schema = validated_schema(
        test_any_of,
        f"DefaultRangeEQ_{default_range}",
        framework,
        classes=classes,
        default_range=default_range,
        core_elements=["any_of", "range"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework in [PYTHON_DATACLASSES, SQL_DDL_SQLITE]:
        expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == JSON_SCHEMA and use_default_range:
        expected_behavior = ValidationBehavior.INCOMPLETE
    # TODO: rdflib transformer has issues around ranges
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
def test_exactly_one_of(framework, data_name, value, is_valid):
    """
    Tests behavior of exactly_one_of.

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
        test_exactly_one_of,
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
def test_all_of(framework, data_name, value, is_valid):
    """
    Tests behavior of all_of.

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
        test_all_of,
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
def test_none_of(framework, data_name, value, is_valid):
    """
    Tests behavior of none_of.

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
        test_none_of,
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
@pytest.mark.skip("requires metamodel changes")
def test_cardinality_in_exactly_one_of(framework, data_name, instance, is_valid):
    """
    Tests intersection of cardinality and exactly_one_of.

    TODO: unskip this test when metamodel allows attributes or slot usage on anon expressions.

    :param framework:
    :param data_name:
    :param instance:
    :param is_valid:
    :return:
    """
    classes = {
        CLASS_C: {
            "exactly_one_of": [
                {
                    "attributes": {
                        SLOT_S1: {
                            "required": True,
                        },
                    },
                },
                {
                    "attributes": {
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
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework != JSON_SCHEMA:
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
    :param value: data value to use in the instance
    :param is_valid: whether the test instance is expected to be valid
    :param use_default_range: if True, the default range will be included in addition to any_of.
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
                        PYDANTIC: f"{SLOT_S1}: int = Field(..., ge={min_val}, le={max_val})"
                        if not equals_number
                        else ""
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
    :param data_name: name of data to test with
    :param value: value of slot in data to test with
    :param is_valid: whether the data is valid or not
    :return:
    """
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
    :param data_name: name of data to test with
    :param value: value of slot in data to test with
    :param is_valid: whether the data is valid or not
    :return:
    """
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
