import unittest
import json

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from tests.test_issues.environment import env


class RequiredPropertyTestCase(unittest.TestCase):
    def test_required_property_json_schema(self):
        """Check that the xsd:dateTime format is per ISO 8601 standards."""

        json_schema_str = JsonSchemaGenerator(
            env.input_path("issue_433_fixed.yaml"),
            top_class="PhysicalSampleRecord",
        ).serialize()

        json_schema_dict = json.loads(json_schema_str)

        # check if the required key is part of the dictionary
        self.assertIn("required", json_schema_dict)

        # valdiate the values that show up in the required property
        assert sorted(json_schema_dict["required"]) == [
            "id",
            "label",
            "sampleidentifier",
        ]


if __name__ == "__main__":
    unittest.main()
