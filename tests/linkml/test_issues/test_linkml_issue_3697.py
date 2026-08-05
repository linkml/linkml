import pytest

from linkml.validator.plugins import JsonschemaValidationPlugin
from linkml.validator.validation_context import ValidationContext
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

SCHEMA = """
id: https://example.org/td-as-uriorcurie
name: td_as_uriorcurie
prefixes:
  linkml: https://w3id.org/linkml/
  domain: https://example.org/domain/
  model: https://example.org/model/
imports:
  - linkml:types
default_prefix: model
default_range: string

classes:
  Root:
    tree_root: true
    attributes:
      foos:
        range: Foo
        multivalued: true
        inlined: true
  Foo:
    class_uri: https://example.org/domain/Foo
    attributes:
      type:
        range: uriorcurie
        designates_type: true
  Bar:
    is_a: Foo
    class_uri: https://example.org/domain/Bar
"""


@pytest.mark.parametrize(
    "type_values",
    [
        ["domain:Foo", "domain:Bar"],
        [
            "https://example.org/domain/Foo",
            "https://example.org/domain/Bar",
        ],
    ],
)
def test_uriorcurie_type_designator_accepts_curies_and_uris(type_values):
    schema = yaml_loader.loads(SCHEMA, target_class=SchemaDefinition)
    context = ValidationContext(schema)
    plugin = JsonschemaValidationPlugin(closed=True)
    instance = {"foos": [{"type": type_value} for type_value in type_values]}

    assert list(plugin.process(instance, context)) == []
