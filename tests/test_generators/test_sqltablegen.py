import os
import re
import sqlite3
import tempfile
import unittest
from enum import Enum
from typing import List

from linkml_runtime.linkml_model.meta import SlotDefinition
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView
from sqlalchemy.sql.sqltypes import Enum, Text

from linkml.generators.sqltablegen import SqlNamingPolicy, SQLTableGenerator
from linkml.transformers.relmodel_transformer import ForeignKeyPolicy
from linkml.utils.schema_builder import SchemaBuilder
from tests.test_generators.environment import env

SCHEMA = env.input_path("personinfo.yaml")
OUT_PATH = env.expected_path("personinfo.relational.yaml")
RSCHEMA_EXPANDED = env.expected_path("personinfo.relational.expanded.yaml")
OUT_DDL = env.expected_path("personinfo.ddl.sql")
META_OUT_DDL = env.expected_path("meta.ddl.sql")
SQLDDLLOG = env.expected_path("personinfo.sql.log")
DB = env.expected_path("personinfo.db")
DUMMY_CLASS = "dummy class"


class SQLTableGeneratorTestCase(unittest.TestCase):
    """
    Tests the (new) SQLTableGenerator
    """

    def test_inject_primary_key(self):
        """
        test a minimal schema with no primary names declared
        """
        b = SchemaBuilder()
        slots = ["full name", "description"]
        b.add_class(DUMMY_CLASS, slots)
        b.add_defaults()
        gen = SQLTableGenerator(b.schema)
        ddl = gen.generate_ddl()
        # print(ddl)
        assert "PRIMARY KEY (id)" in ddl
        assert "full_name TEXT" in ddl
        assert 'CREATE TABLE "dummy class"' in ddl

    def test_no_injection(self):
        """
        test a minimal schema with no primary names declared
        """
        b = SchemaBuilder()
        slots = ["full name", "description"]
        b.add_class(DUMMY_CLASS, slots)
        b.add_defaults()
        gen = SQLTableGenerator(b.schema, use_foreign_keys=False)
        ddl = gen.generate_ddl()
        # print(ddl)
        assert "PRIMARY KEY (id)" not in ddl
        assert "full_name TEXT" in ddl
        assert 'CREATE TABLE "dummy class"' in ddl

        # now test with full schema
        gen = SQLTableGenerator(SCHEMA, use_foreign_keys=False)
        ddl = gen.generate_ddl()
        assert "FOREIGN KEY" not in ddl

    def test_dialect(self):
        """
        test dialect options
        """
        b = SchemaBuilder()
        slots = ["full name", "description", "age"]
        b.add_class(DUMMY_CLASS, slots, description="My dummy class")
        b.add_slot(
            SlotDefinition("age", range="integer", description="age of person in years")
        )
        b.add_defaults()
        for dialect in ["postgresql", "sqlite", "mysql"]:
            gen = SQLTableGenerator(b.schema, dialect=dialect)
            ddl = gen.generate_ddl()
            print(f"DIALECT: {dialect}\n SQL:\n{ddl}")
            if dialect == "postgresql":
                assert "id SERIAL" in ddl
                assert "COMMENT ON TABLE" in ddl
                assert "COMMENT ON COLUMN" in ddl
            if dialect == "sqlite":
                assert "id INTEGER" in ddl
                # sqlite does not support comments
            if dialect == "mysql":
                assert "id INTEGER AUTO_INCREMENT" in ddl
                assert "COMMENT" in ddl

    def test_generate_ddl(self):
        """Generate contents of DDL file as a string."""
        gen = SQLTableGenerator(SCHEMA)

        ddl = gen.generate_ddl()

        new_file, filename = tempfile.mkstemp()
        temp_ddl_filepath = filename + ".sql.ddl"

        with open(temp_ddl_filepath, "w") as stream:
            stream.write(ddl)

        py_file_list = []
        with open(temp_ddl_filepath) as file:
            lines = file.readlines()
            py_file_list = [line.rstrip() for line in lines]

        tbl_list = []
        for item in py_file_list:
            res = re.search(r"\"(.*?)\"", item)
            if res:
                tbl_list.append(res.group(1))

        self.assertTrue(
            all(
                x in tbl_list
                for x in [
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
            ),
            f"Expected classes from {SCHEMA} not written to {temp_ddl_filepath}",
        )

    def test_get_sql_range(self):
        """Test case for the get_sql_range() method."""
        gen = SQLTableGenerator(SCHEMA)

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

        # Slot range in list of schema classes
        actual_1_output = gen.get_sql_range(case_1_slot)

        # Slot range in list of schema enums
        actual_2_output = gen.get_sql_range(case_2_slot)

        # Slot not present in schema
        actual_3_output = gen.get_sql_range(case_3_slot)

        self.assertIsInstance(actual_1_output, Text)
        self.assertIsInstance(actual_2_output, Enum)
        self.assertIsInstance(actual_3_output, Text)

    def test_get_foreign_key(self):
        """Test case for the get_foreign_key() method."""
        gen = SQLTableGenerator(SCHEMA)

        sv = SchemaView(schema=SCHEMA)

        fk_value = gen.get_foreign_key("Person", sv)

        self.assertEqual(fk_value, "Person.id")

    def test_sqlddl_on_metamodel(self):
        sv = package_schemaview("linkml_runtime.linkml_model.meta")
        gen = SQLTableGenerator(sv.schema)
        ddl = gen.generate_ddl()
        with open(META_OUT_DDL, "w") as stream:
            stream.write(ddl)
        assert "CREATE TABLE class_definition (" in ddl
        assert "CREATE TABLE annotation (" in ddl

    def test_sqlddl_basic(self):
        """
        End to end example
        """
        # sv = SchemaView(SCHEMA)
        # sqltr = RelationalModelTransformer(sv)
        gen = SQLTableGenerator(SCHEMA)
        # ddl = gen.generate_ddl(naming_policy=SqlNamingPolicy.underscore)
        ddl = gen.generate_ddl()
        with open(OUT_DDL, "w") as stream:
            stream.write(ddl)

        with open(SQLDDLLOG, "w") as log:
            # with open(DDL_PATH, 'w') as stream:
            #     stream.write(ddl)
            # print(ddl)
            try:
                os.remove(DB)
            except OSError:
                pass
            con = sqlite3.connect(DB)
            cur = con.cursor()
            cur.executescript(ddl)
            NAME = "fred"
            cur.execute(
                "INSERT INTO Person (id, name, age_in_years) VALUES (?,?,?)",
                ("P1", NAME, 33),
            )
            cur.execute(
                "INSERT INTO Person_alias (Person_id, alias) VALUES (?,?)",
                ("P1", "wibble"),
            )
            cur.execute(
                "INSERT INTO FamilialRelationship (Person_id, type, related_to) VALUES (?,?,?)",
                ("P1", "P2", "BROTHER_OF"),
            )
            cur.execute("select * from Person where name=:name", {"name": NAME})
            rows = cur.fetchall()
            log.write(f"{rows}\n")
            assert len(rows) == 1
            con.commit()
            with self.assertRaises(Exception):
                # PK violation
                cur.execute(
                    "INSERT INTO Person (id, name, age_in_years) VALUES (?,?,?)",
                    ("P1", "other person", 22),
                )
            with self.assertRaises(Exception):
                cur.execute(
                    "INSERT INTO Person_alias (Person_id, alias) VALUES (?,?)",
                    ("P1", "wibble"),
                )

            con.close()


if __name__ == "__main__":
    unittest.main()
