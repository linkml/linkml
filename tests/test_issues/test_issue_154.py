import yaml
from linkml_runtime.utils.yamlutils import as_yaml

from linkml.generators.pythongen import PythonGenerator


def test_roundtrip(input_path):
    """Test as_yaml emitter"""

    # We use the PythonGenerator as a generic generator instance.  We don't actually serialize
    yaml_fname = input_path("issue_134.yaml")
    gen = PythonGenerator(yaml_fname)
    yaml_str = as_yaml(gen.schema)
    generated = yaml.safe_load(yaml_str)
    with open(yaml_fname) as yaml_file:
        original = yaml.safe_load(yaml_file)

    # The generated YAML contains many added fields. Some with default values. Therefore, we can't directly
    # compare it to the original.
    for key in original:
        assert len(original[key]) == len(generated[key])
        if isinstance(original[key], dict):
            for subkey in original[key]:
                assert subkey in generated[key]
