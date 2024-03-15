from pathlib import Path

import pytest

from linkml import (
    LOCAL_MODEL_YAML_FILES,
    NAMESPACES,
)
from linkml.generators.jsonldcontextgen import ContextGenerator


@pytest.mark.parametrize("model,namespace", zip(LOCAL_MODEL_YAML_FILES, NAMESPACES))
def test_models_jsonld_context(model, namespace, snapshot):
    generated = ContextGenerator(model).serialize(base=namespace)
    output_file = Path(model).with_suffix(".jsonld").name
    assert generated == snapshot(output_file)
