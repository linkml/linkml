import logging
import sys
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import List, Type, Union

from linkml_runtime.linkml_model import ClassDefinition
from linkml_runtime.utils.distroutils import get_schema_string
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot


SCHEMA_PATH_VAR = 'schema_path'

def package_schema_path(package: Union[str, ModuleType]) -> Path:
    if isinstance(package, str):
        package = sys.modules[package]
    if SCHEMA_PATH_VAR in vars(package):
        return package[SCHEMA_PATH_VAR]
    package_location = Path(package.__file__)
    name = package_location.name
    for rel_path in [".", "linkml", "schema", "model", Path("model") / "schema"]:
        path = package_location.parent / rel_path / name
        if path.exists():
            return path


@lru_cache()
def package_schemaview(package: str, **kwargs) -> SchemaView:
    """
    Returns the corresponding SchemaView for a package

    :param package: Python package as string, e.g. linkml_runtime.linkml_model.meta
    :param kwargs: See :func:`get_packaged_file_as_str`
    :return:
    """
    return SchemaView(get_schema_string(package, **kwargs))

def object_schemaview(obj: YAMLRoot) -> SchemaView:
    """
    Given an object that instantiates a LinkML class, return the corresponding SchemaView

    :param obj: an object that instantiates a LinkML class
    :return: SchemaView that contains the object type
    """
    cls = type(obj)
    return package_schemaview(cls.__module__)

def object_class_definition(obj: YAMLRoot) -> ClassDefinition:
    """
    Given an object that instantiates a LinkML class, return its ClassDefinition

    :param obj: an object that instantiates a LinkML class
    :return: ClassDefinition corresponding to the object type
    """
    sv = object_schemaview(obj)
    cls = type(obj)
    return sv.get_class(cls.class_name)


