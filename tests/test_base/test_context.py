from pathlib import Path

import pytest

from tests import (
    LOCAL_MODEL_YAML_NO_META,
    NAMESPACES_NO_META,
)
from linkml.generators.jsonldcontextgen import ContextGenerator


@pytest.mark.parametrize("model,namespace", zip(LOCAL_MODEL_YAML_NO_META, NAMESPACES_NO_META))
def test_models_jsonld_context(model, namespace, snapshot):
    generated = ContextGenerator(model).serialize(base=namespace)
    output_file = Path(model).with_suffix(".jsonld").name
    assert generated == snapshot(output_file)
