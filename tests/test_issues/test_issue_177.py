import jsonasobj
from linkml_runtime.utils.yamlutils import as_yaml

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.utils.schemaloader import SchemaLoader


def test_issue_177(input_path, snapshot):
    output = JsonSchemaGenerator(input_path("issue_177.yaml")).serialize()
    assert output == snapshot("issue_177.json")

    sobj = jsonasobj.loads(output)
    props = sobj["properties"]
    assert props["sa"]["type"] == "string"
    assert props["sb"]["type"] == "integer"


def test_issue_177_dup(input_path, snapshot):
    output = as_yaml(SchemaLoader(input_path("issue_177_error.yaml")).resolve())
    assert output == snapshot("issue_177_error.yaml")
