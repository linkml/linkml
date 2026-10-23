from pathlib import Path

import pytest

from linkml.validator import validate_file

PERSONINFO_SCHEMA = str(Path(__file__).parent / "input/personinfo.yaml")

# Shared relative-import fixture tree (also exercised by the SchemaView tests'
# ``test_imports_relative``). ``main.yaml`` pulls in sibling, nested-subdirectory, parent and
# cross-tree schemas via relative imports, so validating against a class defined in one of those
# imports proves the validator resolves them relative to the schema's own directory.
RELATIVE_IMPORT_MAIN = (
    Path(__file__).parents[2] / "linkml_runtime/test_utils/input/imports_relative/L0_0/L1_0_0/main.yaml"
)

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


def test_validate_file_resolves_schema_relative_imports_from_schema_dir(tmp_path, monkeypatch):
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()

    base_schema = schema_dir / "base.yaml"
    base_schema.write_text(
        """id: https://example.org/base
name: base
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
classes:
  Thing:
    attributes:
      id:
        identifier: true
""",
        encoding="utf-8",
    )

    main_schema = schema_dir / "main.yaml"
    main_schema.write_text(
        """id: https://example.org/main
name: main
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
  - ./base
""",
        encoding="utf-8",
    )

    data_path = tmp_path / "data.yaml"
    data_path.write_text("id: x\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    report = validate_file(str(data_path), str(main_schema), target_class="Thing")

    assert report.results == []


@pytest.mark.parametrize(
    "target_class",
    [
        "Main",  # class in the entry schema itself
        "Child1",  # class from a nested-subdirectory import (``./L2_0_0_0/child``)
        "StepChild",  # class from a nested import declared without ``./`` (``L2_0_0_2/stepchild``)
        "Neighborhood_Parent",  # class reached transitively via ``../parent`` -> ``../neighborhood_parent``
    ],
)
def test_validate_file_resolves_nested_and_sibling_relative_imports(tmp_path, monkeypatch, target_class):
    """The validator resolves sibling, nested-subdirectory and parent relative imports against the
    schema's own directory, not the current working directory.

    Reuses the shared ``imports_relative`` fixture tree so this end-to-end validator coverage stays
    in sync with the SchemaView-level ``test_imports_relative``.
    """
    data_path = tmp_path / "data.yaml"
    data_path.write_text("value: hello\n", encoding="utf-8")

    # chdir somewhere unrelated to the schema so resolution can only succeed relative to the schema.
    monkeypatch.chdir(tmp_path)

    report = validate_file(str(data_path), str(RELATIVE_IMPORT_MAIN), target_class=target_class)

    assert report.results == []
