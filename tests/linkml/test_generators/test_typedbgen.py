"""Tests for the TypeDB TypeQL generator."""

import re

import pytest
from click.testing import CliRunner

from linkml.generators.typedbgen import TypeDBGenerator, cli

pytestmark = pytest.mark.typedbgen


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


@pytest.mark.parametrize(
    "linkml_type,expected_typedb_type",
    [
        ("string", "string"),
        ("integer", "integer"),
        ("float", "double"),
        ("boolean", "boolean"),
        ("datetime", "datetime"),
    ],
)
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


def test_enum_produces_values_annotation(tmp_path):
    """Enums produce string attributes with a @values(...) annotation."""
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
    assert '@values("employed", "unemployed", "student")' in output


def test_multiple_enums_each_get_values_annotation(tmp_path):
    """Each enum-ranged slot gets its own @values annotation on its attribute declaration."""
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
      - role
slots:
  status:
    range: EmploymentStatus
  role:
    range: RoleType
enums:
  EmploymentStatus:
    permissible_values:
      employed: {}
      unemployed: {}
  RoleType:
    permissible_values:
      admin: {}
      user: {}
      guest: {}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert 'attribute status, value string @values("employed", "unemployed");' in output
    assert 'attribute role-attr, value string @values("admin", "user", "guest");' in output


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


def test_reserved_keyword_slot_gets_suffix(tmp_path):
    """Slots with names matching TypeDB reserved keywords get an -attr suffix."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Thing:
    slots:
      - type
slots:
  type:
    range: string
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "attribute type-attr, value string" in output
    assert "owns type-attr" in output


def test_name_collision_attr_gets_suffix(tmp_path):
    """When an attribute name collides with an entity name it gets an -attr suffix."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Person:
    slots:
      - person
slots:
  person:
    range: string
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "attribute person-attr, value string" in output
    assert "owns person-attr" in output


@pytest.mark.parametrize(
    "slot_extra,expected_range",
    [
        ("minimum_value: 0\n    maximum_value: 150", "@range(0..150)"),
        ("minimum_value: 0", "@range(0..)"),
        ("maximum_value: 100", "@range(..100)"),
    ],
)
def test_range_annotation(slot_extra, expected_range, tmp_path):
    """minimum_value / maximum_value produce @range annotations on attribute declarations."""
    schema_yaml = f"""
id: http://example.org/test
name: test-schema
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Thing:
    slots:
      - score
slots:
  score:
    range: integer
    {slot_extra}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert f"attribute score, value integer {expected_range};" in output


def test_no_range_annotation_when_unset(tmp_path):
    """No @range annotation when minimum_value and maximum_value are both unset."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Thing:
    slots:
      - score
slots:
  score:
    range: integer
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "attribute score, value integer;" in output
    assert "@range" not in output


def test_attribute_subtyping_basic(tmp_path):
    """A slot with is_a pointing to another scalar slot emits 'sub' instead of 'value'."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Thing:
    slots:
      - contact_info
      - email
slots:
  contact_info:
    range: string
  email:
    is_a: contact_info
    range: string
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "attribute contact-info, value string;" in output
    assert "attribute email, sub contact-info;" in output
    # Child should NOT have a value declaration
    assert "attribute email, value string;" not in output


def test_attribute_subtyping_chain(tmp_path):
    """A chain of slot is_a relationships produces a chain of sub declarations."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Thing:
    slots:
      - base_field
      - mid_field
      - leaf_field
slots:
  base_field:
    range: string
  mid_field:
    is_a: base_field
    range: string
  leaf_field:
    is_a: mid_field
    range: string
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "attribute base-field, value string;" in output
    assert "attribute mid-field, sub base-field;" in output
    assert "attribute leaf-field, sub mid-field;" in output


