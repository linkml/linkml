"""Tests for SQL Validation Generator."""

import logging
import re
import sqlite3

import pytest
import yaml
from click.testing import CliRunner

from linkml.generators.sqltablegen import SQLTableGenerator
from linkml.generators.sqlvalidationgen import SQLValidationGenerator, cli
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.linkml_model.meta import (
    AnonymousClassExpression,
    ClassRule,
    SlotDefinition,
    UniqueKey,
)
from linkml_runtime.utils.schema_builder import SchemaBuilder


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


def test_single_column_unique_key():
    """Single-column unique key should use simple IN subquery, not tuple syntax."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("code"))
    b.add_class(
        "Item",
        slots=["id", "code"],
        unique_keys={"code_key": UniqueKey(unique_key_name="code_key", unique_key_slots=["code"])},
    )
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema)
    queries = gen.generate_validation_queries()

    assert "unique_key" in queries
    assert "code" in queries
    assert "GROUP BY" in queries
    # Single-column path does not use tuple syntax
    assert "ROW(" not in queries


def test_multi_column_unique_key():
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


def test_unique_key_with_aliased_slot():
    """Unique key slots are given as slot names, but the columns are named after the alias."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("first name"))
    b.add_slot(SlotDefinition("last name"))
    b.add_class(
        "Person",
        slots=["id", "first name", "last name"],
        slot_usage={"first name": SlotDefinition("first name", alias="given_name")},
        unique_keys={"name_key": UniqueKey(unique_key_name="name_key", unique_key_slots=["first name", "last name"])},
    )
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema)
    queries = gen.generate_validation_queries()

    assert "unique_key" in queries
    assert "GROUP BY given_name, last_name" in queries
    assert "first_name" not in queries


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
        ("sqlite", "REGEXP"),
    ],
)
def test_dialect_specific_pattern(minimal_schema, dialect, pattern_syntax):
    """Test dialect-specific pattern matching syntax."""
    gen = SQLValidationGenerator(minimal_schema, dialect=dialect)
    queries = gen.generate_validation_queries()

    assert pattern_syntax in queries


@pytest.mark.parametrize("dialect", ["postgresql", "sqlite"])
def test_pattern_check_guards_against_null(minimal_schema, dialect):
    """Pattern checks must exclude NULLs: absence of a value is the required constraint's concern.

    On SQLite the guard is also what keeps NULLs out of the user-registered REGEXP
    function, see test_pattern_check_ignores_nulls_sqlite.
    """
    gen = SQLValidationGenerator(minimal_schema, dialect=dialect)
    queries = gen.generate_validation_queries()

    pattern_query = next(q for q in queries.split("UNION ALL") if "'pattern'" in q)

    assert "email IS NOT NULL" in pattern_query


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


