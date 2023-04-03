import unittest
from linkml_runtime import SchemaView

URL = ("https://raw.githubusercontent.com/linkml/linkml-runtime/"
       "2a46c65fe2e7db08e5e524342e5ff2ffb94bec92/tests/test_utils/input/kitchen_sink.yaml")

MIXS_URL = ("https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/"
            "83be82a99d0a210e83b371b20b3dadb6423ec612/model/schema/mixs.yaml")


class TestRemoteModularSchemaView(unittest.TestCase):
    """
    See https://github.com/linkml/linkml/issues/1317
    """

    def setUp(self) -> None:
        self.schemaview = SchemaView(URL)

    def test_view_created(self):
        """test_remote_modular_schema_view"""
        sv = self.schemaview
        sv = SchemaView(URL)
        self.assertEqual(sv.schema.name, "kitchen_sink")

    def test_imported_classes_present(self):
        """test_remote_modular_schema_view"""
        sv = SchemaView(URL)
        class_count = len(sv.all_classes())
        self.assertGreater(class_count, 0)
        self.assertIn("activity", sv.all_classes())
        self.assertIn("activity", sv.all_classes(imports=True))
        self.assertNotIn("activity", sv.all_classes(imports=False))

    @unittest.skip("Test is slow and may be fragile")
    def test_mixs(self):
        """
        Note this test case involves using an external github repo.

        We use commit hashes to avoid false positive test fails caused by repo changes,
        but in theory this test could break if the mixs repo is deleted or changes its
        name or org.

        We will likely keep skipping this for now, but once stabilized it can be unskipped

        Note that the sam functionality is likely captured in the other tests that use
        a more stable repo
        """
        sv = SchemaView(MIXS_URL)
        class_count = len(sv.all_classes())
        self.assertGreater(class_count, 0)


if __name__ == "__main__":
    unittest.main()