import os
from typing import Union

from linkml.validator.loaders.delimited_file_loader import CsvLoader, TsvLoader
from linkml.validator.loaders.json_loader import JsonLoader
from linkml.validator.loaders.loader import Loader


def default_loader_for_file(file: Union[str, bytes, os.PathLike]) -> Loader:
    _, ext = os.path.splitext(file)
    if ext == ".csv":
        return CsvLoader(file, skip_empty_rows=True)
    elif ext == ".tsv":
        return TsvLoader(file, skip_empty_rows=True)
    elif ext == ".json":
        return JsonLoader(str(file))

    raise ValueError(f"Could not find loader for file: {file}")


__all__ = ["CsvLoader", "JsonLoader", "Loader", "TsvLoader", "default_loader_for_file"]
