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
    """gen-project forwards generator_args to gen-java, including the Java package.

    Regression test for the gen-java / gen-project integration (issue #2537):
    JavaGenerator takes ``directory`` in serialize() (not the constructor) and
    writes one file per class, so ProjectGenerator must split those args and not
    route a returned string.
    """
    config = ProjectConfiguration()
    config.directory = tmp_path
    config.includes = ["java"]
    config.generator_args["java"] = {"package": "com.example.generated"}

    ProjectGenerator().generate(kitchen_sink_path, config)

    java_files = list((tmp_path / "java").glob("*.java"))
    assert java_files, "expected gen-java to write .java files under java/"
    for java_file in java_files:
        assert java_file.read_text(encoding="UTF-8").startswith("package com.example.generated;")
