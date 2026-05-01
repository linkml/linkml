"""Tests for the InstantiatesValidationPlugin."""

import pytest

from linkml.validator.plugins.instantiates_validation_plugin import (
    InstantiatesValidationPlugin,
    check_instantiates_constraints,
)
from linkml.validator.report import Severity
from linkml.validator.validation_context import ValidationContext
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView

# ---------------------------------------------------------------------------
# Test schemas
# ---------------------------------------------------------------------------

SCHEMA_WITH_VIOLATIONS = """\
id: https://w3id.org/test/instantiates
name: instantiates_test
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
  linkml: https://w3id.org/linkml/
default_range: string

types:
  string:
    uri: xsd:string
    base: str

classes:
  ValueMicroschemaDefinition:
    annotations:
      must_not_have_id_slot: true
      must_be_inlined: true

  BadQuantity:
    instantiates:
      - ValueMicroschemaDefinition
    attributes:
      id:
        identifier: true
      value:

  Container:
    tree_root: true
    attributes:
      quantities:
        range: BadQuantity
        multivalued: true
"""

SCHEMA_COMPLIANT = """\
id: https://w3id.org/test/instantiates_ok
name: instantiates_ok
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
  linkml: https://w3id.org/linkml/
default_range: string

types:
  string:
    uri: xsd:string
    base: str

classes:
  ValueMicroschemaDefinition:
    annotations:
      must_not_have_id_slot: true
      must_be_inlined: true

  GoodQuantity:
    instantiates:
      - ValueMicroschemaDefinition
    attributes:
      value:

  Container:
    tree_root: true
    attributes:
      quantities:
        range: GoodQuantity
        multivalued: true
        inlined_as_list: true
"""

SCHEMA_UNRESOLVABLE = """\
id: https://w3id.org/test/instantiates_missing
name: instantiates_missing
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
default_range: string

types:
  string:
    uri: xsd:string
    base: str

classes:
  MyClass:
    tree_root: true
    instantiates:
      - NonExistentClass
    attributes:
      value:
"""

SCHEMA_NO_ANNOTATIONS = """\
id: https://w3id.org/test/instantiates_no_ann
name: instantiates_no_ann
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
default_range: string

types:
  string:
    uri: xsd:string
    base: str

classes:
  BaseDef:
    description: A base class with no constraint annotations

  MyClass:
    tree_root: true
    instantiates:
      - BaseDef
    attributes:
      id:
        identifier: true
      value:
"""

SCHEMA_ONLY_ID_VIOLATION = """\
id: https://w3id.org/test/instantiates_id_only
name: instantiates_id_only
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
default_range: string

types:
  string:
    uri: xsd:string
    base: str

classes:
  NoIdDef:
    annotations:
      must_not_have_id_slot: true

  HasId:
    instantiates:
      - NoIdDef
    attributes:
      id:
        identifier: true
      value:

  Container:
    tree_root: true
    attributes:
      items:
        range: HasId
        multivalued: true
        inlined_as_list: true
"""

SCHEMA_ONLY_INLINE_VIOLATION = """\
id: https://w3id.org/test/instantiates_inline_only
name: instantiates_inline_only
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
default_range: string

types:
  string:
    uri: xsd:string
    base: str

classes:
  InlineDef:
    annotations:
      must_be_inlined: true

  NoIdClass:
    instantiates:
      - InlineDef
    attributes:
      value:

  Container:
    tree_root: true
    attributes:
      items:
        range: NoIdClass
        multivalued: true
"""

