import logging
import os
from dataclasses import dataclass
from typing import Optional

import click

from sqlalchemy import Column, MetaData, Table  # noqa: F401 — used in generate_ddl and get_sql_range
from sqlalchemy.schema import CreateTable  # noqa: F401 — used in generate_ddl and get_sql_range
from sqlalchemy.types import Boolean, Date, DateTime, Float, Integer, LargeBinary, Numeric, String, Time  # noqa: F401 — used in generate_ddl and get_sql_range

from linkml._version import __version__
from linkml.generators.sqltablegen import SQLTableGenerator, METAMODEL_TYPE_TO_BASE  # noqa: F401 — used in generate_ddl and get_sql_range
from linkml.utils.generator import shared_arguments

logger = logging.getLogger(__name__)

# Module-level stubs so the file is importable without sqlalchemy-bigquery installed.
_BQ_AVAILABLE = False
ARRAY = STRUCT = BigQueryDialect = TIMESTAMP = bigquery = None


def _require_bq():
    """Import sqlalchemy-bigquery lazily. Call this at the top of any method that needs it."""
    global _BQ_AVAILABLE, ARRAY, STRUCT, BigQueryDialect, TIMESTAMP, bigquery
    if not _BQ_AVAILABLE:
        try:
            from sqlalchemy_bigquery import ARRAY, STRUCT, BigQueryDialect
            from sqlalchemy_bigquery import TIMESTAMP
            import google.cloud.bigquery as bigquery
            _BQ_AVAILABLE = True
        except ImportError as exc:
            raise ImportError(
                "sqlalchemy-bigquery is required. Install with: pip install 'linkml[bigquery]'"
            ) from exc


# Maps LinkML type bases to BigQuery SQLAlchemy types.
# Replaces the parent's RANGEMAP — every mapping here is explicit and BQ-correct.
BQ_TYPEMAP = {
    "str": String(),
    "string": String(),
    "int": Integer(),
    "float": Float(),
    "double": Float(),
    "Decimal": Numeric(),        # parent maps this to Integer() — incorrect for BQ
    "Bool": Boolean(),
    "URI": String(),
    "URIorCURIE": String(),
    "NCName": String(),
    "ElementIdentifier": String(),
    "NodeIdentifier": String(),
    "XSDDate": Date(),
    "XSDTime": Time(),
    "XSDDateTime": DateTime(),   # → DATETIME in BQ; use bigquery_type: TIMESTAMP to override
}


