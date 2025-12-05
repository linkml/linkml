from pathlib import Path

from linkml.validator import validate_file

PERSONINFO_SCHEMA = str(Path(__file__).parent / "input/personinfo.yaml")

CSV_DATA = """id, name, telephone, age
id:1,Person A,555-1234,25
id:2,Person B,555-0101,57
id:3,Person C,,
"""


def test_valid_csv_file(tmp_file_factory):
    f = tmp_file_factory("data.csv", CSV_DATA)
    report = validate_file(f, PERSONINFO_SCHEMA, "Person")
    assert report.results == []


def test_valid_tsv_file(tmp_file_factory):
    f = tmp_file_factory("data.tsv", CSV_DATA.replace(",", "\t"))
    report = validate_file(f, PERSONINFO_SCHEMA, "Person")
    assert report.results == []


def test_valid_json_file(tmp_file_factory):
    data = """{
    "persons": [
        {
            "id": "id:1",
            "name": "Person A",
            "aliases": ["A", "a"],
            "telephone": "555-1234",
            "age": 25
        }
    ]
}
"""
    f = tmp_file_factory("data.json", data)
    report = validate_file(f, PERSONINFO_SCHEMA)
    assert report.results == []


def test_valid_yaml_file(tmp_file_factory):
    data = """
persons:
    - id: "id:1"
      name: Person A
      aliases:
        - A
          a
      telephone: 555-1234
      age: 25
    """
    f = tmp_file_factory("data.yaml", data)
    report = validate_file(f, PERSONINFO_SCHEMA)
    assert report.results == []


def test_invalid_csv_file(tmp_file_factory):
    data = """id, name, telephone, age
id:1, Person A, 555-1234, 25
id:2, Person B, ABC-0101, 57
"""
    f = tmp_file_factory("data.csv", data)
    report = validate_file(f, PERSONINFO_SCHEMA, "Person")
    assert len(report.results) == 1
    assert "ABC" in report.results[0].message


def test_invalid_tsv_file(tmp_file_factory):
    data = """id\t name\t telephone\t age
id:1\tPerson A\t555-1234\ttwenty
id:2\tPerson B\t555-0101\t57
"""
    f = tmp_file_factory("data.tsv", data)
    report = validate_file(f, PERSONINFO_SCHEMA, "Person")
    assert len(report.results) == 1
    assert "twenty" in report.results[0].message


def test_invalid_json_file(tmp_file_factory):
    data = """[
    {
        "id": "id:1",
        "name": "Person A",
        "aliases": "uh-oh",
        "telephone": "555-1234",
        "age": 25
    },
    {
        "name": "Person B",
        "aliases": ["B", "b"],
        "telephone": "555-1234",
        "age": 25
    }
]
"""
    f = tmp_file_factory("data.json", data)
    report = validate_file(f, PERSONINFO_SCHEMA, "Person")
    assert len(report.results) == 2
    assert "uh-oh" in report.results[0].message
    assert "id" in report.results[1].message


def test_invalid_yaml_file(tmp_file_factory):
    data = """
id: "id:1"
name: Person A
aliases: uh-oh
telephone: 555-1234
age: 25
---
name: Person B
aliases:
  - B
    b
telephone: 555-1234
age: 25
"""
    f = tmp_file_factory("data.yaml", data)
    report = validate_file(f, PERSONINFO_SCHEMA, "Person")
    assert len(report.results) == 2
    assert "uh-oh" in report.results[0].message
    assert "id" in report.results[1].message
