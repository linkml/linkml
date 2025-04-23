import re
import sqlite3

import pytest
from linkml_runtime.linkml_model.meta import SlotDefinition
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView
from sqlalchemy.dialects.oracle import VARCHAR2
from sqlalchemy.sql.sqltypes import Enum, Integer, Text

from linkml.generators.sqltablegen import SQLTableGenerator
from linkml.utils.schema_builder import SchemaBuilder

# from tests.test_generators.environment import env

# SCHEMA = env.input_path("personinfo.yaml")
# OUT_PATH = env.expected_path("personinfo.relational.yaml")
# RSCHEMA_EXPANDED = env.expected_path("personinfo.relational.expanded.yaml")
# OUT_DDL = env.expected_path("personinfo.ddl.sql")
# META_OUT_DDL = env.expected_path("meta.ddl.sql")
# SQLDDLLOG = env.expected_path("personinfo.sql.log")
# DB = env.expected_path("personinfo.db")
DUMMY_CLASS = "dummy class"


@pytest.fixture
def schema(input_path):
    return str(input_path("personinfo.yaml"))


def test_inject_primary_key():
    """
    test a minimal schema with no primary names declared
    """
    b = SchemaBuilder()
    slots = ["full name", "description"]
    b.add_class(DUMMY_CLASS, slots)
    b.add_defaults()
    gen = SQLTableGenerator(b.schema)
    ddl = gen.generate_ddl()
    assert "PRIMARY KEY (id)" in ddl
    assert "full_name TEXT" in ddl
    assert 'CREATE TABLE "dummy class"' in ddl


def test_no_injection(schema):
    """
    test a minimal schema with no primary names declared
    """
    b = SchemaBuilder()
    slots = ["full name", "description"]
    b.add_class(DUMMY_CLASS, slots)
    b.add_defaults()
    gen = SQLTableGenerator(b.schema, use_foreign_keys=False)
    ddl = gen.generate_ddl()
    assert "PRIMARY KEY (id)" not in ddl
    assert "full_name TEXT" in ddl
    assert 'CREATE TABLE "dummy class"' in ddl

    # now test with full schema
    gen = SQLTableGenerator(schema, use_foreign_keys=False)
    ddl = gen.generate_ddl()
    assert "FOREIGN KEY" not in ddl


def test_dialect():
    """
    test dialect options
    """
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("age", range="integer", description="age of person in years"))
    slots = ["full name", "description", "age"]
    b.add_class(DUMMY_CLASS, slots, description="My dummy class")
    b.add_defaults()
    for dialect in ["postgresql", "sqlite", "mysql"]:
        gen = SQLTableGenerator(b.schema, dialect=dialect)
        ddl = gen.generate_ddl()

        if dialect == "postgresql":
            assert "id SERIAL" in ddl
            assert "COMMENT ON TABLE" in ddl
            assert "COMMENT ON COLUMN" in ddl
        if dialect == "sqlite":
            assert "id INTEGER" in ddl
            # sqlite does not support comments
        if dialect == "mysql":
            # TODO: make this test stricter
            # newer versions of linkml-runtime enforce required for identifier slots
            assert "id INTEGER NOT NULL AUTO_INCREMENT" in ddl or "id INTEGER AUTO_INCREMENT" in ddl
            assert "COMMENT" in ddl


def test_generate_ddl(schema):
    """Generate contents of DDL file as a string."""
    gen = SQLTableGenerator(schema)

    ddl = gen.generate_ddl()
    tables = []
    for item in ddl.splitlines():
        res = re.search(r"\"(.*?)\"", item)
        if res:
            tables.append(res.group(1))

    expected_tables = [
        "NamedThing",
        "Place",
        "Address",
        "Event",
        "Concept",
        "DiagnosisConcept",
        "ProcedureConcept",
        "Relationship",
        "Container",
        "Person",
        "Address",
        "Organization",
    ]
    for expected in expected_tables:
        assert expected in tables


