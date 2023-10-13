import pytest
from jsonasobj2 import JsonObj
from linkml_runtime.utils.compile_python import compile_python
from rdflib import Namespace

from linkml.generators.pythongen import PythonGenerator

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


def test_any():
    """Tests linkml:Any type
    See https://github.com/linkml/linkml/issues/296
    """
    py = PythonGenerator(schema).serialize()
    mod = compile_python(py)
    dict_obj = {"x": 1, "y": {"foo": "foo1", "bar": "bar1"}}
    x = mod.C(s="foo")
    assert x.s == "foo"
    x = mod.C(s=dict_obj)
    assert x.s == JsonObj(dict_obj)
    x = mod.C(s=1)
    assert x.s == 1
    with pytest.raises(Exception):
        mod.C(t=dict_obj)
