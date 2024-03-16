import pytest

from pathlib import Path

from linkml import LOCAL_METAMODEL_LDCONTEXT_FILE
from tests import LOCAL_MODEL_YAML_NO_META
from linkml.generators.rdfgen import RDFGenerator


@pytest.mark.parametrize("format", [".ttl"])
@pytest.mark.parametrize("model", LOCAL_MODEL_YAML_NO_META)
def test_model_rdf(model, format, snapshot):
    generated = RDFGenerator(model).serialize(context="file://" + LOCAL_METAMODEL_LDCONTEXT_FILE)
    output_file = Path(model).with_suffix(format).name
    assert generated == snapshot(output_file)
