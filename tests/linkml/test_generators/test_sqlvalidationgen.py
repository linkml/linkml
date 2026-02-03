"""Tests for SQL Validation Generator."""

import pytest
import yaml
from click.testing import CliRunner

from linkml.generators.sqlvalidationgen import SQLValidationGenerator, cli
from linkml.utils.schema_builder import SchemaBuilder
from linkml_runtime.linkml_model.meta import SlotDefinition, UniqueKey


@pytest.fixture
def minimal_schema():
    """Create a minimal schema with various constraints for testing."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("name", required=True))
    b.add_slot(SlotDefinition("age", range="integer", minimum_value=0, maximum_value=120))
    b.add_slot(SlotDefinition("email", pattern=r"^\S+@[\S+\.]+\S+"))
    b.add_class("Person", slots=["id", "name", "age", "email"])
    b.add_defaults()
    return b.schema


@pytest.fixture
def minimal_schema_queries(minimal_schema):
    """Create the validation queries from the minimal schema."""
    gen = SQLValidationGenerator(minimal_schema)
    return gen.generate_validation_queries()


def test_output_format_standardization(minimal_schema_queries):
    """Test that output has standardized column names."""

    assert "table_name" in minimal_schema_queries
    assert "column_name" in minimal_schema_queries
    assert "constraint_type" in minimal_schema_queries


def test_required_constraint(minimal_schema_queries):
    """Test generation of required field validation query."""
    assert "name" in minimal_schema_queries
    assert "required" in minimal_schema_queries
    assert "name IS NULL" in minimal_schema_queries
    assert "Person" in minimal_schema_queries


def test_minimum_value_constraint(minimal_schema_queries):
    """Test generation of minimum value validation query."""

    assert "age" in minimal_schema_queries
    assert "age < 0" in minimal_schema_queries
    assert "range" in minimal_schema_queries


def test_maximum_value_constraint(minimal_schema_queries):
    """Test generation of maximum value validation query."""

    assert "age" in minimal_schema_queries
    assert "age > 120" in minimal_schema_queries
    assert "range" in minimal_schema_queries


def test_range_constraint_combined(minimal_schema_queries):
    """Test that min and max constraints are combined in one query."""

    assert (
        "age < 0" in minimal_schema_queries
        and "age > 120" in minimal_schema_queries
        and " OR " in minimal_schema_queries
    )


def test_pattern_constraint(minimal_schema):
    """Test generation of pattern validation query."""
    gen = SQLValidationGenerator(minimal_schema, dialect="postgresql")
    queries = gen.generate_validation_queries()

    # Should check email pattern
    assert "email" in queries
    assert "pattern" in queries
    # PostgreSQL uses ~ operator
    assert "~" in queries or "REGEXP" in queries


def test_identifier_uniqueness(minimal_schema_queries):
    """Test generation of identifier uniqueness validation query."""

    # Should check for duplicate id values
    assert "identifier" in minimal_schema_queries
    assert "GROUP BY" in minimal_schema_queries and ".id" in minimal_schema_queries
    assert "HAVING" in minimal_schema_queries and "count(*) > 1" in minimal_schema_queries


def test_unique_key_constraint():
    """Test generation of unique key validation query."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("first_name"))
    b.add_slot(SlotDefinition("last_name"))
    b.add_class(
        "Person",
        slots=["id", "first_name", "last_name"],
        unique_keys={"name_key": UniqueKey(unique_key_name="name_key", unique_key_slots=["first_name", "last_name"])},
    )
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema)
    queries = gen.generate_validation_queries()

    # Should check for duplicate name combinations
    assert "unique_key" in queries
    assert "first_name" in queries and "last_name" in queries
    assert "GROUP BY" in queries
    assert "HAVING" in queries and "count(*) > 1" in queries


