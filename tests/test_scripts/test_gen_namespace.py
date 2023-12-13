import re

from click.testing import CliRunner

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.generators.namespacegen import cli


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate a namespace manager for all of the prefixes represented in a LinkML model" in re.sub(
        r"\s+", " ", result.output
    )


def test_metamodel(snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, [LOCAL_METAMODEL_YAML_FILE])
    assert result.exit_code == 0
    assert result.output == snapshot("gennamespace/meta_namespaces.py")
