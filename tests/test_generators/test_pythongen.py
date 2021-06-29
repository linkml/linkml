import unittest

from linkml_runtime.loaders import yaml_loader, json_loader, rdf_loader
from linkml_runtime.dumpers import json_dumper, rdf_dumper
from linkml.generators.pythongen import PythonGenerator
from tests.test_generators.environment import env
import jsonschema
import json
import yaml
from output.kitchen_sink import *

SCHEMA = env.input_path('kitchen_sink.yaml')
PYTHON = env.expected_path('kitchen_sink.py')
DATA = env.input_path('kitchen_sink_inst_01.yaml')

def make_python() -> None:
    """
    Note: if you change the yaml schema and associated test instance objects,
    you may need to run this test twice
    """
    pstr = str(PythonGenerator(SCHEMA, mergeimports=True).serialize())
    #eval(compile(pstr))
    with open(PYTHON, 'w') as io:
        io.write(pstr)
    c = Company('ROR:1')
    h = EmploymentEvent(employed_at=c.id)
    p = Person('P:1', has_employment_history=[h])

class PythonGenTestCase(unittest.TestCase):
    def test_pythongen(self):
        """ python """
        make_python()

if __name__ == '__main__':
    unittest.main()
