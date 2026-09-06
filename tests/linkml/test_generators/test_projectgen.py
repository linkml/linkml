from dataclasses import dataclass

import click
import pytest
from click.testing import CliRunner

from linkml.generators import projectgen
from linkml.generators.projectgen import ProjectConfiguration, ProjectGenerator
from linkml.generators.projectgen import cli as projectgen_cli
from linkml.utils.generator import Generator


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


def test_directory_arg_scoped_per_generator_not_globally_stripped(kitchen_sink_path, tmp_path, monkeypatch):
    """A `directory` value configured for a generator other than java must reach that
    generator's constructor. Serialize-only args are scoped per GEN_MAP entry, not filtered
    by a name shared globally across every generator (several real generators -- dotgen,
    docgen, plantumlgen -- take `directory` as a constructor arg, not a serialize-only one)."""
    captured = {}

    @dataclass
    class FakeDirGenerator(Generator):
        uses_schemaloader = False
        requires_metamodel = False
        valid_formats = ["fake"]
        directory: str | None = None

        def serialize(self, **kwargs):
            captured["directory"] = self.directory
            return None

    # `serialize_only` omitted: a generator that takes `directory` in its constructor
    # needs no entry in it, which is the default.
    monkeypatch.setitem(
        projectgen.GEN_MAP,
        "fakedir",
        projectgen.GeneratorConfig(FakeDirGenerator, "fakedir/{name}.fake", {}),
    )

    config = ProjectConfiguration()
    config.directory = tmp_path
    config.includes = ["fakedir"]
    config.generator_args["fakedir"] = {"directory": "passthrough-value"}

    ProjectGenerator().generate(kitchen_sink_path, config)

    assert captured["directory"] == "passthrough-value"


def test_projectgen_java_default_package_without_config(kitchen_sink_path, tmp_path):
    """Without generator_args for java, the normal package precedence (schema annotation, then
    the `example` default) still applies via gen-project, unaffected by the constructor/serialize
    arg-filtering in GEN_MAP."""
    config = ProjectConfiguration()
    config.directory = tmp_path
    config.includes = ["java"]
    gen = ProjectGenerator()
    gen.generate(kitchen_sink_path, config)
    java_files = list((tmp_path / "java").glob("*.java"))
    assert java_files, "expected at least one generated .java file"
    for f in java_files:
        assert "package example;" in f.read_text(encoding="UTF-8")


def test_generate_validates_generator_args_before_constructing_anything(kitchen_sink_path, tmp_path):
    """A bad `generator_args` value is rejected by JavaGenerator.validate_generator_args()
    before any generator is built for any schema -- so this, and not construction itself, is
    the only place in `generate()` a bad config value can come from. The message is already
    generator-specific ("valid Java package name") so needs no extra prefixing."""
    config = ProjectConfiguration()
    config.directory = tmp_path
    config.includes = ["java"]
    config.generator_args["java"] = {"package": "1bad.pkg"}

    with pytest.raises(click.UsageError, match="is not a valid Java package name"):
        ProjectGenerator().generate(kitchen_sink_path, config)


def test_generate_rejects_bad_config_before_generating_anything(kitchen_sink_path, tmp_path):
    """A bad `generator_args` value for one generator is rejected before ANY generator
    runs -- generators earlier in GEN_MAP (graphql here) must not have written output,
    nor the project directory been created, only for the run to die halfway through."""
    out_dir = tmp_path / "out"
    config = ProjectConfiguration()
    config.directory = out_dir
    config.includes = ["graphql", "java"]  # graphql iterates first in GEN_MAP
    config.generator_args["java"] = {"package": "1bad.pkg"}

    with pytest.raises(click.UsageError, match="is not a valid Java package name"):
        ProjectGenerator().generate(kitchen_sink_path, config)

    assert not out_dir.exists()


def test_generate_does_not_mistake_a_schema_error_for_a_bad_config_value(tmp_path):
    """A ValueError raised while actually constructing a generator (e.g. an unloadable
    schema) is a genuine failure, not a `generator_args` problem, and must propagate with
    its own traceback rather than being caught and relabelled -- reproduces
    https://github.com/linkml/linkml/pull/3781#discussion_r3862911491 (too broadl)."""
    bad_schema = tmp_path / "bad.yaml"
    bad_schema.write_text("justastring\n", encoding="UTF-8")
    config = ProjectConfiguration()
    config.directory = tmp_path / "out"
    config.mergeimports = True  # matches gen-project's own CLI default

    with pytest.raises(ValueError) as exc_info:
        ProjectGenerator().generate(str(bad_schema), config)

    # a plain ValueError with its own message intact -- not the click.UsageError
    # validate_generator_args() raises, and not relabelled with a generator name
    assert type(exc_info.value) is ValueError
    assert not str(exc_info.value).startswith(tuple(f"{name}:" for name in projectgen.GEN_MAP))


def test_cli_bad_generator_args_is_a_usage_error_not_a_traceback(kitchen_sink_path, tmp_path):
    """gen-project reports a bad `generator_args` value the way the individual generator
    CLIs do, rather than letting a ValueError escape as a traceback."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        f"directory: {tmp_path / 'out'}\ngenerator_args:\n  java:\n    package: 1bad.pkg\n",
        encoding="UTF-8",
    )

    result = CliRunner().invoke(
        projectgen_cli, ["--config-file", str(config_path), "-I", "java", str(kitchen_sink_path)]
    )

    assert result.exit_code != 0
    assert not isinstance(result.exception, ValueError)
    assert "is not a valid Java package name" in result.output
