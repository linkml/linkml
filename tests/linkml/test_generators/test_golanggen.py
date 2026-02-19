"""
Tests for the Golang generator.

Tests the golanggen package implementation based on pydanticgen architecture.
Schemas are defined inline to keep tests self-contained.
"""

import pytest

from linkml.generators.golanggen import GolangGenerator

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
    range: decimal
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


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_struct_generation():
    """Test basic struct generation from a simple schema."""
    gen = GolangGenerator(schema=SIMPLE_SCHEMA)
    module = gen.render()

    assert "Person" in module.structs
    person = module.structs["Person"]
    assert person.name == "Person"
    assert person.description == "A human being"
    assert person.fields is not None

    field_go_names = {f.go_name for f in person.fields.values()}
    assert "Name" in field_go_names
    assert "Age" in field_go_names
    assert "Email" in field_go_names


def test_serialized_output():
    """Test that serialized output contains expected Go constructs."""
    code = GolangGenerator(schema=SIMPLE_SCHEMA).serialize()

    assert "package simple" in code
    assert "type Person struct {" in code
    assert 'json:"name"' in code
    assert 'json:"age' in code
    assert "omitempty" in code


def test_inheritance_embedding():
    """Test that is_a produces struct embedding with json:",inline" tag."""
    code = GolangGenerator(schema=INHERITANCE_SCHEMA).serialize()

    # Person embeds NamedThing
    assert 'NamedThing `json:",inline"`' in code
    # Employee embeds Person
    assert 'Person `json:",inline"`' in code

    # Verify via the model too
    module = GolangGenerator(schema=INHERITANCE_SCHEMA).render()

    person = module.structs["Person"]
    assert person.embedded_structs == ["NamedThing"]

    employee = module.structs["Employee"]
    assert employee.embedded_structs == ["Person"]

    # Direct slots only — inherited ones come via embedding
    person_field_names = {f.go_name for f in person.fields.values()}
    assert "Age" in person_field_names
    # "Id" and "Name" are inherited, so must NOT appear as direct fields
    assert "Id" not in person_field_names
    assert "Name" not in person_field_names


def test_enum_generation():
    """Test enum / const block generation."""
    gen = GolangGenerator(schema=ENUM_SCHEMA)
    module = gen.render()

    assert "Color" in module.enums
    color = module.enums["Color"]
    assert color.type == "string"
    assert "RED" in color.values
    assert "GREEN" in color.values
    assert "BLUE" in color.values

    assert "Status" in module.enums
    status = module.enums["Status"]
    assert status.description == "Object status"

    code = gen.serialize()
    assert "type Color string" in code
    assert "const (" in code
    assert 'ColorRED Color = "RED"' in code


@pytest.mark.parametrize(
    "slot_name, expected_type",
    [
        ("name", "string"),
        ("age", "*int"),
        ("score", "*float64"),
    ],
    ids=["string_slot", "integer_slot", "decimal_slot"],
)
def test_type_mapping(slot_name, expected_type):
    """Test that LinkML types are correctly mapped to Go types.

    nullable_primitives is True by default, so optional primitives are pointers.
    The ``name`` slot is required + identifier, so it stays a bare string.
    """
    module = GolangGenerator(schema=SIMPLE_SCHEMA).render()
    person = module.structs["Person"]
    field = person.fields[slot_name]
    assert field.type == expected_type


def test_multivalued_fields():
    """Test that multivalued slots produce Go slice types."""
    module = GolangGenerator(schema=COMPOSITION_SCHEMA).render()
    person = module.structs["Person"]

    friends = person.fields["friends"]
    assert friends.type.startswith("[]"), f"Expected slice type, got {friends.type}"


def test_optional_pointer_for_class_range():
    """Test that an optional slot with a class range produces a pointer type."""
    module = GolangGenerator(schema=COMPOSITION_SCHEMA).render()
    person = module.structs["Person"]

    address_field = person.fields["address"]
    assert address_field.type == "*Address"


