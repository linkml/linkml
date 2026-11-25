import yaml

from linkml.generators.yamlgen import YAMLGenerator

SCHEMA = """
name: Example
id: https://example.com/
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  ExampleClass:
    slots:
      - example_slot
    slot_usage:
      example_slot: {}
slots:
  example_slot:
    annotations:
      x: y
"""


def test_slot_usage_inherits_annotations():
    """A slot_usage entry without its own annotations inherits the slot's annotations
    and the schema can still be serialized to YAML.
    See https://github.com/linkml/linkml/issues/2805
    """
    out = YAMLGenerator(SCHEMA).serialize()
    slots = yaml.safe_load(out)["slots"]
    assert slots["example_slot"]["annotations"]["x"]["value"] == "y"
    assert slots["ExampleClass_example_slot"]["annotations"]["x"]["value"] == "y"


def test_slot_usage_own_annotations_merged():
    """A slot_usage entry with its own annotations keeps them next to the inherited ones."""
    schema = SCHEMA.replace("example_slot: {}", "example_slot:\n        annotations:\n          a: b")
    out = YAMLGenerator(schema).serialize()
    usage = yaml.safe_load(out)["slots"]["ExampleClass_example_slot"]
    assert usage["annotations"]["a"]["value"] == "b"
