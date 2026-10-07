"""Tests for gen-rust crate-name validation and --config-file.

These only render the crate, so unlike ``test_rustgen.py`` they need no Rust
toolchain and are not gated behind ``--with-rustgen``.
"""

import warnings

import click
import pytest
from click.testing import CliRunner

from linkml.generators.rustgen import RustGenerator
from linkml.generators.rustgen.cli import cli
from linkml.generators.rustgen.rustgen import _derive_crate_name, _is_valid_rust_ident

SCHEMA = """
id: https://example.org/thing
name: thing_schema
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
classes:
  Thing:
    attributes:
      name:
"""


@pytest.mark.parametrize(
    "crate_name,valid",
    [
        ("thing", True),
        ("my_crate", True),
        ("_private", True),
        ("Crate2", True),
        ("", False),
        ("_", False),
        ("my-crate", False),
        ("2crate", False),
        ("my.crate", False),
        ("fn", False),
        ("Self", False),
        ("test", False),
        ("core", False),
    ],
)
def test_is_valid_rust_ident(crate_name, valid):
    assert _is_valid_rust_ident(crate_name) is valid


@pytest.mark.parametrize("crate_name", ["my-crate", "fn", 123])
def test_constructor_invalid_crate_name_errors(crate_name):
    """An explicit crate name that cannot be a cargo [lib] name is rejected, including
    a non-string one such as an unquoted number from a config file."""
    with pytest.raises(ValueError, match="not a valid Rust crate name"):
        RustGenerator(SCHEMA, crate_name=crate_name)


def test_validate_generator_args():
    RustGenerator.validate_generator_args({"crate_name": None})
    RustGenerator.validate_generator_args({"crate_name": "my_crate"})
    with pytest.raises(click.UsageError, match="not a valid Rust crate name"):
        RustGenerator.validate_generator_args({"crate_name": "my-crate"})


# --config-file tests follow the javagen/golanggen ones (test_cli_config_file_sets_package,
# test_cli_package_overrides_config_file, test_cli_invalid_config_package_errors), with
# --crate-name in place of --package.


def _rust_config(tmp_path, body: str):
    """Write the schema, a config file with a `generator_args.rust` section, and an output dir."""
    schema_file = tmp_path / "thing.yaml"
    schema_file.write_text(SCHEMA)
    config_file = tmp_path / "config.yaml"
    config_file.write_text("generator_args:\n  rust:\n" + body)
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    return schema_file, config_file, out_dir


def test_cli_config_file_sets_crate_name(tmp_path):
    schema_file, config_file, out_dir = _rust_config(tmp_path, "    crate_name: from_config\n")

    result = CliRunner().invoke(cli, [str(schema_file), "--config-file", str(config_file), "-o", str(out_dir)])

    assert result.exit_code == 0, result.output
    assert 'name = "from_config"' in (out_dir / "Cargo.toml").read_text()


def test_cli_crate_name_overrides_config_file(tmp_path):
    schema_file, config_file, out_dir = _rust_config(tmp_path, "    crate_name: from_config\n")

    result = CliRunner().invoke(
        cli, [str(schema_file), "-C", str(config_file), "-o", str(out_dir), "--crate-name", "from_cli"]
    )

    assert result.exit_code == 0, result.output
    cargo = (out_dir / "Cargo.toml").read_text()
    assert 'name = "from_cli"' in cargo
    assert "from_config" not in cargo


def test_cli_config_file_sets_mode(tmp_path):
    """A non-name option is overlaid too: `mode: file` writes one .rs file, no Cargo.toml."""
    schema_file, config_file, out_dir = _rust_config(tmp_path, "    mode: file\n")
    out_file = out_dir / "thing.rs"

    result = CliRunner().invoke(cli, [str(schema_file), "-C", str(config_file), "-o", str(out_file)])

    assert result.exit_code == 0, result.output
    assert "pub struct Thing" in out_file.read_text()
    assert not (out_dir / "Cargo.toml").exists()


