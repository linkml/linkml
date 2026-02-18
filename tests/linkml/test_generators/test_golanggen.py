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

slots:
  name:
    range: string
    required: true
    identifier: true
  age:
    range: integer
  email:
    range: string
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
    assert 'omitempty' in code


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
        ("age", "int"),
    ],
    ids=["string_slot", "integer_slot"],
)
def test_type_mapping(slot_name, expected_type):
    """Test that LinkML types are correctly mapped to Go types."""
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


def test_package_name_derived():
    """Test that the package name is derived from the schema name."""
    module = GolangGenerator(schema=SIMPLE_SCHEMA).render()
    assert module.package_name == "simple"


def test_package_name_override():
    """Test that --package-name overrides the derived value."""
    module = GolangGenerator(schema=SIMPLE_SCHEMA, package_name="mypkg").render()
    assert module.package_name == "mypkg"


def test_imports_time_package():
    """Test that the time package is imported when date/time types are used."""
    schema = """
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

slots:
  started_at:
    range: date
"""
    code = GolangGenerator(schema=schema).serialize()
    assert '"time"' in code
    assert "time.Time" in code


def test_root_struct_names():
    """Test that root_struct_names excludes classes used as field types."""
    module = GolangGenerator(schema=COMPOSITION_SCHEMA).render()

    # Address is referenced by Person.address → not root
    # Person is referenced by Dataset.persons and Person.friends → not root
    # Dataset is never referenced as a field type → root
    assert "Dataset" in module.root_struct_names
    assert "Address" not in module.root_struct_names
    assert "Person" not in module.root_struct_names


def test_root_struct_names_no_references():
    """When no class references another, all are root classes."""
    module = GolangGenerator(schema=SIMPLE_SCHEMA).render()
    assert "Person" in module.root_struct_names


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
        '{% if imports and imports.strip() %}\n'
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
