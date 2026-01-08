"""
Unit tests for Prisma template rendering.

Tests the Jinja2 template with mock data (no full generator needed).
"""

from dataclasses import dataclass

import pytest
from jinja2 import Template

from linkml.generators.prisma.prisma_template import prisma_template_str


@dataclass
class PrismaFieldInfo:
    """Mock field info for testing."""

    name: str
    prisma_type: str
    modifiers: str = ""
    is_optional: bool = False
    is_relation: bool = False
    relation_fields: bool = False
    fk_field_name: str = ""
    fk_type: str = ""
    linkml_metadata: str = ""


@dataclass
class PrismaModelInfo:
    """Mock model info for testing."""

    name: str
    fields: list
    description: str = ""
    is_a: str = ""
    mixins: str = ""
    abstract: bool = False
    is_join_table: bool = False
    composite_key: str = ""
    unique_constraints: list = None

    def __post_init__(self):
        if self.unique_constraints is None:
            self.unique_constraints = []


@dataclass
class PrismaEnumValue:
    """Mock enum value for testing."""

    name: str
    description: str = ""


@dataclass
class PrismaEnumInfo:
    """Mock enum info for testing."""

    name: str
    values: list


class TestTemplateBasicRendering:
    """Test basic template rendering with minimal data."""

    def test_template_renders_header(self):
        template = Template(prisma_template_str)
        output = template.render(
            schema_name="test",
            datasource_provider="postgresql",
            models=[],
            enums=[],
        )

        assert "// Prisma schema generated from LinkML schema: test" in output
        assert 'provider = "postgresql"' in output
        assert 'provider = "prisma-client-js"' in output
        assert "datasource db {" in output
        assert "generator client {" in output

    def test_template_with_schema_id(self):
        template = Template(prisma_template_str)
        output = template.render(
            schema_name="test",
            schema_id="https://example.org/test",
            datasource_provider="postgresql",
            models=[],
            enums=[],
        )

        assert "// @linkml:id https://example.org/test" in output

    def test_template_with_schema_description(self):
        template = Template(prisma_template_str)
        output = template.render(
            schema_name="test",
            schema_description="A test schema",
            datasource_provider="postgresql",
            models=[],
            enums=[],
        )

        assert "// A test schema" in output


class TestTemplateModelRendering:
    """Test model rendering."""

    def test_renders_basic_model(self):
        template = Template(prisma_template_str)
        models = [
            PrismaModelInfo(
                name="Person",
                fields=[
                    PrismaFieldInfo("id", "String", "@id @default(auto())"),
                    PrismaFieldInfo("name", "String", ""),
                ],
            )
        ]

        output = template.render(
            schema_name="test",
            datasource_provider="postgresql",
            models=models,
            enums=[],
        )

        assert "model Person {" in output
        assert "id" in output
        assert "@id" in output
        assert "name" in output
        assert "String" in output

    def test_renders_optional_field(self):
        template = Template(prisma_template_str)
        models = [
            PrismaModelInfo(
                name="Person",
                fields=[
                    PrismaFieldInfo("id", "String", "@id"),
                    PrismaFieldInfo("nickname", "String", "", is_optional=True),
                ],
            )
        ]

        output = template.render(
            schema_name="test",
            datasource_provider="postgresql",
            models=models,
            enums=[],
        )

        assert "nickname" in output
        assert "String?" in output
        assert "model Person {" in output

    def test_renders_model_with_description(self):
        template = Template(prisma_template_str)
        models = [
            PrismaModelInfo(
                name="Person",
                description="A person entity",
                fields=[
                    PrismaFieldInfo("id", "String", "@id"),
                ],
            )
        ]

        output = template.render(
            schema_name="test",
            datasource_provider="postgresql",
            models=models,
            enums=[],
        )

        assert "// A person entity" in output
        assert "model Person {" in output

    def test_renders_inheritance_metadata(self):
        template = Template(prisma_template_str)
        models = [
            PrismaModelInfo(
                name="Student",
                is_a="Person",
                mixins='["HasAliases"]',
                fields=[
                    PrismaFieldInfo("id", "String", "@id"),
                ],
            )
        ]

        output = template.render(
            schema_name="test",
            datasource_provider="postgresql",
            models=models,
            enums=[],
        )

        assert "// @linkml:is_a Person" in output
        assert '// @linkml:mixins ["HasAliases"]' in output

    def test_renders_abstract_class(self):
        template = Template(prisma_template_str)
        models = [
            PrismaModelInfo(
                name="NamedThing",
                abstract=True,
                fields=[
                    PrismaFieldInfo("id", "String", "@id"),
                ],
            )
        ]

        output = template.render(
            schema_name="test",
            datasource_provider="postgresql",
            models=models,
            enums=[],
        )

        assert "// @linkml:abstract true" in output


