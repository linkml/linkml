"""
Tests involving metadata.

These typically do not include meaningful instance tests since metadata does not affect behavior.

- TODO: license slot
"""
import pytest

from tests.test_compliance.helper import (
    PYDANTIC,
    PYTHON_DATACLASSES,
    SQL_DDL_POSTGRES,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CORE_FRAMEWORKS, SLOT_S1


@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_descriptions(framework):
    """
    Tests behavior of description metamodel slots.

    Note that descriptions are documentation/metadata and do not affect behavior.
    This test ensures that descriptions are properly propagated as documentation to
    generated frameworks.

    :param framework:
    :return:
    """
    c_description = "C description"
    s1_description = "s1 description"
    classes = {
        CLASS_C: {
            "description": c_description,
            "attributes": {
                SLOT_S1: {
                    "description": s1_description,
                    "_mappings": {
                        PYDANTIC: s1_description,
                        # PYTHON_DATACLASSES: s1_description,
                        SQL_DDL_POSTGRES: f"s1 IS '{s1_description}'",
                    },
                }
            },
            "_mappings": {
                PYDANTIC: c_description,
                PYTHON_DATACLASSES: c_description,
                SQL_DDL_POSTGRES: f'"C" IS \'{c_description}',
            },
        },
    }
    # Note: if the docstring for this test changes, change this too
    schema_description = "Tests behavior of description metamodel slots"
    schema = validated_schema(
        test_descriptions,
        "basic",
        framework,
        classes=classes,
        _mappings={
            PYDANTIC: "",
            PYTHON_DATACLASSES: schema_description,
        },  # TODO - add description in pydantic
    )
    check_data(
        schema,
        "null_test",
        framework,
        {},
        True,
        target_class=CLASS_C,
        description="null test",
    )


@pytest.mark.skip(reason="TODO - add support for deprecation annotations in generators")
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_deprecated(framework):
    """
    Tests behavior of deprecated metamodel slots.

    Note that deprecated assertions are documentation/metadata and do not affect behavior.
    This test ensures that deprecateds are properly propagated as documentation to
    generated frameworks.

    :param framework:
    :return:
    """
    c_deprecated = "C deprecated"
    s1_deprecated = "s1 deprecated"
    classes = {
        CLASS_C: {
            "deprecated": c_deprecated,
            "attributes": {
                SLOT_S1: {
                    "deprecated": s1_deprecated,
                    "_mappings": {
                        PYDANTIC: s1_deprecated,
                    },
                }
            },
            "_mappings": {
                PYDANTIC: c_deprecated,
                PYTHON_DATACLASSES: c_deprecated,
            },
        },
    }
    # Note: if the docstring for this test changes, change this too
    schema = validated_schema(
        test_deprecated,
        "basic",
        framework,
        classes=classes,
    )
    check_data(
        schema,
        "null_test",
        framework,
        {},
        True,
        target_class=CLASS_C,
        description="null test",
    )


@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_element_uris(framework):
    """
    Tests behavior of element uris (class_uri, slot_uri, enum_uri).

    :param framework:
    :return:
    """
    c_uri = "schema:C"
    s1_uri = "schema:s1"
    classes = {
        CLASS_C: {
            "class_uri": c_uri,
            "attributes": {
                SLOT_S1: {
                    "slot_uri": s1_uri,
                    "_mappings": {
                        PYTHON_DATACLASSES: "",
                    },
                }
            },
            "_mappings": {
                PYTHON_DATACLASSES: c_uri,
            },
        },
    }
    # Note: if the docstring for this test changes, change this too
    schema = validated_schema(
        test_element_uris,
        "basic",
        framework,
        classes=classes,
        prefixes={"schema": "http://schema.org/"},
    )
    check_data(
        schema,
        "null_test",
        framework,
        {},
        True,
        target_class=CLASS_C,
        description="null test",
    )
