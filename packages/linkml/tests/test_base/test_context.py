from pathlib import Path

import pytest

from linkml.generators.jsonldcontextgen import ContextGenerator
from tests import (
    LOCAL_MODEL_YAML_NO_META,
    METAMODEL_NAMESPACE,
)


@pytest.mark.parametrize("model", LOCAL_MODEL_YAML_NO_META)
def test_models_jsonld_context(model, snapshot):
    generated = ContextGenerator(model).serialize(base=METAMODEL_NAMESPACE)
    output_file = Path(model).with_suffix(".context.jsonld").name
    assert generated == snapshot(output_file)
