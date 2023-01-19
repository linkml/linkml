import pprint
import unittest

import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml.generators.linkmlgen import LinkmlGenerator

from tests.test_data.environment import env

ROOT_SCHEMA = env.input_path("issue_1239_root.yaml")
IMPORT_SCHEMA = env.input_path("issue_1239_import.yaml")


class MergerRetentionTestCase(unittest.TestCase):

    def test_create_import_view(self):
        root_view = SchemaView(IMPORT_SCHEMA)
        self.assertEqual(type(root_view), SchemaView)

        # todo why doesn't this complain about the undefined default_range "fake"

    def test_create_root_view(self):
        root_view = SchemaView(ROOT_SCHEMA, merge_imports=True)
        print(yaml_dumper.dumps(root_view.schema))
        self.assertEqual(type(root_view), SchemaView)

    def test_class_retained_in_merge(self):
        gen = LinkmlGenerator(ROOT_SCHEMA, format='yaml', mergeimports=True)
        yaml_string = gen.serialize()
        dict_from_yaml_gen = yaml.safe_load(yaml_string)
        pprint.pprint(dict_from_yaml_gen)
        self.assertIn('import_class', dict_from_yaml_gen['classes'])

    def test_def_prefix_retained_in_merge(self):
        root_view = SchemaView(ROOT_SCHEMA, merge_imports=True)
        import_slot = root_view.schema.slots['import_slot']
        import_slot_uri = import_slot.slot_uri
        self.assertEqual(import_slot_uri, 'https://example.com/import_prefix/import_slot')

    def test_def_range_retained_in_merge(self):
        root_view = SchemaView(ROOT_SCHEMA, merge_imports=True)
        import_slot = root_view.schema.slots['import_slot']
        import_slot_range = import_slot.range
        self.assertEqual(import_slot_range, 'fake')
