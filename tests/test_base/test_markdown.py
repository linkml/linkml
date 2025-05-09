from pathlib import Path

import pytest

from linkml.generators.markdowngen import MarkdownGenerator
from tests import LOCAL_MODEL_YAML_NO_META


@pytest.mark.parametrize("model", LOCAL_MODEL_YAML_NO_META)
def test_models_markdown(model, snapshot, temp_dir):
    output_dir = Path("markdown") / Path(model).stem
    MarkdownGenerator(model, directory=str(temp_dir)).serialize(directory=str(temp_dir))
    assert temp_dir == snapshot(str(output_dir))
