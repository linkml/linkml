import os
from typing import Union

import pytest
from hbreader import FileInfo
from pydantic import BaseModel

import tests.environment as test_base
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import json_loader, yaml_loader
from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.yamlutils import YAMLRoot
from tests.test_loaders_dumpers.environment import env
from tests.test_loaders_dumpers.models.books_normalized_pydantic import BookSeries
from tests.test_loaders_dumpers.models.kitchen_sink_pydantic import Dataset


def loader_test(filename: str, model: Union[type[YAMLRoot], type[BaseModel]], loader: Loader) -> None:
    """
    Test the various permutations of the supplied loader using the input file 'filename' -- both load and loads

    :param filename: un-pathed file name to load
    :param model: model to load the file name into
    :param loader: package that contains 'load' and 'loads' operations
    """
    metadata = FileInfo()
    name, typ = filename.rsplit(".", 1)
    expected_yaml = env.expected_path("load", name + "_" + typ + ".yaml")
    if issubclass(model, YAMLRoot):
        python_obj: YAMLRoot = loader.load(filename, model, metadata=metadata, base_dir=env.indir)
    elif issubclass(model, BaseModel):
        python_obj: BaseModel = loader.load(filename, model, metadata=metadata, base_dir=env.indir)
    else:
        raise TypeError(f"Unknown target class: {model}")
    env.eval_single_file(expected_yaml, yaml_dumper.dumps(python_obj))

    # Make sure metadata gets filled out properly
    rel_path = os.path.abspath(os.path.join(test_base.env.cwd, ".."))
    assert os.path.normpath("tests/test_loaders_dumpers/input") == os.path.normpath(
        os.path.relpath(metadata.base_path, rel_path)
    )
    assert os.path.normpath(f"tests/test_loaders_dumpers/input/{filename}") == os.path.normpath(
        os.path.relpath(metadata.source_file, rel_path)
    )


@pytest.mark.parametrize(
    "filename,model,loader",
    [
        ("book_series_lotr.yaml", BookSeries, yaml_loader),
        ("book_series_lotr.json", BookSeries, json_loader),
        ("kitchen_sink_normalized_inst_01.yaml", Dataset, yaml_loader),
        ("kitchen_sink_normalized_inst_01.json", Dataset, json_loader),
    ],
)
def test_loader(filename, model, loader):
    loader_test(filename, model, loader)
