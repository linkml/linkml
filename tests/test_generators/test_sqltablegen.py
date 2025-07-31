import re
import sqlite3

import pytest
from linkml_runtime.linkml_model.meta import Annotation, SlotDefinition, UniqueKey
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView
from sqlalchemy.dialects.oracle import VARCHAR2
from sqlalchemy.sql.sqltypes import Boolean, Date, DateTime, Enum, Float, Integer, Text, Time

from linkml.generators.sqltablegen import ORACLE_MAX_VARCHAR_LENGTH, SQLTableGenerator
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
def schema(input_path) -> str:
    return str(input_path("personinfo.yaml"))


def test_inject_primary_key() -> None:
    """Test a minimal schema with no primary names declared, PK injection."""
    b = SchemaBuilder()
    slots = ["full name", "description"]
    b.add_class(DUMMY_CLASS, slots)
    b.add_defaults()
    gen = SQLTableGenerator(b.schema)
    ddl = gen.generate_ddl()
    assert "PRIMARY KEY (id)" in ddl
    assert "full_name TEXT" in ddl
    assert 'CREATE TABLE "dummy class"' in ddl


def test_no_injection(schema: str) -> None:
    """Test a minimal schema with no primary names declared, no PK injection."""
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


def test_dialect() -> None:
    """Test dialect options."""
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


def test_generate_ddl(schema: str) -> None:
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


def test_abstract_class(capsys):
    b = SchemaBuilder()
    slots = ["full name", "description"]
    abstract_def = {"abstract": 1}
    b.add_class(DUMMY_CLASS, slots, **abstract_def)
    new_slots = ["nickname"]
    inheritance_def = {"is_a": "dummy class"}
    b.add_class("inherited class", new_slots, **inheritance_def)
    b.add_defaults()
    # Testing the inheritance of an abstract class
    gen = SQLTableGenerator(b.schema, generate_abstract_class_ddl=False)
    ddl = gen.generate_ddl()
    assert "Abstract Class: dummy class" in ddl
    assert 'CREATE TABLE "dummy class"' not in ddl
    assert 'CREATE TABLE "inherited class"' in ddl
    # Creating and asserting the default values work
    gen2 = SQLTableGenerator(b.schema)
    assert gen2.generate_abstract_class_ddl
    ddl2 = gen2.generate_ddl()
    assert "Abstract Class: dummy class" in ddl2
    assert 'CREATE TABLE "dummy class"' in ddl2
    assert 'CREATE TABLE "inherited class"' in ddl2