def test_check_enums_disabled():
    """Test disabling enum constraint checks."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("status", range="StatusEnum"))
    b.add_enum("StatusEnum", permissible_values=["active", "inactive", "pending"])
    b.add_class("Record", slots=["id", "status"])
    b.add_defaults()
    gen = SQLValidationGenerator(b.schema, check_enums=False)
    queries = gen.generate_validation_queries()

    assert "enum" not in queries
    assert " NOT IN " not in queries


def test_check_unique_keys_disabled():
    """Test disabling unique_keys constraint checks."""
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
    gen = SQLValidationGenerator(b.schema, check_unique_keys=False)
    queries = gen.generate_validation_queries()
    assert "unique_key" not in queries


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


@pytest.mark.slow
def test_pattern_check_ignores_nulls_sqlite(tmp_path):
    """Executing pattern checks against SQLite must survive NULLs in the constrained column.

    SQLite has no built-in REGEXP: the operator dispatches to a scalar function the
    application registers, and SQLite hands that function a NULL argument rather than
    short-circuiting the way a native operator would. The function registered here is
    deliberately NULL-intolerant (the idiomatic implementation), so an unguarded pattern
    check surfaces as sqlite3.OperationalError and takes down the entire UNION ALL query.

    Unlike the other interop tests, this one leaves check_patterns enabled.
    """
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    # optional, so NULL is a legal value despite the pattern
    b.add_slot(SlotDefinition("email", pattern=r"^\S+@\S+$"))
    b.add_class("Person", slots=["id", "email"])
    b.add_defaults()
    schema = b.schema

    ddl = SQLTableGenerator(schema, dialect="sqlite").generate_ddl()
    validation_sql = SQLValidationGenerator(schema, dialect="sqlite").generate_validation_queries()

    conn = sqlite3.connect(str(tmp_path / "pattern_null_test.db"))
    conn.create_function("regexp", 2, lambda pattern, value: re.search(pattern, value) is not None)
    cursor = conn.cursor()
    cursor.executescript(ddl)

    cursor.execute('INSERT INTO "Person" (id, email) VALUES (?, ?)', ("P:001", "jane@example.com"))
    cursor.execute('INSERT INTO "Person" (id, email) VALUES (?, ?)', ("P:002", None))
    cursor.execute('INSERT INTO "Person" (id, email) VALUES (?, ?)', ("P:003", "not-an-email"))
    conn.commit()

    cursor.execute(validation_sql)
    violations = cursor.fetchall()
    conn.close()

    pattern_violations = [v for v in violations if v[2] == "pattern"]
    assert [v[3] for v in pattern_violations] == ["P:003"], (
        f"Only the malformed email should be a pattern violation, got: {pattern_violations}"
    )


def _schema_with_rules(
    rules: list[ClassRule],
    slots: list[SlotDefinition] | None = None,
    class_name: str = "LivingThings",
) -> SchemaDefinition:
    """Helper to build a schema with rules on a class.

    :param rules: list of ClassRule objects
    :param slots: list of SlotDefinition objects (defaults to id/type/age)
    :param class_name: class name to apply rules to
    :return: schema object
    """
    b = SchemaBuilder()
    if slots is None:
        slots = [
            SlotDefinition("id", identifier=True),
            SlotDefinition("type"),
            SlotDefinition("age", range="integer"),
        ]
    for s in slots:
        b.add_slot(s)
    b.add_class(class_name, slots=[s.name for s in slots])
    b.add_defaults()
    # Attach rules directly
    b.schema.classes[class_name].rules = rules
    return b.schema


def test_simple_rule_equals_string_and_maximum_value():
    """Precondition equals_string + postcondition maximum_value."""
    schema = _schema_with_rules(
        [
            ClassRule(
                preconditions=AnonymousClassExpression(
                    slot_conditions={"type": SlotDefinition("type", equals_string="Human")},
                ),
                postconditions=AnonymousClassExpression(
                    slot_conditions={"age": SlotDefinition("age", maximum_value=150)},
                ),
            )
        ]
    )
    gen = SQLValidationGenerator(schema)
    sql = gen.generate_validation_queries()

    # Precondition positive: type = 'Human'
    assert "type" in sql
    assert "'Human'" in sql
    # Postcondition negated: age > 150
    assert "age > 150" in sql
    assert "'rule'" in sql


@pytest.mark.parametrize(
    "preconditions,postconditions,expected_sql,unexpected_sql",
    [
        pytest.param(
            {"type": SlotDefinition("type", equals_string_in=["Human", "Elf"])},
            {"age": SlotDefinition("age", maximum_value=500)},
            ["IN", "'Human'", "'Elf'", "age > 500"],
            [],
            id="equals_string_in-precondition_maximum_value-postcondition",
        ),
        pytest.param(
            {"type": SlotDefinition("type", equals_string="Adult")},
            {"age": SlotDefinition("age", minimum_value=18)},
            ["age < 18"],
            [],
            id="minimum_value-postcondition",
        ),
        pytest.param(
            None,
            {"age": SlotDefinition("age", maximum_value=200)},
            ["age > 200"],
            ["'Human'"],  # no preconditions → no precondition clause
            id="postcondition-only",
        ),
        pytest.param(
            {"type": SlotDefinition("type", equals_string="Human")},
            {
                "age": SlotDefinition("age", maximum_value=150),
                "weight": SlotDefinition("weight", maximum_value=500),
            },
            ["age > 150", "weight > 500", " OR "],
            [],
            id="multiple-postcondition-slots",
        ),
        pytest.param(
            {"type": SlotDefinition("type", equals_string="Human")},
            {"name": SlotDefinition("name", required=True)},
            ["name IS NULL"],
            [],
            id="required-postcondition",
        ),
        pytest.param(
            {"age": SlotDefinition("age", equals_number=0)},
            {"type": SlotDefinition("type", equals_string="Newborn")},
            ["age = 0"],
            [],
            id="equals_number-precondition",
        ),
    ],
)
def test_rule_slot_condition_types(
    preconditions: dict[str, SlotDefinition] | None,
    postconditions: dict[str, SlotDefinition],
    expected_sql: list[str],
    unexpected_sql: list[str],
) -> None:
    """Various slot condition types in rule pre/postconditions.

    :param preconditions: slot_conditions for the rule preconditions, or None for no preconditions
    :param postconditions: slot_conditions for the rule postconditions
    :param expected_sql: SQL fragments that must appear in the generated queries
    :param unexpected_sql: SQL fragments that must not appear in the generated queries
    """
    slots = [
        SlotDefinition("id", identifier=True),
        SlotDefinition("type"),
        SlotDefinition("age", range="integer"),
        SlotDefinition("weight", range="integer"),
        SlotDefinition("name"),
    ]
    rule = ClassRule(postconditions=AnonymousClassExpression(slot_conditions=postconditions))
    if preconditions is not None:
        rule.preconditions = AnonymousClassExpression(slot_conditions=preconditions)

    schema = _schema_with_rules([rule], slots=slots)
    gen = SQLValidationGenerator(schema)
    sql = gen.generate_validation_queries()

    for fragment in expected_sql:
        assert fragment in sql
    for fragment in unexpected_sql:
        assert fragment not in sql


def test_check_rules_disabled():
    """check_rules=False should suppress all rule SQL."""
    schema = _schema_with_rules(
        [
            ClassRule(
                preconditions=AnonymousClassExpression(
                    slot_conditions={"type": SlotDefinition("type", equals_string="Human")},
                ),
                postconditions=AnonymousClassExpression(
                    slot_conditions={"age": SlotDefinition("age", maximum_value=150)},
                ),
            )
        ]
    )
    gen = SQLValidationGenerator(schema, check_rules=False)
    sql = gen.generate_validation_queries()

    assert "'rule'" not in sql


def test_rule_deactivated():
    """Deactivated rules should be skipped."""
    schema = _schema_with_rules(
        [
            ClassRule(
                preconditions=AnonymousClassExpression(
                    slot_conditions={"type": SlotDefinition("type", equals_string="Human")},
                ),
                postconditions=AnonymousClassExpression(
                    slot_conditions={"age": SlotDefinition("age", maximum_value=150)},
                ),
                deactivated=True,
            )
        ]
    )
    gen = SQLValidationGenerator(schema)
    sql = gen.generate_validation_queries()

    assert "'rule'" not in sql


def test_cli_check_rules_option(tmp_path):
    """CLI --no-check-rules suppresses rule queries."""
    schema = _schema_with_rules(
        [
            ClassRule(
                postconditions=AnonymousClassExpression(
                    slot_conditions={"age": SlotDefinition("age", maximum_value=150)},
                ),
            )
        ]
    )
    schema_path = tmp_path / "rules_schema.yaml"
    from linkml_runtime.dumpers import yaml_dumper

    with open(schema_path, "w") as f:
        f.write(yaml_dumper.dumps(schema))

    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_path), "--no-check-rules"])
    assert result.exit_code == 0
    assert "'rule'" not in result.output


@pytest.mark.parametrize(
    "slot_condition_kwargs",
    [
        {"equals_string": "Alive"},
        {"equals_number": 1},
        {"equals_string_in": ["Alive", "Dormant"]},
    ],
)
def test_rule_equals_postcondition_null_safe(slot_condition_kwargs):
    """Negated equals-type postcondition checks must treat NULL as a violation.

    SQL's three-valued logic makes `col != lit` and `col NOT IN (...)` evaluate to
    NULL (not TRUE) when col is NULL, silently dropping the row from the WHERE
    clause. The generated SQL must explicitly OR in an `IS NULL` check so that a
    NULL value in a postcondition column is treated as failing the postcondition.
    """
    schema = _schema_with_rules(
        [
            ClassRule(
                preconditions=AnonymousClassExpression(
                    slot_conditions={"type": SlotDefinition("type", equals_string="Human")},
                ),
                postconditions=AnonymousClassExpression(
                    slot_conditions={"status": SlotDefinition("status", **slot_condition_kwargs)},
                ),
            )
        ],
        slots=[
            SlotDefinition("id", identifier=True),
            SlotDefinition("type"),
            SlotDefinition("status"),
        ],
    )
    gen = SQLValidationGenerator(schema)
    sql = gen.generate_validation_queries()

    rule_query = next(q for q in sql.split("UNION ALL") if "'rule'" in q)
    assert "status IS NULL" in rule_query


@pytest.mark.slow
def test_rule_interop_equals_string_null_is_violation(tmp_path):
    """A NULL value in a postcondition equals_string column must be detected as a violation."""
    schema = _schema_with_rules(
        [
            ClassRule(
                preconditions=AnonymousClassExpression(
                    slot_conditions={"type": SlotDefinition("type", equals_string="Human")},
                ),
                postconditions=AnonymousClassExpression(
                    slot_conditions={"status": SlotDefinition("status", equals_string="Alive")},
                ),
            )
        ],
        slots=[
            SlotDefinition("id", identifier=True),
            SlotDefinition("type"),
            SlotDefinition("status"),
        ],
    )
    table_gen = SQLTableGenerator(schema, dialect="sqlite")
    ddl = table_gen.generate_ddl()
    val_gen = SQLValidationGenerator(schema, dialect="sqlite", check_patterns=False)
    validation_sql = val_gen.generate_validation_queries()

    db_path = tmp_path / "rule_null_test.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.executescript(ddl)

    cursor.execute('INSERT INTO "LivingThings" (id, type, status) VALUES (?, ?, ?)', ("1", "Human", "Alive"))
    cursor.execute('INSERT INTO "LivingThings" (id, type, status) VALUES (?, ?, ?)', ("2", "Elf", None))
    cursor.execute('INSERT INTO "LivingThings" (id, type, status) VALUES (?, ?, ?)', ("3", "Human", None))
    conn.commit()

    cursor.execute(validation_sql)
    violations = cursor.fetchall()
    conn.close()

    rule_violations = [v for v in violations if v[2] == "rule"]
    violating_ids = {v[3] for v in rule_violations}
    assert "3" in violating_ids, f"Expected record 3 (NULL status) to violate rule. Violations: {rule_violations}"
    assert "2" not in violating_ids, f"Record 2 should not violate (precondition unmet). Violations: {rule_violations}"


def test_rule_slot_names_resolved_to_sql_columns():
    """Rule slot names must be resolved through alias/underscore."""
    schema = _schema_with_rules(
        [
            ClassRule(
                preconditions=AnonymousClassExpression(
                    slot_conditions={"driver status": SlotDefinition("driver status", equals_string="licensed")},
                ),
                postconditions=AnonymousClassExpression(
                    slot_conditions={"age value": SlotDefinition("age value", minimum_value=18)},
                ),
            )
        ],
        slots=[
            SlotDefinition("id", identifier=True),
            SlotDefinition("driver status"),
            SlotDefinition("age value", alias="personAge", range="integer"),
        ],
    )
    validation_sql = SQLValidationGenerator(schema, dialect="sqlite").generate_validation_queries()

    rule_query = next(q for q in validation_sql.split("UNION ALL") if "'rule'" in q)
    assert "driver_status" in rule_query, f"Spaced slot name not underscored: {rule_query}"
    assert "driver status" not in rule_query, f"Raw schema slot name leaked into SQL: {rule_query}"
    assert "personAge" in rule_query, f"Alias not resolved: {rule_query}"
    assert "age value" not in rule_query, f"Raw schema slot name leaked into SQL: {rule_query}"


@pytest.mark.slow
def test_rule_interop_sqlite(tmp_path):
    """End-to-end: create DB, insert violating data, run validation, verify detection."""
    schema = _schema_with_rules(
        [
            ClassRule(
                preconditions=AnonymousClassExpression(
                    slot_conditions={"type": SlotDefinition("type", equals_string="Human")},
                ),
                postconditions=AnonymousClassExpression(
                    slot_conditions={"age": SlotDefinition("age", maximum_value=150)},
                ),
            )
        ]
    )
    # Generate DDL and validation
    table_gen = SQLTableGenerator(schema, dialect="sqlite")
    ddl = table_gen.generate_ddl()
    val_gen = SQLValidationGenerator(schema, dialect="sqlite", check_patterns=False)
    validation_sql = val_gen.generate_validation_queries()

    db_path = tmp_path / "rules_test.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.executescript(ddl)

    # Valid: Human with age <= 150
    cursor.execute('INSERT INTO "LivingThings" (id, type, age) VALUES (?, ?, ?)', ("1", "Human", 30))
    # Valid: non-Human with age > 150 (precondition not met)
    cursor.execute('INSERT INTO "LivingThings" (id, type, age) VALUES (?, ?, ?)', ("2", "Elf", 500))
    # INVALID: Human with age > 150
    cursor.execute('INSERT INTO "LivingThings" (id, type, age) VALUES (?, ?, ?)', ("3", "Human", 200))
    conn.commit()

    cursor.execute(validation_sql)
    violations = cursor.fetchall()

    rule_violations = [v for v in violations if v[2] == "rule"]
    assert len(rule_violations) >= 1, f"Expected rule violations but got: {violations}"
    # The violating record should be id=3
    violating_ids = {v[3] for v in rule_violations}
    assert "3" in violating_ids, f"Expected record 3 to violate rule. Violations: {rule_violations}"

    conn.close()


def test_unknown_dialect_fallback(caplog):
    """Unknown dialects should log a warning and fall back to sqlite syntax (REGEXP, not ~)."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("email", pattern=r"^\S+@\S+$"))
    b.add_class("Person", slots=["id", "email"])
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema, dialect="mysql")
    with caplog.at_level(logging.WARNING, logger="linkml.generators.sqlvalidationgen"):
        queries = gen.generate_validation_queries()

    assert any("mysql" in record.message and "sqlite" in record.message for record in caplog.records)
    assert gen.dialect == "sqlite"
    # Should fall back to sqlite syntax
    assert "REGEXP" in queries
    assert "~" not in queries


