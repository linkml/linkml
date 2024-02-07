import pytest
from click.testing import CliRunner
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import cli


@pytest.fixture
def cli_runner():
    return CliRunner()


def test_pythongen_forward_declaration_w_import(cli_runner, input_path):
    """Tests https://github.com/linkml/linkml/issues/1857"""

    schema_path = input_path("issue_1857/machine.yaml")
    result = cli_runner.invoke(cli, [schema_path])
    assert result.exception is None
    assert result.exit_code == 0
    compile_python(result.output, "mod")
