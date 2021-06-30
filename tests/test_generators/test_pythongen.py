import unittest
from typing import Optional

from linkml_runtime.loaders import yaml_loader, json_loader, rdf_loader
from linkml_runtime.dumpers import json_dumper, rdf_dumper
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator
from tests.test_generators.environment import env
import jsonschema
import json
import yaml

SCHEMA = env.input_path('kitchen_sink.yaml')
PYTHON = env.expected_path('kitchen_sink.py')
DATA = env.input_path('kitchen_sink_inst_01.yaml')


def make_python(save: Optional[bool] = False) -> None:
    """
    Note: if you change the yaml schema and associated test instance objects,
    you may need to run this test twice
    """
    pstr = str(PythonGenerator(SCHEMA, mergeimports=True).serialize())
    kitchen_module = compile_python(pstr)
    if save:
        with open(PYTHON, 'w') as io:
            io.write(pstr)
    return kitchen_module


class PythonGenTestCase(unittest.TestCase):
    def test_pythongen(self):
        """ python """
        kitchen_module = make_python(True)
        c = kitchen_module.Company('ROR:1')
        h = kitchen_module.EmploymentEvent(employed_at=c.id)
        p = kitchen_module.Person('P:1', has_employment_history=[h])


if __name__ == '__main__':
    unittest.main()
