import unittest

from jsonasobj2 import JsonObj
from linkml_runtime.linkml_model.meta import LINKML
from linkml_runtime.utils.compile_python import compile_python
from rdflib import Graph, Namespace

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase

NS = Namespace("https://example.org/test/")

schema = f"""id: {NS}
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  MyAny:
    class_uri: linkml:Any
  d:
    attributes:
      a:
      b:
  c:
    attributes:
      s:
        range: MyAny
      t:
        range: d
"""


class Issue296TestCase(TestEnvironmentTestCase):
    """Tests linkml:Any type
    See https://github.com/linkml/linkml/issues/296
    """

    env = env

    def test_any(self):
        py = PythonGenerator(schema).serialize()
        # print(py)
        mod = compile_python(py)
        dict_obj = {"x": 1, "y": {"foo": "foo1", "bar": "bar1"}}
        x = mod.C(s="foo")
        # print(x)
        self.assertEqual(x.s, "foo")
        x = mod.C(s=dict_obj)
        # print(x)
        self.assertEqual(x.s, JsonObj(dict_obj))
        x = mod.C(s=1)
        # print(x)
        self.assertEqual(x.s, 1)
        with self.assertRaises(Exception):
            mod.C(t=dict_obj)


if __name__ == "__main__":
    unittest.main()
