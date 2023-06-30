import unittest
from copy import deepcopy

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition, SlotDefinitionName
from linkml_runtime.utils.schema_as_dict import schema_as_dict, schema_as_yaml_dump

from linkml.utils.schema_builder import SchemaBuilder
from linkml.utils.schema_fixer import SchemaFixer
from tests.test_issues.environment import env

MY_CLASS = "MyClass"
MY_CLASS2 = "MyClass2"
MY_ENUM = "MyEnum"
ID = "id"
FULL_NAME = "full_name"
DESC = "description"
LIVING = "Living"
DEAD = "Dead"

NMDC_SCHEMA = env.input_path("nmdc_submission_schema.yaml")
NMDC_SCHEMA_OUT = env.expected_path("nmdc_submission_schema.fixed.yaml")


class SchemaIssue954(unittest.TestCase):
    """
    Tests https://github.com/linkml/linkml/issues/954
    """

    def test_nmdc_submission_schema(self):
        view = SchemaView(NMDC_SCHEMA)
        s = view.schema
        fixer = SchemaFixer()
        fixer.remove_redundant_slot_usage(s)
        self.assertGreater(len(fixer.history), 100)
        with open(NMDC_SCHEMA_OUT, "w", encoding="UTF-8") as file:
            file.write(schema_as_yaml_dump(s))
        jgi = s.classes["soil_jgi_mg"].slot_usage
        jgi_ecosystem = jgi["ecosystem"]
        self.assertIn("slot_group", jgi_ecosystem)
        self.assertIn("required", jgi_ecosystem)
        self.assertIn("range", jgi_ecosystem)
        self.assertNotIn("description", jgi_ecosystem)
        self.assertNotIn("name", jgi_ecosystem)
        self.assertNotIn("owner", jgi_ecosystem)


if __name__ == "__main__":
    unittest.main()
