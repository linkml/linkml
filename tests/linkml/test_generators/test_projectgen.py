import re

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
    ("config_yaml", "message"),
    [
        pytest.param(
            "excludes: jsonldcontext\n",
            "expected a YAML list of generator names at 'excludes'",
            id="excludes-string",
        ),
        pytest.param(
            "includes: python\n",
            "expected a YAML list of generator names at 'includes'",
            id="includes-string",
        ),
        pytest.param("excludes:\n  - 1\n", "expected a generator name in 'excludes'", id="excludes-non-name"),
        pytest.param("directory: [a, b]\n", "expected a directory path at 'directory'", id="directory-list"),
        pytest.param("1: x\n", "expected a configuration name at the top level", id="non-string-key"),
    ],
)
def test_cli_malformed_config_file_values_error(tmp_path, schema_path, config_yaml, message):
    """Keys that are not mappings get checked too, so the whole configuration is reported
    against the key that holds the mistake rather than failing later during generation."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_yaml)

    result = CliRunner().invoke(cli, ["--config-file", str(config_path), "-d", str(tmp_path / "out"), str(schema_path)])

    assert result.exit_code != 0
    assert message in result.output
    assert not isinstance(result.exception, AttributeError | TypeError)


def test_cli_excludes_matches_whole_names_only(tmp_path, schema_path):
    """`jsonld` is a substring of `jsonldcontext`, and names are matched with ``in``.
    Excluding one generator must not quietly take out the other as well."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text("excludes:\n  - jsonldcontext\n")
    out_dir = tmp_path / "out"

    result = CliRunner().invoke(
        cli,
        [
            "--config-file",
            str(config_path),
            "-I",
            "jsonld",
            "-I",
            "jsonldcontext",
            "-d",
            str(out_dir),
            str(schema_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert (out_dir / "jsonld" / "schema.jsonld").is_file()
    assert not (out_dir / "jsonld" / "schema.context.jsonld").is_file()


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
    assert "--generator-arguments is not valid YAML" in result.output


def test_cli_unparseable_config_file_errors(tmp_path, schema_path):
    """A --config-file that isn't valid YAML reports the same way as a bad -A blob."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text("generator_args:\n  python: {unclosed\n")

    result = CliRunner().invoke(cli, ["--config-file", str(config_path), "-d", str(tmp_path / "out"), str(schema_path)])

    assert result.exit_code != 0
    assert "--config-file is not valid YAML" in result.output


@pytest.mark.parametrize(
    "config_yaml",
    [
        pytest.param("", id="empty-file"),
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


def _generated_json_schema(out_dir):
    return (out_dir / "jsonschema" / "schema.schema.json").read_text()


@pytest.mark.parametrize(
    ("arguments", "expected"),
    [
        pytest.param("owl: {metaclasses: false}", '"additionalProperties": false', id="other-generator-kept"),
        pytest.param("jsonschema: {not_closed: true}", '"additionalProperties": true', id="same-setting-overridden"),
    ],
)
def test_cli_generator_arguments_layer_over_config_file(tmp_path, schema_path, arguments, expected):
    """-A is layered over --config-file setting by setting. Naming one setting on the
    command line used to discard everything the file configured."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text("generator_args:\n  jsonschema:\n    not_closed: false\n")
    out_dir = tmp_path / "out"

    result = CliRunner().invoke(
        cli,
        [
            "--config-file",
            str(config_path),
            "-A",
            arguments,
            "-I",
            "jsonschema",
            "-d",
            str(out_dir),
            str(schema_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert expected in _generated_json_schema(out_dir)


@pytest.mark.parametrize(
    ("attribute", "value", "message"),
    [
        pytest.param(
            "generator_args", "notamapping", "expected a YAML mapping at 'generator_args'", id="generator-args-scalar"
        ),
        pytest.param(
            "generator_args",
            {"python": "notamapping"},
            "expected a YAML mapping at 'generator_args.python'",
            id="generator-section-scalar",
        ),
        pytest.param(
            "excludes", "python", "expected a YAML list of generator names at 'excludes'", id="excludes-string"
        ),
        pytest.param(
            "includes", "python", "expected a YAML list of generator names at 'includes'", id="includes-string"
        ),
    ],
)
def test_generate_checks_a_configuration_built_in_code(tmp_path, schema_path, attribute, value, message):
    """A ProjectConfiguration assembled in code is checked the same way as one read from a
    file, so using this as a library reports the mistake instead of failing part-way in."""
    config = ProjectConfiguration()
    config.directory = str(tmp_path / "out")
    setattr(config, attribute, value)

    with pytest.raises(ValueError, match=re.escape(message)):
        ProjectGenerator().generate(str(schema_path), config)
