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
    """Test that alphabetical sort orders enums but keeps structs topological."""
    module = CppGenerator(schema=ENUM_SCHEMA, alphabetical_sort=True).render()

    enum_names = list(module.enums.keys())
    assert enum_names == sorted(enum_names)


def test_structs_stay_topological_with_sort():
    """Test that alphabetical sort does not reorder structs (C++ needs base before derived)."""
    module = CppGenerator(schema=INHERITANCE_SCHEMA, alphabetical_sort=True).render()

    struct_names = list(module.structs.keys())
    # Employee extends Person extends NamedThing, so topological order must be preserved
    assert struct_names.index("NamedThing") < struct_names.index("Person")
    assert struct_names.index("Person") < struct_names.index("Employee")


def test_no_string_conversions():
    """Test that --no-gen-string-conversions omits to_string/from_string."""
    code = CppGenerator(schema=ENUM_SCHEMA, gen_string_conversions=False).serialize()
    assert "#include <cstring>" not in code


# ---------------------------------------------------------------------------
# Tests: ifabsent / default values
# ---------------------------------------------------------------------------

IFABSENT_SCHEMA = """
id: https://example.org/ifabsent
name: ifabsent_test
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  Config:
    slots:
      - label
      - retries
      - ratio
      - enabled
      - disabled

slots:
  label:
    range: string
    required: true
    identifier: true
  retries:
    range: integer
    required: true
    ifabsent: int(3)
  ratio:
    range: float
    required: true
    ifabsent: float(0.5)
  enabled:
    range: boolean
    required: true
    ifabsent: "true"
  disabled:
    range: boolean
    required: true
    ifabsent: "false"
"""


@pytest.mark.parametrize(
    "slot_name, expected_default",
    [
        ("retries", "3"),
        ("ratio", "0.5f"),
        ("enabled", "true"),
        ("disabled", "false"),
    ],
    ids=["int_ifabsent", "float_ifabsent", "bool_true_ifabsent", "bool_false_ifabsent"],
)
def test_ifabsent_defaults(slot_name, expected_default):
    """Test that ifabsent expressions are parsed into C++ defaults."""
    module = CppGenerator(schema=IFABSENT_SCHEMA).render()
    config = module.structs["Config"]
    field = config.fields[slot_name]
    assert field.default_value == expected_default


def test_parse_ifabsent_unknown_returns_none():
    """Test that an unrecognized ifabsent expression returns None."""
    gen = CppGenerator(schema=SIMPLE_SCHEMA)
    assert gen._parse_ifabsent("unknown(foo)") is None


def test_parse_ifabsent_string():
    """Test that string() ifabsent produces a quoted C++ literal."""
    gen = CppGenerator(schema=SIMPLE_SCHEMA)
    assert gen._parse_ifabsent("string(unknown)") == '"unknown"'


# ---------------------------------------------------------------------------
# Tests: mixins
# ---------------------------------------------------------------------------

MIXIN_SCHEMA = """
id: https://example.org/mixin
name: mixin_test
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  Identifiable:
    mixin: true
    slots:
      - id

  Describable:
    mixin: true
    slots:
      - description

  Item:
    is_a: Identifiable
    mixins:
      - Describable
    slots:
      - name

slots:
  id:
    range: string
    required: true
    identifier: true
  description:
    range: string
  name:
    range: string
"""


def test_mixin_inheritance():
    """Test that mixins produce multiple base classes in the struct."""
    code = CppGenerator(schema=MIXIN_SCHEMA).serialize()
    assert "struct Item : public Identifiable, public Describable" in code


# ---------------------------------------------------------------------------
# Tests: sort_classes error
# ---------------------------------------------------------------------------


def test_sort_classes_cycle_raises():
    """Test that sort_classes raises ValueError on an unresolvable cycle."""
    from linkml_runtime.linkml_model.meta import ClassDefinition

    cls_a = ClassDefinition(name="A", is_a="B")
    cls_b = ClassDefinition(name="B", is_a="A")
    with pytest.raises(ValueError, match="Could not topologically sort"):
        CppGenerator.sort_classes([cls_a, cls_b])


# ---------------------------------------------------------------------------
# Tests: edge cases in generate_cpp_type
# ---------------------------------------------------------------------------

UNKNOWN_TYPE_SCHEMA = """
id: https://example.org/unknown_type
name: unknown_type_test
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

types:
  CustomType:
    typeof: string
    uri: xsd:string

classes:
  Thing:
    slots:
      - data

slots:
  data:
    range: CustomType
"""


def test_type_with_known_base_maps_correctly():
    """Test that a custom type whose base is in TYPE_MAP resolves correctly."""
    module = CppGenerator(schema=UNKNOWN_TYPE_SCHEMA).render()
    thing = module.structs["Thing"]
    # CustomType -> typeof string -> base 'str' -> std::string, and it's optional
    assert "string" in thing.fields["data"].cpp_type


# ---------------------------------------------------------------------------
# Tests: default_value_for_type
# ---------------------------------------------------------------------------


