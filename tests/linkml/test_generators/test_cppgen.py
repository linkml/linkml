"""Tests for the C++ header generator.

Schemas are defined inline to keep tests self-contained.
"""


import pytest
from click.testing import CliRunner

from linkml.generators.cppgen import CppGenerator, cli

# ---------------------------------------------------------------------------
# Shared inline schemas
# ---------------------------------------------------------------------------

SIMPLE_SCHEMA = """
id: https://example.org/simple
name: simple_test
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/

imports:
  - linkml:types

classes:
  Person:
    description: A human being
    slots:
      - name
      - age
      - email
      - score

slots:
  name:
    range: string
    required: true
    identifier: true
  age:
    range: integer
  email:
    range: string
  score:
    range: float
"""

INHERITANCE_SCHEMA = """
id: https://example.org/inheritance
name: inheritance_test
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/

imports:
  - linkml:types

classes:
  NamedThing:
    description: A generic named entity
    slots:
      - id
      - name

  Person:
    is_a: NamedThing
    description: A human being
    slots:
      - age

  Employee:
    is_a: Person
    description: A person with a job
    slots:
      - company

slots:
  id:
    range: string
    required: true
    identifier: true
  name:
    range: string
  age:
    range: integer
  company:
    range: string
"""

ENUM_SCHEMA = """
id: https://example.org/enum
name: enum_test
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/

imports:
  - linkml:types

enums:
  Color:
    permissible_values:
      RED:
      GREEN:
      BLUE:

  Status:
    description: Object status
    permissible_values:
      ACTIVE:
      INACTIVE:
      PENDING:

classes:
  Widget:
    slots:
      - color
      - status

slots:
  color:
    range: Color
  status:
    range: Status
"""

COMPOSITION_SCHEMA = """
id: https://example.org/composition
name: composition_test
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/

imports:
  - linkml:types

classes:
  Address:
    description: A postal address
    slots:
      - street
      - city

  Person:
    description: A human being
    slots:
      - name
      - address
      - friends

  Dataset:
    description: A top-level container
    slots:
      - persons

slots:
  street:
    range: string
  city:
    range: string
  name:
    range: string
    required: true
    identifier: true
  address:
    range: Address
  friends:
    range: Person
    multivalued: true
  persons:
    range: Person
    multivalued: true
    inlined_as_list: true
"""

MULTILINE_DESCRIPTION_SCHEMA = """
id: https://example.org/multiline
name: multiline_test
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

enums:
  Priority:
    description: |
      Task priority levels.
      Use HIGH sparingly.
    permissible_values:
      LOW:
        description: |
          Low priority.
          Can be deferred.
      HIGH:

classes:
  Task:
    description: |
      A task to complete.
      This spans multiple lines.
    slots:
      - title
      - note

slots:
  title:
    range: string
    required: true
    identifier: true
  note:
    range: string
"""


# ---------------------------------------------------------------------------
# Tests: struct generation
# ---------------------------------------------------------------------------


def test_struct_generation():
    """Test basic struct generation from a simple schema."""
    gen = CppGenerator(schema=SIMPLE_SCHEMA)
    module = gen.render()

    assert "Person" in module.structs
    person = module.structs["Person"]
    assert person.name == "Person"
    assert person.description == "A human being"
    assert person.fields is not None

    field_names = set(person.fields.keys())
    assert "name" in field_names
    assert "age" in field_names
    assert "email" in field_names


def test_serialized_output():
    """Test that serialized output contains expected C++ constructs."""
    code = CppGenerator(schema=SIMPLE_SCHEMA).serialize()

    assert "#pragma once" in code
    assert "namespace simple_test" in code
    assert "struct Person" in code
    assert "std::string name" in code


def test_struct_descriptions_as_comments():
    """Test that class descriptions become C++ doc comments."""
    code = CppGenerator(schema=SIMPLE_SCHEMA).serialize()
    assert "/// A human being" in code


# ---------------------------------------------------------------------------
# Tests: inheritance
# ---------------------------------------------------------------------------


def test_inheritance_base_classes():
    """Test that is_a produces public inheritance."""
    code = CppGenerator(schema=INHERITANCE_SCHEMA).serialize()

    assert "struct Person : public NamedThing" in code
    assert "struct Employee : public Person" in code


def test_inheritance_only_direct_slots():
    """Test that inherited slots are not duplicated in derived structs."""
    module = CppGenerator(schema=INHERITANCE_SCHEMA).render()

    person = module.structs["Person"]
    person_field_names = set(person.fields.keys()) if person.fields else set()
    assert "age" in person_field_names
    # "id" and "name" are inherited from NamedThing, should not appear
    assert "id" not in person_field_names
    assert "name" not in person_field_names


def test_inheritance_topological_order():
    """Test that base classes are declared before derived classes."""
    code = CppGenerator(schema=INHERITANCE_SCHEMA).serialize()

    named_thing_pos = code.index("struct NamedThing")
    person_pos = code.index("struct Person")
    employee_pos = code.index("struct Employee")
    assert named_thing_pos < person_pos < employee_pos


# ---------------------------------------------------------------------------
# Tests: type mapping
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "slot_name, expected_type",
    [
        ("name", "std::string"),
        ("age", "std::optional<int32_t>"),
        ("score", "std::optional<float>"),
    ],
    ids=["string_required", "integer_optional", "float_optional"],
)
def test_type_mapping(slot_name, expected_type):
    """Test that LinkML types map to correct C++ types."""
    module = CppGenerator(schema=SIMPLE_SCHEMA).render()
    person = module.structs["Person"]
    field = person.fields[slot_name]
    assert field.cpp_type == expected_type


