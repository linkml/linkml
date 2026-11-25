"""Tests for the Frictionless generator.

The generator code is in ohi LinkML, so the tests here check mostly that the options reach it,
that the one-file and many-file outputs agree, and that the files are written where they should be.
"""

import dataclasses
import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from linkml.generators.common.ohi import build_info
from linkml.generators.frictionlessgen import DATA_PACKAGE, FrictionlessGenerator, cli

ohi_linkml = pytest.importorskip("ohi_linkml", reason="the ohi LinkML bindings are not installed")

pytestmark = pytest.mark.frictionlessgen

SCHEMA = Path(__file__).parent / "input" / "frictionless_model.yaml"

IMPORTED_TABLES = {"activity", "agent"}
"""Tables of the classes in core.yaml, which :data:`SCHEMA` imports."""


def tables(package: dict) -> set[str]:
    """The names of the tables in a parsed data package."""
    return {resource["name"] for resource in package["resources"]}


def table_schema(package: dict, table: str) -> dict:
    """The Table Schema of one table in a parsed data package, with the table schemas in it."""
    return next(resource["schema"] for resource in package["resources"] if resource["name"] == table)


@pytest.fixture(scope="module")
def files() -> dict[str, str]:
    """The generated files for :data:`SCHEMA`, by path."""
    with FrictionlessGenerator(str(SCHEMA)) as generator:
        return generator.as_files()


@pytest.fixture(scope="module")
def package() -> dict:
    """The generated data package for :data:`SCHEMA`, with the table schemas in it, parsed."""
    with FrictionlessGenerator(str(SCHEMA)) as generator:
        return json.loads(generator.serialize())


def test_one_file_per_table(files, package):
    """``datapackage.json`` refers to a ``schemas/<table>.json`` for each table, and nothing else."""
    assert set(files) == {DATA_PACKAGE} | {f"schemas/{table}.json" for table in tables(package)}
    resources = json.loads(files[DATA_PACKAGE])["resources"]
    assert {resource["name"]: resource["schema"] for resource in resources} == {
        table: f"schemas/{table}.json" for table in tables(package)
    }


def test_serialize_puts_each_table_schema_into_its_resource(files, package):
    """The one-file package is the many-file one, with each ``schema`` path replaced by the file."""
    for table in tables(package):
        assert table_schema(package, table) == json.loads(files[f"schemas/{table}.json"])


def test_concrete_classes_become_tables(package):
    """Abstract classes get no table, imported classes do."""
    assert tables(package) == {"registry", "person", "organization", "address", "pet"} | IMPORTED_TABLES


def test_references_become_foreign_keys(package):
    """A reference to another class gets a foreign key to its table, a self-reference an empty resource."""
    person = table_schema(package, "person")
    assert person["primaryKey"] == "uid"
    assert {key["fields"]: key["reference"] for key in person["foreignKeys"]} == {
        "employer": {"resource": "organization", "fields": "uid"},
        "manager": {"resource": "", "fields": "uid"},
    }


@pytest.mark.parametrize(
    "pruning_mode,tree_root,kept",
    [
        ("schema", None, {"registry", "person", "organization", "address", "pet"}),
        ("tree_root", None, {"registry", "person", "organization", "address"}),
        ("tree_root", "Person", {"person", "organization", "address"}),
    ],
)
def test_pruning_mode_drops_unreachable_tables(pruning_mode, tree_root, kept):
    """``--pruning-mode`` and ``--tree-root`` become ohi LinkML's ``pruning_mode`` and ``tree_root``."""
    with FrictionlessGenerator(str(SCHEMA), pruning_mode=pruning_mode, tree_root=tree_root) as generator:
        assert tables(generator.as_dict()) == kept


def test_skip_classes_without_identifier(package):
    """``--skip-classes-without-identifier`` drops the tables with no primary key, except the tree root."""
    with FrictionlessGenerator(str(SCHEMA), skip_classes_without_identifier=True) as generator:
        assert tables(generator.as_dict()) == tables(package) - {"address"}


def test_unknown_format_is_rejected():
    """The base generator validates ``--format`` against ``valid_formats``."""
    with pytest.raises(ValueError, match="Unrecognized format"):
        FrictionlessGenerator(str(SCHEMA), format="yaml")


def test_cli_prints_the_package(package):
    """Without ``-o`` or ``-d``, the CLI prints the package as one JSON document."""
    result = CliRunner().invoke(cli, [str(SCHEMA)])
    assert result.exit_code == 0
    assert json.loads(result.output) == package


def test_cli_options_reach_the_generator():
    """``--pruning-mode``, ``--tree-root`` and ``--skip-classes-without-identifier`` reach the generator."""
    result = CliRunner().invoke(
        cli,
        [str(SCHEMA), "--pruning-mode", "tree_root", "--tree-root", "Person", "--skip-classes-without-identifier"],
    )
    assert result.exit_code == 0
    assert tables(json.loads(result.output)) == {"person", "organization"}


def test_cli_output_writes_one_file(package, tmp_path):
    """``-o`` writes the package as one JSON document to a file instead of stdout."""
    destination = tmp_path / "datapackage.json"
    result = CliRunner().invoke(cli, [str(SCHEMA), "-o", str(destination)])
    assert result.exit_code == 0
    assert result.output == ""
    assert json.loads(destination.read_text(encoding="utf-8")) == package


def test_cli_writes_the_files_to_the_output_directory(files, tmp_path):
    """``-d`` writes ``datapackage.json`` and the table schemas below it."""
    out = tmp_path / "out"
    result = CliRunner().invoke(cli, [str(SCHEMA), "-d", str(out)])
    assert result.exit_code == 0
    assert result.output == ""
    # Read as bytes, so that line endings are compared as they are on disk.
    written = {path.relative_to(out).as_posix(): path.read_bytes().decode("utf-8") for path in out.rglob("*.json")}
    assert written == files


def test_cli_output_and_output_directory_are_exclusive(tmp_path):
    """The package is either one file or a directory of files."""
    result = CliRunner().invoke(cli, [str(SCHEMA), "-o", str(tmp_path / "p.json"), "-d", str(tmp_path / "out")])
    assert result.exit_code == 2
    assert "not both" in result.output


def test_every_cli_option_is_accepted_by_the_generator():
    """``cli`` hands its options straight to the constructor, so each one needs a field."""
    fields = {field.name for field in dataclasses.fields(FrictionlessGenerator)}
    options = {param.name for param in cli.params if param.expose_value}
    assert options - fields == {"yamlfile", "output_directory"}, (
        "yamlfile is the schema itself, and the CLI writes the files itself"
    )


def test_cli_version_reports_both_versions():
    """A bug report needs the linkml version and the ohi LinkML version, so ``-V`` shows both."""
    result = CliRunner().invoke(cli, ["-V"])
    assert result.exit_code == 0
    assert "linkml " in result.output
    assert f"ohi LinkML {build_info()['linkml_scala_version']}" in result.output
