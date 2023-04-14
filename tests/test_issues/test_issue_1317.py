import unittest
from linkml_runtime import SchemaView

mixs_root_url = "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/model/schema/mixs.yaml"


@unittest.skip("potentially fragile test: mixs schema changing may break this")
class TestRemoteModularSchemaView(unittest.TestCase):
    """
    Tests imports from a URL.

    """
    def test_view_created(self):
        """test_remote_modular_schema_view"""
        sv = SchemaView(mixs_root_url)
        self.assertEqual(sv.schema.name, "MIxS")

    def test_imported_classes_present(self):
        """test_remote_modular_schema_view"""
        sv = SchemaView(mixs_root_url)
        class_count = len(sv.all_classes())
        self.assertGreater(class_count, 0)
        # seems to be confused about where to find the import
        # E           FileNotFoundError: [Errno 2] No such file or directory: '/home/mark/gitrepos/linkml/tests/test_issues/agriculture.yaml'


if __name__ == "__main__":
    unittest.main()
