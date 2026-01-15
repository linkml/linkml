import pytest

from linkml.validator.loaders import CsvLoader, TsvLoader


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
