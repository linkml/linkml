import json
import unittest
from typing import List, Tuple, Any

from jsonasobj2 import JsonObj, as_json

from linkml_runtime.utils.formatutils import camelcase, underscore, lcamelcase, be, split_line, wrapped_annotation, \
    is_empty, remove_empty_items

empty_things = [None, dict(), list(), JsonObj(), JsonObj({}), JsonObj([])]
non_empty_things = [0, False, "", {'k': None}, {0:0}, [None], JsonObj(k=None), JsonObj(**{'k': None}), JsonObj([None])]

things_removed: List[Tuple[Any, Any]] = \
    [(None, None),
     (dict(), {}),
     (list(), []),
     (JsonObj(), {}),
     (JsonObj({}), {}),
     (JsonObj([]), []),
     (0, 0),
     (False, False),
     ("", ""),
     ({'k': None}, {}),
     ({0:0}, {0:0}),
     ([None], []),
     (JsonObj(k=None), {}),
     (JsonObj(**{'k': None}), {}),
     (JsonObj([None]), []),
     ([None], []),
     ([None, None],[]),
     ([None, [], [{}]], []),
     ({"k": [{"l": None, "m": [None]}]}, {})
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


class FormatUtilsTestCase(unittest.TestCase):
    def test_formats(self):
        self.assertEqual("ThisIsIt", camelcase("this is it"))
        self.assertEqual("ThisIsIT", camelcase("  this   is iT   "))
        self.assertEqual("IBeY", camelcase("i be y "))
        self.assertEqual("ThisIsIt", camelcase("This__is_it"))

        self.assertEqual("this_is_it", underscore(" this is it "))
        self.assertEqual("this_is_it", underscore("this   is   it"))

        self.assertEqual("thisIsIt", lcamelcase("   this   is\t  it\n"))

        self.assertEqual('abc', be('  abc\n'))
        self.assertEqual('', be(None))
        self.assertEqual('', be('   '))

    def test_linestuff(self):
        text = "This is a mess'o test that goes on for a long way.  It has some carriage\n returns embedded in it " \
               "but otherwise it drags on and on and on until the cows come home.  Splitline covers this we hope."
        self.assertEqual(["This is a mess'o test that goes on for a long way. It has some carriage returns embedded"
                          " in it but otherwise it ",
                          'drags on and on and on until the cows come home. Splitline covers this we hope. '],
                         split_line(text))
        self.assertEqual(["This is a mess'o ", 'test that goes on ', 'for a long way. It ', 'has some carriage ',
                          'returns embedded in ', 'it but otherwise it ', 'drags on and on and ', 'on until the cows ',
                          'come home. ', 'Splitline covers ', 'this we hope. '], split_line(text, 20))
        self.assertEqual(['X' * 100 + ' '], split_line('X'*100, 20))
        self.assertEqual("""This is a mess'o test that goes on for a long way.  It has some carriage
	returns embedded in it but otherwise it drags on and on and on until the cows come home. Splitline covers this we 
	hope. """, wrapped_annotation(text))

    def test_empty_functions(self):
        """ Test the various forms of is_empty """
        for thing in empty_things:
            self.assertTrue(is_empty(thing), msg=f"{thing} should clock in as empty")
        for thing in non_empty_things:
            self.assertFalse(is_empty(thing))

    def test_remove_empty_items(self):
        """ Test the various remove empty items paths """
        seen = set()
        save = list()      # Keep garbage collection from re-using ids
        for thing, expected in things_removed:
            actual = remove_empty_items(thing)
            self.assertEqual(expected, actual, msg=f"Input = {thing}")
            self.assertFalse(isinstance(actual, JsonObj), msg="JSON objects are never returned")
            if isinstance(expected, (dict, list)):
                self.assertNotEqual(id(expected), id(actual), msg=f"Copy of {thing} was not returned")
                self.assertNotIn(id(actual), seen, msg="remove_empty_items should always return a new thing")
                save.append(actual)
                seen.add(id(actual))

    def test_enumerations_case(self):
        self.assertEqual("""[
   "state",
   {
      "text": "1",
      "description": "production",
      "meaning": "http://ontologies.r.us/wonderful/states/19923"
   }
]""", as_json(remove_empty_items(json.loads(issue_157_1), hide_protected_keys=True)))
        self.assertEqual("""[
   "namedstate",
   {
      "text": "production",
      "description": "production",
      "meaning": "http://ontologies.r.us/wonderful/states/19923"
   }
]""", as_json(remove_empty_items(json.loads(issue_157_2), hide_protected_keys=True)))

if __name__ == '__main__':
    unittest.main()
