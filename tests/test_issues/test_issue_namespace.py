import pytest

from linkml.generators.rdfgen import RDFGenerator


# TODO: Find out why test_issue_namespace is emitting generation_date in the TYPE namespace
@pytest.mark.skip(reason="non-deterministic, see https://github.com/linkml/linkml/issues/1650")
def test_namespace(input_path, snapshot):
    # TODO: Do not depend on an external URL whose content may change
    context = "https://biolink.github.io/biolink-model/context.jsonld"
    output = RDFGenerator(input_path("issue_namespace.yaml")).serialize(context=context)
    assert output == snapshot("issue_namespace.ttl")
