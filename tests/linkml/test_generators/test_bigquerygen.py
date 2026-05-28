import pytest
from linkml_runtime.linkml_model.meta import SlotDefinition
from sqlalchemy.types import Boolean, Date, DateTime, Float, Integer, Numeric, String, Time

from linkml.generators.bigquerygen import BigQueryGenerator
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
