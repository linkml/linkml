from pathlib import Path

import pytest
from hbreader import FileInfo
from pydantic import BaseModel

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import json_loader, yaml_loader
from tests.test_loaders_dumpers.environment import env
from tests.test_loaders_dumpers.models.books_normalized_pydantic import BookSeries
from tests.test_loaders_dumpers.models.kitchen_sink_pydantic import Dataset


@pytest.mark.parametrize(
    "filename,model,loader",
    [
        ("book_series_lotr.yaml", BookSeries, yaml_loader),
        ("book_series_lotr.json", BookSeries, json_loader),
        ("kitchen_sink_normalized_inst_01.yaml", Dataset, yaml_loader),
        ("kitchen_sink_normalized_inst_01.json", Dataset, json_loader),
    ],
)
def test_loader_basemodel(filename, model, loader):
    name = Path(filename).stem
    type = Path(filename).suffix.lstrip(".")
    expected_yaml_file = env.input_path(f"{name}_{type}.yaml")

    metadata = FileInfo()

    python_obj: BaseModel = loader.load(filename, model, metadata=metadata, base_dir=env.indir)

    # Load expected output
    with open(expected_yaml_file) as expf:
        expected = expf.read()

    got = yaml_dumper.dumps(python_obj)
    expected_trimmed = expected.replace("\r\n", "\n").strip()
    got_trimmed = got.replace("\r\n", "\n").strip()
    assert expected_trimmed == got_trimmed
