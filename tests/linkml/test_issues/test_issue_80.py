import pytest
from jsonasobj2 import as_json

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.yamlutils import as_rdf


@pytest.mark.jsonldcontextgen
@pytest.mark.pythongen
def test_issue_80(input_path, snapshot, bundled_snapshot_text):
    """Make sure that types are generated as part of the output"""
    outputs: dict[str, str] = {}

    output = PythonGenerator(input_path("issue_80.yaml")).serialize()
    outputs["issue_80.py"] = output

    module = compile_python(output)
    example = module.Person("http://example.org/person/17", "Fred Jones", 43)

    json_output = as_json(example)
    outputs["issue_80.json"] = json_output

    jsonld_context_output = ContextGenerator(input_path("issue_80.yaml")).serialize()
    outputs["issue_80.context.jsonld"] = jsonld_context_output

    rdf_output = as_rdf(example, contexts=jsonld_context_output).serialize(format="turtle")
    outputs["issue_80.ttl"] = rdf_output

    assert bundled_snapshot_text(outputs) == snapshot("issue_80.txt")
