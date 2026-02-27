from pathlib import Path

import pytest

from linkml import LOCAL_METAMODEL_LDCONTEXT_FILE
from linkml.generators.rdfgen import RDFGenerator
from tests import LOCAL_MODEL_YAML_NO_META


@pytest.mark.parametrize("format", [".ttl"])
@pytest.mark.parametrize("model", LOCAL_MODEL_YAML_NO_META)
def test_model_rdf(model, format, snapshot):
    generated = RDFGenerator(model).serialize(context=LOCAL_METAMODEL_LDCONTEXT_FILE)
    output_file = Path(model).with_suffix(format).name
    assert generated == snapshot(output_file)
