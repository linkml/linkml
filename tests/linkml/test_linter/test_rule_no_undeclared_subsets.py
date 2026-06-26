"""Tests of the linter's in_subset integrity rule."""

from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel
from linkml.linter.linter import LinterProblem
from linkml.linter.rules import NoUndeclaredSubsetsRule
from linkml_runtime.utils.schemaview import SchemaView


def check_schema(test_schema: str) -> list[LinterProblem]:
    """Check a schema using the NoUndeclaredSubsetsRule linter.

    :param test_schema: schema to test, as a string
    :type test_schema: str
    :return: list of linting problems discovered
    :rtype: list[LinterProblem]
    """
    schema_view = SchemaView(test_schema)
    config = RuleConfig(level=RuleLevel.error.text)

    rule = NoUndeclaredSubsetsRule(config)
    return list(rule.check(schema_view, fix=False))


def test_valid_in_subset() -> None:
    """in_subset that names a declared subset is valid."""
    test_schema = """id: http://example.org/test_subsets
name: test_subsets
subsets:
  a_subset:
    description: a declared subset
slots:
  member_slot:
    in_subset:
      - a_subset
"""
    assert not check_schema(test_schema)


def test_no_in_subset() -> None:
    """A slot with no in_subset produces no problems."""
    test_schema = """id: http://example.org/test_subsets
name: test_subsets
slots:
  plain_slot:
"""
    assert not check_schema(test_schema)


def test_undeclared_in_subset_on_slot() -> None:
    """in_subset naming an undeclared subset is an error."""
    test_schema = """id: http://example.org/test_subsets
name: test_subsets
slots:
  member_slot:
    in_subset:
      - made_up_subset
"""
    problems = check_schema(test_schema)
    assert len(problems) == 1
    assert problems[0].message == "Slot 'member_slot' asserts membership in undeclared subset 'made_up_subset'."


def test_undeclared_in_subset_on_class_and_enum() -> None:
    """in_subset on classes, enums, and permissible values is checked."""
    test_schema = """id: http://example.org/test_subsets
name: test_subsets
classes:
  SomeClass:
    in_subset:
      - missing_class_subset
enums:
  SomeEnum:
    in_subset:
      - missing_enum_subset
    permissible_values:
      VALUE:
        in_subset:
          - missing_pv_subset
"""
    messages = sorted(p.message for p in check_schema(test_schema))
    assert messages == [
        "Class 'SomeClass' asserts membership in undeclared subset 'missing_class_subset'.",
        "Enum 'SomeEnum' asserts membership in undeclared subset 'missing_enum_subset'.",
        "Enum 'SomeEnum' permissible value 'VALUE' asserts membership in undeclared subset 'missing_pv_subset'.",
    ]


def test_undeclared_in_subset_in_slot_usage() -> None:
    """in_subset asserted in a class's slot_usage is also checked."""
    test_schema = """id: http://example.org/test_subsets
name: test_subsets
slots:
  member_slot:
classes:
  SomeClass:
    slots:
      - member_slot
    slot_usage:
      member_slot:
        in_subset:
          - made_up_subset
"""
    problems = check_schema(test_schema)
    assert len(problems) == 1
    assert (
        problems[0].message
        == "Class 'SomeClass' slot_usage 'member_slot' asserts membership in undeclared subset 'made_up_subset'."
    )


def test_undeclared_in_subset_on_class_attributes() -> None:
    """in_subset on inline attributes is checked per class.

    Covers attributes that share a name across classes and an attribute that overrides
    a globally declared slot name. all_slots() de-duplicates these by name, so this
    guards against the rule silently skipping them.
    """
    test_schema = """id: http://example.org/test_subsets
name: test_subsets
slots:
  shared:
    in_subset:
      - missing_global
classes:
  A:
    attributes:
      shared:
        in_subset:
          - missing_in_a
  B:
    attributes:
      shared:
        in_subset:
          - missing_in_b
"""
    messages = sorted(p.message for p in check_schema(test_schema))
    assert messages == [
        "Class 'A' attribute 'shared' asserts membership in undeclared subset 'missing_in_a'.",
        "Class 'B' attribute 'shared' asserts membership in undeclared subset 'missing_in_b'.",
        "Slot 'shared' asserts membership in undeclared subset 'missing_global'.",
    ]
