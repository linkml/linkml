import pytest

from linkml.generators.pythongen import PythonGenerator


def test_good_ifabsent(input_path, snapshot):
    """Test ifabsent with no default_prefix"""
    output = PythonGenerator(input_path("ifabsents.yaml")).serialize()
    assert output == snapshot("ifabsents.py")


def test_good_ifabsent2(input_path, snapshot):
    """Test isabsents with default_prefix specified"""
    output = PythonGenerator(input_path("ifabsents2.yaml")).serialize()
    assert output == snapshot("ifabsents2.py")


def test_good_ifabsent3(input_path, snapshot):
    """Test isabsent with no default_prefix, but prefix specified that matches the module id"""
    output = PythonGenerator(input_path("ifabsents3.yaml")).serialize()
    assert output == snapshot("ifabsents3.py")


def test_bad_ifabsent(input_path):
    with pytest.raises(ValueError):
        PythonGenerator(input_path("ifabsents_error.yaml")).serialize()


def test_ifabsent_uri(input_path, snapshot):
    output = PythonGenerator(input_path("ifabsent_uri.yaml")).serialize()
    assert output == snapshot("ifabsent_uri.py")
