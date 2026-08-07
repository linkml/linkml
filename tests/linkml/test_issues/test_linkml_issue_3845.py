from linkml_runtime.utils.schemaview import SchemaView


def test_zero_valued_constraint_is_inherited(input_path):
    """A parent's ``minimum_value`` of 0 must survive onto the child slot.

    ``induced_slot`` used to treat 0 as unset, so the constraint disappeared instead
    of failing and a negative value passed a slot whose parent said the minimum was
    zero.

    Tests https://github.com/linkml/linkml/issues/3845
    """
    view = SchemaView(input_path("linkml_issue_3845.yaml"))

    assert view.induced_slot("inherits_bound", "TestClass").minimum_value == 0


def test_inherited_boolean_is_not_cleared_by_child(input_path):
    """A child's ``required: false`` must NOT clear a parent's ``required: true``.

    The issue originally reported this as a second bug. It is not one: the Combine
    Slots algorithm, the specification's rules for merging a slot with its parent,
    combines boolean metaslots with ``v1 OR v2``, so ``True`` wins. Pinned here so
    the fix for the zero case above is never widened into an off-specification
    change.

    https://linkml.io/linkml-model/latest/docs/specification/04derived-schemas/#algorithm-combine-slots

    Tests https://github.com/linkml/linkml/issues/3845
    """
    view = SchemaView(input_path("linkml_issue_3845.yaml"))

    assert view.induced_slot("opts_out_of_required", "TestClass").required is True
