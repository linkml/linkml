from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.utils.schema_builder import SchemaBuilder
from linkml_runtime.utils.schemaview import SchemaView


def _view_with_parent_and_child(parent: SlotDefinition, child: SlotDefinition) -> SchemaView:
    """Build a schema where ``child`` inherits from ``parent`` and class ``C`` uses the child."""
    sb = SchemaBuilder()
    sb.add_slot(parent)
    sb.add_slot(child)
    sb.add_class("C", ["child"])
    sb.add_defaults()
    return SchemaView(sb.schema)


def test_zero_valued_constraint_is_inherited():
    """A parent's ``minimum_value`` of 0 must survive onto the child slot.

    The truthiness guard in ``induced_slot`` treated 0 as unset, so the constraint
    disappeared instead of failing and a negative value passed a slot whose parent
    said the minimum was zero.

    Tests https://github.com/linkml/linkml/issues/3845
    """
    view = _view_with_parent_and_child(
        SlotDefinition("parent", range="integer", minimum_value=0),
        SlotDefinition("child", is_a="parent"),
    )
    assert view.induced_slot("child", "C").minimum_value == 0


def test_inherited_boolean_is_not_cleared_by_child():
    """A child's ``required: false`` must NOT clear a parent's ``required: true``.

    The issue originally reported this as a second bug. It is not one: the Combine
    Slots algorithm combines boolean metaslots with ``v1 OR v2``, so ``True`` wins.
    Pinned here so the fix for the zero case above is never widened into an
    off-spec change.

    https://linkml.io/linkml-model/latest/docs/specification/04derived-schemas/#algorithm-combine-slots

    Tests https://github.com/linkml/linkml/issues/3845
    """
    view = _view_with_parent_and_child(
        SlotDefinition("parent", required=True),
        SlotDefinition("child", is_a="parent", required=False),
    )
    assert view.induced_slot("child", "C").required is True
