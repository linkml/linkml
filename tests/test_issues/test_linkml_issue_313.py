from linkml.generators.yamlgen import YAMLGenerator

# Tests: https://github.com/linkml/linkml/issues/313


def test_roundtrip(input_path, tmp_path):
    name = "linkml_issue_313"
    inpath = input_path(f"{name}.yaml")
    outpath = str(tmp_path / f"{name}-roundtrip.yaml")
    gen = YAMLGenerator(inpath)
    gen.serialize(output=outpath)
    schema = gen.schema
    assert "c1" in schema.classes
    c1 = schema.classes["c1"]
    assert c1.id_prefixes == ["c1val"]
    e1 = schema.enums["e1"]
    pv = list(e1.permissible_values.values())[0]
    assert pv.text == "v1"
    assert pv.description == "v1val"
