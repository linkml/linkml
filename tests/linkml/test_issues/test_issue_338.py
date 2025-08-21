import pytest

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.utils.schemaloader import SchemaLoader


def test_biolink():
    """SchemaLoader should be monotonic - metamodel test"""
    biolink_schema = SchemaLoader(LOCAL_METAMODEL_YAML_FILE).resolve()
    biolink_schema_2 = SchemaLoader(biolink_schema).resolve()
    assert biolink_schema == biolink_schema_2


@pytest.mark.skip("Consider moving this to biolink test directory or removing")
def test_biolink_model(input_path):
    """SchemaLoader should be monotonic - biolink-model test"""
    bm_schema = SchemaLoader(input_path("biolink-model.yaml")).resolve()
    bm_schema_2 = SchemaLoader(bm_schema).resolve()
    assert bm_schema == bm_schema_2
