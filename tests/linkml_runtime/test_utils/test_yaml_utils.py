from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Optional, Union

import hbreader
import pytest
import yaml
from jsonasobj2 import JsonObj

from linkml_runtime.linkml_model import Annotation, SchemaDefinition
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


def test_safe_dumper_handles_jsonobj_with_annotation_value() -> None:
    """Regression test for JsonObj representer registration in yamlutils.

    Reproduces a crash path where a JsonObj containing Annotation values under
    slot annotations raised yaml.representer.RepresenterError.
    """
    fail_value = JsonObj(metadata_scheme=Annotation(tag="metadata_scheme", value=True))
    slot_payload = {"issuer": {"range": "string", "annotations": fail_value}}

    dumped = yaml.dump(slot_payload, Dumper=yaml.SafeDumper, sort_keys=False)

    assert "issuer:" in dumped
    assert "annotations:" in dumped
    assert "metadata_scheme:" in dumped
    assert "tag: metadata_scheme" in dumped
    assert "value: true" in dumped


# ---------------------------------------------------------------------------
# _normalize_inlined with inherited classes (issue #3244)
#
# Classes below generated by ``PythonGenerator(SCHEMA, mergeimports=True)``
# (URI-metadata ClassVars stripped; they do not affect _normalize_inlined)
# from this schema:
#
# id: https://example.org/test_issue_3244
# name: test_issue_3244
# imports:
#   - linkml:types
# prefixes:
#   linkml: https://w3id.org/linkml/
#   ex: https://example.org/test_issue_3244/
# default_prefix: ex
# default_range: string
# classes:
#   ParentClass:
#     attributes:
#       title:
#         range: string
#   ChildClass:
#     is_a: ParentClass
#     attributes:
#       notation:
#         identifier: true
#         range: string
#   ContainerList:
#     tree_root: true
#     attributes:
#       items:
#         range: ChildClass
#         multivalued: true
#         inlined_as_list: true
#   ContainerDict:
#     attributes:
#       items:
#         range: ChildClass
#         multivalued: true
#         inlined: true
#
# ChildClass inherits from ParentClass, so its __init__ signature is
# (title, notation) — the identifier ``notation`` is LAST. This exposes
# bugs where _normalize_inlined used positional args to instantiate the
# slot type.
# ---------------------------------------------------------------------------


class ChildClassNotation(extended_str):
    pass


