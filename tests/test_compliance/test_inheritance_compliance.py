"""Tests involving inheritance (is_a) and related constructs."""

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
    CLASS_C1,
    CLASS_C2,
    CLASS_D,
    CLASS_D1,
    CLASS_MC1,
    CLASS_MC2,
    CLASS_X,
    CLASS_Y,
    CLASS_Z,
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
                "s1": {"type": ["string", "null"]},
                "s2": {"type": ["string", "null"]},
            },
            "title": "C",
            "type": "object",
        },
    }
    if not parent_is_abstract:
        json_schema_defs["D"] = {
            "additionalProperties": False,
            "description": "",
            "properties": {"s1": {"type": ["string", "null"]}},
            "title": "D",
            "type": "object",
        }
    classes = {
        CLASS_D: {
            "abstract": parent_is_abstract,
            "attributes": {
                SLOT_S1: {
                    "_mappings": {
                        PYDANTIC: "s1: Optional[str] = Field(None",
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
                PYTHON_DATACLASSES: "@dataclass(repr=False)\nclass C(D):",
                JSON_SCHEMA: {"$defs": json_schema_defs},
            },
        },
    }
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if cls == CLASS_D and parent_is_abstract:
        is_valid = False
        if framework in [PYDANTIC, PYTHON_DATACLASSES, SQL_DDL_SQLITE, OWL, SHACL]:
            # currently lax about instantiating abstract classes
            expected_behavior = ValidationBehavior.INCOMPLETE
    schema = validated_schema(
        test_basic_class_inheritance,
        f"ABS{parent_is_abstract}",
        framework,
        classes=classes,
        core_elements=["is_a", "abstract"],
    )
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

    This sets sets up a schema with class C with slot s3, which mixes in MC1.s1 and MC2.s3

    This schema is tested with various objects that attempt to instantiate one of these classes.

    Note that the only framework to prohibit instantiating mixins is JSONSchema; the mixin
    classes are entirely rolled down.

    Currently in dataclasses, the mixins are rolled down, but in the pydantic we allow
    multiple inheritance

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
                "s1": {"type": ["string", "null"]},
                "s2": {"type": ["string", "null"]},
                "s3": {"type": ["string", "null"]},
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
                        PYDANTIC: "s1: Optional[str] = Field(None",
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
                PYTHON_DATACLASSES: "@dataclass(repr=False)\nclass C(YAMLRoot):",  # DC rolls up
                JSON_SCHEMA: json_schema_defs,
            },
        },
        CLASS_D: {
            "attributes": {
                SLOT_S4: {
                    "range": CLASS_ANY,
                    "any_of": [
                        {"range": CLASS_MC1},
                        {"range": CLASS_MC2},
                    ],
                }
            }
        },
        CLASS_ANY: {
            "class_uri": "linkml:Any",
        },
    }
    schema = validated_schema(test_mixins, "default", framework, classes=classes, core_elements=["mixins", "mixin"])
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if cls != CLASS_C:
        if framework in [PYDANTIC, PYTHON_DATACLASSES, SQL_DDL_SQLITE, OWL, SHACL]:
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
            "basic slot usage, slots are inherited",
            CLASS_X,
            {
                SLOT_S2: 5,
                SLOT_S3: 5,
            },
            True,
        ),
        (
            "basic slot usage, slots not inherited upwards",
            CLASS_Y,
            {
                SLOT_S3: 5,
            },
            False,
        ),
        (
            "slot_usage is inherited",
            CLASS_C,
            {
                SLOT_S1: {
                    SLOT_S3: 5,
                },
            },
            True,
        ),
        (
            "minimum_value inheritance",
            CLASS_C,
            {
                SLOT_S1: {
                    SLOT_S2: 1,
                },
            },
            False,
        ),
        (
            "slot_usage is not inherited upwards",
            CLASS_D,
            {
                SLOT_S1: {
                    SLOT_S3: 5,
                },
            },
            False,
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_slot_usage(framework, description, cls: str, object, is_valid):
    """
    Tests slot usage inheritance.

    * C is_a D, and refines range of s1 from Y to X
    * X is_a Y

    :param framework:
    :param description:
    :param object:
    :param is_valid:
    :return:
    """
    slots = {
        SLOT_S1: {
            "description": "Example of a slot with class (X/Y/Z) as a range",
            "range": CLASS_Z,
        },
        SLOT_S2: {
            "description": "A slot on X with a type (integer) range",
            "range": "integer",
        },
        SLOT_S3: {
            "description": "A slot on Y with a type (integer) range",
            "range": "integer",
        },
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
        CLASS_Z: {
            "abstract": True,
        },
        CLASS_Y: {
            "slots": [SLOT_S2],
            "is_a": CLASS_Z,
            "slot_usage": {
                SLOT_S2: {
                    "minimum_value": 0,
                },
            },
        },
        CLASS_X: {
            "slots": [SLOT_S3],
            "is_a": CLASS_Y,
            "slot_usage": {
                SLOT_S2: {
                    "minimum_value": 5,
                },
                SLOT_S3: {
                    "minimum_value": 0,
                },
            },
        },
    }
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if description == "minimum_value inheritance":
        if framework in [PYTHON_DATACLASSES, SQL_DDL_SQLITE, SHACL]:
            expected_behavior = ValidationBehavior.INCOMPLETE
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
        expected_behavior=expected_behavior,
        target_class=cls,
        description="pattern",
    )


