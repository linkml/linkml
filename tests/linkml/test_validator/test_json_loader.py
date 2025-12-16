import json

import pytest

from linkml.validator.loaders import JsonLoader


def test_load_object(tmp_file_factory):
    test_data = {
        "hello": "world",
        "number": 1,
        "boolean": True,
        "array": ["of", "strings"],
    }
    json_file = tmp_file_factory("data.json", json.dumps(test_data))

    loader = JsonLoader(json_file)
    instances = loader.iter_instances()
    assert next(instances) == test_data
    with pytest.raises(StopIteration):
        next(instances)


def test_load_list_of_objects(tmp_file_factory):
    test_data = [{"id": 1}, {"id": 2}]
    json_file = tmp_file_factory("data.json", json.dumps(test_data))

    loader = JsonLoader(json_file)
    instances = loader.iter_instances()
    assert next(instances) == test_data[0]
    assert next(instances) == test_data[1]
    with pytest.raises(StopIteration):
        next(instances)