def test_index_sqlddl():
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("age", range="integer", description="age of person in years"))
    b.add_slot(SlotDefinition("dummy_foreign_key", range="Class With Nowt", description="foreign key test"))
    b.add_slot("identifier_slot", identifier=True)
    slots = ["full name", "description", "dummy_foreign_key", "age"]
    # Simple Multicolumn index defined in annotation
    test_index = Annotation(tag="index", value={"index2": ["id", "age"], "index_desc": ["description"]})
    # Duplicate Index Name
    test_index_2 = Annotation(tag="index", value={"ix_Class_With_Id_identifier_slot": ["identifier_slot", "name"]})
    test_index_3 = Annotation(tag="index", value={"Class_With_Nowt_slot_1_slot_2_idx": ["slot_1"]})
    test_index_dict = {"index": test_index}
    test_index_dict_2 = {"index": test_index_2}
    test_index_dict_3 = {"index": test_index_3}
    # testing to ensure
    b.add_class(DUMMY_CLASS, slots, description="My dummy class", annotations=test_index_dict)
    # testing to ensure the duplicated index isn't generated
    b.add_class("Class_With_Id", slots=["identifier_slot", "name", "whatever"], annotations=test_index_dict_2)
    # Testing Unique Constraint
    slot_1_2_UK = UniqueKey(unique_key_name="unique_keys", unique_key_slots=["slot_1", "slot_2"])
    b.add_class(
        "Class_With_Nowt",
        slots=["slot_1", "slot_2"],
        annotations=test_index_dict_3,
        unique_keys={"unique_keys": slot_1_2_UK},
    )
    gen = SQLTableGenerator(b.schema, use_foreign_keys=True)
    ddl = gen.generate_ddl()
    # Tests autogeneration of primary key index
    assert 'CREATE INDEX "ix_dummy class_id" ON "dummy class" (id);' in ddl
    # Test the multi-column index defined in annotation
    assert 'CREATE INDEX index2 ON "dummy class" (id, age);' in ddl
    assert 'CREATE INDEX index_desc ON "dummy class" (description);' in ddl
    # Tests generation of unique key index
    assert 'CREATE INDEX "Class_With_Nowt_slot_1_slot_2_idx" ON "Class_With_Nowt" (slot_1, slot_2);' in ddl
    # Tests to ensure that an index with a duplicate name as a previous index is not created
    assert 'CREATE INDEX "Class_With_Nowt_slot_1_slot_2_idx" ON "Class_With_Nowt" (slot_1);' not in ddl
    # Test for the foreign key identifier slots
    assert 'CREATE INDEX "ix_Class_With_Id_identifier_slot" ON "Class_With_Id" (identifier_slot);' in ddl
    assert 'CREATE INDEX "ix_Class_With_Nowt_id" ON "Class_With_Nowt" (id)' in ddl
    # Tests to ensure the duplicate index name isn't created
    assert 'CREATE INDEX "ix_Class_With_Id_identifier_slot" ON "Class_With_Id" (identifier_slot, name);' not in ddl


@pytest.mark.parametrize(
    ("slot_range", "ddl_type"),
    [
        ("Person", Text),  # class with a text PK
        ("IntegerPrimaryKeyObject", Integer),  # class with an int PK
        ("MedicalEvent", Text),  # class with no PK
        ("NonExistentRange", Text),  # class that doesn't exist
        ("FamilialRelationshipType", Enum),  # enum
        ("jsonpath", Text),  # type, base type is string
        ("str", Text),
        ("string", Text),
        ("integer", Integer),
        ("boolean", Boolean),
        ("float", Float),
        ("double", Float),
        ("decimal", Integer),  # ???
        ("time", Time),
        ("date", Date),
        ("datetime", DateTime),
        ("uriorcurie", Text),
        ("uri", Text),
        ("ncname", Text),
        ("objectidentifier", Text),
        ("nodeidentifier", Text),
        # various incorrect types that get set to text instead
        ("int", Text),  # "int" is invalid -- should be "integer"
        ("number", Text),  # "int" is invalid -- should be "integer"
    ],
)
def test_get_sql_range(schema: str, slot_range: str, ddl_type: type) -> None:
    """Test case for the get_sql_range() method."""
    gen = SQLTableGenerator(schema)
    slot = SlotDefinition(name="range_test", range=slot_range)
    assert isinstance(gen.get_sql_range(slot), ddl_type)


