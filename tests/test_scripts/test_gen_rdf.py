import pytest
from click.testing import CliRunner

from linkml import LOCAL_METAMODEL_LDCONTEXT_FILE
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.rdfgen import cli

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate an RDF representation of a LinkML model" in result.output


@pytest.fixture(scope="session")
def gen_context_file(tmp_path_factory):
    path = tmp_path_factory.mktemp("test_rdf_gen") / "meta_context_rdf.jsonld"
    with path.open("w") as output:
        output.write(ContextGenerator(KITCHEN_SINK_PATH, useuris=True).serialize())
    return str(path)


@pytest.mark.xfail
@pytest.mark.parametrize(
    "arguments,snapshot_file", [([], "meta.ttl"), (["--metauris"], "metan.ttl"), (["-f", "n3"], "meta.n3")]
)
def test_metamodel(arguments, snapshot_file, snapshot, gen_context_file):
    """Test the RDF generator on the metamodel"""
    runner = CliRunner()
    result = runner.invoke(cli, arguments + ["--context", gen_context_file, KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot(f"genrdf/{snapshot_file}")


@pytest.mark.xfail
def test_make_script(snapshot):
    """Test a relative file path in JSON"""
    runner = CliRunner()
    result = runner.invoke(cli, ["--context", LOCAL_METAMODEL_LDCONTEXT_FILE, KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot("genrdf/make_output.ttl")
