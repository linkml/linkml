"""Runtime-only tests for ``EnumDefinitionImpl._registry`` (Phase 3 of #723).

These tests exercise the registry primitives without involving the
``pythongen`` generator or the ``SchemaView`` lookup helpers.
"""

import pytest

from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue
from linkml_runtime.utils.enumerations import EnumDefinitionImpl


class _Color(EnumDefinitionImpl):
    RED = PermissibleValue(text="RED")
    GREEN = PermissibleValue(text="GREEN")
    _defn = EnumDefinition(name="_Color")


SCHEMA_ID = "http://example.org/enum-registry-runtime"


@pytest.fixture(autouse=True)
def _isolate_registry():
    """Snapshot and restore the registry so tests don't leak entries."""
    snapshot = dict(EnumDefinitionImpl._registry)
    yield
    EnumDefinitionImpl._registry.clear()
    EnumDefinitionImpl._registry.update(snapshot)


def test_register_and_lookup() -> None:
    _Color._register(SCHEMA_ID, "_Color")
    assert EnumDefinitionImpl.for_schema_element(SCHEMA_ID, "_Color") is _Color


def test_for_schema_element_missing_returns_none() -> None:
    assert EnumDefinitionImpl.for_schema_element(SCHEMA_ID, "Absent") is None


def test_re_register_overwrites() -> None:
    _Color._register(SCHEMA_ID, "_Color")

    class _OtherColor(EnumDefinitionImpl):
        BLUE = PermissibleValue(text="BLUE")
        _defn = EnumDefinition(name="_Color")

    _OtherColor._register(SCHEMA_ID, "_Color")
    assert EnumDefinitionImpl.for_schema_element(SCHEMA_ID, "_Color") is _OtherColor


def test_registry_keyed_by_schema_id() -> None:
    _Color._register(SCHEMA_ID, "_Color")
    _Color._register(SCHEMA_ID + "/v2", "_Color")
    assert EnumDefinitionImpl.for_schema_element(SCHEMA_ID, "_Color") is _Color
    assert EnumDefinitionImpl.for_schema_element(SCHEMA_ID + "/v2", "_Color") is _Color
