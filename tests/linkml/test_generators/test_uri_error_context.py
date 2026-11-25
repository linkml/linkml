"""Contextual URI expansion failures in RDF generators."""

from collections.abc import Callable

import pytest
from rdflib import Graph, URIRef

from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml_runtime.linkml_model import (
    ClassDefinition,
    EnumDefinition,
    PermissibleValue,
    SchemaDefinition,
    SlotDefinition,
)


@pytest.fixture(
    params=[
        pytest.param((OwlSchemaGenerator, {}), id="owl", marks=pytest.mark.owlgen),
        pytest.param((OwlSchemaGenerator, {"use_native_uris": True}), id="owl-native", marks=pytest.mark.owlgen),
        pytest.param((ShaclGenerator, {}), id="shacl", marks=pytest.mark.shaclgen),
        pytest.param((ShaclGenerator, {"use_class_uri_names": False}), id="shacl-native", marks=pytest.mark.shaclgen),
    ]
)
def generate(request: pytest.FixtureRequest) -> Callable[[SchemaDefinition], str]:
    """Generate RDF using each generator's native and mapped URI modes."""
    generator_type, options = request.param

    def serialize(schema: SchemaDefinition) -> str:
        """Serialize a real schema without replacing any generator behavior."""
        return generator_type(schema, **options).serialize()

    return serialize


def _schema_with_identifier(field: str, value: str) -> SchemaDefinition:
    """Build a schema with one configurable class URI or enum meaning."""
    return SchemaDefinition(
        id="https://example.org/error_context",
        name="error_context",
        prefixes={"ex": "https://example.org/", "linkml": "https://w3id.org/linkml/"},
        imports=["linkml:types"],
        default_prefix="ex",
        classes={
            "Person": ClassDefinition(
                name="Person", class_uri=value if field == "class_uri" else "ex:Person", slots=["status"]
            )
        },
        slots={"status": SlotDefinition(name="status", range="Status")},
        enums={
            "Status": EnumDefinition(
                name="Status",
                permissible_values={
                    "ACTIVE": PermissibleValue(text="ACTIVE", meaning=value if field == "meaning" else "ex:ACTIVE")
                },
            )
        },
    )


@pytest.mark.parametrize(
    ("field", "value", "context"),
    [
        ("class_uri", "UNREGISTERED_PREFIX:C", ("class 'Person'",)),
        ("meaning", "UNREGISTERED_PREFIX:1", ("enum 'Status'", "permissible value 'ACTIVE'")),
        ("meaning", "relative/active", ("enum 'Status'", "permissible value 'ACTIVE'")),
    ],
)
def test_uri_error_context(
    generate: Callable[[SchemaDefinition], str], field: str, value: str, context: tuple[str, ...]
) -> None:
    """URI errors identify the schema element, field, and offending value."""
    with pytest.raises(ValueError) as error:
        generate(_schema_with_identifier(field, value))

    message = str(error.value)
    assert field in message
    assert value in message
    for part in context:
        assert part in message
    assert isinstance(error.value.__cause__, ValueError)
    assert value in str(error.value.__cause__)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("class_uri", "UNREG:C"),
        ("meaning", "UNREG:1"),
        ("class_uri", "urn:example:Person"),
        ("meaning", "urn:example:active"),
    ],
)
def test_valid_uri_is_not_rejected(generate: Callable[[SchemaDefinition], str], field: str, value: str) -> None:
    """Adding error context does not reject custom schemes or authority-free URIs."""
    graph = Graph().parse(data=generate(_schema_with_identifier(field, value)), format="turtle")
    assert URIRef(value) in graph.all_nodes()
