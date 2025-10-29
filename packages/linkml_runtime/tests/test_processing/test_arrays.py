from pathlib import Path

import pytest
import yaml

from linkml_runtime.processing.referencevalidator import (
    ReferenceValidator,
)
from linkml_runtime.utils.schemaview import SchemaView
from tests.test_processing import INPUT_DIR


@pytest.fixture
def normalizer():
    """ReferenceValidator instance for array example schema."""
    sv = SchemaView(str(Path(INPUT_DIR) / "array_example.yaml"))
    return ReferenceValidator(sv)


@pytest.fixture
def matrix_data():
    """Load matrix data from array example data file."""
    return yaml.safe_load(open(str(Path(INPUT_DIR) / "array_example_data.yaml")))


def test_array_normalization(normalizer, matrix_data):
    """
    Test that we can infer the collection form of a slot.

    Tests array normalization functionality.
    See: https://linkml.io/linkml/howtos/multidimensional-arrays
    """
    matrix = normalizer.normalize(matrix_data)
    vals = [int(x) for x in matrix["temperatures"]]
    assert vals == [11, 12, 13, 21, 22, 23, 31, 32, 33]
