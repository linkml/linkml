import pytest
from linkml_runtime.utils.yamlutils import as_yaml

from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.utils.schemaloader import SchemaLoader


def test_issue_167(input_path, snapshot):
    """Test extensions to the four basic types"""
    output = as_yaml(SchemaLoader(input_path("issue_167.yaml")).resolve())
    assert output == snapshot("issue_167.yaml")


def test_issue_167b_yaml(input_path, snapshot):
    """Annotations yaml example"""
    output = as_yaml(SchemaLoader(input_path("issue_167b.yaml")).resolve())
    assert output == snapshot("issue_167b.yaml")


@pytest.mark.pythongen
def test_issue_167b_python(input_path, snapshot):
    """Annotations python example"""
    output = PythonGenerator(
        input_path("issue_167b.yaml"),
        emit_metadata=False,
    ).serialize()
    assert output == snapshot("issue_167b.py")

    output = PythonGenerator(
        input_path("issue_167b.yaml"),
        mergeimports=False,
        emit_metadata=False,
    ).serialize()
    assert output == snapshot("issue_167b2.py")


@pytest.mark.jsonldgen
@pytest.mark.skip("skipped during refactor: https://github.com/linkml/linkml/pull/924")
def test_issue_167b_json(input_path, snapshot):
    output = JSONLDGenerator(
        input_path("issue_167b.yaml"),
    ).serialize()
    assert output == snapshot("issue_167b.json")


@pytest.mark.rdfgen
@pytest.mark.skip("Stopped working during refactor -- to hard to debug")
def test_issue_167b_rdf(input_path, snapshot):
    output = RDFGenerator(input_path("issue_167b.yaml")).serialize()
    assert output == snapshot("issue_167b.ttl")