def test_enum_constraint():
    """Test generation of enum validation query."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("status", range="StatusEnum"))
    b.add_enum("StatusEnum", permissible_values=["active", "inactive", "pending"])
    b.add_class("Record", slots=["id", "status"])
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema)
    queries = gen.generate_validation_queries()

    # Should check values against enum
    assert "enum" in queries
    assert "NOT IN" in queries
    assert "active" in queries
    assert "inactive" in queries
    assert "pending" in queries


@pytest.mark.parametrize(
    "dialect,pattern_syntax",
    [
        ("postgresql", "~"),
        ("mysql", "REGEXP"),
        ("oracle", "REGEXP_LIKE"),
        ("sqlite", "REGEXP"),
    ],
)
def test_dialect_specific_pattern(minimal_schema, dialect, pattern_syntax):
    """Test dialect-specific pattern matching syntax."""
    gen = SQLValidationGenerator(minimal_schema, dialect=dialect)
    queries = gen.generate_validation_queries()

    assert pattern_syntax in queries


def test_with_personinfo_schema(input_path):
    """Test with the personinfo.yaml schema."""
    schema = str(input_path("personinfo.yaml"))
    gen = SQLValidationGenerator(schema)
    queries = gen.generate_validation_queries()

    # Should find constraints in personinfo schema
    # age_in_years has alias 'age' and min=0, max=999
    assert "age" in queries and ("age < 0" in queries or "age > 999" in queries)

    # primary_email has pattern
    assert "primary_email" in queries

    # telephone has pattern
    assert "telephone" in queries

    # name is required
    assert "name" in queries

    # Should have header
    assert "SQL Validation Queries" in queries


def test_skip_abstract_classes():
    """Test that abstract classes are skipped."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("name", required=True))
    b.add_class("AbstractPerson", slots=["id", "name"], abstract=True)
    b.add_class("ConcretePerson", is_a="AbstractPerson", slots=["id", "name"])
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema)
    queries = gen.generate_validation_queries()

    assert "AbstractPerson" not in queries
    assert "ConcretePerson" in queries


def test_check_required_disabled(minimal_schema):
    """Test disabling required field checks."""
    gen = SQLValidationGenerator(minimal_schema, check_required=False)
    queries = gen.generate_validation_queries()

    assert "name IS NULL" not in queries


def test_check_ranges_disabled(minimal_schema):
    """Test disabling range checks."""
    gen = SQLValidationGenerator(minimal_schema, check_ranges=False)
    queries = gen.generate_validation_queries()

    assert "age < 0" not in queries
    assert "age > 120" not in queries


def test_check_patterns_disabled(minimal_schema):
    """Test disabling pattern checks."""
    gen = SQLValidationGenerator(minimal_schema, check_patterns=False)
    queries = gen.generate_validation_queries()

    assert "pattern" not in queries
    assert "REGEXP" not in queries


def test_include_comments_disabled(minimal_schema):
    """Test disabling comments in output."""
    gen = SQLValidationGenerator(minimal_schema, include_comments=False)
    queries = gen.generate_validation_queries()

    assert "-- Validation:" not in queries
    assert "-- Constraint:" not in queries


def test_empty_schema():
    """Test with schema that has no constraints."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("data"))  # No constraints
    b.add_class("Record", slots=["id", "data"])
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema)
    queries = gen.generate_validation_queries()

    # Not null check for identifier
    assert 'WHERE "Record".id IS NULL' in queries
    # Uniqueness check for identifier
    assert "HAVING count(*) > 1;" in queries


def test_multiple_constraints_same_field():
    """Test field with multiple constraint types."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("age", range="integer", required=True, minimum_value=0, maximum_value=120))
    b.add_class("Person", slots=["id", "age"])
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema)
    queries = gen.generate_validation_queries()

    assert "age IS NULL" in queries
    assert "age < 0" in queries and "age > 120" in queries


