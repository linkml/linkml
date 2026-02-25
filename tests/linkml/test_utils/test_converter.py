import json

import pytest
from click.testing import CliRunner
from rdflib import Graph

from linkml.converter.cli import cli


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner(mix_stderr=False)


def test_help(cli_runner):
    result = cli_runner.invoke(cli, ["--help"])
    out = result.stdout
    assert "INPUT" in out


P1_EXPECTED = {
    "full_name": "first1 last1",
    "is_juvenile": True,
    "age_in_years": 10,
    "age_in_months": 120,
    "age_category": "juvenile",
}

P2_EXPECTED = {
    "full_name": "first2 last2",
    "age_in_years": 20,
    "age_in_months": 240,
    "age_category": "adult",
}


def check_output(json_out):
    with open(json_out) as file:
        obj = json.load(file)
        persons = obj["persons"]
        for p, exptc in [(persons["P:1"], P1_EXPECTED), (persons["P:2"], P2_EXPECTED)]:
            for attr in exptc.keys():
                assert p[attr] == exptc[attr]

        assert "is_juvenile" not in persons["P:2"]


def test_infer(input_path, cli_runner, tmp_path):
    """
    Tests using the --infer option to add missing values
    """
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example.out.json"
    result = cli_runner.invoke(cli, ["--infer", "-s", schema, data_in, "-o", json_out])
    assert result.exit_code == 0
    check_output(json_out)


@pytest.mark.xfail(reason="Bug 2723: missing intermediate checks")
def test_convert(input_path, cli_runner, tmp_path):
    """
    Tests using the --infer option to add missing values, and also roundtripping
    through yaml->json->yaml->rdf->json
    """
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example.out.json"
    yaml_out = tmp_path / "data_example.out.yaml"
    rdf_out = tmp_path / "data_example.out.ttl"
    result = cli_runner.invoke(cli, ["--infer", "-s", schema, data_in, "-o", json_out])
    assert result.exit_code == 0
    result = cli_runner.invoke(cli, ["-s", schema, json_out, "-t", "yaml", "-o", yaml_out])
    assert result.exit_code == 0
    result = cli_runner.invoke(cli, ["-s", schema, yaml_out, "-t", "rdf", "-o", rdf_out])
    assert result.exit_code == 0
    result = cli_runner.invoke(cli, ["-s", schema, rdf_out, "-t", "json", "-o", json_out])
    assert result.exit_code == 0
    check_output(json_out)


def test_prefix_file(input_path, cli_runner, tmp_path):
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    rdf_out = tmp_path / "data_example.out.ttl"
    prefix_file = input_path("data_example_prefix_map.yaml")
    result = cli_runner.invoke(
        cli, ["-s", schema, data_in, "-t", "rdf", "-o", rdf_out, "--prefix-file", prefix_file], catch_exceptions=True
    )
    assert result.exit_code == 0
    rdf_graph = Graph()
    rdf_graph.parse(rdf_out, format="turtle")
    namespaces = {str(prefix): str(namespace) for prefix, namespace in rdf_graph.namespaces()}
    assert "P" in namespaces
    assert namespaces["P"] == "http://www.example.com/personinfo/"


def test_version(cli_runner):
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.stdout


def test_both_prefix_and_prefix_file_error(input_path, cli_runner, tmp_path):
    """Test that passing both --prefix and --prefix-file raises an error."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example.out.json"
    prefix_file = input_path("data_example_prefix_map.yaml")
    result = cli_runner.invoke(
        cli, ["-s", schema, data_in, "-o", json_out, "-P", "ex=http://example.org/", "--prefix-file", prefix_file]
    )
    assert result.exit_code != 0
    assert result.exception is not None
    assert "Either set prefix OR prefix_file, not both" in str(result.exception)


def test_missing_module_and_schema_error(input_path, cli_runner, tmp_path):
    """Test that not passing either --module or --schema raises an error."""
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example.out.json"
    result = cli_runner.invoke(cli, [data_in, "-o", json_out])
    assert result.exit_code != 0
    assert result.exception is not None
    assert "must pass one of module OR schema" in str(result.exception)


def test_invalid_prefix_file_path(input_path, cli_runner, tmp_path):
    """Test that passing a non-existent prefix file path raises an error."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example.out.json"
    result = cli_runner.invoke(
        cli, ["-s", schema, data_in, "-o", json_out, "--prefix-file", "/nonexistent/path/to/prefix.yaml"]
    )
    assert result.exit_code != 0
    assert result.exception is not None
    assert "does not exists" in str(result.exception)


