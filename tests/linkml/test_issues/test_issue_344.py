import json

from linkml.generators.jsonldcontextgen import ContextGenerator


def test_issue_344(input_path, snapshot):
    """Test to check if prefixes of CURIEs from granular mappings show up in the json-ld context"""
    output = ContextGenerator(
        input_path("issue_344.yaml"),
        emit_metadata=False,
    ).serialize()
    assert output == snapshot("issue_344_context.json")

    context = json.loads(output)
    assert "PCO" in context["@context"]
    assert "PATO" in context["@context"]
    assert "GO" in context["@context"]
