import pytest

from linkml.utils.schemaloader import SchemaLoader

# Issue #206 - SchemaLoader needs to do a yaml_loader.load early on


@pytest.mark.xfail
def test_class_list(input_path):
    """SchemaLoader should be monotonic - metamodel test"""
    SchemaLoader(input_path("issue_206.yaml")).resolve()