def test_json_tags():
    """Test JSON struct tags with omitempty for optional fields."""
    code = GolangGenerator(schema=SIMPLE_SCHEMA).serialize()

    # required + identifier → no omitempty
    assert 'json:"name"' in code
    # optional fields → omitempty
    assert 'json:"age,omitempty"' in code
    assert 'json:"email,omitempty"' in code


def test_comments_from_descriptions():
    """Test that class descriptions produce Go comments."""
    code = GolangGenerator(schema=SIMPLE_SCHEMA).serialize()
    assert "// A human being" in code


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
    description: |
      An optional note.
      May contain details.
"""


@pytest.mark.parametrize(
    "fragment",
    [
        # struct description: every line prefixed with //
        "// A task to complete.\n// This spans multiple lines.",
        # field description (indented)
        "\t// An optional note.\n\t// May contain details.",
        # enum type description
        "// Task priority levels.\n// Use HIGH sparingly.",
        # enum value description (indented)
        "\t// Low priority.\n\t// Can be deferred.",
    ],
    ids=[
        "struct_multiline",
        "field_multiline",
        "enum_type_multiline",
        "enum_value_multiline",
    ],
)
def test_multiline_descriptions_go_comment(fragment):
    """Test that multi-line descriptions are rendered with // on every line."""
    code = GolangGenerator(schema=MULTILINE_DESCRIPTION_SCHEMA).serialize()
    assert fragment in code, f"Expected {fragment!r} in generated code"


def test_single_line_description_unchanged():
    """Test that single-line descriptions still render correctly."""
    code = GolangGenerator(schema=SIMPLE_SCHEMA).serialize()
    assert "// A human being" in code


def test_package_name_derived():
    """Test that the package name is derived from the schema name."""
    module = GolangGenerator(schema=SIMPLE_SCHEMA).render()
    assert module.package_name == "simple"


def test_package_name_override():
    """Test that --package-name overrides the derived value."""
    module = GolangGenerator(schema=SIMPLE_SCHEMA, package_name="mypkg").render()
    assert module.package_name == "mypkg"


TIME_SCHEMA = """
id: https://example.org/dates
name: dates_test
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/

imports:
  - linkml:types

classes:
  Event:
    slots:
      - started_at
      - created_at
      - timestamps

slots:
  started_at:
    range: date
  created_at:
    range: datetime
    required: true
  timestamps:
    range: date
    multivalued: true
"""


def test_imports_time_package():
    """Test that the time package is imported when date/time types are used."""
    code = GolangGenerator(schema=TIME_SCHEMA).serialize()
    assert '"time"' in code
    assert "time.Time" in code


def test_time_always_pointer_when_optional():
    """time.Time is always a pointer when optional, regardless of nullable_primitives."""
    module = GolangGenerator(schema=TIME_SCHEMA, nullable_primitives=False).render()
    event = module.structs["Event"]

    # optional date → *time.Time (always, even with nullable_primitives=False)
    assert event.fields["started_at"].type == "*time.Time"
    # required datetime → time.Time (no pointer)
    assert event.fields["created_at"].type == "time.Time"
    # multivalued date → []time.Time (slices are already nil-able)
    assert event.fields["timestamps"].type == "[]time.Time"


def test_root_struct_names():
    """Test that root_struct_names excludes classes used as field types."""
    module = GolangGenerator(schema=COMPOSITION_SCHEMA).render()

    # Address is referenced by Person.address → not root
    # Person is referenced by Dataset.persons and Person.friends → not root
    # Dataset is never referenced as a field type → root
    assert "Dataset" in module.root_struct_names
    assert "Address" not in module.root_struct_names
    assert "Person" not in module.root_struct_names


def test_root_struct_names_non_inlined():
    """Classes referenced via non-inlined slots (type aliases) are not root."""
    module = GolangGenerator(schema=REFERENCED_SCHEMA).render()
    # Container is the root; KeyedInt is referenced via KeyedIntId alias
    assert "Container" in module.root_struct_names
    assert "KeyedInt" not in module.root_struct_names


def test_root_struct_names_no_references():
    """When no class references another, all are root classes."""
    module = GolangGenerator(schema=SIMPLE_SCHEMA).render()
    assert "Person" in module.root_struct_names


