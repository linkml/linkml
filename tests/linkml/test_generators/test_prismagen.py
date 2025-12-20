"""
Integration tests for Prisma generator.

Tests full pipeline with minimal schemas using SchemaBuilder.
"""

import pytest
from linkml_runtime import SchemaView

from linkml.generators.prismagen import PrismaGenerator, prepare_prisma_enums, prepare_prisma_models
from linkml.transformers.relmodel_transformer import RelationalModelTransformer
from linkml.utils.schema_builder import SchemaBuilder


class TestPrismaBasicGeneration:
    """Test basic schema generation."""

    def test_minimal_schema(self):
        """Test generation with a minimal schema."""
        sb = SchemaBuilder("test")
        sb.add_slot("id", identifier=True, range="string")
        sb.add_slot("name", range="string", required=True)
        sb.add_class("Person", slots=["id", "name"])
        sb.add_defaults()

        gen = PrismaGenerator(sb.schema)
        output = gen.serialize()

        assert "generator client {" in output
        assert "datasource db {" in output
        assert 'provider = "postgresql"' in output
        assert "model Person {" in output

    def test_schema_with_description(self):
        """Test that schema description is included."""
        sb = SchemaBuilder("test")
        sb.schema.description = "A test schema"
        sb.add_slot("id", identifier=True)
        sb.add_class("Person", slots=["id"])
        sb.add_defaults()

        gen = PrismaGenerator(sb.schema)
        output = gen.serialize()

        assert "A test schema" in output


class TestPrismaTypes:
    """Test type mapping."""

    def test_basic_types(self):
        """Test basic LinkML type mappings."""
        sb = SchemaBuilder("test")
        sb.add_slot("id", identifier=True, range="string")
        sb.add_slot("name", range="string")
        sb.add_slot("age", range="integer")
        sb.add_slot("active", range="boolean")
        sb.add_class("Person", slots=["id", "name", "age", "active"])
        sb.add_defaults()

        gen = PrismaGenerator(sb.schema)
        output = gen.serialize()

        assert "String" in output
        assert "Int" in output
        assert "Boolean" in output


class TestPrismaEnums:
    """Test enum generation."""

    def test_basic_enum(self):
        """Test basic enum generation."""
        sb = SchemaBuilder("test")
        sb.add_slot("id", identifier=True)
        sb.add_slot("status", range="StatusEnum")
        sb.add_enum("StatusEnum", permissible_values=["ACTIVE", "INACTIVE"])
        sb.add_class("Person", slots=["id", "status"])
        sb.add_defaults()

        gen = PrismaGenerator(sb.schema)
        output = gen.serialize()

        assert "enum StatusEnum {" in output
        assert "ACTIVE" in output
        assert "INACTIVE" in output


class TestPrismaDatasourceProviders:
    """Test different datasource providers."""

    @pytest.mark.parametrize("provider", ["postgresql", "mysql", "sqlite", "cockroachdb"])
    def test_datasource_provider(self, provider):
        """Test different database providers."""
        sb = SchemaBuilder("test")
        sb.add_slot("id", identifier=True)
        sb.add_class("Person", slots=["id"])
        sb.add_defaults()

        gen = PrismaGenerator(sb.schema, datasource_provider=provider)
        output = gen.serialize()

        assert f'provider = "{provider}"' in output


class TestPrismaModelPreparation:
    """Test model preparation function independently."""

    def test_prepare_models_basic(self):
        """Test prepare_prisma_models with basic schema."""
        sb = SchemaBuilder("test")
        sb.add_slot("id", identifier=True, range="string")
        sb.add_slot("name", range="string")
        sb.add_class("Person", slots=["id", "name"])
        sb.add_defaults()

        sv = SchemaView(sb.schema)
        transformer = RelationalModelTransformer(sv)
        tr_result = transformer.transform()

        models = prepare_prisma_models(tr_result.schema, sv)

        assert len(models) >= 1
        person_model = next((m for m in models if m.name == "Person"), None)
        assert person_model is not None


