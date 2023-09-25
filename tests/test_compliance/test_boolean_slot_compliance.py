"""Constants for boolean slots tests (any_of, all_of, etc)."""

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
    CLASS_ANY,
    CLASS_C,
    CLASS_D,
    CLASS_U1,
    CLASS_U2,
    CORE_FRAMEWORKS,
    SLOT_S1,
    SLOT_S2,
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

    any_of is a special case as it cleanly maps to many language constructs (e.g. Union in Python),
    and it is often possible to normalize complex combinations to any_of form.

    :param framework:
    :param data_name:
    :param value:
    :param is_valid:
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
        f"DR{default_range}",
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

    :param framework:
    :param data_name:
    :param value:
    :param is_valid:
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

    :param framework:
    :param data_name:
    :param value:
    :param is_valid:
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

    :param framework:
    :param data_name:
    :param value:
    :param is_valid:
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
    "value",
    [1, 10, 15, 20, 21],
)
@pytest.mark.parametrize(
    "min_val,max_val",
    [(10, 20), (10, 10), (20, 10)],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_min_max(framework, min_val, max_val, value):
    """
    Tests behavior of minimum and maximum value.

    :param framework:
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
                    "_mappings": {
                        PYDANTIC: f"{SLOT_S1}: int = Field(..., ge={min_val}, le={max_val})",
                    },
                },
            },
        },
    }
    satisfiable = min_val <= max_val
    comments = []
    if not satisfiable:
        comments.append("not satisfiable min {min_val} > max {max_val}")
    schema = validated_schema(
        test_min_max,
        f"min{min_val}_max{max_val}",
        framework,
        classes=classes,
        core_elements=["minimum_value", "maximum_value", "range"],
        comments=comments,
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    is_valid = min_val <= value <= max_val
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

    :param framework:
    :param data_name:
    :param value:
    :param is_valid:
    :param use_default_range:
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
    if framework != JSON_SCHEMA:
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

    Uses a class with two slots, s1 and s2, where either s1 or s2 is set,
    but not both.

    :param framework:
    :param multivalued:
    :param data_name:
    :param instance:
    :param is_valid:
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
