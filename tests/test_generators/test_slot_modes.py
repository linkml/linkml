from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators.rustgen.rustgen import (
    SlotContainerMode,
    SlotInlineMode,
    determine_slot_mode,
)


def test_determine_slot_mode(kitchen_sink_path):
    sv = SchemaView(kitchen_sink_path)

    age_slot = sv.get_slot("age in years")
    assert determine_slot_mode(age_slot, sv) == (
        SlotContainerMode.SINGLE_VALUE,
        SlotInlineMode.PRIMITIVE,
    )

    aliases_slot = sv.get_slot("aliases")
    assert determine_slot_mode(aliases_slot, sv) == (
        SlotContainerMode.LIST,
        SlotInlineMode.PRIMITIVE,
    )

    hist_slot = sv.get_slot("has employment history")
    assert determine_slot_mode(hist_slot, sv) == (
        SlotContainerMode.LIST,
        SlotInlineMode.INLINE,
    )

    employed_slot = sv.get_slot("employed at")
    assert determine_slot_mode(employed_slot, sv) == (
        SlotContainerMode.SINGLE_VALUE,
        SlotInlineMode.REFERENCE,
    )