def test_default_value_for_type():
    """Test Go zero-value defaults for various types."""
    gen = GolangGenerator(schema=SIMPLE_SCHEMA)
    assert gen.default_value_for_type("string") == '""'
    assert gen.default_value_for_type("int") == "0"
    assert gen.default_value_for_type("bool") == "false"
    assert gen.default_value_for_type("float64") == "0.0"
    assert gen.default_value_for_type("time.Time") == "time.Time{}"
    assert gen.default_value_for_type("SomeStruct") == "nil"


def test_serialize_with_prerendered_module():
    """Test serialize() when given a pre-rendered module."""
    gen = GolangGenerator(schema=SIMPLE_SCHEMA)
    module = gen.render()
    code = gen.serialize(rendered_module=module)
    assert "package simple" in code
    assert "type Person struct" in code


def test_enum_field_type_in_struct():
    """Test that enum-typed fields use the enum name as Go type."""
    module = GolangGenerator(schema=ENUM_SCHEMA).render()
    widget = module.structs["Widget"]
    assert widget.fields["color"].type == "Color"
    assert widget.fields["status"].type == "Status"


def test_package_name_no_underscore():
    """Test package name derivation when schema name has no underscore."""
    schema = """
id: https://example.org/myschema
name: myschema
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  Foo:
    slots:
      - bar
slots:
  bar:
    range: string
"""
    module = GolangGenerator(schema=schema).render()
    assert module.package_name == "myschema"


def test_cli_happy_path(tmp_path):
    """Test the CLI generates output successfully."""
    from click.testing import CliRunner

    from linkml.generators.golanggen.golanggen import cli

    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(SIMPLE_SCHEMA)

    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_file)])
    assert result.exit_code == 0
    assert "package simple" in result.output
    assert "type Person struct" in result.output


def test_cli_with_package_name(tmp_path):
    """Test CLI --package-name flag."""
    from click.testing import CliRunner

    from linkml.generators.golanggen.golanggen import cli

    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(SIMPLE_SCHEMA)

    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_file), "--package-name", "mypkg"])
    assert result.exit_code == 0
    assert "package mypkg" in result.output


def test_cli_with_template_dir(tmp_path):
    """Test CLI --template-dir flag with a valid directory."""
    from click.testing import CliRunner

    from linkml.generators.golanggen.golanggen import cli

    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(SIMPLE_SCHEMA)

    template_dir = tmp_path / "templates"
    template_dir.mkdir()

    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_file), "--template-dir", str(template_dir)])
    assert result.exit_code == 0
    assert "package simple" in result.output


def test_import_model():
    """Test Import template model rendering."""
    from linkml.generators.golanggen.template import Import

    imp = Import(module="fmt")
    assert imp.group == "stdlib"
    rendered = imp.render()
    assert '"fmt"' in rendered

    imp_ext = Import(module="github.com/example/pkg")
    assert imp_ext.group == "thirdparty"

    imp_alias = Import(module="github.com/example/pkg", alias="mypkg")
    rendered_alias = imp_alias.render()
    assert "mypkg" in rendered_alias


def test_imports_sort():
    """Test that imports are sorted by group then alphabetically."""
    from linkml.generators.golanggen.template import Import, Imports

    imports = Imports(
        imports=[
            Import(module="github.com/example/z"),
            Import(module="fmt"),
            Import(module="github.com/example/a"),
            Import(module="time"),
        ]
    )
    imports.sort()
    modules = [i.module for i in imports.imports]
    assert modules == ["fmt", "time", "github.com/example/a", "github.com/example/z"]


def test_backwards_compatibility():
    """Test that the generator is importable from both locations."""
    from linkml.generators.golanggen import GolangGenerator as NewGen
    from linkml.generators.golanggen.golanggen import GolangGenerator as DirectGen

    assert NewGen is DirectGen


# ---------------------------------------------------------------------------
# Template-dir tests
# ---------------------------------------------------------------------------


