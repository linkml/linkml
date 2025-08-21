from linkml.generators.projectgen import ProjectConfiguration, ProjectGenerator


def test_projectgen(kitchen_sink_path, tmp_path):
    def check_contains(v: str, folder: str, local_path: str):
        with open(tmp_path / folder / local_path, encoding="UTF-8") as stream:
            assert v in stream.read()

    """Generate whole project"""
    config = ProjectConfiguration()
    config.directory = tmp_path
    config.generator_args["jsonschema"] = {
        "top_class": "Dataset",
        "not_closed": False,
    }
    config.generator_args["owl"] = {"metaclasses": False, "type_objects": False}
    gen = ProjectGenerator()
    gen.generate(kitchen_sink_path, config)
    # some of these tests may be quite rigid as they make assumptions about formatting
    check_contains("CREATE TABLE", "sqlschema", "kitchen_sink.sql")
    check_contains("ks:age_in_years a owl:DatatypeProperty", "owl", "kitchen_sink.owl.ttl")
    # TODO: restore this test
    # self.check_contains("Address.md", "docs", "index.md")
    check_contains("ks:Address", "docs", "Address.md")
    check_contains('"additionalProperties": false', "jsonschema", "kitchen_sink.schema.json")
