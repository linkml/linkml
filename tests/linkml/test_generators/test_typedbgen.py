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
    # manager is_a employee (organization.yaml classes carry descriptions, so @doc
    # is attached to the label before the sub clause)
    assert ", sub employee" in output
    assert "entity manager @doc(" in output


def test_scalar_slot_produces_attribute_type(input_path):
    """Scalar slots produce attribute type declarations."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    # 'name' slot in organization.yaml carries a description, so @doc precedes value
    assert "attribute name @doc(" in output
    assert ", value string" in output


def test_attribute_types_deduplicated(input_path):
    """The same attribute type is only declared once even if used by multiple classes."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    # 'name' is used by multiple slots — should appear exactly once in attribute defs
    assert output.count("attribute name @doc(") == 1


def test_identifier_slot_produces_key_annotation(input_path):
    """A slot with identifier: true produces @key annotation."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    assert "owns id @key" in output


def test_required_singular_slot_produces_card_annotation(input_path):
    """A required, non-multivalued slot produces @card(1)."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    # last name has slot_usage required: true on employee
    assert "@card(1)" in output


def test_multivalued_slot_produces_card_annotation(input_path):
    """A multivalued slot produces @card(0..) annotation."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    assert "@card(0..)" in output


def test_object_ranged_slot_produces_relation(input_path):
    """A slot with a class range produces a TypeDB relation type."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    # has_boss slot has range: manager
    assert "relation has_boss" in output


def test_object_ranged_slot_produces_plays(input_path):
    """Classes involved in an object-ranged slot get plays declarations."""
    gen = TypeDBGenerator(str(input_path("organization.yaml")))
    output = gen.serialize()
    assert "plays has_boss" in output


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
    assert f"attribute my_attr, value {expected_typedb_type}" in output


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


def test_enum_without_static_values_is_plain_string(tmp_path):
    """A dynamic enum (no permissible_values) becomes a plain string, not an empty @values()."""
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
      - process
slots:
  process:
    range: ProcessEnum
enums:
  ProcessEnum:
    reachable_from:
      source_ontology: obo:go
      source_nodes: [GO:0008150]
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "attribute process, value string;" in output
    assert "@values" not in output


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
    # 'role' is not a reserved TypeQL keyword (see the keyword glossary at
    # https://typedb.com/docs/typeql-reference/keywords/), so it is not suffixed.
    assert 'attribute role, value string @values("admin", "user", "guest");' in output


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
    assert "entity Animal @abstract" in output
    assert "entity Dog, sub Animal" in output


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


@pytest.mark.parametrize("class_name", ["Person", "Company", "Dataset"])
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
    """Slots with names matching TypeDB reserved keywords get an _attr suffix."""
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
    assert "attribute type_attr, value string" in output
    assert "owns type_attr" in output


def test_name_collision_attr_gets_suffix(tmp_path):
    """When an attribute name collides with an entity name it gets an _attr suffix.

    Names are preserved verbatim, so the collision requires identical spelling --
    a ``Person`` class and a ``person`` slot do *not* collide, since TypeQL labels
    are case-sensitive.
    """
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  person:
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
    assert "attribute person_attr, value string" in output
    assert "owns person_attr" in output


def test_differing_case_does_not_collide(tmp_path):
    """A class and slot differing only by case keep their own labels (TypeQL is case-sensitive)."""
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
    assert "attribute person, value string" in output
    assert "entity Person" in output
    assert "_attr" not in output


@pytest.mark.parametrize(
    "slot_extra,expected_range",
    [
        ("minimum_value: 0\n    maximum_value: 150", "@range(0..150)"),
        ("minimum_value: 0", "@range(0..)"),
        ("maximum_value: 100", "@range(..100)"),
    ],
)
def test_range_annotation(slot_extra, expected_range, tmp_path):
    """minimum_value / maximum_value produce @range annotations on the owning class's
    ``owns`` declaration (not the shared attribute type — see
    test_slot_usage_constraint_narrowed_per_owner for why: TypeQL lets ``owns`` narrow
    ``@range`` per-owner, so putting it there instead of on the attribute keeps a
    constraint from one owner leaking onto every other owner of the same attribute)."""
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
    assert "attribute score, value integer;" in output
    assert f"owns score {expected_range};" in output


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
    assert "attribute contact_info, value string;" in output
    assert "attribute email, sub contact_info;" in output
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
    assert "attribute base_field, value string;" in output
    assert "attribute mid_field, sub base_field;" in output
    assert "attribute leaf_field, sub mid_field;" in output


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
    assert "attribute name_of_related, value string;" in output
    assert "sub related_to" not in output


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
    assert "entity HasAliases" not in output
    # Mixin slot should appear as owns on the consuming class
    person_block = re.search(r"^\s*entity Person\b[^;]*;", output, re.MULTILINE | re.DOTALL)
    assert person_block, f"Person entity block not found:\n{output}"
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
    assert "entity WithLocation" not in output
    # MarriageEvent should have plays for in_location (from mixin)
    marriage_block = re.search(r"^\s*entity MarriageEvent\b[^;]*;", output, re.MULTILINE | re.DOTALL)
    assert marriage_block, f"MarriageEvent entity block not found:\n{output}"
    assert "plays in_location:" in marriage_block.group(0) or "plays in_location_rel:" in marriage_block.group(0), (
        f"mixin object-ranged slot missing from MarriageEvent:\n{marriage_block.group(0)}"
    )