def test_template_dir_overrides_struct(tmp_path):
    """Test that --template-dir overrides individual templates."""
    custom_struct = tmp_path / "struct.go.jinja"
    custom_struct.write_text(
        "// CUSTOM TEMPLATE\n"
        "{% if description %}\n"
        "// {{ description }}\n"
        "{% endif -%}\n"
        "type {{ name }} struct {\n"
        "{% if embedded_structs %}\n"
        "{% for embed in embedded_structs %}\n"
        "\t{{ embed }}\n"
        "{% endfor %}\n"
        "{% endif -%}\n"
        "{% if fields %}\n"
        "{% for field in fields.values() %}\n"
        "{{ field }}\n"
        "{% endfor -%}\n"
        "{% endif %}\n"
        "}\n"
    )

    code = GolangGenerator(schema=SIMPLE_SCHEMA, template_dir=str(tmp_path)).serialize()
    assert "// CUSTOM TEMPLATE" in code
    assert "package simple" in code


def test_template_dir_fallback(tmp_path):
    """Test that an empty template-dir falls back to built-in templates."""
    code = GolangGenerator(schema=SIMPLE_SCHEMA, template_dir=str(tmp_path)).serialize()
    assert "package simple" in code
    assert "type Person struct" in code


def test_template_dir_nonexistent_raises(tmp_path):
    """Test that a nonexistent template_dir raises an error in the CLI."""
    from click.testing import CliRunner

    from linkml.generators.golanggen.golanggen import cli

    # Write a minimal schema file so the CLI positional arg is valid
    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(SIMPLE_SCHEMA)

    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_file), "--template-dir", "/nonexistent/path"])
    assert result.exit_code != 0
    assert "does not exist" in str(result.exception)


def test_template_dir_jsonld_wrapper(tmp_path):
    """Test custom module template that includes jsonld_wrapper for root classes only."""
    # Create a custom module template that includes jsonld_wrapper
    module_tpl = tmp_path / "module.go.jinja"
    module_tpl.write_text(
        "// Code generated by linkml-golanggen. DO NOT EDIT.\n"
        "package {{ package_name }}\n"
        "\n"
        "import (\n"
        "{% if imports and imports.strip() %}\n"
        '{{ imports | replace("import (", "") | replace(")", "") }}\n'
        "{% endif %}\n"
        '\t"encoding/json"\n'
        '\t"reflect"\n'
        ")\n"
        "{% if enums %}\n"
        "{% for e in enums.values() %}\n"
        "{{ e }}\n"
        "{% endfor %}\n"
        "{% endif %}\n"
        "{% for s in structs.values() %}\n"
        "{{ s }}\n"
        "{% endfor %}\n"
        "{% for name in root_struct_names %}\n"
        '{% include "jsonld_wrapper.go.jinja" %}\n'
        "{% endfor %}\n"
    )

    # Create the jsonld_wrapper template
    wrapper_tpl = tmp_path / "jsonld_wrapper.go.jinja"
    wrapper_tpl.write_text(
        "\n"
        "// JsonLD{{ name }} is a JSON-LD wrapper for {{ name }}\n"
        "type JsonLD{{ name }} struct {\n"
        '\tContext     map[string]interface{} `json:"@context"`\n'
        '\tPayloadType string                 `json:"@type"`\n'
        '\tPayload     {{ name }}             `json:",inline"`\n'
        "}\n"
    )

    code = GolangGenerator(schema=COMPOSITION_SCHEMA, template_dir=str(tmp_path)).serialize()

    # Dataset is a root class → wrapper generated
    assert "type JsonLDDataset struct {" in code
    assert "// JsonLDDataset is a JSON-LD wrapper for Dataset" in code

    # Address and Person are referenced as field types → no wrapper
    assert "JsonLDAddress" not in code
    assert "JsonLDPerson" not in code

    # Basic structure still present
    assert "type Person struct {" in code
    assert "type Address struct {" in code
    assert "type Dataset struct {" in code
    assert '"encoding/json"' in code
    assert '"reflect"' in code


# ---------------------------------------------------------------------------
# Alphabetical sort tests
# ---------------------------------------------------------------------------


