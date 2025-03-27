import unittest

from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.utils.introspection import package_schemaview, object_class_definition


class IntrospectionTestCase(unittest.TestCase):

    def test_introspection_on_metamodel(self):
        view = package_schemaview('linkml_runtime.linkml_model.meta')
        for cn in ['class_definition', 'type_definition', 'slot_definition']:
            assert cn in view.all_classes()
        for tn in ['uriorcurie', 'string', 'float']:
            assert tn in view.all_types()
        obj = SchemaDefinition(id='x', name='x')
        c = object_class_definition(obj)
        assert 'classes' in c.slots



if __name__ == '__main__':
    unittest.main()