@dataclass
class BigQueryGenerator(SQLTableGenerator):
    """
    A Generator for BigQuery CREATE TABLE DDL.

    Produces native BigQuery DDL including ARRAY<T>, STRUCT<...>,
    PARTITION BY, CLUSTER BY, and OPTIONS clauses.

    Usage::

        gen = BigQueryGenerator("schema.yaml")
        print(gen.serialize())
    """

    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["bigquery"]
    file_extension = "sql"
    uses_schemaloader = False

    # Overrides parent defaults — BQ doesn't use normalised join tables or
    # enforced primary keys, so both are off by default.
    use_foreign_keys: bool = False
    inject_primary_keys: bool = False

    # Optional dataset prefix: when set, table names are emitted as
    # `dataset.TableName` for fully-qualified DDL.
    dataset: Optional[str] = None

    def serialize(self, **kwargs) -> str:
        return self.generate_ddl(**kwargs)

    def generate_ddl(self, **kwargs) -> str:
        """Generate BigQuery CREATE TABLE DDL for all non-abstract, non-mixin classes."""
        _require_bq()
        from linkml_runtime.utils.schemaview import SchemaView

        sv = SchemaView(self.schema)
        dialect = BigQueryDialect()
        ddl_parts = []

        for cn in sv.all_classes():
            c = sv.get_class(cn)
            if c.abstract or c.mixin:
                continue

            self._validate_partition(c, sv)

            cols = [
                Column(
                    slot.name,
                    self.get_sql_range(slot, sv=sv),
                    nullable=not slot.required,
                )
                for slot in sv.class_induced_slots(cn)
            ]
            if not cols:
                continue

            table_name = f"{self.dataset}.{cn}" if self.dataset else cn
            table_kwargs = self._bq_table_kwargs(c, sv)

            try:
                table = Table(table_name, MetaData(), *cols, **table_kwargs)
                ddl = str(CreateTable(table).compile(dialect=dialect))
                ddl_parts.append(ddl.rstrip() + ";")
            except Exception as exc:
                raise ValueError(
                    f"Failed to generate DDL for class {cn!r}: {exc}"
                ) from exc

        return "\n\n".join(ddl_parts)

    def _validate_partition(self, class_def, sv) -> None:
        """Pre-flight check for partition annotations. Raises ValueError on misconfiguration."""
        pass  # implemented in Task 5

    def _bq_table_kwargs(self, class_def, sv) -> dict:
        """Build BigQuery dialect kwargs (partitioning, clustering) from class annotations."""
        return {}  # implemented in Task 4

    def get_sql_range(self, slot, schema=None, sv=None):
        """Returns the BigQuery SQLAlchemy column type for the given slot."""
        _require_bq()
        from linkml_runtime.utils.schemaview import SchemaView

        if schema is None:
            schema = self.schema
        if sv is None:
            sv = SchemaView(schema)

        # 1. Explicit annotation override takes precedence over everything.
        if "bigquery_type" in slot.annotations:
            return self._resolve_type_override(slot.annotations["bigquery_type"].value)

        # 2. Multivalued scalar → ARRAY<inner_type>.
        if slot.multivalued:
            inner = self._get_scalar_type(slot.range, sv)
            return ARRAY(inner)

        # 3. Inlined class-range → STRUCT<field type, ...>.
        if slot.range in sv.all_classes() and (slot.inlined or slot.inlined_as_list):
            return self._build_struct(slot.range, sv)

        # 4. Scalar (default path).
        return self._get_scalar_type(slot.range, sv)

    def _get_scalar_type(self, range_, sv):
        """Resolve a scalar LinkML range name to a BQ SQLAlchemy type."""
        if range_ is None:
            return String()
        if range_ in sv.all_enums():
            return String()
        if range_ in sv.all_classes():
            pk = sv.get_identifier_slot(range_)
            if pk:
                return self._get_scalar_type(pk.range, sv)
            return String()
        if range_ in METAMODEL_TYPE_TO_BASE:
            base = METAMODEL_TYPE_TO_BASE[range_]
        elif range_ in sv.all_types():
            base = sv.all_types()[range_].base
        else:
            logger.warning("Unknown range %r — defaulting to STRING", range_)
            return String()
        return BQ_TYPEMAP.get(base, String())

    def _build_struct(self, class_name, sv):
        """Build a STRUCT<...> type from the induced slots of class_name."""
        _require_bq()
        fields = {}
        for slot in sv.class_induced_slots(class_name):
            fields[slot.name.replace(" ", "_")] = self.get_sql_range(slot, sv=sv)
        return STRUCT(**fields)

    def _resolve_type_override(self, type_str):
        """Return the BQ SQLAlchemy type for a bigquery_type annotation value."""
        _require_bq()
        overrides = {
            "TIMESTAMP": lambda: TIMESTAMP(),
            "DATE": lambda: Date(),
            "DATETIME": lambda: DateTime(),
            "STRING": lambda: String(),
            "INT64": lambda: Integer(),
            "FLOAT64": lambda: Float(),
            "NUMERIC": lambda: Numeric(),
            "BOOL": lambda: Boolean(),
            "TIME": lambda: Time(),
            "BYTES": lambda: LargeBinary(),
        }
        factory = overrides.get(type_str.upper())
        if factory is None:
            raise ValueError(
                f"Unknown bigquery_type annotation value {type_str!r}. "
                f"Valid values: {sorted(overrides)}"
            )
        return factory()


@shared_arguments(BigQueryGenerator)
@click.command(name="bigquery")
@click.option("--dataset", default=None, help="BigQuery dataset prefix")
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, dataset=None, **args):
    """Generate BigQuery DDL representation"""
    gen = BigQueryGenerator(yamlfile, **args)
    if dataset:
        gen.dataset = dataset
    print(gen.serialize())


if __name__ == "__main__":
    cli()
