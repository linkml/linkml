import pytest

from linkml.generators.jsonschemagen import JsonSchemaGenerator


@pytest.mark.jsonschemagen
def test_enums(input_path, snapshot):
    """Make sure that enums are generated as part of the output"""
    gen = JsonSchemaGenerator(input_path("issue_239.yaml"))
    gen.topCls = "c"
    output = gen.serialize()
    assert output == snapshot("issue_239.json")
