"""Tests of the linter's range-checking rules."""

import pytest
from linkml_runtime.utils.schemaview import SchemaView

from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel
from linkml.linter.linter import LinterProblem
from linkml.linter.rules import NoUndeclaredRangesRule


def check_schema(test_schema: str) -> list[LinterProblem]:
    """Check a schema using the NoUndeclaredRangesRule linter.

    :param test_schema: schema to test, as a string
    :type test_schema: str
    :return: list of linting problems discovered
    :rtype: list[LinterProblem]
    """
    schema_view = SchemaView(test_schema)
    config = RuleConfig(level=RuleLevel.error.text)

    rule = NoUndeclaredRangesRule(config)
    return list(rule.check(schema_view, fix=False))


@pytest.mark.parametrize("range_def", ["integer", "SomeClass", "SomeEnum"])
def test_declared_range_type_class_enum(range_def):
    """Test that declaring a defined class, type, or enum as a range does not throw an error."""
    schema_start = """id: http://example.org/test_undeclared_ranges
slots:
  some_slot:"""
    range_declaration = f"    range: {range_def}"
    schema_end = """

classes:
  SomeClass:
    slots:
      - some_slot

enums:
  SomeEnum:

types:
  integer:
"""
    test_schema = "\n".join([schema_start, range_declaration, schema_end])
    problems = check_schema(test_schema)
    assert not problems


@pytest.mark.parametrize("range_def", ["integer", "SomeClass", "SomeEnum"])
def test_declared_default_range_type_class_enum(range_def) -> None:
    """Test that declaring a default_range using a defined type/class/enum does not throw an error.

    'some_slot' will have the default range.
    """
    schema_start = "id: http://example.org/test_undeclared_ranges"
    range_declaration = f"default_range: {range_def}"
    schema_end = """slots:
  some_slot:

classes:
  SomeClass:
    slots:
      - some_slot

enums:
  SomeEnum:

types:
  integer:
"""
    test_schema = "\n".join([schema_start, range_declaration, schema_end])
    problems = check_schema(test_schema)
    assert not problems


def test_missing_default_range_no_undeclared_ranges() -> None:
    """Test that a schema with no default_range but where every entity has a specified range does not throw an error."""
    test_schema = """id: http://example.org/test_undeclared_ranges

slots:
  truth:
    range: bool
  some_float:
    range: float
  some_int:
    range: integer
  some_string:
    range: string

classes:
  SomeClass:
    slots:
      - truth
      - some_float
      - some_int
      - some_string

types:
  bool:
  float:
  integer:
  string:
"""
    problems = check_schema(test_schema)
    assert not problems


def test_missing_default_range_undeclared_ranges() -> None:
    """Test that a schema with no default_range and entities lacking a range value throws an error.

    'some_int' and 'some_string' should default to the default range, but the default range is not defined.
    """

    test_schema = """id: http://example.org/test_undeclared_ranges

slots:
  truth:
    range: bool
  some_float:
    range: float
  some_int:
  some_string:

classes:
  SomeClass:
    slots:
      - truth
      - some_float
      - some_int
      - some_string

types:
  bool:
  float:
  integer:
  string:
"""
    problems = check_schema(test_schema)
    assert len(problems) == 2

    assert problems[0].message == "Class 'SomeClass' slot 'some_int' range 'None' is not defined."
    assert problems[1].message == "Class 'SomeClass' slot 'some_string' range 'None' is not defined."


def test_default_range_type_not_defined_default_unused() -> None:
    """Test that declaring a default_range with an undefined type throws an error.

    The default range is not used in the test schema.
    """

    test_schema = """id: http://example.org/test_undeclared_ranges
default_range: integer

slots:
  some_string:
    range: string

classes:
  SomeClass:
    slots:
      - some_string

types:
  string:
"""
    problems = check_schema(test_schema)

    assert len(problems) == 1
    assert problems[0].message == "Schema default_range 'integer' is not defined."


def test_default_range_type_not_defined_default_used() -> None:
    """Test that declaring a default_range with an undefined type throws an error.

    The default range is used in the test schema.
    """
    test_schema = """id: http://example.org/test_undeclared_ranges

default_range: made_up

slots:
  some_string:
    range: string
  some_integer:

classes:
  SomeClass:
    slots:
      - some_string
      - some_integer

types:
  string:
"""
    problems = check_schema(test_schema)

    assert len(problems) == 2
    assert problems[0].message == "Schema default_range 'made_up' is not defined."
    assert problems[1].message == "Class 'SomeClass' slot 'some_integer' range 'made_up' is not defined."


def test_undeclared_ranges():
    """Test that declaring a range that does not appear elsewhere in the schema throws an error."""

    test_schema = """id: http://example.org/test_undeclared_ranges
slots:
  some_slot:
    range: integer

classes:
  SomeClass:
    slots:
      - some_slot
"""
    problems = check_schema(test_schema)

    assert len(problems) == 1
    assert problems[0].message == "Class 'SomeClass' slot 'some_slot' range 'integer' is not defined."


