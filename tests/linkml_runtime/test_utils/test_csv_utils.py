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
# - https://github.com/turbomam/issues/issues/48 (tracking issue)
#
# Design from Chris Mungall (Dec 2025 rolling notes):
# - Schema/slot annotations: list_syntax (python|plaintext), list_delimiter
# - Slot-level annotations override schema-level settings
# - Maps to json-flattener: csv_list_markers, csv_inner_delimiter
# - IMPORTANT: Logic should be in loader/dumper, NOT in csvutils.py
# =============================================================================


# -----------------------------------------------------------------------------
# Inline test schemas for annotation testing
#
# We use inline schemas here because:
# 1. The existing personinfo.yaml doesn't have list_syntax/list_delimiter annotations
# 2. Inline schemas make tests self-documenting - you can see exactly what's tested
# 3. We can test various annotation combinations without modifying shared fixtures
# -----------------------------------------------------------------------------

SCHEMA_WITH_MULTIVALUED_PRIMITIVES = """
id: https://example.org/test
name: test_multivalued
description: >-
  Minimal schema for testing multivalued primitive slot handling in CSV/TSV.
  The 'tags' slot is multivalued with string range - the loader/dumper should
  build a KeyConfig so json-flattener knows to split/join on delimiter.
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

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

SCHEMA_WITH_LIST_ANNOTATIONS = """
id: https://example.org/test
name: test_annotations
description: >-
  Schema with list_syntax and list_delimiter annotations on a slot.
  This tests the annotation-based configuration approach where:
  - list_syntax: plaintext -> csv_list_markers = ("", "") (no brackets)
  - list_delimiter: "|" -> csv_inner_delimiter = "|"
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

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
    annotations:
      list_syntax: plaintext
      list_delimiter: "|"
"""

SCHEMA_WITH_SCHEMA_LEVEL_ANNOTATIONS = """
id: https://example.org/test
name: test_schema_annotations
description: >-
  Schema demonstrating schema-level settings with slot-level override.
  - Schema-level: list_syntax=plaintext, list_delimiter="|"
  - Slot 'categories' overrides with list_delimiter=";"
  This tests the cascading behavior where slot annotations take precedence.
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

default_range: string

settings:
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
      - tags
      - categories

slots:
  items:
    range: Item
    multivalued: true
    inlined_as_list: true
  id:
    identifier: true
  tags:
    multivalued: true
  categories:
    multivalued: true
    annotations:
      list_delimiter: ";"
"""


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def schemaview_multivalued():
    """Schema with multivalued primitive slots but no annotations."""
    return SchemaView(SCHEMA_WITH_MULTIVALUED_PRIMITIVES)


@pytest.fixture
def schemaview_with_annotations():
    """Schema with list_syntax and list_delimiter annotations on slot."""
    return SchemaView(SCHEMA_WITH_LIST_ANNOTATIONS)


@pytest.fixture
def schemaview_schema_level():
    """Schema with schema-level settings and slot-level override."""
    return SchemaView(SCHEMA_WITH_SCHEMA_LEVEL_ANNOTATIONS)


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

    def test_slot_has_list_syntax_annotation(self, schemaview_with_annotations):
        """Slot annotations should be readable via SchemaView."""
        slot = schemaview_with_annotations.get_slot("tags")
        assert slot.annotations is not None
        assert "list_syntax" in slot.annotations
        assert slot.annotations["list_syntax"].value == "plaintext"

    def test_slot_has_list_delimiter_annotation(self, schemaview_with_annotations):
        """Slot annotations should include list_delimiter."""
        slot = schemaview_with_annotations.get_slot("tags")
        assert "list_delimiter" in slot.annotations
        assert slot.annotations["list_delimiter"].value == "|"


# -----------------------------------------------------------------------------
# Unit tests: Building CSV config from annotations (to be implemented)
# -----------------------------------------------------------------------------


class TestCsvConfigFromAnnotations:
    """
    Unit tests for building CSV config from annotations.

    These tests are skipped until the implementation is complete.
    They define the expected behavior for the get_csv_list_config() function
    that will read annotations and return json-flattener configuration.
    """

    def test_get_csv_list_config_default(self, schemaview_multivalued):
        """Without annotations, should use default (python/bracket) style."""
        # This function doesn't exist yet - will be implemented
        # list_markers, inner_delimiter = get_csv_list_config(schemaview_multivalued, "tags")
        # assert list_markers == ("[", "]")  # default bracket style
        # assert inner_delimiter == "|"  # default pipe
        pytest.skip("get_csv_list_config not yet implemented")

    def test_get_csv_list_config_plaintext(self, schemaview_with_annotations):
        """With list_syntax=plaintext, should use empty markers."""
        # list_markers, inner_delimiter = get_csv_list_config(schemaview_with_annotations, "tags")
        # assert list_markers == ("", "")  # no brackets
        # assert inner_delimiter == "|"
        pytest.skip("get_csv_list_config not yet implemented")

    def test_schema_level_settings_cascade(self, schemaview_schema_level):
        """Schema-level settings should apply to all slots."""
        # tags should inherit schema-level settings
        # list_markers, inner_delimiter = get_csv_list_config(schemaview_schema_level, "tags")
        # assert list_markers == ("", "")
        # assert inner_delimiter == "|"
        pytest.skip("get_csv_list_config not yet implemented")

    def test_slot_annotation_overrides_schema(self, schemaview_schema_level):
        """Slot-level annotation should override schema-level setting."""
        # categories has list_delimiter=";" which overrides schema's "|"
        # list_markers, inner_delimiter = get_csv_list_config(schemaview_schema_level, "categories")
        # assert inner_delimiter == ";"
        pytest.skip("get_csv_list_config not yet implemented")


@pytest.mark.parametrize(
    "list_syntax,expected_markers",
    [
        ("python", ("[", "]")),
        ("plaintext", ("", "")),
        (None, ("[", "]")),  # default
    ],
)
def test_list_syntax_to_markers(list_syntax, expected_markers):
    """
    Different list_syntax values should produce correct csv_list_markers.

    This tests a helper function that converts the annotation value to
    the tuple format expected by json-flattener's GlobalConfig.
    """
    # markers = list_syntax_to_markers(list_syntax)
    # assert markers == expected_markers
    pytest.skip("list_syntax_to_markers not yet implemented")
