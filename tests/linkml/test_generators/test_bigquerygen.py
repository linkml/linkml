import os as _os

import pytest
from sqlalchemy.types import Boolean, Date, DateTime, Float, LargeBinary, Numeric, String, Time

from linkml.generators.bigquerygen import BigQueryGenerator
from linkml_runtime.linkml_model.meta import SlotDefinition
from linkml_runtime.utils.schema_builder import SchemaBuilder


def test_decimal_maps_to_numeric():
    """decimal range must map to NUMERIC, not INTEGER (regression guard against parent RANGEMAP)"""
    b = SchemaBuilder()
    b.add_class("Thing", slots=["price"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    result = gen.get_sql_range(SlotDefinition("price", range="decimal"), b.schema)
    assert isinstance(result, Numeric)


def test_enum_range_maps_to_string():
    """BQ has no ENUM type; enum-ranged slots must compile as STRING"""
    from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue

    b = SchemaBuilder()
    b.schema.enums["Status"] = EnumDefinition(
        name="Status",
        permissible_values={"active": PermissibleValue(text="active")},
    )
    b.add_class("Thing", slots=["status"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    result = gen.get_sql_range(SlotDefinition("status", range="Status"), b.schema)
    assert isinstance(result, String)


def test_datetime_maps_to_datetime():
    """XSDDateTime defaults to DATETIME (timezone-naive) in BQ DDL"""
    b = SchemaBuilder()
    b.add_class("Thing", slots=["ts"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    result = gen.get_sql_range(SlotDefinition("ts", range="datetime"), b.schema)
    assert isinstance(result, DateTime)


def test_bigquery_type_annotation_overrides_mapping():
    """bigquery_type slot annotation takes precedence over automatic type resolution"""
    from sqlalchemy_bigquery import TIMESTAMP

    from linkml_runtime.linkml_model.meta import Annotation

    b = SchemaBuilder()
    b.add_class("Thing", slots=["ts"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    slot = SlotDefinition("ts", range="datetime")
    slot.annotations["bigquery_type"] = Annotation("bigquery_type", "TIMESTAMP")
    result = gen.get_sql_range(slot, b.schema)
    assert isinstance(result, TIMESTAMP)


def test_multivalued_scalar_produces_array():
    """multivalued slot with scalar range → ARRAY<STRING>, not a join table"""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("aliases", range="string", multivalued=True))
    b.add_class("Person", slots=["id", "aliases"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    ddl = gen.generate_ddl()
    assert "ARRAY<STRING>" in ddl
    assert "CREATE TABLE" in ddl


def test_inlined_object_produces_struct():
    """inlined class-range slot → STRUCT<street STRING, city STRING>"""
    from linkml_runtime.linkml_model.meta import SlotDefinition as SD

    b = SchemaBuilder()
    b.add_slot(SD("street", range="string"))
    b.add_slot(SD("city", range="string"))
    b.add_class("Address", slots=["street", "city"])
    b.add_slot(SD("address", range="Address", inlined=True))
    b.add_class("Person", slots=["id", "address"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    ddl = gen.generate_ddl()
    assert "STRUCT<" in ddl
    assert "street STRING" in ddl
    assert "city STRING" in ddl


def test_nested_struct_recursion():
    """a STRUCT whose fields include another inlined class → nested STRUCT<...>"""
    from linkml_runtime.linkml_model.meta import SlotDefinition as SD

    b = SchemaBuilder()
    b.add_slot(SD("lat", range="float"))
    b.add_slot(SD("lon", range="float"))
    b.add_class("GeoPoint", slots=["lat", "lon"])
    b.add_slot(SD("location", range="GeoPoint", inlined=True))
    b.add_slot(SD("street", range="string"))
    b.add_class("Address", slots=["street", "location"])
    b.add_slot(SD("address", range="Address", inlined=True))
    b.add_class("Place", slots=["id", "address"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    ddl = gen.generate_ddl()
    assert "STRUCT<" in ddl


def _make_partitioned_schema(partition_type="DAY", field_range="datetime"):
    """Helper: schema with a class annotated for time partitioning."""
    from linkml_runtime.linkml_model.meta import Annotation

    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_slot(SlotDefinition("created_at", range=field_range))
    b.add_class("Event", slots=["id", "created_at"])
    b.add_defaults()
    c = b.schema.classes["Event"]
    c.annotations["bigquery_partition_by"] = Annotation("bigquery_partition_by", "created_at")
    c.annotations["bigquery_partition_type"] = Annotation("bigquery_partition_type", partition_type)
    return b.schema


def test_time_partition_by_day():
    """bigquery_partition_by + bigquery_partition_type=DAY on a datetime slot"""
    gen = BigQueryGenerator(_make_partitioned_schema("DAY"))
    ddl = gen.generate_ddl()
    assert "PARTITION BY DATETIME_TRUNC(created_at, DAY)" in ddl


def test_time_partition_by_month():
    """bigquery_partition_type=MONTH produces DATETIME_TRUNC(..., MONTH)"""
    gen = BigQueryGenerator(_make_partitioned_schema("MONTH"))
    ddl = gen.generate_ddl()
    assert "PARTITION BY DATETIME_TRUNC(created_at, MONTH)" in ddl


def test_range_partition():
    """bigquery_partition_type=RANGE on an integer slot produces RANGE_BUCKET(...)"""
    from linkml_runtime.linkml_model.meta import Annotation

    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_slot(SlotDefinition("user_id", range="integer"))
    b.add_class("Event", slots=["id", "user_id"])
    b.add_defaults()
    c = b.schema.classes["Event"]
    c.annotations["bigquery_partition_by"] = Annotation("bigquery_partition_by", "user_id")
    c.annotations["bigquery_partition_type"] = Annotation("bigquery_partition_type", "RANGE")
    c.annotations["bigquery_partition_range"] = Annotation("bigquery_partition_range", "0,100,10")
    gen = BigQueryGenerator(b.schema)
    ddl = gen.generate_ddl()
    assert "PARTITION BY RANGE_BUCKET" in ddl


def test_cluster_by():
    """bigquery_cluster_by annotation produces CLUSTER BY clause"""
    from linkml_runtime.linkml_model.meta import Annotation

    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_slot(SlotDefinition("region", range="string"))
    b.add_class("Event", slots=["id", "region"])
    b.add_defaults()
    c = b.schema.classes["Event"]
    c.annotations["bigquery_cluster_by"] = Annotation("bigquery_cluster_by", "region, id")
    gen = BigQueryGenerator(b.schema)
    ddl = gen.generate_ddl()
    assert "CLUSTER BY region, id" in ddl


def test_partition_and_cluster_combined():
    """PARTITION BY and CLUSTER BY can appear together on the same table"""
    from linkml_runtime.linkml_model.meta import Annotation

    schema = _make_partitioned_schema("DAY")
    c = schema.classes["Event"]
    c.annotations["bigquery_cluster_by"] = Annotation("bigquery_cluster_by", "id")
    gen = BigQueryGenerator(schema)
    ddl = gen.generate_ddl()
    assert "PARTITION BY" in ddl
    assert "CLUSTER BY" in ddl


def test_partition_expiration_and_filter():
    """partition_expiration_days and require_partition_filter appear in OPTIONS(...)"""
    from linkml_runtime.linkml_model.meta import Annotation

    schema = _make_partitioned_schema("DAY")
    c = schema.classes["Event"]
    c.annotations["bigquery_partition_expiration_days"] = Annotation("bigquery_partition_expiration_days", "90")
    c.annotations["bigquery_require_partition_filter"] = Annotation("bigquery_require_partition_filter", "true")
    gen = BigQueryGenerator(schema)
    ddl = gen.generate_ddl()
    assert "OPTIONS(" in ddl
    assert "require_partition_filter=true" in ddl


def test_partition_on_nonexistent_field_raises():
    """bigquery_partition_by naming a field not in the class must raise ValueError"""
    from linkml_runtime.linkml_model.meta import Annotation

    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_class("Event", slots=["id"])
    b.add_defaults()
    c = b.schema.classes["Event"]
    c.annotations["bigquery_partition_by"] = Annotation("bigquery_partition_by", "nonexistent")
    gen = BigQueryGenerator(b.schema)
    with pytest.raises(ValueError, match="nonexistent"):
        gen.generate_ddl()


def test_time_partition_on_string_field_raises():
    """time partitioning on a STRING field must raise ValueError mentioning 'date'"""
    from linkml_runtime.linkml_model.meta import Annotation

    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_slot(SlotDefinition("name", range="string"))
    b.add_class("Event", slots=["id", "name"])
    b.add_defaults()
    c = b.schema.classes["Event"]
    c.annotations["bigquery_partition_by"] = Annotation("bigquery_partition_by", "name")
    c.annotations["bigquery_partition_type"] = Annotation("bigquery_partition_type", "DAY")
    gen = BigQueryGenerator(b.schema)
    with pytest.raises(ValueError, match="date"):
        gen.generate_ddl()


def test_range_partition_on_non_integer_field_raises():
    """range partitioning on a non-integer field must raise ValueError mentioning 'integer'"""
    from linkml_runtime.linkml_model.meta import Annotation

    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_slot(SlotDefinition("label", range="string"))
    b.add_class("Event", slots=["id", "label"])
    b.add_defaults()
    c = b.schema.classes["Event"]
    c.annotations["bigquery_partition_by"] = Annotation("bigquery_partition_by", "label")
    c.annotations["bigquery_partition_type"] = Annotation("bigquery_partition_type", "RANGE")
    c.annotations["bigquery_partition_range"] = Annotation("bigquery_partition_range", "0,100,10")
    gen = BigQueryGenerator(b.schema)
    with pytest.raises(ValueError, match="integer"):
        gen.generate_ddl()


# ---------------------------------------------------------------------------
# Task 6 — Schema traversal: inheritance, abstract classes, mixins
# ---------------------------------------------------------------------------


def test_inherited_slots_appear_in_child_ddl():
    """A child class must include slots defined on its parent in the generated DDL."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_slot(SlotDefinition("name", range="string"))
    b.add_slot(SlotDefinition("email", range="string"))
    b.add_class("NamedThing", slots=["id", "name"])
    b.add_class("Person", slots=["email"], is_a="NamedThing")
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    ddl = gen.generate_ddl()
    person_ddl = next(block for block in ddl.split("\n\n") if "Person" in block)
    assert "id" in person_ddl
    assert "name" in person_ddl
    assert "email" in person_ddl


def test_abstract_class_produces_no_table():
    """Abstract classes must not appear as CREATE TABLE statements."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_class("AbstractBase", slots=["id"])
    b.schema.classes["AbstractBase"].abstract = True
    b.add_class("Concrete", slots=["id"], is_a="AbstractBase")
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    ddl = gen.generate_ddl()
    assert "AbstractBase" not in ddl
    assert "Concrete" in ddl


def test_mixin_slots_appear_in_class_ddl():
    """Slots contributed by a mixin must be flattened into the mixing class's DDL."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_slot(SlotDefinition("created_at", range="datetime"))
    b.add_class("Timestamped", slots=["created_at"])
    b.schema.classes["Timestamped"].mixin = True
    b.add_class("Event", slots=["id"])
    b.schema.classes["Event"].mixins = ["Timestamped"]
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    ddl = gen.generate_ddl()
    event_ddl = next(block for block in ddl.split("\n\n") if "Event" in block)
    assert "created_at" in event_ddl
    assert "Timestamped" not in ddl


# ---------------------------------------------------------------------------
# Task 8 — Integration test with personinfo.yaml
# ---------------------------------------------------------------------------

_PERSONINFO_YAML = _os.path.join(
    _os.path.dirname(__file__),
    "..",
    "..",
    "..",
    "examples",
    "PersonSchema",
    "personinfo.yaml",
)


@pytest.mark.integration
def test_personinfo_generates_valid_ddl():
    """BigQueryGenerator must produce valid CREATE TABLE DDL for the personinfo schema
    without errors, and include expected concrete classes (Person, Organization)
    while excluding abstract/mixin classes."""
    gen = BigQueryGenerator(_PERSONINFO_YAML)
    ddl = gen.generate_ddl()
    assert "CREATE TABLE" in ddl
    # Concrete classes must appear
    assert "Person" in ddl
    assert "Organization" in ddl
    # Each statement must be terminated
    for block in ddl.split("\n\n"):
        if block.strip():
            assert block.rstrip().endswith(";"), f"DDL block missing semicolon:\n{block}"


# ---------------------------------------------------------------------------
# Task 7 — Generator defaults and --dataset flag
# ---------------------------------------------------------------------------


def test_use_foreign_keys_is_false_by_default():
    """BigQueryGenerator must default use_foreign_keys=False (BQ doesn't enforce FKs)."""
    b = SchemaBuilder()
    b.add_class("Thing", slots=["id"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    assert gen.use_foreign_keys is False


def test_inject_primary_keys_is_false_by_default():
    """BigQueryGenerator must default inject_primary_keys=False (BQ PKs are non-enforced)."""
    b = SchemaBuilder()
    b.add_class("Thing", slots=["id"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    assert gen.inject_primary_keys is False


def test_dataset_prefix_applied_to_table_names():
    """When dataset is set, table names must be emitted as `dataset.ClassName`."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_class("Person", slots=["id"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    gen.dataset = "my_dataset"
    ddl = gen.generate_ddl()
    assert "my_dataset.Person" in ddl


def test_serialize_delegates_to_generate_ddl():
    """serialize() must return the same output as generate_ddl()."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_class("Thing", slots=["id"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    assert gen.serialize() == gen.generate_ddl()


def test_get_sql_range_without_sv_argument():
    """get_sql_range() must build SchemaView internally when sv is not supplied."""
    b = SchemaBuilder()
    b.add_class("Thing", slots=["id"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    result = gen.get_sql_range(SlotDefinition("id", range="string"))
    assert isinstance(result, String)


def test_inlined_as_list_produces_array_of_struct():
    """inlined_as_list slot → ARRAY<STRUCT<...>> (list of embedded objects)."""
    from linkml_runtime.linkml_model.meta import SlotDefinition as SD

    b = SchemaBuilder()
    b.add_slot(SD("street", range="string"))
    b.add_class("Address", slots=["street"])
    b.add_slot(SD("addresses", range="Address", inlined_as_list=True, multivalued=True))
    b.add_class("Person", slots=["id", "addresses"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    ddl = gen.generate_ddl()
    assert "ARRAY<" in ddl


def test_unknown_range_defaults_to_string(caplog):
    """An unrecognised range name must log a warning and map to STRING."""
    import logging

    b = SchemaBuilder()
    b.add_class("Thing", slots=["id"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    with caplog.at_level(logging.WARNING, logger="linkml.generators.bigquerygen"):
        result = gen.get_sql_range(SlotDefinition("x", range="NonExistentType"), b.schema)
    assert isinstance(result, String)
    assert "NonExistentType" in caplog.text


def test_class_range_without_identifier_defaults_to_string():
    """A slot whose range is a class with no identifier slot must resolve to STRING."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("zip_code", range="string"))
    b.add_class("PostalAddress", slots=["zip_code"])
    b.add_slot(SlotDefinition("mailing_address", range="PostalAddress"))
    b.add_class("Person", slots=["id", "mailing_address"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    result = gen.get_sql_range(SlotDefinition("mailing_address", range="PostalAddress"), b.schema)
    assert isinstance(result, String)


@pytest.mark.parametrize(
    "type_str, expected_class",
    [
        ("DATE", Date),
        ("DATETIME", DateTime),
        ("STRING", String),
        ("FLOAT64", Float),
        ("NUMERIC", Numeric),
        ("BOOL", Boolean),
        ("TIME", Time),
        ("BYTES", LargeBinary),
    ],
)
def test_resolve_type_override_all_types(type_str, expected_class):
    """Every valid bigquery_type annotation value must resolve without error."""
    b = SchemaBuilder()
    b.add_class("Thing", slots=["id"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    result = gen._resolve_type_override(type_str)
    assert isinstance(result, expected_class)


def test_resolve_type_override_int64():
    """INT64 bigquery_type annotation must resolve to INTEGER."""
    from sqlalchemy.types import INTEGER

    b = SchemaBuilder()
    b.add_class("Thing", slots=["id"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    assert isinstance(gen._resolve_type_override("INT64"), INTEGER)


def test_resolve_type_override_invalid_raises():
    """An unrecognised bigquery_type annotation value must raise ValueError."""
    b = SchemaBuilder()
    b.add_class("Thing", slots=["id"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    with pytest.raises(ValueError, match="NOTATYPE"):
        gen._resolve_type_override("NOTATYPE")


def test_bigquery_description_in_options():
    """bigquery_description annotation must appear in the generated OPTIONS clause."""
    from linkml_runtime.linkml_model.meta import Annotation

    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_class("Event", slots=["id"])
    b.add_defaults()
    b.schema.classes["Event"].annotations["bigquery_description"] = Annotation(
        "bigquery_description", "Tracks user events"
    )
    gen = BigQueryGenerator(b.schema)
    ddl = gen.generate_ddl()
    assert "Tracks user events" in ddl


def test_cli_produces_ddl(tmp_path):
    """The gen-bigquery CLI entry point must print valid DDL to stdout."""
    from click.testing import CliRunner

    from linkml.generators.bigquerygen import cli

    runner = CliRunner()
    result = runner.invoke(cli, [str(_PERSONINFO_YAML)])
    assert result.exit_code == 0, result.output
    assert "CREATE TABLE" in result.output


def test_cli_dataset_flag():
    """--dataset flag must prefix table names in CLI output."""
    from click.testing import CliRunner

    from linkml.generators.bigquerygen import cli

    runner = CliRunner()
    result = runner.invoke(cli, [str(_PERSONINFO_YAML), "--dataset", "my_ds"])
    assert result.exit_code == 0, result.output
    assert "my_ds." in result.output


def test_class_with_no_slots_skipped_in_ddl():
    """A concrete class that induces no slots must produce no CREATE TABLE statement."""
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("id", range="string", identifier=True))
    b.add_class("Empty")  # no slots
    b.add_class("HasId", slots=["id"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    ddl = gen.generate_ddl()
    assert "Empty" not in ddl
    assert "HasId" in ddl


def test_custom_type_with_unmapped_base_defaults_to_string():
    """A custom type whose base is not in BQ_TYPEMAP must fall back to STRING."""
    from linkml_runtime.linkml_model.meta import TypeDefinition

    b = SchemaBuilder()
    b.schema.types["MyBytes"] = TypeDefinition(name="MyBytes", base="bytes", uri="xsd:base64Binary")
    b.add_slot(SlotDefinition("payload", range="MyBytes"))
    b.add_class("Thing", slots=["id", "payload"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    result = gen.get_sql_range(SlotDefinition("payload", range="MyBytes"), b.schema)
    assert isinstance(result, String)


def test_none_range_defaults_to_string():
    """A slot with no range set must resolve to STRING without error."""
    b = SchemaBuilder()
    b.add_class("Thing", slots=["id"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    from linkml_runtime.utils.schemaview import SchemaView

    sv = SchemaView(b.schema)
    result = gen._get_scalar_type(None, sv)
    assert isinstance(result, String)


def test_require_partition_filter_false_omitted_from_options():
    """bigquery_require_partition_filter=false must not add require_partition_filter to OPTIONS."""
    from linkml_runtime.linkml_model.meta import Annotation

    schema = _make_partitioned_schema("DAY")
    c = schema.classes["Event"]
    c.annotations["bigquery_require_partition_filter"] = Annotation("bigquery_require_partition_filter", "false")
    gen = BigQueryGenerator(schema)
    ddl = gen.generate_ddl()
    assert "require_partition_filter" not in ddl


def test_inlined_as_list_non_multivalued_produces_struct():
    """inlined_as_list=True on a non-multivalued slot must produce STRUCT, not ARRAY."""
    from linkml_runtime.linkml_model.meta import SlotDefinition as SD

    b = SchemaBuilder()
    b.add_slot(SD("label", range="string"))
    b.add_class("Tag", slots=["label"])
    b.add_slot(SD("primary_tag", range="Tag", inlined_as_list=True))
    b.add_class("Article", slots=["id", "primary_tag"])
    b.add_defaults()
    gen = BigQueryGenerator(b.schema)
    ddl = gen.generate_ddl()
    assert "STRUCT<" in ddl
    assert "ARRAY<" not in ddl.split("Article")[1].split(";")[0]


def test_semver_from_package_unknown_returns_zero():
    """SemVer.from_package() must return 0.0.0 for an uninstalled package."""
    from linkml.utils.deprecation import SemVer

    v = SemVer.from_package("linkml-nonexistent-package-xyzzy")
    assert v.major == 0
    assert v.minor == 0
    assert v.patch == 0


# ---------------------------------------------------------------------------
# Full-features integration test using bigquery_features.yaml
# ---------------------------------------------------------------------------

_FEATURES_YAML = _os.path.join(
    _os.path.dirname(__file__),
    "input",
    "bigquery_features.yaml",
)


@pytest.mark.integration
def test_bigquery_features_schema():
    """Full integration test against tests/linkml/test_generators/input/bigquery_features.yaml.

    Expected DDL (abbreviated):

        CREATE TABLE `GeoPoint` (
            `lat` FLOAT64,
            `lon` FLOAT64
        );

        CREATE TABLE `Address` (
            `street` STRING,
            `city` STRING,
            `location` STRUCT<lat FLOAT64, lon FLOAT64>   -- inlined GeoPoint
        );

        CREATE TABLE `Event` (
            `name` STRING,
            `status` STRING,                              -- enum EventStatus → STRING
            `tags` ARRAY<STRING>,                         -- multivalued scalar
            `home_address` STRUCT<street STRING,          -- inlined Address with nested STRUCT
                                  city STRING,
                                  location STRUCT<lat FLOAT64, lon FLOAT64>>,
            `score` NUMERIC,                              -- decimal → NUMERIC
            `recorded_at` TIMESTAMP,                      -- bigquery_type: TIMESTAMP override
            `created_at` DATETIME,                        -- partition field
            `updated_at` DATETIME,                        -- from HasTimestamps mixin
            `id` STRING NOT NULL                          -- from Identifiable base class
        ) PARTITION BY DATETIME_TRUNC(created_at, DAY)
        CLUSTER BY name, status
        OPTIONS(partition_expiration_days=90.0, require_partition_filter=true);

        CREATE TABLE `MetricSnapshot` (
            `id` STRING NOT NULL,
            `bucket_id` INT64,                            -- integer range partition field
            `value` FLOAT64
        ) PARTITION BY RANGE_BUCKET(bucket_id, GENERATE_ARRAY(0, 1000, 100));

    Classes NOT expected in output:
        - Identifiable  (abstract=true)
        - HasTimestamps (mixin=true)
    """
    gen = BigQueryGenerator(_FEATURES_YAML)
    ddl = gen.generate_ddl()

    # Helpers: extract per-table DDL blocks for targeted assertions
    def get_block(table: str) -> str:
        return next(
            b
            for b in ddl.split("\n\n")
            if f"`{table}`" in b or f" {table} " in b or b.startswith(f"CREATE TABLE `{table}`")
        )

    event = get_block("Event")
    metric = get_block("MetricSnapshot")
    address = get_block("Address")

    # ── Abstract and mixin classes produce no table ──────────────────────────
    assert "Identifiable" not in ddl
    assert "HasTimestamps" not in ddl

    # ── GeoPoint and Address exist as standalone tables ──────────────────────
    assert "GeoPoint" in ddl
    assert "Address" in ddl

    # ── Event: inherited slot from abstract Identifiable ─────────────────────
    assert "`id` STRING NOT NULL" in event

    # ── Event: mixin slots from HasTimestamps ────────────────────────────────
    assert "`created_at` DATETIME" in event
    assert "`updated_at` DATETIME" in event

    # ── Event: enum-ranged slot → STRING ─────────────────────────────────────
    assert "`status` STRING" in event

    # ── Event: multivalued scalar slot → ARRAY<STRING> ───────────────────────
    assert "`tags` ARRAY<STRING>" in event

    # ── Event: inlined Address → STRUCT with nested GeoPoint STRUCT ──────────
    assert "STRUCT<street STRING, city STRING, location STRUCT<lat FLOAT64, lon FLOAT64>>" in event

    # ── Event: decimal slot → NUMERIC ────────────────────────────────────────
    assert "`score` NUMERIC" in event

    # ── Event: bigquery_type:TIMESTAMP annotation overrides DATETIME ─────────
    assert "`recorded_at` TIMESTAMP" in event

    # ── Event: PARTITION BY DATETIME_TRUNC (time partition, DAY) ────────────
    assert "PARTITION BY DATETIME_TRUNC(created_at, DAY)" in event

    # ── Event: CLUSTER BY ────────────────────────────────────────────────────
    assert "CLUSTER BY name, status" in event

    # ── Event: OPTIONS with partition expiration and required filter ─────────
    assert "OPTIONS(" in event
    assert "partition_expiration_days=90.0" in event
    assert "require_partition_filter=true" in event

    # ── Address: nested STRUCT for inlined GeoPoint ──────────────────────────
    assert "`location` STRUCT<lat FLOAT64, lon FLOAT64>" in address

    # ── MetricSnapshot: integer RANGE partition ───────────────────────────────
    assert "PARTITION BY RANGE_BUCKET(bucket_id, GENERATE_ARRAY(0, 1000, 100))" in metric

    # ── Every statement ends with a semicolon ────────────────────────────────
    for block in ddl.split("\n\n"):
        if block.strip():
            assert block.rstrip().endswith(";"), f"Missing semicolon:\n{block}"
