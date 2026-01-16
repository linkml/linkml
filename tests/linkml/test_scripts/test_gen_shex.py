import json
from io import BytesIO
from unittest.mock import MagicMock, patch

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
from tests.conftest import KITCHEN_SINK_PATH

# Cached ShEx JSON-LD context to avoid 429 errors from w3.org during tests
# Source: http://www.w3.org/ns/shex.jsonld
SHEX_JSONLD_CONTEXT = {
    "@context": {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "shex": "http://www.w3.org/ns/shex#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "annotations": {"@id": "shex:annotation", "@container": "@list", "@type": "@id"},
        "exclusions": {"@id": "shex:exclusion", "@container": "@list", "@type": "@id"},
        "id": "@id",
        "language": "@language",
        "type": "@type",
        "value": "@value",
        "Annotation": "shex:Annotation",
        "EachOf": "shex:EachOf",
        "IriStem": "shex:IriStem",
        "IriStemRange": "shex:IriStemRange",
        "Language": "shex:Language",
        "LanguageStem": "shex:LanguageStem",
        "LanguageStemRange": "shex:LanguageStemRange",
        "LiteralStem": "shex:LiteralStem",
        "LiteralStemRange": "shex:LiteralStemRange",
        "NodeConstraint": "shex:NodeConstraint",
        "OneOf": "shex:OneOf",
        "Schema": "shex:Schema",
        "SemAct": "shex:SemAct",
        "Shape": "shex:Shape",
        "ShapeAnd": "shex:ShapeAnd",
        "ShapeExternal": "shex:ShapeExternal",
        "ShapeNot": "shex:ShapeNot",
        "ShapeOr": "shex:ShapeOr",
        "Stem": "shex:Stem",
        "StemRange": "shex:StemRange",
        "TripleConstraint": "shex:TripleConstraint",
        "Wildcard": "shex:Wildcard",
        "closed": {"@id": "shex:closed", "@type": "xsd:boolean"},
        "code": {"@id": "shex:code", "@language": None},
        "datatype": {"@id": "shex:datatype", "@type": "@id"},
        "expression": {"@id": "shex:expression", "@type": "@id"},
        "expressions": {"@id": "shex:expressions", "@type": "@id", "@container": "@list"},
        "extra": {"@id": "shex:extra", "@type": "@id"},
        "extends": {"@id": "shex:extends", "@type": "@id"},
        "flags": {"@id": "shex:flags", "@language": None},
        "fractiondigits": {"@id": "shex:fractiondigits", "@type": "xsd:integer"},
        "inverse": {"@id": "shex:inverse", "@type": "xsd:boolean"},
        "languageTag": {"@id": "shex:languageTag", "@language": None},
        "length": {"@id": "shex:length", "@type": "xsd:integer"},
        "max": {"@id": "shex:max", "@type": "xsd:integer"},
        "maxexclusive": {"@id": "shex:maxexclusive", "@type": "xsd:integer"},
        "maxinclusive": {"@id": "shex:maxinclusive", "@type": "xsd:integer"},
        "maxlength": {"@id": "shex:maxlength", "@type": "xsd:integer"},
        "min": {"@id": "shex:min", "@type": "xsd:integer"},
        "minexclusive": {"@id": "shex:minexclusive", "@type": "xsd:integer"},
        "mininclusive": {"@id": "shex:mininclusive", "@type": "xsd:integer"},
        "minlength": {"@id": "shex:minlength", "@type": "xsd:integer"},
        "name": {"@id": "shex:name", "@type": "@id"},
        "nodeKind": {"@id": "shex:nodeKind", "@type": "@vocab"},
        "object": {"@id": "shex:object", "@type": "@id"},
        "pattern": {"@id": "shex:pattern", "@language": None},
        "predicate": {"@id": "shex:predicate", "@type": "@id"},
        "semActs": {"@id": "shex:semActs", "@type": "@id", "@container": "@list"},
        "shapeExpr": {"@id": "shex:shapeExpr", "@type": "@id"},
        "shapeExprs": {"@id": "shex:shapeExprs", "@type": "@id", "@container": "@list"},
        "shapes": {"@id": "shex:shapes", "@type": "@id", "@container": "@list"},
        "start": {"@id": "shex:start", "@type": "@id"},
        "startActs": {"@id": "shex:startActs", "@type": "@id", "@container": "@list"},
        "stem": {"@id": "shex:stem", "@type": "xsd:string"},
        "totaldigits": {"@id": "shex:totaldigits", "@type": "xsd:integer"},
        "valueExpr": {"@id": "shex:valueExpr", "@type": "@id"},
        "values": {"@id": "shex:values", "@type": "@id", "@container": "@list"},
        "bnode": "shex:bnode",
        "iri": "shex:iri",
        "literal": "shex:literal",
        "nonliteral": "shex:nonliteral",
    }
}


@pytest.fixture
def mock_shex_context():
    """
    Mock urllib.request.urlopen to return cached ShEx context for w3.org requests.

    This prevents 429 "Too Many Requests" errors from w3.org during tests while
    keeping the production code unchanged.
    """
    original_urlopen = None

    def mock_urlopen(url, *args, **kwargs):
        url_str = url if isinstance(url, str) else url.full_url
        if "w3.org" in url_str and "shex.jsonld" in url_str:
            response = MagicMock()
            response.read.return_value = json.dumps(SHEX_JSONLD_CONTEXT).encode("utf-8")
            response.__enter__ = lambda s: s
            response.__exit__ = MagicMock(return_value=False)
            return response
        return original_urlopen(url, *args, **kwargs)

    import urllib.request

    original_urlopen = urllib.request.urlopen

    with patch("urllib.request.urlopen", side_effect=mock_urlopen):
        yield


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
def test_meta(arguments, snapshot_file, snapshot, mock_shex_context):
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
