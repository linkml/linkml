import unittest
from pathlib import Path

from linkml.validator import validate_file
from tests.test_validator import data_file

PERSONINFO_SCHEMA = str(Path(__file__).parent / "input/personinfo.yaml")

CSV_DATA = """id, full_name, phone, age
id:1,Person A,555-1234,25
id:2,Person B,555-0101,57
id:3,Person C,,
"""


class TestValidate(unittest.TestCase):
    def test_valid_csv_file(self):
        with data_file(CSV_DATA, suffix=".csv") as f:
            report = validate_file(f, PERSONINFO_SCHEMA, "Person")
            self.assertEqual(report.results, [])

    def test_valid_tsv_file(self):
        with data_file(CSV_DATA.replace(",", "\t"), suffix=".tsv") as f:
            report = validate_file(f, PERSONINFO_SCHEMA, "Person")
            self.assertEqual(len(report.results), 0)

    def test_valid_json_file(self):
        data = """{
    "persons": [
        {
            "id": "id:1",
            "full_name": "Person A",
            "aliases": ["A", "a"],
            "phone": "555-1234",
            "age": 25
        }
    ]
}
"""
        with data_file(data, suffix=".json") as f:
            report = validate_file(f, PERSONINFO_SCHEMA)
            self.assertEqual(len(report.results), 0)

    def test_invalid_csv_file(self):
        data = """id, full_name, phone, age
id:1, Person A, 555-1234, 25
id:2, Person B, ABC-0101, 57
"""
        with data_file(data, suffix=".csv") as f:
            report = validate_file(f, PERSONINFO_SCHEMA, "Person")
            self.assertEqual(len(report.results), 1)
            self.assertIn("ABC", report.results[0].message)

    def test_invalid_tsv_file(self):
        data = """id\t full_name\t phone\t age
id:1\tPerson A\t555-1234\ttwenty
id:2\tPerson B\t555-0101\t57
"""
        with data_file(data, suffix=".tsv") as f:
            report = validate_file(f, PERSONINFO_SCHEMA, "Person")
            self.assertEqual(len(report.results), 1)
            self.assertIn("twenty", report.results[0].message)

    def test_invalid_json_file(self):
        data = """[
    {
        "id": "id:1",
        "full_name": "Person A",
        "aliases": "uh-oh",
        "phone": "555-1234",
        "age": 25
    },
    {
        "full_name": "Person B",
        "aliases": ["B", "b"],
        "phone": "555-1234",
        "age": 25
    }
]
"""
        with data_file(data, suffix=".json") as f:
            report = validate_file(f, PERSONINFO_SCHEMA, "Person")
            self.assertEqual(len(report.results), 2)
            self.assertIn("uh-oh", report.results[0].message)
            self.assertIn("id", report.results[1].message)
