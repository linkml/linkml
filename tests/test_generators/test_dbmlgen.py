import pytest
from pathlib import Path

from jinja2.filters import do_map
from linkml_runtime.utils.schemaview import SchemaView
from linkml.generators.dbmlgen import DBMLGenerator



@pytest.fixture
def example_schema() -> SchemaView:
    """
    Create a temporary LinkML schema YAML file for testing.
    """
    schema_content = """
    id: example_schema
    name: ExampleSchema
    classes:
      Person:
        attributes:
          id:
            identifier: true
            range: string
          name:
            required: true
            range: string
          address:
            range: Address
      Address:
        attributes:
          id:
            identifier: true
            range: string
          city:
            range: string
          country:
            range: string
    """
    sv = SchemaView(schema_content)
    return sv


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
