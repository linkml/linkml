import importlib
import json
from functools import lru_cache
from typing import Dict

import stringcase
from linkml.utils.generator import Generator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.pythongen import PythonGenerator

from linkml.validator.plugins.base import BasePlugin


@lru_cache()
def get_python_module(schema: str, generator: Generator = PythonGenerator, **kwargs) -> object:
    """
    Get Python representation of the schema.

    Args:
        schema: Path or URL to schema YAML
        generator: The generator to use to generate the Python module

    Returns:
        object: The Python module compiled from schema YAML

    """
    kwargs["schema"] = schema
    python_module = generator(**kwargs).compile_module()
    return python_module


@lru_cache()
def get_generator(generator: Generator, **kwargs) -> Generator:
    """
    Get an instance of a given Generator.

    Args:
        generator: A Generator class that is to be instantiated
        kwargs: Additional arguments to the generator

    Returns:
        Generator: An instance of the given Generator

    """
    return generator(**kwargs)


@lru_cache()
def get_jsonschema(schema: str, py_target_class: object = None, generator: Generator = JsonSchemaGenerator, **kwargs) -> Dict:
    """
    Get JSONSchema representation of the schema.

    Args:
        schema: Path or URL to schema YAML
        py_target_class: The Python representation of the target class
        generator: The generator to use to generate the JSONSchema

    Returns:
        dict: The JSONSchema compiled from the schema YAML

    """
    if "mergeimports" not in kwargs:
        kwargs["mergeimports"] = True
    kwargs["schema"] = schema
    if "not_closed" not in kwargs:
        kwargs["not_closed"] = False
    top_class = py_target_class.class_name if py_target_class else None
    generator = get_generator(generator, **kwargs)
    generator.top_class = top_class
    jsonschemastr = generator.serialize()
    jsonschema_obj = json.loads(jsonschemastr)
    return jsonschema_obj


def import_plugin(plugin_module_name: str, plugin_class_name: str) -> BasePlugin:
    """
    Import a plugin class.

    Args:
        plugin_module_name: The name of the plugin module
        plugin_class_name: The name of the class in the plugin module

    Returns:
        BasePlugin: The plugin class

    """
    plugin_module = importlib.import_module(plugin_module_name)
    plugin_class = getattr(plugin_module, plugin_class_name)
    if not issubclass(plugin_class, BasePlugin):
        raise Exception(f"{plugin_module_name}.{plugin_class_name} must be a subclass of {BasePlugin}")
    return plugin_class


def camelcase_to_sentencecase(name: str) -> str:
    """
    Convert a given string from CamelCase to sentence case.

    Args:
        name: A string in CamelCase

    Returns:
        str: The converted string in sentence case

    """
    return stringcase.sentencecase(stringcase.snakecase(name)).lower()


def snakecase_to_sentencecase(name: str) -> str:
    """
    Convert a given string from snake_case to sentence case.

    Args:
        name: A string in snake_case

    Returns:
        str: The converted string in sentence case

    """
    return stringcase.sentencecase(name).lower()


def truncate(text_str: str, max_length: int = 256) -> str:
    """
    Truncate a string, from the middle, to a given max length.

    Args:
        text_str: The text to truncate
        max_length: The maximum length of the truncated string

    Returns:
        str: The truncated string

    """
    truncated_str = text_str[:max_length]
    if len(truncated_str) == max_length:
        i = max(0, (max_length - 3) // 2)
        j = max(0, max_length - 3 - i)
        truncated_str = text_str[:i] + text_str[len(text_str)-j:]
        truncated_str = truncated_str[:i] + '...' + truncated_str[len(truncated_str)-j:]
    return truncated_str