import unittest

from linkml_runtime import SchemaView


def test_slot_inheritance(input_path):
    """
    Tests: https://github.com/linkml/linkml/issues/774

    Ensures that mappings and
    """
    name = "linkml_issue_774"
    infile = input_path(f"{name}.yaml")
    sv = SchemaView(infile)
    slot = sv.induced_slot("s", "C")
    assert ["ex:1"] == slot.exact_mappings
    any_of_ranges = [x.range for x in slot.any_of]
    tc = unittest.TestCase()
    tc.assertCountEqual(["D", "E"], any_of_ranges)
    induced_c = sv.induced_class("C")
    # slots converted to attributes for derived view:
    # this allows local properties to be inlined
    assert [] == induced_c.slots
    assert ["s"] == list(induced_c.attributes.keys())
    slot = induced_c.attributes["s"]
    assert ["ex:1"] == slot.exact_mappings
    any_of_ranges = [x.range for x in slot.any_of]
    tc.assertCountEqual(["D", "E"], any_of_ranges)
