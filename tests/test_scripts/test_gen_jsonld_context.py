import pytest
from click.testing import CliRunner

from linkml.generators.jsonldcontextgen import cli
from tests.utils.validate_jsonld_context import RdfExpectations

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate jsonld @context definition from LinkML model" in result.output


@pytest.mark.parametrize(
    "arguments,snapshot_file", [([], "meta.context.jsonld"), (["--metauris"], "meta_context.jsonld")]
)
def test_metamodel(arguments, snapshot_file, snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, arguments + [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot(f"gencontext/{snapshot_file}")


@pytest.mark.parametrize(
    "arguments,snapshot_file",
    [
        (["--no-metadata", "--no-mergeimports", "--no-model"], "simple_uri_test.no_merge.prefixes_only.context.jsonld"),
        (
            ["--no-metadata", "--no-mergeimports", "--no-model", "--flatprefixes"],
            "simple_uri_test.no_merge.flatprefixes_only.context.jsonld",
        ),
        (["--no-metadata", "--no-mergeimports", "--no-prefixes"], "simple_uri_test.no_merge.model_only.context.jsonld"),
        (["--no-metadata", "--no-mergeimports", "--model", "--prefixes"], "simple_uri_test.no_merge.context.jsonld"),
        (["--no-metadata", "--mergeimports", "--no-model"], "simple_uri_test.merge.prefixes_only.context.jsonld"),
        (
            ["--no-metadata", "--mergeimports", "--no-model", "--flatprefixes"],
            "simple_uri_test.merge.flatprefixes_only.context.jsonld",
        ),
        (["--no-metadata", "--mergeimports", "--no-prefixes"], "simple_uri_test.merge.model_only.context.jsonld"),
        (["--no-metadata", "--mergeimports", "--model", "--prefixes"], "simple_uri_test.merge.context.jsonld"),
    ],
)
def test_prefix_options(input_path, arguments, snapshot_file, snapshot):
    """Test various prefix emission options"""
    schema = input_path("simple_uri_test.yaml")
    runner = CliRunner()
    result = runner.invoke(cli, arguments + [str(schema)])
    assert result.exit_code == 0
    assert result.output == snapshot(f"gencontext/{snapshot_file}")


def test_slot_class_uri(input_path, snapshot):
    # Note: two warnings are expected below:
    #   WARNING:ContextGenerator:No namespace defined for URI: http://example.org/slot/su
    #   WARNING:ContextGenerator:No namespace defined for URI: http://example.org/class/cu
    schema = input_path("uri_tests.yaml")
    runner = CliRunner()
    result = runner.invoke(cli, [str(schema)])
    assert result.exit_code == 0
    assert result.output == snapshot("gencontext/uri_tests.jsonld")


@pytest.mark.parametrize(
    "schema",
    [
        pytest.param(
            "simple_uri_test.yaml",
            marks=pytest.mark.xfail(reason="Bug linkml#2625: different context between class or cli"),
        ),
        pytest.param(
            "uri_tests.yaml", marks=pytest.mark.xfail(reason="Bug linkml#2625: different context between class or cli")
        ),
    ],
)
def test_expected_rdf(input_path, schema):
    schema_path = input_path(schema)
    runner = CliRunner()
    result = runner.invoke(cli, [str(schema_path)])
    assert result.exit_code == 0

    rdf_expects = RdfExpectations(schema_path, result.output)
    rdf_expects.check_expectations()
