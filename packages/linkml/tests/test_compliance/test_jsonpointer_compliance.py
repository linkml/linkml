import pytest

from tests.test_compliance.helper import (
    PANDERA_POLARS_CLASS,
    SHACL,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CORE_FRAMEWORKS, SLOT_ID


@pytest.mark.parametrize(
    "data_name,data,invalid_reason",
    [
        (
            "simple",
            {
                "id": "object1234",
                "source": [
                    {"property": "#/height", "provenance": "fooSource"},
                    {"property": "#/width", "provenance": "barSource"},
                    {"property": "#/address[0]", "provenance": "fizzSource"},
                    {"property": "#/address[1]", "provenance": "bazSource"},
                ],
                "height": 10.0,
                "width": 20.0,
                "address": ["120 Main St", "100 Second St"],
            },
            None,
        ),
        (
            "invalid_jsonpointer",
            {
                "id": "object1234",
                "source": [
                    {"property": "#/height", "provenance": "fooSource"},
                    {"property": "#/width", "provenance": "barSource"},
                    {"property": "#/address[0]", "provenance": "fizzSource"},
                    {"property": "#/address[1]", "provenance": "bazSource"},
                ],
                "height": 10.0,
                "width": 20.0,
                "address": ["120 Main St", "100 Second St"],
            },
            "pointer to a non-existent property",
        ),
        (
            "invalid_array_element",
            {
                "id": "object1234",
                "source": [
                    {"property": "#/height", "provenance": "fooSource"},
                    {"property": "#/width", "provenance": "barSource"},
                    {"property": "#/address[0]", "provenance": "fizzSource"},
                    {"property": "#/address[99]", "provenance": "bazSource"},
                ],
                "height": 10.0,
                "width": 20.0,
                "address": ["120 Main St", "100 Second St"],
            },
            "array out of bounds",
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_jsonpointer(framework, data_name, data, invalid_reason):
    """
    Tests behavior of json pointers.

    Note: this feature is under discussion
    and incompletely implemented. See:

    https://github.com/linkml/linkml/issues/1469

    :param framework: all should support built-in types
    :param data_name: id for data instance
    :param data: value to check
    :param invalid_reason: reason for invalidity (valid if None)
    :return:
    """
    if framework == SHACL:
        pytest.skip("TODO: handle @base in RDF translation")
    CLASS_SOURCE = "Source"
    classes = {
        CLASS_SOURCE: {
            "attributes": {
                "property": {
                    "range": "jsonpointer",
                },
                "provenance": {
                    "description": "Provenance of the assignment property points at",
                },
            }
        },
        CLASS_C: {
            "attributes": {
                SLOT_ID: {
                    "identifier": True,
                },
                "height": {
                    "range": "float",
                },
                "width": {
                    "range": "float",
                },
                "address": {
                    "multivalued": True,
                },
                "source": {
                    "description": "Key value to lookup source of S1/S2 assignment",
                    "range": CLASS_SOURCE,
                    "multivalued": True,
                },
            }
        },
    }
    schema = validated_schema(
        test_jsonpointer,
        "default",
        framework,
        classes=classes,
        core_elements=["jsonpointer"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework == PANDERA_POLARS_CLASS:
        expected_behavior = ValidationBehavior.INCOMPLETE
    is_valid = invalid_reason is None
    if not is_valid:
        # validation behavior is not yet implemented for ANY framework.
        # precise behavior is yet to be defined, but at a minimum
        # any jsonpointer should be valid syntax and should resolve
        # to a valid object within the json/tree form of the document.
        # TODO decide:
        #   - do we want to allow dangling pointers to reference a None assignment?
        #   - should only inlined references be traversed?
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        data,
        is_valid,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        description=data_name,
    )
