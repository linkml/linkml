import logging
import json
import yaml
import unittest
from decimal import Decimal
from numbers import Number
import jsonasobj
import jsonschema
from jsonschema.exceptions import ValidationError

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.dumpers import yaml_dumper, json_dumper
from linkml_runtime.loaders import yaml_loader, json_loader

from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase

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

class IssueDecimalCase(TestEnvironmentTestCase):
    env = env

    def test_decimals(self):
        """ Make sure decimals work """
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
            obj['age'] = v
            # JSON-Schema validation is strict: string values not allowed
            try:
                r = jsonschema.validate(obj, jsonschema_obj)
                logging.info(f'V={r}')
            except ValidationError as e:
                logging.info(f'Error="{e}" ;;\nExpected={expected_pass}')
                assert not expected_pass
            yaml_str = yaml.dump(obj)
            # Python initializers will convert from string to decimal
            try:
                py_obj = pymod.Person(**obj)
                #print(f'PY={py_obj} // {type(py_obj.age)}')
                logging.info(f'PY={py_obj}')
                logging.info(f'AGE_PLUS_ONE={py_obj.age + 1}')
                assert (py_obj.age + 1) -1 == py_obj.age
                assert isinstance(py_obj.age, Number)
                assert isinstance(py_obj.age, Decimal)
                # https://github.com/yaml/pyyaml/issues/255
                #yaml_str = yaml_dumper.dumps(py_obj)
                #print(yaml_str)
                # https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object
                # https://bugs.python.org/issue16535
                json_str = json_dumper.dumps(py_obj)
                py_obj2 = json_loader.loads(json_str, target_class=pymod.Person)
                assert py_obj.age == py_obj2.age
                assert (py_obj2.age + 1) -1 == py_obj2.age
                assert isinstance(py_obj2.age, Number)
                assert isinstance(py_obj2.age, Decimal)
            except Exception as e:
                if v is None:
                    # exception expected
                    assert True
                else:
                    logging.error(f'Unexpected exception: {e}')
                    assert False





if __name__ == '__main__':
    unittest.main()
