"""Minimal tests for the Ossie generator.

The generator code is in LinkML-Scala, so the tests here check mostly that all the
options work correctly.
"""

import dataclasses
import json
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from linkml.generators.common.scala import build_info
from linkml.generators.ossiegen import OssieGenerator, cli

linkml_scala = pytest.importorskip("linkml_scala", reason="the LinkML-Scala bindings are not installed")

pytestmark = pytest.mark.ossiegen

SCHEMA = Path(__file__).parent / "input" / "ossie_ontology.yaml"

IMPORTED_CLASS = "Activity"
"""A class from core.yaml, which :data:`SCHEMA` imports."""

UNREACHABLE_CLASS = "Organization"
"""A class in :data:`SCHEMA` that its tree root does not reach."""


def concepts(ontology: dict) -> set[str]:
    """The names of the concepts in a parsed ontology."""
    return {component["concept"] for component in ontology["ontology"]}


@pytest.fixture(scope="module")
def ontology() -> dict:
    """The generated ontology for :data:`SCHEMA`, parsed."""
    with OssieGenerator(str(SCHEMA)) as generator:
        return generator.as_dict()


@pytest.mark.parametrize("fmt", OssieGenerator.valid_formats)
def test_format_selection(fmt):
    """YAML and JSON must be passed through directly."""
    with OssieGenerator(str(SCHEMA), format=fmt) as generator:
        upstream = {"yaml": generator.as_yaml, "json": generator.as_json}[fmt]
        assert generator.serialize() == upstream()


@pytest.mark.parametrize("concept", ["Registry", "HasAliases", "Person", "Organization", "VitalStatus"])
def test_classes_and_enums_become_concepts(ontology, concept):
    """Basic test: check if the generator emits something."""
    assert concept in concepts(ontology)


@pytest.mark.parametrize("fmt", OssieGenerator.valid_formats)
def test_every_format_contains_the_same_ontology(ontology, fmt):
    """Serializing to each supported format and reading it back gives the same ontology.

    Driven off ``valid_formats`` so that adding a format cannot skip this check.
    """
    with OssieGenerator(str(SCHEMA), format=fmt) as generator:
        parsed = yaml.safe_load(generator.serialize())
    assert parsed == ontology


def test_unknown_format_is_rejected():
    """The base generator validates ``--format`` against ``valid_formats``."""
    with pytest.raises(ValueError, match="Unrecognized format"):
        OssieGenerator(str(SCHEMA), format="ttl")


@pytest.mark.parametrize(
    "pruning_mode,tree_root,kept",
    [
        ("schema", None, {"Registry", "HasAliases", "Person", UNREACHABLE_CLASS, "VitalStatus"}),
        ("treeRoot", None, {"Registry", "HasAliases", "Person", "VitalStatus"}),
        ("treeRoot", "Person", {"HasAliases", "Person", "VitalStatus"}),
    ],
)
def test_pruning_mode_drops_unreachable_concepts(pruning_mode, tree_root, kept):
    """``--pruning-mode`` and ``--tree-root`` become LinkML-Scala's ``pruning_mode`` and ``tree_root``."""
    with OssieGenerator(str(SCHEMA), pruning_mode=pruning_mode, tree_root=tree_root) as generator:
        assert concepts(generator.as_dict()) == kept


def test_no_pruning_keeps_imported_concepts(ontology):
    """The default, ``skip``, keeps the imported classes too."""
    assert IMPORTED_CLASS in concepts(ontology)


def test_tree_root_without_tree_root_pruning_is_rejected():
    """A tree root only means something with ``pruning_mode="treeRoot"``."""
    with OssieGenerator(str(SCHEMA), tree_root="Person") as generator:
        with pytest.raises(ValueError, match="tree_root only applies"):
            generator.serialize()


def test_cli_pruning_mode():
    """``--pruning-mode`` and ``--tree-root`` reach the generator."""
    result = CliRunner().invoke(
        cli, [str(SCHEMA), "--format", "json", "--pruning-mode", "treeRoot", "--tree-root", "Person"]
    )
    assert result.exit_code == 0
    assert "Registry" not in concepts(json.loads(result.output))


def test_cli_output_writes_a_file(tmp_path):
    """``-o`` writes the ontology to a file instead of stdout."""
    destination = tmp_path / "ontology.yaml"
    result = CliRunner().invoke(cli, [str(SCHEMA), "-o", str(destination)])
    assert result.exit_code == 0
    assert result.output == ""
    assert yaml.safe_load(destination.read_text())


def test_cli():
    """``gen-ossie schema.yaml`` prints YAML."""
    result = CliRunner().invoke(cli, [str(SCHEMA)])
    assert result.exit_code == 0
    assert yaml.safe_load(result.output)


def test_every_cli_option_is_accepted_by_the_generator():
    """``cli`` hands its options straight to the constructor, so each one needs a field."""
    fields = {field.name for field in dataclasses.fields(OssieGenerator)}
    options = {param.name for param in cli.params if param.expose_value}
    assert options - fields == {"yamlfile"}, "yamlfile is the schema itself, the rest are options"


def test_cli_version_reports_both_versions():
    """A bug report needs the linkml version and the LinkML-Scala version, so ``-V`` shows both."""
    result = CliRunner().invoke(cli, ["-V"])
    assert result.exit_code == 0
    assert "linkml " in result.output
    assert f"LinkML-Scala {build_info()['linkml_scala_version']}" in result.output
