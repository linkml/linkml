import csv
import json
import logging
import re

import pytest
import yaml
from rdflib import Graph, URIRef

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.prefixmapgen import PrefixGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.yamlgen import YAMLGenerator
from tests.linkml.test_prefixes.environment import env

pytestmark = pytest.mark.xdist_group("prefixes")


@pytest.fixture
def schema():
    return env.input_path("prefixtest.yaml")


@pytest.fixture
def owl_output(tmp_path):
    return str(tmp_path / "prefixtest.owl.ttl")


@pytest.fixture
def rdf_output(tmp_path):
    return str(tmp_path / "prefixtest.rdf.nt")


@pytest.fixture
def pm_output(tmp_path):
    return str(tmp_path / "prefixtest.prefixmap.json")


@pytest.fixture
def context_output(tmp_path):
    return str(tmp_path / "prefixtest.context.jsonld")


@pytest.fixture
def tsv_output():
    return env.expected_path("prefix_map_prefixtest.tsv")


logger = logging.getLogger(__name__)


def test_owlgen(schema, owl_output):
    """owl"""
    owl = OwlSchemaGenerator(schema, mergeimports=False, ontology_uri_suffix=".owl.ttl", format="nt").serialize()
    with open(owl_output, "w") as stream:
        stream.write(owl)
    g = Graph()
    # TODO: test with turtle when https://github.com/linkml/linkml/issues/163#issuecomment-906507968 is resolved
    # g.parse(owl_output, format="turtle")
    g.parse(owl_output, format="nt")
    # TODO: fix owlgen such that we don't have to hardcode exceptions
    check_triples(
        g,
        exceptions=[
            "http://schema.org/additionalName",
            "http://purl.obolibrary.org/obo/BFO_0000050",
            "http://schema.org/isPartOf",
        ],
    )


# TODO: restore. See: https://github.com/linkml/linkml/issues/537
@pytest.mark.skip("https://github.com/linkml/linkml/issues/537")
def test_rdfgen(schema, rdf_output):
    # TODO: ttl output fails - check why
    # TODO: imports do not seem to work
    rdf = RDFGenerator(schema, mergeimports=True, format="nt").serialize()
    with open(rdf_output, "w") as stream:
        stream.write(rdf)
    g = Graph()
    g.parse(rdf_output, format="nt")
    check_triples(g)


def test_prefixmapgen(schema, pm_output, tsv_output):
    out = PrefixGenerator(schema, mergeimports=True).serialize()
    with open(pm_output, "w") as stream:
        stream.write(out)
    expected = {
        "BFO": "http://purl.obolibrary.org/obo/BFO_",
        "CL": "http://purl.obolibrary.org/obo/CL_",
        "GO": "http://purl.obolibrary.org/obo/GO_",
        "PR": "http://purl.obolibrary.org/obo/PR_",
        "SIO": "http://semanticscience.org/resource/SIO_",
        "SO": "http://purl.obolibrary.org/obo/SO_",
        "biolink": "https://w3id.org/biolink/",
        "dbont": "http://dbpedia.org/ontology/",
        "dce": "http://purl.org/dc/elements/1.1/",
        "lego": "http://geneontology.org/lego/",
        "linkml": "https://w3id.org/linkml/",
        "owl": "http://www.w3.org/2002/07/owl#",
        "pav": "http://purl.org/pav/",
        "prefixtest": "https://w3id.org/linkml/tests/prefixtest/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "sdo": "http://schema.org/",
        "wd": "https://www.wikidata.org/wiki/",
    }
    with open(pm_output) as stream:
        obj = json.load(stream)
    fails = 0
    for k, v in expected.items():
        if k in obj:
            if v != obj[k]:
                logger.error(f"{k} = {v} expected {expected[k]}")
                fails += 1
        else:
            logger.error(f"Missing key: {k}")
            fails += 1
    assert fails == 0

    # unit test when format option tsv is supplied
    tsv_str = PrefixGenerator(schema, format="tsv", mergeimports=True).serialize()
    actual_tsv_dict = {}
    split_tsv = re.split(r"\n+", tsv_str)
    for elem in split_tsv:
        pair = re.split(r"\t+", elem)

        if len(pair) == 2:
            actual_tsv_dict[pair[0]] = pair[1]

    expected_tsv_dict = {}
    with open(tsv_output) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for row in rd:
            expected_tsv_dict[row[0]] = row[1]

    expected_tsv_dict = dict(sorted(expected_tsv_dict.items()))

    assert actual_tsv_dict == expected_tsv_dict


