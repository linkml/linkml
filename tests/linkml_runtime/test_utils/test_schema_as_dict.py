import os
import unittest
import logging

from linkml_runtime.linkml_model.meta import ClassDefinition
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.utils.schema_as_dict import schema_as_yaml_dump, schema_as_dict
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.schema_builder import ClassDefinition, SchemaBuilder, SlotDefinition

from tests.test_utils import INPUT_DIR, OUTPUT_DIR

logger = logging.getLogger(__name__)

SCHEMA_NO_IMPORTS = os.path.join(INPUT_DIR, 'kitchen_sink_noimports.yaml')
SCHEMA_WITH_IMPORTS = os.path.join(INPUT_DIR, 'kitchen_sink.yaml')
CLEAN_SCHEMA = os.path.join(OUTPUT_DIR, 'kitchen_sink.clean.yaml')

yaml_loader = YAMLLoader()


class SchemaAsDictTestCase(unittest.TestCase):

    def test_as_dict(self):
        """
        tests schema_as_dict, see https://github.com/linkml/linkml/issues/100
        """
        view = SchemaView(SCHEMA_NO_IMPORTS)
        all_slots = view.all_slots()
        self.assertIn('name', all_slots)
        logger.debug(view.schema.id)
        ystr = schema_as_yaml_dump(view.schema)
        with open(CLEAN_SCHEMA, 'w') as stream:
            stream.write(ystr)
        view2 = SchemaView(ystr)
        obj = schema_as_dict(view.schema)
        # ensure that prefixes are compacted
        assert obj['prefixes']['pav'] == 'http://purl.org/pav/'
        assert '@type' not in obj
        for k in ['slots', 'classes', 'enums', 'subsets']:
            elt_dict = obj[k]
            for e_name, e in elt_dict.items():
                assert 'name' not in e
            if k == 'enums':
                for e in elt_dict.values():
                    for pv in e.get('permissible_values', {}).values():
                        assert 'text' not in pv
        self.assertIn('name', obj['slots'])


    def test_as_dict_with_attributes(self):
        """
        tests schema_as_dict, see https://github.com/linkml/linkml/issues/100
        """

        # Create a class with an attribute named 'name'
        cls = ClassDefinition(name="Patient")
        slots = [
            SlotDefinition(name="id", range="string"),
            SlotDefinition(name="name", range="string"),
        ]
        builder = SchemaBuilder()
        builder.add_class(cls=cls, slots=slots, use_attributes=True)

        # Verify that the 'name' slot exists in the schema
        view = SchemaView(builder.schema)
        self.assertIn('name', view.all_slots())

        # Convert the schema to a dict
        obj = schema_as_dict(view.schema)

        # Verify that the 'name' slot still exists, as an attribute
        self.assertIn('name', obj['classes']['Patient']['attributes'])


if __name__ == '__main__':
    unittest.main()
