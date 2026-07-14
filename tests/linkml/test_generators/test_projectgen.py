from linkml.generators.projectgen import GEN_MAP, ProjectConfiguration, ProjectGenerator
from linkml.utils.generator import Generator

# Every documented built-in generator output path (see the "Built-in generators"
# table in docs/generators/project-generator.rst). {name} == kitchen_sink here.
BUILTIN_OUTPUT_PATHS = [
    "graphql/kitchen_sink.graphql",
    "jsonld/kitchen_sink.context.jsonld",
    "jsonld/kitchen_sink.jsonld",
    "jsonschema/kitchen_sink.schema.json",
    "owl/kitchen_sink.owl.ttl",
    "prefixmap/kitchen_sink.yaml",
    "protobuf/kitchen_sink.proto",
    "kitchen_sink.py",
    "shex/kitchen_sink.shex",
    "shacl/kitchen_sink.shacl.ttl",
    "sqlschema/kitchen_sink.sql",
    "excel/kitchen_sink.xlsx",
]


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
    # Guard the RST "Built-in generators" table: every documented path must exist.
    missing = [p for p in BUILTIN_OUTPUT_PATHS if not (tmp_path / p).is_file()]
    assert not missing, f"Documented built-in outputs missing: {missing}"


def test_projectgen_includes_limits_output(kitchen_sink_path, tmp_path):
    """`--include` / ``ProjectConfiguration.includes`` restricts run to listed keys."""
    ProjectGenerator().generate(
        kitchen_sink_path,
        ProjectConfiguration(directory=str(tmp_path), includes=["python"]),
    )
    assert (tmp_path / "kitchen_sink.py").is_file()
    # Non-included built-ins must not have run.
    for path in ("shex", "shacl", "sqlschema", "owl", "jsonschema", "graphql", "excel"):
        assert not (tmp_path / path).exists(), f"{path}/ should not have been created"


def test_projectgen_excludes_omits_listed(kitchen_sink_path, tmp_path):
    """`--exclude` / ``ProjectConfiguration.excludes`` drops listed keys from the run."""
    ProjectGenerator().generate(
        kitchen_sink_path,
        ProjectConfiguration(
            directory=str(tmp_path),
            includes=["python", "shex"],  # scope to keep test fast
            excludes=["shex"],
        ),
    )
    assert (tmp_path / "kitchen_sink.py").is_file()
    assert not (tmp_path / "shex").exists()


def test_projectgen_parent_template_interpolates_in_default_gen_args(kitchen_sink_path, tmp_path):
    """`{parent}` in default_gen_args string values resolves to the artefact's output subdir.

    Built-in ``jsonld`` sets ``context="{parent}/{name}.context.jsonld"``. If
    interpolation broke, `str.format` would raise KeyError; asserting the file
    exists is enough to catch a regression.
    """
    ProjectGenerator().generate(
        kitchen_sink_path,
        ProjectConfiguration(directory=str(tmp_path), includes=["jsonld", "jsonldcontext"]),
    )
    assert (tmp_path / "jsonld" / "kitchen_sink.jsonld").is_file()
    assert (tmp_path / "jsonld" / "kitchen_sink.context.jsonld").is_file()


class _EchoGenerator(Generator):
    """Minimal generator used by extension-hook tests.

    Emits a fixed marker string that identifies both the class and the schema
    name passed at construction, so tests can assert the plugin path was taken.
    """

    generatorname = "echo"
    generatorversion = "0.0.1"
    valid_formats = ["txt"]
    uses_schemaloader = False
    requires_metamodel = False

    def serialize(self, **kwargs) -> str:
        return f"ECHO {self.schemaview.schema.name}"


def test_projectgen_extension_hook_registers_new_generator(kitchen_sink_path, tmp_path):
    """User-supplied `generators` entries are honoured alongside the built-in map."""
    config = ProjectConfiguration(
        directory=str(tmp_path),
        generators={"echo": (_EchoGenerator, "echo/{name}.txt", {})},
        includes=["echo"],  # keep test focused; skip built-ins for speed
    )
    ProjectGenerator().generate(kitchen_sink_path, config)

    out = tmp_path / "echo" / "kitchen_sink.txt"
    assert out.is_file(), "Extension hook did not produce the expected file"
    assert out.read_text(encoding="UTF-8").startswith("ECHO ")


def test_projectgen_extension_hook_overrides_builtin(kitchen_sink_path, tmp_path):
    """A user entry with the same key as a built-in wins."""
    # Sanity: `python` is a built-in producing `{name}.py`.
    assert "python" in GEN_MAP

    config = ProjectConfiguration(
        directory=str(tmp_path),
        generators={"python": (_EchoGenerator, "python/{name}.txt", {})},
        includes=["python"],
    )
    ProjectGenerator().generate(kitchen_sink_path, config)

    # The override produced the plugin's file, not the built-in PythonGenerator's.
    override_out = tmp_path / "python" / "kitchen_sink.txt"
    builtin_out = tmp_path / "kitchen_sink.py"
    assert override_out.is_file() and override_out.read_text().startswith("ECHO ")
    assert not builtin_out.exists()


def test_projectgen_extension_hook_none_is_noop(kitchen_sink_path, tmp_path):
    """`generators=None` (the default) leaves the built-in map untouched."""
    config = ProjectConfiguration(
        directory=str(tmp_path),
        includes=["python"],
    )
    assert config.generators is None
    ProjectGenerator().generate(kitchen_sink_path, config)

    assert (tmp_path / "kitchen_sink.py").is_file()
