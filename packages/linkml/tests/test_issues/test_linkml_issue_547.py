import json
from decimal import Decimal
from numbers import Number

import jsonschema
import pytest
from jsonschema.exceptions import ValidationError
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.loaders import json_loader

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.pythongen import PythonGenerator

schema_str = """
id: http://example.org/decimals
name: decimals
imports:
  - https://w3id.org/linkml/types
default_range: string

classes:
  Person:
    tree_root: true
    attributes:
      id:
        identifier: true
      name: {}
      age:
        range: decimal
        required: true
"""


def test_decimals():
    """Make sure decimals work"""
    gen = JsonSchemaGenerator(schema_str)
    jsonschema_str = gen.serialize(not_closed=False)
    jsonschema_obj = json.loads(jsonschema_str)
    gen = PythonGenerator(schema_str)
    pymod = gen.compile_module()
    ages = [
        (30, True),
        (30.5, True),
        (Decimal("30"), True),
        (Decimal("30.5"), True),
        (Decimal(30), True),
        ("30", False),
        (None, False),
    ]
    obj = {"id": "bob"}
    for v, expected_pass in ages:
        obj["age"] = v

        # JSON-Schema validation is strict: string values not allowed
        def jsonschema_validate():
            jsonschema.validate(obj, jsonschema_obj)

        if expected_pass:
            jsonschema_validate()
        else:
            with pytest.raises(ValidationError):
                jsonschema_validate()

        # Python initializers will convert from string to decimal
        def python_validate():
            py_obj = pymod.Person(**obj)
            assert (py_obj.age + 1) - 1 == py_obj.age
            assert isinstance(py_obj.age, Number)
            assert isinstance(py_obj.age, Decimal)
            # https://github.com/yaml/pyyaml/issues/255
            # yaml_str = yaml_dumper.dumps(py_obj)
            # https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object
            # https://bugs.python.org/issue16535
            json_str = json_dumper.dumps(py_obj)
            py_obj2 = json_loader.loads(json_str, target_class=pymod.Person)
            assert py_obj.age == py_obj2.age
            assert (py_obj2.age + 1) - 1 == py_obj2.age
            assert isinstance(py_obj2.age, Number)
            assert isinstance(py_obj2.age, Decimal)

        if v is None:
            with pytest.raises(ValueError, match="age"):
                python_validate()
        else:
            python_validate()
