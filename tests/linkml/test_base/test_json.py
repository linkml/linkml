from pathlib import Path

import pytest

from linkml.generators.jsonldgen import JSONLDGenerator
from tests import LOCAL_MODEL_YAML_NO_META, METAMODEL_NAMESPACE


@pytest.mark.parametrize("model", LOCAL_MODEL_YAML_NO_META)
def test_models_jsonld(model, snapshot):
    generated = JSONLDGenerator(model).serialize(base=METAMODEL_NAMESPACE, context_kwargs={"model": True})
    output_file = Path(model).with_suffix(".json").name
    assert generated == snapshot(output_file)