def test_no_declared_range_Any() -> None:
    """Test that it is possible to set a range to 'Any' without specifying what the 'Any' is.

    N.b. all tests that use `linkml:Any` in combination with `any_of` and `exactly_one_of` rely on
    the underlying SchemaView functionality being correctly implemented.
    """
    test_schema = """id: http://example.org/test_undeclared_ranges

slots:
  some_slot:
    range: Any

classes:
  Any:
    class_uri: linkml:Any

  SomeClass:
    slots:
      - some_slot
"""
    problems = check_schema(test_schema)
    assert not problems


@pytest.mark.parametrize("range_type", ["any_of", "exactly_one_of"])
def test_declared_ranges_Any(range_type: str) -> None:
    """Test that declaring an 'Any' range with defined types does not throw an error.

    The possible values for 'Any' are set in the `slot_usage` declaration.

    N.b. all tests that use `linkml:Any` in combination with `any_of` and `exactly_one_of` rely on
    the underlying SchemaView functionality being correctly implemented.
    """
    schema_start = """id: http://example.org/test_undeclared_ranges

slots:
  some_slot:

classes:
  Any:
    class_uri: linkml:Any

  SomeClass:
    slots:
      - some_slot
    slot_usage:
      some_slot:
        range: Any
"""

    range_declaration = f"        {range_type}:"
    schema_end = """
        - range: string
        - range: spreadsheet

types:
  string:
  spreadsheet:
"""
    test_schema = "".join([schema_start, range_declaration, schema_end])
    problems = check_schema(test_schema)
    assert not problems


@pytest.mark.parametrize("range_type", ["any_of", "exactly_one_of"])
def test_declared_ranges_Any_in_slots(range_type: str) -> None:
    """Test that declaring an 'Any' range with defined types does not throw an error.

    The possible values for 'Any' are set in the `slots` declaration.

    N.b. all tests that use `linkml:Any` in combination with `any_of` and `exactly_one_of` rely on
    the underlying SchemaView functionality being correctly implemented.
    """
    schema_start = """id: http://example.org/test_undeclared_ranges

slots:
  some_slot:
    range: Any
"""
    range_declaration = f"    {range_type}:"
    schema_end = """
    - range: string
    - range: spreadsheet

classes:
  Any:
    class_uri: linkml:Any

  SomeClass:
    slots:
      - some_slot

types:
  string:
  spreadsheet:
"""
    test_schema = "".join([schema_start, range_declaration, schema_end])
    problems = check_schema(test_schema)
    assert not problems


@pytest.mark.parametrize("range_type", ["any_of", "exactly_one_of"])
def test_undeclared_ranges_Any(range_type: str) -> None:
    """Test that declaring an 'Any' range with undefined throws an error.

    The possible values for 'Any' are set in the `slot_usage` declaration.

    N.b. all tests that use `linkml:Any` in combination with `any_of` and `exactly_one_of` rely on
    the underlying SchemaView functionality being correctly implemented.
    """
    schema_start = """id: http://example.org/test_undeclared_ranges

slots:
  some_slot:

classes:
  Any:
    class_uri: linkml:Any

  SomeClass:
    slots:
      - some_slot
    slot_usage:
      some_slot:
        range: Any
"""

    range_declaration = f"        {range_type}:"
    schema_end = """
        - range: string
        - range: spreadsheet

types:
  string:
"""
    test_schema = "".join([schema_start, range_declaration, schema_end])
    problems = check_schema(test_schema)
    assert len(problems) == 1
    assert problems[0].message == "Class 'SomeClass' slot 'some_slot' range 'spreadsheet' is not defined."


@pytest.mark.parametrize("range_type", ["any_of", "exactly_one_of"])
def test_undeclared_ranges_Any_in_slots(range_type: str) -> None:
    """Test that declaring an 'Any' range with undefined types throws an error.

    The possible values for 'Any' are set in the `slots` declaration.

    N.b. all tests that use `linkml:Any` in combination with `any_of` and `exactly_one_of` rely on
    the underlying SchemaView functionality being correctly implemented.
    """
    schema_start = """id: http://example.org/test_undeclared_ranges

slots:
  some_slot:
    range: Any
"""
    range_declaration = f"    {range_type}:"
    schema_end = """
    - range: string
    - range: spreadsheet

classes:
  Any:
    class_uri: linkml:Any

  SomeClass:
    slots:
      - some_slot

types:
  string:
"""
    test_schema = "".join([schema_start, range_declaration, schema_end])
    problems = check_schema(test_schema)
    assert len(problems) == 1
    assert problems[0].message == "Class 'SomeClass' slot 'some_slot' range 'spreadsheet' is not defined."
