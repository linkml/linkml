import pytest

from linkml.utils.logictools import (
    And,
    Bottom,
    Eq,
    IsIn,
    Or,
    Term,
    Top,
    UniversalSet,
    Value,
    Variable,
    is_contradiction,
    simplify,
    simplify_full,
    to_dnf,
)

# constants for variables and builtin terms for testing
a = Variable("a")
b = Variable("b")
c = Variable("c")
d = Variable("d")
F = Bottom()
T = Top()


@pytest.mark.parametrize(
    "expr1,expr2,is_eq",
    [
        (a, a, True),
        (a, b, False),
        (Term("P"), Term("P"), True),
        (Term("P"), Term("P"), True),
        (Term("P", a), Term("P", a), True),
        (Term("P", a, b), Term("P", a, b), True),
        (Term("P", a, b), Term("P", b, a), False),
        (a < b, a < b, True),
        (a < b, b < a, False),
        (a < b, a > b, False),
        (Eq(a, b), Eq(a, b), True),
        (Eq(b, a), Eq(a, b), False),
    ],
)
def test_eq(expr1, expr2, is_eq):
    """
    Test structural equality of expressions.

    :param expr1:
    :param expr2:
    :param is_eq:
    :return:
    """
    if is_eq:
        assert expr1 == expr2
    else:
        assert expr1 != expr2


@pytest.mark.parametrize(
    "expr,expected_contradiction,dnf,simplified",
    [
        (T, False, T, T),
        (F, True, F, F),
        (~T, True, ~T, F),
        (~F, False, ~F, T),
        (~~T, False, T, T),
        (~~F, True, F, F),
        (F & F, True, F & F, F),
        (F & T, True, F & T, F),
        (F | T, False, F | T, T),
        (F | F, True, F | F, F),
        (And(T), False, And(T), T),
        (Or(T), False, Or(T), T),
        (a, None, a, a),
        (And(a), None, And(a), a),
        (Or(a), None, Or(a), a),
        (a & a, None, a & a, a),
        ((a & b) & c, None, And(a, b, c), And(a, b, c)),
        # (a & (b & c), None, a & (b & c), a & b & c),
        (a & F, True, a & F, F),
        (F & a, True, F & a, F),
        (a & T, None, a & T, a & T),
        (~a, None, ~a, ~a),
        (a & ~a, True, a & ~a, F),
        (~a & a, True, ~a & a, F),
        (~a & ~a, None, ~a & ~a, ~a),
        (~(a | b), None, ~a & ~b, ~a & ~b),
        (~(a & b), None, ~a | ~b, ~a | ~b),
        (a & (b & ~c), None, And(a, b, ~c), And(a, b, ~c)),
        (a & (b | ~c), None, (a & b) | (a & ~c), (a & b) | (a & ~c)),
        ((a & b) | c, None, (a & b) | c, (a & b) | c),
        ((a | b) & c, None, (a & c) | (b & c), (a & c) | (b & c)),
        ((a | b) & (c | d), None, Or(a & c, a & d, b & c, b & d), Or(a & c, a & d, b & c, b & d)),
        (And(a, And(b, c)), None, And(a, b, c), And(a, b, c)),
        (a & (b & ~a), True, And(a, b, ~a), F),
        # (a & (b | (c & ~a)), None, ((c & ~a) & a) | (a & b), a),
        (Or(Or(Or(a, b))), None, Or(a, b), Or(a, b)),
        (~~a, None, a, a),
        (a & ~~~a, True, a & ~a, F),
        (a < b, None, a < b, a < b),
        (a < Value(5), None, a < Value(5), a < Value(5)),
        ((a < 5) & (a < 10), None, (a < 5) & (a < 10), a < 5),
        ((a < 5) & (b < 10), None, (a < 5) & (b < 10), (a < 5) & (b < 10)),
        ((a < 5) | (a < 10), None, (a < 5) | (a < 10), a < 10),
        ((a < 10) & (a > 20), True, (a < 10) & (a > 20), F),
        (((a < 10) & c) & (a > 20), True, And(a < 10, c, a > 20), F),
        (a % b, None, a % b, a % b),
        (IsIn(a, UniversalSet()), False, IsIn(a, UniversalSet()), T),
        (IsIn(a, [1, 2, 3]), None, IsIn(a, [1, 2, 3]), IsIn(a, [1, 2, 3])),
        (
            IsIn(a, [1, 2, 3]) & IsIn(a, [2, 3, 4]),
            None,
            IsIn(a, [1, 2, 3]) & IsIn(a, [2, 3, 4]),
            IsIn(a, [2, 3]),
        ),
        (
            IsIn(a, [1, 2, 3]) | IsIn(a, [2, 3, 4]),
            None,
            IsIn(a, [1, 2, 3]) | IsIn(a, [2, 3, 4]),
            IsIn(a, [1, 2, 3, 4]),
        ),
        (
            IsIn(a, [1, 2, 3]) | (IsIn(a, [2, 3, 4]) & IsIn(a, [3, 4, 5])),
            None,
            IsIn(a, [1, 2, 3]) | (IsIn(a, [2, 3, 4]) & IsIn(a, [3, 4, 5])),
            IsIn(a, [1, 2, 3, 4]),
        ),
        (
            IsIn(a, [1, 2, 3]) & (IsIn(a, [0, 1]) | IsIn(a, [3, 4])),
            None,
            (IsIn(a, [1, 2, 3]) & IsIn(a, [0, 1])) | (IsIn(a, [1, 2, 3]) & IsIn(a, [3, 4])),
            IsIn(a, [1, 3]),
        ),
        # (a < 5, None, a < 5, a < 5),
    ],
)
def test_logic_functions(expr, expected_contradiction, dnf, simplified):
    """
    Test logic functions.

    - First expr is checked for satisfiability (contradictions);
    - next, the expression is converted to Disjunctive Normal Form (DNF)
    - next, the DNF is simplified.

    :param expr:
    :param expected_contradiction:
    :param dnf:
    :param simplified:
    :return:
    """
    assert is_contradiction(expr, apply_dnf=True) == expected_contradiction
    expr_to_dnf = to_dnf(expr)
    assert expr_to_dnf == dnf
    expr_simplified = simplify_full(expr_to_dnf)
    assert expr_simplified == simplified


@pytest.mark.parametrize(
    "expr,expected",
    [
        (T, T),
        (F, F),
        (T & T, T),
        (T | T, T),
        (F & F, F),
        (F | F, F),
        (F & T, F),
        (T | F, T),
        (~T, F),
        (~F, T),
        (~~T, T),
        (~~F, F),
        (a, a),
        (a & a, a),
        ((a & a) & a, a),
        (a & b, a & b),
        (a & b, b & a),
        (a | a, a),
        (a | b, a | b),
        (a | b, b | a),
        (~a, ~a),
        (~~a, a),
        (a & F, F),
        (a | F, a | F),
        (a & ~b, a & ~b),
        (a & ~a, F),
        (a | ~a, T),
        ((a | b) & c, (a & c) | (b & c)),
        ((a | b) & (c | d), Or(a & c, a & d, b & c, b & d)),
        ((~b) & (a | b), (a & ~b) | F),
        (Term("P", a, b), Term("P", a, b)),
        (Term("<", 5), Term("<", 5)),
    ],
)
def test_solve(expr, expected):
    r = to_dnf(expr)
    simplified = simplify(r)
    assert simplified == expected