def test_required_no_optional():
    """Test that required/identifier slots are not wrapped in std::optional."""
    module = CppGenerator(schema=SIMPLE_SCHEMA).render()
    person = module.structs["Person"]
    name_field = person.fields["name"]
    assert "optional" not in name_field.cpp_type
    assert name_field.cpp_type == "std::string"


# ---------------------------------------------------------------------------
# Tests: multivalued fields
# ---------------------------------------------------------------------------


def test_multivalued_produces_vector():
    """Test that multivalued slots produce std::vector<T> types."""
    module = CppGenerator(schema=COMPOSITION_SCHEMA).render()
    person = module.structs["Person"]

    friends = person.fields["friends"]
    assert friends.cpp_type == "std::vector<Person>"


def test_optional_class_range():
    """Test that an optional slot with a class range produces std::optional<T>."""
    module = CppGenerator(schema=COMPOSITION_SCHEMA).render()
    person = module.structs["Person"]

    address_field = person.fields["address"]
    assert address_field.cpp_type == "std::optional<Address>"


# ---------------------------------------------------------------------------
# Tests: enums
# ---------------------------------------------------------------------------


def test_enum_generation():
    """Test enum class generation with values."""
    gen = CppGenerator(schema=ENUM_SCHEMA)
    module = gen.render()

    assert "Color" in module.enums
    color = module.enums["Color"]
    assert "RED" in color.values
    assert "GREEN" in color.values
    assert "BLUE" in color.values

    assert "Status" in module.enums
    status = module.enums["Status"]
    assert status.description == "Object status"


def test_enum_serialized_output():
    """Test enum class appears correctly in serialized output."""
    code = CppGenerator(schema=ENUM_SCHEMA).serialize()

    assert "enum class Color" in code
    assert "RED" in code
    assert "GREEN" in code
    assert "BLUE" in code

    # to_string/from_string helpers
    assert "to_string(Color value)" in code
    assert "from_string(const char* str, Color& out)" in code


def test_enum_in_struct_field():
    """Test that a slot with enum range uses the enum type."""
    module = CppGenerator(schema=ENUM_SCHEMA).render()
    widget = module.structs["Widget"]

    color_field = widget.fields["color"]
    assert color_field.cpp_type == "std::optional<Color>"


# ---------------------------------------------------------------------------
# Tests: includes
# ---------------------------------------------------------------------------


def test_includes_generated():
    """Test that the correct system includes are generated."""
    code = CppGenerator(schema=SIMPLE_SCHEMA).serialize()

    assert "#include <string>" in code
    assert "#include <optional>" in code
    assert "#include <cstdint>" in code


def test_vector_include_for_multivalued():
    """Test that std::vector triggers <vector> include."""
    code = CppGenerator(schema=COMPOSITION_SCHEMA).serialize()
    assert "#include <vector>" in code


# ---------------------------------------------------------------------------
# Tests: namespace
# ---------------------------------------------------------------------------


def test_default_namespace():
    """Test that namespace is derived from schema name."""
    code = CppGenerator(schema=SIMPLE_SCHEMA).serialize()
    assert "namespace simple_test" in code


def test_custom_namespace():
    """Test that namespace can be overridden."""
    code = CppGenerator(schema=SIMPLE_SCHEMA, namespace="my::custom::ns").serialize()
    assert "namespace my::custom::ns" in code


# ---------------------------------------------------------------------------
# Tests: multiline descriptions
# ---------------------------------------------------------------------------


def test_multiline_class_description():
    """Test that multiline descriptions produce multi-line C++ comments."""
    code = CppGenerator(schema=MULTILINE_DESCRIPTION_SCHEMA).serialize()
    assert "/// A task to complete." in code
    assert "/// This spans multiple lines." in code


def test_multiline_enum_description():
    """Test that multiline enum descriptions produce multi-line C++ comments."""
    code = CppGenerator(schema=MULTILINE_DESCRIPTION_SCHEMA).serialize()
    assert "/// Task priority levels." in code


# ---------------------------------------------------------------------------
# Tests: options
# ---------------------------------------------------------------------------


def test_no_optional_mode():
    """Test that --no-use-optional disables std::optional wrapping."""
    module = CppGenerator(schema=SIMPLE_SCHEMA, use_optional=False).render()
    person = module.structs["Person"]
    age_field = person.fields["age"]
    assert "optional" not in age_field.cpp_type


def test_alphabetical_sort():
    """Test that alphabetical sort produces deterministic ordering."""
    module = CppGenerator(schema=ENUM_SCHEMA, alphabetical_sort=True).render()

    enum_names = list(module.enums.keys())
    assert enum_names == sorted(enum_names)

    struct_names = list(module.structs.keys())
    assert struct_names == sorted(struct_names)


def test_no_string_conversions():
    """Test that --no-gen-string-conversions omits to_string/from_string."""
    code = CppGenerator(
        schema=ENUM_SCHEMA, gen_string_conversions=False
    ).serialize()
    assert "#include <cstring>" not in code


# ---------------------------------------------------------------------------
# Tests: CLI
# ---------------------------------------------------------------------------


def test_cli_prints_to_stdout(tmp_path):
    """Test that the CLI outputs generated code to stdout."""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(SIMPLE_SCHEMA)

    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_file)])

    assert result.exit_code == 0
    assert "#pragma once" in result.output
    assert "struct Person" in result.output


def test_cli_custom_namespace(tmp_path):
    """Test --namespace CLI option."""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(SIMPLE_SCHEMA)

    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_file), "--namespace", "game::ontology"])

    assert result.exit_code == 0
    assert "namespace game::ontology" in result.output