def test_get_sql_range(schema):
    """Test case for the get_sql_range() method."""
    gen = SQLTableGenerator(schema)
    # Test case to enable Varchar2 usage

    # loader = SchemaLoader(data=SCHEMA)
    # schema_def_str = loader.resolve()

    case_1_slot = SlotDefinition(
        name="id",
        definition_uri="https://w3id.org/linkml/examples/personinfo/id",
        mappings=["schema:identifier"],
        from_schema="https://w3id.org/linkml/examples/personinfo",
        range="string",
        slot_uri="schema:identifier",
        owner="Place",
        domain_of=["NamedThing", "Place"],
    )

    case_2_slot = SlotDefinition(
        name="FamilialRelationship_type",
        from_schema="https://w3id.org/linkml/examples/personinfo",
        is_a="type",
        domain="FamilialRelationship",
        range="FamilialRelationshipType",
        slot_uri="personinfo:type",
        alias="type",
        owner="FamilialRelationship",
        domain_of=["FamilialRelationship"],
        usage_slot_name="type",
    )

    case_3_slot = SlotDefinition(name="NonExistentSlot", range="NonExistentRange")

    case_4_slot = SlotDefinition(name="ForeignKeySlot", range="IntegerPrimaryKeyObject")

    # Slot range in list of schema classes
    actual_1_output = gen.get_sql_range(case_1_slot)

    # Slot range in list of schema enums
    actual_2_output = gen.get_sql_range(case_2_slot)

    # Slot not present in schema
    actual_3_output = gen.get_sql_range(case_3_slot)

    # foreign key slot type
    actual_4_output = gen.get_sql_range(case_4_slot)

    # Slot range for oracle dialect type
    # varchar_output = gen_oracle.get_sql_range(case_1_slot)

    assert isinstance(actual_1_output, Text)
    assert isinstance(actual_2_output, Enum)
    assert isinstance(actual_3_output, Text)
    assert isinstance(actual_4_output, Integer)
    # assert isinstance(varchar_output, VARCHAR2())


