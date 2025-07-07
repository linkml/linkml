from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

import hbreader
import pytest
import yaml

from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.utils.yamlutils import DupCheckYamlLoader, TypedNode, YAMLRoot, from_yaml
from tests.test_utils.environment import env


def test_yaml_load_with_dupes() -> None:
    """Make sure the duplicate checker finds duplicates."""
    with open(env.input_path("yaml1.yaml")) as f:
        y1 = yaml.safe_load(f)
        assert y1["f1"] == 17


def test_dupcheck_loader_no_dupes() -> None:
    """Test a file without dupes with the DupCheckYamlLoader."""
    with open(env.input_path("schema1.yaml")) as f:
        s1 = yaml.load(f, DupCheckYamlLoader)
        assert s1["name"] == "schema1"


@pytest.mark.parametrize("file_name", ["yaml1.yaml", "yaml2.yaml"])
def test_dupcheck_loader_has_dupes(file_name: str) -> None:
    """Ensure that files with duplicates throw an error."""
    with open(env.input_path(file_name)) as f, pytest.raises(ValueError, match="Duplicate key:"):
        yaml.load(f, DupCheckYamlLoader)


def test_line_numbers() -> None:
    s = """
    name: schema1
    info: foo
    x:
        a: 1
        b: 2
    l: [1, 2, 3]
    """
    obj = yaml.load(s, DupCheckYamlLoader)
    cases = [
        ("name", 1),
        ("info", 2),
        ("x", 3),
        ("l", 6),
    ]
    key_to_lines = [(k, k._s.line) for k in obj]
    assert cases == key_to_lines


@pytest.mark.xfail(reason="Reporting line numbers should happen at load time not when instantiating dataclasses")
def test_issue_38() -> None:
    # The goal is to provide line numbers on error messages.   We've tweaked the parser so that it returns augmented
    # str's and int's with the line numbers on them.  The problem we are trying to address now is that the dataclass
    # constructor doesn't support **argv out of the box.  We can certainly tweak the generator to emit the __init__
    # method to do this, but it would be really handy

    @dataclass
    class FesterBesterTester(YAMLRoot):
        cv: ClassVar[int] = 42

        a: int | None = 0
        b: str | None = None

    with pytest.raises(TypeError, match="unexpected keyword argument 'c'"):
        FesterBesterTester(a=12, b="Sell", c="buy")

    yaml_str = """base:
        a: 17
        b: Ice Cream
        c: sell"""

    parsed_yaml = yaml.load(yaml_str, DupCheckYamlLoader)
    with pytest.raises(TypeError, match='File "<unicode string>", line 4, col 9'):
        FesterBesterTester(**parsed_yaml["base"])

    parsed_yaml["base"].pop("c", None)

    instance = FesterBesterTester(**parsed_yaml["base"])
    assert instance.a == 17
    assert instance.b == "Ice Cream"


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


def test_read_dangling_name() -> None:
    """Dangling name should not throw a type error.

    See https://github.com/linkml/linkml/issues/626
    """
    model_txt = """
id: http://x.org
name: test

default_range: string
types:
  string:
    base: str
    uri: xsd:string

slots:
  name:
"""
    schema = from_yaml(model_txt, SchemaDefinition)
    assert "name" in schema.slots