def test_prefix_file_without_prefixes_key(input_path, cli_runner, tmp_path):
    """Test that a prefix file without the 'prefixes' key raises an error."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example.out.json"
    # Create a prefix file without the 'prefixes' key
    invalid_prefix_file = tmp_path / "invalid_prefix_map.yaml"
    invalid_prefix_file.write_text("invalid:\n  key: value\n")
    result = cli_runner.invoke(cli, ["-s", schema, data_in, "-o", json_out, "--prefix-file", str(invalid_prefix_file)])
    assert result.exit_code != 0
    assert result.exception is not None
    assert "does not contain the prefixes key" in str(result.exception)


def test_target_class_from_path(input_path, cli_runner, tmp_path):
    """Test --target-class-from-path option to infer target class from filename."""
    import shutil

    schema = input_path("schema_with_inference.yaml")
    # Rename the data file to start with the target class name
    data_in_original = input_path("data_example.yaml")
    data_in = tmp_path / "Container-example.yaml"
    shutil.copy(data_in_original, data_in)
    json_out = tmp_path / "data_example.out.json"

    result = cli_runner.invoke(cli, ["--target-class-from-path", "-s", schema, str(data_in), "-o", json_out])
    assert result.exit_code == 0


def test_output_to_stdout(input_path, cli_runner):
    """Test that when output is not specified, result is printed to stdout."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")

    # Not specifying -o should print to stdout
    result = cli_runner.invoke(cli, ["-s", schema, data_in, "-t", "json"])
    assert result.exit_code == 0
    # Check that output contains JSON data
    assert "persons" in result.stdout
    assert "P:1" in result.stdout


def test_input_format_option(input_path, cli_runner, tmp_path):
    """Test specifying --input-format explicitly."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example.out.json"

    result = cli_runner.invoke(cli, ["-s", schema, "-f", "yaml", data_in, "-o", json_out])
    assert result.exit_code == 0


def test_output_format_option(input_path, cli_runner, tmp_path):
    """Test specifying --output-format explicitly."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example.out.json"

    result = cli_runner.invoke(cli, ["-s", schema, data_in, "-t", "json", "-o", json_out])
    assert result.exit_code == 0


def test_target_class_option(input_path, cli_runner, tmp_path):
    """Test explicitly specifying --target-class."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example.out.json"

    result = cli_runner.invoke(cli, ["-s", schema, "-C", "Container", data_in, "-o", json_out])
    assert result.exit_code == 0


def test_jsonld_output_with_context(input_path, cli_runner, tmp_path):
    """Test JSON-LD output with context generation from schema."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    jsonld_out = tmp_path / "data_example.out.jsonld"

    result = cli_runner.invoke(cli, ["-s", schema, data_in, "-t", "json-ld", "-o", jsonld_out])
    assert result.exit_code == 0
    # Verify the output contains JSON-LD structure
    with open(jsonld_out) as f:
        data = json.load(f)
        assert "@context" in data


def test_yaml_to_json_conversion(input_path, cli_runner, tmp_path):
    """Test basic YAML to JSON conversion."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example.out.json"

    result = cli_runner.invoke(cli, ["-s", schema, data_in, "-o", json_out])
    assert result.exit_code == 0
    assert json_out.exists()
    with open(json_out) as f:
        data = json.load(f)
        assert "persons" in data


def test_json_to_yaml_conversion(input_path, cli_runner, tmp_path):
    """Test JSON to YAML conversion."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    # First convert to JSON
    json_file = tmp_path / "data_example.json"
    result = cli_runner.invoke(cli, ["-s", schema, data_in, "-o", json_file])
    assert result.exit_code == 0

    # Then convert back to YAML
    yaml_out = tmp_path / "data_example.out.yaml"
    result = cli_runner.invoke(cli, ["-s", schema, str(json_file), "-t", "yaml", "-o", yaml_out])
    assert result.exit_code == 0
    assert yaml_out.exists()