def test_alphabetical_sort_structs():
    """Test that alphabetical_sort orders structs by name."""
    module = GolangGenerator(schema=COMPOSITION_SCHEMA, alphabetical_sort=True).render()
    struct_names = list(module.structs.keys())
    assert struct_names == sorted(struct_names), f"Structs not alphabetically sorted: {struct_names}"


def test_alphabetical_sort_enums():
    """Test that alphabetical_sort orders enums by name."""
    module = GolangGenerator(schema=ENUM_SCHEMA, alphabetical_sort=True).render()
    enum_names = list(module.enums.keys())
    assert enum_names == sorted(enum_names), f"Enums not alphabetically sorted: {enum_names}"


def test_alphabetical_sort_serialized_order():
    """Test that struct definitions appear in alphabetical order in generated code."""
    code = GolangGenerator(schema=COMPOSITION_SCHEMA, alphabetical_sort=True).serialize()
    # Address < Dataset < Person
    addr_pos = code.index("type Address struct")
    dataset_pos = code.index("type Dataset struct")
    person_pos = code.index("type Person struct")
    assert addr_pos < dataset_pos < person_pos


def test_alphabetical_sort_disabled_by_default():
    """Test that alphabetical_sort is off by default (topological order preserved)."""
    gen = GolangGenerator(schema=COMPOSITION_SCHEMA)
    assert gen.alphabetical_sort is False


# ---------------------------------------------------------------------------
# Nullable primitives tests
# ---------------------------------------------------------------------------


def test_nullable_primitives_pointer_types():
    """Test that nullable_primitives adds pointer prefix to optional primitive fields."""
    module = GolangGenerator(schema=SIMPLE_SCHEMA, nullable_primitives=True).render()
    person = module.structs["Person"]

    # 'age' is optional integer → *int
    assert person.fields["age"].type == "*int"
    # 'email' is optional string → *string
    assert person.fields["email"].type == "*string"


def test_nullable_primitives_required_fields_unchanged():
    """Test that required/identifier fields are not turned into pointers."""
    module = GolangGenerator(schema=SIMPLE_SCHEMA, nullable_primitives=True).render()
    person = module.structs["Person"]

    # 'name' is required + identifier → stays string (no pointer)
    assert person.fields["name"].type == "string"


def test_nullable_primitives_class_range_unchanged():
    """Test that class-range optional fields are not double-pointered."""
    module = GolangGenerator(schema=COMPOSITION_SCHEMA, nullable_primitives=True).render()
    person = module.structs["Person"]

    # 'address' is optional class range → still *Address (not **Address)
    assert person.fields["address"].type == "*Address"


def test_nullable_primitives_multivalued_unchanged():
    """Test that multivalued primitive fields are not given pointer element types."""
    schema = """
id: https://example.org/multitest
name: multitest
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  TagBag:
    slots:
      - tags

slots:
  tags:
    range: string
    multivalued: true
"""
    module = GolangGenerator(schema=schema, nullable_primitives=True).render()
    tagbag = module.structs["TagBag"]

    # multivalued string → []string, NOT []*string (slices are already nil-able)
    assert tagbag.fields["tags"].type == "[]string"


def test_nullable_primitives_serialized_output():
    """Test that serialized output uses pointer syntax for optional primitives."""
    code = GolangGenerator(schema=SIMPLE_SCHEMA, nullable_primitives=True).serialize()

    # optional int → *int
    assert "*int" in code
    # optional string → *string
    assert "*string" in code
    # required identifier stays bare string
    assert 'Name string `json:"name"' in code


def test_nullable_primitives_enabled_by_default():
    """Test that nullable_primitives is on by default."""
    gen = GolangGenerator(schema=SIMPLE_SCHEMA)
    assert gen.nullable_primitives is True


def test_nullable_primitives_bool_field():
    """Test that optional bool fields become *bool with nullable_primitives."""
    schema = """
id: https://example.org/booltest
name: booltest
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  Feature:
    slots:
      - name
      - enabled
      - count

slots:
  name:
    range: string
    required: true
    identifier: true
  enabled:
    range: boolean
  count:
    range: integer
"""
    module = GolangGenerator(schema=schema, nullable_primitives=True).render()
    feature = module.structs["Feature"]

    assert feature.fields["enabled"].type == "*bool"
    assert feature.fields["count"].type == "*int"
    assert feature.fields["name"].type == "string"  # required → no pointer