def test_attribute_subtyping_skipped_for_class_ranged_parent(tmp_path):
    """A slot with is_a pointing to a class-ranged slot does NOT emit sub."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Person:
    slots:
      - related_to
      - name_of_related
  OtherPerson:
    slots: []
slots:
  related_to:
    range: OtherPerson
  name_of_related:
    is_a: related_to
    range: string
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    # Parent is class-ranged (relation), child is scalar — no sub, just a normal attribute
    assert "attribute name-of-related, value string;" in output
    assert "sub related-to" not in output


def test_mixin_slots_appear_on_consuming_class(tmp_path):
    """Mixin-contributed slots are emitted as owns on the consuming class."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  HasAliases:
    mixin: true
    attributes:
      aliases:
        range: string
        multivalued: true
  Person:
    mixins:
      - HasAliases
    slots:
      - name
slots:
  name:
    range: string
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    # Mixin class should NOT appear as a TypeDB entity
    assert "entity hasaliases" not in output
    # Mixin slot should appear as owns on the consuming class
    person_block = re.search(r"^\s*entity person\b[^;]*;", output, re.MULTILINE | re.DOTALL)
    assert person_block, f"person entity block not found:\n{output}"
    assert "owns aliases" in person_block.group(0)
    assert "owns name" in person_block.group(0)


def test_mixin_with_object_ranged_slot(tmp_path):
    """Mixin-contributed object-ranged slots produce plays on the consuming class."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Place:
    slots:
      - name
  WithLocation:
    mixin: true
    slots:
      - in_location
  Event:
    slots:
      - description
  MarriageEvent:
    is_a: Event
    mixins:
      - WithLocation
    slots:
      - married_to
  Person:
    slots:
      - name
slots:
  name:
    range: string
  in_location:
    range: Place
  description:
    range: string
  married_to:
    range: Person
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    # Mixin class should NOT appear as a TypeDB entity
    assert "entity withlocation" not in output
    # MarriageEvent should have plays for in_location (from mixin)
    marriage_block = re.search(r"^\s*entity marriageevent\b[^;]*;", output, re.MULTILINE | re.DOTALL)
    assert marriage_block, f"marriageevent entity block not found:\n{output}"
    assert "plays in-location:" in marriage_block.group(0) or "plays in-location-rel:" in marriage_block.group(0), (
        f"mixin object-ranged slot missing from marriageevent:\n{marriage_block.group(0)}"
    )


@pytest.mark.parametrize(
    "slot_extra,expected_card",
    [
        ("minimum_cardinality: 1\n    maximum_cardinality: 5", "@card(1..5)"),
        ("minimum_cardinality: 2", "@card(2..)"),
        ("maximum_cardinality: 3", "@card(0..3)"),
        ("exact_cardinality: 1", "@card(1..1)"),
    ],
)
def test_precise_cardinality_annotation(slot_extra, expected_card, tmp_path):
    """Precise cardinality fields produce exact @card(min..max) annotations."""
    schema_yaml = f"""
id: http://example.org/test
name: test-schema
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Thing:
    slots:
      - tags
slots:
  tags:
    range: string
    multivalued: true
    {slot_extra}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert f"owns tags {expected_card}" in output


def test_represents_relationship_class_becomes_relation(tmp_path):
    """A class with represents_relationship: true becomes a TypeDB relation type."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Person:
    slots:
      - name
  FamilialRelationship:
    represents_relationship: true
    slots:
      - subject
      - object
      - description
slots:
  name:
    range: string
  subject:
    range: Person
  object:
    range: Person
  description:
    range: string
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    # Relationship class becomes a TypeDB relation, not entity
    assert "relation familialrelationship" in output
    assert "entity familialrelationship" not in output
    # Object-ranged slots become relates roles (using slot name)
    assert "relates subject" in output
    assert "relates object" in output
    # Scalar slot becomes owns on the relation
    assert "owns description" in output
    # Range class (Person) gets plays declarations
    assert "plays familialrelationship:subject" in output
    assert "plays familialrelationship:object" in output
    # No standalone relation per slot (since they're handled as relates)
    assert "relation subject" not in output
    assert "relation object" not in output
