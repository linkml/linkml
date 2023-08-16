import unittest
from linkml_runtime.linkml_model.meta import Element, LINKML

class PolyDataclassTestCase(unittest.TestCase):
    def test_class_for_uri(self):
        """ Test various class lookup options """
        e = Element

        # Test class URI
        cls = e._class_for_uri(LINKML.ClassDefinition)
        self.assertEqual('ClassDefinition', cls.__name__)

        # Test model URI
        cls = e._class_for_uri(LINKML.TypeDefinition, use_model_uri=True)
        self.assertEqual('TypeDefinition', cls.__name__)

        # Test class curie (note there isn't any model curie
        cls = e._class_for_curie("linkml:TypeDefinition")
        self.assertEqual('TypeDefinition', cls.__name__)

        # Make sure the self test works
        cls = e._class_for_uri(LINKML.Element)
        self.assertEqual('Element', cls.__name__)

        # Make sure we fail gracefully
        cls = e._class_for_uri("linkml:Missing")
        self.assertIsNone(cls)


if __name__ == '__main__':
    unittest.main()
