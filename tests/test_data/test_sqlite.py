import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from sqlalchemy.orm import sessionmaker

from linkml.utils.sqlutils import SQLStore

from tests.test_data.model.personinfo import Container, Person
import tests.test_data.model.personinfo
from tests.test_data.environment import env
from tests.utils.dict_comparator import compare_yaml

SCHEMA = env.input_path('personinfo.yaml')
DATA = env.input_path('personinfo_data01.yaml')
DATA_RECAP = env.expected_path('personinfo_data01.recap.yaml')
DB = env.expected_path('personinfo.db')


class SQLiteStoreTest(unittest.TestCase):
    def test_sqlite_store(self):
        sv = SchemaView(SCHEMA)
        #TODO: avoid mangled names
        #endpoint = SQLiteEndpoint(sv.schema, database_path=DB, include_schema_in_database=False)
        endpoint = SQLStore(SCHEMA, database_path=DB, include_schema_in_database=False)
        endpoint.native_module = tests.test_data.model.personinfo
        endpoint.db_exists(force=True)
        endpoint.compile()
        container: Container = yaml_loader.load(DATA, target_class=Container)
        endpoint.dump(container)
        session_class = sessionmaker(bind=endpoint.engine)
        session = session_class()
        q = session.query(endpoint.module.Person)
        all_objs = q.all()
        x = endpoint.load_all(target_class=Container)
        y = yaml_dumper.dumps(x[0])
        container_loaded = endpoint.load()
        yaml_dumper.dump(container_loaded, to_file=DATA_RECAP)
        y = yaml_dumper.dumps(container_loaded)
        diff = compare_yaml(DATA, DATA_RECAP)
        self.assertEqual(diff, "")




if __name__ == '__main__':
    unittest.main()
