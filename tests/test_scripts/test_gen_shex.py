import pytest
from click.testing import CliRunner
from pyshex import ShExEvaluator
from rdflib import Graph

from linkml import METAMODEL_NAMESPACE
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.shexgen import ShExGenerator, cli
from tests import SKIP_SHEX_VALIDATION, SKIP_SHEX_VALIDATION_REASON

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, "--help")
    assert "Generate a ShEx Schema for a  LinkML model" in result.output


@pytest.mark.parametrize(
    "arguments,snapshot_file",
    [
        ([], "metashex.shex"),
        (["-f", "json"], "metashex.json"),
        (["-f", "rdf"], "metashex.ttl"),
        (["-f", "shex"], "metashex.shex"),
        (["--metauris"], "metashexn.shex"),
    ],
)
@pytest.mark.network
def test_meta(arguments, snapshot_file, snapshot):
    """Generate various forms of the metamodel in ShEx"""
    runner = CliRunner()
    result = runner.invoke(cli, arguments + [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot(f"genshex/{snapshot_file}")


@pytest.mark.skip(reason="Restore when JSONLD generator works")
def test_rdf_shex(tmp_path):
    """Generate ShEx and RDF for the model and verify that the RDF represents a valid instance"""

    json_file = tmp_path / "meta.jsonld"
    json_str = JSONLDGenerator(KITCHEN_SINK_PATH).serialize()
    with open(json_file, "w") as f:
        f.write(json_str)

    context_file = tmp_path / "metacontext.jsonld"
    ContextGenerator(KITCHEN_SINK_PATH).serialize(output=context_file)
    assert context_file.exists()

    rdf_file = tmp_path / "meta.ttl"
    RDFGenerator(KITCHEN_SINK_PATH).serialize(output=rdf_file, context=context_file)
    assert rdf_file.exists()

    shex_file = tmp_path / "meta.shex"
    ShExGenerator(KITCHEN_SINK_PATH).serialize(output=shex_file, collections=False)
    assert shex_file.exists()

    if SKIP_SHEX_VALIDATION:
        print(f"tests/test_scripts/test_gen_shex.py: {SKIP_SHEX_VALIDATION_REASON}")
    else:
        g = Graph()
        g.load(rdf_file, format="ttl")
        focus = METAMODEL_NAMESPACE.metamodel
        start = METAMODEL_NAMESPACE.SchemaDefinition
        results = ShExEvaluator(g, str(shex_file), focus, start).evaluate(debug=False)
        success = all(r.result for r in results)
        if not success:
            for r in results:
                if not r.result:
                    print(r.reason)
        assert success
