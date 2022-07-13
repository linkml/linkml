import os
import unittest
from decimal import Decimal

from linkml_runtime.utils.inference_utils import infer_all_slot_values, generate_slot_value, infer_slot_value, Policy, \
    Config
from linkml_runtime.utils.schemaview import SchemaView

from tests.test_utils.model.inference_example import Person, Container, Evil, Relationship, AgeEnum
from tests.test_utils import INPUT_DIR

SCHEMA = os.path.join(INPUT_DIR, 'inference-example.yaml')

AGE_IN_YEARS = 12
FIRST, LAST = 'x', 'y'
FULL = f'{FIRST} {LAST}'
REPLACE_ME = 'REPLACE ME'


class InferenceUtilsTestCase(unittest.TestCase):
    """
    Tests for inkml_runtime.utils.inference_utils
    """

    def test_rstring_serialization(self):
        """
        Tests serialization of strings via linkml:string_serialization
        """
        sv = SchemaView(SCHEMA)
        p = Person(first_name=FIRST, last_name=LAST)
        v = generate_slot_value(p, 'full_name', sv)

    def test_string_serialization(self):
        """
        Tests serialization of strings via linkml:string_serialization
        """
        sv = SchemaView(SCHEMA)
        p = Person(first_name=FIRST, last_name=LAST)
        v = generate_slot_value(p, 'full_name', sv)
        self.assertEqual(v, FULL)
        infer_slot_value(p, 'full_name', sv)
        self.assertEqual(p.full_name, FULL)
        p = Person(first_name=FIRST, last_name=LAST)
        infer_all_slot_values(p, schemaview=sv)
        self.assertEqual(p.full_name, FULL)
        # test override
        p = Person(first_name=FIRST, last_name=LAST, full_name=REPLACE_ME)
        infer_all_slot_values(p, schemaview=sv, policy=Policy.OVERRIDE)
        self.assertEqual(p.full_name, FULL)
        # test keep
        p = Person(first_name=FIRST, last_name=LAST, full_name=REPLACE_ME)
        infer_all_slot_values(p, schemaview=sv, policy=Policy.KEEP)
        self.assertEqual(p.full_name, REPLACE_ME)
        # test strict
        p = Person(first_name=FIRST, last_name=LAST, full_name=REPLACE_ME)
        with self.assertRaises(ValueError):
            infer_all_slot_values(p, schemaview=sv, policy=Policy.STRICT)
        # same value test
        for policy in [Policy.OVERRIDE, Policy.STRICT, Policy.KEEP]:
            p = Person(first_name=FIRST, last_name=LAST, full_name=FULL)
            infer_all_slot_values(p, schemaview=sv, policy=policy)
            self.assertEqual(p.full_name, FULL)
        # test recursion
        c = Container(persons=[Person(first_name=FIRST, last_name=LAST)])
        infer_all_slot_values(c, schemaview=sv)
        self.assertEqual(c.persons[0].full_name, FULL)
        # test slots with spaces
        p = Person(slot_with_spaces="test")
        infer_all_slot_values(p, schemaview=sv)
        self.assertEqual(p.derived_slot_with_spaces, "test")

    def test_infer_expressions(self):
        """
        Tests using of string_serialization to infer value setting from expressions
        """
        sv = SchemaView(SCHEMA)
        p = Person(age_in_years=Decimal(AGE_IN_YEARS))
        config = Config(use_expressions=True)
        policy = Policy.STRICT
        infer_all_slot_values(p, schemaview=sv, config=config, policy=policy)
        self.assertEqual(p.age_in_months, p.age_in_years * 12)
        self.assertEqual(p.is_juvenile, True)
        self.assertEqual(AGE_IN_YEARS, p.age_in_years)
        infer_all_slot_values(p, schemaview=sv, config=config, policy=policy)
        self.assertEqual(p.age_in_months, p.age_in_years * 12)
        p.age_in_months = None
        infer_all_slot_values(p, schemaview=sv, config=config, policy=policy)
        self.assertEqual(p.age_in_months, p.age_in_years * 12)
        # reverse
        p = Person(age_in_months=Decimal(AGE_IN_YEARS) * 12)
        infer_all_slot_values(p, schemaview=sv, config=config, policy=policy)
        self.assertEqual(p.age_in_months, p.age_in_years * 12)
        self.assertEqual(p.age_in_years, AGE_IN_YEARS)
        # inconsistency
        p = Person(age_in_years=Decimal(AGE_IN_YEARS), age_in_months=Decimal(AGE_IN_YEARS))
        with self.assertRaises(ValueError):
            infer_all_slot_values(p, schemaview=sv, config=config, policy=Policy.STRICT)
        p = Person(age_in_years=Decimal(AGE_IN_YEARS), age_in_months=Decimal(AGE_IN_YEARS))
        infer_all_slot_values(p, schemaview=sv, config=config, policy=Policy.OVERRIDE)
        # final answer should be consistent
        self.assertEqual(p.age_in_months, p.age_in_years * 12)
        # answer not guaranteed
        assert p.age_in_years == AGE_IN_YEARS or p.age_in_years == AGE_IN_YEARS / 12

        p = Person(age_in_years=Decimal(50))
        config = Config(use_expressions=True)
        infer_all_slot_values(p, schemaview=sv, config=config)
        assert not p.is_juvenile
        p = Person(age_in_years=Decimal(10))
        config = Config(use_expressions=True)
        infer_all_slot_values(p, schemaview=sv, config=config)
        assert p.is_juvenile
        self.assertEqual(p.age_category, AgeEnum('juvenile'))
        self.assertEqual(p.age_category.code, AgeEnum.juvenile)
        #e1 = AgeEnum('juvenile')
        #e2 = AgeEnum.juvenile
        #print(f'e1={e1} c={e1.code} t={type(e1)}')
        #print(f'e2={e2} {type(e2)}')
        # test slots with spaces
        p = Person(slot_with_spaces="test")
        infer_all_slot_values(p, schemaview=sv, config=config)
        self.assertEqual(p.derived_expression_from_spaces, "test")

    def test_if_then(self):
        sv = SchemaView(SCHEMA)
        p = Person(first_name='x', last_name='y', age_in_years=Decimal(AGE_IN_YEARS))
        config = Config(use_expressions=True)
        infer_all_slot_values(p, schemaview=sv, config=config)
        self.assertEqual(p.summary, f'xy AGE: {AGE_IN_YEARS}')
        p = Person(first_name='x', last_name='y')
        infer_all_slot_values(p, schemaview=sv, config=config)
        self.assertEqual(p.summary, 'xy NO AGE SPECIFIED')

    def test_custom_function(self):
        sv = SchemaView(SCHEMA)
        p = Person(first_name='abc', last_name='def', age_in_years=Decimal(AGE_IN_YEARS))
        config = Config(resolve_function=lambda x, _: f'"{x.upper()}"' if isinstance(x, str) else x)
        infer_all_slot_values(p, schemaview=sv, config=config)
        self.assertEqual(p.full_name, '"ABC" "DEF"')
        self.assertEqual(p.age_in_years, Decimal(AGE_IN_YEARS))

    def test_protect_against_evil(self):
        """
        Ensure that certain patterns cannot be evaluated

        See `<https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string>`_
        """
        sv = SchemaView(SCHEMA)
        p = Evil()
        config = Config(use_expressions=True)
        policy = Policy.OVERRIDE
        with self.assertRaises(NotImplementedError):
            infer_all_slot_values(p, schemaview=sv, config=config, policy=policy)


    def test_nesting(self):
        """
        Tests use of nested variables
        """
        sv = SchemaView(SCHEMA)
        p1 = Person(first_name='a', last_name='b')
        p2 = Person(first_name='c', last_name='d')
        r = Relationship(person1=p1, person2=p2, type='SIBLING_OF')
        infer_all_slot_values(r, schemaview=sv)
        self.assertEqual('"b, a" IS SIBLING_OF "d, c"', r.description)
        self.assertEqual('"a b" IS SIBLING_OF "c d"', r.description2)


if __name__ == '__main__':
    unittest.main()
