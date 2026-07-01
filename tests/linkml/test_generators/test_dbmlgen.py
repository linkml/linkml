from click.testing import CliRunner

from linkml.generators.dbmlgen import DBMLGenerator, cli

# Ensure SchemaView uses base_dir, so relative imports are resolved against
# the schema's directory.
_RELATIVE_IMPORT_BASE = """\
id: https://example.org/dbml-base
name: dbml_base
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
classes:
  Base:
    attributes:
      id:
        identifier: true
"""

_RELATIVE_IMPORT_MAIN = """\
id: https://example.org/dbml-main
name: dbml_main
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
  - ./base
default_range: string
classes:
  Thing:
    is_a: Base
    attributes:
      label:
"""

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


def test_dbml_resolves_relative_imports_from_schema_directory(tmp_path, monkeypatch):
    """The DBML generator must resolve sibling-relative imports from the schema directory.

    Regression: ``DBMLGenerator.__post_init__`` used to construct ``SchemaView(self.schema)``
    without passing ``base_dir``. ``SchemaLoader.resolve()`` strips ``source_file`` to a
    basename, so ``SchemaView`` fell back to ``os.getcwd()`` for import resolution.
    Running ``gen-dbml`` from any directory other than the schema's own would fail.
    """
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    (schemas_dir / "base.yaml").write_text(_RELATIVE_IMPORT_BASE)
    (schemas_dir / "main.yaml").write_text(_RELATIVE_IMPORT_MAIN)

    # Run from a directory that does NOT contain ``base.yaml`` to prove the
    # generator no longer relies on ``os.getcwd()`` for import resolution.
    monkeypatch.chdir(tmp_path)

    dbml = DBMLGenerator(str(schemas_dir / "main.yaml")).serialize()
    assert "Table Thing" in dbml
    assert "Table Base" in dbml


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
