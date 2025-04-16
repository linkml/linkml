import pytest
from jsonasobj2 import as_json
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.yamlutils import as_rdf

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.pythongen import PythonGenerator


@pytest.mark.jsonldcontextgen
@pytest.mark.pythongen
def test_issue_80(input_path, snapshot):
    """Make sure that types are generated as part of the output"""
    output = PythonGenerator(input_path("issue_80.yaml")).serialize()
    assert output == snapshot("issue_80.py")

    module = compile_python(output)
    example = module.Person("http://example.org/person/17", "Fred Jones", 43)

    json_output = as_json(example)
    assert json_output == snapshot("issue_80.json")

    jsonld_context_output = ContextGenerator(input_path("issue_80.yaml")).serialize()
    assert jsonld_context_output == snapshot("issue_80.context.jsonld")

    rdf_output = as_rdf(example, contexts=jsonld_context_output).serialize(format="turtle")
    assert rdf_output == snapshot("issue_80.ttl")
