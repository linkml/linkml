from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Optional, Union

import hbreader
import pytest
import yaml

from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.utils.metamodelcore import empty_dict, empty_list
from linkml_runtime.utils.yamlutils import DupCheckYamlLoader, TypedNode, YAMLRoot, extended_str, from_yaml
from tests.linkml_runtime.test_utils.environment import env


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


# ---------------------------------------------------------------------------
# _normalize_inlined with inherited classes (issue #3244)
#
# ChildClass inherits from ParentClass, so its __init__ signature is
# (title, description, notation) — the identifier ``notation`` is LAST.
# This exposes bugs where _normalize_inlined used positional args to
# instantiate the slot type.
# ---------------------------------------------------------------------------


class _ChildClassNotation(extended_str):
    pass


@dataclass
class _ParentClass(YAMLRoot):
    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)
        super().__post_init__(**kwargs)


@dataclass
class _ChildClass(_ParentClass):
    notation: Union[str, _ChildClassNotation] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.notation is None:
            raise ValueError("notation must be supplied")
        if not isinstance(self.notation, _ChildClassNotation):
            self.notation = _ChildClassNotation(self.notation)
        super().__post_init__(**kwargs)


@dataclass
class _ContainerList(YAMLRoot):
    items: Optional[Union[dict, list]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="items", slot_type=_ChildClass, key_name="notation", keyed=True)
        super().__post_init__(**kwargs)


@dataclass
class _ContainerDict(YAMLRoot):
    items: Optional[Union[dict, list]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="items", slot_type=_ChildClass, key_name="notation", keyed=True)
        super().__post_init__(**kwargs)


def test_normalize_inlined_single_key_dict_matching_key_name():
    """[{key_name: value}] must set the identifier, not the first field."""
    c = _ContainerList(items=[{"notation": "n1"}])
    assert c.items == [_ChildClass(notation="n1")]


def test_normalize_inlined_simple_dict_in_list():
    """[{key_val: other_val}] — SimpleDict shorthand in list form."""
    c = _ContainerList(items=[{"n1": "t1"}])
    assert c.items == [_ChildClass(notation="n1", title="t1")]


def test_normalize_inlined_simple_dict_in_dict():
    """{key_val: scalar} — SimpleDict shorthand in dict form."""
    c = _ContainerDict(items={"n1": "t1", "n2": "t2"})
    assert c.items == {
        "n1": _ChildClass(notation="n1", title="t1"),
        "n2": _ChildClass(notation="n2", title="t2"),
    }


def test_normalize_inlined_duplicate_keys_with_inherited_identifier():
    """Duplicate key detection must still work after the kwargs fix."""
    with pytest.raises(ValueError, match="duplicate key"):
        _ContainerList(items=[{"notation": "n1"}, {"notation": "n1"}])
