import os
import unittest
from typing import Callable

from jsonasobj2 import as_json, loads, load, as_dict, JsonObj

from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml.utils.rawloader import load_raw_schema
from linkml.utils.schemaloader import SchemaLoader
from tests.test_utils.environment import env


class RawLoaderTestCase(unittest.TestCase):

    def _verify_schema1_content(self, schema: SchemaDefinition, source_file,
                                addl_checks: Callable[[SchemaDefinition], None]=None) -> None:
        expected = loads(f"""{{
           "default_prefix": "http://example.org/{source_file}/",
           "name": "{source_file}",
           "id": "http://example.org/{source_file}",
           "title": "Load Raw Schema Test",
           "metamodel_version": "0.5.0",
           "source_file": "{source_file}.yaml",
           "source_file_date": "Mon Dec 31 11:25:38 2018",
           "source_file_size": 76,
           "generation_date": "2018-12-31 11:50"
        }}""")

        schema.source_file = os.path.basename(schema.source_file)
        if addl_checks:
            addl_checks(schema)
        self.assertTrue(isinstance(schema.metamodel_version, str))
        expected.metamodel_version = schema.metamodel_version
        self.assertTrue(isinstance(schema.source_file_date, str))
        expected.source_file_date = schema.source_file_date
        self.assertTrue(isinstance(schema.source_file_size, int))
        expected.source_file_size = schema.source_file_size
        self.assertTrue(isinstance(schema.generation_date, str))
        expected.generation_date = schema.generation_date
        self.assertEqual(expected, loads(as_json(schema)))

    def test_load_raw_file(self):
        """ Test loading a data file """
        self._verify_schema1_content(load_raw_schema(env.input_path('schema1.yaml')), 'schema1')

        # Verify that we can't pass source_file parameters when we've got a directory name
        with self.assertRaises(AssertionError) as e:
            load_raw_schema(env.input_path('schema1.yaml'), source_file_size=117)
        self.assertIn("source_file_size parameter not allowed if data is a file or URL", str(e.exception))

    @unittest.skip("Disabled until we implement SchemaDefinitionList")
    def test_explicit_name(self):
        """ Test the named schema option """
        self._verify_schema1_content(load_raw_schema(env.input_path('schema2.yaml')), 'schema2')

    @unittest.skip("Disabled until we implement SchemaDefinitionList")
    def test_multi_schemas(self):
        """ Test multiple schemas in the same file """
        def check_types(s: SchemaDefinition) -> None:
            output = env.expected_path('schema4.json')
            if not os.path.exists(output):
                with open(output, 'w') as f:
                    f.write(as_json(JsonObj(**{k: as_dict(loads(as_json(v))) for k, v in s.types.items()})))

            with open(output) as f:
                expected = as_dict(load(f))
            self.assertEqual(expected, {k: as_dict(loads(as_json(v))) for k, v in s.types.items()})
            s.types = None

        self._verify_schema1_content(load_raw_schema(env.input_path('schema4.yaml')), 'schema4', check_types)

    def test_base_dir(self):
        """ Test the base directory option  """
        self._verify_schema1_content(load_raw_schema('schema1.yaml', base_dir=env.indir), 'schema1')

    def test_schema_id(self):
        """ Test loading a schema with just an id """
        self._verify_schema1_content(load_raw_schema('schema3.yaml', base_dir=env.indir), 'schema3')

    def test_name_from_sourcefile(self):
        """ Test no identifier at all  """
        with self.assertRaises(ValueError):
            load_raw_schema(env.input_path('schema5.yaml'))


    def test_load_text(self):
        """ Test loading straight text """
        with open(env.input_path('schema1.yaml')) as f:
            self._verify_schema1_content(load_raw_schema(f.read(), 'schema1.yaml', "Mon Dec 31 11:25:38 2018", 76),
                                         'schema1')

    def test_representation_errors(self):
        """ Test misformed schema elements """
        fn = env.input_path('typeerror1.yaml')
        with self.assertRaises(ValueError) as e:
            SchemaLoader(fn)
        print(str(e.exception))
        # previously, this returned a value error.  The new loader is robust enough that it no longer does
        fn = env.input_path('typeerror2.yaml')
        SchemaLoader(fn)
        # with self.assertRaises(ValueError) as e:
        #     SchemaLoader(fn)
        # print(str(e.exception))
        fn = env.input_path('typeerror3.yaml')
        SchemaLoader(fn)
        # with self.assertRaises(ValueError) as e:
        #     SchemaLoader(fn)
        # print(str(e.exception))
        fn = env.input_path('typeerror4.yaml')
        SchemaLoader(fn)
        # with self.assertRaises(ValueError) as e:
        #     SchemaLoader(fn)
        # print(str(e.exception))


if __name__ == '__main__':
    unittest.main()
