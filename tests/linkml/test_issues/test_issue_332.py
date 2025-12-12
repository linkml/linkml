from jsonasobj2 import JsonObj, as_json, loads

from linkml.generators.jsonldgen import JSONLDGenerator


def test_context(input_path):
    """Test no context in the argument"""
    json_ld = JSONLDGenerator(input_path("issue_332.yaml")).serialize()
    json_ld_obj = loads(json_ld)
    expected = JsonObj(
        [
            "https://w3id.org/linkml/meta.context.jsonld",
            {
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                "meta": "https://w3id.org/linkml/",
                "test14": "https://example.com/test14/",
                "@vocab": "https://example.com/test14/",
            },
            {"@base": "https://example.com/test14/"},
        ]
    )
    assert as_json(expected) == as_json(json_ld_obj["@context"])


def test_context_2(input_path):
    """Test a single context argument"""
    json_ld = JSONLDGenerator(input_path("issue_332.yaml")).serialize(
        context="http://some.org/nice/meta.context.jsonld"
    )
    json_ld_obj = loads(json_ld)
    expected = JsonObj(
        [
            "http://some.org/nice/meta.context.jsonld",
            {"@base": "https://example.com/test14/"},
        ]
    )
    assert as_json(expected) == as_json(json_ld_obj["@context"])


def test_context_3(input_path):
    """Test multi context arguments"""
    json_ld = JSONLDGenerator(input_path("issue_332.yaml")).serialize(
        context=[
            "http://some.org/nice/meta.context.jsonld",
            "http://that.org/meta.context.jsonld",
        ]
    )
    json_ld_obj = loads(json_ld)
    expected = JsonObj(
        [
            "http://some.org/nice/meta.context.jsonld",
            "http://that.org/meta.context.jsonld",
            {"@base": "https://example.com/test14/"},
        ]
    )
    assert as_json(expected) == as_json(json_ld_obj["@context"])
