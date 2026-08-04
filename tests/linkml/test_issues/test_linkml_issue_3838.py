from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.loaders import json_loader


def test_uriorcurie_designator_uses_full_class_uri_when_curie_is_unavailable():
    schema = """
id: https://example.org/designator-test
name: designator_test

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

default_prefix: ex

imports:
  - linkml:types

slots:
  schema_type:
    range: uriorcurie
    designates_type: true

classes:
  Association:
    class_uri: https://unregistered.example/Association
    slots:
      - schema_type
"""
    expected = "https://unregistered.example/Association"
    model = PythonGenerator(schema).compile_module()

    constructed = model.Association()
    loaded = json_loader.load({"schema_type": expected}, target_class=model.Association)

    assert constructed.schema_type == expected
    assert loaded.schema_type == expected
