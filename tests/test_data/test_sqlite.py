import os
import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView, SchemaDefinition
from sqlalchemy.orm import sessionmaker

from linkml.utils.schema_builder import SchemaBuilder
from linkml.utils.sqlutils import SQLStore

from tests.test_data.model.personinfo import Container, Person
import tests.test_data.model.personinfo
from tests.test_data.environment import env
from tests.utils.dict_comparator import compare_yaml, compare_objs

SCHEMA = env.input_path('personinfo.yaml')
METAMODEL_SCHEMA = env.input_path(os.path.join('meta', 'meta.yaml'))
DATA = env.input_path('personinfo_data01.yaml')
DATA_RECAP = env.expected_path('personinfo_data01.recap.yaml')
DB = env.expected_path('personinfo.db')
TMP_DB = env.expected_path('tmp.db')
METAMODEL_DB = env.expected_path('meta.db')


class SQLiteStoreTest(unittest.TestCase):
    """
    Tests :class:`SQLStore`

    - :meth:`SQLStore.dump`
    - :meth:`SQLStore.load`
    """

    def test_sqlite_store(self):
        """
        tests a complete end-to-end example with a dump-load cycle
        """
        # step 1: setup
        sv = SchemaView(SCHEMA)
        #TODO: currently it is necessary to pass the actual yaml rather than a schema object
        #endpoint = SQLiteEndpoint(sv.schema, database_path=DB, include_schema_in_database=False)
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
        # step 4: test loading from SQLStore
        # 4a: first test load_all, diff to original data should be empty
        x = endpoint.load_all(target_class=Container)
        y = yaml_dumper.dumps(x[0])
        with open(DATA_RECAP, 'w') as stream:
            stream.write(y)
        diff = compare_yaml(DATA, DATA_RECAP)
        self.assertEqual(diff, "")
        # 4b: next test load implicit object, diff to original data should be empty
        container_loaded = endpoint.load()
        yaml_dumper.dump(container_loaded, to_file=DATA_RECAP)
        y = yaml_dumper.dumps(container_loaded)
        diff = compare_yaml(DATA, DATA_RECAP)
        self.assertEqual(diff, "")

    @unittest.skip("TODO")
    def test_metamodel_sqlite(self):
        # step 1: setup
        sv = package_schemaview("linkml_runtime.linkml_model.meta")
        #sv = SchemaView(METAMODEL_SCHEMA)
        endpoint = SQLStore(sv.schema, database_path=METAMODEL_DB, include_schema_in_database=False)
        endpoint.native_module = tests.test_data.model.personinfo
        endpoint.db_exists(force=True)
        endpoint.compile()
        # step 2: load data from file and store in SQLStore
        container: SchemaDefinition = yaml_loader.load(SCHEMA, target_class=SchemaDefinition)
        endpoint.dump(container)


    def test_mixin(self):
        b = SchemaBuilder()
        b.add_defaults()
        b.add_slot(SlotDefinition("ref_to_c1", range="my_class1", multivalued=True))
        b.add_class("my_mixin", slots=['my_mixin_slot'], mixin=True)
        b.add_class("my_abstract", slots=['my_abstract_slot'], abstract=True)
        b.add_class("my_class1", is_a="my_abstract", mixins=["my_mixin"])
        b.add_class("my_class2", slots=["ref_to_c1"])
        #print(yaml_dumper.dumps(b.schema))
        endpoint = SQLStore(b.schema, database_path=TMP_DB)
        endpoint.db_exists(force=True)
        mod = endpoint.compile_native()
        i1 = mod.MyClass1(my_mixin_slot="v1", my_abstract_slot="v2")
        i2 = mod.MyClass2(ref_to_c1=i1)
        endpoint.dump(i2)
        i2_recap = endpoint.load(target_class=mod.MyClass2)
        #print(yaml_dumper.dumps(i2_recap))
        diff = compare_objs(i2, i2_recap)
        self.assertEqual(diff, "")


if __name__ == '__main__':
    unittest.main()
