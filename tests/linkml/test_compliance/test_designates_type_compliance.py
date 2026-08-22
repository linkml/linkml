import pytest

from tests.linkml.test_compliance.helper import (
    JSON_SCHEMA,
    PANDERA_POLARS_CLASS,
    PYDANTIC,
    PYTHON_DATACLASSES,
    ValidationBehavior,
    check_data,
    feature_category,
    validated_schema,
)
from tests.linkml.test_compliance.test_compliance import (
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

ALTERNATE_NAMESPACE = "http://example.org/altns/"
CLASS_URI_CURIE = "curie"
CLASS_URI_REGISTERED_FULL = "registered_full"
CLASS_URI_TEMPLATES = {
    CLASS_URI_CURIE: "altns:{class_name}",
    CLASS_URI_REGISTERED_FULL: f"{ALTERNATE_NAMESPACE}{{class_name}}",
}


@feature_category("Identity & Keys", "Type designator")
@pytest.mark.parametrize(
    "description,type_range,object,is_valid,class_uri_mode,abstract_classes",
    [
        ("t0 type optional", "string", {}, True, None, []),
        ("t1", "string", {SLOT_TYPE: CLASS_C1a}, True, None, []),
        ("t1a", "string", {SLOT_TYPE: CLASS_C1a}, True, None, [CLASS_C1]),
        ("t1a2", "string", {SLOT_TYPE: CLASS_C1a}, False, None, [CLASS_C1, CLASS_C1a]),
        ("t2", "string", {SLOT_TYPE: "fake"}, False, None, []),
        ("t2 generic A", "string", {SLOT_TYPE: CLASS_C1, SLOT_S1a: "..."}, False, None, []),
        ("t2 generic B", "string", {SLOT_TYPE: CLASS_C1, SLOT_S1b: "..."}, False, None, []),
        ("t3", "string", {SLOT_TYPE: CLASS_C1a, SLOT_S1a: "..."}, True, None, []),
        ("t3b", "string", {SLOT_TYPE: CLASS_C1a1, SLOT_S1a: "..."}, True, None, []),
        ("t4", "string", {SLOT_TYPE: CLASS_C1a, SLOT_S1b: "..."}, False, None, []),
        ("t5", "string", {SLOT_TYPE: CLASS_C1b, SLOT_S1b: "..."}, True, None, []),
        ("t6 native CURIE", "uriorcurie", {SLOT_TYPE: f"ex:{CLASS_C1a}"}, True, None, []),
        pytest.param(
            "t6 CURIE-declared assigned CURIE",
            "uriorcurie",
            {SLOT_TYPE: f"altns:{CLASS_C1a}", SLOT_S1a: "..."},
            True,
            CLASS_URI_CURIE,
            [],
            id="uriorcurie_curie_declared_curie",
        ),
        pytest.param(
            "t6 CURIE-declared assigned full URI",
            "uriorcurie",
            {SLOT_TYPE: f"{ALTERNATE_NAMESPACE}{CLASS_C1a}", SLOT_S1a: "..."},
            True,
            CLASS_URI_CURIE,
            [],
            id="uriorcurie_curie_declared_full_uri",
        ),
        pytest.param(
            "t6 assigned CURIE",
            "uriorcurie",
            {SLOT_TYPE: f"altns:{CLASS_C1a}", SLOT_S1a: "..."},
            True,
            CLASS_URI_REGISTERED_FULL,
            [],
            id="uriorcurie_assigned_curie",
        ),
        pytest.param(
            "t6 assigned full URI",
            "uriorcurie",
            {SLOT_TYPE: f"{ALTERNATE_NAMESPACE}{CLASS_C1a}", SLOT_S1a: "..."},
            True,
            CLASS_URI_REGISTERED_FULL,
            [],
            id="uriorcurie_assigned_full_uri",
        ),
        pytest.param(
            "t6 unknown CURIE",
            "uriorcurie",
            {SLOT_TYPE: "altns:Unknown", SLOT_S1a: "..."},
            False,
            CLASS_URI_REGISTERED_FULL,
            [],
            id="uriorcurie_unknown_curie",
        ),
        pytest.param(
            "t6 unknown URI",
            "uriorcurie",
            {SLOT_TYPE: f"{ALTERNATE_NAMESPACE}Unknown", SLOT_S1a: "..."},
            False,
            CLASS_URI_REGISTERED_FULL,
            [],
            id="uriorcurie_unknown_uri",
        ),
        pytest.param(
            "t6 out-of-hierarchy CURIE",
            "uriorcurie",
            {SLOT_TYPE: f"altns:{CLASS_CONTAINER}", SLOT_S1a: "..."},
            False,
            CLASS_URI_REGISTERED_FULL,
            [],
            id="uriorcurie_outside_curie",
        ),
        pytest.param(
            "t6 out-of-hierarchy URI",
            "uriorcurie",
            {SLOT_TYPE: f"{ALTERNATE_NAMESPACE}{CLASS_CONTAINER}", SLOT_S1a: "..."},
            False,
            CLASS_URI_REGISTERED_FULL,
            [],
            id="uriorcurie_outside_uri",
        ),
        ("t7 native URI", "uri", {SLOT_TYPE: f"http://example.org/{CLASS_C1a}"}, True, None, []),
        (
            "t7 assigned URI",
            "uri",
            {SLOT_TYPE: f"{ALTERNATE_NAMESPACE}{CLASS_C1a}"},
            True,
            CLASS_URI_CURIE,
            [],
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_designates_type(framework, description, type_range, object, is_valid, class_uri_mode, abstract_classes):
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
    :param class_uri_mode: how to use class_uri to override the type
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
                            f'{SLOT_TYPE}: Literal["{CLASS_C1}"] = Field(default="{CLASS_C1}"'
                            if type_range == "string"
                            else ""
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
    if class_uri_mode:
        class_uri_template = CLASS_URI_TEMPLATES[class_uri_mode]
        for cn, cls in classes.items():
            cls["class_uri"] = class_uri_template.format(class_name=cn)
    if framework == PANDERA_POLARS_CLASS:
        pytest.skip("PanderaGen class ranges are not implemented")
    schema = validated_schema(
        test_designates_type,
        f"R{type_range}_classuri{class_uri_mode or 'default'}_ab{'_'.join(abstract_classes)}",
        framework,
        classes=classes,
        prefixes={
            "altns": ALTERNATE_NAMESPACE,
        },
        core_elements=["designates_type"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework != PYDANTIC and framework != JSON_SCHEMA and framework != PYTHON_DATACLASSES:
        expected_behavior = ValidationBehavior.INCOMPLETE
    if class_uri_mode and framework == PYDANTIC:
        # Pydantic support for assigned class URIs remains incomplete.
        expected_behavior = ValidationBehavior.INCOMPLETE
    if class_uri_mode and framework == PYTHON_DATACLASSES and type_range != "uriorcurie":
        # Dataclasses still lack assigned uri-range support.
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
