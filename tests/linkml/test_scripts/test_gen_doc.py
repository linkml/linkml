import os.path
import re

from click.testing import CliRunner

from linkml.generators.docgen import cli

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert re.search("Generate documentation folder from a LinkML YAML schema", result.output)


def test_metamodel(tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["-d", tmp_path, KITCHEN_SINK_PATH])
    assert result.exit_code == 0


def test_mergeimports(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "-d",
            tmp_path,
            "--mergeimports",
            KITCHEN_SINK_PATH,
        ],
    )
    assert result.exit_code == 0

    index_path = os.path.join(tmp_path, "index.md")
    assert (
        re.search(
            r"\s*\|\s*\[Agent\]\(Agent\.md\)\s*\|\s*",
            open(index_path).read(),
        )
        is not None
    )


def test_no_mergeimports(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "-d",
            tmp_path,
            "--no-mergeimports",
            KITCHEN_SINK_PATH,
        ],
    )
    assert result.exit_code == 0

    index_path = os.path.join(tmp_path, "index.md")
    assert (
        re.search(
            r"\s*\|\s*\[Agent\]\(Agent\.md\)\s*\|\s*",
            open(index_path).read(),
        )
        is None
    )


def test_no_render_imports(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "-d",
            tmp_path,
            "--no-mergeimports",
            "--no-render-imports",
            KITCHEN_SINK_PATH,
        ],
    )
    assert result.exit_code == 0

    index_path = os.path.join(tmp_path, "index.md")
    assert (
        re.search(
            r"\s*\|\s*\[Agent\]\(Agent\.md\)\s*\|\s*",
            open(index_path).read(),
        )
        is None
    )


def test_render_imports(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "-d",
            tmp_path,
            "--no-mergeimports",
            "--render-imports",
            KITCHEN_SINK_PATH,
        ],
    )
    assert result.exit_code == 0

    index_path = os.path.join(tmp_path, "index.md")

    assert (
        re.search(
            r"\s*\|\s*\[Agent\]\(Agent\.md\)\s*\|\s*",
            open(index_path).read(),
        )
        is not None
    )