# ---------------------------------------------------------------------------
# CLI tests for new flags
# ---------------------------------------------------------------------------


def test_cli_alphabetical_sort(tmp_path):
    """Test CLI --alphabetical-sort flag."""
    from click.testing import CliRunner

    from linkml.generators.golanggen.golanggen import cli

    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(COMPOSITION_SCHEMA)

    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_file), "--alphabetical-sort"])
    assert result.exit_code == 0
    code = result.output
    addr_pos = code.index("type Address struct")
    dataset_pos = code.index("type Dataset struct")
    person_pos = code.index("type Person struct")
    assert addr_pos < dataset_pos < person_pos


def test_cli_nullable_primitives(tmp_path):
    """Test CLI --nullable-primitives flag."""
    from click.testing import CliRunner

    from linkml.generators.golanggen.golanggen import cli

    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(SIMPLE_SCHEMA)

    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_file), "--nullable-primitives"])
    assert result.exit_code == 0
    assert "*int" in result.output
    assert "*string" in result.output


# ---------------------------------------------------------------------------
# Inlined vs referenced tests
# ---------------------------------------------------------------------------

REFERENCED_SCHEMA = """
id: https://example.org/referenced
name: referenced_test
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  KeyedInt:
    slots:
      - id
      - value

  Container:
    tree_root: true
    slots:
      - items
      - single_ref

slots:
  id:
    range: string
    identifier: true
  value:
    range: integer
    required: true
  items:
    range: KeyedInt
    multivalued: true
  single_ref:
    range: KeyedInt
"""


def test_referenced_multivalued_uses_id_type():
    """When a class has an identifier and inlined is not set, multivalued slots
    should use the identifier type, not the full struct."""
    module = GolangGenerator(schema=REFERENCED_SCHEMA).render()
    container = module.structs["Container"]

    # multivalued, not inlined → []KeyedIntId
    assert container.fields["items"].type == "[]KeyedIntId"


def test_referenced_single_valued_uses_pointer_id_type():
    """A single-valued non-inlined optional slot uses *IdType."""
    module = GolangGenerator(schema=REFERENCED_SCHEMA).render()
    container = module.structs["Container"]

    # single-valued, optional, not inlined → *KeyedIntId
    assert container.fields["single_ref"].type == "*KeyedIntId"


def test_referenced_generates_type_definition():
    """Non-inlined references produce a named Go type definition."""
    code = GolangGenerator(schema=REFERENCED_SCHEMA).serialize()

    assert "type KeyedIntId string" in code


def test_inlined_as_list_uses_full_struct():
    """When inlined_as_list is set, the full struct should be used."""
    schema = """
id: https://example.org/inlined
name: inlined_test
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  Item:
    slots:
      - id
      - label

  Bag:
    slots:
      - contents

slots:
  id:
    range: string
    identifier: true
  label:
    range: string
  contents:
    range: Item
    multivalued: true
    inlined_as_list: true
"""
    module = GolangGenerator(schema=schema).render()
    bag = module.structs["Bag"]

    # explicitly inlined → []Item, not []ItemId
    assert bag.fields["contents"].type == "[]Item"


def test_no_identifier_auto_inlined():
    """A class with no identifier is always inlined (no way to reference it)."""
    schema = """
id: https://example.org/noid
name: noid_test
default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  Point:
    slots:
      - x
      - y

  Shape:
    slots:
      - vertices

slots:
  x:
    range: integer
    required: true
  y:
    range: integer
    required: true
  vertices:
    range: Point
    multivalued: true
"""
    module = GolangGenerator(schema=schema).render()
    shape = module.structs["Shape"]

    # Point has no identifier → auto-inlined → []Point
    assert shape.fields["vertices"].type == "[]Point"
    # No type alias should be generated
    assert "PointId" not in module.structs
