import json
from typing import Any

from jsonasobj2 import JsonObj, as_json

from linkml_runtime.utils.formatutils import (
    be,
    camelcase,
    is_empty,
    lcamelcase,
    remove_empty_items,
    split_line,
    uncamelcase,
    underscore,
    wrapped_annotation,
)

empty_things = [None, dict(), list(), JsonObj(), JsonObj({}), JsonObj([])]
non_empty_things = [0, False, "", {"k": None}, {0: 0}, [None], JsonObj(k=None), JsonObj(**{"k": None}), JsonObj([None])]

things_removed: list[tuple[Any, Any]] = [
    (None, None),
    (dict(), {}),
    (list(), []),
    (JsonObj(), {}),
    (JsonObj({}), {}),
    (JsonObj([]), []),
    (0, 0),
    (False, False),
    ("", ""),
    ({"k": None}, {}),
    ({0: 0}, {0: 0}),
    ([None], []),
    (JsonObj(k=None), {}),
    (JsonObj(**{"k": None}), {}),
    (JsonObj([None]), []),
    ([None], []),
    ([None, None], []),
    ([None, [], [{}]], []),
    ({"k": [{"l": None, "m": [None]}]}, {}),
]

issue_157_1 = """
[
  "state",
  {
    "_code": {
      "text": "1",
      "description": "production",
      "meaning": "http://ontologies.r.us/wonderful/states/19923",
      "alt_descriptions": {},
      "deprecated": null,
      "todos": [],
      "notes": [],
      "comments": [],
      "examples": [],
      "in_subset": [],
      "from_schema": null,
      "imported_from": null,
      "see_also": [],
      "deprecated_element_has_exact_replacement": null,
      "deprecated_element_has_possible_replacement": null,
      "is_a": null,
      "mixins": [],
      "extensions": {},
      "annotations": {}
    }
  }
]"""

issue_157_2 = """
[
  "namedstate",
  {
    "_code": {
      "text": "production",
      "description": "production",
      "meaning": "http://ontologies.r.us/wonderful/states/19923",
      "alt_descriptions": {},
      "deprecated": null,
      "todos": [],
      "notes": [],
      "comments": [],
      "examples": [],
      "in_subset": [],
      "from_schema": null,
      "imported_from": null,
      "see_also": [],
      "deprecated_element_has_exact_replacement": null,
      "deprecated_element_has_possible_replacement": null,
      "is_a": null,
      "mixins": [],
      "extensions": {},
      "annotations": {}
    }
  }
]
"""


def test_formats():
    assert "ThisIsIt" == camelcase("this is it")
    assert "ThisIsIT" == camelcase("  this   is iT   ")
    assert "un camelcased" == uncamelcase("UnCamelcased")
    assert "oneword" == uncamelcase("Oneword")
    assert "one_word" == uncamelcase("one_word")
    assert "another word" == uncamelcase("anotherWord")
    assert "IBeY" == camelcase("i be y ")
    assert "ThisIsIt" == camelcase("This__is_it")

    assert "this_is_it" == underscore(" this is it ")
    assert "this_is_it" == underscore("this   is   it")

    assert "thisIsIt" == lcamelcase("   this   is\t  it\n")

    assert "abc" == be("  abc\n")
    assert "" == be(None)
    assert "" == be("   ")


def test_linestuff():
    text = (
        "This is a mess'o test that goes on for a long way.  It has some carriage\n returns embedded in it "
        "but otherwise it drags on and on and on until the cows come home.  Splitline covers this we hope."
    )
    assert [
        "This is a mess'o test that goes on for a long way. It has some carriage returns embedded"
        " in it but otherwise it ",
        "drags on and on and on until the cows come home. Splitline covers this we hope. ",
    ] == split_line(text)
    assert [
        "This is a mess'o ",
        "test that goes on ",
        "for a long way. It ",
        "has some carriage ",
        "returns embedded in ",
        "it but otherwise it ",
        "drags on and on and ",
        "on until the cows ",
        "come home. ",
        "Splitline covers ",
        "this we hope. ",
    ] == split_line(text, 20)
    assert ["X" * 100 + " "] == split_line("X" * 100, 20)
    assert (
        "This is a mess'o test that goes on for a long way.  It has some carriage\n"
        "\treturns embedded in it but otherwise it drags on and on and on until the "
        "cows come home. Splitline covers this we \n"
        "\thope. "
    ) == wrapped_annotation(text)


def test_empty_functions():
    """Test the various forms of is_empty"""
    for thing in empty_things:
        assert is_empty(thing), f"{thing} should clock in as empty"
    for thing in non_empty_things:
        assert not is_empty(thing)
    obj = JsonObj([])
    assert is_empty(obj)


def test_remove_empty_items():
    """Test the various remove empty items paths"""
    seen = set()
    save = list()  # Keep garbage collection from reusing ids
    for thing, expected in things_removed:
        actual = remove_empty_items(thing)
        assert expected == actual, f"Input = {thing}"
        assert not isinstance(actual, JsonObj), "JSON objects are never returned"
        if isinstance(expected, (dict, list)):
            assert id(expected) != id(actual), f"Copy of {thing} was not returned"
            assert id(actual) not in seen, "remove_empty_items should always return a new thing"
            save.append(actual)
            seen.add(id(actual))


def test_enumerations_case():
    assert """[
   "state",
   "1"
]""" == as_json(remove_empty_items(json.loads(issue_157_1), hide_protected_keys=True))
    assert """[
   "namedstate",
   "production"
]""" == as_json(remove_empty_items(json.loads(issue_157_2), hide_protected_keys=True))
