import json
import tempfile
import unittest

from linkml.validator.loaders import JsonLoader


class TestJsonLoader(unittest.TestCase):
    def test_load_object(self):
        with tempfile.NamedTemporaryFile(mode="w+") as json_file:
            test_data = {
                "hello": "world",
                "number": 1,
                "boolean": True,
                "array": ["of", "strings"],
            }
            json.dump(test_data, json_file)
            json_file.seek(0)

            loader = JsonLoader(json_file)
            instances = loader.iter_instances()
            self.assertEqual(next(instances), test_data)
            self.assertRaises(StopIteration, lambda: next(instances))

    def test_load_list_of_objects(self):
        with tempfile.NamedTemporaryFile(mode="w+") as json_file:
            test_data = [{"id": 1}, {"id": 2}]
            json.dump(test_data, json_file)
            json_file.seek(0)

            loader = JsonLoader(json_file)
            instances = loader.iter_instances()
            self.assertEqual(next(instances), test_data[0])
            self.assertEqual(next(instances), test_data[1])
            self.assertRaises(StopIteration, lambda: next(instances))
