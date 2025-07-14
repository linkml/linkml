import logging

from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)


schema_str = """
id: https://example.com/test-induced
name: test-induced
title: test induced

description: >-
    test schema view's finding of induced slot information.

classes:
    class1:
        slots:
            - slot1
            - slot2
            - slot3
        slot_usage:
            slot2:
                description: induced slot2
                required: true
                range: class1
    class2:
        is_a: class1

    mixin1a:
        mixin: true
        slot_usage:
            slot2:
                description: mixin slot2
                required: false
                range: mixin1a

    mixin1b:
        mixin: true
        slot_usage:
            slot2:
                description: mixin slot2
                required: false
                range: mixin1b

    class2_1a:
        is_a: class2
        mixins:
          - mixin1a
          - mixin1b

    class2_1b:
        is_a: class2
        mixins:
          - mixin1b
          - mixin1a

    class0:

slots:
    slot1:
        description: non-induced slot1
        range: class0
    slot2:
        description: non-induced slot2
        required: false
        range: class0
    slot3:
        range: class0

"""


def test_induced_slots() -> None:
    """Test induced slots and load order of mixins and is_a.

    See https://github.com/linkml/linkml/issues/479 and
    https://github.com/linkml/linkml-runtime/issues/68 for details.
    """
    view = SchemaView(schema_str)

    # test descripton for slot1
    s1 = view.get_slot("slot1")
    assert s1.description == "non-induced slot1"
    assert s1.range == "class0"

    s2 = view.get_slot("slot2")
    assert not s2.required
    assert s2.range == "class0"

    s2_induced = view.induced_slot("slot2", "class1")
    assert s2_induced.required
    assert s2_induced.range == "class1"

    # test description for slot2
    # this behavior is expected see: https://github.com/linkml/linkml-runtime/issues/68
    assert s2_induced.description == "induced slot2"

    s2_induced_c2 = view.induced_slot("slot2", "class2")
    assert s2_induced_c2.required
    assert s2_induced_c2.description == "induced slot2"
    assert s2_induced.range == "class1"

    s3_induced_c2 = view.induced_slot("slot3", "class2")
    assert not s3_induced_c2.required
    assert s3_induced_c2.description is None
    assert s3_induced_c2.range == "class0"

    # mixins take priority over is-a
    # mixins specified in order of priority
    s2_induced_c2_1a = view.induced_slot("slot2", "class2_1a")
    assert not s2_induced_c2_1a.required
    assert s2_induced_c2_1a.description == "mixin slot2"
    assert s2_induced_c2_1a.range == "mixin1a"

    s2_induced_c2_1b = view.induced_slot("slot2", "class2_1b")
    assert not s2_induced_c2_1b.required
    assert s2_induced_c2_1b.description == "mixin slot2"
    assert s2_induced_c2_1b.range == "mixin1b"
