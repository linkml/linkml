"""Tests involving inheritance (is_a) and related constructs."""
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
    CLASS_C,
    CLASS_D,
    CLASS_MC1,
    CLASS_MC2,
    CLASS_X,
    CLASS_Y,
    CORE_FRAMEWORKS,
    EXAMPLE_STRING_VALUE_1,
    EXAMPLE_STRING_VALUE_2,
    EXAMPLE_STRING_VALUE_3,
    EXAMPLE_STRING_VALUE_4,
    SLOT_S1,
    SLOT_S2,
    SLOT_S3,
    SLOT_S4,
)


@pytest.mark.parametrize("parent_is_abstract", [False, True])
@pytest.mark.parametrize(
    "description,cls,object,is_valid",
    [
        ("object may be empty", CLASS_C, {}, True),
        (
            "not all attributes need to be specified",
            CLASS_C,
            {
                SLOT_S1: EXAMPLE_STRING_VALUE_1,
            },
            True,
        ),
        (
            "all attributes can be specified",
            CLASS_C,
            {
                SLOT_S1: EXAMPLE_STRING_VALUE_1,
                SLOT_S2: EXAMPLE_STRING_VALUE_2,
            },
            True,
        ),
        (
            "attributes not in the class are not allowed",
            CLASS_C,
            {
                SLOT_S1: EXAMPLE_STRING_VALUE_1,
                SLOT_S2: EXAMPLE_STRING_VALUE_2,
                SLOT_S3: EXAMPLE_STRING_VALUE_3,
            },
            False,
        ),
        (
            "instantiate parent",
            CLASS_D,
            {
                SLOT_S1: EXAMPLE_STRING_VALUE_1,
            },
            True,
        ),
        (
            "cannot inherit from children",
            CLASS_D,
            {
                SLOT_S1: EXAMPLE_STRING_VALUE_1,
                SLOT_S2: EXAMPLE_STRING_VALUE_2,
            },
            False,
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_basic_class_inheritance(framework, description, cls: str, object, is_valid, parent_is_abstract):
    """
    Tests behavior is_a in class hierarchies.

    :param framework:
    :param description:
    :param object:
    :param is_valid:
    :param parent_is_abstract:
    :return:
    """
    json_schema_defs = {
        "C": {
            "additionalProperties": False,
            "description": "",
            "properties": {
                "s1": {"type": "string"},
                "s2": {"type": "string"},
            },
            "title": "C",
            "type": "object",
        },
    }
    if not parent_is_abstract:
        json_schema_defs["D"] = {
            "additionalProperties": False,
            "description": "",
            "properties": {"s1": {"type": "string"}},
            "title": "D",
            "type": "object",
        }
    classes = {
        CLASS_D: {
            "abstract": parent_is_abstract,
            "attributes": {
                SLOT_S1: {
                    "_mappings": {
                        PYDANTIC: "s1: Optional[str] = Field(None)",
                        PYTHON_DATACLASSES: "s1: Optional[str] = None",
                    }
                },
            },
        },
        CLASS_C: {
            "is_a": CLASS_D,
            "attributes": {
                SLOT_S2: {},
            },
            "_mappings": {
                PYDANTIC: "class C(D):",
                PYTHON_DATACLASSES: "@dataclass\nclass C(D):",
                JSON_SCHEMA: {"$defs": json_schema_defs},
            },
        },
    }
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if cls == CLASS_D and parent_is_abstract:
        is_valid = False
        if framework in [PYDANTIC, PYTHON_DATACLASSES, SQL_DDL_SQLITE, OWL]:
            # currently lax about instantiating abstract classes
            expected_behavior = ValidationBehavior.INCOMPLETE
    schema = validated_schema(test_basic_class_inheritance, f"ABS{parent_is_abstract}", framework, classes=classes)
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        object,
        is_valid,
        expected_behavior=expected_behavior,
        target_class=cls,
        description="pattern",
    )


@pytest.mark.parametrize(
    "description,cls,object,is_valid",
    [
        ("object may be empty", CLASS_C, {}, True),
        (
            "not all attributes need to be specified",
            CLASS_C,
            {
                SLOT_S3: EXAMPLE_STRING_VALUE_1,
            },
            True,
        ),
        (
            "mixin parent attributes can be specified",
            CLASS_C,
            {
                SLOT_S1: EXAMPLE_STRING_VALUE_1,
                SLOT_S2: EXAMPLE_STRING_VALUE_2,
            },
            True,
        ),
        (
            "attributes not in the class are not allowed",
            CLASS_C,
            {
                SLOT_S1: EXAMPLE_STRING_VALUE_1,
                SLOT_S2: EXAMPLE_STRING_VALUE_2,
                SLOT_S3: EXAMPLE_STRING_VALUE_3,
                SLOT_S4: EXAMPLE_STRING_VALUE_4,
            },
            False,
        ),
        (
            "instantiating mixin parent forbidden",
            CLASS_MC1,
            {
                SLOT_S1: EXAMPLE_STRING_VALUE_1,
            },
            False,
        ),
        (
            "cannot inherit from children",
            CLASS_MC1,
            {
                SLOT_S1: EXAMPLE_STRING_VALUE_1,
                SLOT_S3: EXAMPLE_STRING_VALUE_2,
            },
            False,
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_mixins(framework, description, cls, object, is_valid):
    """
    Tests behavior of mixins.

    :param framework:
    :param description:
    :param object:
    :param is_valid:
    :return:
    """
    json_schema_defs = {
        "C": {
            "additionalProperties": False,
            "description": "",
            "properties": {
                "s1": {"type": "string"},
                "s2": {"type": "string"},
                "s3": {"type": "string"},
            },
            "title": "C",
            "type": "object",
        },
    }
    classes = {
        CLASS_MC1: {
            "mixin": True,
            "attributes": {
                SLOT_S1: {
                    "_mappings": {
                        PYDANTIC: "s1: Optional[str] = Field(None)",
                        PYTHON_DATACLASSES: "s1: Optional[str] = None",
                    }
                },
            },
        },
        CLASS_MC2: {
            "mixin": True,
            "attributes": {
                SLOT_S2: {},
            },
        },
        CLASS_C: {
            "mixins": [CLASS_MC1, CLASS_MC2],
            "attributes": {
                SLOT_S3: {},
            },
            "_mappings": {
                PYDANTIC: "class C(MC2, MC1):",
                PYTHON_DATACLASSES: "@dataclass\nclass C(YAMLRoot):",  # DC rolls up
                JSON_SCHEMA: {"$defs": json_schema_defs},
            },
        },
    }
    schema = validated_schema(test_mixins, "default", framework, classes=classes)
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if cls != CLASS_C:
        if framework in [PYDANTIC, PYTHON_DATACLASSES, SQL_DDL_SQLITE, OWL]:
            # currently lax about prohibiting instantiating mixins
            expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        object,
        is_valid,
        expected_behavior=expected_behavior,
        target_class=cls,
        description="pattern",
    )


@pytest.mark.parametrize(
    "description,cls,object,is_valid",
    [
        (
            "attribute ranges are refined",
            CLASS_C,
            {
                SLOT_S1: {
                    SLOT_S3: EXAMPLE_STRING_VALUE_3,
                },
            },
            True,
        ),
        (
            "attribute ranges are not inherited upwards",
            CLASS_D,
            {
                SLOT_S1: {
                    SLOT_S3: EXAMPLE_STRING_VALUE_3,
                },
            },
            False,
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_refine_attributes(framework, description, cls, object, is_valid):
    """
    Tests refining of attributes via is_a.

    This test is analogous to test_slot_usage

    :param framework:
    :param description:
    :param object:
    :param is_valid:
    :return:
    """
    classes = {
        CLASS_D: {
            "attributes": {
                SLOT_S1: {
                    "range": CLASS_Y,
                },
            },
        },
        CLASS_C: {
            "is_a": CLASS_D,
            "attributes": {
                SLOT_S1: {
                    "range": CLASS_X,
                },
            },
        },
        CLASS_Y: {
            "attributes": {
                SLOT_S2: {},
            },
        },
        CLASS_X: {
            "is_a": CLASS_Y,
            "attributes": {
                SLOT_S3: {},
            },
        },
    }
    schema = validated_schema(
        test_refine_attributes,
        "default",
        framework,
        classes=classes,
        core_elements=["is_a", "attributes"],
    )
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        object,
        is_valid,
        target_class=cls,
        description="pattern",
    )


@pytest.mark.parametrize(
    "description,cls,object,is_valid",
    [
        (
            "slot_usage is inherited",
            CLASS_C,
            {
                SLOT_S1: {
                    SLOT_S3: EXAMPLE_STRING_VALUE_3,
                },
            },
            True,
        ),
        (
            "slot_usage is not inherited upwards",
            CLASS_D,
            {
                SLOT_S1: {
                    SLOT_S3: EXAMPLE_STRING_VALUE_3,
                },
            },
            False,
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_slot_usage(framework, description, cls, object, is_valid):
    """
    Tests slot usage inheritance.

    * C is_a D, and refines s1 from Y to X
    * X is_a Y

    :param framework:
    :param description:
    :param object:
    :param is_valid:
    :return:
    """
    slots = {
        SLOT_S1: {},
        SLOT_S2: {},
        SLOT_S3: {},
    }
    classes = {
        CLASS_D: {
            "slots": [SLOT_S1],
            "slot_usage": {
                SLOT_S1: {
                    "range": CLASS_Y,
                },
            },
        },
        CLASS_C: {
            "is_a": CLASS_D,
            "slot_usage": {
                SLOT_S1: {
                    "range": CLASS_X,
                },
            },
        },
        CLASS_Y: {
            "slots": [SLOT_S2],
            "slot_usage": {
                SLOT_S2: {},
            },
        },
        CLASS_X: {
            "slots": [SLOT_S3],
            "is_a": CLASS_Y,
            "slot_usage": {
                SLOT_S3: {},
            },
        },
    }
    schema = validated_schema(
        test_slot_usage,
        "default",
        framework,
        classes=classes,
        slots=slots,
        core_elements=["slot_usage", "is_a"],
    )
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        object,
        is_valid,
        target_class=cls,
        description="pattern",
    )


@pytest.mark.parametrize(
    "description,cls,object,is_valid",
    [
        ("object may be empty", CLASS_C, {}, True),
        (
            "slots are inherited",
            CLASS_C,
            {
                SLOT_S2: {
                    SLOT_S3: EXAMPLE_STRING_VALUE_3,
                },
            },
            True,
        ),
        (
            "slots are inherited2",
            CLASS_C,
            {
                SLOT_S2: EXAMPLE_STRING_VALUE_2,
            },
            False,
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_basic_slot_inheritance(
    framework,
    description,
    cls: str,
    object,
    is_valid,
):
    """
    Tests behavior of is_a in slot hierarchies.

    :param framework:
    :param description:
    :param object:
    :param is_valid:
    :return:
    """
    slots = {
        SLOT_S1: {"range": CLASS_X},
        SLOT_S2: {
            "is_a": SLOT_S1,
        },
    }
    classes = {
        CLASS_X: {
            "attributes": {
                SLOT_S3: {
                    "required": True,
                },
            }
        },
        CLASS_C: {
            "slots": [SLOT_S2],
        },
    }

    expected_behavior = ValidationBehavior.IMPLEMENTS
    schema = validated_schema(
        test_basic_slot_inheritance,
        "default",
        framework,
        classes=classes,
        slots=slots,
        core_elements=["is_a", "slots"],
    )
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        object,
        is_valid,
        expected_behavior=expected_behavior,
        target_class=cls,
        description=description,
    )