def test_rdf_output(input_path, cli_runner, tmp_path):
    """Test RDF/Turtle output generation."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    rdf_out = tmp_path / "data_example.ttl"

    result = cli_runner.invoke(cli, ["-s", schema, data_in, "-t", "rdf", "-o", rdf_out])
    assert result.exit_code == 0
    assert rdf_out.exists()
    # Verify it's valid RDF
    rdf_graph = Graph()
    rdf_graph.parse(rdf_out, format="turtle")
    assert len(rdf_graph) > 0


def test_ttl_output(input_path, cli_runner, tmp_path):
    """Test explicit TTL format output."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    ttl_out = tmp_path / "data_example_explicit.ttl"

    result = cli_runner.invoke(cli, ["-s", schema, data_in, "-t", "ttl", "-o", ttl_out])
    assert result.exit_code == 0
    assert ttl_out.exists()


def test_with_infer_flag(input_path, cli_runner, tmp_path):
    """Test that --infer flag adds inferred values."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example_inferred.json"

    result = cli_runner.invoke(cli, ["--infer", "-s", schema, data_in, "-o", json_out])
    assert result.exit_code == 0
    check_output(json_out)


def test_with_no_infer_flag(input_path, cli_runner, tmp_path):
    """Test that --no-infer flag is the default and doesn't add inferred values."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example_no_infer.json"

    result = cli_runner.invoke(cli, ["--no-infer", "-s", schema, data_in, "-o", json_out])
    assert result.exit_code == 0
    # Verify that inferred fields are not present
    with open(json_out) as f:
        data = json.load(f)
        p1 = data["persons"]["P:1"]
        # Without inference, full_name should not be present
        assert "full_name" not in p1


def test_multiple_prefix_options(input_path, cli_runner, tmp_path):
    """Test using multiple --prefix options for RDF output."""
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    rdf_out = tmp_path / "data_example_prefixes.ttl"

    result = cli_runner.invoke(
        cli,
        [
            "-s",
            schema,
            data_in,
            "-t",
            "rdf",
            "-o",
            rdf_out,
            "-P",
            "test1=http://test1.example.org/",
            "-P",
            "test2=http://test2.example.org/",
        ],
    )
    assert result.exit_code == 0
    # The prefix may or may not appear in the output depending on usage,
    # but the command should succeed
    assert rdf_out.exists()


# -----------------------------------------------------------------------------
# CLI tests for boolean output formatting (issue #2580)
# -----------------------------------------------------------------------------

BOOLEAN_SCHEMA = """
id: https://example.org/test
name: boolean_test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  Container:
    tree_root: true
    slots:
      - items
  Item:
    slots:
      - id
      - is_active

slots:
  items:
    range: Item
    multivalued: true
    inlined_as_list: true
  id:
    identifier: true
  is_active:
    range: boolean
"""

BOOLEAN_DATA = """
items:
  - id: "1"
    is_active: true
  - id: "2"
    is_active: false
"""


def test_boolean_output_default(cli_runner, tmp_path):
    """Test default boolean output is true/false."""
    schema_file = tmp_path / "schema.yaml"
    data_file = tmp_path / "data.yaml"
    output_file = tmp_path / "output.tsv"

    schema_file.write_text(BOOLEAN_SCHEMA)
    data_file.write_text(BOOLEAN_DATA)

    result = cli_runner.invoke(
        cli,
        [
            "-s",
            str(schema_file),
            "-C",
            "Container",
            "-S",
            "items",
            "-t",
            "tsv",
            "-o",
            str(output_file),
            str(data_file),
        ],
    )
    assert result.exit_code == 0, f"CLI failed: {result.output}"

    content = output_file.read_text()
    assert "true" in content.lower()
    assert "false" in content.lower()


