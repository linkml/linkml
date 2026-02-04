"""Tests for SQL Validation Generator."""

import sqlite3

import pytest
import yaml
from click.testing import CliRunner

from linkml.generators.sqltablegen import SQLTableGenerator
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

    assert "identifier" in minimal_schema_queries
    assert ".id" in minimal_schema_queries
    assert "GROUP BY" in minimal_schema_queries
    assert "count(*) > 1" in minimal_schema_queries


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

    assert "unique_key" in queries
    assert "first_name" in queries and "last_name" in queries
    assert "GROUP BY" in queries
    assert "count(*) > 1" in queries
    # Should concatenate values with pipe separator
    assert "||" in queries or "CONCAT" in queries


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


def test_with_kitchen_sink_schema(input_path):
    """Test with the kitchen_sink.yaml schema."""
    schema = str(input_path("kitchen_sink.yaml"))
    gen = SQLValidationGenerator(schema)
    queries = gen.generate_validation_queries()

    # Should find constraints in personinfo schema
    # age_in_years has alias 'age' and min=0, max=999
    assert "age_in_years" in queries
    assert "age_in_years < 0" in queries
    assert "age_in_years > 999" in queries

    assert "REGEXP" in queries

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

    assert 'WHERE "Record".id IS NULL' in queries
    assert "count(*) > 1" in queries
    assert "UNION ALL" in queries


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
    assert "UNION ALL" in result.output


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
    assert ".id" in queries
    assert ".code" in queries
    assert "UNION ALL" in queries


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


def test_union_all_combination(minimal_schema):
    """Test that all validation queries are combined with UNION ALL."""
    gen = SQLValidationGenerator(minimal_schema)
    queries = gen.generate_validation_queries()

    assert "UNION ALL" in queries

    # Should have only one semicolon at the end
    assert queries.count(";") == 1
    assert queries.rstrip().endswith(";")

    # Should have standardized columns in output
    assert "table_name" in queries
    assert "column_name" in queries
    assert "constraint_type" in queries
    assert "record_id" in queries
    assert "invalid_value" in queries


@pytest.mark.slow
def test_validation_interop_with_valid_data(input_path, tmp_path):
    """Test validation queries against a real SQLite database with valid data.

    This test verifies interoperability between SQLTableGenerator and
    SQLValidationGenerator by:
    1. Creating a database schema using SQLTableGenerator
    2. Populating it with valid data
    3. Running validation queries - should find no violations
    """

    schema_path = str(input_path("kitchen_sink.yaml"))
    table_gen = SQLTableGenerator(schema_path, dialect="sqlite")
    ddl = table_gen.generate_ddl()

    # Create SQLite database and execute DDL
    db_path = tmp_path / "valid_test.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.executescript(ddl)

    cursor.execute('INSERT INTO "Person" (id, name, age_in_years) VALUES (?, ?, ?)', ("P:001", "John Doe", 30))
    cursor.execute(
        'INSERT INTO "Person" (id, name, age_in_years) VALUES (?, ?, ?)',
        ("P:002", "Jane Smith", 0),  # Edge case: minimum valid age
    )
    cursor.execute(
        'INSERT INTO "Person" (id, name, age_in_years) VALUES (?, ?, ?)',
        ("P:003", "Old Person", 999),  # Edge case: maximum valid age
    )

    conn.commit()

    # Generate and execute validation queries (skip pattern checks for SQLite since REGEXP is
    # a module that is not available in standard sqlite)
    val_gen = SQLValidationGenerator(schema_path, dialect="sqlite", check_patterns=False)
    validation_query = val_gen.generate_validation_queries()

    cursor.execute(validation_query)
    violations = cursor.fetchall()

    assert len(violations) == 0, f"Expected no violations but found: {violations}"

    conn.close()


@pytest.mark.slow
def test_validation_interop_with_invalid_data(input_path, tmp_path):
    """Test validation queries against a real SQLite database with invalid data.

    This test verifies interoperability between SQLTableGenerator and
    SQLValidationGenerator by:
    1. Creating a database schema using SQLTableGenerator
    2. Populating it with invalid data
    3. Running validation queries - should detect violations
    """
    schema_path = str(input_path("kitchen_sink.yaml"))
    table_gen = SQLTableGenerator(schema_path, dialect="sqlite")
    ddl = table_gen.generate_ddl()

    # Create SQLite database and execute DDL
    db_path = tmp_path / "invalid_test.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.executescript(ddl)

    # Note: We test violations that SQL DDL doesn't enforce (range checks, etc.)
    # SQL UNIQUE/NOT NULL constraints would prevent insertion, pattern checks require
    # REGEXP to be present in sqlite which it is not by default

    cursor.execute('INSERT INTO "Person" (id, name, age_in_years) VALUES (?, ?, ?)', ("P:001", "Negative Age", -5))
    cursor.execute('INSERT INTO "Person" (id, name, age_in_years) VALUES (?, ?, ?)', ("P:002", "Too Old", 1000))
    cursor.execute('INSERT INTO "Person" (id, name, age_in_years) VALUES (?, ?, ?)', ("P:003", "Way Too Old", 5000))

    conn.commit()

    # Generate and execute validation queries (skip pattern checks for SQLite)
    val_gen = SQLValidationGenerator(schema_path, dialect="sqlite", check_patterns=False)
    validation_query = val_gen.generate_validation_queries()

    cursor.execute(validation_query)
    violations = cursor.fetchall()

    assert len(violations) > 0, "Expected to find violations but found none"
    assert any("range" in str(v).lower() for v in violations), (
        f"Should detect age range violations. Violations found: {violations}"
    )
    invalid_ages = {v[4] for v in violations if v[1] == "age_in_years"}  # invalid_value at index 4
    assert any(int(age) < 0 or int(age) > 999 for age in invalid_ages if age is not None), (
        f"Should detect out-of-range ages. Found ages: {invalid_ages}"
    )

    conn.close()
