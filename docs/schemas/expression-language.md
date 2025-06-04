# Expression Language

The Expression Language is a domain-specific language (DSL) that allows for the evaluation of expressions with a syntax similar to Python. It provides a restricted subset of Python's features to ensure safe and controlled execution.

See the [inference documentation](../developers/inference) for details on how to use these at run time.

## Syntax

The Expression Language supports the following syntax elements:

### Literals

- Numbers: Integer and floating-point numbers are supported.
  - Examples: `42`, `3.14`
- Strings: String literals are enclosed in double quotes (`"`).
  - Example: `"Hello, world!"`
- Booleans: Boolean values are represented by `True` and `False`.
- None: The `None` value represents the absence of a value.

### Arithmetic Operations

- Addition: `+`
  - Example: `1 + 2`
- Subtraction: `-`
  - Example: `5 - 3`
- Multiplication: `*`
  - Example: `2 * 4`
- Division: `/`
  - Example: `10 / 2`
- Exponentiation: `^` or `**`
  - Example: `2^3` or `2**3`
- Bitwise XOR: `^`
  - Example: `5 ^ 3`

### Comparison Operations

- Equal to: `==`
  - Example: `x == y`
- Less than: `<`
  - Example: `x < y`
- Less than or equal to: `<=`
  - Example: `x <= y`
- Greater than: `>`
  - Example: `x > y`
- Greater than or equal to: `>=`
  - Example: `x >= y`

### Logical Operations

- Logical AND: `and`
  - Example: `x and y`
- Logical OR: `or`
  - Example: `x or y`
- Logical NOT: `not`
  - Example: `not x`

### Variables

Variables can be referenced by their names. They are resolved from the context in which the expression is evaluated.

- Example: `x + y`

If a variable is not defined or has a value of `None`, it will be treated as `None` in the expression.

### Functions

The Expression Language provides a set of built-in functions:

- `max(arg1, arg2, ...)`: Returns the maximum value among the arguments.
- `min(arg1, arg2, ...)`: Returns the minimum value among the arguments.
- `len(arg)`: Returns the length of a string or a list.
- `str(arg)`: Converts the argument to a string.
- `case(cond1, val1, cond2, val2, ..., default)`: Evaluates the conditions in order and returns the value associated with the first true condition. If no condition is true, the default value is returned.

### Attribute Access

Attributes of objects can be accessed using dot notation (`object.attribute`). Attribute access can be chained to navigate through nested objects.

- Example: `person.name`, `person.address.street`

When an attribute is accessed on a list, the operation is distributed over the elements of the list.

- Example: `persons.name` (returns a list of names)

### Conditional Expressions

Conditional expressions allow for the evaluation of different expressions based on a condition.

- Syntax: `<expression_if_true> if <condition> else <expression_if_false>`
- Example: `"Positive" if x > 0 else "Non-positive"`

### Operator Precedence

The Expression Language follows the same operator precedence rules as Python. Parentheses can be used to override the default precedence order.

## Limitations

The Expression Language has the following limitations:

- It does not support control flow statements such as loops or function definitions.
- It does not allow the use of certain potentially unsafe operations, such as `__import__`.
- It is designed for simple expressions and does not provide the full range of features available in Python.

## Examples

Here are a few examples of expressions in the Expression Language:

- `1 + 2 * 3`: Evaluates to `7`.
- `"Hello, " + "world!"`: Evaluates to `"Hello, world!"`.
- `x > 10 and y < 5`: Evaluates to `True` if `x` is greater than `10` and `y` is less than `5`, otherwise `False`.
- `max(x, y, z)`: Returns the maximum value among `x`, `y`, and `z`.
- `person.name`: Returns the value of the `name` attribute of the `person` object.
- `"Positive" if x > 0 else "Non-positive"`: Returns `"Positive"` if `x` is greater than `0`, otherwise returns `"Non-positive"`.

This documentation provides an overview of the Expression Language and its supported features. It is independent of any specific implementation or programming language.
