"""
Dual-flavor parity tests for SchemaView.

A SchemaView constructed with ``metamodel="pydantic"`` (backed by the
provisional pydantic metamodel) must answer queries identically to the
default dataclass-backed view.
"""

from pathlib import Path

import pytest
from pydantic import BaseModel

from linkml_runtime.utils.schemaview import SchemaView

INPUT_DIR = Path(__file__).parent / "input"
KITCHEN_SINK = str(INPUT_DIR / "kitchen_sink.yaml")


@pytest.fixture(scope="module")
def dataclass_view() -> SchemaView:
    return SchemaView(KITCHEN_SINK)


@pytest.fixture(scope="module")
def pydantic_view() -> SchemaView:
    return SchemaView(KITCHEN_SINK, metamodel="pydantic")


def test_flavor_attribute(dataclass_view: SchemaView, pydantic_view: SchemaView) -> None:
    """The flavor is recorded on the view and inferred from schema instances."""
    assert dataclass_view.metamodel_flavor == "dataclass"
    assert pydantic_view.metamodel_flavor == "pydantic"
    inferred = SchemaView(pydantic_view.schema)
    assert inferred.metamodel_flavor == "pydantic"


def test_imports_closure_uses_flavor(pydantic_view: SchemaView) -> None:
    """Imported schemas load into the same metamodel flavor as the root schema."""
    pydantic_view.imports_closure()
    for schema in pydantic_view.schema_map.values():
        assert isinstance(schema, BaseModel), f"{schema.name} is not a pydantic schema"


@pytest.mark.parametrize(
    "query",
    [
        pytest.param(lambda sv: sorted(sv.all_classes()), id="all_classes"),
        pytest.param(lambda sv: sorted(sv.all_slots()), id="all_slots"),
        pytest.param(lambda sv: sorted(sv.all_enums()), id="all_enums"),
        pytest.param(lambda sv: sorted(sv.all_types()), id="all_types"),
        pytest.param(lambda sv: sorted(sv.all_subsets()), id="all_subsets"),
        pytest.param(lambda sv: sorted(sv.all_elements()), id="all_elements"),
        pytest.param(lambda sv: sv.class_ancestors("Person"), id="class_ancestors"),
        pytest.param(lambda sv: sorted(sv.class_descendants("Thing")), id="class_descendants"),
        pytest.param(lambda sv: sv.class_slots("Person"), id="class_slots"),
        pytest.param(
            lambda sv: [(s.name, str(s.range), s.multivalued) for s in sv.class_induced_slots("Person")],
            id="class_induced_slots",
        ),
        pytest.param(
            lambda sv: [(s.name, str(s.range)) for s in sv.class_induced_slots("MedicalEvent")],
            id="induced_slots_mixin",
        ),
        pytest.param(lambda sv: [sv.get_uri(c) for c in sorted(sv.all_classes())], id="get_uri_classes"),
        pytest.param(
            lambda sv: [sv.get_uri(s, native=True) for s in sorted(sv.all_slots())], id="get_uri_slots_native"
        ),
        pytest.param(
            lambda sv: [(s, sv.is_inlined(sv.induced_slot(s, "Person"))) for s in sv.class_slots("Person")],
            id="is_inlined",
        ),
        pytest.param(lambda sv: sorted(sv.usage_index()), id="usage_index"),
        pytest.param(lambda sv: sv.slot_ancestors("city"), id="slot_ancestors"),
        pytest.param(
            lambda sv: sorted((str(k), str(v)) for k, v in sv.namespaces().items()),
            id="namespaces",
        ),
    ],
)
def test_query_parity(dataclass_view: SchemaView, pydantic_view: SchemaView, query) -> None:
    """Both flavors give identical answers for read queries over kitchen_sink."""
    assert query(dataclass_view) == query(pydantic_view)


def test_induced_slot_metaslot_parity(dataclass_view: SchemaView, pydantic_view: SchemaView) -> None:
    """induced_slot agrees on every metaslot value (the mutation-heavy hot path)."""
    for class_name in sorted(dataclass_view.all_classes()):
        for slot_name in dataclass_view.class_slots(class_name):
            dc_slot = dataclass_view.induced_slot(slot_name, class_name)
            pyd_slot = pydantic_view.induced_slot(slot_name, class_name)
            for metaslot in ("name", "range", "required", "multivalued", "inlined", "alias", "owner", "domain_of"):
                dc_value, pyd_value = getattr(dc_slot, metaslot), getattr(pyd_slot, metaslot)
                # dataclass empty containers (e.g. domain_of) may be JsonObj-backed lists
                if isinstance(dc_value, list) or isinstance(pyd_value, list):
                    dc_value, pyd_value = list(dc_value or []), list(pyd_value or [])
                assert dc_value == pyd_value, f"{class_name}.{slot_name}.{metaslot}: {dc_value!r} != {pyd_value!r}"
