"""
Smoke tests for the vendored pydantic metamodel
(:mod:`linkml_runtime.linkml_model.pydantic`).

The semantic round-trip equivalence with the dataclass metamodel is tested in
``tests/linkml/test_generators/test_pydanticgen_metamodel.py`` (it needs the
generator); these tests only cover the committed artifact itself.
"""

import yaml

from linkml_runtime.linkml_model.linkml_files import LOCAL_PATH_FOR, Format, Source
from linkml_runtime.linkml_model.pydantic import ClassDefinition, SchemaDefinition, SlotDefinition


def test_construct_minimal_schema() -> None:
    """The vendored pydantic SchemaDefinition constructs from keyword args."""
    schema = SchemaDefinition(id="https://example.org/test", name="test")
    assert schema.name == "test"


def test_validate_keyed_collections() -> None:
    """Inlined-as-dict slots accept keyed-dict YAML form with key injection."""
    schema = SchemaDefinition.model_validate(
        yaml.safe_load(
            """
            id: https://example.org/test
            name: test
            prefixes:
              linkml: https://w3id.org/linkml/
            classes:
              Person:
                slots:
                  - id
            slots:
              id:
                identifier: true
            """
        )
    )
    assert isinstance(schema.classes["Person"], ClassDefinition)
    assert schema.classes["Person"].name == "Person"
    assert isinstance(schema.slots["id"], SlotDefinition)
    assert schema.slots["id"].name == "id"
    assert schema.slots["id"].identifier is True
    assert schema.prefixes["linkml"] == "https://w3id.org/linkml/"


def test_validate_vendored_metamodel_yaml() -> None:
    """The vendored pydantic SchemaDefinition loads the vendored meta.yaml."""
    meta_yaml = LOCAL_PATH_FOR(Source.META, Format.YAML)
    with open(meta_yaml) as f:
        schema = SchemaDefinition.model_validate(yaml.safe_load(f))
    assert "class_definition" in schema.classes


def test_mutation_after_construction() -> None:
    """Post-construction mutation (the SchemaView pattern) works on pydantic models."""
    slot = SlotDefinition(name="s")
    slot.description = "mutated"
    slot.domain_of = ["Person"]
    slot.domain_of.append("Pet")
    assert slot.description == "mutated"
    assert slot.domain_of == ["Person", "Pet"]
