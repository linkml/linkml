import pytest

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    PYDANTIC,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import (
    CLASS_C1,
    CLASS_CONTAINER,
    CORE_FRAMEWORKS,
    SLOT_TYPE,
    CLASS_C1a,
    CLASS_C1b,
    SLOT_S1a,
    SLOT_S1b,
)


@pytest.mark.parametrize(
    "description,type_range,object,is_valid",
    [
        ("t0 type optional", "string", {}, True),
        ("t1", "string", {SLOT_TYPE: CLASS_C1a}, True),
        ("t2", "string", {SLOT_TYPE: "fake"}, False),
        ("t3", "string", {SLOT_TYPE: CLASS_C1a, SLOT_S1a: "..."}, True),
        ("t4", "string", {SLOT_TYPE: CLASS_C1a, SLOT_S1b: "..."}, False),
        ("t5", "string", {SLOT_TYPE: CLASS_C1b, SLOT_S1b: "..."}, True),
        ("t6", "uriorcurie", {SLOT_TYPE: f"ex:{CLASS_C1a}"}, True),
        ("t7", "uri", {SLOT_TYPE: f"http://example.org/{CLASS_C1a}"}, True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_designates_type(framework, description, type_range, object, is_valid):
    """
    Tests behavior of designates_type.

    :param framework:
    :param description:
    :param type_range:
    :param object:
    :param is_valid:
    :return:
    """
    classes = {
        CLASS_CONTAINER: {
            "tree_root": True,
            "attributes": {
                "entities": {
                    "multivalued": True,
                    "range": CLASS_C1,
                    "inlined": True,
                },
            },
        },
        CLASS_C1: {
            "attributes": {
                SLOT_TYPE: {
                    "designates_type": True,
                    "range": type_range,
                    "_mappings": {
                        PYDANTIC: f'{SLOT_TYPE}: Literal["{CLASS_C1}"] = Field("{CLASS_C1}")'
                        if type_range == "string"
                        else "",
                    },
                },
            },
        },
        CLASS_C1a: {
            "is_a": CLASS_C1,
            "attributes": {
                SLOT_S1a: {},
            },
        },
        CLASS_C1b: {
            "is_a": CLASS_C1,
            "attributes": {
                SLOT_S1b: {},
            },
        },
    }
    schema = validated_schema(
        test_designates_type,
        f"R{type_range}",
        framework,
        classes=classes,
        core_elements=["designates_type"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework != PYDANTIC and framework != JSON_SCHEMA:
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        {"entities": [object]},
        is_valid,
        target_class=CLASS_CONTAINER,
        expected_behavior=expected_behavior,
        description=description,
        exclude_rdf=True, # TODO
    )