@pytest.mark.parametrize(
    "description,schema_name,default_range,s1def,s2def,cls,object,is_valid",
    [
        ("object may be empty", "rX", "string", {"range": CLASS_X}, {}, CLASS_C, {}, True),
        ("inherits basic type", "rINT", CLASS_ANY, {"range": "integer"}, {}, CLASS_C, {SLOT_S2: 5}, True),
        ("inherits Any type 1", "rANY", "string", {"range": CLASS_ANY}, {}, CLASS_C, {SLOT_S2: 5}, True),
        ("inherits Any type 2", "rANY", "string", {"range": CLASS_ANY}, {}, CLASS_C, {SLOT_S2: {SLOT_S3: "..."}}, True),
        ("inherits constraints", "rMAX", "integer", {"maximum_value": 10}, {}, CLASS_C, {SLOT_S2: 5}, True),
        ("inherits constraints invalid", "rMAX", "integer", {"maximum_value": 10}, {}, CLASS_C, {SLOT_S2: 15}, False),
        (
            "slots are inherited",
            "rX",
            "string",
            {"range": CLASS_X},
            {},
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
            "rX",
            "string",
            {"range": CLASS_X},
            {},
            CLASS_C,
            {
                SLOT_S2: EXAMPLE_STRING_VALUE_2,
            },
            False,
        ),
    ],
)
@pytest.mark.parametrize("mixins", [False, True])
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_basic_slot_inheritance(
    framework,
    mixins,
    description,
    schema_name,
    default_range,
    s1def,
    s2def,
    cls: str,
    object,
    is_valid,
):
    """
    Tests behavior of is_a in slot hierarchies.

    This sets up a simple slot hierarchy where S2 inherits from S1

    :param framework:
    :param description:
    :param schema_name:
    :param cls:
    :param object:
    :param is_valid:
    :return:
    """
    slots = {
        SLOT_S1: s1def,
        SLOT_S2: s2def,
    }
    if mixins:
        slots[SLOT_S2]["mixins"] = [SLOT_S1]
    else:
        slots[SLOT_S2]["is_a"] = SLOT_S1
    classes = {
        CLASS_ANY: {
            "class_uri": "linkml:Any",
        },
        CLASS_X: {
            "attributes": {
                SLOT_S3: {
                    "required": True,
                    "range": "string",
                },
            }
        },
        CLASS_C: {
            "slots": [SLOT_S2],
        },
    }

    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework in [PYTHON_DATACLASSES, SQL_DDL_SQLITE]:
        if schema_name == "rMAX":
            # range constraints are not enforced in these frameworks
            expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == SQL_DDL_SQLITE and schema_name == "rANY":
        pytest.skip("TODO: inconsistencies in SQLA generation")
    schema = validated_schema(
        test_basic_slot_inheritance,
        f"mixins{mixins}_{schema_name}",
        framework,
        default_range=default_range,
        classes=classes,
        slots=slots,
        core_elements=["is_a", "slots"],
    )
    exclude_rdf = schema_name in ["rANY"]
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        object,
        is_valid,
        exclude_rdf=exclude_rdf,
        expected_behavior=expected_behavior,
        target_class=cls,
        description=description,
    )


@pytest.mark.parametrize(
    "obj,target_class,valid",
    [
        (
            {
                SLOT_S3: {
                    SLOT_S1: "foo",
                    SLOT_S2: 5,
                },
            },
            CLASS_D1,
            True,
        ),
        (
            {
                SLOT_S1: "foo",
            },
            CLASS_C,
            False,
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_abstract_classes(
    framework,
    obj,
    target_class,
    valid,
):
    """
    Tests behavior of abstract classes.

    Currently the only framework to forbid instantiation of abstract classes in JSON-Schema

    :param framework:
    :return:
    """
    abstract_classes = [CLASS_C, CLASS_D]
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "required": True,
                    "range": "string",
                },
            }
        },
        CLASS_C1: {
            "is_a": CLASS_C,
            "attributes": {
                SLOT_S2: {
                    "required": True,
                    "range": "integer",
                }
            },
        },
        CLASS_C2: {
            "is_a": CLASS_C,
        },
        CLASS_D: {
            "attributes": {
                SLOT_S3: {
                    "range": CLASS_C,
                }
            }
        },
        CLASS_D1: {
            "attributes": {
                SLOT_S3: {
                    "range": CLASS_C1,
                }
            }
        },
    }
    for c in abstract_classes:
        classes[c]["abstract"] = True
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if not valid and target_class in abstract_classes:
        if framework != JSON_SCHEMA:
            expected_behavior = ValidationBehavior.INCOMPLETE
    schema = validated_schema(
        test_abstract_classes,
        f"abstract_{'_'.join(abstract_classes)}",
        framework,
        classes=classes,
        core_elements=["is_a", "abstract"],
    )
    check_data(
        schema,
        "test",
        framework,
        obj,
        valid,
        expected_behavior=expected_behavior,
        target_class=target_class,
        description="default",
    )
