from linkml.generators.javagen import JavaGenerator


def test_slot_uri_on_locally_defined_attribute(input_path):
    """The generator should produce the correct slot_uri for a locally defined attribute."""
    gen = JavaGenerator(input_path("linkml_issue_3677.yaml"))
    docs = gen.create_documents()
    witness = [doc for doc in docs if doc.name == "PrefixDeclaration"][0]
    assert witness.classes[0].fields[0].slot_uri == "http://www.w3.org/ns/shacl#prefix"
    assert witness.classes[0].fields[1].slot_uri == "http://www.w3.org/ns/shacl#namespace"
