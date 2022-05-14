import logging
import os
import unittest
from io import StringIO
from typing import Optional

import jsonasobj
from jsonasobj2 import as_json, load

from linkml.utils.schemaloader import SchemaLoader
from tests.test_utils.environment import env
from tests.utils.filters import json_metadata_filter
from tests.utils.test_environment import TestEnvironmentTestCase


class SchemaLoaderTestCase(TestEnvironmentTestCase):
    env = env

    def eval_loader(self, base_name: str, logger: Optional[logging.Logger] = None, source: Optional[str] = None) -> None:
        loader = SchemaLoader(source or self.env.input_path(base_name + '.yaml'), logger=logger)
        self.env.generate_single_file(base_name + '.json', lambda: as_json(loader.resolve()),
                                      filtr=json_metadata_filter, value_is_returned=True)
        self.env.generate_single_file(base_name + '.errs', lambda: '\n'.join(loader.synopsis.errors()),
                                      filtr=json_metadata_filter, value_is_returned=True)

    @unittest.skip("Disabled until we get SchemaDefinitionList implemented")
    def test_basic_merge(self):
        """ Test the basic merge paths """
        logstream = StringIO()
        logging.basicConfig()
        logger = logging.getLogger(self.__class__.__name__)
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.addHandler(logging.StreamHandler(logstream))
        logger.setLevel(logging.INFO)
        self.eval_loader('merge1', logger=logger)
        self.assertIn("Overlapping subset and slot names: s1, s2", logstream.getvalue().strip())

    @unittest.skip("Disabled until we get SchemaDefinitionList implemented")
    def test_mergeerror1(self):
        """ Test conflicting definitions path """
        fn = env.input_path('mergeerror1.yaml')
        with self.assertRaises(ValueError) as ve:
            SchemaLoader(fn)
        self.assertEqual("Conflicting URIs (http://example.org/schema2, http://example.org/schema1) for item: c1",
                         str(ve.exception))

    def test_imports(self):
        self.eval_loader('base')

    @unittest.skip("Re-enable this once we get fully migrated")
    def test_error_paths(self):
        """ Test various loader error situations"""

        fn = env.input_path('loadererror1.yaml')
        with self.assertRaises(ValueError, msg="Unknown slot domain should fail") as e:
            SchemaLoader(fn).resolve()
        self.assertIn('loadererror1.yaml", line 11, col 13', str(e.exception))

        fn = env.input_path('loadererror2.yaml')
        with self.assertRaises(ValueError, msg="No Type URI") as e:
            SchemaLoader(fn).resolve()
        self.assertIn('type "string" does not declare a URI', str(e.exception))

        fn = env.input_path('loadererror2a.yaml')
        with self.assertRaises(ValueError, msg="Optional key slot should fail") as e:
            SchemaLoader(fn).resolve()
        self.assertIn('slot: s1 - key and identifier slots cannot be optional', str(e.exception))

        fn = env.input_path('loadertest1.yaml')
        schema = SchemaLoader(fn).resolve()
        self.assertEqual('string', schema.slots['s1'].range)

        fn = env.input_path('loadererror4.yaml')
        with self.assertRaises(ValueError, msg="Default prefix is not defined") as e:
            SchemaLoader(fn).resolve()
        self.assertIn('loadererror4.yaml", line 6, col 17', str(e.exception))

    @unittest.skip("Re-enable this once we get fully migrated")
    def test_empty_range(self):
        """ A type must have either a base or a parent """
        fn = env.input_path('loadererror5.yaml')
        with self.assertRaises(ValueError, msg="Range error should be raised") as e:
            _ = SchemaLoader(fn).resolve()
        self.assertIn('loadererror5.yaml", line 9, col 3', str(e.exception))

    def test_multi_key(self):
        """ Multiple keys are not supported """
        fn = env.input_path('loadererror6.yaml')
        with self.assertRaises(ValueError, msg='Multiple keys/identifiers not allowed') as e:
            _ = SchemaLoader(fn).resolve()
        self.assertIn('multiple keys/identifiers not allowed', str(e.exception))

        fn = env.input_path('loadererror7.yaml')
        with self.assertRaises(ValueError, msg="Two or more keys are not allowed") as e:
            _ = SchemaLoader(fn).resolve()
        self.assertIn('multiple keys/identifiers not allowed', str(e.exception))

    def test_key_and_id(self):
        """ A slot cannot be both a key and an identifier """
        fn = env.input_path('loadererror8.yaml')
        with self.assertRaises(ValueError, msg="A slot cannot be both a key and identifier") as e:
            _ = SchemaLoader(fn).resolve()
        self.assertIn('A slot cannot be both a key and identifier at the same time', str(e.exception))

        fn = env.input_path('loadererror9.yaml')
        with self.assertRaises(ValueError, msg="A slot cannot be both a key and identifier") as e:
            _ = SchemaLoader(fn).resolve()
        self.assertIn('A slot cannot be both a key and identifier at the same time', str(e.exception))

    @unittest.skip("Re-enable this once we get fully migrated")
    def test_missing_type_uri(self):
        """ A type with neither a typeof or uri is an error """
        fn = env.input_path('loadererror10.yaml')
        with self.assertRaises(ValueError, msg="A non-typeof type has to have a URI") as e:
            _ = SchemaLoader(fn).resolve()
        self.assertIn('loadererror10.yaml", line 12, col 3', str(e.exception))
        fn = env.input_path('loaderpass11.yaml')
        _ = SchemaLoader(fn).resolve()

    @unittest.skip("Re-enable this once we get fully migrated")
    def test_undefined_subset(self):
        """ Throw an error on an undefined subset reference """
        fn = env.input_path('loadererror11.yaml')
        with self.assertRaises(ValueError, msg="Subset references must be valid") as e:
            _ = SchemaLoader(fn).resolve()
        self.assertIn('loadererror11.yaml", line 22, col 16', str(e.exception))

    def test_importmap(self):
        """ Test the importmap parameter """
        fn = env.input_path('import_test_1.yaml')
        importmap = {"http://example.org/import_test_2" : "import_test_2",
                      "loc/imp3": "import_test_3",
                      "base:import_test_4": "http://example.org/import_test_4",
                      "http://example.org/import_test_4": "import_test_4",
                      "types": "http://w3id.org/linkml/types"}
        self.env.generate_single_file('import_test_1.json',
                                      lambda: as_json(SchemaLoader(fn, importmap=importmap).resolve()),
                                      filtr=json_metadata_filter)


if __name__ == '__main__':
    unittest.main()