@pytest.mark.parametrize(
    "slot_extra,expected_card",
    [
        ("minimum_cardinality: 1\n    maximum_cardinality: 5", "@card(1..5)"),
        ("minimum_cardinality: 2", "@card(2..)"),
        ("maximum_cardinality: 3", "@card(0..3)"),
        ("exact_cardinality: 1", "@card(1)"),
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


def test_inline_attributes_produce_owns(input_path):
    """Classes that declare attributes inline via `attributes:` must own them.

    Regression test for a bug where `gen-typedb` emitted the
    `attribute <name>, value <type>;` declarations for inline attributes but
    dropped the matching `owns <name>` clauses from the entity block, leaving
    TypeDB unable to attach those attributes to inserted entities.
    """
    gen = TypeDBGenerator(str(input_path("typedb_inline_attributes.yaml")))
    output = gen.serialize()

    # Sanity: both shapes declare their attribute types.
    assert "attribute shared_name" in output
    assert "attribute inline_name" in output
    assert "attribute inline_description" in output

    # The `slots:`-based class works (control).
    slots_block = re.search(r"^\s*entity ClassWithSlots\b[^;]*;", output, re.MULTILINE | re.DOTALL)
    assert slots_block, f"ClassWithSlots entity block not found:\n{output}"
    assert "owns shared_name" in slots_block.group(0)
    assert "owns shared_description" in slots_block.group(0)

    # The `attributes:`-based class must also own its inline attributes.
    attrs_block = re.search(r"^\s*entity ClassWithAttributes\b[^;]*;", output, re.MULTILINE | re.DOTALL)
    assert attrs_block, f"ClassWithAttributes entity block not found:\n{output}"
    assert "owns inline_name" in attrs_block.group(0), (
        f"inline `attributes:` were declared but not owned by the entity:\n{attrs_block.group(0)}"
    )
    assert "owns inline_description" in attrs_block.group(0)


def test_inline_attributes_with_class_range_produce_relation(input_path):
    """A class-ranged slot declared inline via `attributes:` must produce relates/plays.

    Regression test for the object-ranged half of the inline-attributes fix: the
    `inline_owner` attribute on `ClassWithAttributes` ranges over `ClassWithSlots`,
    so it should be collected as a relation (with an owning role and a played role)
    and both classes should get matching `plays` declarations, exactly like an
    object-ranged slot declared via top-level `slots:`.
    """
    gen = TypeDBGenerator(str(input_path("typedb_inline_attributes.yaml")))
    output = gen.serialize()

    # The inline class-ranged slot produces a standalone relation type: the owning
    # role is named after the slot and the played role after the range class.
    relation_block = re.search(r"^\s*relation inline_owner\b[^;]*;", output, re.MULTILINE | re.DOTALL)
    assert relation_block, f"inline_owner relation block not found:\n{output}"
    assert "relates inline_owner" in relation_block.group(0)
    assert "relates ClassWithSlots" in relation_block.group(0)

    # Both the declaring class and the range class get plays declarations.
    attrs_block = re.search(r"^\s*entity ClassWithAttributes\b[^;]*;", output, re.MULTILINE | re.DOTALL)
    assert attrs_block, f"ClassWithAttributes entity block not found:\n{output}"
    assert "plays inline_owner:inline_owner" in attrs_block.group(0)

    slots_block = re.search(r"^\s*entity ClassWithSlots\b[^;]*;", output, re.MULTILINE | re.DOTALL)
    assert slots_block, f"ClassWithSlots entity block not found:\n{output}"
    assert "plays inline_owner:ClassWithSlots" in slots_block.group(0)


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
    assert "relation FamilialRelationship" in output
    assert "entity FamilialRelationship" not in output
    # Object-ranged slots become relates roles (using slot name)
    assert "relates subject" in output
    assert "relates object" in output
    # Scalar slot becomes owns on the relation
    assert "owns description" in output
    # Range class (Person) gets plays declarations
    assert "plays FamilialRelationship:subject" in output
    assert "plays FamilialRelationship:object" in output
    # No standalone relation per slot (since they're handled as relates)
    assert "relation subject" not in output
    assert "relation object" not in output


def test_reflexive_class_ranged_slot_gets_distinct_roles(tmp_path):
    """A class-ranged slot whose range is its own declaring class gets two distinct roles.

    Previously both ends of a reflexive slot (e.g. Person.parent: range Person) were
    named after the player's class, collapsing to a single role capped at TypeDB's
    default @card(0..1) and making the relationship inexpressible in one direction.
    """
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  Person:
    slots: [id, parent]
slots:
  id: {identifier: true}
  parent: {range: Person}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "relates parent" in output
    assert "relates Person" in output
    assert "plays parent:parent" in output
    assert "plays parent:Person" in output


def test_multivalued_class_ranged_slot_is_one_relation_per_link(tmp_path):
    """Each link holds exactly one owner and one target; the slot's cardinality bounds
    how many links the owner takes part in, on its plays."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Person:
    slots:
      - name
  Team:
    slots:
      - members
slots:
  name:
    range: string
  members:
    range: Person
    multivalued: true
    required: true
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "relates members @card(1)" in output
    assert "relates Person @card(1)" in output
    assert "plays members:members @card(1..)" in output
    assert "plays members:Person;" in output


def test_slot_usage_constraint_narrowed_per_owner(tmp_path):
    """A slot_usage range constraint on one class narrows only that class's owns,
    not the shared attribute type (which would otherwise wrongly restrict every owner)."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Employee:
    slots:
      - age
  Manager:
    slots:
      - age
    slot_usage:
      age:
        minimum_value: 21
slots:
  age:
    range: integer
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    # Shared attribute type stays unconstrained
    assert "attribute age, value integer;" in output
    # Manager narrows its own ownership
    assert "owns age @range(21..)" in output
    # Employee's ownership stays unconstrained
    employee_block = re.search(r"entity Employee\b[^;]*;", output, re.DOTALL)
    assert employee_block and "@range" not in employee_block.group(0)


def test_abstract_dropped_when_supertype_is_concrete(tmp_path):
    """An abstract class under a concrete ancestor loses @abstract (TypeDB [SVL14]),
    with a warning comment, rather than propagating @abstract up to the ancestor."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Thing:
    slots: [id]
  Organism:
    is_a: Thing
    abstract: true
  Dog:
    is_a: Organism
slots:
  id: {identifier: true}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "entity Thing," in output
    assert "entity Organism, sub Thing;" in output
    assert "organism @abstract" not in output
    assert "SVL14" in output


def test_abstract_preserved_when_supertype_also_abstract(tmp_path):
    """A legitimate abstract chain (all-abstract ancestors) keeps @abstract throughout."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Animal:
    abstract: true
  Mammal:
    is_a: Animal
    abstract: true
  Dog:
    is_a: Mammal
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "entity Animal @abstract" in output
    assert "entity Mammal @abstract, sub Animal" in output
    assert "SVL14" not in output


def test_abstract_dropped_transitively_when_grandparent_is_concrete(tmp_path):
    """A -> B(abstract) -> C(abstract) where A is concrete: B loses @abstract (direct
    SVL14 violation), which makes C's @abstract illegal too even though C's own direct
    LinkML parent (B) is nominally abstract — B is no longer abstract in the *generated*
    TypeDB schema, so C must lose @abstract as well, not just B.

    Mirrors Biolink's ``named-thing`` (concrete) -> ``biological-entity`` (abstract) ->
    ``organismal-entity`` (abstract) chain.
    """
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Thing:
    slots: [id]
  Organism:
    is_a: Thing
    abstract: true
  Animal:
    is_a: Organism
    abstract: true
  Dog:
    is_a: Animal
slots:
  id: {identifier: true}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "entity Thing," in output
    assert "entity Organism, sub Thing;" in output
    assert "entity Animal, sub Organism;" in output
    assert "organism @abstract" not in output
    assert "animal @abstract" not in output
    assert output.count("SVL14") == 2


def test_enum_values_are_escaped(tmp_path):
    """Enum permissible values containing quotes/backslashes are safely escaped."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Thing:
    slots:
      - status
slots:
  status:
    range: Status
enums:
  Status:
    permissible_values:
      'has "quotes"': {}
      normal: {}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert '\\"quotes\\"' in output
    # The unescaped form must not appear (would be invalid TypeQL)
    assert '"has "quotes""' not in output


def test_pattern_produces_regex_annotation(tmp_path):
    """A slot with pattern produces an @regex annotation on its owns declaration."""
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
      - code
slots:
  code:
    range: string
    pattern: "^[A-Z]{3}$"
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert 'owns code @regex("^[A-Z]{3}$")' in output


def test_description_produces_doc_annotation(tmp_path):
    """A class/slot description produces a @doc annotation."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Thing:
    description: a thing
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
    assert 'entity Thing @doc("a thing")' in output


def test_class_ranged_slot_description_produces_doc_on_relation(tmp_path):
    """A class-ranged slot's description goes on the relation generated for it."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Person:
    slots:
      - parent
slots:
  parent:
    range: Person
    description: a parent of this person
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    output = TypeDBGenerator(str(schema_file)).serialize()
    assert 'relation parent @doc("a parent of this person"),' in output


def test_multiline_description_escaped_in_doc_annotation(tmp_path):
    """A multi-line description is flattened to a single-line, escaped @doc string."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Thing:
    description: |
      line one
      line two
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
    assert "line one\\nline two" in output
    assert "\n      line two" not in output


def test_date_uses_native_date_value_type(tmp_path):
    """``date`` maps to TypeDB's native date value type."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  linkml: https://w3id.org/linkml/
  xsd: http://www.w3.org/2001/XMLSchema#
imports:
  - linkml:types
classes:
  Thing:
    slots:
      - born
slots:
  born:
    range: date
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "attribute born, value date;" in output


def test_reserved_keyword_list_matches_current_typeql(tmp_path):
    """Slot/class names matching current TypeQL keywords (not just the old list) get suffixed."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Thing:
    slots:
      - list
      - median
slots:
  list:
    range: string
  median:
    range: string
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "attribute list_attr, value string" in output
    assert "attribute median_attr, value string" in output


# ---------------------------------------------------------------------------
# Associations as relations (SchemaView.is_relationship detection) and role
# narrowing (relates ... as ...) for slot_usage range overrides.
# ---------------------------------------------------------------------------


def test_rdf_statement_mapping_detected_as_relationship(tmp_path):
    """A class marked via exact_mappings: [rdf:Statement] becomes a relation, even
    without represents_relationship: true (this is how Biolink's association class
    is actually marked, and is what SchemaView.is_relationship() already detects)."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
classes:
  Person:
    slots: [name]
  Association:
    exact_mappings:
      - rdf:Statement
    slots: [id, subject, object]
slots:
  name:
    range: string
  id:
    identifier: true
  subject:
    range: Person
  object:
    range: Person
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "relation Association" in output
    assert "entity Association" not in output
    assert "relates subject" in output
    assert "relates object" in output


def test_represents_relationship_false_suppresses_rdf_fallback(tmp_path):
    """represents_relationship is the primary source of truth, so an explicit false
    keeps a class an entity even though its rdf:Statement mapping would otherwise
    make it a relation."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
classes:
  Statementish:
    represents_relationship: false
    exact_mappings:
      - rdf:Statement
    slots: [id]
slots:
  id: {identifier: true}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "entity Statementish" in output
    assert "relation Statementish" not in output


def test_represents_relationship_nearest_ancestor_wins(tmp_path):
    """LinkML does not propagate represents_relationship through is_a, so the nearest
    ancestor that sets it decides, letting a subclass override an inherited intent."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
classes:
  Edge:
    represents_relationship: true
  InheritsEdge:
    is_a: Edge
  OverridesEdge:
    is_a: Edge
    represents_relationship: false
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "relation Edge" in output
    assert "relation InheritsEdge" in output
    assert "entity OverridesEdge" in output
    assert "relation OverridesEdge" not in output


def test_subclass_narrows_role_via_slot_usage(tmp_path):
    """A relationship subclass that narrows a role's range via slot_usage gets a
    specialized `relates ... as ...` role, and the narrowed range class plays that
    specialized role (not the unspecialized parent role)."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
default_range: string
classes:
  NamedThing:
    slots: [id]
  Gene:
    is_a: NamedThing
  Disease:
    is_a: NamedThing
  Association:
    exact_mappings: [rdf:Statement]
    slots: [id, subject, object]
  GeneToDiseaseAssociation:
    is_a: Association
    slot_usage:
      subject: {range: Gene}
      object: {range: Disease}
slots:
  id: {identifier: true}
  subject: {range: NamedThing}
  object: {range: NamedThing}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "relation GeneToDiseaseAssociation, sub Association," in output
    assert "relates Gene_subject as subject" in output
    assert "relates Disease_object as object" in output
    assert "plays GeneToDiseaseAssociation:Gene_subject" in output
    assert "plays GeneToDiseaseAssociation:Disease_object" in output


def test_subclass_repeating_same_narrowed_range_does_not_redeclare_role(tmp_path):
    """A grandchild that narrows a role to the SAME range its parent already narrowed
    it to does not redeclare the role (would violate TypeDB's unique-role-name-per-
    hierarchy rule) -- it inherits the parent's specialized role unchanged."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
default_range: string
classes:
  NamedThing:
    slots: [id]
  Gene:
    is_a: NamedThing
  Association:
    exact_mappings: [rdf:Statement]
    slots: [id, subject]
  GeneAssociation:
    is_a: Association
    slot_usage:
      subject: {range: Gene}
  GeneHomologyAssociation:
    is_a: GeneAssociation
    slot_usage:
      subject: {range: Gene}
slots:
  id: {identifier: true}
  subject: {range: NamedThing}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "relates Gene_subject as subject" in output
    # gene_homology_association must not redeclare gene_subject
    ghomology_block = re.search(r"relation GeneHomologyAssociation\b[^;]*;", output, re.DOTALL)
    assert ghomology_block, f"gene_homology_association block not found:\n{output}"
    assert "relates" not in ghomology_block.group(0)


def test_required_class_ranged_slot_cardinality_on_owner_plays_only(tmp_path):
    """A required single-valued slot bounds the owner's links to exactly one; the range
    class's plays stays bare, since LinkML says nothing about how often it is targeted."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  Person:
    slots: [id]
  Case:
    slots: [id, diagnosis]
slots:
  id: {identifier: true}
  diagnosis:
    range: Person
    required: true
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "plays diagnosis:diagnosis @card(1)" in output
    assert "plays diagnosis:Person @card" not in output
    assert "plays diagnosis:Person" in output


# ---------------------------------------------------------------------------
# Mixin-ranged roles: a slot ranged at a mixin must grant plays to the mixin's
# concrete implementers, since mixins are not emitted as TypeDB types.
# ---------------------------------------------------------------------------


def test_mixin_ranged_role_grants_plays_to_implementers(tmp_path):
    """A relationship role narrowed to a mixin range is playable by the mixin's
    concrete implementers.

    Mixins are never emitted as TypeDB types, so granting plays to the mixin itself
    would leave the role declared but unplayable -- no entity could be inserted into
    it. Mirrors Biolink's gene_to_disease_association.subject, narrowed to the mixin
    'gene or gene product' and implemented by gene, protein and others.
    """
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
default_range: string
classes:
  NamedThing:
    slots: [id]
  GeneOrGeneProduct:
    mixin: true
  Gene:
    is_a: NamedThing
    mixins: [GeneOrGeneProduct]
  Protein:
    is_a: NamedThing
    mixins: [GeneOrGeneProduct]
  Disease:
    is_a: NamedThing
  Association:
    exact_mappings: [rdf:Statement]
    slots: [id, subject, object]
  GeneToDiseaseAssociation:
    is_a: Association
    slot_usage:
      subject: {range: GeneOrGeneProduct}
      object: {range: Disease}
slots:
  id: {identifier: true}
  subject: {range: NamedThing}
  object: {range: NamedThing}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    # The mixin itself is not a TypeDB type and never receives plays.
    assert "entity Gene_or_gene_product" not in output
    # Every concrete implementer can play the role.
    assert "plays GeneToDiseaseAssociation:GeneOrGeneProduct_subject" in output
    gene_block = re.search(r"entity Gene\b[^;]*;", output, re.DOTALL)
    protein_block = re.search(r"entity Protein\b[^;]*;", output, re.DOTALL)
    assert gene_block and "GeneOrGeneProduct_subject" in gene_block.group(0)
    assert protein_block and "GeneOrGeneProduct_subject" in protein_block.group(0)


def test_mixin_ranged_role_not_redeclared_on_subtypes(tmp_path):
    """Only the most general implementers receive the plays declaration.

    TypeDB propagates plays down the sub chain and rejects a subtype redeclaring an
    inherited capability ([SVL42]), so an implementer that already inherits the role
    from another implementer among its is_a ancestors must be skipped.
    """
    schema_yaml = """
id: http://example.org/test
name: test-schema
prefixes:
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
default_range: string
classes:
  NamedThing:
    slots: [id]
  Taggable:
    mixin: true
  Parent:
    is_a: NamedThing
    mixins: [Taggable]
  Child:
    is_a: Parent
  Disease:
    is_a: NamedThing
  Association:
    exact_mappings: [rdf:Statement]
    slots: [id, subject, object]
  TagAssociation:
    is_a: Association
    slot_usage:
      subject: {range: Taggable}
      object: {range: Disease}
slots:
  id: {identifier: true}
  subject: {range: NamedThing}
  object: {range: NamedThing}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    # Parent declares it; Child inherits it via sub and must NOT redeclare it.
    parent_block = re.search(r"entity Parent\b[^;]*;", output, re.DOTALL)
    child_block = re.search(r"entity Child\b[^;]*;", output, re.DOTALL)
    assert parent_block and "Taggable_subject" in parent_block.group(0)
    assert child_block and "Taggable_subject" not in child_block.group(0)


# ---------------------------------------------------------------------------
# Naming: LinkML names are preserved; only whitespace is transformed.
# ---------------------------------------------------------------------------


def test_camelcase_names_are_preserved(tmp_path):
    """CamelCase names pass through unchanged -- TypeQL labels allow mixed case, so
    there is no need to guess word boundaries (which would mangle acronyms)."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  GeneToDiseaseAssociation:
    slots: [id]
  microRNA:
    slots: [id]
slots:
  id: {identifier: true}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "entity GeneToDiseaseAssociation" in output
    assert "entity microRNA" in output


def test_spaces_become_underscores(tmp_path):
    """Whitespace is the one thing TypeQL labels cannot contain, so it becomes '_'."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  gene to disease association:
    slots: [age in years]
slots:
  age in years: {range: integer}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "entity gene_to_disease_association" in output
    assert "attribute age_in_years" in output


def test_class_name_collision_raises(tmp_path):
    """Two class names differing only by whitespace map to one label, which TypeDB
    would reject -- fail with a diagnostic naming both classes instead."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  gene to disease:
    slots: [id]
  gene_to_disease:
    slots: [id]
slots:
  id: {identifier: true}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    with pytest.raises(ValueError, match="same TypeDB label"):
        gen.serialize()


def test_subclass_narrowing_inherited_slot_redeclares_owns(tmp_path):
    """A subclass that narrows an inherited slot via slot_usage redeclares owns with
    just the tightened constraint.

    Inherited slots are normally not redeclared (TypeDB rejects a plain redeclaration,
    [SVL42]) but a narrowing redeclaration IS accepted, and skipping it on name alone
    would silently discard the constraint.
    """
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  person:
    slots: [id, age]
  child:
    is_a: person
    slot_usage:
      age:
        maximum_value: 17
slots:
  id: {identifier: true}
  age: {range: integer}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "entity child, sub person," in output
    assert "owns age @range(..17)" in output
    # The narrowing redeclaration must not repeat cardinality/@key, which would make it
    # a plain redeclaration and trip [SVL42].
    child_block = re.search(r"entity child\b[^;]*;", output, re.DOTALL)
    assert child_block and "@card" not in child_block.group(0)


def test_subclass_not_narrowing_does_not_redeclare_owns(tmp_path):
    """A subclass that merely inherits a slot unchanged does not redeclare it."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  person:
    slots: [id, age]
  child:
    is_a: person
slots:
  id: {identifier: true}
  age: {range: integer}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "entity child, sub person;" in output


# ---------------------------------------------------------------------------
# Class-ranged slot_usage narrowing on an ordinary (non-relationship) class.
# A sub-relation is emitted so the narrowed range's implementers get a specialized
# role, without dropping the narrowing (mirrors Biolink's molecular_activity.enabled_by).
# ---------------------------------------------------------------------------


def test_class_ranged_narrowing_on_entity_emits_sub_relation(tmp_path):
    """slot_usage narrowing a class-ranged slot on an ordinary entity subclass emits a
    sub-relation, so the narrower range's implementers get a specialized role instead
    of the narrowing being silently dropped."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  named_thing:
    slots: [id]
  physical_entity:
    is_a: named_thing
  gene:
    is_a: named_thing
  process:
    is_a: named_thing
    slots: [enabled_by]
  molecular_activity:
    is_a: process
    slot_usage:
      enabled_by:
        range: gene
slots:
  id: {identifier: true}
  enabled_by:
    range: physical_entity
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "relation enabled_by," in output
    assert "relation enabled_by_molecular_activity sub enabled_by," in output
    assert "relates gene_physical_entity as physical_entity" in output
    assert "plays enabled_by_molecular_activity:gene_physical_entity" in output


def test_class_ranged_narrowing_does_not_redeclare_inherited_plays(tmp_path):
    """The narrowing subclass does not repeat the base relation's owning-role plays --
    it already inherits that via sub, and redeclaring it would trip TypeDB's [SVL42]."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  named_thing:
    slots: [id]
  physical_entity:
    is_a: named_thing
  gene:
    is_a: named_thing
  process:
    is_a: named_thing
    slots: [enabled_by]
  molecular_activity:
    is_a: process
    slot_usage:
      enabled_by:
        range: gene
slots:
  id: {identifier: true}
  enabled_by:
    range: physical_entity
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    ma_block = re.search(r"entity molecular_activity\b[^;]*;", output, re.DOTALL)
    assert ma_block, f"molecular_activity entity block not found:\n{output}"
    assert "plays" not in ma_block.group(0)


def test_class_ranged_narrowing_on_declaring_class(tmp_path):
    """slot_usage narrowing a class-ranged slot on the class that declares it keeps the
    base relation on the slot's own range, and the declaring class still plays the owning
    role with its cardinality, since it has no supertype to inherit that from."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  animal:
    abstract: true
    slots: [id]
  dog:
    is_a: animal
  person:
    slots: [id, pets]
    slot_usage:
      pets:
        range: dog
slots:
  id: {identifier: true}
  pets:
    range: animal
    multivalued: true
    minimum_cardinality: 1
    maximum_cardinality: 3
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert re.search(r"relation pets,\s+relates pets @card\(1\),\s+relates animal @card\(1\);", output)
    assert "relation pets_person sub pets," in output
    assert "relates dog_animal as animal" in output
    person_block = re.search(r"entity person\b[^;]*;", output, re.DOTALL)
    assert person_block, f"person entity block not found:\n{output}"
    assert "plays pets:pets @card(1..3)" in person_block.group(0)
    dog_block = re.search(r"entity dog\b[^;]*;", output, re.DOTALL)
    assert dog_block, f"dog entity block not found:\n{output}"
    assert "plays pets_person:dog_animal" in dog_block.group(0)


def test_class_ranged_narrowing_restated_unchanged_is_not_redeclared(tmp_path):
    """A grandchild that restates the SAME narrowed range as its parent does not get
    its own sub-relation -- it's a restatement, not a new narrowing, and it already
    inherits the parent's specialized role via sub."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  named_thing:
    slots: [id]
  physical_entity:
    is_a: named_thing
  gene:
    is_a: named_thing
  process:
    is_a: named_thing
    slots: [enabled_by]
  molecular_activity:
    is_a: process
    slot_usage:
      enabled_by:
        range: gene
  molecular_function:
    is_a: molecular_activity
    slot_usage:
      enabled_by:
        range: gene
slots:
  id: {identifier: true}
  enabled_by:
    range: physical_entity
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    gen = TypeDBGenerator(str(schema_file))
    output = gen.serialize()
    assert "enabled_by_molecular_activity" in output
    assert "enabled_by_molecular_function" not in output


# ---------------------------------------------------------------------------
# Class-ranged slot hierarchies: slot is_a becomes a sub-relation.
# ---------------------------------------------------------------------------

_SLOT_TREE_SCHEMA = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  NamedThing:
    slots: [id]
  Gene:
    is_a: NamedThing
    slots: [related to]
  Protein:
    is_a: NamedThing
  SpecialGene:
    is_a: Gene
    slots: [interacts with]
slots:
  id: {identifier: true}
  related to: {range: NamedThing, multivalued: true}
  interacts with: {is_a: related to}
  binds: {is_a: interacts with, range: Protein}
"""


def _slot_tree_output(tmp_path):
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(_SLOT_TREE_SCHEMA)
    return TypeDBGenerator(str(schema_file)).serialize()


def test_slot_inherits_class_range_through_is_a(tmp_path):
    """A slot with no range of its own inherits its parent's class range, so it becomes
    a relation rather than falling back to a default_range string attribute."""
    output = _slot_tree_output(tmp_path)
    assert "attribute interacts_with" not in output
    assert "attribute binds" not in output
    assert "relation interacts_with," in output


def test_class_ranged_slot_is_a_becomes_sub_relation(tmp_path):
    """Each level subtypes its parent's relation and specializes the owning role; the
    played role is inherited unless the range narrows."""
    output = _slot_tree_output(tmp_path)
    assert "relation interacts_with,\n      sub related_to,\n      relates interacts_with as related_to @card(1);" in output
    assert "relates binds as interacts_with @card(1)" in output
    assert "relates Protein as NamedThing @card(1)" in output
    assert "plays binds:Protein" in output


def test_owning_role_players_play_every_role_below(tmp_path):
    """The class that declares a slot plays the owning role at every level below it, and
    a subclass declaring a lower slot does not redeclare the inherited plays."""
    output = _slot_tree_output(tmp_path)
    gene_block = output.split("entity Gene,")[1].split(";")[0]
    assert "plays related_to:related_to @card(0..)" in gene_block
    assert "plays interacts_with:interacts_with" in gene_block
    assert "plays binds:binds" in gene_block
    assert "entity SpecialGene, sub Gene;" in output


def test_root_relation_declares_slots_from_entity_ancestor(tmp_path):
    """A relationship class whose parent is an ordinary class has no relation supertype,
    so it declares the parent's slots itself."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
prefixes:
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
classes:
  Entity:
    slots: [id, category]
  Thing:
    is_a: Entity
  Association:
    is_a: Entity
    exact_mappings: [rdf:Statement]
    slots: [subject]
slots:
  id: {identifier: true}
  category: {multivalued: true}
  subject: {range: Thing}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    output = TypeDBGenerator(str(schema_file)).serialize()
    association = output.split("relation Association")[1].split(";")[0]
    assert "sub Entity" not in association
    assert "owns id @key" in association
    assert "owns category @card(0..)" in association


def test_enum_set_by_slot_usage_goes_on_owns_not_attribute(tmp_path):
    """An enum range set by one class's slot_usage restricts only that class."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  Edge:
    slots: [predicate]
  CausalEdge:
    is_a: Edge
    slot_usage:
      predicate: {range: CausalPredicate}
  Other:
    slots: [predicate]
    slot_usage:
      predicate: {range: CausalPredicate}
slots:
  predicate: {range: string}
enums:
  CausalPredicate:
    permissible_values:
      causes: {}
      prevents: {}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    output = TypeDBGenerator(str(schema_file)).serialize()
    assert "attribute predicate, value string;" in output
    assert 'entity CausalEdge, sub Edge,\n      owns predicate @values("causes", "prevents");' in output
    assert 'owns predicate @values("causes", "prevents")' in output.split("entity Other")[1].split(";")[0]
    assert "@values" not in output.split("entity Edge")[1].split(";")[0]


def test_undeclared_slot_is_played_by_its_domain(tmp_path):
    """A class-ranged slot no class declares is played by its domain class on the owning
    side and its range class on the played side; each level uses its own domain."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  NamedThing:
    slots: [id]
  Gene:
    is_a: NamedThing
  Chemical:
    is_a: NamedThing
slots:
  id: {identifier: true}
  interacts with: {domain: NamedThing, range: NamedThing, multivalued: true}
  genetically interacts with: {is_a: interacts with, domain: Gene, range: Gene}
  unowned link: {range: NamedThing}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    output = TypeDBGenerator(str(schema_file)).serialize()
    named = output.split("entity NamedThing,")[1].split(";")[0]
    gene = output.split("entity Gene, sub NamedThing,")[1].split(";")[0]
    assert "plays interacts_with:interacts_with @card(0..)" in named
    assert "plays interacts_with:NamedThing" in named
    assert "genetically_interacts_with" not in named
    assert "plays genetically_interacts_with:genetically_interacts_with @card(0..)" in gene
    assert "plays genetically_interacts_with:Gene" in gene
    assert "entity Chemical, sub NamedThing;" in output
    assert "plays unowned_link:unowned_link" not in output


def test_undeclared_scalar_slot_is_owned_by_its_domain(tmp_path):
    """A scalar slot no class declares is owned by its domain class; abstract slots are not."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
classes:
  Dataset:
    slots: [id]
slots:
  id: {identifier: true}
  node property: {domain: Dataset, abstract: true}
  version: {is_a: node property}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    output = TypeDBGenerator(str(schema_file)).serialize()
    dataset = output.split("entity Dataset,")[1].split(";")[0]
    assert "owns version" in dataset
    assert "owns node_property" not in dataset
    assert "attribute version, sub node_property;" in output


def test_attribute_subtype_requires_matching_value_type(tmp_path):
    """A slot whose range differs in value type from its parent's is not an attribute subtype,
    since a TypeDB attribute subtype inherits its parent's value type."""
    schema_yaml = """
id: http://example.org/test
name: test-schema
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
imports: [linkml:types]
classes:
  Thing:
    slots: [title, score]
slots:
  annotation: {}
  title: {is_a: annotation}
  score: {is_a: annotation, range: float}
"""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(schema_yaml)
    output = TypeDBGenerator(str(schema_file)).serialize()
    assert "attribute title, sub annotation;" in output
    assert "attribute score, value double;" in output
