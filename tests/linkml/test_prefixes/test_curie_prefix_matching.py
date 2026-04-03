import json

import pytest
import yaml

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.yamlgen import YAMLGenerator
from tests.linkml.test_prefixes.environment import env

pytestmark = pytest.mark.xdist_group("prefixes")


def test_longest_prefix_wins_for_context_terms():
    schema = env.input_path("curie_prefix_matching.yaml")

    generated_yaml = yaml.safe_load(YAMLGenerator(schema).serialize())
    assert generated_yaml["types"]["t1"]["uri"] == "p1:c/suffix1"
    assert generated_yaml["types"]["t2"]["uri"] == "p2:suffix2"
    assert generated_yaml["types"]["t3"]["uri"] == "http://example.org/prefixes/a/b/c/suffix3"

    generated_context = json.loads(ContextGenerator(schema).serialize())["@context"]
    assert generated_context["C1"]["@id"] == "p1:/c/c1"
    assert generated_context["C2"]["@id"] == "p2:/c2"
    assert generated_context["C3"]["@id"] == "p2:c3"


def test_prefix_case_is_canonicalized_in_context():
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
