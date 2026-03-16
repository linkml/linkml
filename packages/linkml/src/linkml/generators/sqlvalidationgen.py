from __future__ import annotations

import copy
import logging
import os
from dataclasses import dataclass
from typing import Any

import click
from sqlalchemy import and_, column, func, literal, null, or_, select, table, union_all
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects import sqlite as sqlite_dialect
from sqlalchemy.sql.selectable import TableClause
from sqlalchemy.types import Float, Integer, Text

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import SlotDefinition
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)


def _literal_num(val):
    """Return a typed SQLAlchemy literal for a numeric value."""
    return literal(val, type_=Integer() if isinstance(val, int) else Float())


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
    check_rules: bool = True

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

        sv = SchemaView(self.schema)

        # Iterate through all classes
        for class_name in sv.all_classes():
            class_def = sv.get_class(class_name)
            if class_def.abstract or class_def.mixin:
                continue

            raw_induced_slots = sv.class_induced_slots(class_name)
            if not raw_induced_slots:
                continue

            induced_slots = []
            for slot in raw_induced_slots:
                slot = copy.copy(slot)
                slot.name = underscore(slot.alias or slot.name)
                if slot.identifier or slot.key:
                    slot.required = True
                induced_slots.append(slot)

            # Find the identifier slot for this class
            identifier_slot_name = "id"  # default fallback
            for induced in induced_slots:
                if induced.identifier:
                    identifier_slot_name = induced.name
                    break

            for induced in induced_slots:
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
                slot_names = {s.name for s in induced_slots}
                for _, uk in class_def.unique_keys._items():
                    query = self._generate_unique_key_violations(class_name, slot_names, uk, identifier_slot_name)
                    if query is not None:
                        query_objects.append(query)

            # Check rules (precondition/postcondition constraints)
            if self.check_rules and class_def.rules:
                for _, rule in enumerate(class_def.rules):
                    if rule.deactivated:
                        continue
                    query = self._generate_rule_violations(class_name, rule, identifier_slot_name)
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

    def _build_violation_query(
        self,
        class_name: str,
        column_name: str,
        constraint_type: str,
        identifier_slot_name: str,
        invalid_value,
        tbl: TableClause,
        where_condition=None,
    ):
        """
        Build a standardized violation query SELECT statement.

        :param class_name: Name of the class/table
        :param column_name: Name of the slot/constraint for column_name label
        :param constraint_type: Type of constraint violated
        :param identifier_slot_name: Name of the identifier slot
        :param invalid_value: Expression for invalid_value column (literal or column)
        :param where_condition: SQLAlchemy WHERE condition
        :param tbl: Optional SQLAlchemy table object (created if not provided)
        :return: SQLAlchemy select object
        """

        query = select(
            literal(class_name, type_=Text()).label("table_name"),
            literal(column_name, type_=Text()).label("column_name"),
            literal(constraint_type, type_=Text()).label("constraint_type"),
            column(identifier_slot_name).label("record_id"),
            invalid_value.label("invalid_value"),
        ).select_from(tbl)

        if where_condition is not None:
            query = query.where(where_condition)

        return query

    def _generate_required_violations(self, class_name: str, slot: SlotDefinition, identifier_slot_name: str):
        """
        Generate query to find NULL values in required fields.

        :param class_name: Name of the class/table
        :param slot: Slot definition with required=True
        :param identifier_slot_name: Name of the identifier slot
        :return: SQLAlchemy select object
        """
        tbl = table(class_name, column(identifier_slot_name), column(slot.name))

        return self._build_violation_query(
            class_name=class_name,
            column_name=slot.name,
            constraint_type="required",
            identifier_slot_name=identifier_slot_name,
            invalid_value=null(),
            tbl=tbl,
            where_condition=tbl.c[slot.name].is_(None),
        )

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
            conditions.append(tbl.c[slot.name] < _literal_num(slot.minimum_value))

        if slot.maximum_value is not None:
            conditions.append(tbl.c[slot.name] > _literal_num(slot.maximum_value))

        if not conditions:
            return None

        return self._build_violation_query(
            class_name=class_name,
            column_name=slot.name,
            constraint_type="range",
            identifier_slot_name=identifier_slot_name,
            invalid_value=column(slot.name),
            tbl=tbl,
            where_condition=or_(*conditions),
        )

    def _generate_pattern_violations(self, class_name: str, slot: SlotDefinition, identifier_slot_name: str):
        """
        Generate query to find pattern (regex) violations.

        Uses SQLAlchemy's ``regexp_match`` which compiles to the dialect-specific
        syntax (PostgreSQL: ``~``, SQLite: ``REGEXP``).

        :param class_name: Name of the class/table
        :param slot: Slot definition with pattern constraint
        :param identifier_slot_name: Name of the identifier slot
        :return: SQLAlchemy select object
        """
        tbl = table(class_name, column(identifier_slot_name), column(slot.name))

        pattern_check = ~tbl.c[slot.name].regexp_match(literal(slot.pattern, type_=Text()))

        return self._build_violation_query(
            class_name=class_name,
            column_name=slot.name,
            constraint_type="pattern",
            identifier_slot_name=identifier_slot_name,
            invalid_value=column(slot.name),
            tbl=tbl,
            where_condition=and_(tbl.c[slot.name].isnot(None), pattern_check),
        )

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

        return self._build_violation_query(
            class_name=class_name,
            column_name=slot.name,
            constraint_type=constraint_type,
            identifier_slot_name=identifier_slot_name,
            invalid_value=column(slot.name),
            where_condition=tbl.c[slot.name].in_(duplicate_subquery),
            tbl=tbl,
        )

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

        permissible_values = [literal(str(v), type_=Text()) for v in enum.permissible_values.keys()]

        tbl = table(class_name, column(identifier_slot_name), column(slot.name))

        return self._build_violation_query(
            class_name=class_name,
            column_name=slot.name,
            constraint_type="enum",
            identifier_slot_name=identifier_slot_name,
            invalid_value=column(slot.name),
            tbl=tbl,
            where_condition=and_(tbl.c[slot.name].isnot(None), tbl.c[slot.name].notin_(permissible_values)),
        )

    def _generate_unique_key_violations(self, class_name: str, slot_names: set[str], uk, identifier_slot_name: str):
        """
        Generate query to find unique_keys violations (multi-column uniqueness).

        Finds individual records with duplicate combinations of values across multiple columns.

        :param class_name: Name of the class/table
        :param slot_names: Set of valid slot names for this class
        :param uk: UniqueKey definition
        :param identifier_slot_name: Name of the identifier slot
        :return: SQLAlchemy select object or None
        """
        # Get column names from unique key slots (underscored for SQL)
        columns = []
        for slot_name in uk.unique_key_slots:
            sql_name = underscore(slot_name)
            if sql_name in slot_names:
                columns.append(sql_name)

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
                    concat_parts.append(literal("|", type_=Text()))

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

        return self._build_violation_query(
            class_name=class_name,
            column_name=uk.unique_key_name,
            constraint_type="unique_key",
            identifier_slot_name=identifier_slot_name,
            invalid_value=concat_expr,
            tbl=tbl,
            where_condition=where_clause,
        )

    def _slot_condition_to_sqlalchemy(self, tbl, slot_name, slot_condition, negate=False):
        """
        Convert a single slot condition to SQLAlchemy WHERE clause(s).

        :param tbl: SQLAlchemy table object
        :param slot_name: Name of the slot/column
        :param slot_condition: SlotDefinition with constraint properties
        :param negate: If True, negate the condition (for postcondition violation detection)
        :return: list of SQLAlchemy conditions
        """
        conditions = []
        col = tbl.c[slot_name]

        if slot_condition.equals_string is not None:
            val = slot_condition.equals_string
            lit = literal(val, type_=Text())
            if negate:
                conditions.append(or_(col != lit, col.is_(None)))
            else:
                conditions.append(col == lit)

        if slot_condition.equals_number is not None:
            val = slot_condition.equals_number
            if negate:
                conditions.append(or_(col != _literal_num(val), col.is_(None)))
            else:
                conditions.append(col == _literal_num(val))

        if slot_condition.equals_string_in:
            vals = list(slot_condition.equals_string_in)
            lit_vals = [literal(v, type_=Text()) for v in vals]
            if negate:
                conditions.append(or_(col.notin_(lit_vals), col.is_(None)))
            else:
                conditions.append(col.in_(lit_vals))

        if slot_condition.minimum_value is not None:
            val = slot_condition.minimum_value
            if negate:
                conditions.append(col < _literal_num(val))
            else:
                conditions.append(col >= _literal_num(val))

        if slot_condition.maximum_value is not None:
            val = slot_condition.maximum_value
            if negate:
                conditions.append(col > _literal_num(val))
            else:
                conditions.append(col <= _literal_num(val))

        return conditions

    def _class_expression_to_sqlalchemy(self, tbl, expression, negate=False):
        """
        Convert an AnonymousClassExpression to a composite WHERE clause.

        :param tbl: SQLAlchemy table object
        :param expression: AnonymousClassExpression with slot_conditions
        :param negate: If True, negate the expression (for postcondition violation detection). Note that negated
        conditions are concatenated with OR -> De Morgan's law.
        :return: SQLAlchemy condition or None
        """
        if not expression or not expression.slot_conditions:
            return None

        # Warn about unsupported features
        for attr in ("any_of", "all_of", "none_of", "exactly_one_of"):
            if getattr(expression, attr, None):
                logger.warning(f"Rule class expression '{attr}' is not yet supported in SQL validation")

        all_conditions = []
        for slot_name, slot_condition in expression.slot_conditions.items():
            conds = self._slot_condition_to_sqlalchemy(tbl, slot_name, slot_condition, negate=negate)
            all_conditions.extend(conds)

        if not all_conditions:
            return None

        if negate:
            # De Morgan's law: negating AND → OR
            return or_(*all_conditions)
        else:
            return and_(*all_conditions)

    def _generate_rule_violations(self, class_name, rule, identifier_slot_name):
        """
        Generate query to find rows violating a rule's postconditions.

        A violation occurs when the precondition is met but the postcondition is not.

        Preconditions are concatenated with AND. Postconditions are concatenated with OR.
        Postcondition is required, precondition is not required. If no precondition is given,
        the postcondition applies to all entries.

        :param class_name: Name of the class/table
        :param rule: ClassRule with preconditions/postconditions
        :param identifier_slot_name: Name of the identifier slot
        :return: SQLAlchemy select object or None
        """
        if not rule.postconditions or not rule.postconditions.slot_conditions:
            logger.warning("Could not generate rule-based query: A rule needs to have a 'postcondition'.")
            return None

        # Collect all referenced column names
        col_names = {identifier_slot_name}
        if rule.preconditions and rule.preconditions.slot_conditions:
            col_names.update(rule.preconditions.slot_conditions.keys())
        col_names.update(rule.postconditions.slot_conditions.keys())

        postcondition_slot_names = list(rule.postconditions.slot_conditions.keys())
        column_name_label = ",".join(postcondition_slot_names)

        tbl = table(class_name, *[column(c) for c in col_names])

        # Build WHERE: precondition AND (negated postcondition)
        where_parts = []
        if rule.preconditions:
            pre = self._class_expression_to_sqlalchemy(tbl, rule.preconditions, negate=False)
            if pre is not None:
                where_parts.append(pre)

        post = self._class_expression_to_sqlalchemy(tbl, rule.postconditions, negate=True)
        if post is None:
            logger.warning(
                "Could not generate rule-based query: postconditions exist but produced "
                "no SQL conditions (unsupported slot condition types?)."
            )
            return None
        where_parts.append(post)

        where_clause = and_(*where_parts) if len(where_parts) > 1 else where_parts[0]

        return self._build_violation_query(
            class_name=class_name,
            column_name=column_name_label,
            constraint_type="rule",
            identifier_slot_name=identifier_slot_name,
            invalid_value=column(postcondition_slot_names[0]),
            tbl=tbl,
            where_condition=where_clause,
        )


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
    "--check-rules/--no-check-rules",
    default=True,
    show_default=True,
    help="Generate queries for rule (precondition/postcondition) violations",
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
