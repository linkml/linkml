import warnings

from click.testing import CliRunner

from linkml.generators.yamlgen import cli
from tests.conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, "--help")
    assert "Validate input and produce fully resolved yaml equivalent" in result.output


def test_no_duplicate_option_warnings(input_path):
    """Ensure -V (--version) does not collide with --validateonly/--generate (issue #4235)."""
    runner = CliRunner()
    clean_yaml = input_path("yaml_validate_clean.yaml")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", UserWarning)

        help_res = runner.invoke(cli, ["--help"])
        assert help_res.exit_code == 0

        ver_res = runner.invoke(cli, ["-V"])
        assert ver_res.exit_code == 0
        assert "version" in ver_res.output.lower()

        val_res = runner.invoke(cli, [clean_yaml, "--validateonly"])
        assert val_res.exit_code == 0
        assert "Classes:" in val_res.output
        assert "name: cleanyaml" not in val_res.output

        gen_res = runner.invoke(cli, [clean_yaml, "-g"])
        assert gen_res.exit_code == 0
        assert "name: cleanyaml" in gen_res.output
        assert "id: http://example.org/tests/cleanyaml" in gen_res.output

    duplicate_warnings = [w for w in caught if "used more than once" in str(w.message)]
    assert duplicate_warnings == []


def test_metamodel(snapshot):
    """Test emitting a YAML file"""
    runner = CliRunner()
    result = runner.invoke(cli, [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot("genyaml/meta.yaml")


def test_validate_yaml(input_path, snapshot):
    """Test YAML file validation"""
    runner = CliRunner()
    result = runner.invoke(cli, [input_path("yaml_validate_clean.yaml"), "-v"])
    assert result.exit_code == 0
    assert result.output == snapshot("genyaml/clean.yaml")

    result = runner.invoke(cli, [input_path("yaml_validate_invalid.yaml"), "-v"], standalone_mode=False)
    assert result.exit_code != 0
    assert "slot: k - unrecognized range (none)" in str(result.exception)
