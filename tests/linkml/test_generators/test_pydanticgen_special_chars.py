"""
Tests for Pydantic generator handling of special characters in field and class names
"""

import pytest

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.pydanticgen.pydanticgen import _is_valid_python_name, make_valid_python_identifier
from linkml.validator import Validator
from linkml.validator.plugins import PydanticValidationPlugin

pytestmark = pytest.mark.pydanticgen


def test_make_valid_python_identifier():
    """Test the helper function for creating valid Python identifiers"""
    assert make_valid_python_identifier("@id") == "id"
    assert make_valid_python_identifier("@type") == "type"
    assert make_valid_python_identifier("@context") == "context"
    assert make_valid_python_identifier("my-field") == "my_field"
    assert make_valid_python_identifier("field:name") == "field_name"
    assert make_valid_python_identifier("123field") == "field_123field"
    assert make_valid_python_identifier("class") == "class_"
    assert make_valid_python_identifier("def") == "def_"
    assert make_valid_python_identifier("") == "field"
    assert make_valid_python_identifier("___") == "field"
    assert make_valid_python_identifier("@@@") == "field"


def test_pydantic_generation_with_at_symbols():
    """Test that Pydantic code generation works with @ symbols in slot names"""
    schema_text = """
    id: test_schema
    name: test_schema
    imports:
      - linkml:types
    default_range: string

    classes:
      Entity:
        slots:
          - "@id"
          - "@type"

    slots:
      "@id":
        identifier: true
        required: true
      "@type":
        designates_type: true
        range: string
    """
    generator = PydanticGenerator(schema_text)
    code = generator.serialize()
    compile(code, "test", "exec")
    assert 'alias="@id"' in code
    assert 'alias="@type"' in code
    assert "id:" in code
    assert "type:" in code
    assert "@id:" not in code
    assert "@type:" not in code


def test_validation_with_at_symbols():
    """Test that validation works with @ symbols in data"""
    schema_text = """
    id: test_schema
    name: test_schema
    imports:
      - linkml:types
    default_range: string

    classes:
      Container:
        tree_root: true
        attributes:
          "@graph":
            multivalued: true
            inlined_as_list: true
            range: Entity
      Entity:
        slots:
          - "@id"
          - "@type"

    slots:
      "@id":
        identifier: true
        required: true
      "@type":
        designates_type: true
        range: string
    """
    test_data = {"@graph": [{"@id": "entity1", "@type": "Entity"}]}
    validator = Validator(schema=schema_text, validation_plugins=[PydanticValidationPlugin()])
    report = validator.validate(test_data)
    assert len(report.results) == 0, f"Validation failed: {report.results}"


def test_validation_with_python_field_names():
    """Test that validation also works with Python-style field names (thanks to aliases)"""
    schema_text = """
    id: test_schema
    name: test_schema
    imports:
      - linkml:types
    default_range: string

    classes:
      Container:
        tree_root: true
        attributes:
          "@graph":
            multivalued: true
            inlined_as_list: true
            range: Entity
      Entity:
        slots:
          - "@id"
          - "@type"

    slots:
      "@id":
        identifier: true
        required: true
      "@type":
        designates_type: true
        range: string
    """
    test_data = {"graph": [{"id": "entity1", "type": "Entity"}]}
    validator = Validator(schema=schema_text, validation_plugins=[PydanticValidationPlugin()])
    report = validator.validate(test_data)
    assert len(report.results) == 0, f"Validation failed: {report.results}"


# --- Tests for _is_valid_python_name ---


@pytest.mark.parametrize(
    "name, expected",
    [
        ("person", True),
        ("MyClass", True),
        ("_private", True),
        ("3DModel", False),
        ("Per-son", False),
        ("Per!son", False),
        ("def", False),
        ("class", False),
        ("in", False),
    ],
)
def test_is_valid_python_name(name: str, expected: bool):
    assert _is_valid_python_name(name) is expected


# --- Tests for invalid class names ---


@pytest.mark.parametrize("class_name", ["3DModel", "Per-son", "Per!son"])
def test_invalid_class_name_without_alias_raises(class_name):
    """Classes with invalid Python names and no alias should raise ValueError."""
    schema_text = f"""
    id: test_schema
    name: test_schema
    imports:
      - linkml:types
    default_range: string

    classes:
      {class_name}:
        attributes:
          name:
            range: string
    """
    with pytest.raises(ValueError, match="not a valid Python identifier"):
        PydanticGenerator(schema_text).serialize()


@pytest.mark.parametrize(
    "class_name, class_alias",
    [
        ("3DModel", "ThreeDModel"),
        ("Per-son", "Person"),
        ("my-class", "MyClass"),
    ],
)
def test_class_name_with_alias(class_name, class_alias):
    """Classes with invalid Python names but valid aliases should use the alias."""
    schema_text = f"""
    id: test_schema
    name: test_schema
    imports:
      - linkml:types
    default_range: string

    classes:
      {class_name}:
        alias: {class_alias}
        attributes:
          name:
            range: string
    """
    generator = PydanticGenerator(schema_text)
    code = generator.serialize()
    # The generated code should compile and use the alias as the class name
    compile(code, "test", "exec")
    assert f"class {class_alias}" in code


@pytest.mark.parametrize(
    "class_name, bad_alias",
    [
        ("3DModel", "3DAlias"),
        ("Per-son", "Per-son-alias"),
    ],
)
def test_class_name_with_invalid_alias_raises(class_name, bad_alias):
    """Classes with invalid names AND invalid aliases should raise ValueError."""
    schema_text = f"""
    id: test_schema
    name: test_schema
    imports:
      - linkml:types
    default_range: string

    classes:
      {class_name}:
        alias: {bad_alias}
        attributes:
          name:
            range: string
    """
    with pytest.raises(ValueError, match="not a valid Python identifier"):
        PydanticGenerator(schema_text).serialize()