def test_boolean_output_yes_no(cli_runner, tmp_path):
    """Test --boolean-output yes produces yes/no output."""
    schema_file = tmp_path / "schema.yaml"
    data_file = tmp_path / "data.yaml"
    output_file = tmp_path / "output.tsv"

    schema_file.write_text(BOOLEAN_SCHEMA)
    data_file.write_text(BOOLEAN_DATA)

    result = cli_runner.invoke(
        cli,
        [
            "-s",
            str(schema_file),
            "-C",
            "Container",
            "-S",
            "items",
            "--boolean-output",
            "yes",
            "-t",
            "tsv",
            "-o",
            str(output_file),
            str(data_file),
        ],
    )
    assert result.exit_code == 0, f"CLI failed: {result.output}"

    content = output_file.read_text()
    assert "yes" in content
    assert "no" in content
    assert "true" not in content.lower()


def test_boolean_output_numeric(cli_runner, tmp_path):
    """Test --boolean-output 1 produces 1/0 output."""
    schema_file = tmp_path / "schema.yaml"
    data_file = tmp_path / "data.yaml"
    output_file = tmp_path / "output.tsv"

    schema_file.write_text(BOOLEAN_SCHEMA)
    data_file.write_text(BOOLEAN_DATA)

    result = cli_runner.invoke(
        cli,
        [
            "-s",
            str(schema_file),
            "-C",
            "Container",
            "-S",
            "items",
            "--boolean-output",
            "1",
            "-t",
            "tsv",
            "-o",
            str(output_file),
            str(data_file),
        ],
    )
    assert result.exit_code == 0, f"CLI failed: {result.output}"

    content = output_file.read_text()
    # Should have 1 and 0, not true/false
    lines = content.strip().split("\n")
    # Header line + 2 data lines
    assert len(lines) == 3
    # Check data lines contain 1 or 0
    assert "\t1\n" in content or "\t1" in lines[1]
    assert "\t0\n" in content or "\t0" in lines[2]


BOOLEAN_TRUTHY_OVERRIDE_SCHEMA = """
id: https://example.org/test
name: boolean_truthy_test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  Container:
    tree_root: true
    slots:
      - items
  Item:
    slots:
      - id
      - is_active
      - name

slots:
  items:
    range: Item
    multivalued: true
    inlined_as_list: true
  id:
    identifier: true
  is_active:
    range: boolean
  name:
    range: string
"""


def test_boolean_truthy_cli_override(cli_runner, tmp_path):
    """Test --boolean-truthy adds 'yes' as a truthy value for loading."""
    schema_file = tmp_path / "schema.yaml"
    tsv_file = tmp_path / "data.tsv"
    output_file = tmp_path / "output.json"

    schema_file.write_text(BOOLEAN_TRUTHY_OVERRIDE_SCHEMA)
    tsv_file.write_text("id\tis_active\tname\n1\tyes\ttest\n")

    result = cli_runner.invoke(
        cli,
        [
            "-s",
            str(schema_file),
            "-C",
            "Container",
            "-S",
            "items",
            "--boolean-truthy",
            "yes",
            "--boolean-falsy",
            "no",
            "-t",
            "json",
            "-o",
            str(output_file),
            str(tsv_file),
        ],
    )
    assert result.exit_code == 0, f"CLI failed: {result.output}"

    content = json.loads(output_file.read_text())
    assert content["items"][0]["is_active"] is True


def test_empty_string_to_null_via_cli(cli_runner, tmp_path):
    """Test that empty strings in CSV are coerced to null."""
    schema_file = tmp_path / "schema.yaml"
    tsv_file = tmp_path / "data.tsv"
    output_file = tmp_path / "output.json"

    schema_file.write_text(BOOLEAN_TRUTHY_OVERRIDE_SCHEMA)
    tsv_file.write_text("id\tis_active\tname\n1\ttrue\t\n")

    result = cli_runner.invoke(
        cli,
        [
            "-s",
            str(schema_file),
            "-C",
            "Container",
            "-S",
            "items",
            "-t",
            "json",
            "-o",
            str(output_file),
            str(tsv_file),
        ],
    )
    assert result.exit_code == 0, f"CLI failed: {result.output}"

    content = json.loads(output_file.read_text())
    # Empty string should have been coerced to null (absent from JSON)
    assert content["items"][0].get("name") is None
