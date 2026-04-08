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
