from dataclasses import dataclass

import pytest

from linkml_runtime.utils.eval_utils import eval_expr


@dataclass
class Person:
    name: str = None
    aliases: list[str] = None
    address: "Address" = None


@dataclass
class Address:
    street: str = None


@dataclass
class Container:
    name: str = None
    persons: list[Person] = None
    person_index: dict[str, Person] = None


def test_eval_expressions():
    assert eval_expr("1 + 2") == 3
    assert eval_expr("1 + 2 + 3") == 6
    assert eval_expr("{z} + 2", z=1) == 3
    assert eval_expr('{x} + {y}', x=5, y=None) is None
    assert eval_expr("'x' + 'y'") == 'xy'
    assert eval_expr("['a','b'] + ['c','d']") == ['a', 'b', 'c', 'd']
    assert eval_expr("{x} + {y}", x=['a', 'b'], y=['c', 'd']) == ['a', 'b', 'c', 'd']
    assert eval_expr("{'a': 1}") == {'a': 1}
    assert eval_expr("max([1, 5, 2])") == 5
    assert eval_expr("max({x})", x=[1, 5, 2]) == 5
    assert eval_expr("True") is True
    assert eval_expr("False") is False
    assert eval_expr("1 + 1 == 3") is False
    assert eval_expr("1 < 2") is True
    assert eval_expr("1 <= 1") is True
    assert eval_expr("1 >= 1") is True
    assert eval_expr("2 > 1") is True
    assert eval_expr("'EQ' if {x} == {y} else 'NEQ'", x=1, y=1) == 'EQ'
    assert eval_expr("'EQ' if {x} == {y} else 'NEQ'", x=1, y=2) == 'NEQ'
    assert eval_expr("'NOT_NULL' if x else 'NULL'", x=1) == 'NOT_NULL'
    assert eval_expr("'NOT_NULL' if x else 'NULL'", x=None) == 'NULL'
    assert eval_expr("'EQ' if {x} == {y} else 'NEQ'", x=1, y=2) == 'NEQ'
    case = "case(({x} < 25, 'LOW'), ({x} > 75, 'HIGH'), (True, 'MEDIUM'))"
    assert eval_expr(case, x=10) == 'LOW'
    assert eval_expr(case, x=100) == 'HIGH'
    assert eval_expr(case, x=50) == 'MEDIUM'
    assert eval_expr('x', x='a') == 'a'
    assert eval_expr('x+y', x=1, y=2) == 3
    assert eval_expr('x["a"] + y', x={'a': 1}, y=2) == 3
    assert eval_expr('x["a"]["b"] + y', x={'a': {'b': 1}}, y=2) == 3
    p = Person(name='x', aliases=['a', 'b', 'c'], address=Address(street='1 x street'))
    assert eval_expr('p.name', p=p) == 'x'
    assert eval_expr('p.address.street', p=p) == '1 x street'
    assert eval_expr('len(p.aliases)', p=p) == 3
    assert eval_expr('p.aliases', p=p) == p.aliases
    p2 = Person(name='x2', aliases=['a2', 'b2', 'c2'], address=Address(street='2 x street'))
    c = Container(persons=[p, p2])
    assert eval_expr('c.persons.name', c=c) == ['x', 'x2']
    assert eval_expr('c.persons.address.street', c=c) == ['1 x street', '2 x street']
    assert eval_expr('strlen(c.persons.address.street)', c=c) == [10, 10]
    c = Container(person_index={p.name: p, p2.name: p2})
    assert eval_expr('c.person_index.name', c=c) == ['x', 'x2']
    assert eval_expr('c.person_index.address.street', c=c) == ['1 x street', '2 x street']
    assert eval_expr('strlen(c.person_index.name)', c=c) == [1, 2]
    pd = dict(name='x', aliases=['a', 'b', 'c'], address=Address(street='1 x street'))
    assert eval_expr('p.name', p=pd, _distribute=False) == 'x'


def test_no_eval_prohibited():
    with pytest.raises(NotImplementedError):
        eval_expr("__import__('os').listdir()")


def test_funcs():
    with pytest.raises(NotImplementedError):
        eval_expr("my_func([1,2,3])")