def test_default_value_for_known_type():
    """Test default_value_for_type returns the correct literal for known types."""
    gen = CppGenerator(schema=SIMPLE_SCHEMA)
    assert gen.default_value_for_type("std::string") == '""'
    assert gen.default_value_for_type("int32_t") == "0"
    assert gen.default_value_for_type("bool") == "false"


def test_default_value_for_unknown_type():
    """Test default_value_for_type falls back to '{}' for unknown types."""
    gen = CppGenerator(schema=SIMPLE_SCHEMA)
    assert gen.default_value_for_type("SomeUnknownType") == "{}"


# ---------------------------------------------------------------------------
# Tests: serialize with pre-rendered module
# ---------------------------------------------------------------------------


def test_serialize_with_prerendered_module():
    """Test that serialize() accepts a pre-rendered CppModule."""
    gen = CppGenerator(schema=SIMPLE_SCHEMA)
    module = gen.render()
    code = gen.serialize(rendered_module=module)
    assert "#pragma once" in code
    assert "struct Person" in code


# ---------------------------------------------------------------------------
# Tests: custom template_dir
# ---------------------------------------------------------------------------


def test_custom_template_dir(tmp_path):
    """Test that template_dir option adds a custom loader."""
    gen = CppGenerator(schema=SIMPLE_SCHEMA, template_dir=str(tmp_path))
    # Should still work — custom dir is searched first, then falls back to built-in
    code = gen.serialize()
    assert "#pragma once" in code


# ---------------------------------------------------------------------------
# Tests: template.py Includes operations
# ---------------------------------------------------------------------------


def test_includes_add_single():
    """Test adding a single CppInclude to Includes."""
    from linkml.generators.cppgen.template import CppInclude, Includes

    inc = Includes(includes=[CppInclude(header="string", system=True)])
    result = inc + CppInclude(header="vector", system=True)
    assert len(result) == 2


def test_includes_add_deduplicates():
    """Test that adding a duplicate include is a no-op."""
    from linkml.generators.cppgen.template import CppInclude, Includes

    inc = Includes(includes=[CppInclude(header="string", system=True)])
    result = inc + CppInclude(header="string", system=True)
    assert len(result) == 1


def test_includes_add_includes_object():
    """Test merging two Includes objects."""
    from linkml.generators.cppgen.template import CppInclude, Includes

    a = Includes(includes=[CppInclude(header="string")])
    b = Includes(includes=[CppInclude(header="vector")])
    result = a + b
    assert len(result) == 2


def test_includes_add_list():
    """Test adding a list of CppInclude to Includes."""
    from linkml.generators.cppgen.template import CppInclude, Includes

    inc = Includes()
    result = inc + [CppInclude(header="string"), CppInclude(header="vector")]
    assert len(result) == 2


def test_includes_sort():
    """Test that sort orders system includes first, then alphabetically."""
    from linkml.generators.cppgen.template import CppInclude, Includes

    inc = Includes(
        includes=[
            CppInclude(header="vector", system=True),
            CppInclude(header="myheader.h", system=False),
            CppInclude(header="algorithm", system=True),
        ]
    )
    inc.sort()
    headers = [i.header for i in inc.includes]
    assert headers == ["algorithm", "vector", "myheader.h"]


# ---------------------------------------------------------------------------
# Tests: template render without explicit environment
# ---------------------------------------------------------------------------


def test_template_render_without_environment():
    """Test that CppTemplateModel.render() works without an explicit environment."""
    from linkml.generators.cppgen.template import CppEnum, CppEnumValue

    enum = CppEnum(
        name="Color",
        values={"RED": CppEnumValue(name="RED", value="RED")},
    )
    rendered = enum.render()
    assert "enum class Color" in rendered


# ---------------------------------------------------------------------------
# Tests: build.py merge with includes
# ---------------------------------------------------------------------------


def test_build_result_merge_with_includes():
    """Test that merging build results combines includes."""
    from linkml.generators.cppgen.build import CppBuildResult
    from linkml.generators.cppgen.template import CppInclude, Includes

    a = CppBuildResult(includes=Includes(includes=[CppInclude(header="string")]))
    b = CppBuildResult(includes=Includes(includes=[CppInclude(header="vector")]))
    merged = a.merge(b)
    assert merged.includes is not None


def test_build_result_merge_includes_into_none():
    """Test merging includes into a result that has no includes yet."""
    from linkml.generators.cppgen.build import CppBuildResult
    from linkml.generators.cppgen.template import CppInclude, Includes

    a = CppBuildResult(includes=None)
    b = CppBuildResult(includes=Includes(includes=[CppInclude(header="string")]))
    merged = a.merge(b)
    assert merged.includes is not None


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


def test_cli_nonexistent_template_dir(tmp_path):
    """Test that CLI raises an error for a non-existent template directory."""
    schema_file = tmp_path / "test.yaml"
    schema_file.write_text(SIMPLE_SCHEMA)

    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_file), "--template-dir", "/nonexistent/path"])

    assert result.exit_code != 0
