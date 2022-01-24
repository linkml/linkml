import unittest
from dataclasses import dataclass
from typing import List, Dict

from linkml_runtime.utils.eval_utils import eval_expr


@dataclass
class Person:
    name: str = None
    aliases: List[str] = None
    address: "Address" = None


@dataclass
class Address:
    street: str = None


@dataclass
class Container:
    name: str = None
    persons: List[Person] = None
    person_index: Dict[str, Person] = None


class EvalUtilsTestCase(unittest.TestCase):
    """
    Tests for linkml_runtime.utils.eval_utils
    """

    def test_eval_expressions(self):
        """
        Tests evaluation of expressions using eval_expr
        """
        x = eval_expr("1 + 2")
        self.assertEqual(x, 3)
        self.assertEqual(eval_expr("1 + 2 + 3"), 6)
        x = eval_expr("{z} + 2", z=1)
        self.assertEqual(x, 3)
        self.assertIsNone(eval_expr('{x} + {y}', x=5, y=None))
        x = eval_expr("'x' + 'y'")
        assert x == 'xy'
        #x = eval_expr("'{x}' + '{y}'", x='a', y='b')
        #self.assertEqual(x, 'ab')
        self.assertEqual(eval_expr("['a','b'] + ['c','d']"), ['a', 'b', 'c', 'd'])
        self.assertEqual(eval_expr("{x} + {y}", x=['a', 'b'], y=['c', 'd']), ['a', 'b', 'c', 'd'])
        self.assertEqual(eval_expr("{'a': 1}"), {'a': 1})
        self.assertEqual(eval_expr("max([1, 5, 2])"), 5)
        self.assertEqual(eval_expr("max({x})", x=[1, 5, 2]), 5)
        self.assertEqual(eval_expr("True"), True)
        self.assertEqual(eval_expr("False"), False)
        self.assertEqual(eval_expr("1 + 1 == 3"), False)
        self.assertEqual(eval_expr("1 < 2"), True)
        self.assertEqual(eval_expr("1 <= 1"), True)
        self.assertEqual(eval_expr("1 >= 1"), True)
        self.assertEqual(eval_expr("2 > 1"), True)
        self.assertEqual(eval_expr("'EQ' if {x} == {y} else 'NEQ'", x=1, y=1), 'EQ')
        self.assertEqual(eval_expr("'EQ' if {x} == {y} else 'NEQ'", x=1, y=2), 'NEQ')
        self.assertEqual(eval_expr("'NOT_NULL' if x else 'NULL'", x=1), 'NOT_NULL')
        self.assertEqual(eval_expr("'NOT_NULL' if x else 'NULL'", x=None), 'NULL')
        self.assertEqual(eval_expr("'EQ' if {x} == {y} else 'NEQ'", x=1, y=2), 'NEQ')
        case = "case(({x} < 25, 'LOW'), ({x} > 75, 'HIGH'), (True, 'MEDIUM'))"
        self.assertEqual(eval_expr(case, x=10), 'LOW')
        self.assertEqual(eval_expr(case, x=100), 'HIGH')
        self.assertEqual(eval_expr(case, x=50), 'MEDIUM')
        self.assertEqual(eval_expr('x', x='a'), 'a')
        self.assertEqual(eval_expr('x+y', x=1, y=2), 3)
        # todo
        self.assertEqual(eval_expr('x["a"] + y', x={'a': 1}, y=2), 3)
        self.assertEqual(eval_expr('x["a"]["b"] + y', x={'a': {'b': 1}}, y=2), 3)
        p = Person(name='x', aliases=['a', 'b', 'c'], address=Address(street='1 x street'))
        self.assertEqual(eval_expr('p.name', p=p), 'x')
        self.assertEqual(eval_expr('p.address.street', p=p), '1 x street')
        self.assertEqual(eval_expr('len(p.aliases)', p=p), 3)
        self.assertEqual(eval_expr('p.aliases', p=p), p.aliases)
        p2 = Person(name='x2', aliases=['a2', 'b2', 'c2'], address=Address(street='2 x street'))
        c = Container(persons=[p, p2])
        x = eval_expr('c.persons.name', c=c)
        self.assertEqual(x, ['x', 'x2'])
        x = eval_expr('c.persons.address.street', c=c)
        self.assertEqual(x, ['1 x street', '2 x street'])
        x = eval_expr('strlen(c.persons.address.street)', c=c)
        self.assertEqual(x, [10, 10])
        c = Container(person_index={p.name: p, p2.name: p2})
        x = eval_expr('c.person_index.name', c=c)
        #print(x)
        self.assertEqual(x, ['x', 'x2'])
        x = eval_expr('c.person_index.address.street', c=c)
        self.assertEqual(x, ['1 x street', '2 x street'])
        x = eval_expr('strlen(c.person_index.name)', c=c)
        self.assertEqual(x, [1, 2])
        #self.assertEqual('x', eval_expr('"x" if True else "y"'))

    def test_no_eval_prohibited(self):
        """
        Ensure that certain patterns cannot be evaluated

        See `<https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string>`_
        """
        with self.assertRaises(NotImplementedError):
            eval_expr("__import__('os').listdir()")

    def test_funcs(self):
        """
        Not yet implemented
        """
        with self.assertRaises(NotImplementedError):
            eval_expr("my_func([1,2,3])")


if __name__ == '__main__':
    unittest.main()
