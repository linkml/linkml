"""
Test example runner using a simulated setup.

 - input/personinfo.yaml
 - input/examples
 - input/counter_examples
"""

import pytest
from linkml_runtime import SchemaView
from prefixmaps.io.parser import load_multi_context
from click.testing import CliRunner
from linkml.workspaces.example_runner import ExampleRunner, cli

@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def example_runner(input_path, tmp_path):
    schemaview = SchemaView(input_path("personinfo.yaml"))
    ctxt = load_multi_context(["obo", "linked_data", "prefixcc"])
    return ExampleRunner(
        schemaview=schemaview,
        input_directory=input_path("examples"),
        counter_example_input_directory=input_path("counter_examples"),
        output_directory=tmp_path,
        prefix_map=ctxt.as_dict(),
    )


def test_load_from_dict(example_runner):
    """test loading from a dict object, including using type designators."""
    obj = example_runner._load_from_dict({"persons": [{"id": "p1", "name": "John"}]})
    assert obj is not None


def test_example_runner(example_runner):
    """Process all YAML examples in input folder."""
    example_runner.process_examples()
    md = str(example_runner.summary)
    assert "Container-001" in example_runner.summary.inputs
    assert "Container-001.yaml" in example_runner.summary.outputs
    assert "Container-001.json" in example_runner.summary.outputs
    assert "Container-001.ttl" in example_runner.summary.outputs
    assert "Container-001" in md
    assert "Container-002" not in md


def test_example_runner_non_defaults(example_runner):
    """
    Process all JSON examples in input folder,
    using only ttl writing.
    :return:
    """
    example_runner.input_formats = ["json"]
    example_runner.output_formats = ["ttl"]
    example_runner.process_examples()
    md = str(example_runner.summary)
    assert "Container-002" in example_runner.summary.inputs
    assert "Container-002.yaml" not in example_runner.summary.outputs
    assert "Container-002.json" not in example_runner.summary.outputs
    assert "Container-002.ttl" in example_runner.summary.outputs
    assert "Container-001" not in md
    assert "Container-002" in md


def test_cli_required_options(runner, example_runner, tmp_path):
    """Test the CLI with required options."""
    schema_path = example_runner.schemaview.schema.source_file
    output_directory = example_runner.output_directory

    result = runner.invoke(cli, ['--schema', schema_path, '--output-directory', str(output_directory)])
    assert result.exit_code == 0

def test_cli_with_prefixes(runner, example_runner, tmp_path):
    """Test the CLI with the --prefixes option."""
    schema_path = example_runner.schemaview.schema.source_file
    output_directory = example_runner.output_directory
    prefixes_file = tmp_path / "prefixes.yaml"

    # Write prefixes to a temporary file
    prefixes_file.write_text("""
    prefixes:
      ex: https://example.org/
    """)

    result = runner.invoke(cli, [
        '--schema', schema_path,
        '--prefixes', str(prefixes_file),
        '--output-directory', str(output_directory)
    ])
    assert result.exit_code == 0

def test_cli_with_input_directory(runner, example_runner):
    """Test the CLI with the --input-directory option."""
    schema_path = example_runner.schemaview.schema.source_file
    input_directory = example_runner.input_directory
    output_directory = example_runner.output_directory

    result = runner.invoke(cli, [
        '--schema', schema_path,
        '--input-directory', str(input_directory),
        '--output-directory', str(output_directory)
    ])
    assert result.exit_code == 0

def test_cli_no_schema(runner, example_runner):
    """Test the CLI when the required --schema option is missing."""
    output_directory = example_runner.output_directory

    result = runner.invoke(cli, ['--output-directory', str(output_directory)])
    assert result.exit_code != 0
    assert "Error: Missing option '--schema'" in result.output
