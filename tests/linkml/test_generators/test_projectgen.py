import pytest
from click.testing import CliRunner

from linkml.generators.projectgen import ProjectConfiguration, ProjectGenerator, cli


def test_projectgen(kitchen_sink_path, tmp_path):
    def check_contains(v: str, folder: str, local_path: str):
        with open(tmp_path / folder / local_path, encoding="UTF-8") as stream:
            assert v in stream.read()

    """Generate whole project"""
    config = ProjectConfiguration()
    config.directory = tmp_path
    config.generator_args["jsonschema"] = {
        "top_class": "Dataset",
        "not_closed": False,
    }
    config.generator_args["owl"] = {"metaclasses": False, "type_objects": False}
    gen = ProjectGenerator()
    gen.generate(kitchen_sink_path, config)
    # some of these tests may be quite rigid as they make assumptions about formatting
    check_contains("CREATE TABLE", "sqlschema", "kitchen_sink.sql")
    check_contains("ks:age_in_years a owl:DatatypeProperty", "owl", "kitchen_sink.owl.ttl")
    check_contains('"additionalProperties": false', "jsonschema", "kitchen_sink.schema.json")


MINIMAL_SCHEMA = """
id: https://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
classes:
  Thing:
    slots:
      - name
slots:
  name:
"""


@pytest.fixture
def schema_path(tmp_path):
    """A schema small enough to run the CLI against quickly."""
    path = tmp_path / "schema.yaml"
    path.write_text(MINIMAL_SCHEMA)
    return path


@pytest.mark.parametrize(
    ("config_yaml", "where"),
    [
        pytest.param("justastring\n", "the top level", id="top-level-scalar"),
        pytest.param("- 1\n- 2\n", "the top level", id="top-level-list"),
        pytest.param("generator_args: notamapping\n", "'generator_args'", id="scalar-generator-args"),
        pytest.param(
            "generator_args:\n  jsonschema: notamapping\n",
            "'generator_args.jsonschema'",
            id="scalar-generator-section",
        ),
    ],
)
def test_cli_malformed_config_file_errors(tmp_path, schema_path, config_yaml, where):
    """A --config-file that is the wrong shape names the offending key, rather than crashing
    later with an AttributeError or TypeError from deep inside generation."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_yaml)

    result = CliRunner().invoke(cli, ["--config-file", str(config_path), "-d", str(tmp_path / "out"), str(schema_path)])

    assert result.exit_code != 0
    assert f"expected a YAML mapping at {where}" in result.output
    assert not isinstance(result.exception, AttributeError | TypeError)


@pytest.mark.parametrize(
    ("arguments", "where"),
    [
        pytest.param("notamapping", "the top level", id="scalar"),
        pytest.param("- 1\n- 2\n", "the top level", id="list"),
        pytest.param("jsonschema: notamapping", "'jsonschema'", id="scalar-generator-section"),
    ],
)
def test_cli_malformed_generator_arguments_errors(tmp_path, schema_path, arguments, where):
    """-A/--generator-arguments gets the same shape check as --config-file. Without it, a
    blob that parses but isn't a mapping crashes later with nothing pointing back at -A."""
    result = CliRunner().invoke(cli, ["-A", arguments, "-d", str(tmp_path / "out"), str(schema_path)])

    assert result.exit_code != 0
    assert f"expected a YAML mapping at {where}" in result.output
    assert not isinstance(result.exception, AttributeError | TypeError)


def test_cli_unparseable_generator_arguments_errors(tmp_path, schema_path):
    """A -A blob that isn't valid YAML at all reports as a usage error, not a raw traceback."""
    result = CliRunner().invoke(cli, ["-A", "{unclosed", "-d", str(tmp_path / "out"), str(schema_path)])

    assert result.exit_code != 0
    assert "must be a valid YAML blob" in result.output


@pytest.mark.parametrize(
    "config_yaml",
    [
        pytest.param("generator_args:\n", id="empty-generator-args"),
        pytest.param("generator_args:\n  python:\n", id="empty-generator-section"),
        pytest.param("generator_args:\n  python:\n    genmeta: false\n", id="populated"),
    ],
)
def test_cli_valid_config_file_generates(tmp_path, schema_path, config_yaml):
    """Well-formed configuration still generates, including sections left deliberately
    empty: an absent value means "nothing configured here", not a mistake."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_yaml)
    out_dir = tmp_path / "out"

    result = CliRunner().invoke(
        cli, ["--config-file", str(config_path), "-I", "python", "-d", str(out_dir), str(schema_path)]
    )

    assert result.exit_code == 0, result.output
    assert (out_dir / "schema.py").is_file()


def test_cli_valid_generator_arguments_generates(tmp_path, schema_path):
    """The -A happy path is unaffected by the added validation."""
    out_dir = tmp_path / "out"

    result = CliRunner().invoke(
        cli,
        ["-A", "python: {genmeta: false}", "-I", "python", "-d", str(out_dir), str(schema_path)],
    )

    assert result.exit_code == 0, result.output
    assert (out_dir / "schema.py").is_file()
