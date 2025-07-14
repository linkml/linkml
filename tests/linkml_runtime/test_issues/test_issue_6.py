import hbreader
import pytest
import yaml

from linkml_runtime.utils.yamlutils import DupCheckYamlLoader, TypedNode

inp_yaml = """
foo:
    x: 17
    y: I yam that I yam
    z: 12.43
"""


def test_loc_function() -> None:
    """Test the TypedNode.yaml_loc function."""
    inp = yaml.load(hbreader.hbread(inp_yaml), DupCheckYamlLoader)
    assert TypedNode.yaml_loc(inp["foo"]["x"]) == 'File "<unicode string>", line 3, col 8: '
    assert TypedNode.yaml_loc(inp["foo"]["x"], suffix="") == 'File "<unicode string>", line 3, col 8'
    assert TypedNode.yaml_loc(inp["foo"]["y"]) == 'File "<unicode string>", line 4, col 8: '
    assert (
        TypedNode.yaml_loc(inp["foo"]["y"], suffix=inp["foo"]["y"])
        == 'File "<unicode string>", line 4, col 8I yam that I yam'
    )
    assert TypedNode.yaml_loc(inp["foo"]["z"]) == 'File "<unicode string>", line 5, col 8: '


def test_yaml_loc_warning() -> None:
    """Test that a warning is emitted when using the `loc` method."""
    inp = yaml.load(hbreader.hbread(inp_yaml), DupCheckYamlLoader)
    with pytest.warns(DeprecationWarning) as warning_list:
        assert TypedNode.loc(inp["foo"]["x"]) == 'File "<unicode string>", line 3, col 8'
    assert len(warning_list) == 1
    assert str(warning_list[0].message) == "Call to deprecated method loc. (Use yaml_loc instead)"


@pytest.mark.parametrize("loc", [None, "abc", ["a", "b"]])
def test_yaml_loc_empty_str(loc) -> None:
    """Test yaml_loc values that translate to an empty string."""
    assert TypedNode.yaml_loc(loc) == ""
