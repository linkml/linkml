import pytest

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    PYDANTIC,
    PYTHON_DATACLASSES,
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
    CLASS_C1a1,
    CLASS_C1b,
    SLOT_S1a,
    SLOT_S1b,
)


@pytest.mark.parametrize(
    "description,type_range,object,is_valid,override_uri,abstract_classes",
    [
        ("t0 type optional", "string", {}, True, False, []),
        ("t1", "string", {SLOT_TYPE: CLASS_C1a}, True, False, []),
        ("t1a", "string", {SLOT_TYPE: CLASS_C1a}, True, False, [CLASS_C1]),
        ("t1a2", "string", {SLOT_TYPE: CLASS_C1a}, False, False, [CLASS_C1, CLASS_C1a]),
        ("t2", "string", {SLOT_TYPE: "fake"}, False, False, []),
        ("t2 generic A", "string", {SLOT_TYPE: CLASS_C1, SLOT_S1a: "..."}, False, False, []),
        ("t2 generic B", "string", {SLOT_TYPE: CLASS_C1, SLOT_S1b: "..."}, False, False, []),
        ("t3", "string", {SLOT_TYPE: CLASS_C1a, SLOT_S1a: "..."}, True, False, []),
        ("t3b", "string", {SLOT_TYPE: CLASS_C1a1, SLOT_S1a: "..."}, True, False, []),
        ("t4", "string", {SLOT_TYPE: CLASS_C1a, SLOT_S1b: "..."}, False, False, []),
        ("t5", "string", {SLOT_TYPE: CLASS_C1b, SLOT_S1b: "..."}, True, False, []),
        ("t6", "uriorcurie", {SLOT_TYPE: f"ex:{CLASS_C1a}"}, True, False, []),
        ("t6", "uriorcurie", {SLOT_TYPE: f"altns:{CLASS_C1a}"}, True, True, []),
        ("t7", "uri", {SLOT_TYPE: f"http://example.org/{CLASS_C1a}"}, True, False, []),
        ("t7", "uri", {SLOT_TYPE: f"http://example.org/altns/{CLASS_C1a}"}, True, True, []),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_designates_type(framework, description, type_range, object, is_valid, override_uri, abstract_classes):
    """
    Tests behavior of designates_type.

    This creates a schema consisting of a *container* class that has a multivalued slot *entities*,
    with a range of C1. C1 has a slot *type* that designates the type of the entity.  C1a and C1b
    are subclasses of C1.

    C1a has a slot S1a, C1b has a slot S1b.

    The schema is tested against different data objects with different combinations of these slots
    set.

    The data is only valid if the slots are specified for the correct type.

    :param framework: generator to test
    :param description: name of test data object
    :param type_range: range of the type designator slot (e.g. string, uriorcurie)
    :param object: data instance to test
    :param is_valid: whether the data is valid
    :param override_uri: whether to use class_uri to override the type
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
                        PYDANTIC: (
                            f'{SLOT_TYPE}: Literal["{CLASS_C1}"] = Field("{CLASS_C1}"' if type_range == "string" else ""
                        ),
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
        CLASS_C1a1: {
            "is_a": CLASS_C1a,
        },
    }
    for c in abstract_classes:
        classes[c]["abstract"] = True
    if override_uri:
        for cn, cls in classes.items():
            cls["class_uri"] = f"altns:{cn}"
    schema = validated_schema(
        test_designates_type,
        f"R{type_range}_override{override_uri}_ab{'_'.join(abstract_classes)}",
        framework,
        classes=classes,
        prefixes={
            "altns": "http://example.org/altns/",
        },
        core_elements=["designates_type"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework != PYDANTIC and framework != JSON_SCHEMA and framework != PYTHON_DATACLASSES:
        expected_behavior = ValidationBehavior.INCOMPLETE
    if override_uri and framework in [PYDANTIC, PYTHON_DATACLASSES]:
        # Pydantic and dataclasses don't support using class_uri to override the type
        expected_behavior = ValidationBehavior.INCOMPLETE
    if description == "t1a2":
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
        exclude_rdf=True,  # TODO
    )