SCHEMA_MULTIPLE_INSTANTIATES = """\
id: https://w3id.org/test/instantiates_multi
name: instantiates_multi
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
default_range: string

types:
  string:
    uri: xsd:string
    base: str

classes:
  NoIdDef:
    annotations:
      must_not_have_id_slot: true

  InlineDef:
    annotations:
      must_be_inlined: true

  MultiClass:
    instantiates:
      - NoIdDef
      - InlineDef
    attributes:
      id:
        identifier: true
      value:

  Container:
    tree_root: true
    attributes:
      items:
        range: MultiClass
        multivalued: true
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _results_from_schema(schema_str: str) -> list:
    """Run check_instantiates_constraints on an inline schema string."""
    sv = SchemaView(schema_str)
    return list(check_instantiates_constraints(sv))


def _make_context(schema_str: str, target_class: str) -> ValidationContext:
    schema = yaml_loader.load(schema_str, SchemaDefinition)
    return ValidationContext(schema, target_class)


# ---------------------------------------------------------------------------
# Tests for check_instantiates_constraints (core logic)
# ---------------------------------------------------------------------------


def test_violations_detected():
    """Schema with both id-slot and non-inlined violations should report errors."""
    results = _results_from_schema(SCHEMA_WITH_VIOLATIONS)
    messages = [r.message for r in results]
    assert any("identifier slot" in m and "BadQuantity" in m for m in messages)
    assert any("inlined" in m and "BadQuantity" in m for m in messages)
    assert all(r.severity == Severity.ERROR for r in results)


def test_compliant_schema_no_results():
    """A fully compliant schema should produce no results."""
    results = _results_from_schema(SCHEMA_COMPLIANT)
    assert results == []


def test_unresolvable_instantiates():
    """An unresolvable instantiates target should produce a warning."""
    results = _results_from_schema(SCHEMA_UNRESOLVABLE)
    assert len(results) == 1
    assert results[0].severity == Severity.WARN
    assert "NonExistentClass" in results[0].message
    assert "could not be resolved" in results[0].message


def test_no_annotations_no_results():
    """If the instantiated class has no constraint annotations, no errors."""
    results = _results_from_schema(SCHEMA_NO_ANNOTATIONS)
    assert results == []


def test_only_id_slot_violation():
    """Only the must_not_have_id_slot annotation is present and violated."""
    results = _results_from_schema(SCHEMA_ONLY_ID_VIOLATION)
    assert len(results) == 1
    assert "identifier slot" in results[0].message
    assert results[0].severity == Severity.ERROR


def test_only_inline_violation():
    """Only the must_be_inlined annotation is present and violated."""
    results = _results_from_schema(SCHEMA_ONLY_INLINE_VIOLATION)
    assert len(results) == 1
    assert "inlined" in results[0].message
    assert results[0].severity == Severity.ERROR


def test_multiple_instantiates():
    """A class instantiating multiple targets picks up annotations from all."""
    results = _results_from_schema(SCHEMA_MULTIPLE_INSTANTIATES)
    messages = [r.message for r in results]
    assert any("identifier slot" in m for m in messages)
    assert any("inlined" in m for m in messages)


# ---------------------------------------------------------------------------
# Tests for InstantiatesValidationPlugin (plugin interface)
# ---------------------------------------------------------------------------


def test_plugin_yields_results_on_first_process():
    """Plugin should yield schema-level results on the first process() call."""
    context = _make_context(SCHEMA_WITH_VIOLATIONS, "Container")
    plugin = InstantiatesValidationPlugin()
    plugin.pre_process(context)

    results = list(plugin.process({"quantities": []}, context))
    assert len(results) > 0
    assert all(r.type == "instantiates" for r in results)


def test_plugin_yields_results_only_once():
    """Plugin should yield results only on the first process() call."""
    context = _make_context(SCHEMA_WITH_VIOLATIONS, "Container")
    plugin = InstantiatesValidationPlugin()
    plugin.pre_process(context)

    first_results = list(plugin.process({"quantities": []}, context))
    assert len(first_results) > 0

    second_results = list(plugin.process({"quantities": []}, context))
    assert len(second_results) == 0


def test_plugin_no_results_for_compliant_schema():
    """Plugin should yield no results for a compliant schema."""
    context = _make_context(SCHEMA_COMPLIANT, "Container")
    plugin = InstantiatesValidationPlugin()
    plugin.pre_process(context)

    results = list(plugin.process({"quantities": []}, context))
    assert results == []


@pytest.mark.parametrize(
    "schema_str,expected_count",
    [
        (SCHEMA_WITH_VIOLATIONS, 2),
        (SCHEMA_COMPLIANT, 0),
        (SCHEMA_UNRESOLVABLE, 1),
        (SCHEMA_NO_ANNOTATIONS, 0),
        (SCHEMA_ONLY_ID_VIOLATION, 1),
        (SCHEMA_ONLY_INLINE_VIOLATION, 1),
    ],
    ids=[
        "both_violations",
        "compliant",
        "unresolvable",
        "no_annotations",
        "id_only",
        "inline_only",
    ],
)
def test_result_counts(schema_str, expected_count):
    """Parametrized check of expected result counts across schemas."""
    results = _results_from_schema(schema_str)
    assert len(results) == expected_count
