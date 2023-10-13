import unittest
from pathlib import Path

import yaml

from linkml.validator import validate

PERSONINFO_SCHEMA = str(Path(__file__).parent / "input/personinfo.yaml")


class TestValidate(unittest.TestCase):
    def test_valid_instance_against_schema_file(self):
        instance = {
            "persons": [
                {"id": "1", "full_name": "Person A"},
                {"id": "2", "full_name": "Person B"},
            ]
        }
        report = validate(instance, PERSONINFO_SCHEMA)
        self.assertEqual(len(report.results), 0)

    def test_valid_instance_against_schema_instance(self):
        with open(PERSONINFO_SCHEMA) as schema_file:
            schema = yaml.safe_load(schema_file)
        instance = {
            "persons": [
                {"id": "1", "full_name": "Person A"},
                {"id": "2", "full_name": "Person B"},
            ]
        }
        report = validate(instance, schema)
        self.assertEqual(len(report.results), 0)

    def test_invalid_instance(self):
        instance = {
            "persons": [
                {"full_name": "Person A"},
                {"full_name": "Person B"},
            ]
        }
        report = validate(instance, PERSONINFO_SCHEMA)
        self.assertEqual(len(report.results), 2)
        self.assertIn("'id' is a required property", report.results[0].message)
        self.assertIn("'id' is a required property", report.results[1].message)

    def test_valid_instance_specified_class(self):
        instance = {"id": "1", "full_name": "Person A"}
        report = validate(instance, PERSONINFO_SCHEMA, "Person")
        self.assertEqual(len(report.results), 0)

    def test_invalid_instance_specified_class(self):
        instance = {"full_name": "Person A"}
        report = validate(instance, PERSONINFO_SCHEMA, "Person")
        self.assertEqual(len(report.results), 1)
        self.assertIn("'id' is a required property", report.results[0].message)

    def test_invalid_instance_strict(self):
        instance = {
            "persons": [
                {"full_name": "Person A"},
                {"full_name": "Person B"},
            ]
        }
        report = validate(instance, PERSONINFO_SCHEMA, strict=True)
        self.assertEqual(len(report.results), 1)
        self.assertIn("'id' is a required property", report.results[0].message)

    def test_not_a_valid_schema(self):
        instance = {}
        schema = {"foo": "bar"}
        self.assertRaisesRegex(ValueError, "Invalid schema", lambda: validate(instance, schema))
