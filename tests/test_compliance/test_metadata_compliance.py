"""
Tests involving metadata.

These typically do not include meaningful instance tests since metadata does not affect behavior.

- TODO: license slot
"""

from copy import deepcopy

import pytest

from tests.test_compliance.helper import (
    OWL,
    PYDANTIC,
    PYTHON_DATACLASSES,
    SQL_DDL_POSTGRES,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import (
    CLASS_C,
    CORE_FRAMEWORKS,
    ENUM_E,
    PV_1,
    SLOT_S1,
    SLOT_S2,
    SUBSET_SS,
    TYPE_T,
)


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
        },
        core_elements=["description"],
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
        core_elements=["deprecated"],
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
        core_elements=["class_uri", "slot_uri"],
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
def test_common_metadata(framework):
    """
    Tests behavior of common metadata elements.

    :param framework:
    :return:
    """

    def triples(
        subject: str,
    ):
        header = (
            "@prefix dcterms: <http://purl.org/dc/terms/> ."
            "@prefix ex: <http://example.org/> ."
            "@prefix linkml: <https://w3id.org/linkml/> ."
            "@prefix ns1: <http://purl.org/ontology/bibo/> ."
            "@prefix orcid: <https://orcid.org/> ."
            "@prefix owl: <http://www.w3.org/2002/07/owl#> ."
            "@prefix pav: <http://purl.org/pav/> ."
            "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> ."
            "@prefix schema: <http://schema.org/> ."
            "@prefix shex: <http://www.w3.org/ns/shex#> ."
            "@prefix skos: <http://www.w3.org/2004/02/skos/core#> ."
            "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ."
        )
        body = [
            "dcterms:contributor orcid:0000-0000-0000-0000",
            'schema:keywords "a keyword"',
            'dcterms:title "a title"',
            'skos:definition "a description"',
            "dcterms:contributor orcid:0000-0000-0000-0000",
        ]
        return "\n".join([header] + list([f"{subject} {t} ." for t in body]))

    common = {
        "title": "a title",
        "description": "a description",
        "created_on": "2021-01-01",
        "last_updated_on": "2021-01-01",
        "comments": ["a comment"],
        "contributors": ["orcid:0000-0000-0000-0000"],
        "categories": ["schema:SomeCategory"],
        "keywords": ["a keyword"],
        "source": "schema:SomeSource",
        "status": "pav:Testing",
        "todos": ["a todo"],
        "notes": ["a note"],
        "examples": [
            {
                "description": "an example with only a description",
            },
            {
                "description": "an example with all fields",
                "value": "a value",
                "object": {"foo": "bar"},
            },
        ],
    }
    classes = {
        CLASS_C: {
            **deepcopy(common),
            "attributes": {
                SLOT_S1: {
                    **deepcopy(common),
                    "_mappings": {OWL: triples("ex:s1")},
                }
            },
            "_mappings": {OWL: triples("ex:C")},
        },
    }
    slots = {
        SLOT_S2: {
            **deepcopy(common),
            "_mappings": {OWL: triples("ex:s2")},
        },
    }
    types = {
        TYPE_T: {
            "typeof": "string",
            **deepcopy(common),
            "_mappings": {
                # OWL: triples("ex:T")
            },
        },
    }
    enums = {
        ENUM_E: {
            "permissible_values": {
                PV_1: {
                    **deepcopy(common),
                }
            },
            **deepcopy(common),
            "_mappings": {
                # OWL: triples("ex:E")
            },
        }
    }
    subsets = {
        SUBSET_SS: {
            **deepcopy(common),
        }
    }
    # Note: if the docstring for this test changes, change this too
    _schema = validated_schema(
        test_common_metadata,
        "basic",
        framework,
        classes=classes,
        enums=enums,
        slots=slots,
        types=types,
        subsets=subsets,
        prefixes={
            "schema": "http://schema.org/",
            "pav": "http://purl.org/pav",
            "orcid": "https://orcid.org/",
        },
        core_elements=["common_metadata"],
        license="https://creativecommons.org/publicdomain/zero/1.0/",
        **deepcopy(common),
    )
