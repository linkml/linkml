import textwrap

from click.testing import CliRunner

from linkml.generators.dbmlgen import DBMLGenerator, cli


def test_linkml_to_dbml_generator(input_path, tmp_path):
    """
    Test the LinkML to DBML generator with the example schema.
    """

    organization_schema = str(input_path("organization.yaml"))

    # Initialize the generator
    generator = DBMLGenerator(organization_schema)

    # Generate DBML
    dbml_output = generator.serialize()
    assert dbml_output.startswith("// DBML generated from LinkML schema\n")
    assert "Table Organization" in dbml_output
    assert "Table Employee" in dbml_output
    assert (
        """Table Organization {
id varchar [not null, primary key]"""
        in dbml_output
    )
    assert "Ref: Organization.has_boss > Manager.id" in dbml_output


def test_cli_generate_dbml_to_stdout(input_path):
    """
    Test the CLI to generate DBML and print to stdout.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["--schema", str(input_path("organization.yaml"))])
    assert result.exit_code == 0
    assert result.output.startswith("// DBML generated from LinkML schema\n")
    assert "Table Organization" in result.output
    assert "Table Employee" in result.output
    assert (
        """Table Organization {
id varchar [not null, primary key]"""
        in result.output
    )


def test_slot_usage_required_respected(input_path):
    """
    slot_usage overrides must reach the DBML columns.

    ``organization.yaml`` marks ``last name`` as ``required: true`` only via the ``employee``
    class's ``slot_usage``. The generator must read the induced slot, not the global one, or the
    ``not null`` constraint is lost.
    """
    dbml_output = DBMLGenerator(str(input_path("organization.yaml"))).serialize()
    assert "last_name varchar [not null]" in dbml_output


def test_relative_imports_resolved_from_schema_dir(tmp_path, monkeypatch):
    """
    Imports must resolve relative to the schema file, not the process working directory.

    Regression test for the SchemaLoader init path resolving imports against ``os.getcwd()``.
    """
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()
    (schema_dir / "imported.yaml").write_text(
        textwrap.dedent(
            """
            id: https://example.org/imported
            name: imported
            prefixes:
              linkml: https://w3id.org/linkml/
            imports:
              - linkml:types
            default_range: string
            classes:
              Widget:
                attributes:
                  id:
                    identifier: true
                  label:
            """
        )
    )
    (schema_dir / "main.yaml").write_text(
        textwrap.dedent(
            """
            id: https://example.org/main
            name: main
            prefixes:
              linkml: https://w3id.org/linkml/
            imports:
              - linkml:types
              - imported
            default_range: string
            classes:
              Gadget:
                attributes:
                  id:
                    identifier: true
                  name:
            """
        )
    )

    # Run from an unrelated working directory to prove resolution follows the schema path.
    monkeypatch.chdir(tmp_path.parent)
    dbml_output = DBMLGenerator(str(schema_dir / "main.yaml")).serialize()
    assert "Table Widget" in dbml_output
    assert "Table Gadget" in dbml_output
