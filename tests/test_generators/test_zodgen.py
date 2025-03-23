from click.testing import CliRunner
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SlotDefinition
from mock import patch

from linkml.generators.zodgen import ZodGenerator, cli
from linkml.utils.schema_builder import SchemaBuilder


def test_zodgen(kitchen_sink_path):
    """Test that Zod schemas are generated from a kitchen sink schema."""
    # Generate the Zod schema as a string
    zod_schema = ZodGenerator(kitchen_sink_path)
    zod_schema_str = zod_schema.serialize()

    def assert_in(expected: str) -> None:
        # Remove spaces to do a flexible comparison
        assert expected.replace(" ", "") in zod_schema_str.replace(" ", "")

    # Check that the zod import is present
    assert 'import { z } from "zod";' in zod_schema_str
    # Check that an example schema for Organization is present
    assert "export const OrganizationSchema" in zod_schema_str
    # Check that a Person schema is generated
    assert_in("export const PersonSchema")
    # Check that a sample multivalued slot from the kitchen sink is generated
    assert_in("has_familial_relationships: z.array(")
    # Check that a reference to a CodeSystem is generated correctly
    assert_in("code_systems: z.array(")


def test_required_slots_zod():
    """Test that required and optional slots are generated correctly in Zod schemas."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    # Create a required slot and an optional slot
    id_slot = SlotDefinition(name="id", multivalued=False, range="string", required=True)
    description_slot = SlotDefinition(name="description", multivalued=False, range="string")
    sb.add_class("Person", slots=[id_slot, description_slot])
    schema = sb.schema

    # Generate Zod schema with type utilities (if relevant) and including induced slots
    zod_schema_str = ZodGenerator(schema, include_induced_slots=True).serialize()

    # The required field "id" should be mapped to a plain z.string()
    assert "id: z.string()" in zod_schema_str
    # The optional field "description" should be marked with .optional()
    assert "description: z.string().optional()" in zod_schema_str


def test_multivalued_string_zod():
    """Test that multivalued string slots are generated as z.array(z.string()) in Zod schemas."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    # Create two multivalued slots: one optional and one required
    aliases = SlotDefinition(name="aliases", multivalued=True, range="string")
    descriptions = SlotDefinition(name="descriptions", multivalued=True, range="string", required=True)
    sb.add_class("Person", slots=[aliases, descriptions])
    schema = sb.schema

    zod_schema_str = ZodGenerator(schema, include_induced_slots=True).serialize()

    # Optional multivalued field "aliases" should be wrapped in z.array(...) and be optional
    assert "aliases: z.array(z.string()).optional()" in zod_schema_str
    # Required multivalued field "descriptions" should be wrapped in z.array(z.string()) without .optional()
    assert "descriptions: z.array(z.string())" in zod_schema_str


def test_output_option_zod(kitchen_sink_path, tmp_path):
    """Test that Zod generator writes output to a file when the --output option is used."""
    zod_generator = ZodGenerator(kitchen_sink_path)
    output_file = tmp_path / "kitchen_sink_zod.ts"
    zod_generator.serialize(output=output_file)
    assert output_file.exists()


def test_cli_print_stdout_without_output_zod(kitchen_sink_path):
    """Test that the CLI prints to stdout when no output file is provided."""
    runner = CliRunner()
    with patch("builtins.print") as mock_print:
        result = runner.invoke(cli, [kitchen_sink_path])
        assert result.exit_code == 0
        mock_print.assert_called_once()


def test_cli_no_print_with_output_zod(kitchen_sink_path, tmp_path):
    """Test that the CLI does not print to stdout when an output file is specified."""
    runner = CliRunner()
    with patch("builtins.print") as mock_print:
        output_path = tmp_path / "kitchen_sink_zod.ts"
        result = runner.invoke(cli, [kitchen_sink_path, "--output", str(output_path)])
        assert result.exit_code == 0
        mock_print.assert_not_called()