import pytest
import yaml

from linkml.validator.loaders import CsvLoader, TsvLoader

SCHEMA_WITH_ENUM = {
    "id": "https://example.org/test",
    "name": "test",
    "prefixes": {"linkml": "https://w3id.org/linkml/"},
    "imports": ["linkml:types"],
    "default_range": "string",
    "classes": {
        "Record": {
            "attributes": {
                "id": {"range": "integer", "identifier": True},
                "zipcode": {"range": "string"},
                "score": {"range": "score_enum"},
                "weight": {"range": "float"},
            }
        }
    },
    "enums": {
        "score_enum": {
            "permissible_values": {
                "1": {"description": "Low"},
                "2": {"description": "Medium"},
                "3": {"description": "High"},
            }
        }
    },
}


@pytest.fixture()
def schema_path(tmp_path):
    """Write the test schema to a YAML file and return its path."""
    path = tmp_path / "schema.yaml"
    path.write_text(yaml.dump(SCHEMA_WITH_ENUM))
    return str(path)


@pytest.mark.parametrize("delimiter,loader_cls", [(",", CsvLoader), ("\t", TsvLoader)])
def test_load(delimiter, loader_cls, tmp_file_factory):
    data = "\n".join(
        (
            delimiter.join(("one", "two", "three", "four")),
            delimiter.join(("1", "2.0001", "three", "4.4.4")),
        )
    )
    f = tmp_file_factory("data", data)
    loader = loader_cls(f)
    instances = loader.iter_instances()
    assert next(instances) == {"one": 1, "two": 2.0001, "three": "three", "four": "4.4.4"}
    with pytest.raises(StopIteration):
        next(instances)


def test_load_empty_rows(tmp_file_factory):
    data = """one, two, three
a, b, c
,,
d, e, f
"""
    csv_file = tmp_file_factory("data", data)
    loader = CsvLoader(csv_file)
    instances = loader.iter_instances()
    assert next(instances) == {"one": "a", "two": "b", "three": "c"}
    assert next(instances) == {}
    assert next(instances) == {"one": "d", "two": "e", "three": "f"}
    with pytest.raises(StopIteration):
        next(instances)

    loader = CsvLoader(csv_file, skip_empty_rows=True)
    instances = loader.iter_instances()
    assert next(instances) == {"one": "a", "two": "b", "three": "c"}
    assert next(instances) == {"one": "d", "two": "e", "three": "f"}
    with pytest.raises(StopIteration):
        next(instances)


def test_load_index_slot(tmp_file_factory):
    data = """one, two, three
a, b, c
d, e, f
"""
    csv_file = tmp_file_factory("data", data)
    loader = CsvLoader(csv_file, index_slot_name="some_things")
    instances = loader.iter_instances()
    assert next(instances) == {
        "some_things": [
            {"one": "a", "two": "b", "three": "c"},
            {"one": "d", "two": "e", "three": "f"},
        ]
    }
    with pytest.raises(StopIteration):
        next(instances)


def test_empty_column(tmp_file_factory):
    data = """one, two, three
a, , c
d, e, f
"""
    csv_file = tmp_file_factory("data", data)
    loader = CsvLoader(csv_file)
    instances = loader.iter_instances()
    assert next(instances) == {"one": "a", "three": "c"}
    assert next(instances) == {"one": "d", "two": "e", "three": "f"}
    with pytest.raises(StopIteration):
        next(instances)


@pytest.mark.parametrize("delimiter,loader_cls", [(",", CsvLoader), ("\t", TsvLoader)])
def test_schema_aware_preserves_string_and_enum_columns(delimiter, loader_cls, tmp_file_factory, schema_path):
    """String-ranged and enum-ranged columns stay as strings; others are still coerced."""
    data = "\n".join(
        (
            delimiter.join(("id", "zipcode", "score", "weight")),
            delimiter.join(("1", "90210", "2", "3.5")),
        )
    )
    f = tmp_file_factory("data", data)
    loader = loader_cls(f, schema_path=schema_path, target_class="Record")
    row = next(loader.iter_instances())
    assert row == {"id": 1, "zipcode": "90210", "score": "2", "weight": 3.5}
    # Verify types explicitly
    assert isinstance(row["id"], int)
    assert isinstance(row["zipcode"], str)
    assert isinstance(row["score"], str)
    assert isinstance(row["weight"], float)


@pytest.mark.parametrize("delimiter,loader_cls", [(",", CsvLoader), ("\t", TsvLoader)])
def test_without_schema_numeric_strings_are_coerced(delimiter, loader_cls, tmp_file_factory):
    """Without schema info, numeric-looking strings are still coerced (backward compat)."""
    data = "\n".join(
        (
            delimiter.join(("id", "zipcode", "score")),
            delimiter.join(("1", "90210", "2")),
        )
    )
    f = tmp_file_factory("data", data)
    loader = loader_cls(f)
    row = next(loader.iter_instances())
    assert row == {"id": 1, "zipcode": 90210, "score": 2}
    assert isinstance(row["zipcode"], int)


@pytest.mark.parametrize("delimiter,loader_cls", [(",", CsvLoader), ("\t", TsvLoader)])
def test_schema_aware_non_numeric_strings_unchanged(delimiter, loader_cls, tmp_file_factory, schema_path):
    """Non-numeric values in string/enum columns are unaffected by the schema-aware path."""
    data = "\n".join(
        (
            delimiter.join(("id", "zipcode", "score", "weight")),
            delimiter.join(("1", "abc", "3", "2.0")),
        )
    )
    f = tmp_file_factory("data", data)
    loader = loader_cls(f, schema_path=schema_path, target_class="Record")
    row = next(loader.iter_instances())
    assert row == {"id": 1, "zipcode": "abc", "score": "3", "weight": 2.0}
