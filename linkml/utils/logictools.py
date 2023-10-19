import operator
from copy import deepcopy
from itertools import product
from typing import Any, Collection, List, Optional, Tuple


def member_of(item: Any, collection: Collection[Any]) -> bool:
    return item in collection


OPS = {
    operator.__lt__: "<",
    operator.__le__: "<=",
    operator.__eq__: "==",
    operator.__ne__: "!=",
    operator.__gt__: ">",
    operator.__ge__: ">=",
    operator.__and__: "&",
    operator.__or__: "|",
    operator.__invert__: "~",
    operator.__mod__: "%",
    # operator.__contains__: 'in',
    member_of: "in",
}


class Expression:
    def __eq__(self, other: "Expression"):
        if isinstance(other, Expression):
            return self._ordered_str() == other._ordered_str()
        else:
            return False

    def __and__(self, other: "Expression"):
        return And(self, other)

    def __or__(self, other: "Expression"):
        return Or(self, other)

    def __invert__(self):
        return Not(self)

    def __lt__(self, other: Any):
        return Term("<", self, other)

    def __le__(self, other: Any):
        return Term("<=", self, other)

    def __ne__(self, other: Any):
        return Term("!=", self, other)

    def __gt__(self, other: Any):
        return Term(">", self, other)

    def __ge__(self, other: Any):
        return Term(">=", self, other)

    def __mod__(self, other: Any):
        return Term("%", self, other)

    def __contains__(self, other: Any):
        return Term("contains", self, other)

    def _ordered_str(self, **kwargs):
        return str(self)

    def __repr__(self):
        return self._ordered_str()


class Variable(Expression):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return str(self.name)

    def _ordered_str(self, **kwargs):
        return str(self.name)


class Top(Expression):
    def __str__(self):
        return "T"

    def _ordered_str(self, **kwargs):
        return str(self)


class Bottom(Expression):
    def __str__(self):
        return "F"

    def _ordered_str(self, **kwargs):
        return str(self)


class Not(Expression):
    def __init__(self, operand: Expression):
        self.operand = operand

    def __str__(self):
        return f"~{self.operand})"

    def _ordered_str(self, **kwargs):
        return str(self)


class And(Expression):
    def __init__(self, *operands: Expression):
        self.operands: List[Expression] = list(operands)

    def __str__(self):
        return f'({" & ".join(str(operand) for operand in self.operands)})'

    def _ordered_str(self, **kwargs):
        sorted_operands = sorted([op._ordered_str(**kwargs) for op in self.operands], key=str)
        return f'({" & ".join(sorted_operands)})'


class Or(Expression):
    def __init__(self, *operands: Expression):
        self.operands = list(operands)

    def __str__(self):
        return f'({" | ".join(str(operand) for operand in self.operands)})'

    def _ordered_str(self, pairwise=False):
        if pairwise and len(self.operands) > 2:
            return Or(Or(*self.operands[0:2]), Or(*self.operands[2:]))._ordered_str(pairwise=True)
        sorted_operands = sorted([op._ordered_str(pairwise=True) for op in self.operands], key=str)
        return f'({" | ".join(sorted_operands)})'


class Eq(Expression):
    def __init__(self, lhs: Expression, rhs: Expression):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f"{str(self.lhs)} = {str(self.rhs)}"

    def _ordered_str(self, **kwargs):
        return str(self)


class Term(Expression):
    def __init__(self, predicate: str, *operands: Any):
        self.predicate = predicate
        self.operands = list(operands)

    def __str__(self):
        if self.predicate in OPS:
            return f"{str(self.operands[0])} {OPS[self.predicate]} {str(self.operands[1])}"
        else:
            return f'{self.predicate}({", ".join(str(operand) for operand in self.operands)})'

    def _ordered_str(self, **kwargs):
        return str(self)


class IsIn(Term):
    def __init__(self, element: Expression, collection: List[Any]):
        self.predicate = "in"
        self.operands = [element, collection]


class Value(Expression):
    # DEPRECATED
    def __init__(self, operand: Any):
        self.operand = operand

    def __str__(self):
        return str(self.operand)

    def _ordered_str(self, **kwargs):
        return str(self)


class Implies(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} => {self.right})"

    def _ordered_str(self, **kwargs):
        return f"({self.left._ordered_str(**kwargs)} => {self.right._ordered_str(**kwargs)})"


class Iff(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} => {self.right})"

    def _ordered_str(self, **kwargs):
        return f"({self.left._ordered_str(**kwargs)} iff {self.right._ordered_str(**kwargs)})"


class UniversalSet(Expression):
    def __str__(self):
        return "__U__"

    def _ordered_str(self, **kwargs):
        return str(self)


# DNF conversion functions


