"""
meta-circular interpreter for evaluating python expressions

 - See `<https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string>`_
"""

import ast
import operator as op

# supported operators
from typing import Any

operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}
compare_operators = {ast.Eq: op.eq, ast.Lt: op.lt, ast.LtE: op.le, ast.Gt: op.gt, ast.GtE: op.ge}

def eval_conditional(*conds: list[tuple[bool, Any]]) -> Any:
    """
    Evaluate a collection of expression,value tuples, returing the first value whose expression is true

    >>> x= 40
    >>> eval_conditional((x < 25, 'low'),  (x > 25, 'high'), (True, 'low'))
    'high'

    :param subj:
    :return:
    """
    for is_true, val in conds:
        if is_true:
            return val


# (takes_list, func)
funcs = {'max': (True, max),
         'min': (True, min),
         'len': (True, len),
         'str': (False, str),
         'strlen': (False, len),
         'case': (False, eval_conditional)}


class UnsetValueException(Exception):
    pass


def eval_expr(expr: str, _distribute=True, **kwargs) -> Any:
    """
    Evaluates a given expression, with restricted syntax

    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0

    Variables:

    variables can be passed

    >>> eval_expr('{x} + {y}', x=1, y=2)
    3

    Nulls:

    - If a variable is enclosed in {}s then entire expression will eval to None if any variable is unset

    >>> assert eval_expr('{x} + {y}', x=None, y=2) is None

    Functions:

    - only a small set of functions are currently supported. All SPARQL functions will be supported in future

    >>> eval_expr('strlen("a" + "bc")')
    3

    Paths:

    - Expressions such as `person.name` can be used on objects to lookup by attribute/slot
    - Paths can be chained, e.g. `person.address.street`
    - Operations on lists are distributed, e.g `container.persons.name` will return a list of names
    - Similarly `strlen(container.persons.name)` will return a list whose members are the lengths of all names

    :param expr: expression to evaluate
    :param _distribute: if True, distribute operations over collections and return array
    :param kwargs: variables to substitute
    :return: result of evaluation
    """
    #if kwargs:
    #    expr = expr.format(**kwargs)
    if 'None' in expr:
        # TODO: do this as part of parsing
        return None
    else:
        try:
            return eval_(ast.parse(expr, mode='eval').body, kwargs, distribute=_distribute)
        except UnsetValueException:
            return None



def eval_(node, bindings=None, distribute=True):
    if bindings is None:
        bindings = {}
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Str):
        if 's' in vars(node):
            return node.s
        else:
            return node.value
    elif isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Name):
        return bindings.get(node.id)
    elif isinstance(node, ast.Subscript):
        if isinstance(node.slice, ast.Index):
            # required for python 3.7
            k = eval_(node.slice.value, bindings)
        else:
            k = eval_(node.slice, bindings)
        v = eval_(node.value, bindings)
        return v[k]
    elif isinstance(node, ast.Attribute):
        # e.g. for person.name, this returns the val of person
        v = eval_(node.value, bindings)
        # lookup attribute, potentially distributing the results over collections
        def _get(obj: Any, k: str, recurse=distribute) -> Any:
            if isinstance(obj, dict):
                # dicts are treated as collections; distribute results
                if recurse:
                    return [_get(e, k, False) for e in obj.values()]
                else:
                    return obj.get(k)
            elif isinstance(obj, list):
                # attributes are distributed over lists
                return [_get(e, k, False) for e in obj]
            elif obj is None:
                return None
            else:
                return getattr(obj, k)
        return _get(v, node.attr)
    elif isinstance(node, ast.List):
        return [eval_(x, bindings) for x in node.elts]
    elif isinstance(node, ast.Set):
        # sets are not part of the language; we use {x} as notation for x
        if len(node.elts) != 1:
            raise ValueError(f'The {{}} must enclose a single variable')
        e = node.elts[0]
        if not isinstance(e, ast.Name):
            raise ValueError(f'The {{}} must enclose a variable')
        v = eval_(e, bindings)
        if v is None:
            raise UnsetValueException(f'{e} is not set')
        else:
            return v
    elif isinstance(node, ast.Tuple):
        return tuple([eval_(x, bindings) for x in node.elts])
    elif isinstance(node, ast.Dict):
        return {eval_(k, bindings): eval_(v, bindings) for k, v in zip(node.keys, node.values)}
    elif isinstance(node, ast.Compare):  # <left> <operator> <right>
        if len(node.ops) != 1:
            raise ValueError(f'Must be exactly one op in {node}')
        if type(node.ops[0]) not in compare_operators:
            raise NotImplementedError(f'Not implemented: {node.ops[0]} in {node}')
        py_op = compare_operators[type(node.ops[0])]
        if len(node.comparators) != 1:
            raise ValueError(f'Must be exactly one comparator in {node}')
        right = node.comparators[0]
        return py_op(eval_(node.left, bindings), eval_(right, bindings))
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left, bindings), eval_(node.right, bindings))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand, bindings))
    #elif isinstance(node, ast.Match):
    #    # implementing this would restrict python version to 3.10
    #    # https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
    #    raise NotImplementedError(f'Not supported')
    elif isinstance(node, ast.IfExp):
        if eval_(node.test, bindings):
            return eval_(node.body, bindings)
        else:
            return eval_(node.orelse, bindings)
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            fn = node.func.id
            if fn in funcs:
                takes_list, func = funcs[fn]
                args = [eval_(x, bindings) for x in node.args]
                if isinstance(args[0], list) and not takes_list:
                    return [func(*[x]+args[1:]) for x in args[0]]
                else:
                    return func(*args)
        raise NotImplementedError(f'Call {node.func} not implemented. node = {node}')
    else:
        raise TypeError(node)
