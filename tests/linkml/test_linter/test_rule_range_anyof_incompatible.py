"""Tests for the RangeAnyOfIncompatibleRule linter rule."""

import pytest

from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel
from linkml.linter.rules import RangeAnyOfIncompatibleRule
from linkml_runtime import SchemaView


def check_schema(schema_str: str) -> list:
    """Helper to run the rule against a schema string."""
    schema_view = SchemaView(schema_str)
    config = RuleConfig(level=RuleLevel.warning.text)
    rule = RangeAnyOfIncompatibleRule(config)
    return list(rule.check(schema_view, fix=False))


def test_range_string_anyof_enum_no_warning():
    """Test that range=string with any_of containing enum does NOT warn."""
    schema = """
id: http://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

slots:
  my_slot:
    range: string
    any_of:
      - range: MyEnum

enums:
  MyEnum:
    permissible_values:
      A:
      B:

classes:
  MyClass:
    slots:
      - my_slot
"""
    problems = check_schema(schema)
    assert len(problems) == 0


def test_range_class_without_identifier_anyof_string_warns():
    """Test that range=SomeClass (no identifier) with any_of string warns.

    A class without an identifier must be inlined, so it's an object type.
    """
    schema = """
id: http://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

slots:
  my_slot:
    range: SomeClass
    any_of:
      - range: string

classes:
  SomeClass:
    slots: []
  MyClass:
    slots:
      - my_slot
"""
    problems = check_schema(schema)
    assert len(problems) == 1
    assert "object" in problems[0].message
    assert "string" in problems[0].message


def test_range_class_with_identifier_anyof_string_no_warning():
    """Test that range=SomeClass (with identifier) with any_of string does NOT warn.

    A class with a string identifier is a string reference when not inlined.
    """
    schema = """
id: http://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

slots:
  id:
    identifier: true
  my_slot:
    range: SomeClass
    any_of:
      - range: string

classes:
  SomeClass:
    slots:
      - id
  MyClass:
    slots:
      - my_slot
"""
    problems = check_schema(schema)
    assert len(problems) == 0


def test_range_class_with_integer_identifier_anyof_integer_no_warning():
    """Test that range=SomeClass (with integer identifier) with any_of integer does NOT warn.

    A class with an integer identifier is an integer reference when not inlined.
    """
    schema = """
id: http://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

slots:
  id:
    identifier: true
    range: integer
  my_slot:
    range: SomeClass
    any_of:
      - range: integer

classes:
  SomeClass:
    slots:
      - id
  MyClass:
    slots:
      - my_slot
"""
    problems = check_schema(schema)
    assert len(problems) == 0


def test_range_class_with_integer_identifier_anyof_string_warns():
    """Test that range=SomeClass (with integer identifier) with any_of string DOES warn.

    A class with an integer identifier is an integer reference, not compatible with string.
    """
    schema = """
id: http://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

slots:
  id:
    identifier: true
    range: integer
  my_slot:
    range: SomeClass
    any_of:
      - range: string

classes:
  SomeClass:
    slots:
      - id
  MyClass:
    slots:
      - my_slot
"""
    problems = check_schema(schema)
    assert len(problems) == 1
    assert "integer" in problems[0].message
    assert "string" in problems[0].message


def test_range_class_without_identifier_anyof_integer_warns():
    """Test that range=SomeClass (no identifier) with any_of integer warns.

    A class without an identifier must be inlined (object), incompatible with integer.
    """
    schema = """
id: http://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

slots:
  my_slot:
    range: SomeClass
    any_of:
      - range: integer

classes:
  SomeClass:
    slots: []
  MyClass:
    slots:
      - my_slot
"""
    problems = check_schema(schema)
    assert len(problems) == 1
    assert "object" in problems[0].message
    assert "integer" in problems[0].message


def test_range_class_with_string_identifier_anyof_integer_warns():
    """Test that range=SomeClass (with string identifier) with any_of integer warns.

    A class with a string identifier is a string reference, incompatible with integer.
    """
    schema = """
id: http://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

slots:
  id:
    identifier: true
  my_slot:
    range: SomeClass
    any_of:
      - range: integer

classes:
  SomeClass:
    slots:
      - id
  MyClass:
    slots:
      - my_slot
"""
    problems = check_schema(schema)
    assert len(problems) == 1
    assert "string" in problems[0].message
    assert "integer" in problems[0].message


def test_range_class_explicit_inlined_anyof_string_warns():
    """Test that range=SomeClass with explicit inlined:true and any_of string warns.

    Even if the class has an identifier, explicit inlined:true means it's an object,
    which is incompatible with string.
    """
    schema = """
id: http://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

slots:
  id:
    identifier: true
  my_slot:
    range: SomeClass
    inlined: true
    any_of:
      - range: string

classes:
  SomeClass:
    slots:
      - id
  MyClass:
    slots:
      - my_slot
"""
    problems = check_schema(schema)
    assert len(problems) == 1
    assert "object" in problems[0].message
    assert "string" in problems[0].message


def test_no_range_no_warning():
    """Test that slots without range do NOT trigger warnings."""
    schema = """
id: http://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

slots:
  my_slot:
    any_of:
      - range: string
      - range: integer

classes:
  MyClass:
    slots:
      - my_slot
"""
    problems = check_schema(schema)
    assert len(problems) == 0


def test_no_anyof_no_warning():
    """Test that slots without any_of do NOT trigger warnings."""
    schema = """
id: http://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

slots:
  my_slot:
    range: string

classes:
  MyClass:
    slots:
      - my_slot
"""
    problems = check_schema(schema)
    assert len(problems) == 0


def test_mixed_anyof_warns_only_for_incompatible():
    """Test that mixed any_of warns only for incompatible options."""
    schema = """
id: http://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

slots:
  my_slot:
    range: string
    any_of:
      - range: MyEnum
      - range: integer
      - range: boolean

enums:
  MyEnum:
    permissible_values:
      A:
      B:

classes:
  MyClass:
    slots:
      - my_slot
"""
    problems = check_schema(schema)
    # Should warn for integer and boolean, not for MyEnum
    assert len(problems) == 2
    messages = [p.message for p in problems]
    assert any("integer" in m for m in messages)
    assert any("boolean" in m for m in messages)
    assert not any("MyEnum" in m for m in messages)


@pytest.mark.parametrize(
    "range_type,anyof_type,should_warn",
    [
        ("string", "integer", True),
        ("string", "boolean", True),
        ("integer", "string", True),
        ("integer", "boolean", True),
        ("boolean", "string", True),
        ("boolean", "integer", True),
        ("integer", "float", False),  # number compatible
        ("float", "integer", False),  # number compatible
        ("string", "string", False),  # same type
        ("integer", "integer", False),  # same type
    ],
)
def test_type_compatibility_matrix(range_type, anyof_type, should_warn):
    """Test the type compatibility matrix with parametrized inputs."""
    schema = f"""
id: http://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

slots:
  my_slot:
    range: {range_type}
    any_of:
      - range: {anyof_type}

classes:
  MyClass:
    slots:
      - my_slot
"""
    problems = check_schema(schema)
    if should_warn:
        assert len(problems) == 1, f"Expected warning for {range_type} vs {anyof_type}"
    else:
        assert len(problems) == 0, f"Expected no warning for {range_type} vs {anyof_type}"