def eliminate_implications(expr: Expression) -> Expression:
    """
    Eliminate implications and iffs from an expression.

    - ``P => Q is equivalent to ~P | Q``
    - ``P iff Q is equivalent to (~P | Q) & (P | ~Q)``

    Also recurse through sub-expressions

    :param expr:
    :return:
    """
    if isinstance(expr, Implies):
        # P => Q is equivalent to ~P | Q
        return Or(Not(expr.left), expr.right)
    elif isinstance(expr, Iff):
        # P iff Q is equivalent to (~P | Q) & (P | ~Q)
        return And(Or(Not(expr.left), expr.right), Or(expr.left, Not(expr.right)))
    elif isinstance(expr, And) or isinstance(expr, Or):
        # Recursively eliminate implications from Ands:
        # Tr(P1 & P2 & ... & Pn) is equivalent to Tr(P1) & Tr(P2) & ... & Tr(Pn)
        expr.operands = list(map(eliminate_implications, expr.operands))
    elif isinstance(expr, Not) and isinstance(expr.operand, (And, Or, Implies, Iff)):
        # Recursively eliminate implications from Nots:
        # Tr(~(P1)) is equivalent to ~Tr(P1)
        expr.operand = eliminate_implications(expr.operand)
    return expr


def move_not_inwards(expr: Expression) -> Expression:
    """
    Move negations inwards in an expression.

    :param expr:
    :return:
    """
    if isinstance(expr, Not) and isinstance(expr.operand, Not):
        return expr.operand.operand
    elif isinstance(expr, Not) and isinstance(expr.operand, And):
        return Or(*[Not(operand) for operand in expr.operand.operands])
    elif isinstance(expr, Not) and isinstance(expr.operand, Or):
        return And(*[Not(operand) for operand in expr.operand.operands])
    elif isinstance(expr, And) or isinstance(expr, Or):
        expr.operands = list(map(move_not_inwards, expr.operands))
    elif isinstance(expr, Not) and isinstance(expr.operand, (And, Or)):
        expr.operand = move_not_inwards(expr.operand)
    return expr


def distribute_and_over_or(expr: Expression) -> Expression:
    """
    Distributes AND over OR in the given expression according to the distributive laws of Boolean Algebra.

    The function works recursively, transforming each AND operation in the expression.

    Args:
        expr (Expression): The input expression which is an instance of Expression or its subclasses.

    Returns:
        Expression: The transformed expression with AND distributed over OR.
    """
    if isinstance(expr, And):
        or_exprs = [operand for operand in expr.operands if isinstance(operand, Or)]
        other_exprs = [operand for operand in expr.operands if not isinstance(operand, Or)]
        if or_exprs:
            new_operands = []
            for combination in product(*[or_expr.operands for or_expr in or_exprs]):
                new_operands.append(And(*(other_exprs + list(combination))))
            return Or(*new_operands)
        expr.operands = list(map(distribute_and_over_or, expr.operands))
        # conj over conj
        and_exprs = [operand for operand in expr.operands if isinstance(operand, And)]
        if and_exprs:
            new_operands = []
            for and_expr in and_exprs:
                new_operands.extend(and_expr.operands)
            new_operands.extend([operand for operand in expr.operands if not isinstance(operand, And)])
            return And(*new_operands)
    elif isinstance(expr, Or):
        expr.operands = list(map(distribute_and_over_or, expr.operands))
        # disj over disj
        or_exprs = [operand for operand in expr.operands if isinstance(operand, Or)]
        if or_exprs:
            new_operands = []
            for or_expr in or_exprs:
                new_operands.extend(or_expr.operands)
            new_operands.extend([operand for operand in expr.operands if not isinstance(operand, Or)])
            return Or(*new_operands)
    elif isinstance(expr, Not):
        expr.operand = distribute_and_over_or(expr.operand)
    return expr


def is_contradiction(expr: Expression, apply_dnf=False) -> Optional[bool]:
    if apply_dnf:
        expr = to_dnf(expr)
        expr = simplify(expr)
    if isinstance(expr, And):
        for i, op_i in enumerate(expr.operands):
            if isinstance(op_i, Not):
                for j, op_j in enumerate(expr.operands):
                    if op_i != op_j:
                        if op_i.operand == op_j:
                            return True
        opx = [is_contradiction(operand) for operand in expr.operands]
        if any(opx):
            return True
        elif any([x is None for x in opx]):
            return None
        else:
            return False
        # return any([is_contradiction(operand) for operand in expr.operands])
    elif isinstance(expr, Not):
        negated_expr = is_contradiction(expr.operand)
        if negated_expr is None:
            return None
        else:
            return not negated_expr
    elif isinstance(expr, Or):
        opx = [is_contradiction(operand) for operand in expr.operands]
        if all(opx):
            return True
        elif any([x is False for x in opx]):
            return False
        else:
            return None
    if expr == Bottom():
        return True
    elif expr == Top():
        return False
    elif isinstance(expr, Term) and expr.predicate == "in":
        if expr.operands[1] == UniversalSet():
            return False
        if expr.operands[1] == []:
            return True
    return None


