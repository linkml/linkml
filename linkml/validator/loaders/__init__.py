"""
The ``linkml.validator.loaders`` package contain classes which are responsible for yielding data
instance from a source. Instances of these classes are passed to
:meth:`linkml.validator.Validator.validate_source` and
:meth:`linkml.validator.Validator.iter_results_from_source`
"""

import os
from typing import Union

from linkml.validator.loaders.delimited_file_loader import CsvLoader, TsvLoader
from linkml.validator.loaders.json_loader import JsonLoader
from linkml.validator.loaders.loader import Loader
from linkml.validator.loaders.yaml_loader import YamlLoader


def default_loader_for_file(file: Union[str, bytes, os.PathLike]) -> Loader:
    _, ext = os.path.splitext(file)
    if ext == ".csv":
        return CsvLoader(file, skip_empty_rows=True)
    elif ext == ".tsv":
        return TsvLoader(file, skip_empty_rows=True)
    elif ext == ".json":
        return JsonLoader(str(file))
    elif ext in (".yaml", ".yml"):
        return YamlLoader(file)

    raise ValueError(f"Could not find loader for file: {file}")


__all__ = [
    "CsvLoader",
    "JsonLoader",
    "Loader",
    "TsvLoader",
    "YamlLoader",
    "default_loader_for_file",
]