@dataclass(repr=False)
class _ParentClass(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    title: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class _ChildClass(_ParentClass):
    _inherited_slots: ClassVar[list[str]] = []

    notation: Union[str, ChildClassNotation] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.notation):
            self.MissingRequiredField("notation")
        if not isinstance(self.notation, ChildClassNotation):
            self.notation = ChildClassNotation(self.notation)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class _ContainerList(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    items: Optional[
        Union[dict[Union[str, ChildClassNotation], Union[dict, _ChildClass]], list[Union[dict, _ChildClass]]]
    ] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="items", slot_type=_ChildClass, key_name="notation", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class _ContainerDict(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    items: Optional[
        Union[dict[Union[str, ChildClassNotation], Union[dict, _ChildClass]], list[Union[dict, _ChildClass]]]
    ] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
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


def test_normalize_inlined_duplicate_keys():
    """Duplicate key detection must still work after the kwargs fix."""
    with pytest.raises(ValueError, match="duplicate key"):
        _ContainerList(items=[{"notation": "n1"}, {"notation": "n1"}])


# ---------------------------------------------------------------------------
# _normalize_inlined with multivalued key_name field (keyed=False)
#
# Classes below generated by ``PythonGenerator(SCHEMA, mergeimports=True)``
# (URI-metadata ClassVars stripped; they do not affect _normalize_inlined)
# from this schema:
#
# id: https://example.org/test_list_key
# name: test_list_key
# imports:
#   - linkml:types
# prefixes:
#   linkml: https://w3id.org/linkml/
#   ex: https://example.org/test_list_key/
# default_prefix: ex
# default_range: string
# classes:
#   BaseEntity:
#     attributes:
#       title:
#         range: string
#   TaggedEntity:
#     is_a: BaseEntity
#     attributes:
#       tags:
#         range: string
#         required: true
#         multivalued: true
#   TaggedEntityContainer:
#     tree_root: true
#     attributes:
#       items:
#         range: TaggedEntity
#         multivalued: true
#         inlined_as_list: true
#
# No identifier -> keyed=False; the key_name field (tags) is multivalued,
# so its value is a list. _normalize_inlined must pass list values through.
# ---------------------------------------------------------------------------


@dataclass(repr=False)
class _BaseEntity(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    title: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class _TaggedEntity(_BaseEntity):
    _inherited_slots: ClassVar[list[str]] = []

    tags: Union[str, list[str]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.tags):
            self.MissingRequiredField("tags")
        if not isinstance(self.tags, list):
            self.tags = [self.tags] if self.tags is not None else []
        self.tags = [v if isinstance(v, str) else str(v) for v in self.tags]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class _TaggedEntityContainer(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    items: Optional[Union[Union[dict, _TaggedEntity], list[Union[dict, _TaggedEntity]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="items", slot_type=_TaggedEntity, key_name="tags", keyed=False)

        super().__post_init__(**kwargs)


def test_normalize_inlined_key_name_with_list_value():
    """[{key_name: [values]}] — multivalued field value must pass through."""
    c = _TaggedEntityContainer(items=[{"tags": ["t1"]}])
    assert c.items == [_TaggedEntity(tags=["t1"])]


def test_normalize_inlined_list_of_lists_with_inheritance():
    """List-of-lists: first element must map to key, not first MRO field."""
    c = _ContainerList(items=[["n1", "t1"]])
    assert c.items == [_ChildClass(notation="n1", title="t1")]


# ---------------------------------------------------------------------------
# _normalize_inlined with values containing commas (issue #3367)
#
# Classes below model the reproducer from the issue:
#
# id: https://example.org/comma-bug
# name: comma_bug
# imports:
#   - linkml:types
# prefixes:
#   linkml: https://w3id.org/linkml/
#   ex: https://example.org/
# default_prefix: ex
# default_range: string
# classes:
#   CommaContainer:
#     tree_root: true
#     attributes:
#       items:
#         range: CommaItem
#         multivalued: true
#         inlined_as_list: true
#   CommaItem:
#     attributes:
#       item_id:
#         identifier: true
#         range: string
#       synonyms:
#         range: CommaSynonym
#         multivalued: true
#         inlined_as_list: true
#   CommaSynonym:
#     attributes:
#       synonym_text:
#         required: true
#       synonym_type:
#         range: string
#
# CommaSynonym has no identifier — synonym_text is just required.
# Values like "48,XXYY syndrome" must not be split or rejected.
# ---------------------------------------------------------------------------


class _CommaItemId(extended_str):
    pass


@dataclass(repr=False)
class _CommaSynonym(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    synonym_text: str = None
    synonym_type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.synonym_text):
            self.MissingRequiredField("synonym_text")
        if not isinstance(self.synonym_text, str):
            self.synonym_text = str(self.synonym_text)

        if self.synonym_type is not None and not isinstance(self.synonym_type, str):
            self.synonym_type = str(self.synonym_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class _CommaItem(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    item_id: Union[str, _CommaItemId] = None
    synonyms: Optional[Union[Union[dict, _CommaSynonym], list[Union[dict, _CommaSynonym]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.item_id):
            self.MissingRequiredField("item_id")
        if not isinstance(self.item_id, _CommaItemId):
            self.item_id = _CommaItemId(self.item_id)

        self._normalize_inlined_as_list(
            slot_name="synonyms", slot_type=_CommaSynonym, key_name="synonym_text", keyed=False
        )

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class _CommaContainer(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    items: Optional[Union[dict[Union[str, _CommaItemId], Union[dict, _CommaItem]], list[Union[dict, _CommaItem]]]] = (
        empty_dict()
    )

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="items", slot_type=_CommaItem, key_name="item_id", keyed=True)

        super().__post_init__(**kwargs)


@pytest.mark.parametrize(
    "synonym_text",
    [
        "48,XXYY syndrome",
        "a,b,c",
        ",leading comma",
        "trailing comma,",
        "1,000",
        "Smith, John",
    ],
)
def test_normalize_inlined_comma_in_value(synonym_text: str):
    """Values containing commas must survive _normalize_inlined (issue #3367)."""
    c = _CommaContainer(
        items=[{"item_id": "ex:001", "synonyms": [{"synonym_text": synonym_text}]}],
    )
    assert len(c.items) == 1
    assert len(c.items[0].synonyms) == 1
    assert c.items[0].synonyms[0].synonym_text == synonym_text


def test_normalize_inlined_comma_in_value_from_yaml():
    """Values with commas must round-trip through YAML loading (issue #3367)."""
    yaml_str = """
items:
- item_id: ex:001
  synonyms:
  - synonym_text: '48,XXYY syndrome'
  - synonym_text: simple synonym
"""
    result = from_yaml(yaml_str, _CommaContainer)
    assert len(result.items) == 1
    synonyms = result.items[0].synonyms
    assert len(synonyms) == 2
    assert synonyms[0].synonym_text == "48,XXYY syndrome"
    assert synonyms[1].synonym_text == "simple synonym"


def test_normalize_inlined_comma_in_identifier():
    """Commas in identifier values must also be handled (issue #3367)."""
    c = _CommaContainer(
        items=[{"item_id": "48,XXYY", "synonyms": [{"synonym_text": "syn1"}]}],
    )
    assert len(c.items) == 1
    assert str(c.items[0].item_id) == "48,XXYY"
