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
    check_contains('"additionalProperties": false', "jsonschema", "kitchen_sink.schema.json")
    # Excel writes its own binary file via serialize(); guard against regressions
    # in the generic "generator returned None -> skip disk-routing" branch.
    excel_out = tmp_path / "excel" / "kitchen_sink.xlsx"
    assert excel_out.is_file() and excel_out.stat().st_size > 0


def test_projectgen_java_package_from_config(kitchen_sink_path, tmp_path):
    """java GEN_MAP wiring: package flows from generator_args through to JavaGenerator."""
    config = ProjectConfiguration()
    config.directory = tmp_path
    config.includes = ["java"]
    config.generator_args["java"] = {"package": "com.example.generated"}
    gen = ProjectGenerator()
    gen.generate(kitchen_sink_path, config)
    java_files = list((tmp_path / "java").glob("*.java"))
    assert java_files, "expected at least one generated .java file"
    for f in java_files:
        assert "package com.example.generated;" in f.read_text(encoding="UTF-8")


def test_projectgen_java_default_package_without_config(kitchen_sink_path, tmp_path):
    """Without generator_args for java, the normal package precedence (schema annotation, then
    the `example` default) still applies via gen-project, unaffected by SERIALIZE_ONLY_ARGS filtering."""
    config = ProjectConfiguration()
    config.directory = tmp_path
    config.includes = ["java"]
    gen = ProjectGenerator()
    gen.generate(kitchen_sink_path, config)
    java_files = list((tmp_path / "java").glob("*.java"))
    assert java_files, "expected at least one generated .java file"
    for f in java_files:
        assert "package example;" in f.read_text(encoding="UTF-8")
