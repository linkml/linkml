"""
Tests for honoring per-class ``extra_slots`` metadata in the Pydantic generator.

LinkML's metamodel lets a class declare ``extra_slots: {allowed: true}`` to opt
in to open-world semantics (see https://github.com/linkml/linkml/issues/1341).
These tests verify that 'gen-pydantic' honors the per-class setting, matching
behavior already seen in 'gen-json-schema'.
"""

import pytest

from linkml.generators.pydanticgen import PydanticGenerator
from linkml_runtime.utils.compile_python import compile_python

SCHEMA_MIXED = """
id: https://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
default_prefix: ex
default_range: string

types:
  string:
    uri: xsd:string
    base: str

classes:
  StrictPerson:
    description: Person with closed-world semantics (default)
    attributes:
      name:
        required: true

  FlexiblePerson:
    description: Person with open-world semantics via extra_slots
    extra_slots:
      allowed: true
    attributes:
      name:
        required: true

  ExplicitlyClosedPerson:
    description: Person explicitly closed via extra_slots
    extra_slots:
      allowed: false
    attributes:
      name:
        required: true
"""


@pytest.fixture
def schema_file(tmp_path):
    p = tmp_path / "schema.yaml"
    p.write_text(SCHEMA_MIXED)
    return str(p)


class TestPydanticGeneratorPerClassExtraSlots:
    """PydanticGenerator honors per-class ``extra_slots.allowed``."""

    def test_default_extra_fields_unchanged(self, schema_file):
        """The generator-wide default is still ``forbid``."""
        gen = PydanticGenerator(schema_file)
        assert gen.extra_fields == "forbid"

    def test_strict_class_has_no_per_class_override(self, schema_file):
        code = PydanticGenerator(schema_file).serialize()
        # StrictPerson should not have its own model_config override
        strict_block = _extract_class_block(code, "StrictPerson")
        assert "model_config" not in strict_block

    def test_open_class_emits_extra_allow(self, schema_file):
        code = PydanticGenerator(schema_file).serialize()
        flex_block = _extract_class_block(code, "FlexiblePerson")
        assert 'extra = "allow"' in flex_block

    def test_explicitly_closed_class_emits_extra_forbid(self, schema_file):
        code = PydanticGenerator(schema_file).serialize()
        closed_block = _extract_class_block(code, "ExplicitlyClosedPerson")
        assert 'extra = "forbid"' in closed_block

    def test_runtime_open_class_accepts_extras(self, schema_file):
        """Compile and verify that ``extra_slots.allowed=true`` enables extras at runtime."""
        code = PydanticGenerator(schema_file).serialize()
        module = compile_python(code)
        instance = module.FlexiblePerson(name="Bob", extra_field="value")
        assert instance.name == "Bob"
        assert instance.extra_field == "value"

    def test_runtime_strict_class_rejects_extras(self, schema_file):
        """Default closed-world classes still reject extras at runtime."""
        from pydantic import ValidationError

        code = PydanticGenerator(schema_file).serialize()
        module = compile_python(code)
        with pytest.raises(ValidationError):
            module.StrictPerson(name="Alice", extra_field="x")


def _extract_class_block(code: str, class_name: str) -> str:
    """Return the source block for ``class_name`` up to the next top-level class."""
    marker = f"class {class_name}("
    start = code.index(marker)
    rest = code[start + len(marker) :]
    next_class = rest.find("\nclass ")
    end = start + len(marker) + (next_class if next_class != -1 else len(rest))
    return code[start:end]