def evals_to_true(expr: Expression, apply_dnf=False) -> Optional[bool]:
    """
    Two-valued logic

    :param expr:
    :param apply_dnf:
    :return:
    """
    if apply_dnf:
        expr = to_dnf(expr)
    if isinstance(expr, And):
        return all([evals_to_true(operand) for operand in expr.operands])
    elif isinstance(expr, Not):
        if is_contradiction(expr.operand) is False:
            return True
        else:
            return False
    elif isinstance(expr, Or):
        return any([evals_to_true(operand) for operand in expr.operands])
    elif expr == Top():
        return True
    elif isinstance(expr, IsIn):
        if expr.operands[1] == UniversalSet():
            return True
    else:
        return False


def is_tautology(expr):
    """
    Checks if the given propositional logic formula is a tautology.

    A formula is a tautology if it is true under every possible valuation of its variables.

    Args:
        expr (Expression): The input formula which is an instance of Expression or its subclasses.

    Returns:
        bool: True if the formula is a tautology, False otherwise.
    """
    if isinstance(expr, Or):
        for i in range(len(expr.operands)):
            for j in range(i + 1, len(expr.operands)):
                if isinstance(expr.operands[i], Not) and expr.operands[i].operand == expr.operands[j]:
                    return True
                elif isinstance(expr.operands[j], Not) and expr.operands[j].operand == expr.operands[i]:
                    return True
    elif isinstance(expr, And):
        for operand in expr.operands:
            if is_tautology(operand):
                return True
    return False


def eliminate_redundant(expr: Expression) -> Expression:
    if isinstance(expr, And):
        visited = set()
        new_operands = []
        for i, operand in enumerate(expr.operands):
            # if isinstance(operand, Top):
            #    continue
            operand = eliminate_redundant(operand)
            operand_str = operand._ordered_str()
            if operand_str not in visited:
                visited.add(operand_str)
                new_operands.append(operand)
        expr.operands = new_operands
    elif isinstance(expr, Or):
        visited = set()
        new_operands = []
        for i, operand in enumerate(expr.operands):
            if isinstance(operand, Bottom):
                continue
            operand = eliminate_redundant(operand)
            operand_str = operand._ordered_str()
            if operand_str not in visited:
                visited.add(operand_str)
                new_operands.append(operand)
        expr.operands = new_operands
    return expr


def simplify_full(expr: Expression) -> Expression:
    simplified = simplify(expr)
    if str(simplified) != str(expr):
        return simplify_full(simplified)
    else:
        return simplified


def simplify(expr: Expression) -> Expression:
    """
    Simplifies the given propositional logic formula.

    :param expr:
    :return:
    """
    expr = to_dnf(expr)
    if expr == ~Bottom():
        return Top()
    if expr == ~Top():
        return Bottom()
    if is_contradiction(expr, apply_dnf=False):
        return Bottom()
    if evals_to_true(expr):
        return Top()
    if isinstance(expr, (And, Or)):
        modified = True
        while modified:
            modified = False
            modifications = []
            for i, op_i in enumerate(expr.operands):
                for j, op_j in enumerate(expr.operands):
                    if i < j:
                        for composition in COMPOSITIONS[type(expr)]:
                            new_expr = composition(op_i, op_j)
                            if new_expr is not None:
                                modifications.append((i, j, new_expr))
                            else:
                                new_expr = composition(op_j, op_i)
                                if new_expr is not None:
                                    modifications.append((j, i, new_expr))
                                else:
                                    if (
                                        isinstance(op_i, Term)
                                        and isinstance(op_j, Term)
                                        and op_i.operands[0] == op_j.operands[0]
                                    ):
                                        new_tpl = compose_operators(
                                            type(expr),
                                            op_i.predicate,
                                            op_i.operands[1],
                                            op_j.predicate,
                                            op_j.operands[1],
                                        )
                                        if new_tpl is not None:
                                            new_op, new_arg = new_tpl
                                            new_expr = Term(OPS[new_op], op_i.operands[0], new_arg)
                                            modifications.append((i, j, new_expr))
            if modifications:
                modified = True
                for i, j, new_expr in modifications:
                    expr.operands[i] = new_expr
                    expr.operands[j] = None
                expr.operands = [op for op in expr.operands if op is not None]
        if len(expr.operands) == 1:
            return simplify(expr.operands[0])
        else:
            return type(expr)(*list(map(simplify, expr.operands)))
    elif isinstance(expr, Not):
        return Not(simplify(expr.operand))
    else:
        return expr