def test_skip_mixin_classes():
    """Mixin classes should be excluded from generated queries."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("name", required=True))
    b.add_class("HasName", slots=["id", "name"])
    b.add_defaults()
    b.schema.classes["HasName"].mixin = True

    gen = SQLValidationGenerator(b.schema)
    queries = gen.generate_validation_queries()

    assert "HasName" not in queries


def test_rule_no_postconditions_skipped():
    """Rule with no postconditions should be silently skipped (no 'rule' in output)."""
    schema = _schema_with_rules(
        [
            ClassRule(
                preconditions=AnonymousClassExpression(
                    slot_conditions={"type": SlotDefinition("type", equals_string="Human")},
                ),
                # no postconditions
            )
        ]
    )
    gen = SQLValidationGenerator(schema)
    sql = gen.generate_validation_queries()

    assert "'rule'" not in sql


def test_rule_any_of_logs_warning(caplog):
    """Unsupported class expression attributes (any_of) should log a warning."""
    schema = _schema_with_rules(
        [
            ClassRule(
                postconditions=AnonymousClassExpression(
                    slot_conditions={"age": SlotDefinition("age", maximum_value=150)},
                    any_of=[
                        AnonymousClassExpression(
                            slot_conditions={"type": SlotDefinition("type", equals_string="Human")}
                        )
                    ],
                ),
            )
        ]
    )
    gen = SQLValidationGenerator(schema)
    with caplog.at_level(logging.WARNING):
        sql = gen.generate_validation_queries()

    assert "any_of" in caplog.text
    # The supported slot_conditions still produce a query
    assert "age > 150" in sql


@pytest.mark.parametrize("combinator", ["any_of", "all_of", "none_of", "exactly_one_of"])
def test_rule_precondition_only_combinator_skips_rule(caplog, combinator):
    """A precondition expressed purely via an unsupported combinator must skip the whole rule.

    Dropping such a precondition would apply the postcondition to every row of the table,
    producing false-positive violations.
    """
    schema = _schema_with_rules(
        [
            ClassRule(
                preconditions=AnonymousClassExpression(
                    **{
                        combinator: [
                            AnonymousClassExpression(
                                slot_conditions={"type": SlotDefinition("type", equals_string="Human")}
                            )
                        ]
                    }
                ),
                postconditions=AnonymousClassExpression(
                    slot_conditions={"age": SlotDefinition("age", maximum_value=150)},
                ),
            )
        ]
    )
    gen = SQLValidationGenerator(schema)
    with caplog.at_level(logging.WARNING):
        sql = gen.generate_validation_queries()

    assert combinator in caplog.text
    assert "Skipping the rule" in caplog.text
    # The rule must not be emitted at all: an unconditional "age > 150" check would flag
    # non-Human rows that the precondition was meant to exclude.
    assert "'rule'" not in sql
    assert "age > 150" not in sql


def test_postgresql_casts_invalid_value():
    """PostgreSQL dialect should wrap invalid_value in CAST(... AS TEXT)."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", identifier=True))
    b.add_slot(SlotDefinition("age", range="integer", minimum_value=0, maximum_value=120))
    b.add_class("Person", slots=["id", "age"])
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema, dialect="postgresql")
    queries = gen.generate_validation_queries()

    assert "CAST" in queries
    assert "age AS TEXT" in queries


