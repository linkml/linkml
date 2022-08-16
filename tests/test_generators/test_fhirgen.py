"""Tests for: fhirgen: FHIR-related generators"""
import unittest

from linkml.generators.fhirgen import FhirValueSetGenerator
from tests.test_generators.environment import env


INPUT_SCHEMA_PATH = env.input_path("dynamic-enums-example.yaml")
# todo: Write to file and utilize this:
OUTPUT_JSON_DIR = env.expected_path("dynamic_enums_example_json")
# OUTPUT_XML_DIR = env.expected_path("dynamic_enums_example_xml")  # todo: minor. JSON is *much* more popular in FHIR.


# todo: repurpose
def assert_json_contains(
    filename,
    text,
    # outdir=JSON_DIR,
    invert=False,
) -> None:
    """Assert JSON contains something"""
    pass


# todo: do I want this?
# def assert_json_does_not_contain(*args, **kwargs) -> None:
#     assert_json_contains(*args, **kwargs, invert=True)


class FhirValueSetGeneratorTestCase(unittest.TestCase):

    def test_fhir_valueset_gen(self):
        """Tests basic document generator functionality"""
        gen = FhirValueSetGenerator(INPUT_SCHEMA_PATH)
        json = gen.serialize(outdir=OUTPUT_JSON_DIR)
        print()
        # assert_json_contains("Organization.md", "Organization")
        # assert_json_does_not_contain("index.md", "Markdown headers")


if __name__ == "__main__":
    unittest.main()
