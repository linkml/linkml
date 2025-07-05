from __future__ import annotations

from copy import deepcopy

import pytest

from linkml_runtime.linkml_model import (
    ClassDefinition,
    EnumDefinition,
    Prefix,
    SchemaDefinition,
    SlotDefinition,
    SubsetDefinition,
    TypeDefinition,
)
from linkml_runtime.utils.schemaview import SchemaView

ELEMENTS = ["prefixes", "classes", "slots", "enums", "types", "subsets"]
EXPECTED = {
    "prefixes": {"sc1p1", "sc2p1"},
    "classes": {"sc1c1", "sc1c2", "sc2c1", "sc2c2"},
    "slots": {"sc1s1", "sc1s2", "sc2s1", "sc2s2"},
    "enums": {"sc1e1", "sc2e1"},
    "types": {"sc1t1", "sc2t1"},
    "subsets": {"sc1ss1", "sc2ss1"},
}


def make_schema(
    name: str,
    prefixes: list[Prefix] | None = None,
    classes: list[ClassDefinition] | None = None,
    slots: list[SlotDefinition] | None = None,
    enums: list[EnumDefinition] | None = None,
    types: list[TypeDefinition] | None = None,
    subsets: list[SubsetDefinition] | None = None,
) -> SchemaView:
    """Make a schema with the given elements.

    :param name:
    :param prefixes:
    :param classes:
    :param slots:
    :param enums:
    :param types:
    :param subsets:
    :return:
    """
    schema = SchemaDefinition(id=name, name=name)
    if prefixes:
        for p in prefixes:
            schema.prefixes[p.prefix_prefix] = p
    if classes:
        for c in classes:
            schema.classes[c.name] = c
    if slots:
        for s in slots:
            schema.slots[s.name] = s
    if enums:
        for e in enums:
            schema.enums[e.name] = e
    if types:
        for t in types:
            schema.types[t.name] = t
    if subsets:
        for s in subsets:
            schema.subsets[s.name] = s
    return SchemaView(schema)


"""
https://github.com/linkml/linkml/issues/1143
"""


@pytest.fixture
def sv1() -> SchemaView:
    return make_schema(
        "s1",
        prefixes=[Prefix(prefix_prefix="sc1p1", prefix_reference="http://example.org/sc1url1")],
        classes=[ClassDefinition(name="sc1c1", slots=["sc1s1"]), ClassDefinition(name="sc1c2", slots=["sc1s2"])],
        slots=[SlotDefinition(name="sc1s1", range="string"), SlotDefinition(name="sc1s2", range="float")],
        enums=[
            EnumDefinition(
                name="sc1e1",
                permissible_values={
                    "sc1e1v1": "sc1e1v1",
                },
            )
        ],
        types=[TypeDefinition(name="sc1t1", base="string")],
        subsets=[SubsetDefinition(name="sc1ss1", description="sc1ss1")],
    )


@pytest.fixture
def sv2() -> SchemaView:
    return make_schema(
        "s2",
        prefixes=[Prefix(prefix_prefix="sc2p1", prefix_reference="http://example.org/sc2url1")],
        classes=[ClassDefinition(name="sc2c1", slots=["sc2s1"]), ClassDefinition(name="sc2c2", slots=["sc2s2"])],
        slots=[SlotDefinition(name="sc2s1", range="string"), SlotDefinition(name="sc2s2", range="float")],
        enums=[
            EnumDefinition(
                name="sc2e1",
                permissible_values={
                    "sc2e1v1": "sc2e1v1",
                },
            )
        ],
        types=[TypeDefinition(name="sc2t1", base="string")],
        subsets=[SubsetDefinition(name="sc2ss1", description="sc2ss1")],
    )


@pytest.fixture
def empty_schema() -> SchemaView:
    return make_schema("s3")


def is_identical(s1: SchemaDefinition, s2: SchemaDefinition) -> None:
    """Compare two schemas for strict identity.

    :param s1: schema 1
    :param s2: schema 2
    :return:
    """
    for k in ELEMENTS:
        assert getattr(s1, k) == getattr(s2, k)


def test_merge_empty(sv1: SchemaView, empty_schema: SchemaView) -> None:
    """Trivial case: merge a schema into an empty schema."""
    empty_schema.merge_schema(sv1.schema)
    is_identical(empty_schema.schema, sv1.schema)


def test_merge_empty_rev(sv1: SchemaView, empty_schema: SchemaView) -> None:
    """Trivial case: merge an empty schema into a non-empty schema."""
    sv1_orig = deepcopy(sv1)
    sv1.merge_schema(empty_schema.schema)
    is_identical(sv1_orig.schema, sv1.schema)


def test_merge_schema(sv1: SchemaView, sv2: SchemaView) -> None:
    """Merge two schemas with disjoint elements."""
    sv2.merge_schema(sv1.schema)

    for k, vs in EXPECTED.items():
        assert set(getattr(sv2.schema, k).keys()) == vs


def _get_clobbered_field_val(element: str) -> tuple[str, str]:
    if element == "prefixes":
        return "prefix_reference", "http://example.org/clobbered"
    return "description", "clobbered"


def test_no_clobber(sv1: SchemaView, sv2: SchemaView) -> None:
    """Merge non-disjoint schemas, ensuring that elements in the source schema are not clobbered."""
    sv2.merge_schema(sv1.schema)
    for element in ELEMENTS:
        (field, val) = _get_clobbered_field_val(element)
        for v in getattr(sv1.schema, element).values():
            setattr(v, field, val)

    sv2.merge_schema(sv1.schema, clobber=False)
    for element in ELEMENTS:
        (field, val) = _get_clobbered_field_val(element)
        for k, v in getattr(sv2.schema, element).items():
            if k in getattr(sv1.schema, element):
                assert getattr(v, field) != val


def test_clobber(sv1: SchemaView, sv2: SchemaView) -> None:
    """Merge non-disjoint schemas, ensuring that elements in source schema are clobbered."""
    sv2.merge_schema(sv1.schema)
    for element in ELEMENTS:
        (field, val) = _get_clobbered_field_val(element)
        for v in getattr(sv1.schema, element).values():
            setattr(v, field, val)

    sv2.merge_schema(sv1.schema, clobber=True)
    for element in ELEMENTS:
        (field, val) = _get_clobbered_field_val(element)
        for k, v in getattr(sv2.schema, element).items():
            if k in getattr(sv1.schema, element):
                assert getattr(v, field) == val