def test_jsonldcontext(schema, context_output):
    out = ContextGenerator(schema, mergeimports=True).serialize()
    with open(context_output, "w") as stream:
        stream.write(out)
    expected = {
        "BFO": {"@id": "http://purl.obolibrary.org/obo/BFO_", "@prefix": True},
        "CL": {"@id": "http://purl.obolibrary.org/obo/CL_", "@prefix": True},
        "GO": {"@id": "http://purl.obolibrary.org/obo/GO_", "@prefix": True},
        "PR": {"@id": "http://purl.obolibrary.org/obo/PR_", "@prefix": True},
        "SIO": {"@id": "http://semanticscience.org/resource/SIO_", "@prefix": True},
        "SO": {"@id": "http://purl.obolibrary.org/obo/SO_", "@prefix": True},
        "biolink": "https://w3id.org/biolink/",
        "dbont": "http://dbpedia.org/ontology/",
        "dce": "http://purl.org/dc/elements/1.1/",
        "lego": "http://geneontology.org/lego/",
        "linkml": "https://w3id.org/linkml/",
        "owl": "http://www.w3.org/2002/07/owl#",
        "pav": "http://purl.org/pav/",
        "prefixtest": "https://w3id.org/linkml/tests/prefixtest/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "sdo": "http://schema.org/",
        "wd": "https://www.wikidata.org/wiki/",
        "@vocab": "https://w3id.org/linkml/tests/prefixtest/",
        "additionalName": {"@id": "sdo:additionalName"},
        "id": "@id",
        "label": {"@id": "rdfs:label"},
        "part_of": {"@id": "BFO:0000050"},
        "type": {"@id": "rdf:type"},
    }
    with open(context_output) as stream:
        obj = json.load(stream)["@context"]
    fails = 0
    for k, v in expected.items():
        if k in obj:
            if v != obj[k]:
                if not ("@id" in v and "@id" in obj[k] and v["@id"] == obj[k]["@id"]):
                    logger.error(f"{k} = {v} expected {expected[k]}")
                    fails += 1
        else:
            logger.error(f"Missing key: {k}")
            fails += 1
    assert fails == 0

    # unexpected - we don't want to import unused prefixes from the default_curi_map
    assert "FOODON" not in obj
    assert "OBI" not in obj
    assert "ENVO" not in obj


def test_issue_curie_prefix_matching_longest_prefix_wins_for_context_terms():
    schema = env.input_path("curie_prefix_matching.yaml")

    generated_yaml = yaml.safe_load(YAMLGenerator(schema).serialize())
    assert generated_yaml["types"]["t1"]["uri"] == "p1:c/suffix1"
    assert generated_yaml["types"]["t2"]["uri"] == "p2:suffix2"
    assert generated_yaml["types"]["t3"]["uri"] == "http://example.org/prefixes/a/b/c/suffix3"

    generated_context = json.loads(ContextGenerator(schema).serialize())["@context"]
    assert generated_context["C1"]["@id"] == "p1:/c/c1"
    assert generated_context["C2"]["@id"] == "p2:/c2"
    assert generated_context["C3"]["@id"] == "p2:c3"


def test_issue_curie_prefix_matching_prefix_case_is_canonicalized_in_context():
    schema = env.input_path("curie_case.yaml")

    generated_yaml = yaml.safe_load(YAMLGenerator(schema).serialize())
    assert generated_yaml["classes"]["c1"]["class_uri"] == "abc:c1"
    assert generated_yaml["classes"]["c2"]["class_uri"] == "ABC:t2"
    assert generated_yaml["classes"]["c3"]["class_uri"] == "aBc:t3"

    generated_context = json.loads(ContextGenerator(schema).serialize())["@context"]
    assert {generated_context[prefix] for prefix in ("ABC", "aBC", "aBc", "abc")} == {"http://example.org/abc#"}
    assert generated_context["C1"]["@id"] == "aBC:c1"
    assert generated_context["C2"]["@id"] == "aBC:t2"
    assert generated_context["C3"]["@id"] == "aBC:t3"


def check_triples(g, exceptions=None):
    """
    currently testing is fairly weak: simply checks if the expected expanded URIs are
    present as objects
    """

    if exceptions is None:
        exceptions = []

    expected = [
        "http://purl.obolibrary.org/obo/PR_000000001",
        "http://purl.obolibrary.org/obo/SO_0000704",
        "http://semanticscience.org/resource/SIO_010035",
        "http://schema.org/additionalName",
        "http://purl.obolibrary.org/obo/BFO_0000050",
    ]
    for triple in g.triples((None, None, None)):
        # print(f'T= {triple}')
        (_, _, o) = triple
        if isinstance(o, URIRef):
            v = str(o)
            if v in expected:
                expected.remove(v)
    for v in exceptions:
        if v in expected:
            logger.warning(f"TODO: figure why {v} not present")
            expected.remove(v)
    if len(expected) > 0:
        for e in expected:
            logger.error(f"Did not find {e}")
        assert False
    else:
        assert True
