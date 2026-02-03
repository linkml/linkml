from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

import click
from sqlalchemy import and_, column, func, literal_column, or_, select, table
from sqlalchemy.dialects import mysql, oracle, postgresql
from sqlalchemy.dialects import sqlite as sqlite_dialect

from linkml._version import __version__
from linkml.transformers.relmodel_transformer import ForeignKeyPolicy, RelationalModelTransformer
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)


@dataclass
class SQLValidationGenerator(Generator):
    """
    A :class:`~linkml.utils.generator.Generator` for creating SQL validation queries.

    This generator creates SELECT statements that identify data entries violating
    LinkML schema constraints. The queries can be executed against a database to
    find constraint violations.

    Supported constraint types:
    - required: Find NULL values in required fields
    - minimum_value/maximum_value: Find numeric range violations
    - pattern: Find regex pattern violations
    - identifier/key: Find uniqueness violations
    - unique_keys: Find multi-column uniqueness violations

    Example:
        >>> gen = SQLValidationGenerator("schema.yaml", dialect="postgresql")
        >>> queries = gen.generate_validation_queries()
        >>> print(queries)

    The generated queries return standardized columns:
    - table_name: The class/table name
    - column_name: The slot/column name
    - constraint_type: Type of constraint violated
    - record_id: ID of the violating record
    - invalid_value: The value that violates the constraint
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["sql"]
    file_extension = "sql"
    uses_schemaloader = False

    # ObjectVars
    dialect: str = "sqlite"
    include_comments: bool = True
    check_required: bool = True
    check_ranges: bool = True
    check_patterns: bool = True
    check_enums: bool = True
    check_unique_keys: bool = True

    def _get_dialect(self):
        """
        Get the SQLAlchemy dialect object for the configured dialect.

        :return: SQLAlchemy dialect instance
        """
        dialect_map = {
            "postgresql": postgresql.dialect(),
            "mysql": mysql.dialect(),
            "oracle": oracle.dialect(),
            "sqlite": sqlite_dialect.dialect(),
        }
        return dialect_map.get(self.dialect, sqlite_dialect.dialect())

    def _compile_query(self, query) -> str:
        """
        Compile a SQLAlchemy query to SQL string for the configured dialect.

        :param query: SQLAlchemy selectable object
        :return: Compiled SQL string
        """
        dialect = self._get_dialect()
        compiled = query.compile(dialect=dialect, compile_kwargs={"literal_binds": True})
        return str(compiled)

    def serialize(self, **kwargs: dict[str, Any]) -> str:
        """
        Main entry point for generating validation queries.

        :param kwargs: Additional arguments passed to generate_validation_queries
        :return: SQL validation queries as a string
        :rtype: str
        """
        return self.generate_validation_queries(**kwargs)

    def generate_validation_queries(self, **kwargs: dict[str, Any]) -> str:
        """
        Generate SQL validation queries for all constraints in the schema.

        This method:
        1. Transforms the LinkML schema to a relational model
        2. Iterates through all classes and their slots
        3. Generates validation queries for each constraint type
        4. Returns all queries as a formatted SQL string

        :param kwargs: Additional arguments for schema transformation
        :return: SQL validation queries as a string
        :rtype: str
        """
        queries = []

        # Add header comment
        if self.include_comments:
            header = self._generate_header()
            queries.append(header)

        # Transform schema to relational model
        sqltr = RelationalModelTransformer(SchemaView(self.schema))
        sqltr.foreign_key_policy = ForeignKeyPolicy.NO_FOREIGN_KEYS
        tr_result = sqltr.transform(tgt_schema_name=kwargs.get("tgt_schema_name"), top_class=kwargs.get("top_class"))
        schema = tr_result.schema
        sv = SchemaView(schema)

        # Iterate through all classes
        for class_name, class_def in schema.classes.items():
            if class_def.abstract:
                continue

            if not class_def.attributes:
                # skip if no attributes are present
                continue

            for slot_name, _ in class_def.attributes.items():
                # Get induced slot to capture inherited constraints
                induced = sv.induced_slot(slot_name, class_name)

                # Generate validation queries for each constraint type
                if self.check_required and induced.required:
                    query = self._generate_required_violations(class_name, induced)
                    if query:
                        queries.append(query)

                if self.check_ranges:
                    if induced.minimum_value is not None or induced.maximum_value is not None:
                        query = self._generate_range_violations(class_name, induced)
                        if query:
                            queries.append(query)

                if self.check_patterns and induced.pattern:
                    query = self._generate_pattern_violations(class_name, induced)
                    if query:
                        queries.append(query)

                # Check identifier/key uniqueness
                if induced.identifier or induced.key:
                    query = self._generate_identifier_violations(class_name, induced)
                    if query:
                        queries.append(query)

                # Check enum constraints
                if self.check_enums and induced.range and induced.range in sv.all_enums():
                    query = self._generate_enum_violations(class_name, induced, sv)
                    if query:
                        queries.append(query)

            # Check unique_keys constraints (multi-column uniqueness)
            if self.check_unique_keys and class_def.unique_keys:
                for _, uk in class_def.unique_keys.items():
                    query = self._generate_unique_key_violations(class_name, class_def, uk)
                    if query:
                        queries.append(query)

        # Join all queries with blank lines
        result = "\n\n".join(queries)
        if result and not result.endswith("\n"):
            result += "\n"
        return result

    def _generate_header(self) -> str:
        """Generate a header comment for the SQL output."""
        header = f"""-- ====================================================================
        -- SQL Validation Queries
        -- Generated from LinkML schema
        -- Generator: {self.generatorname} v{self.generatorversion}
        -- Dialect: {self.dialect}
        -- ===================================================================="""
        return header

    def _generate_required_violations(self, class_name: str, slot: SlotDefinition) -> str:
        """
        Generate query to find NULL values in required fields.

        :param class_name: Name of the class/table
        :param slot: Slot definition with required=True
        :return: SQL query string
        """
        tbl = table(class_name, column("id"), column(slot.name))

        query = (
            select(
                literal_column(f"'{class_name}'").label("table_name"),
                literal_column(f"'{slot.name}'").label("column_name"),
                literal_column("'required'").label("constraint_type"),
                column("id").label("record_id"),
                literal_column("NULL").label("invalid_value"),
            )
            .select_from(tbl)
            .where(tbl.c[slot.name].is_(None))
        )

        query_parts = []
        if self.include_comments:
            query_parts.append(
                f"-- Validation: {class_name}.{slot.name} - Required field\n"
                f"-- Records with NULL values in required field"
            )

        query_parts.append(self._compile_query(query) + ";")

        return "\n".join(query_parts)

    def _generate_range_violations(self, class_name: str, slot: SlotDefinition) -> str:
        """
        Generate query to find minimum_value/maximum_value violations.

        :param class_name: Name of the class/table
        :param slot: Slot definition with min/max constraints
        :return: SQL query string
        """
        conditions = []
        constraint_desc = []

        tbl = table(class_name, column("id"), column(slot.name))

        if slot.minimum_value is not None:
            conditions.append(tbl.c[slot.name] < literal_column(str(slot.minimum_value)))
            constraint_desc.append(f"minimum_value: {slot.minimum_value}")

        if slot.maximum_value is not None:
            conditions.append(tbl.c[slot.name] > literal_column(str(slot.maximum_value)))
            constraint_desc.append(f"maximum_value: {slot.maximum_value}")

        if not conditions:
            return ""

        query = (
            select(
                literal_column(f"'{class_name}'").label("table_name"),
                literal_column(f"'{slot.name}'").label("column_name"),
                literal_column("'range'").label("constraint_type"),
                column("id").label("record_id"),
                column(slot.name).label("invalid_value"),
            )
            .select_from(tbl)
            .where(or_(*conditions))
        )

        query_parts = []
        if self.include_comments:
            query_parts.append(
                f"-- Validation: {class_name}.{slot.name} - Range constraint\n"
                f"-- Constraint: {', '.join(constraint_desc)}"
            )

        query_parts.append(self._compile_query(query) + ";")

        return "\n".join(query_parts)

    def _generate_pattern_violations(self, class_name: str, slot: SlotDefinition) -> str:
        """
        Generate query to find pattern (regex) violations.

        Handles dialect-specific regex syntax:
        - PostgreSQL: ~ operator
        - SQLite: REGEXP function (requires extension)
        - MySQL: REGEXP operator
        - Oracle: REGEXP_LIKE function

        :param class_name: Name of the class/table
        :param slot: Slot definition with pattern constraint
        :return: SQL query string
        """
        tbl = table(class_name, column("id"), column(slot.name))

        pattern = slot.pattern

        # Generate dialect-specific pattern matching using SQLAlchemy
        # We need to use literal_column for dialect-specific operators
        # TODO: Is there a way to do his by using sqlalchemy builtin dialect distinction?
        if self.dialect == "postgresql":
            pattern_check = ~literal_column(f"{slot.name} ~ '{pattern}'")
        elif self.dialect == "sqlite":
            # SQLite REGEXP requires extension
            pattern_check = ~literal_column(f"(REGEXP('{pattern}', {slot.name}) = 1)")
        elif self.dialect == "mysql":
            pattern_check = ~literal_column(f"{slot.name} REGEXP '{pattern}'")
        elif self.dialect == "oracle":
            pattern_check = ~literal_column(f"REGEXP_LIKE({slot.name}, '{pattern}')")
        else:
            # Default to PostgreSQL syntax
            pattern_check = ~literal_column(f"{slot.name} ~ '{pattern}'")

        query = (
            select(
                literal_column(f"'{class_name}'").label("table_name"),
                literal_column(f"'{slot.name}'").label("column_name"),
                literal_column("'pattern'").label("constraint_type"),
                column("id").label("record_id"),
                column(slot.name).label("invalid_value"),
            )
            .select_from(tbl)
            .where(and_(tbl.c[slot.name].isnot(None), pattern_check))
        )

        query_parts = []
        if self.include_comments:
            comment = f"-- Validation: {class_name}.{slot.name} - Pattern constraint\n"
            comment += f"-- Pattern: {pattern}"
            if self.dialect == "sqlite":
                comment += "\n-- Note: SQLite requires REGEXP extension to be loaded"
            query_parts.append(comment)

        query_parts.append(self._compile_query(query) + ";")

        return "\n".join(query_parts)

    def _generate_identifier_violations(self, class_name: str, slot: SlotDefinition) -> str:
        """
        Generate query to find identifier/key uniqueness violations.

        Finds duplicate values in identifier or key slots.

        :param class_name: Name of the class/table
        :param slot: Slot definition with identifier=True or key=True
        :return: SQL query string
        """
        tbl = table(class_name, column(slot.name))

        constraint_type = "identifier" if slot.identifier else "key"

        query = (
            select(
                literal_column(f"'{class_name}'").label("table_name"),
                literal_column(f"'{slot.name}'").label("column_name"),
                literal_column(f"'{constraint_type}'").label("constraint_type"),
                column(slot.name).label("duplicate_value"),
                func.count().label("duplicate_count"),
            )
            .select_from(tbl)
            .group_by(tbl.c[slot.name])
            .having(func.count() > 1)
        )

        query_parts = []
        if self.include_comments:
            query_parts.append(
                f"-- Validation: {class_name}.{slot.name} - {constraint_type.capitalize()} uniqueness\n"
                f"-- Find duplicate {constraint_type} values"
            )

        query_parts.append(self._compile_query(query) + ";")

        return "\n".join(query_parts)

    def _generate_enum_violations(self, class_name: str, slot: SlotDefinition, sv: SchemaView) -> str:
        """
        Generate query to find enum constraint violations.

        Finds values not in the enum's permissible_values list.

        :param class_name: Name of the class/table
        :param slot: Slot definition with enum range
        :param sv: SchemaView for looking up enum values
        :return: SQL query string
        """
        # Get the enum definition
        enum = sv.all_enums().get(slot.range)
        if not enum or not enum.permissible_values:
            return ""

        # Get permissible values
        permissible_values = [str(v) for v in enum.permissible_values.keys()]

        tbl = table(class_name, column("id"), column(slot.name))

        query = (
            select(
                literal_column(f"'{class_name}'").label("table_name"),
                literal_column(f"'{slot.name}'").label("column_name"),
                literal_column("'enum'").label("constraint_type"),
                column("id").label("record_id"),
                column(slot.name).label("invalid_value"),
            )
            .select_from(tbl)
            .where(and_(tbl.c[slot.name].isnot(None), tbl.c[slot.name].notin_(permissible_values)))
        )

        query_parts = []
        if self.include_comments:
            query_parts.append(
                f"-- Validation: {class_name}.{slot.name} - Enum constraint\n"
                f"-- Permissible values: {', '.join(permissible_values)}"
            )

        query_parts.append(self._compile_query(query) + ";")

        return "\n".join(query_parts)

    def _generate_unique_key_violations(self, class_name: str, class_def: ClassDefinition, uk) -> str:
        """
        Generate query to find unique_keys violations (multi-column uniqueness).

        Finds duplicate combinations of values across multiple columns.

        :param class_name: Name of the class/table
        :param class_def: Class definition
        :param uk: UniqueKey definition
        :return: SQL query string
        """
        # Get column names from unique key slots
        columns = []
        for slot_name in uk.unique_key_slots:
            if slot_name in class_def.attributes:
                columns.append(slot_name)

        if not columns:
            return ""

        tbl = table(class_name, *[column(col) for col in columns])

        # Build select columns
        select_columns = [
            literal_column(f"'{class_name}'").label("table_name"),
            literal_column(f"'{uk.unique_key_name}'").label("constraint_name"),
            literal_column("'unique_key'").label("constraint_type"),
        ]

        # Add the unique key columns
        for col in columns:
            select_columns.append(column(col))

        select_columns.append(func.count().label("duplicate_count"))

        # Build group by columns
        group_by_columns = [tbl.c[col] for col in columns]

        query = select(*select_columns).select_from(tbl).group_by(*group_by_columns).having(func.count() > 1)

        columns_str = ", ".join(columns)

        query_parts = []
        if self.include_comments:
            query_parts.append(
                f"-- Validation: {class_name} - Unique key constraint\n"
                f"-- Unique key: {uk.unique_key_name} ({columns_str})\n"
                f"-- Find duplicate combinations"
            )

        query_parts.append(self._compile_query(query) + ";")

        return "\n".join(query_parts)


@shared_arguments(SQLValidationGenerator)
@click.command(name="sqlvalidation")
@click.option(
    "--dialect",
    default="sqlite",
    show_default=True,
    help="SQL dialect (sqlite, postgresql, mysql, oracle)",
)
@click.option(
    "--check-required/--no-check-required",
    default=True,
    show_default=True,
    help="Generate queries for required field violations",
)
@click.option(
    "--check-ranges/--no-check-ranges",
    default=True,
    show_default=True,
    help="Generate queries for min/max value violations",
)
@click.option(
    "--check-patterns/--no-check-patterns",
    default=True,
    show_default=True,
    help="Generate queries for pattern violations",
)
@click.option(
    "--check-enums/--no-check-enums",
    default=True,
    show_default=True,
    help="Generate queries for enum violations",
)
@click.option(
    "--check-unique-keys/--no-check-unique-keys",
    default=True,
    show_default=True,
    help="Generate queries for unique key violations",
)
@click.option(
    "--include-comments/--no-include-comments",
    default=True,
    show_default=True,
    help="Include description of tests in generated query",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile: str, dialect: str = None, **args):
    """Generate SQL validation queries from LinkML schema."""
    gen = SQLValidationGenerator(yamlfile, **args)
    if dialect:
        gen.dialect = dialect
    print(gen.generate_validation_queries())


if __name__ == "__main__":
    cli()
