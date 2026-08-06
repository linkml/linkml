"""Unit tests for prefix/element merging helpers in :mod:`linkml.utils.mergeutils`.

These exercise the merge helpers directly (rather than through a full
``SchemaLoader.resolve()``) so each branch is covered in isolation:

* :func:`merge_namespaces` propagates absolute prefixes from the mergee onto the
  target schema's ``prefixes`` dict, raises on genuine mismatches, and handles
  relative prefixes without failing.
* :func:`_structurally_equal` ignores provenance-only fields.
* :func:`merge_dicts` silently collapses identical sibling re-declarations but
  still raises on structurally different ones.
"""

from __future__ import annotations

import pytest

from linkml.utils.mergeutils import _structurally_equal, merge_dicts, merge_namespaces
from linkml_runtime.linkml_model.meta import ClassDefinition, Prefix, SchemaDefinition
from linkml_runtime.utils.namespaces import Namespaces


def _schema(name: str, **prefixes: str) -> SchemaDefinition:
    schema = SchemaDefinition(id=f"https://example.org/{name}", name=name)
    for pfx, ref in prefixes.items():
        schema.prefixes[pfx] = Prefix(pfx, ref)
    return schema


# ---------------------------------------------------------------------------
# merge_namespaces
# ---------------------------------------------------------------------------


def test_merge_namespaces_propagates_absolute_prefix_to_target() -> None:
    target = _schema("target")
    mergee = _schema("mergee", abs="https://example.org/abs/")
    ns = Namespaces()

    merge_namespaces(target, mergee, ns)

    assert "abs" in target.prefixes
    assert target.prefixes["abs"].prefix_reference == "https://example.org/abs/"
    assert str(ns["abs"]) == "https://example.org/abs/"


def test_merge_namespaces_does_not_overwrite_matching_prefix() -> None:
    target = _schema("target", abs="https://example.org/abs/")
    mergee = _schema("mergee", abs="https://example.org/abs/")

    merge_namespaces(target, mergee, Namespaces())

    assert target.prefixes["abs"].prefix_reference == "https://example.org/abs/"


def test_merge_namespaces_raises_on_absolute_mismatch() -> None:
    target = _schema("target", abs="https://example.org/one/")
    mergee = _schema("mergee", abs="https://example.org/two/")

    with pytest.raises(ValueError, match=r"Prefix: abs mismatch between target and mergee"):
        merge_namespaces(target, mergee, Namespaces())


def test_merge_namespaces_relative_prefix_propagated_from_shared_namespaces() -> None:
    """A relative prefix already resolved in the shared Namespaces is copied to target."""
    target = _schema("target")
    mergee = _schema("mergee", rel="relative/path#")
    ns = Namespaces()
    # Simulate another schema already having contributed the absolute form.
    ns["rel"] = "https://example.org/resolved/"

    merge_namespaces(target, mergee, ns)

    assert "rel" in target.prefixes
    assert target.prefixes["rel"].prefix_reference == "https://example.org/resolved/"


def test_merge_namespaces_relative_prefix_added_to_namespaces_when_unknown() -> None:
    target = _schema("target")
    mergee = _schema("mergee", rel="relative/path#")
    ns = Namespaces()

    merge_namespaces(target, mergee, ns)

    # Unknown relative prefix is registered in the shared Namespaces map...
    assert str(ns["rel"]) == "relative/path#"
    # ...but not forced onto the target schema's prefixes.
    assert "rel" not in target.prefixes


# ---------------------------------------------------------------------------
# _structurally_equal
# ---------------------------------------------------------------------------


def test_structurally_equal_ignores_provenance_fields() -> None:
    a = ClassDefinition("C", from_schema="https://example.org/a", imported_from="a")
    b = ClassDefinition("C", from_schema="https://example.org/b", imported_from="b")
    assert _structurally_equal(a, b)


def test_structurally_equal_detects_real_difference() -> None:
    a = ClassDefinition("C", from_schema="https://example.org/a")
    b = ClassDefinition("C", from_schema="https://example.org/a", description="different")
    assert not _structurally_equal(a, b)


# ---------------------------------------------------------------------------
# merge_dicts
# ---------------------------------------------------------------------------


def test_merge_dicts_collapses_identical_sibling_redeclaration() -> None:
    target = {"C": ClassDefinition("C", from_schema="https://example.org/a")}
    source = {"C": ClassDefinition("C", from_schema="https://example.org/b")}

    merge_dicts(target, source, imported_from=None, imported_from_uri=None, merge_imports=True)

    # Existing entry with its original provenance is retained.
    assert target["C"].from_schema == "https://example.org/a"


def test_merge_dicts_raises_on_structurally_different_redeclaration() -> None:
    target = {"C": ClassDefinition("C", from_schema="https://example.org/a")}
    source = {"C": ClassDefinition("C", from_schema="https://example.org/b", description="different")}

    with pytest.raises(ValueError, match=r"Conflicting URIs .* for item: C"):
        merge_dicts(target, source, imported_from=None, imported_from_uri=None, merge_imports=True)
