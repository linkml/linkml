import yaml
from linkml_runtime import SchemaView

from linkml.generators.linkmlgen import LinkmlGenerator


def test_generate(kitchen_sink_path):
    sv = SchemaView(kitchen_sink_path)
    assert "activity" in sv.all_classes(imports=True)
    assert "activity" not in sv.all_classes(imports=False)
    assert ["is_living"] == list(sv.get_class("Person").attributes.keys())

    gen = LinkmlGenerator(kitchen_sink_path, format="yaml", mergeimports=False)
    out = gen.serialize()
    # TODO: restore this when imports works for string inputs
    # schema2 = YAMLGenerator(out).schema
    # sv2 = SchemaView(schema2)
    # self.assertEqual(len(sv2.all_classes(imports=False)), len(sv.all_classes(imports=False)))
    # self.assertIn("activity", sv2.all_classes(imports=True))
    # self.assertNotIn("activity", sv2.all_classes(imports=False))
    # self.assertEqual([], list(sv2.get_class("Person").attributes.keys()))

    yobj = yaml.safe_load(out)
    assert len(yobj["classes"]) == len(sv.all_classes(imports=False))
    # self.assertNotIn("attributes", yobj["classes"]["Person"])
    # test with material-attributes option
    gen2 = LinkmlGenerator(kitchen_sink_path, format="yaml", mergeimports=False)
    gen2.materialize_attributes = True
    out2 = gen2.serialize()
    yobj2 = yaml.safe_load(out2)
    assert len(yobj2["classes"]) == len(sv.all_classes(imports=False))
    assert "attributes" in yobj2["classes"]["Person"]
    assert "activity" not in yobj2["classes"]
    assert "agent" not in yobj2["classes"]

    # turn on mergeimports option
    gen3 = LinkmlGenerator(kitchen_sink_path, format="yaml", mergeimports=True)
    out3 = gen3.serialize()
    yobj3 = yaml.safe_load(out3)
    assert len(yobj3["classes"]) == len(sv.all_classes(imports=True))
    assert "activity" in yobj3["classes"]
    assert "agent" in yobj3["classes"]


def test_structured_pattern(input_path):
    # test that structured patterns are being expanded
    # and populated into the pattern property on a class
    pattern_gen = LinkmlGenerator(
        str(input_path("pattern-example.yaml")),
        materialize_patterns=True,
        format="yaml",
    )

    pattern_gen.serialize()
    # log yaml_filename so developers can look at its contents
    assert pattern_gen.schemaview.get_slot("id").pattern == r"^P\d{7}"
    assert pattern_gen.schemaview.get_slot("height").pattern == "\\d+[\\.\\d+] (centimeter|meter|inch)"
    assert pattern_gen.schemaview.get_slot("weight").pattern == "\\d+[\\.\\d+] (kg|g|lbs|stone)"
