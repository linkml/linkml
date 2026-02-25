import pytest

from linkml_runtime.utils.csvutils import get_configmap
from linkml_runtime.utils.schemaview import SchemaView
from tests.linkml_runtime.test_utils.environment import env


def test_null_configmap():
    get_configmap(None, "unknown")


def test_get_configmap():
    fname = env.input_path("kitchen_sink.yaml")
    schema = SchemaView(fname)
    get_configmap(schema, "unknown")


SCHEMA_WITH_LIST_ANNOTATIONS = """
id: https://example.org/test
name: test_annotations
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
annotations:
  list_wrapper: none
  list_delimiter: "|"

classes:
  Container:
    tree_root: true
    slots:
      - items
  Item:
    slots:
      - id
      - name
      - tags

slots:
  items:
    range: Item
    multivalued: true
    inlined_as_list: true
  id:
    identifier: true
  name:
    range: string
  tags:
    range: string
    multivalued: true
"""


@pytest.fixture
def schemaview_with_annotations():
    """Schema with list_wrapper and list_delimiter annotations."""
    return SchemaView(SCHEMA_WITH_LIST_ANNOTATIONS)


def test_schema_has_list_wrapper_annotation(schemaview_with_annotations):
    """Schema-level list_wrapper annotation should be readable via SchemaView."""
    schema = schemaview_with_annotations.schema
    assert schema.annotations is not None
    assert "list_wrapper" in schema.annotations
    assert schema.annotations["list_wrapper"].value == "none"


def test_schema_has_list_delimiter_annotation(schemaview_with_annotations):
    """Schema-level list_delimiter annotation should be readable via SchemaView."""
    schema = schemaview_with_annotations.schema
    assert "list_delimiter" in schema.annotations
    assert schema.annotations["list_delimiter"].value == "|"
