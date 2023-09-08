from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.yamlgen import YAMLGenerator


def test_multi_curies(input_path, snapshot):
    schema = input_path("curie_prefix_matching.yaml")

    output = YAMLGenerator(schema).serialize()
    assert output == snapshot("curie_prefix_matching.yaml")

    output = ContextGenerator(schema).serialize()
    assert output == snapshot("curie_prefix_matching.context.jsonld")


def test_curie_case(input_path, snapshot):
    schema = input_path("curie_case.yaml")

    output = YAMLGenerator(schema).serialize()
    assert output == snapshot("curie_case.yaml")

    output = ContextGenerator(schema).serialize()
    assert output == snapshot("curie_case.context.jsonld")
