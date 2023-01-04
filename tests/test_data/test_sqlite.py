import csv
import os
import unittest

import _csv
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.loaders import csv_loader, yaml_loader
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaDefinition, SchemaView
from sqlalchemy.orm import sessionmaker

import tests.test_data.model.personinfo
from linkml.utils.schema_builder import SchemaBuilder
from linkml.utils.schema_fixer import SchemaFixer
from linkml.utils.sqlutils import SQLStore
from tests.test_data.environment import env
from tests.test_data.model.personinfo import (Container, FamilialRelationship,
                                              GenderType, Person)
from tests.utils.dict_comparator import compare_objs, compare_yaml

SCHEMA = env.input_path("personinfo.yaml")
METAMODEL_SCHEMA = env.input_path(os.path.join("meta", "meta.yaml"))
DATA = env.input_path("personinfo_data01.yaml")
DATA_RECAP = env.expected_path("personinfo_data01.recap.yaml")
DB = env.expected_path("personinfo.db")
TMP_DB = env.expected_path("tmp.db")
TMP_TSV = env.expected_path("tmp.tsv")
METAMODEL_DB = env.expected_path("meta.db")


class SQLiteStoreTest(unittest.TestCase):
    """
    Tests :class:`SQLStore`

    - :meth:`SQLStore.dump`
    - :meth:`SQLStore.load`
    """

    def test_enums(self):
        """
        Tests that enum objects can be constructed inlined.

        See https://github.com/linkml/linkml/issues/817
        """
        r = FamilialRelationship(type="SIBLING_OF", related_to="x")
        p = Person(id="x", gender=GenderType(GenderType.cisgender_man))
        self.assertEqual(type(p.gender), GenderType)
        c = Container(persons=[p])

    def test_sqlite_store(self):
        """
        tests a complete end-to-end example with a dump-load cycle
        """
        # step 1: setup
        sv = SchemaView(SCHEMA)
        # TODO: currently it is necessary to pass the actual yaml rather than a schema object
        # endpoint = SQLiteEndpoint(sv.schema, database_path=DB, include_schema_in_database=False)
        endpoint = SQLStore(SCHEMA, database_path=DB, include_schema_in_database=False)
        endpoint.native_module = tests.test_data.model.personinfo
        endpoint.db_exists(force=True)
        endpoint.compile()
        # step 2: load data from file and store in SQLStore
        container: Container = yaml_loader.load(DATA, target_class=Container)
        endpoint.dump(container)
        # step 3: test query using SQL Alchemy
        session_class = sessionmaker(bind=endpoint.engine)
        session = session_class()
        q = session.query(endpoint.module.Person)
        all_objs = q.all()
        self.assertEqual(2, len(all_objs))
        for p in all_objs:
            print(p)
            for rel in p.has_familial_relationships:
                print(rel)
                print(rel.type)
        q = session.query(endpoint.module.FamilialRelationship)
        for r in q.all():
            print(r)
        session.close()
        # step 4: test loading from SQLStore
        # 4a: first test load_all, diff to original data should be empty
        x = endpoint.load_all(target_class=Container)
        y = yaml_dumper.dumps(x[0])
        with open(DATA_RECAP, "w") as stream:
            stream.write(y)
        diff = compare_yaml(DATA, DATA_RECAP)
        self.assertEqual(diff, "")
        # 4b: next test load implicit object, diff to original data should be empty
        container_loaded = endpoint.load()
        endpoint.engine.dispose()
        yaml_dumper.dump(container_loaded, to_file=DATA_RECAP)
        y = yaml_dumper.dumps(container_loaded)
        diff = compare_yaml(DATA, DATA_RECAP)
        self.assertEqual(diff, "")

    @unittest.skip("TODO")
    def test_metamodel_sqlite(self):
        # step 1: setup
        sv = package_schemaview("linkml_runtime.linkml_model.meta")
        # sv = SchemaView(METAMODEL_SCHEMA)
        endpoint = SQLStore(
            sv.schema, database_path=METAMODEL_DB, include_schema_in_database=False
        )
        endpoint.native_module = tests.test_data.model.personinfo
        endpoint.db_exists(force=True)
        endpoint.compile()
        # step 2: load data from file and store in SQLStore
        container: SchemaDefinition = yaml_loader.load(
            SCHEMA, target_class=SchemaDefinition
        )
        schema_instance = SchemaDefinition(id="test", name="test")
        endpoint.dump(schema_instance)

    def test_mixin(self):
        b = SchemaBuilder()
        b.add_defaults()
        b.add_slot(SlotDefinition("ref_to_c1", range="my_class1", multivalued=True))
        b.add_class("my_mixin", slots=["my_mixin_slot"], mixin=True)
        b.add_class("my_abstract", slots=["my_abstract_slot"], abstract=True)
        b.add_class("my_class1", is_a="my_abstract", mixins=["my_mixin"])
        b.add_class("my_class2", slots=["ref_to_c1"])
        # print(yaml_dumper.dumps(b.schema))
        endpoint = SQLStore(b.schema, database_path=TMP_DB)
        endpoint.db_exists(force=True)
        mod = endpoint.compile_native()
        i1 = mod.MyClass1(my_mixin_slot="v1", my_abstract_slot="v2")
        i2 = mod.MyClass2(ref_to_c1=i1)
        endpoint.dump(i2)
        i2_recap = endpoint.load(target_class=mod.MyClass2)
        # print(yaml_dumper.dumps(i2_recap))
        diff = compare_objs(i2, i2_recap)
        self.assertEqual(diff, "")

    def test_csv_limit(self):
        """
        Tests https://github.com/linkml/linkml/issues/815
        """
        b = SchemaBuilder()
        b.add_class("Person", ["name"]).add_defaults()
        schema = b.schema
        sf = SchemaFixer()
        sf.add_container(schema)
        for size in [20, 200000]:
            csv.field_size_limit(size)
            for diff in [1, -1]:
                name = "N" * (size + diff)
                endpoint = SQLStore(schema, database_path=TMP_DB)
                endpoint.db_exists(force=True)
                mod = endpoint.compile_native()
                with open(TMP_TSV, "w", encoding="UTF-8") as file:
                    file.write("name\n")
                    file.write(name)
                    file.write("\n")
                if diff == -1:
                    obj = csv_loader.load(
                        TMP_TSV,
                        target_class=mod.Container,
                        index_slot="Person_index",
                        schema=schema,
                    )
                    endpoint.dump(obj)
                    obj2 = endpoint.load(target_class=mod.Container)
                    person = getattr(obj2, "Person_index")[0]
                    name2 = getattr(person, "name")
                    self.assertEqual(name, name2)
                else:
                    with self.assertRaises(Exception):
                        csv_loader.load(
                            TMP_TSV,
                            target_class=mod.Container,
                            index_slot="Person_index",
                            schema=schema,
                        )
                # mod holds a reference to sqlite that prevents file closing
                del mod
                # dispose engine to allow creating of a new engine of same name
                endpoint.engine.dispose()


if __name__ == "__main__":
    unittest.main()
