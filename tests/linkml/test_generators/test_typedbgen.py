"""Tests for the TypeDB TypeQL generator."""

import pytest
from click.testing import CliRunner

from linkml.generators.typedbgen import TypeDBGenerator, cli


def test_output_starts_with_define_block(input_path):
    """Generator output starts with a define block."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    assert "define" in output


def test_entity_types_generated(input_path):
    """Each LinkML class produces a TypeDB entity type declaration."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    assert "entity organization" in output
    assert "entity employee" in output
    assert "entity manager" in output


def test_inheritance_sub_keyword(input_path):
    """A class with is_a produces a sub declaration."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    # manager is_a employee
    assert "entity manager, sub employee" in output


def test_scalar_slot_produces_attribute_type(input_path):
    """Scalar slots produce attribute type declarations."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    assert "attribute name, value string" in output


def test_attribute_types_deduplicated(input_path):
    """The same attribute type is only declared once even if used by multiple classes."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    # 'name' is used by multiple slots — should appear exactly once in attribute defs
    assert output.count("attribute name, value string") == 1


def test_identifier_slot_produces_key_annotation(input_path):
    """A slot with identifier: true produces @key annotation."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    assert "owns id @key" in output


def test_required_singular_slot_produces_card_annotation(input_path):
    """A required, non-multivalued slot produces @card(1..1)."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    # last name has slot_usage required: true on employee
    assert "@card(1..1)" in output


def test_multivalued_slot_produces_card_annotation(input_path):
    """A multivalued slot produces @card(0..) annotation."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    assert "@card(0..)" in output


def test_object_ranged_slot_produces_relation(input_path):
    """A slot with a class range produces a TypeDB relation type."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    # has-boss slot has range: manager
    assert "relation has-boss" in output


def test_object_ranged_slot_produces_plays(input_path):
    """Classes involved in an object-ranged slot get plays declarations."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    assert "plays has-boss" in output


def test_header_comment_present(input_path):
    """Output contains a header comment with schema name."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    assert "# Generated" in output


def test_cli_output_matches_serialize(input_path, tmp_path):
    """CLI produces the same output as serialize()."""
    schema_path = str(input_path("organization.yaml"))
    runner = CliRunner()
    result = runner.invoke(cli, [schema_path])
    assert result.exit_code == 0
    expected = TypeDBGenerator(schema_path).serialize()
    assert result.output.strip() == expected.strip()


@pytest.mark.parametrize("linkml_type,expected_typedb_type", [
    ("string", "string"),
    ("integer", "integer"),
    ("float", "double"),
    ("boolean", "boolean"),
    ("datetime", "datetime"),
])
def test_primitive_type_mapping(linkml_type, expected_typedb_type, tmp_path):
    """Primitive LinkML types map to the correct TypeDB value types."""
    schema_yaml = f"""
id: http://example.org/test
name: test-schema
types:
  string:
    base: str
    uri: xsd:string
  integer:
    base: int
    uri: xsd:integer
  float:
    base: float
    uri: xsd:float
  boolean:
    base: bool
    uri: xsd:boolean
  datetime:
    base: str
    uri: xsd:dateTime
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
classes:
  Thing:
    slots:
      - my_attr
slots:
  my_attr:
    range: {linkml_type}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert f"attribute my-attr, value {expected_typedb_type}" in output


def test_enum_produces_string_attribute_with_comment(tmp_path):
    """Enums produce string attributes with a comment listing permitted values."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
types:
  string:
    base: str
    uri: xsd:string
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
classes:
  Person:
    slots:
      - status
slots:
  status:
    range: EmploymentStatus
enums:
  EmploymentStatus:
    permissible_values:
      employed: {}
      unemployed: {}
      student: {}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "attribute status, value string" in output
    # enum values should be mentioned in a comment
    assert "employed" in output
    assert "unemployed" in output
    assert "student" in output


def test_abstract_class_produces_annotation(tmp_path):
    """An abstract LinkML class produces the @abstract annotation in TypeDB."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Animal:
    abstract: true
  Dog:
    is_a: Animal
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "entity animal @abstract" in output
    assert "entity dog, sub animal" in output


# ---------------------------------------------------------------------------
# kitchen_sink.yaml tests — standard schema used across all LinkML generators
# ---------------------------------------------------------------------------


def test_kitchen_sink_serializes_without_error(kitchen_sink_path):
    """The generator completes without raising an exception on the kitchen_sink schema."""
    gen = TypeDBGenerator(kitchen_sink_path, mergeimports=True)
    output = gen.serialize()
    assert output  # non-empty output


def test_kitchen_sink_output_has_define_block(kitchen_sink_path):
    """The generated TypeQL output contains a define block."""
    output = TypeDBGenerator(kitchen_sink_path, mergeimports=True).serialize()
    assert "define" in output


@pytest.mark.parametrize("class_name", ["person", "company", "dataset"])
def test_kitchen_sink_key_entities_present(kitchen_sink_path, class_name):
    """Key kitchen_sink classes appear as entity type declarations."""
    output = TypeDBGenerator(kitchen_sink_path, mergeimports=True).serialize()
    assert f"entity {class_name}" in output


def test_kitchen_sink_inheritance_present(kitchen_sink_path):
    """A class that uses is_a produces a sub declaration in the kitchen_sink output."""
    output = TypeDBGenerator(kitchen_sink_path, mergeimports=True).serialize()
    # Employment is_a Relationship (or similar); any 'sub' keyword means inheritance works
    assert ", sub " in output