def test_cli_basic(tmp_path):
    """Test CLI with basic schema."""
    # Create a test schema file
    schema_path = tmp_path / "test_schema.yaml"
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("age", range="integer", maximum_value=120))
    b.add_class("Person", slots=["id", "age"])
    b.add_defaults()

    with open(schema_path, "w") as f:
        yaml.dump(b.as_dict(), f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_path)])
    # Should succeed
    assert result.exit_code == 0
    # Should contain validation query
    assert "age > 120" in result.output
    assert "SELECT" in result.output
    assert "HAVING count(*) > 1;" in result.output


def test_cli_with_dialect(tmp_path):
    """Test CLI with different dialects."""
    # Create a test schema file with pattern
    schema_path = tmp_path / "test_schema.yaml"
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("email", pattern=r"^\S+@\S+$"))
    b.add_class("Person", slots=["id", "email"])
    b.add_defaults()

    with open(schema_path, "w") as f:
        yaml.dump(b.as_dict(), f)

    # Test PostgreSQL dialect
    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_path), "--dialect", "postgresql"])

    assert result.exit_code == 0
    assert "~" in result.output  # PostgreSQL regex operator

    # Test MySQL dialect
    result = runner.invoke(cli, [str(schema_path), "--dialect", "mysql"])

    assert result.exit_code == 0
    assert "REGEXP" in result.output


def test_cli_with_options(tmp_path):
    """Test CLI with selective validation options."""
    # Create a test schema with multiple constraint types
    schema_path = tmp_path / "test_schema.yaml"
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("name", required=True))
    b.add_slot(SlotDefinition("age", range="integer", maximum_value=120))
    b.add_slot(SlotDefinition("email", pattern=r"^\S+@\S+$"))
    b.add_class("Person", slots=["id", "name", "age", "email"])
    b.add_defaults()

    with open(schema_path, "w") as f:
        yaml.dump(b.as_dict(), f)

    # Run with --no-check-patterns
    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_path), "--no-check-patterns"])

    assert result.exit_code == 0

    assert "age > 120" in result.output
    assert "pattern" not in result.output
    assert "REGEXP" not in result.output


def test_inherited_constraints():
    """Test that inherited constraints are captured via induced_slot."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("base_field", required=True))
    b.add_slot(SlotDefinition("age", range="integer", maximum_value=120))
    b.add_class("BaseClass", slots=["id", "base_field", "age"])
    b.add_class("DerivedClass", is_a="BaseClass", slots=["id", "base_field", "age"])
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema)
    queries = gen.generate_validation_queries()

    assert "DerivedClass" in queries
    assert "base_field IS NULL" in queries
    assert "age > 120" in queries


def test_key_vs_identifier():
    """Test distinction between key and identifier constraints."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("code", key=True))
    b.add_class("Record", slots=["id", "code"])
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema)
    queries = gen.generate_validation_queries()

    # Should check both identifier and key uniqueness
    assert "identifier" in queries
    assert "key" in queries
    # Should have separate checks for id and code
    assert 'GROUP BY "Record".id' in queries
    assert ".id IS NULL" in queries
    assert 'GROUP BY "Record".code' in queries
    assert ".code IS NULL" in queries


# TODO: Is this test necessary? Or is this special character thing
# just testing sqlalchemy behaviour?
def test_special_characters_in_pattern():
    """Test pattern with special characters that need escaping."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    # Pattern with single quote
    b.add_slot(SlotDefinition("data", pattern=r"test'pattern"))
    b.add_class("Record", slots=["id", "data"])
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema, dialect="postgresql")
    queries = gen.generate_validation_queries()

    # Should escape the single quote
    assert "test''pattern" in queries or "test'pattern" in queries


def test_serialize_method(minimal_schema):
    """Test that serialize() method works as entry point."""
    gen = SQLValidationGenerator(minimal_schema)
    queries = gen.serialize()

    # Should produce same output as generate_validation_queries
    assert "SELECT" in queries
    assert len(queries) > 10
