from click.testing import CliRunner

from linkml.generators.dbmlgen import DBMLGenerator, cli

# DBML supports a slot whose range is a class without an identifier slot.
_NO_IDENTIFIER_SCHEMA = """\
id: https://example.org/noid
name: noid
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
classes:
  Address:
    attributes:
      city:
      country:
  Person:
    attributes:
      id:
        identifier: true
      address:
        range: Address
"""


def test_dbml_skips_relationship_when_referenced_class_has_no_identifier(tmp_path):
    """A reference whose target class has no identifier slot is valid LinkML.

    Regression: ``_generate_relationships`` used to ``raise ValueError`` in this case.
    The correct behavior is to emit the column but no ``Ref:`` line - DBML supports
    foreign-key-less reference columns.
    """
    schema_path = tmp_path / "noid.yaml"
    schema_path.write_text(_NO_IDENTIFIER_SCHEMA)

    dbml = DBMLGenerator(str(schema_path)).serialize()

    # The Person table exists with its address column
    assert "Table Person" in dbml
    assert "address" in dbml
    # The Address table exists
    assert "Table Address" in dbml
    # But no Ref: line is emitted for Person.address -> Address (no identifier)
    assert "Ref: Person.address" not in dbml


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
