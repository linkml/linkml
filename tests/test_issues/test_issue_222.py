import pytest
from click.testing import CliRunner

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.generators.rdfgen import cli


@pytest.mark.skip(
    "Not testing metamodel outside of test_base/test_metamodel - now covered in test_scripts/test_gen_rdf"
)
def test_issue_222():
    """Test that the RDF Generator default is correct"""
    runner = CliRunner()
    result = runner.invoke(cli, [LOCAL_METAMODEL_YAML_FILE])
    assert result.exit_code == 0