def test_include_comments_content(minimal_schema):
    """Default include_comments=True should produce a header with expected content."""
    gen = SQLValidationGenerator(minimal_schema)
    queries = gen.generate_validation_queries()

    assert "SQL Validation Queries" in queries
    assert "LinkML" in queries
    assert "-- " in queries  # comment marker


@pytest.fixture
def no_identifier_schema():
    """Schema whose class has neither an identifier nor a key slot."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("value", range="integer", required=True, minimum_value=0))
    b.add_class("Measurement", slots=["value"])
    b.add_defaults()
    return b.schema


@pytest.mark.parametrize(
    "slots,dialect,expected_record_id",
    [
        ([SlotDefinition("pid", identifier=True)], "sqlite", "pid AS record_id"),
        ([SlotDefinition("code", key=True)], "sqlite", "code AS record_id"),
        # an identifier wins over a key slot, regardless of declaration order
        (
            [SlotDefinition("code", key=True), SlotDefinition("pid", identifier=True)],
            "sqlite",
            "pid AS record_id",
        ),
        # a slot merely named 'id' is not an identifier and must not become the record_id
        ([SlotDefinition("id")], "sqlite", "NULL AS record_id"),
        ([], "sqlite", "NULL AS record_id"),
        ([], "postgresql", "CAST(NULL AS TEXT) AS record_id"),
    ],
    ids=["identifier", "key_only", "identifier_wins_over_key", "plain_slot_named_id", "neither", "neither_postgres"],
)
def test_record_id_column_selection(slots, dialect, expected_record_id, caplog):
    """The record_id is the identifier slot, else the key slot, else NULL.

    A class needs neither in LinkML. Falling back to a hardcoded 'id' column would either
    reference a column absent from the DDL - taking down the whole UNION ALL query - or
    silently report an unrelated data slot as the identity of the violating record.
    """
    b = SchemaBuilder()
    for slot in [*slots, SlotDefinition("name", required=True)]:
        b.add_slot(slot)
    b.add_class("Record", slots=[s.name for s in slots] + ["name"])
    b.add_defaults()

    gen = SQLValidationGenerator(b.schema, dialect=dialect, include_comments=False)
    with caplog.at_level(logging.WARNING, logger="linkml.generators.sqlvalidationgen"):
        queries = gen.generate_validation_queries()

    assert expected_record_id in queries
    # leading space so this does not match a legitimate 'pid AS record_id'
    assert " id AS record_id" not in queries
    # a NULL record_id is announced, and only then
    assert ("no identifier or key slot" in caplog.text) == ("NULL" in expected_record_id)


def test_rule_on_class_without_identifier_selects_null_record_id():
    """The rule path builds its own table clause, and must resolve the record_id the same way."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("status"))
    b.add_slot(SlotDefinition("age", range="integer"))
    b.add_class("Person", slots=["status", "age"])
    b.add_defaults()
    b.schema.classes["Person"].rules = [
        ClassRule(
            preconditions=AnonymousClassExpression(
                slot_conditions={"status": SlotDefinition("status", equals_string="adult")}
            ),
            postconditions=AnonymousClassExpression(slot_conditions={"age": SlotDefinition("age", minimum_value=18)}),
        )
    ]

    gen = SQLValidationGenerator(b.schema, include_comments=False)
    queries = gen.generate_validation_queries()

    assert "'rule'" in queries
    assert "NULL AS record_id" in queries
    assert "id AS record_id" not in queries


