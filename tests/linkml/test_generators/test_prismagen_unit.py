"""
Unit tests for Prisma generator components.

Tests individual functions and components without full schema generation.
"""

from linkml.generators.prisma.type_mappings import (
    PRISMA_RANGEMAP,
    get_prisma_modifiers,
    get_prisma_type,
    is_optional_field,
)
from linkml_runtime.linkml_model.meta import SlotDefinition


class TestTypeMappingScalars:
    """Test scalar type mapping."""

    def test_string_mapping(self):
        assert get_prisma_type("string") == "String"

    def test_integer_mapping(self):
        assert get_prisma_type("integer") == "Int"

    def test_boolean_mapping(self):
        assert get_prisma_type("boolean") == "Boolean"

    def test_float_mapping(self):
        assert get_prisma_type("float") == "Float"

    def test_double_mapping(self):
        assert get_prisma_type("double") == "Float"

    def test_decimal_mapping(self):
        assert get_prisma_type("decimal") == "Decimal"

    def test_date_mapping(self):
        assert get_prisma_type("date") == "DateTime"

    def test_datetime_mapping(self):
        assert get_prisma_type("datetime") == "DateTime"

    def test_time_mapping(self):
        """Time maps to String as Prisma has no Time type."""
        assert get_prisma_type("time") == "String"

    def test_json_mapping(self):
        assert get_prisma_type("json") == "Json"

    def test_uri_mapping(self):
        """URI types map to String."""
        assert get_prisma_type("uri") == "String"
        assert get_prisma_type("uriorcurie") == "String"

    def test_ncname_mapping(self):
        """NCName maps to String."""
        assert get_prisma_type("ncname") == "String"

    def test_bytes_mapping(self):
        assert get_prisma_type("bytes") == "Bytes"

    def test_unknown_type_passthrough(self):
        """Unknown types (like class names) pass through unchanged."""
        assert get_prisma_type("Person") == "Person"
        assert get_prisma_type("CustomType") == "CustomType"


class TestTypeMappingArrays:
    """Test array type mapping."""

    def test_string_array(self):
        assert get_prisma_type("string", is_multivalued=True) == "String[]"

    def test_integer_array(self):
        assert get_prisma_type("integer", is_multivalued=True) == "Int[]"

    def test_boolean_array(self):
        assert get_prisma_type("boolean", is_multivalued=True) == "Boolean[]"

    def test_array_disabled(self):
        """When use_scalar_arrays=False, no array suffix."""
        assert get_prisma_type("string", is_multivalued=True, use_scalar_arrays=False) == "String"


class TestPrismaModifiers:
    """Test Prisma field modifier generation."""

    def test_identifier_modifier(self):
        slot = SlotDefinition("id", range="string")
        mods = get_prisma_modifiers(slot, is_identifier=True)
        assert "@id" in mods

    def test_no_modifiers(self):
        slot = SlotDefinition("name", range="string")
        mods = get_prisma_modifiers(slot, is_identifier=False)
        assert mods == ""

    def test_unique_identifier_not_primary(self):
        """Slot marked as identifier but not the primary identifier gets @unique."""
        slot = SlotDefinition("email", range="string", identifier=True)
        mods = get_prisma_modifiers(slot, is_identifier=False)
        assert "@unique" in mods


class TestOptionalFields:
    """Test optional field detection."""

    def test_required_field(self):
        slot = SlotDefinition("name", range="string", required=True)
        assert not is_optional_field(slot, is_required=True)

    def test_optional_field(self):
        slot = SlotDefinition("nickname", range="string", required=False)
        assert is_optional_field(slot, is_required=False)

    def test_default_is_optional(self):
        """Fields without explicit required=True are optional."""
        slot = SlotDefinition("description", range="string")
        assert is_optional_field(slot, is_required=False)


class TestRangeMap:
    """Test PRISMA_RANGEMAP completeness."""

    def test_rangemap_has_common_types(self):
        """Verify RANGEMAP includes all common LinkML types."""
        expected_types = [
            "string",
            "integer",
            "boolean",
            "float",
            "double",
            "decimal",
            "date",
            "datetime",
            "time",
            "json",
            "uri",
            "uriorcurie",
            "ncname",
            "bytes",
        ]
        for linkml_type in expected_types:
            assert linkml_type in PRISMA_RANGEMAP, f"Missing type: {linkml_type}"

    def test_rangemap_values_are_valid_prisma_types(self):
        """Verify all RANGEMAP values are valid Prisma scalar types."""
        valid_prisma_types = {"String", "Int", "Boolean", "Float", "Decimal", "DateTime", "Json", "Bytes"}
        for prisma_type in PRISMA_RANGEMAP.values():
            assert prisma_type in valid_prisma_types, f"Invalid Prisma type: {prisma_type}"
