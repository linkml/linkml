"""
The ``linkml.validator.loaders`` package contain classes which are responsible for yielding data
instance from a source. Instances of these classes are passed to
:meth:`linkml.validator.Validator.validate_source` and
:meth:`linkml.validator.Validator.iter_results_from_source`

.. admonition:: Deprecated

    Loaders have been moved to ``linkml_runtime.loaders``

"""

import os
import warnings
from typing import Union

from linkml_runtime.loaders import CSVLoader, JSONLoader, TSVLoader, YAMLLoader
from linkml_runtime.loaders.loader_root import Loader


def default_loader_for_file(file: Union[str, bytes, os.PathLike]) -> Loader:
    _, ext = os.path.splitext(file)
    if ext == ".csv":
        return CSVLoader(file, skip_empty_rows=True)
    elif ext == ".tsv":
        return TSVLoader(file, skip_empty_rows=True)
    elif ext == ".json":
        return JSONLoader(str(file))
    elif ext in (".yaml", ".yml"):
        return YAMLLoader(file)

    raise ValueError(f"Could not find loader for file: {file}")


__all__ = [
    "CSVLoader",
    "JSONLoader",
    "Loader",
    "TSVLoader",
    "YAMLLoader",
    "default_loader_for_file",
]


def __getattr__(name):
    deprecation_maps = {
        "CsvLoader": "CSVLoader",
        "TsvLoader": "TSVLoader",
        "JsonLoader": "JSONLoader",
        "YamlLoader": "YAMLLoader",
    }
    if name in deprecation_maps.keys():
        warnings.warn(
            (
                f"Importing from {name} is deprecated, use {deprecation_maps[name]} instead."
                "Loaders have been moved to linkml_runtime.loaders"
            )
        )
        name = deprecation_maps[name]
    if name == "__path__":
        return False
    return globals()[name]
