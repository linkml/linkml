from linkml.generators.rdfgen import RDFGenerator


# TODO: Find out why test_issue_namespace is emitting generation_date in the TYPE namespace
def test_namespace(input_path, snapshot):
    context = "https://biolink.github.io/biolink-model/context.jsonld"
    output = RDFGenerator(input_path("issue_namespace.yaml")).serialize(context=context)
    assert output == snapshot("issue_namespace.ttl")
