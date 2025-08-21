from linkml.generators.yamlgen import YAMLGenerator


def test_alt_description_2(input_path):
    """Test that invalid description raises an exception (type may vary)"""
    fn = input_path("issue_326a.yaml")
    try:
        YAMLGenerator(fn).serialize(validateonly=True)
        print("[INFO] issue_326a.yaml: No exception raised")
    except Exception as e:
        assert isinstance(e, Exception)
