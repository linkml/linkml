"""Unit tests for :func:`linkml.utils.schema_prefix_merge.materialize_prefixes`.

These test the helper in isolation (rather than through a generator round-trip)
so that every branch of the prefix-propagation logic is exercised directly:

* absolute prefixes from imported sub-schemas are copied onto the root schema
* pre-existing root prefixes are never overwritten
* relative prefix references (no ``://``) are skipped
* ``None`` prefix references are skipped without raising
* a ``None`` ``root.prefixes`` is initialised to an empty dict
* the operation is idempotent
"""

from __future__ import annotations

import pytest

from linkml.utils.schema_prefix_merge import materialize_prefixes
from linkml_runtime.linkml_model.meta import Prefix, SchemaDefinition
from linkml_runtime.utils.schemaview import SchemaView


def _prefix_with_none_reference(name: str) -> Prefix:
    """Build a Prefix whose reference is ``None`` (not constructible directly)."""
    pfx = Prefix(name, "placeholder")
    pfx.prefix_reference = None
    return pfx


@pytest.fixture
def schemaview_with_imported_child() -> SchemaView:
    """SchemaView whose root imports an in-memory ``child`` schema.

    The child declares one absolute prefix (``newp``), one prefix that collides
    with a differently-valued root prefix (``abs``), one relative prefix
    (``rel``) and one prefix with a ``None`` reference (``none``).
    """
    root = SchemaDefinition(id="https://example.org/root", name="root")
    root.imports.append("child")
    root.prefixes["abs"] = Prefix("abs", "https://example.org/PREEXISTING/")

    child = SchemaDefinition(id="https://example.org/child", name="child")
    child.prefixes["abs"] = Prefix("abs", "https://example.org/child-abs/")
    child.prefixes["newp"] = Prefix("newp", "https://example.org/newp/")
    child.prefixes["rel"] = Prefix("rel", "relative/path#")
    child.prefixes["none"] = _prefix_with_none_reference("none")

    sv = SchemaView(root)
    # Inject the in-memory child before the import closure is first computed so
    # that it is used instead of attempting to load a file named "child".
    sv.schema_map["child"] = child
    assert set(sv.imports_closure()) == {"root", "child"}
    return sv


def test_absolute_imported_prefix_is_propagated(schemaview_with_imported_child: SchemaView) -> None:
    materialize_prefixes(schemaview_with_imported_child)
    prefixes = schemaview_with_imported_child.schema.prefixes
    assert "newp" in prefixes
    assert prefixes["newp"].prefix_reference == "https://example.org/newp/"


def test_existing_prefix_is_not_overwritten(schemaview_with_imported_child: SchemaView) -> None:
    materialize_prefixes(schemaview_with_imported_child)
    prefixes = schemaview_with_imported_child.schema.prefixes
    # root's own "abs" wins over the child's differently-valued "abs"
    assert prefixes["abs"].prefix_reference == "https://example.org/PREEXISTING/"


def test_relative_prefix_reference_is_skipped(schemaview_with_imported_child: SchemaView) -> None:
    materialize_prefixes(schemaview_with_imported_child)
    assert "rel" not in schemaview_with_imported_child.schema.prefixes


def test_none_prefix_reference_is_skipped(schemaview_with_imported_child: SchemaView) -> None:
    materialize_prefixes(schemaview_with_imported_child)
    assert "none" not in schemaview_with_imported_child.schema.prefixes


def test_none_root_prefixes_is_initialised() -> None:
    root = SchemaDefinition(id="https://example.org/root", name="root")
    sv = SchemaView(root)
    sv.schema.prefixes = None
    # Must not raise on a None prefixes map; the branch initialises it in place.
    materialize_prefixes(sv)
    assert sv.schema.prefixes is not None


def test_materialize_is_idempotent(schemaview_with_imported_child: SchemaView) -> None:
    materialize_prefixes(schemaview_with_imported_child)
    first = {k: v.prefix_reference for k, v in schemaview_with_imported_child.schema.prefixes.items()}
    materialize_prefixes(schemaview_with_imported_child)
    second = {k: v.prefix_reference for k, v in schemaview_with_imported_child.schema.prefixes.items()}
    assert first == second
