import yaml
from click.testing import CliRunner
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SchemaDefinition

from linkml.generators.linkmlgen import LinkmlGenerator, cli


def test_linkmlgen_prefixes():
    schema = SchemaDefinition(
        name="EquipmentSchema", description="", id="equipment_schema", default_prefix="equipment_schema"
    )

    schema.default_range = "string"
    schema.prefixes = {
        "equipment_schema": "https://example.org/equipment_schema/",
        "linkml": "https://w3id.org/linkml/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
    }

    lml_gen = LinkmlGenerator(schema=schema, format="yaml")
    yaml_text = lml_gen.serialize()

    with open("output.yaml", "w") as f:
        f.write(yaml_text)


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
    assert pattern_gen.schemaview.get_slot("name").pattern == r"^[A-Z0-9]\w+.*$"
    assert pattern_gen.schemaview.get_slot("nicknames").pattern == r"^[A-Z0-9]\w+.*$"
    assert pattern_gen.schemaview.get_slot("height").pattern == "\\d+[\\.\\d+] (centimeter|meter|inch)"
    assert pattern_gen.schemaview.get_slot("weight").pattern == "\\d+[\\.\\d+] (kg|g|lbs|stone)"


def test_default_pattern_materialization_true(input_path, tmp_path):
    """
    Test with `--materialize` set to True. Explicit flags override the umbrella flag:
      - If user sets `--no-materialize-attributes` or `--no-materialize-patterns`,
        then those take precedence (so nothing is materialized).
      - If user sets `--materialize-attributes` and `--materialize-patterns`,
        then both are materialized.
    """
    runner = CliRunner()
    schema_path = str(input_path("pattern-example.yaml"))
    yaml_output_path = str(tmp_path / "pattern-materialized.yaml")

    # Scenario 1: User sets `--materialize` but explicitly sets both
    # `--no-materialize-attributes` and `--no-materialize-patterns`.
    # => Should NOT materialize patterns.
    result = runner.invoke(
        cli,
        [
            schema_path,
            "--materialize",
            "--no-materialize-attributes",
            "--no-materialize-patterns",
            "--output",
            yaml_output_path,
        ],
    )
    assert result.exit_code == 0, (
        "Command failed when `--materialize` is True but user also used "
        "`--no-materialize-attributes` and `--no-materialize-patterns`."
    )
    yobj = yaml.safe_load(open(yaml_output_path))
    assert "pattern" not in yobj["slots"]["height"]
    assert "pattern" not in yobj["slots"]["weight"]

    # Scenario 2: User sets `--materialize` AND explicitly sets
    # `--materialize-attributes` and `--materialize-patterns`.
    # => Should materialize patterns.
    result = runner.invoke(
        cli,
        [
            schema_path,
            "--materialize",
            "--materialize-attributes",
            "--materialize-patterns",
            "--output",
            yaml_output_path,
        ],
    )
    assert result.exit_code == 0, (
        "Command failed when `--materialize` is True and user also used "
        "`--materialize-attributes` and `--materialize-patterns`."
    )
    yobj = yaml.safe_load(open(yaml_output_path))
    assert yobj["slots"]["height"]["pattern"] == "\\d+[\\.\\d+] (centimeter|meter|inch)"
    assert yobj["slots"]["weight"]["pattern"] == "\\d+[\\.\\d+] (kg|g|lbs|stone)"


def test_default_pattern_materialization_false(input_path, tmp_path):
    """
    Test with `--no-materialize` set to True (meaning we do NOT materialize by default).
    Again, explicit flags override:
      - If user explicitly sets `--materialize-attributes` or `--materialize-patterns`
        to True, they will be materialized despite `--no-materialize`.
      - If user also sets `--no-materialize-attributes` and `--no-materialize-patterns`,
        nothing is materialized.
    """
    runner = CliRunner()
    schema_path = str(input_path("pattern-example.yaml"))
    yaml_output_path = str(tmp_path / "pattern-not-materialized.yaml")

    # Scenario 1: User sets `--no-materialize`, but explicitly sets
    # `--materialize-attributes` and `--materialize-patterns`.
    # => Patterns should be materialized, overriding the `--no-materialize`.
    result = runner.invoke(
        cli,
        [
            schema_path,
            "--no-materialize",
            "--materialize-attributes",
            "--materialize-patterns",
            "--output",
            yaml_output_path,
        ],
    )
    assert result.exit_code == 0, (
        "Command failed when `--no-materialize` is True but user also used "
        "`--materialize-attributes` and `--materialize-patterns`."
    )
    yobj = yaml.safe_load(open(yaml_output_path))
    assert yobj["slots"]["height"]["pattern"] == "\\d+[\\.\\d+] (centimeter|meter|inch)"
    assert yobj["slots"]["weight"]["pattern"] == "\\d+[\\.\\d+] (kg|g|lbs|stone)"

    # Scenario 2: User sets `--no-materialize` AND also explicitly sets
    # `--no-materialize-attributes` and `--no-materialize-patterns`.
    # => Should NOT materialize patterns at all.
    result = runner.invoke(
        cli,
        [
            schema_path,
            "--no-materialize",
            "--no-materialize-attributes",
            "--no-materialize-patterns",
            "--output",
            yaml_output_path,
        ],
    )
    assert result.exit_code == 0, (
        "Command failed when `--no-materialize` is True and user also used "
        "`--no-materialize-attributes` and `--no-materialize-patterns`."
    )
    yobj = yaml.safe_load(open(yaml_output_path))
    assert "pattern" not in yobj["slots"]["height"]
    assert "pattern" not in yobj["slots"]["weight"]