class TestTemplateEnumRendering:
    """Test enum rendering."""

    def test_renders_basic_enum(self):
        template = Template(prisma_template_str)
        enums = [
            PrismaEnumInfo(
                name="Status",
                values=[
                    PrismaEnumValue("ACTIVE"),
                    PrismaEnumValue("INACTIVE"),
                ],
            )
        ]

        output = template.render(
            schema_name="test",
            datasource_provider="postgresql",
            models=[],
            enums=enums,
        )

        assert "enum Status {" in output
        assert "ACTIVE" in output
        assert "INACTIVE" in output

    def test_renders_enum_with_descriptions(self):
        template = Template(prisma_template_str)
        enums = [
            PrismaEnumInfo(
                name="Status",
                values=[
                    PrismaEnumValue("ACTIVE", "Currently active"),
                    PrismaEnumValue("INACTIVE", "Not active"),
                ],
            )
        ]

        output = template.render(
            schema_name="test",
            datasource_provider="postgresql",
            models=[],
            enums=enums,
        )

        assert "ACTIVE  // Currently active" in output
        assert "INACTIVE  // Not active" in output


class TestTemplateDatasourceProviders:
    """Test different datasource providers."""

    @pytest.mark.parametrize(
        "provider",
        [
            "postgresql",
            "mysql",
            "sqlite",
            "cockroachdb",
        ],
    )
    def test_renders_datasource_provider(self, provider):
        template = Template(prisma_template_str)
        output = template.render(
            schema_name="test",
            datasource_provider=provider,
            models=[],
            enums=[],
        )

        assert f'provider = "{provider}"' in output


class TestTemplateCompositeKeys:
    """Test composite key rendering."""

    def test_renders_composite_primary_key(self):
        template = Template(prisma_template_str)
        models = [
            PrismaModelInfo(
                name="PersonAddress",
                fields=[
                    PrismaFieldInfo("person_id", "String"),
                    PrismaFieldInfo("address_id", "String"),
                ],
                composite_key="person_id, address_id",
            )
        ]

        output = template.render(
            schema_name="test",
            datasource_provider="postgresql",
            models=models,
            enums=[],
        )

        assert "@@id([person_id, address_id])" in output


class TestTemplateUniqueConstraints:
    """Test unique constraint rendering."""

    def test_renders_unique_constraint(self):
        template = Template(prisma_template_str)

        @dataclass
        class UniqueConstraint:
            fields: str
            name: str = ""

        models = [
            PrismaModelInfo(
                name="Person",
                fields=[
                    PrismaFieldInfo("id", "String", "@id"),
                    PrismaFieldInfo("email", "String"),
                ],
                unique_constraints=[
                    UniqueConstraint(fields="email", name="email_unique"),
                ],
            )
        ]

        output = template.render(
            schema_name="test",
            datasource_provider="postgresql",
            models=models,
            enums=[],
        )

        assert '@@unique([email], name: "email_unique")' in output


class TestTemplateMultipleModels:
    """Test rendering multiple models."""

    def test_renders_multiple_models(self):
        template = Template(prisma_template_str)
        models = [
            PrismaModelInfo(
                name="Person",
                fields=[
                    PrismaFieldInfo("id", "String", "@id"),
                    PrismaFieldInfo("name", "String"),
                ],
            ),
            PrismaModelInfo(
                name="Address",
                fields=[
                    PrismaFieldInfo("id", "String", "@id"),
                    PrismaFieldInfo("street", "String"),
                ],
            ),
        ]

        output = template.render(
            schema_name="test",
            datasource_provider="postgresql",
            models=models,
            enums=[],
        )

        assert "model Person {" in output
        assert "model Address {" in output
        assert output.index("model Person") < output.index("model Address")
