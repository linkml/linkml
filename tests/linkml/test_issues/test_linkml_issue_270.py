from linkml.generators.yamlgen import YAMLGenerator


def test_metaslot_inheritance(input_path):
    """
    Tests: https://github.com/linkml/linkml/issues/270

    """
    name = "linkml_issue_270"
    infile = input_path(f"{name}.yaml")
    gen = YAMLGenerator(infile)
    schema = gen.schema
    s = schema.slots["s1"]
    c2_s1 = schema.slots["C2_s1"]
    assert c2_s1.alias == s.name
    assert c2_s1.owner == "C2"

    for k in [
        "description",
        "comments",
        "todos",
        "pattern",
        "recommended",
        "slot_uri",
    ]:
        assert getattr(s, k) == getattr(c2_s1, k)
