"""Tests for the Solr schema generator."""

import json

import pytest
from click.testing import CliRunner

from linkml.generators.solrgen import SolrSchemaGenerator, cli


def test_solr_basic_generation(input_path):
    """
    Test basic Solr schema generation from a LinkML schema.
    """
    schema_path = str(input_path("organization.yaml"))
    generator = SolrSchemaGenerator(schema_path)

    # Generate schema
    output = generator.serialize()

    # Verify it's valid JSON
    schema = json.loads(output)
    assert "add-field" in schema

    # Check that fields were generated
    fields = schema["add-field"]
    assert len(fields) > 0

    # Verify field structure
    field_names = [f["name"] for f in fields]
    assert "id" in field_names
    assert "name" in field_names

    # Check field types
    for field in fields:
        assert "name" in field
        assert "type" in field


def test_solr_field_types(input_path):
    """
    Test that LinkML types are correctly mapped to Solr types.
    """
    schema_path = str(input_path("organization.yaml"))
    generator = SolrSchemaGenerator(schema_path)

    output = generator.serialize()
    schema = json.loads(output)
    fields = {f["name"]: f for f in schema["add-field"]}

    # String fields should map to 'string' type
    assert fields["id"]["type"] == "string"
    assert fields["name"]["type"] == "string"

    # Integer fields should map to 'int' type
    if "age_in_years" in fields:
        assert fields["age_in_years"]["type"] == "int"


def test_solr_multivalued_fields(input_path):
    """
    Test that multivalued slots generate multiValued=true in Solr.
    """
    schema_path = str(input_path("organization.yaml"))
    generator = SolrSchemaGenerator(schema_path)

    output = generator.serialize()
    schema = json.loads(output)
    fields = {f["name"]: f for f in schema["add-field"]}

    # Check for multivalued fields (aliases is multivalued in organization.yaml)
    if "aliases" in fields:
        assert fields["aliases"].get("multiValued") is True


def test_solr_class_references(input_path):
    """
    Test that class references are treated as string fields.
    """
    schema_path = str(input_path("organization.yaml"))
    generator = SolrSchemaGenerator(schema_path)

    output = generator.serialize()
    schema = json.loads(output)
    fields = {f["name"]: f for f in schema["add-field"]}

    # has_boss references Manager class, should be string
    if "has_boss" in fields:
        assert fields["has_boss"]["type"] == "string"

    # has_employees references Employee class, should be string
    if "has_employees" in fields:
        assert fields["has_employees"]["type"] == "string"


def test_solr_top_class_option(input_path):
    """
    Test generating schema for a specific class only.
    """
    schema_path = str(input_path("organization.yaml"))

    # Generate for all classes
    generator_all = SolrSchemaGenerator(schema_path)
    output_all = generator_all.serialize()
    schema_all = json.loads(output_all)
    all_fields = {f["name"] for f in schema_all["add-field"]}

    # Generate for Employee class only
    generator_employee = SolrSchemaGenerator(schema_path)
    output_employee = generator_employee.class_schema("employee")
    schema_employee = json.loads(output_employee)
    employee_fields = {f["name"] for f in schema_employee["add-field"]}

    # Employee-specific fields should be present
    assert "first_name" in employee_fields or "first name" in employee_fields

    # The top class output should have fewer or equal fields than all classes
    assert len(employee_fields) <= len(all_fields)


def test_solr_json_format(input_path):
    """
    Test that output is properly formatted JSON with correct field naming.
    """
    schema_path = str(input_path("organization.yaml"))
    generator = SolrSchemaGenerator(schema_path)

    output = generator.serialize()

    # Should be valid JSON
    schema = json.loads(output)

    # Keys should use hyphen format (add-field, not add_field)
    assert "add-field" in schema

    # Should not have underscore versions
    assert "add_field" not in schema


def test_solr_cli_basic(input_path):
    """
    Test the CLI interface for basic schema generation.
    """
    runner = CliRunner()
    schema_path = str(input_path("organization.yaml"))

    result = runner.invoke(cli, [schema_path])

    # Should succeed
    assert result.exit_code == 0

    # Output should be valid JSON
    schema = json.loads(result.output)
    assert "add-field" in schema
    assert len(schema["add-field"]) > 0


def test_solr_cli_top_class(input_path):
    """
    Test the CLI with --top-class option.
    """
    runner = CliRunner()
    schema_path = str(input_path("organization.yaml"))

    result = runner.invoke(cli, [schema_path, "--top-class", "employee"])

    # Should succeed
    assert result.exit_code == 0

    # Output should be valid JSON
    schema = json.loads(result.output)
    assert "add-field" in schema

    # Should have employee-related fields
    field_names = [f["name"] for f in schema["add-field"]]
    assert any("first" in name.lower() for name in field_names)


def test_solr_empty_transaction(tmp_path):
    """
    Test that a schema with no classes produces an empty field list.
    """
    # Minimal schema with no classes
    minimal_schema = """
id: http://example.org/minimal
name: minimal
"""

    # Write to temporary file
    schema_file = tmp_path / "minimal.yaml"
    schema_file.write_text(minimal_schema)

    generator = SolrSchemaGenerator(str(schema_file))
    output = generator.serialize()
    schema = json.loads(output)

    # Should have add-field key but empty list
    assert "add-field" in schema
    assert schema["add-field"] == []


def test_solr_field_deduplication(input_path):
    """
    Test that duplicate field names across classes are deduplicated.

    Since Solr doesn't have class hierarchy, fields with the same name
    should only appear once in the output.
    """
    schema_path = str(input_path("organization.yaml"))
    generator = SolrSchemaGenerator(schema_path)

    output = generator.serialize()
    schema = json.loads(output)

    # Count field occurrences
    field_names = [f["name"] for f in schema["add-field"]]

    # Each field name should appear exactly once
    assert len(field_names) == len(set(field_names))


@pytest.mark.parametrize(
    "linkml_type,expected_solr_type",
    [
        ("string", "string"),
        ("integer", "int"),
        ("boolean", "boolean"),
        ("float", "pfloat"),
        ("double", "pdouble"),
    ],
)
def test_solr_type_mapping(tmp_path, linkml_type, expected_solr_type):
    """
    Test type mapping from LinkML to Solr types.
    """
    schema = f"""
id: http://example.org/test
name: test

classes:
  TestClass:
    attributes:
      test_field:
        range: {linkml_type}
"""

    # Write to temporary file
    schema_file = tmp_path / f"test_{linkml_type}.yaml"
    schema_file.write_text(schema)

    generator = SolrSchemaGenerator(str(schema_file))
    output = generator.serialize()
    result = json.loads(output)

    fields = {f["name"]: f for f in result["add-field"]}
    assert "test_field" in fields
    assert fields["test_field"]["type"] == expected_solr_type


def test_solr_enum_handling(tmp_path):
    """
    Test that enum ranges are mapped to string type in Solr.
    """
    schema = """
id: http://example.org/test
name: test

enums:
  StatusEnum:
    permissible_values:
      active:
      inactive:
      pending:

classes:
  TestClass:
    attributes:
      status:
        range: StatusEnum
"""

    # Write to temporary file
    schema_file = tmp_path / "test_enum.yaml"
    schema_file.write_text(schema)

    generator = SolrSchemaGenerator(str(schema_file))
    output = generator.serialize()
    result = json.loads(output)

    fields = {f["name"]: f for f in result["add-field"]}
    assert "status" in fields
    # Enums should be mapped to string type
    assert fields["status"]["type"] == "string"