@pytest.mark.slow
def test_interop_class_without_identifier_executes(no_identifier_schema, tmp_path):
    """Queries for an identifier-less class must run against the matching DDL.

    SQLValidationGenerator transforms with NO_FOREIGN_KEYS, under which no surrogate
    primary key is injected, so the corresponding DDL is the one without foreign keys.
    """
    ddl = SQLTableGenerator(no_identifier_schema, dialect="sqlite", use_foreign_keys=False).generate_ddl()
    assert "id" not in ddl.split("CREATE TABLE")[1].split(";")[0]

    conn = sqlite3.connect(str(tmp_path / "no_identifier.db"))
    cursor = conn.cursor()
    cursor.executescript(ddl)
    cursor.execute('INSERT INTO "Measurement" (value) VALUES (?)', (5,))
    cursor.execute('INSERT INTO "Measurement" (value) VALUES (?)', (-1,))
    conn.commit()

    validation_query = SQLValidationGenerator(no_identifier_schema, dialect="sqlite").generate_validation_queries()
    cursor.execute(validation_query)
    violations = cursor.fetchall()
    conn.close()

    # one range violation, reported without a record_id
    assert len(violations) == 1
    table_name, column_name, constraint_type, record_id, invalid_value = violations[0]
    assert (table_name, column_name, constraint_type) == ("Measurement", "value", "range")
    assert record_id is None
    assert invalid_value == -1
