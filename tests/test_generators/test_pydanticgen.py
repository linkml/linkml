import unittest

import yaml
from linkml_runtime import SchemaView
from linkml_runtime.utils.compile_python import compile_python
from pydantic import ValidationError

from linkml.generators.pydanticgen import PydanticGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
DATA = env.input_path('kitchen_sink_inst_01.yaml')
PYDANTIC_OUT = env.expected_path('kitchen_sink_pydantic.py')
PACKAGE = 'kitchen_sink'


class PydanticGeneratorTestCase(unittest.TestCase):

    def test_pydantic(self):
        """ Generate pydantic classes  """
        gen = PydanticGenerator(SCHEMA, package=PACKAGE)
        code = gen.serialize()
        with open(PYDANTIC_OUT, 'w') as stream:
            stream.write(code)
        with open(DATA) as stream:
            dataset_dict = yaml.safe_load(stream)
        # NOTE: compile_python and dynamic compilation in general does not seem to work
        # for pydantic code. As an alternative, we import the generated model within a function
        # that is called *after* the code is generated.
        # note for developers: you will lack IDE support in this section of the code
        def test_dynamic():
            from tests.test_generators.output.kitchen_sink_pydantic import Person, EmploymentEvent, Dataset
            # NOTE: generated pydantic doesn't yet do validation
            e1 = EmploymentEvent(is_current=True)
            p1 = Person(id='x', has_employment_history=[e1])
            print(p1)
            assert p1.id == 'x'
            assert p1.name is None
            json = {'id': 'P1', 'has_employment_history': [{'is_current': True}]}
            p2 = Person(**json)
            print(p2)
            p2 = Person(**dataset_dict['persons'][0])
            ds1 = Dataset(**dataset_dict)
            print(ds1)
            assert len(ds1.persons) == 2
        test_dynamic()

    def test_compile_pydantic(self):
        """ Generate and compile pydantic classes  """
        gen = PydanticGenerator(SCHEMA, package=PACKAGE)
        code = gen.serialize()
        mod = compile_python(code, PACKAGE)
        p = mod.Person(id='P:1')
        assert p.id == 'P:1'
        with self.assertRaises(TypeError):
            mod.Person(no_such_field='x')
        with self.assertRaises(ValidationError):
            mod.Person(age_in_years='x')

    def test_pydantic_enums(self):

        unit_test_schema = """
id: unit_test
name: unit_test

enums:
  TestEnum:
    permissible_values:
      123:
      +:
      This & that, plus maybe a 🎩:
      Ohio:
"""

        sv = SchemaView(unit_test_schema)
        gen = PydanticGenerator(schema=unit_test_schema)
        enums = gen.generate_enums(sv.all_enums())
        assert enums
        enum = enums['TestEnum']
        assert enum
        assert enum['values']['number_123'] == '123'
        assert enum['values']['PLUS_SIGN'] == '+'
        assert enum['values']['This_AMPERSAND_that_plus_maybe_a_TOP_HAT'] == 'This & that, plus maybe a 🎩'
        assert enum['values']['Ohio'] == 'Ohio'

if __name__ == '__main__':
    unittest.main()
