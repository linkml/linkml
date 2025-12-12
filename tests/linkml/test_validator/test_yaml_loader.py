import pytest

from linkml.validator.loaders import YamlLoader


def test_single_document_object(tmp_file_factory):
    yaml_path = tmp_file_factory(
        "data.yaml",
        """
a: 1
b: two
""",
    )

    loader = YamlLoader(yaml_path)
    instances = loader.iter_instances()
    assert next(instances) == {"a": 1, "b": "two"}
    with pytest.raises(StopIteration):
        next(instances)


def test_single_document_array(tmp_file_factory):
    yaml_path = tmp_file_factory(
        "data.yaml",
        """
- a: 1
  b: two
- a: 3
  b: four
""",
    )

    loader = YamlLoader(yaml_path)
    instances = loader.iter_instances()
    assert next(instances) == {"a": 1, "b": "two"}
    assert next(instances) == {"a": 3, "b": "four"}
    with pytest.raises(StopIteration):
        next(instances)


def test_multiple_documents(tmp_file_factory):
    yaml_path = tmp_file_factory(
        "data.yaml",
        """
a: 1
b: two
---
- a: 3
  b: four
- a: 5
  b: six
""",
    )

    loader = YamlLoader(yaml_path)
    instances = loader.iter_instances()
    assert next(instances) == {"a": 1, "b": "two"}
    assert next(instances) == {"a": 3, "b": "four"}
    assert next(instances) == {"a": 5, "b": "six"}
    with pytest.raises(StopIteration):
        next(instances)