@pytest.mark.parametrize("crate_name", ["my-crate", "123"])
def test_cli_invalid_config_crate_name_errors(tmp_path, crate_name):
    """A bad crate name is a usage error raised before the schema is loaded."""
    schema_file, config_file, out_dir = _rust_config(tmp_path, f"    crate_name: {crate_name}\n")

    result = CliRunner().invoke(cli, [str(schema_file), "--config-file", str(config_file), "-o", str(out_dir)])

    assert result.exit_code == 2
    assert "not a valid Rust crate name" in result.output
    assert not (out_dir / "Cargo.toml").exists()


# ---------------------------------------------------------------------------
# Derived crate name, --force and -f
# ---------------------------------------------------------------------------

HYPHEN_SCHEMA = SCHEMA.replace("name: thing_schema", "name: thing-schema")


def _write_schema(tmp_path, schema: str = SCHEMA):
    """Write the schema and make an empty output directory."""
    schema_file = tmp_path / "thing.yaml"
    schema_file.write_text(schema)
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    return schema_file, out_dir


@pytest.mark.parametrize(
    "schema_name,expected",
    [
        ("thing_schema", "thing_schema"),
        ("ThingSchema", "ThingSchema"),
        ("thing-schema", "thing_schema"),
        ("thing.schema", "thing_schema"),
        ("type", "type_"),
        ("test", "test_"),
        ("1abc", "example"),
        ("", "example"),
    ],
)
def test_derive_crate_name(schema_name, expected):
    assert _derive_crate_name(schema_name) == expected


def test_derived_crate_name_is_set_on_the_generator():
    assert RustGenerator(HYPHEN_SCHEMA).crate_name == "thing_schema"


def test_cli_derived_crate_name_is_usable_everywhere(tmp_path):
    """A hyphenated schema name is folded in every place the crate name lands: Cargo.toml
    (cargo refuses a hyphen in a [lib] name), the #[pymodule] function and the stub_gen path."""
    schema_file, out_dir = _write_schema(tmp_path, HYPHEN_SCHEMA)

    result = CliRunner().invoke(cli, [str(schema_file), "-o", str(out_dir), "--pyo3"])

    assert result.exit_code == 0, result.output
    cargo = (out_dir / "Cargo.toml").read_text()
    assert 'name = "thing_schema"' in cargo
    assert "thing-schema" not in cargo
    assert "fn thing_schema(" in (out_dir / "src" / "lib.rs").read_text()
    assert "thing_schema::stub_info()" in (out_dir / "src" / "bin" / "stub_gen.rs").read_text()


def test_cli_crate_name_names_the_python_module(tmp_path):
    """The #[pymodule] function must match the [lib] name or the extension fails to import,
    so an explicit crate name is used for both."""
    schema_file, out_dir = _write_schema(tmp_path)

    result = CliRunner().invoke(cli, [str(schema_file), "-o", str(out_dir), "--pyo3", "--crate-name", "from_cli"])

    assert result.exit_code == 0, result.output
    assert "fn from_cli(" in (out_dir / "src" / "lib.rs").read_text()


def test_cli_force_overwrites_a_non_empty_output_dir(tmp_path):
    schema_file, out_dir = _write_schema(tmp_path)
    (out_dir / "stale").write_text("")

    assert CliRunner().invoke(cli, [str(schema_file), "-o", str(out_dir)]).exit_code != 0
    result = CliRunner().invoke(cli, [str(schema_file), "-o", str(out_dir), "--force"])

    assert result.exit_code == 0, result.output
    assert (out_dir / "Cargo.toml").exists()


def test_cli_short_f_is_the_shared_format_option(tmp_path):
    """-f has always resolved to --format, as on every generator; --force no longer claims
    it too, so click has nothing to warn about."""
    schema_file, out_dir = _write_schema(tmp_path)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = CliRunner().invoke(cli, [str(schema_file), "-f", "rust", "-o", str(out_dir)])

    assert result.exit_code == 0, result.output
    assert not [w for w in caught if "used more than once" in str(w.message)]
