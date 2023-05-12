import unittest
from pathlib import Path

import yaml

from linkml_runtime.utils.schemaview import SchemaView

from linkml_runtime.processing.referencevalidator import (
    ReferenceValidator,
)
from tests.test_processing import INPUT_DIR


class ArrayTestCase(unittest.TestCase):
    """
    Tests array normalization

    See: https://linkml.io/linkml/howtos/multidimensional-arrays
    """


    def setUp(self) -> None:
        sv = SchemaView(str(Path(INPUT_DIR) / "array_example.yaml"))
        self.normalizer = ReferenceValidator(sv)
        self.matrix = yaml.safe_load(open(str(Path(INPUT_DIR) / "array_example_data.yaml")))


    def test_array_normalization(self):
        """Test that we can infer the collection form of a slot."""
        norm = self.normalizer
        matrix = norm.normalize(self.matrix)
        vals = [int(x) for x in matrix["temperatures"]]
        self.assertEqual([11, 12, 13, 21, 22, 23, 31, 32, 33], vals)
