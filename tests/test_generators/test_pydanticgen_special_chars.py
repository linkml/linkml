"""
Tests for Pydantic generator handling of special characters in field names
"""

import pytest

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.pydanticgen.pydanticgen import make_valid_python_identifier
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
