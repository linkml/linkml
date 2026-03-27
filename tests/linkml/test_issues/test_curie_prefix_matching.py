from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.yamlgen import YAMLGenerator


def test_multi_curies(input_path, snapshot, bundled_snapshot_text):
    schema = input_path("curie_prefix_matching.yaml")
    outputs: dict[str, str] = {}

    output = YAMLGenerator(schema).serialize()
    outputs["curie_prefix_matching.yaml"] = output

    output = ContextGenerator(schema).serialize()
    outputs["curie_prefix_matching.context.jsonld"] = output

    assert bundled_snapshot_text(outputs) == snapshot("curie_prefix_matching.txt")


def test_curie_case(input_path, snapshot, bundled_snapshot_text):
    schema = input_path("curie_case.yaml")
    outputs: dict[str, str] = {}

    output = YAMLGenerator(schema).serialize()
    outputs["curie_case.yaml"] = output

    output = ContextGenerator(schema).serialize()
    outputs["curie_case.context.jsonld"] = output

    assert bundled_snapshot_text(outputs) == snapshot("curie_case.txt")
