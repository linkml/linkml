import pytest
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.yamlutils import YAMLRoot, as_yaml

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.pythongen
def test_contained_constructor(input_path, snapshot):
    """Make sure that types are generated as part of the output"""
    test_name = "issue_355"

    output = PythonGenerator(input_path(f"{test_name}.yaml")).serialize()
    assert output == snapshot(f"{test_name}.py")

    module = compile_python(output)
    c = module.Container(module.Containee("11111", "Glaubner's disease"))
    assert (
        as_yaml(c)
        == """entry:
  '11111':
    id: '11111'
    value: Glaubner's disease
"""
    )

    c = module.Container({"22222": dict(id="22222", value="Phrenooscopy")})
    assert (
        as_yaml(c)
        == """entry:
  '22222':
    id: '22222'
    value: Phrenooscopy
"""
    )
    alt_object = YAMLRoot()
    alt_object.id = "33333"
    alt_object.value = "test"
    c = module.Container(alt_object)
    assert (
        as_yaml(c)
        == """entry:
  '33333':
    id: '33333'
    value: test
"""
    )

    c = module.Container([dict(id="44444", value="Gracken's curse")])
    assert (
        as_yaml(c)
        == """entry:
  '44444':
    id: '44444'
    value: Gracken's curse
"""
    )
