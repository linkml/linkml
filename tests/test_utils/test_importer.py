import pytest
from click.testing import CliRunner
from linkml.utils.linkml_importer import cli


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


def test_import_schema(input_path, cli_runner, tmp_path):

    schema = input_path("schema_with_inference.yaml")
    import_schema = "deprecated"
    output_path = tmp_path / "merged_schema.yaml"
    print(output_path)
    print(import_schema)
    result = cli_runner.invoke(cli, ["--schema", schema,
                            "--import_schema_name", import_schema,
                            "--output", output_path])
    print(result.output)
    with open(output_path) as file:
        for line in file:
            print(line)


