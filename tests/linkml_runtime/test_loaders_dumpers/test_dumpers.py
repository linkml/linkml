import os
from typing import cast

import pytest
from rdflib import SKOS, Literal, Namespace

from linkml_runtime.dumpers import json_dumper, rdf_dumper, yaml_dumper
from linkml_runtime.utils.yamlutils import as_json_object
from tests.support.clicktestcase import ClickTestCase
from tests.test_loaders_dumpers import (
    GITHUB_LD10_CONTEXT,
    GITHUB_LD11_CONTEXT,
    HTTP_TEST_PORT,
    HTTPS_TEST_PORT,
    LD_11_DIR,
    LD_11_SSL_SVR,
    LD_11_SVR,
)
from tests.test_loaders_dumpers.environment import env
from tests.test_loaders_dumpers.models.termci_schema import ConceptReference, ConceptSystem, Package

OBO = Namespace("http://purl.obolibrary.org/obo/")
NCIT = Namespace("http://purl.obolibrary.org/obo/NCI_")


@pytest.fixture(scope="module")
def test_package():
    """Generate a small sample TermCI instance for testing purposes"""
    e1 = ConceptReference(
        OBO.NCI_C147796,
        code="C147796",
        defined_in=OBO,
        designation="TSCYC - Being Frightened of Men",
        definition="Trauma Symptom Checklist for Young Children (TSCYC) Please indicate how often"
        " the child has done, felt, or experienced each of the following things in "
        "the last month: Being frightened of men.",
        narrower_than=OBO.NCI_C147557,
        reference=OBO.NCI_C147796,
    )
    e2 = ConceptReference(
        OBO.NCI_C147557,
        code="C147557",
        defined_in=OBO,
        designation="TSCYC Questionnaire Question",
        definition="A question associated with the TSCYC questionnaire.",
        narrower_than=OBO.NCI_C91102,
    )
    c1 = ConceptSystem(OBO, "OBO", contents=[e1, e2])
    return Package([c1])


def dump_test(filename: str, dumper, comparator=None) -> bool:
    """
    Invoke the dumper passing it the output file name and then compare the result to an expected output
    """
    actual_file = env.actual_path(filename)
    expected_file = env.expected_path("dump", filename)

    dumper(actual_file)

    with open(actual_file) as actual_f:
        actual = actual_f.read()
    return env.eval_single_file(expected_file, actual, comparator=comparator)


def dumps_test(filename: str, dumper, comparator=None) -> bool:
    """
    Invoke the string dumper and evaluate the results
    """
    actual = dumper()
    expected_file = env.expected_path("dumps", filename)
    return env.eval_single_file(expected_file, actual, comparator=comparator)


def test_yaml_dumper(test_package):
    """Test the yaml emitter"""
    # TODO: Once this is entered into the BiolinkML test package, compare this to input/obo_test.yaml
    dump_test("obo_sample.yaml", lambda out_fname: yaml_dumper.dump(test_package, out_fname))
    dumps_test("obo_sample.yaml", lambda: yaml_dumper.dumps(test_package))


def test_json_dumper(test_package):
    """Test the json emitter"""
    # TODO: Same as test_yaml_dumper
    dump_test("obo_sample.json", lambda out_fname: json_dumper.dump(test_package, out_fname))

    obo_json_obj = cast(Package, as_json_object(test_package))
    assert obo_json_obj.system[0].namespace == OBO
    assert obo_json_obj.system[0].contents[0].code == "C147796"

    dumps_test("obo_sample.json", lambda: json_dumper.dumps(test_package))
    dump_test(
        "obo_sample_context.json",
        lambda out_fname: json_dumper.dump(
            test_package, out_fname, GITHUB_LD10_CONTEXT + "termci_schema.context.jsonld"
        ),
    )
    dumps_test(
        "obo_sample_context.json",
        lambda: json_dumper.dumps(test_package, GITHUB_LD11_CONTEXT + "termci_schema_inlined.context.jsonld"),
    )


@pytest.mark.skip(reason="This needs an enhanced (https://github.com/hsolbrig/pyld) version of pyld")
def test_rdf_dumper(test_package):
    """Test the rdf dumper"""
    contexts = os.path.join(LD_11_DIR, "termci_schema_inlined.context.jsonld")
    dump_test(
        "obo_sample.ttl",
        lambda out_file: rdf_dumper.dump(test_package, out_file, contexts),
        comparator=ClickTestCase.rdf_comparator,
    )

    g = rdf_dumper.as_rdf_graph(test_package, contexts)
    assert OBO[""] in g.subjects()
    assert NCIT.C147796 in g.subjects()
    assert Literal("C147796") in g.objects(NCIT.C147796, SKOS.notation)

    dumps_test(
        "obo_sample.ttl",
        lambda: rdf_dumper.dumps(test_package, contexts),
        comparator=ClickTestCase.rdf_comparator,
    )

    # Build a vanilla jsonld image for subsequent testing
    fname = "obo_sample.jsonld"
    dump_test(
        fname,
        lambda out_file: rdf_dumper.dump(test_package, out_file, contexts, fmt="json-ld"),
        comparator=lambda e, a: ClickTestCase.rdf_comparator(e, a, fmt="json-ld"),
    )
    with open(env.expected_path("dump", fname)) as f:
        txt = f.read()
    with open(env.input_path("obo_sample.jsonld"), "w") as f:
        f.write(txt)


@pytest.mark.skip(reason="Waiting until PyLD learns to handle relative context URI's")
def test_nested_contexts(test_package):
    """Test JSON-LD with fully nested contexts"""
    from tests.test_loaders_dumpers.loaderdumpertestcase import LoaderDumperTestCase

    context_servers = []
    for possible_server in [LD_11_SVR, LD_11_SSL_SVR]:
        svr = LoaderDumperTestCase.check_context_servers([possible_server])
        if svr:
            context_servers.append(svr)

    if not context_servers:
        pytest.skip(
            f"*****> Nested contexts test skipped - no servers found on sockets {HTTP_TEST_PORT} or {HTTPS_TEST_PORT}"
        )

    for context_base in context_servers:
        nested_context = context_base + "Package.context.jsonld"
        dump_test("obo_sample_nested.ttl", lambda out_file: rdf_dumper.dump(test_package, out_file, nested_context))
        dumps_test("obo_sample_nested.ttl", lambda: rdf_dumper.dumps(test_package, nested_context))
