import logging
import os
from dataclasses import dataclass

import click
from sqlalchemy import Column, MetaData, Table  # noqa: F401 — used in generate_ddl and get_sql_range
from sqlalchemy.schema import CreateTable  # noqa: F401 — used in generate_ddl and get_sql_range
from sqlalchemy.types import (  # noqa: F401 — used in generate_ddl and get_sql_range
    INTEGER,
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    LargeBinary,
    Numeric,
    String,
    Time,
)

from linkml._version import __version__
from linkml.generators.sqltablegen import (  # noqa: F401 — used in generate_ddl and get_sql_range
    METAMODEL_TYPE_TO_BASE,
    SQLTableGenerator,
)
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
            import google.cloud.bigquery as bigquery
            from sqlalchemy_bigquery import ARRAY, STRUCT, TIMESTAMP, BigQueryDialect

            _BQ_AVAILABLE = True
        except ImportError as exc:  # pragma: no cover
            raise ImportError("sqlalchemy-bigquery is required. Install with: pip install 'linkml[bigquery]'") from exc


# Maps LinkML type bases to BigQuery SQLAlchemy types.
# Replaces the parent's RANGEMAP — every mapping here is explicit and BQ-correct.
BQ_TYPEMAP = {
    "str": String(),
    "string": String(),
    "int": INTEGER(),
    "float": Float(),
    "double": Float(),
    "Decimal": Numeric(),  # parent maps this to Integer() — incorrect for BQ
    "Bool": Boolean(),
    "URI": String(),
    "URIorCURIE": String(),
    "NCName": String(),
    "ElementIdentifier": String(),
    "NodeIdentifier": String(),
    "XSDDate": Date(),
    "XSDTime": Time(),
    "XSDDateTime": DateTime(),  # → DATETIME in BQ; use bigquery_type: TIMESTAMP to override
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
    dataset: str | None = None

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
            except Exception as exc:  # pragma: no cover
                raise ValueError(f"Failed to generate DDL for class {cn!r}: {exc}") from exc

        return "\n\n".join(ddl_parts)

    def _validate_partition(self, class_def, sv) -> None:
        """Raise ValueError with a clear message if partition annotations are misconfigured.

        Called before CreateTable.compile() so errors surface cleanly, not as crashes.
        """
        ann = class_def.annotations
        partition_field_ann = ann.get("bigquery_partition_by")
        if partition_field_ann is None:
            return

        cn = class_def.name
        field_name = partition_field_ann.value
        induced_slot_names = {s.name for s in sv.class_induced_slots(cn)}

        if field_name not in induced_slot_names:
            raise ValueError(
                f"Class {cn!r}: bigquery_partition_by field {field_name!r} "
                f"is not a slot of this class. Available slots: {sorted(induced_slot_names)}"
            )

        slot = next(s for s in sv.class_induced_slots(cn) if s.name == field_name)
        bq_type = self.get_sql_range(slot, sv=sv)
        partition_type = ann["bigquery_partition_type"].value if "bigquery_partition_type" in ann else "DAY"

        if partition_type == "RANGE":
            # Range partitioning requires an integer column (INT64 in BQ).
            if not isinstance(bq_type, INTEGER | Integer):
                raise ValueError(
                    f"Class {cn!r}: bigquery_partition_type=RANGE requires an integer field, "
                    f"but {field_name!r} resolves to {type(bq_type).__name__}. "
                    f"Set the slot range to 'integer'."
                )
        else:
            # Time partitioning requires DATE, DATETIME, or TIMESTAMP.
            # sqlalchemy_bigquery.TIMESTAMP inherits from DateTime, so isinstance covers all three.
            if not isinstance(bq_type, Date | DateTime):
                raise ValueError(
                    f"Class {cn!r}: time partitioning requires a date/datetime/timestamp field, "
                    f"but {field_name!r} resolves to {type(bq_type).__name__}. "
                    f"Set the slot range to 'date' or 'datetime', or add a "
                    f"'bigquery_type: TIMESTAMP' annotation."
                )

    def _bq_table_kwargs(self, class_def, _sv) -> dict:
        """Build BigQuery dialect kwargs from bigquery_* class annotations."""
        _require_bq()
        ann = class_def.annotations
        kwargs = {}

        partition_field_ann = ann.get("bigquery_partition_by")
        cluster_by_ann = ann.get("bigquery_cluster_by")

        if cluster_by_ann:
            kwargs["bigquery_clustering_fields"] = [f.strip() for f in cluster_by_ann.value.split(",")]

        if "bigquery_description" in ann:
            kwargs["bigquery_description"] = ann["bigquery_description"].value

        if partition_field_ann is None:
            return kwargs

        field_name = partition_field_ann.value
        partition_type = ann["bigquery_partition_type"].value if "bigquery_partition_type" in ann else "DAY"
        expiration_days_ann = ann.get("bigquery_partition_expiration_days")
        require_filter_ann = ann.get("bigquery_require_partition_filter")

        if partition_type == "RANGE":
            raw = ann["bigquery_partition_range"].value
            start, end, interval = [int(x.strip()) for x in raw.split(",")]
            kwargs["bigquery_range_partitioning"] = bigquery.RangePartitioning(
                field=field_name,
                range_=bigquery.PartitionRange(start=start, end=end, interval=interval),
            )
        else:
            tp_kwargs = {"field": field_name, "type_": partition_type}
            if expiration_days_ann:
                days = float(expiration_days_ann.value)
                tp_kwargs["expiration_ms"] = int(days * 24 * 60 * 60 * 1000)
            kwargs["bigquery_time_partitioning"] = bigquery.TimePartitioning(**tp_kwargs)

        if require_filter_ann and require_filter_ann.value.lower() == "true":
            kwargs["bigquery_require_partition_filter"] = True

        return kwargs

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
            "INT64": lambda: INTEGER(),
            "FLOAT64": lambda: Float(),
            "NUMERIC": lambda: Numeric(),
            "BOOL": lambda: Boolean(),
            "TIME": lambda: Time(),
            "BYTES": lambda: LargeBinary(),
        }
        factory = overrides.get(type_str.upper())
        if factory is None:
            raise ValueError(f"Unknown bigquery_type annotation value {type_str!r}. Valid values: {sorted(overrides)}")
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


if __name__ == "__main__":  # pragma: no cover
    cli()
