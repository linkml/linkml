import pytest
import unittest

from linkml_runtime.utils.csvutils import get_configmap
from linkml_runtime.utils.schemaview import SchemaView
from tests.linkml_runtime.support.test_environment import TestEnvironmentTestCase
from tests.linkml_runtime.test_utils.environment import env


class CsvUtilTestCase(TestEnvironmentTestCase):
    env = env

    def test_null_configmap(self):
        get_configmap(None, "unknown")
        # TODO: with pytest, use captlog to verify the output
        # assert 'Index slot or schema not specified' in caplog.text

    def test_get_configmap(self):
        fname = env.input_path("kitchen_sink.yaml")
        schema = SchemaView(fname)
        get_configmap(schema, "unknown")


if __name__ == "__main__":
    unittest.main()


# =============================================================================
# pytest-style unit tests for annotation-based CSV configuration (issue #3041)
#
# These tests verify that annotations (list_syntax, list_delimiter) are
# readable from schema definitions. The actual loading/dumping behavior
# is tested in test_loaders_dumpers/test_csv_tsv_loader_dumper.py.
#
# Related issues:
# - https://github.com/linkml/linkml/issues/3041 (main issue)
# - https://github.com/linkml/linkml/issues/2581 (configurable syntax)
#
# Design: Schema-level annotations only (json-flattener GlobalConfig is global)
# - list_syntax: python (default, brackets) or plaintext (no brackets)
# - list_delimiter: character between values (default "|")
# - Logic is in loader/dumper, NOT in csvutils.py
# =============================================================================


# -----------------------------------------------------------------------------
# Inline test schemas for annotation testing
#
# We use inline schemas here because:
# 1. The existing personinfo.yaml doesn't have list_syntax/list_delimiter annotations
# 2. Inline schemas make tests self-documenting - you can see exactly what's tested
# 3. We can test various annotation combinations without modifying shared fixtures
# -----------------------------------------------------------------------------

SCHEMA_WITH_LIST_ANNOTATIONS = """
id: https://example.org/test
name: test_annotations
description: >-
  Schema with list_syntax and list_delimiter annotations at the schema level.
  This tests the annotation-based configuration approach where:
  - list_syntax: plaintext -> csv_list_markers = ("", "") (no brackets)
  - list_delimiter: "|" -> csv_inner_delimiter = "|"
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
annotations:
  list_syntax: plaintext
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


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def schemaview_with_annotations():
    """Schema with list_syntax and list_delimiter annotations on slot."""
    return SchemaView(SCHEMA_WITH_LIST_ANNOTATIONS)


# -----------------------------------------------------------------------------
# Note on KeyConfig generation for multivalued primitive slots
#
# The _get_key_config() function in csvutils.py is NOT modified per Chris's
# guidance. Instead, the logic for handling multivalued primitive slots is
# implemented in the loader/dumper files:
# - delimited_file_loader.py: Enhances configmap after calling get_configmap()
# - delimited_file_dumper.py: Same pattern
#
# See test_loaders_dumpers/test_csv_tsv_loader_dumper.py for integration tests
# that verify multivalued primitive slots are correctly handled during
# CSV/TSV loading and dumping.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Unit tests: Reading annotations from schema
# -----------------------------------------------------------------------------


class TestListAnnotationReading:
    """
    Unit tests for reading list_syntax and list_delimiter annotations.

    These annotations control how multivalued fields are serialized in CSV/TSV:
    - list_syntax: "python" (default) -> [a|b|c] with brackets
    - list_syntax: "plaintext" -> a|b|c without brackets
    - list_delimiter: character used between values (default "|")
    """

    def test_schema_has_list_syntax_annotation(self, schemaview_with_annotations):
        """Schema-level annotations should be readable via SchemaView."""
        schema = schemaview_with_annotations.schema
        assert schema.annotations is not None
        assert "list_syntax" in schema.annotations
        assert schema.annotations["list_syntax"].value == "plaintext"

    def test_schema_has_list_delimiter_annotation(self, schemaview_with_annotations):
        """Schema-level annotations should include list_delimiter."""
        schema = schemaview_with_annotations.schema
        assert "list_delimiter" in schema.annotations
        assert schema.annotations["list_delimiter"].value == "|"