class TestPrismaRelations:
    """Test relation generation."""

    def test_relation_with_fk_field(self):
        """Test that relations generate proper FK fields."""
        sb = SchemaBuilder("test")
        sb.add_slot("uuid", identifier=True, range="string")
        sb.add_slot("name", range="string")
        sb.add_slot("study", range="Study")
        sb.add_class("Study", slots=["uuid", "name"])
        sb.add_class("Experiment", slots=["uuid", "name", "study"])
        sb.add_defaults()

        gen = PrismaGenerator(sb.schema)
        output = gen.serialize()

        # Check FK field is generated
        assert "studyId" in output
        # Check relation references correct ID field
        assert "references: [uuid]" in output
        # Check reverse relation
        assert "Experiment[]" in output

    def test_camelcase_field_names(self):
        """Test that field names are converted to camelCase."""
        sb = SchemaBuilder("test")
        sb.add_slot("id", identifier=True, range="string")
        sb.add_slot("full_name", range="string")
        sb.add_slot("created_at", range="datetime")
        sb.add_class("Person", slots=["id", "full_name", "created_at"])
        sb.add_defaults()

        gen = PrismaGenerator(sb.schema)
        output = gen.serialize()

        assert "fullName" in output
        assert "createdAt" in output

    def test_abstract_class_skipped(self):
        """Test that abstract classes are not rendered as models."""
        sb = SchemaBuilder("test")
        sb.add_slot("id", identifier=True, range="string")
        sb.add_class("Entity", slots=["id"])
        sb.schema.classes["Entity"].abstract = True
        sb.add_class("Person", slots=["id"])
        sb.schema.classes["Person"].is_a = "Entity"
        sb.add_defaults()

        gen = PrismaGenerator(sb.schema)
        output = gen.serialize()

        # Entity should not be rendered as a model
        assert "model Entity {" not in output
        # Person should still be rendered
        assert "model Person {" in output

    def test_scalar_arrays(self):
        """Test that scalar arrays use native array types."""
        sb = SchemaBuilder("test")
        sb.add_slot("id", identifier=True, range="string")
        sb.add_slot("tags", range="string", multivalued=True)
        sb.add_class("Article", slots=["id", "tags"])
        sb.add_defaults()

        gen = PrismaGenerator(sb.schema, use_scalar_arrays=True)
        output = gen.serialize()

        # Should use String[] instead of join table
        assert "String[]" in output
        # Join table should not exist
        assert "Article_tags" not in output

    def test_value_object_flattening(self):
        """Test that value objects (no identifier) are flattened."""
        sb = SchemaBuilder("test")
        sb.add_slot("id", identifier=True, range="string")
        sb.add_slot("numeric_value", range="float")
        sb.add_slot("unit", range="string")
        sb.add_slot("measurement", range="QuantityValue")
        sb.add_class("QuantityValue", slots=["numeric_value", "unit"])
        sb.add_class("Observation", slots=["id", "measurement"])
        sb.add_defaults()

        gen = PrismaGenerator(sb.schema)
        output = gen.serialize()

        # QuantityValue should not be a separate model
        assert "model QuantityValue {" not in output
        # Fields should be flattened with prefix
        assert "measurementNumericValue" in output
        assert "measurementUnit" in output

    def test_one_to_many_no_unique_on_fk(self):
        """Test that FK fields don't have @unique (allows one-to-many)."""
        sb = SchemaBuilder("test")
        sb.add_slot("uuid", identifier=True, range="string")
        sb.add_slot("name", range="string")
        sb.add_slot("study", range="Study")
        sb.add_class("Study", slots=["uuid", "name"])
        sb.add_class("Experiment", slots=["uuid", "name", "study"])
        sb.add_defaults()

        gen = PrismaGenerator(sb.schema)
        output = gen.serialize()

        # FK field should exist but NOT have @unique
        assert "studyId" in output
        # Check that @unique is not on the FK line
        lines = output.split("\n")
        for line in lines:
            if "studyId" in line and "String" in line:
                assert "@unique" not in line, f"FK field has @unique: {line}"

    def test_integer_id_autoincrement(self):
        """Test that integer identifiers get @default(autoincrement())."""
        sb = SchemaBuilder("test")
        sb.add_slot("id", identifier=True, range="integer")
        sb.add_slot("name", range="string")
        sb.add_class("Study", slots=["id", "name"])
        sb.add_defaults()

        gen = PrismaGenerator(sb.schema)
        output = gen.serialize()

        assert "Int" in output
        assert "@id" in output
        assert "@default(autoincrement())" in output


class TestPrismaEnumPreparation:
    """Test enum preparation function independently."""

    def test_prepare_enums_basic(self):
        """Test prepare_prisma_enums with basic enum."""
        sb = SchemaBuilder("test")
        sb.add_enum("Status", permissible_values=["ACTIVE", "INACTIVE"])
        sb.add_defaults()

        enums, empty_enums = prepare_prisma_enums(sb.schema)

        assert len(enums) == 1
        assert enums[0].name == "Status"
        assert len(enums[0].values) == 2
        assert len(empty_enums) == 0

    def test_prepare_enums_empty(self):
        """Test that empty enums are tracked separately."""
        sb = SchemaBuilder("test")
        sb.add_enum("EmptyEnum", permissible_values=[])
        sb.add_defaults()

        enums, empty_enums = prepare_prisma_enums(sb.schema)

        assert len(enums) == 0
        assert "EmptyEnum" in empty_enums