COMPOSITIONS = {
    And: [
        (lambda x, y: Bottom() if x == ~y else None),
        (lambda x, _: Bottom() if x == Bottom() else None),
        (lambda x, y: Bottom() if _unsat(x, y) else None),
        (lambda x, y: x if x == y else None),
    ],
    Or: [
        lambda x, y: Top() if x == ~y else None,
        lambda x, _: Top() if x == Top() else None,
        (lambda x, y: x if x == y else None),
    ],
}


def _unsat(x: Expression, y: Expression) -> bool:
    if isinstance(x, Term) and isinstance(y, Term):
        if x.operands[0] == y.operands[0]:
            xp = x.predicate
            yp = y.predicate
            xv = x.operands[1]
            yv = y.operands[1]
            if xp == "<" and yp == ">":
                if xv <= yv:
                    return True
            elif xp == "<" and yp == ">=":
                if xv < yv:
                    return True
            elif xp == "<=" and yp == ">":
                if xv < yv:
                    return True
            elif xp == "<=" and yp == ">=":
                if xv < yv:
                    return True
            elif xp == "in" and yp == "in":
                if xv == UniversalSet() or yv == UniversalSet():
                    return False
                if not set(xv).intersection(set(yv)):
                    return True
    return False


def compose_operators(boolean_op, op1, v1, op2, v2) -> Optional[Tuple]:
    rev_op_map = {v: k for k, v in OPS.items()}
    if not (op1 in rev_op_map and op2 in rev_op_map):
        return None
    op1 = rev_op_map[op1]
    op2 = rev_op_map[op2]
    if boolean_op == And:
        if op1 == operator.__lt__ and op2 == operator.__lt__:
            return operator.__lt__, min(v1, v2)
        elif op1 == operator.__le__ and op2 == operator.__le__:
            return operator.__le__, min(v1, v2)
        elif op1 == operator.__lt__ and op2 == operator.__le__:
            if v1 <= v2:
                return operator.__lt__, v1
            else:
                return operator.__le__, v2
        elif op1 == operator.__le__ and op2 == operator.__lt__:
            if v2 <= v1:
                return operator.__lt__, v2
            else:
                return operator.__le__, v1
        elif op1 == operator.__gt__ and op2 == operator.__gt__:
            return operator.__gt__, max(v1, v2)
        elif op1 == operator.__ge__ and op2 == operator.__ge__:
            return operator.__ge__, max(v1, v2)
        elif op1 == operator.__gt__ and op2 == operator.__ge__:
            if v1 >= v2:
                return operator.__gt__, v1
            else:
                return operator.__ge__, v2
        elif op1 == operator.__ge__ and op2 == operator.__gt__:
            if v2 >= v1:
                return operator.__gt__, v2
            else:
                return operator.__ge__, v1
        elif op1 == member_of and op2 == member_of:
            if v1 == UniversalSet():
                return member_of, v2
            elif v2 == UniversalSet():
                return member_of, v1
            else:
                return member_of, list(set(v1).intersection(v2))
    elif boolean_op == Or:
        if op1 == operator.__lt__ and op2 == operator.__lt__:
            return operator.__lt__, max(v1, v2)
        elif op1 == operator.__le__ and op2 == operator.__le__:
            return operator.__le__, max(v1, v2)
        elif op1 == operator.__lt__ and op2 == operator.__le__:
            if v1 <= v2:
                return operator.__le__, v2
            else:
                return operator.__lt__, v1
        elif op1 == operator.__le__ and op2 == operator.__lt__:
            if v2 <= v1:
                return operator.__le__, v1
            else:
                return operator.__lt__, v2
        elif op1 == operator.__gt__ and op2 == operator.__gt__:
            return operator.__gt__, min(v1, v2)
        elif op1 == operator.__ge__ and op2 == operator.__ge__:
            return operator.__ge__, min(v1, v2)
        elif op1 == operator.__gt__ and op2 == operator.__ge__:
            if v1 >= v2:
                return operator.__ge__, v2
            else:
                return operator.__gt__, v1
        elif op1 == operator.__ge__ and op2 == operator.__gt__:
            if v2 >= v1:
                return operator.__ge__, v1
            else:
                return operator.__gt__, v2
        elif op1 == member_of and op2 == member_of:
            if v1 == UniversalSet() or v2 == UniversalSet():
                return member_of, UniversalSet()
            return member_of, list(set(v1).union(v2))


def to_dnf(expr: Expression) -> Expression:
    expr = deepcopy(expr)
    expr = eliminate_implications(expr)
    expr = move_not_inwards(expr)
    expr = distribute_and_over_or(expr)
    return expr
