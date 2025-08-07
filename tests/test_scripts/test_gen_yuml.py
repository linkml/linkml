import pytest
from click.testing import CliRunner

from linkml.generators.yumlgen import YumlGenerator, cli

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, "--help")
    assert "Generate a yUML representation of a LinkML model" in result.output


@pytest.mark.parametrize(
    "arguments,snapshot_file",
    [
        ([], "meta.yuml"),
        (["-c", "Person"], "person.yuml"),
        (["-c", "Person", "-c", "Event"], "person_event.yuml"),
    ],
)
def test_metamodel(arguments, snapshot_file, snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, arguments + [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot(f"genyuml/{snapshot_file}")


@pytest.mark.network
@pytest.mark.parametrize(
    "arguments,snapshot_dir",
    [
        (["-c", "Person"], "meta"),
        (["-c", "Event"], "meta1"),
    ],
)
def test_metamodel_output_directory(arguments, snapshot_dir, snapshot, tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, arguments + ["-d", str(tmp_path), KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert tmp_path == snapshot(f"genyuml/{snapshot_dir}")


def test_invalid_classname():
    runner = CliRunner()
    result = runner.invoke(cli, ["-c", "noclass", KITCHEN_SINK_PATH], standalone_mode=False)
    assert result.exit_code != 0
    assert "noclass" in str(result.exception)


@pytest.mark.parametrize("format", YumlGenerator.valid_formats)
@pytest.mark.network
def test_formats(format, tmp_path, snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, ["-f", format, "-c", "Person", "-d", str(tmp_path), KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert tmp_path == snapshot(f"genyuml/meta_{format}")


@pytest.mark.network
def test_specified_diagram_name(tmp_path, snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, ["--diagram-name", "specified_name", "-d", str(tmp_path), KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert tmp_path == snapshot("genyuml/specified_name_dir")


def test_yumlgen_deprecation():
    """Test that YumlGenerator emits a deprecation warning since
    it has been marked for deprecation."""
    from linkml.generators.yumlgen import YumlGenerator
    from linkml.utils.deprecation import EMITTED, SemVer

    # Skip test in development environment with version 0.0.0
    ver = SemVer.from_package("linkml")
    if ver.major == 0 and ver.minor == 0 and ver.patch == 0:
        pytest.skip("Deprecation warnings not tested in development environment (version 0.0.0)")

    print(KITCHEN_SINK_PATH)

    # clear any previously emitted warnings for this test
    if "gen-yuml" in EMITTED:
        EMITTED.remove("gen-yuml")

    with pytest.warns(DeprecationWarning) as record:
        YumlGenerator(KITCHEN_SINK_PATH)

    assert len(record) == 1
    assert "gen-yuml" in str(record[0].message)
