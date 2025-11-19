import pytest
import yaml
from jsonasobj2 import as_json
from linkml_runtime.utils.yamlutils import DupCheckYamlLoader, as_yaml

from linkml.utils.rawloader import load_raw_schema


def test_dupcheck_loader(input_path):
    """Make sure the duplicate checker finds duplicates"""
    with open(input_path("yaml1.yaml")) as f:
        y1 = yaml.safe_load(f)
        assert 17 == y1["f1"]
    with open(input_path("yaml1.yaml")) as f:
        with pytest.raises(ValueError):
            yaml.load(f, DupCheckYamlLoader)
    with open(input_path("yaml2.yaml")) as f:
        with pytest.raises(ValueError):
            yaml.load(f, DupCheckYamlLoader)
    with open(input_path("schema1.yaml")) as f:
        s1 = yaml.load(f, DupCheckYamlLoader)
        assert "schema1" == s1["name"]


def test_as_json(input_path, snapshot):
    schema = load_raw_schema(input_path("schema6.yaml"), emit_metadata=False)
    assert as_json(schema) == snapshot("schema6.json")


@pytest.mark.skip(reason="MULTI-Schema test -- re-enable if necessary")
def test_as_yaml(input_path, snapshot):
    """Test the YAML output representation"""
    schema = load_raw_schema(input_path("schema4.yaml"), emit_metadata=False)
    assert as_yaml(schema) == snapshot("schema4.yaml")
