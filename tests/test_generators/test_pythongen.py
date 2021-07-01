import unittest
from types import ModuleType
from typing import Optional

from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
PYTHON = env.expected_path('kitchen_sink.py')
DATA = env.input_path('kitchen_sink_inst_01.yaml')


def make_python(save: Optional[bool] = False) -> ModuleType:
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
        self.assertEqual("Company(id='ROR:1', name=None, aliases=[], ceo=None)", str(c))
        h = kitchen_module.EmploymentEvent(employed_at=c.id)
        self.assertEqual(
            "EmploymentEvent(started_at_time=None, ended_at_time=None, is_current=None, employed_at='ROR:1')", str(h))
        p = kitchen_module.Person('P:1', has_employment_history=[h])
        self.assertEqual("Person(id='P:1', name=None, has_employment_history=[EmploymentEvent(started_at_time=None, "
                         "ended_at_time=None, is_current=None, employed_at='ROR:1')], has_familial_relationships=[], "
                         "has_medical_history=[], age_in_years=None, addresses=[], aliases=[])", str(p))


if __name__ == '__main__':
    unittest.main()
