from pathlib import Path

from click.testing import CliRunner

from linkml.generators import golrgen
from tests.conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(golrgen.cli, ["--help"])
    assert "Generate GOLR representation of a LinkML model" in result.output


def test_metamodel_valid_call(tmp_path, snapshot):
    runner = CliRunner()
    result = runner.invoke(golrgen.cli, ["-d", tmp_path, KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    parts = []
    for yaml_file in sorted(Path(tmp_path).rglob("*.yaml")):
        parts.append(f"# --- {yaml_file.name} ---\n")
        parts.append(yaml_file.read_text(encoding="utf-8"))
        if not parts[-1].endswith("\n"):
            parts[-1] += "\n"
    concatenated = "".join(parts)
    assert concatenated == snapshot("gengolr_meta.yaml")


def test_metamodel_invalid_call(tmp_path):
    runner = CliRunner()
    result = runner.invoke(golrgen.cli, ["-f", "xsv", "-d", tmp_path, KITCHEN_SINK_PATH], standalone_mode=False)
    assert result.exit_code != 0
    assert "xsv" in str(result.exception)