def test_varchar_sql_range(capsys) -> None:
    """Test cases for the get_oracle_sql_range() method for Varchar."""
    slots = [
        SlotDefinition(name="str_column", range="str"),
        SlotDefinition(name="string_column", range="String"),
        SlotDefinition(name="std_string_column", range="string"),  # the standard string type
        SlotDefinition(name="varchar_column", range="VARCHAR"),
        SlotDefinition(name="varchar2_column_no_len", range="VARCHAR2"),
        SlotDefinition(name="varchar2_length_column", range="VARCHAR2(128)"),
        SlotDefinition(name="clob_column", range="VARCHAR2(4097)"),
    ]

    sb = SchemaBuilder()
    sb.add_class(DUMMY_CLASS, slots, description="My dummy class")
    # add in the ranges as types to ensure that the schema will validate
    for varchar in ["str", "String", "VARCHAR", "VARCHAR2", "VARCHAR2(128)", "VARCHAR2(4097)"]:
        sb.add_type(varchar, typeof="string")
    sb.add_defaults()

    # Test case to enable Varchar2 usage
    gen_oracle = SQLTableGenerator(sb.schema, dialect="oracle")
    assert gen_oracle.dialect == "oracle"
    # default length should initially be 4096
    assert gen_oracle.default_length_oracle == ORACLE_MAX_VARCHAR_LENGTH

    # set the default varchar2 length to different values and ensure the ddl reflects them
    for default_length in [256, 4096, 666]:
        gen_oracle.default_length_oracle = default_length
        for slot in slots:
            sql_range = VARCHAR2
            if slot.name == "clob_column":
                # clob_column is over the VARCHAR2 length limit
                sql_range = Text
            assert isinstance(gen_oracle.get_sql_range(slot), sql_range)

        oracle_ddl = gen_oracle.generate_ddl()
        assert f"str_column VARCHAR2({default_length} CHAR)" in oracle_ddl
        assert f"string_column VARCHAR2({default_length} CHAR)" in oracle_ddl
        assert f"std_string_column VARCHAR2({default_length} CHAR)" in oracle_ddl
        assert f"varchar_column VARCHAR2({default_length} CHAR)" in oracle_ddl
        assert f"varchar2_column_no_len VARCHAR2({default_length} CHAR)" in oracle_ddl
        assert "varchar2_length_column VARCHAR2(128 CHAR)" in oracle_ddl
        assert "clob_column CLOB" in oracle_ddl

    # Utilizing the default settings to ensure errors aren't thrown
    gen_sqlite = SQLTableGenerator(sb.schema)
    assert gen_sqlite.dialect == "sqlite"

    # Verifying Text range for sqlite
    for slot_n in slots:
        assert isinstance(gen_sqlite.get_sql_range(slot_n), Text)

    # The DDL should contain text type
    ddl_sqlite = gen_sqlite.generate_ddl()
    assert ddl_sqlite
    assert "str_column TEXT" in ddl_sqlite
    assert "string_column TEXT" in ddl_sqlite
    assert "std_string_column TEXT" in ddl_sqlite
    assert "varchar_column TEXT" in ddl_sqlite
    assert "varchar2_column_no_len TEXT" in ddl_sqlite
    assert "varchar2_length_column TEXT" in ddl_sqlite
    assert "clob_column TEXT" in ddl_sqlite


def test_get_id_or_key() -> None:
    """Test case for the get_id_or_key() method."""
    sb = SchemaBuilder()
    sb.add_slot("identifier_slot", identifier=True)
    sb.add_slot("key_slot", key=True)
    sb.add_class("ClassWithId", slots=["identifier_slot", "name", "whatever"])
    sb.add_class("ClassWithKey", slots=["key_slot", "key_hole", "Torquay"])
    sb.add_class("ClassWithNowt", slots=["slot_1", "slot_2"])
    sb.add_class("ClassWithItAll", slots=["identifier_slot", "key_slot", "name", "miscellany"])
    gen = SQLTableGenerator(sb.schema)
    sv = SchemaView(schema=sb.schema)

    assert gen.get_id_or_key("ClassWithId", sv) == "ClassWithId.identifier_slot"
    assert gen.get_id_or_key("ClassWithKey", sv) == "ClassWithKey.key_slot"
    assert gen.get_id_or_key("ClassWithItAll", sv) == "ClassWithItAll.identifier_slot"
    with pytest.raises(Exception, match="No PK for ClassWithNowt"):
        gen.get_id_or_key("ClassWithNowt", sv)


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
        "INSERT INTO Person (id, name, age) VALUES (?,?,?)",
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
            "INSERT INTO Person (id, name, age) VALUES (?,?,?)",
            ("P1", "other person", 22),
        )
    with pytest.raises(Exception):
        cur.execute(
            "INSERT INTO Person_alias (Person_id, alias) VALUES (?,?)",
            ("P1", "wibble"),
        )

    con.close()
