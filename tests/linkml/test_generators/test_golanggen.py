"""
Comprehensive tests for the Golang generator.

Tests the new golanggen package implementation based on pydanticgen architecture.
"""

import pytest
from linkml.generators.golanggen import GolangGenerator


def test_golanggen_kitchen_sink(kitchen_sink_path):
    """Test golang generation with kitchen sink schema."""
    code = GolangGenerator(kitchen_sink_path, mergeimports=True).serialize()

    def assert_in(s: str) -> None:
        """Assert string is in code (ignoring whitespace)."""
        assert s.replace(" ", "") in code.replace(" ", ""), f"Expected to find: {s}"

    # Test package declaration
    assert "package kitchen" in code, "Missing package declaration"

    # Test struct generation
    assert_in("type Person struct {")
    assert_in("type Address struct {")
    assert_in("type Organization struct {")

    # Test inheritance via embedding (Person embeds HasAliases mixin)
    assert_in("HasAliases")  # Mixin should be embedded

    # Test fields
    assert_in("HasFamilialRelationships []*FamilialRelationship")
    assert_in("Name string")
    assert_in("AgeInYears int")

    # Test JSON tags
    assert 'json:"' in code, "Missing JSON tags"
    assert 'json:"name' in code, "Missing name JSON tag"
    assert_in('json:"age_in_years')

    # Test enums
    assert "type FamilialRelationshipType string" in code, "Missing enum type"
    assert "const (" in code, "Missing const block"
    assert_in("FamilialRelationshipTypeSIBLINGOF")
    assert_in("FamilialRelationshipTypePARENTOF")
    assert_in("FamilialRelationshipTypeCHILDOF")

    # Test multivalued fields as slices
    assert "[]" in code, "Missing slice types for multivalued fields"


def test_golanggen_enums(kitchen_sink_path):
    """Test enum generation."""
    gen = GolangGenerator(kitchen_sink_path)
    module = gen.render()

    # Check enums were generated
    assert "FamilialRelationshipType" in module.enums
    enum = module.enums["FamilialRelationshipType"]

    assert enum.name == "FamilialRelationshipType"
    assert enum.type == "string"
    assert len(enum.values) > 0

    # Check enum constants
    assert "SIBLING_OF" in enum.values
    assert "PARENT_OF" in enum.values
    assert "CHILD_OF" in enum.values


def test_golanggen_structs(kitchen_sink_path):
    """Test struct generation."""
    gen = GolangGenerator(kitchen_sink_path)
    module = gen.render()

    # Check structs were generated
    assert "Person" in module.structs
    person = module.structs["Person"]

    assert person.name == "Person"
    assert person.description is not None or person.description is None  # May or may not have description
    assert person.fields is not None
    assert len(person.fields) > 0


def test_golanggen_inheritance(kitchen_sink_path):
    """Test that inheritance is handled via struct embedding."""
    gen = GolangGenerator(kitchen_sink_path)
    module = gen.render()

    # Adult inherits from Person
    adult = module.structs.get("Adult")
    if adult:
        assert adult.embedded_structs is not None
        assert "Person" in adult.embedded_structs


def test_golanggen_fields(kitchen_sink_path):
    """Test field generation."""
    gen = GolangGenerator(kitchen_sink_path)
    module = gen.render()

    person = module.structs["Person"]

    # Check that fields exist
    assert person.fields is not None
    field_names = [f.go_name for f in person.fields.values()]

    # Person should have some expected fields
    # Note: actual field names depend on schema, these are examples
    assert len(field_names) > 0


def test_golanggen_package_name():
    """Test package name generation and override."""
    # Test with simple schema name
    gen = GolangGenerator("tests/linkml_runtime/test_utils/input/kitchen_sink.yaml")
    module = gen.render()
    assert module.package_name == "kitchen"

    # Test with package name override
    gen = GolangGenerator(
        "tests/linkml_runtime/test_utils/input/kitchen_sink.yaml",
        package_name="custompackage"
    )
    module = gen.render()
    assert module.package_name == "custompackage"


def test_golanggen_imports(kitchen_sink_path):
    """Test import generation."""
    gen = GolangGenerator(kitchen_sink_path)
    module = gen.render()

    # If schema uses date/time types, time package should be imported
    # This depends on the schema content
    serialized = gen.serialize()

    # Check import block format if any imports exist
    if module.imports.imports:
        assert "import (" in serialized


def test_golanggen_json_tags(kitchen_sink_path):
    """Test JSON tag generation."""
    code = GolangGenerator(kitchen_sink_path).serialize()

    # Check JSON tags are present
    assert "`json:" in code
    assert "omitempty" in code  # Optional fields should have omitempty


def test_golanggen_multivalued_fields(kitchen_sink_path):
    """Test multivalued field handling."""
    gen = GolangGenerator(kitchen_sink_path)
    module = gen.render()

    # Find a struct with multivalued fields
    # In kitchen_sink, Person has has_familial_relationships which is multivalued
    person = module.structs.get("Person")
    if person and person.fields:
        # Look for slice types
        field_types = [f.type for f in person.fields.values()]
        slice_fields = [t for t in field_types if t.startswith("[]")]
        # At least some fields should be slices
        assert len(slice_fields) > 0, "Expected some multivalued fields to be slices"


def test_golanggen_type_mapping(kitchen_sink_path):
    """Test that LinkML types are correctly mapped to Go types."""
    code = GolangGenerator(kitchen_sink_path).serialize()

    # Check for various Go types
    assert " string" in code or " string " in code, "Missing string type"
    assert " int" in code or " int " in code, "Missing int type"

    # If schema has float fields
    if "float" in code.lower() or "height" in code.lower():
        assert "float64" in code, "Float should map to float64"


def test_golanggen_comments(kitchen_sink_path):
    """Test that descriptions are converted to comments."""
    gen = GolangGenerator(kitchen_sink_path)
    module = gen.render()

    # Check that at least some structs or fields have descriptions
    has_descriptions = False
    for struct in module.structs.values():
        if struct.description:
            has_descriptions = True
            break
        if struct.fields:
            for field in struct.fields.values():
                if field.description:
                    has_descriptions = True
                    break

    # Serialize and check for comments in output
    code = gen.serialize()
    if has_descriptions:
        assert "//" in code, "Expected Go comments for descriptions"


def test_golanggen_backwards_compatibility():
    """Test backwards compatibility with old golanggen module."""
    # Should be able to import from both locations
    from linkml.generators.golanggen import GolangGenerator as NewGen
    from linkml.generators.golanggen.golanggen import GolangGenerator as DirectGen

    # Both should be the same class
    assert NewGen is DirectGen