def test_varchar_sql_range(schema, capsys):
    """Test case for the get_sql_range() method for Varchar."""
    # Test case to enable Varchar2 usage
    gen_oracle = SQLTableGenerator(schema)
    gen_oracle.dialect = "oracle"

    assert gen_oracle.dialect == "oracle"
    assert gen_oracle.default_length_oracle == 4096

    gen_oracle.default_length_oracle = 256
    assert gen_oracle.default_length_oracle == 256
    string_1_slot = SlotDefinition(name="string_column", range="string")
    string_2_slot = SlotDefinition(name="varchar_column", range="VARCHAR")
    string_3_slot = SlotDefinition(name="varchar2_length_column", range="VARCHAR2(128)")
    string_4_slot = SlotDefinition(name="clob_column", range="VARCHAR2(4097)")

    string_1_output = gen_oracle.get_sql_range(string_1_slot)
    assert isinstance(string_1_output, VARCHAR2)

    string_2_output = gen_oracle.get_sql_range(string_2_slot)
    assert isinstance(string_2_output, VARCHAR2)

    string_3_output = gen_oracle.get_sql_range(string_3_slot)
    assert isinstance(string_3_output, VARCHAR2)

    string_4_output = gen_oracle.get_sql_range(string_4_slot)
    assert isinstance(string_4_output, Text)

    # testing the ddl generation of varchars

    b = SchemaBuilder()
    slots = [string_1_slot, string_2_slot, string_3_slot, string_4_slot]
    b.add_class(DUMMY_CLASS, slots, description="My dummy class")

    gen_oracle2 = SQLTableGenerator(b.schema, dialect="oracle")
    gen_oracle2.default_length_oracle = 256
    ddl = gen_oracle2.generate_ddl()
    assert ddl
    assert "string_column VARCHAR2(256 CHAR)" in ddl
    assert "varchar_column VARCHAR2(256 CHAR)" in ddl
    assert "varchar2_length_column VARCHAR2(128 CHAR)" in ddl
    assert "clob_column CLOB" in ddl

    # Utilizing the default settings to ensure errors aren't thrown
    gen_sqlite = SQLTableGenerator(schema)

    assert gen_sqlite.dialect == "sqlite"
    sqlite_1_slot = SlotDefinition(name="string_column", range="string")
    sqlite_2_slot = SlotDefinition(name="varchar_column", range="VARCHAR")
    sqlite_3_slot = SlotDefinition(name="varchar2_length_column", range="VARCHAR2(128)")
    sqlite_4_slot = SlotDefinition(name="clob_column", range="VARCHAR2(4097)")

    # Verifying Text range for sqlite
    sqlite_1_output = gen_sqlite.get_sql_range(sqlite_1_slot)
    assert isinstance(sqlite_1_output, Text)

    sqlite_2_output = gen_sqlite.get_sql_range(sqlite_2_slot)
    assert isinstance(sqlite_2_output, Text)

    sqlite_3_output = gen_sqlite.get_sql_range(sqlite_3_slot)
    assert isinstance(sqlite_3_output, Text)

    sqlite_4_output = gen_sqlite.get_sql_range(sqlite_4_slot)
    assert isinstance(sqlite_4_output, Text)

    c = SchemaBuilder()
    slots = [sqlite_1_slot, sqlite_2_slot, sqlite_3_slot, sqlite_4_slot]
    c.add_class(DUMMY_CLASS, slots, description="My dummy class")
    # The DDL should contain text type
    gen_sqlite2 = SQLTableGenerator(c.schema)
    ddl2 = gen_sqlite2.generate_ddl()
    assert ddl2
    assert "string_column TEXT" in ddl2
    assert "varchar_column TEXT" in ddl2
    assert "varchar2_length_column TEXT" in ddl2
    assert "clob_column TEXT" in ddl2


def test_get_foreign_key(schema):
    """Test case for the get_foreign_key() method."""
    gen = SQLTableGenerator(schema)

    sv = SchemaView(schema=schema)

    fk_value = gen.get_foreign_key("Person", sv)

    assert fk_value == "Person.id"


def test_sqlddl_on_metamodel():
    sv = package_schemaview("linkml_runtime.linkml_model.meta")
    gen = SQLTableGenerator(sv.schema)
    ddl = gen.generate_ddl()
    assert "CREATE TABLE class_definition (" in ddl
    assert "CREATE TABLE annotation (" in ddl


def test_sqlddl_basic(schema):
    """
    End to end example
    """
    # sv = SchemaView(SCHEMA)
    # sqltr = RelationalModelTransformer(sv)
    gen = SQLTableGenerator(schema)
    # ddl = gen.generate_ddl(naming_policy=SqlNamingPolicy.underscore)
    ddl = gen.generate_ddl()

    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.executescript(ddl)
    name = "fred"
    cur.execute(
        "INSERT INTO Person (id, name, age_in_years) VALUES (?,?,?)",
        ("P1", name, 33),
    )
    cur.execute(
        "INSERT INTO Person_alias (Person_id, alias) VALUES (?,?)",
        ("P1", "wibble"),
    )
    cur.execute(
        "INSERT INTO FamilialRelationship (Person_id, type, related_to) VALUES (?,?,?)",
        ("P1", "P2", "BROTHER_OF"),
    )
    cur.execute("select * from Person where name=:name", {"name": name})
    rows = cur.fetchall()
    assert len(rows) == 1
    con.commit()
    with pytest.raises(Exception):
        # PK violation
        cur.execute(
            "INSERT INTO Person (id, name, age_in_years) VALUES (?,?,?)",
            ("P1", "other person", 22),
        )
    with pytest.raises(Exception):
        cur.execute(
            "INSERT INTO Person_alias (Person_id, alias) VALUES (?,?)",
            ("P1", "wibble"),
        )

    con.close()
