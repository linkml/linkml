from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

import click
from sqlalchemy import and_, column, func, literal_column, or_, select, table, union_all
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects import sqlite as sqlite_dialect
from sqlalchemy.types import Text

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

    This generator creates a unified SELECT statement (combining multiple validation
    checks with UNION ALL) that identifies data entries violating LinkML schema
    constraints. The query can be executed against a database to find constraint
    violations.

    Supported constraint types:
    - required: Find NULL values in required fields
    - minimum_value/maximum_value: Find numeric range violations
    - pattern: Find regex pattern violations
    - identifier/key: Find uniqueness violations
    - unique_keys: Find multi-column uniqueness violations
    - enum: Find values not in the permissible values list

    Example:
        >>> gen = SQLValidationGenerator("schema.yaml", dialect="postgresql")
        >>> queries = gen.generate_validation_queries()
        >>> print(queries)

    The generated query returns standardized columns:
    - table_name: The class/table name
    - column_name: The slot/column name (or constraint name for unique_keys)
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
        Generate SQL validation queries for constraints in the schema.

        This method:
        1. Iterates through all classes and their slots
        2. Generates validation queries for constraint types
        3. Combines all queries with UNION ALL into a single result set

        All results are returned in one table with these columns:
        - table_name: The class/table name
        - column_name: The slot/column name (or constraint name for unique_keys)
        - constraint_type: Type of constraint violated
        - record_id: ID of the violating record
        - invalid_value: The value that violates the constraint

        :param kwargs: Additional arguments for schema transformation
        :return: SQL validation queries as a string
        :rtype: str
        """
        query_objects = []

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

            # Find the identifier slot for this class
            identifier_slot_name = "id"  # default fallback
            for slot_name, _ in class_def.attributes.items():
                induced = sv.induced_slot(slot_name, class_name)
                if induced.identifier:
                    identifier_slot_name = slot_name
                    break

            for slot_name, _ in class_def.attributes.items():
                # Get induced slot to capture inherited constraints
                induced = sv.induced_slot(slot_name, class_name)

                # Generate validation queries for each constraint type
                if self.check_required and induced.required:
                    query = self._generate_required_violations(class_name, induced, identifier_slot_name)

                    if query is not None:
                        query_objects.append(query)

                if self.check_ranges:
                    if induced.minimum_value is not None or induced.maximum_value is not None:
                        query = self._generate_range_violations(class_name, induced, identifier_slot_name)
                        if query is not None:
                            query_objects.append(query)

                if self.check_patterns and induced.pattern:
                    query = self._generate_pattern_violations(class_name, induced, identifier_slot_name)
                    if query is not None:
                        query_objects.append(query)

                # Check identifier/key uniqueness
                if induced.identifier or induced.key:
                    query = self._generate_identifier_violations(class_name, induced, identifier_slot_name)
                    if query is not None:
                        query_objects.append(query)

                # Check enum constraints
                if self.check_enums and induced.range and induced.range in sv.all_enums():
                    query = self._generate_enum_violations(class_name, induced, sv, identifier_slot_name)
                    if query is not None:
                        query_objects.append(query)

            # Check unique_keys constraints (multi-column uniqueness)
            if self.check_unique_keys and class_def.unique_keys:
                for _, uk in class_def.unique_keys.items():
                    query = self._generate_unique_key_violations(class_name, class_def, uk, identifier_slot_name)
                    if query is not None:
                        query_objects.append(query)

        if not query_objects:
            return ""

        # Combine all queries with UNION ALL using SQLAlchemy
        combined_query = union_all(*query_objects)
        compiled_sql = self._compile_query(combined_query)
        # Improve readability by adding line breaks
        compiled_sql = compiled_sql.replace(" UNION ALL ", "\n\nUNION ALL\n\n")

        # Build final result
        result_parts = []
        if self.include_comments:
            header = self._generate_header()
            result_parts.extend([header])
            result_parts.append("")  # blank line after header

        result_parts.append(compiled_sql + ";")

        result = "\n".join(result_parts)
        if result and not result.endswith("\n"):
            result += "\n"
        return result

    def _generate_header(self) -> str:
        """Generate a header comment for the SQL output."""
        header = (
            "-- ====================================================================\n"
            "-- SQL Validation Queries\n"
            "-- Generated from LinkML schema\n"
            f"-- LinkML v{__version__}\n"
            f"-- Generator: {self.generatorname} v{self.generatorversion}\n"
            f"-- Dialect: {self.dialect}\n"
            "-- ===================================================================="
        )
        return header

    def _generate_required_violations(self, class_name: str, slot: SlotDefinition, identifier_slot_name: str):
        """
        Generate query to find NULL values in required fields.

        :param class_name: Name of the class/table
        :param slot: Slot definition with required=True
        :param identifier_slot_name: Name of the identifier slot
        :return: SQLAlchemy select object
        """
        tbl = table(class_name, column(identifier_slot_name), column(slot.name))

        query = (
            select(
                literal_column(f"'{class_name}'").label("table_name"),
                literal_column(f"'{slot.name}'").label("column_name"),
                literal_column("'required'").label("constraint_type"),
                column(identifier_slot_name).label("record_id"),
                literal_column("NULL").label("invalid_value"),
            )
            .select_from(tbl)
            .where(tbl.c[slot.name].is_(None))
        )

        return query

    def _generate_range_violations(self, class_name: str, slot: SlotDefinition, identifier_slot_name: str):
        """
        Generate query to find minimum_value/maximum_value violations.

        :param class_name: Name of the class/table
        :param slot: Slot definition with min/max constraints
        :param identifier_slot_name: Name of the identifier slot
        :return: SQLAlchemy select object or None
        """
        conditions = []

        tbl = table(class_name, column(identifier_slot_name), column(slot.name))

        if slot.minimum_value is not None:
            conditions.append(tbl.c[slot.name] < literal_column(str(slot.minimum_value)))

        if slot.maximum_value is not None:
            conditions.append(tbl.c[slot.name] > literal_column(str(slot.maximum_value)))

        if not conditions:
            return None

        query = (
            select(
                literal_column(f"'{class_name}'").label("table_name"),
                literal_column(f"'{slot.name}'").label("column_name"),
                literal_column("'range'").label("constraint_type"),
                column(identifier_slot_name).label("record_id"),
                column(slot.name).label("invalid_value"),
            )
            .select_from(tbl)
            .where(or_(*conditions))
        )

        return query

    def _generate_pattern_violations(self, class_name: str, slot: SlotDefinition, identifier_slot_name: str):
        """
        Generate query to find pattern (regex) violations.

        Handles dialect-specific regex syntax:
        - PostgreSQL: ~ operator
        - SQLite: REGEXP function (requires extension)

        :param class_name: Name of the class/table
        :param slot: Slot definition with pattern constraint
        :param identifier_slot_name: Name of the identifier slot
        :return: SQLAlchemy select object
        """
        tbl = table(class_name, column(identifier_slot_name), column(slot.name))

        pattern = slot.pattern

        # Generate dialect-specific pattern matching using SQLAlchemy
        # We need to use literal_column for dialect-specific operators
        if self.dialect == "postgresql":
            pattern_check = ~literal_column(f"{slot.name} ~ '{pattern}'")
        elif self.dialect == "sqlite":
            # SQLite REGEXP requires extension
            pattern_check = ~literal_column(f"(REGEXP('{pattern}', {slot.name}) = 1)")

        else:
            # Default to PostgreSQL syntax
            pattern_check = ~literal_column(f"{slot.name} ~ '{pattern}'")

        query = (
            select(
                literal_column(f"'{class_name}'").label("table_name"),
                literal_column(f"'{slot.name}'").label("column_name"),
                literal_column("'pattern'").label("constraint_type"),
                column(identifier_slot_name).label("record_id"),
                column(slot.name).label("invalid_value"),
            )
            .select_from(tbl)
            .where(and_(tbl.c[slot.name].isnot(None), pattern_check))
        )

        return query

    def _generate_identifier_violations(self, class_name: str, slot: SlotDefinition, identifier_slot_name: str):
        """
        Generate query to find identifier/key uniqueness violations.

        Finds individual records with duplicate values in identifier or key slots.

        :param class_name: Name of the class/table
        :param slot: Slot definition with identifier=True or key=True
        :param identifier_slot_name: Name of the identifier slot
        :return: SQLAlchemy select object
        """
        tbl = table(class_name, column(identifier_slot_name), column(slot.name))

        constraint_type = "identifier" if slot.identifier else "key"

        # Subquery to find duplicate values
        duplicate_subquery = (
            select(column(slot.name))
            .select_from(table(class_name, column(slot.name)))
            .group_by(column(slot.name))
            .having(func.count() > 1)
        )

        # Main query to find all records with those duplicate values
        query = (
            select(
                literal_column(f"'{class_name}'").label("table_name"),
                literal_column(f"'{slot.name}'").label("column_name"),
                literal_column(f"'{constraint_type}'").label("constraint_type"),
                column(identifier_slot_name).label("record_id"),
                column(slot.name).label("invalid_value"),
            )
            .select_from(tbl)
            .where(tbl.c[slot.name].in_(duplicate_subquery))
        )

        return query

    def _generate_enum_violations(
        self, class_name: str, slot: SlotDefinition, sv: SchemaView, identifier_slot_name: str
    ):
        """
        Generate query to find enum constraint violations.

        Finds values not in the enum's permissible_values list.

        :param class_name: Name of the class/table
        :param slot: Slot definition with enum range
        :param sv: SchemaView for looking up enum values
        :param identifier_slot_name: Name of the identifier slot
        :return: SQLAlchemy select object or None
        """
        # Get the enum definition
        enum = sv.all_enums().get(slot.range)
        if not enum or not enum.permissible_values:
            return None

        permissible_values = [str(v) for v in enum.permissible_values.keys()]

        tbl = table(class_name, column(identifier_slot_name), column(slot.name))

        query = (
            select(
                literal_column(f"'{class_name}'").label("table_name"),
                literal_column(f"'{slot.name}'").label("column_name"),
                literal_column("'enum'").label("constraint_type"),
                column(identifier_slot_name).label("record_id"),
                column(slot.name).label("invalid_value"),
            )
            .select_from(tbl)
            .where(and_(tbl.c[slot.name].isnot(None), tbl.c[slot.name].notin_(permissible_values)))
        )

        return query

    def _generate_unique_key_violations(
        self, class_name: str, class_def: ClassDefinition, uk, identifier_slot_name: str
    ):
        """
        Generate query to find unique_keys violations (multi-column uniqueness).

        Finds individual records with duplicate combinations of values across multiple columns.

        :param class_name: Name of the class/table
        :param class_def: Class definition
        :param uk: UniqueKey definition
        :param identifier_slot_name: Name of the identifier slot
        :return: SQLAlchemy select object or None
        """
        # Get column names from unique key slots
        columns = []
        for slot_name in uk.unique_key_slots:
            if slot_name in class_def.attributes:
                columns.append(slot_name)

        if not columns:
            return None

        # Main table with identifier and all columns
        tbl = table(class_name, column(identifier_slot_name), *[column(col) for col in columns])

        # Build concatenated value expression (pipe-separated)
        # Use CAST to ensure all values are strings before concatenation
        if len(columns) == 1:
            concat_expr = func.cast(column(columns[0]), Text)
        else:
            # Build concatenation: CAST(col1 AS TEXT) || '|' || CAST(col2 AS TEXT) || ...
            concat_parts = []
            for i, col in enumerate(columns):
                concat_parts.append(func.cast(column(col), Text))
                if i < len(columns) - 1:
                    concat_parts.append(literal_column("'|'"))

            # Chain concatenation operations
            concat_expr = concat_parts[0]
            for part in concat_parts[1:]:
                concat_expr = concat_expr.op("||")(part)

        # Subquery to find duplicate combinations
        subquery_tbl = table(class_name, *[column(col) for col in columns])
        duplicate_subquery = (
            select(*[column(col) for col in columns])
            .select_from(subquery_tbl)
            .group_by(*[column(col) for col in columns])
            .having(func.count() > 1)
        )

        # Build the WHERE clause for multi-column IN
        if len(columns) == 1:
            where_clause = tbl.c[columns[0]].in_(duplicate_subquery)
        else:
            # For multiple columns, use tuple IN syntax
            # SQLAlchemy's tuple_() function handles this properly across dialects
            from sqlalchemy import tuple_

            where_clause = tuple_(*[tbl.c[col] for col in columns]).in_(duplicate_subquery)

        # Main query to find all records with duplicate combinations
        query = (
            select(
                literal_column(f"'{class_name}'").label("table_name"),
                literal_column(f"'{uk.unique_key_name}'").label("column_name"),
                literal_column("'unique_key'").label("constraint_type"),
                column(identifier_slot_name).label("record_id"),
                concat_expr.label("invalid_value"),
            )
            .select_from(tbl)
            .where(where_clause)
        )

        return query


@shared_arguments(SQLValidationGenerator)
@click.command(name="sqlvalidation")
@click.option(
    "--dialect",
    default="sqlite",
    show_default=True,
    help="SQL dialect (sqlite, postgresql)",
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
