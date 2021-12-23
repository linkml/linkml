import logging
from functools import lru_cache
from typing import List, Type

from linkml_runtime.linkml_model import ClassDefinition
from linkml_runtime.utils.distroutils import get_schema_string
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot



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


