"""Tests for the shared utilities behind LinkML-Scala backed generators.

These cover schema loading, reuse and release.
"""

import builtins
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import pytest

from linkml.generators.common.scala import (
    SUPPORTED_PLATFORMS,
    UNSUPPORTED_OPTIONS,
    ScalaBackedGenerator,
    bindings,
    build_info,
)
from linkml.utils.generator_base import GeneratorBase
from linkml_runtime import SchemaView

linkml_scala = pytest.importorskip("linkml_scala", reason="LinkML-Scala has no build for this platform")

pytestmark = pytest.mark.rdfsgen

SCHEMA = Path(__file__).parent / "input" / "rdfs_vocabulary.yaml"

INLINE_SCHEMA = """
id: https://example.org/inline
name: inline
prefixes:
  linkml: https://w3id.org/linkml/
  inline: https://example.org/inline/
default_prefix: inline
default_range: string
imports:
  - linkml:types
classes:
  Thing:
    description: Something
"""
"""A schema with no relative imports."""


@dataclass
class _CountingGenerator(ScalaBackedGenerator):
    """Counts how often the schema is handed to LinkML-Scala."""

    valid_formats: ClassVar[list[str]] = ["ttl"]

    def __post_init__(self) -> None:
        super().__post_init__()
        self.loads = 0

    def _load(self, linkml_scala_module):
        self.loads += 1
        return super()._load(linkml_scala_module)

    def serialize(self, **kwargs) -> str:
        return self.scala_schema.rdfs()


def test_it_implements_the_base_contract():
    """The Scala base is a ``GeneratorBase`` but not a LinkML-Python ``Generator``."""
    from linkml.utils.generator import Generator

    assert issubclass(ScalaBackedGenerator, GeneratorBase)
    assert not issubclass(ScalaBackedGenerator, Generator)


def test_it_is_abstract():
    """``serialize`` is still owed by subclasses."""
    with pytest.raises(TypeError, match="abstract"):
        ScalaBackedGenerator(str(SCHEMA))


def test_schema_is_loaded_once_and_reused():
    """Repeated generator calls must reuse the loaded schema."""
    generator = _CountingGenerator(str(SCHEMA))
    assert generator.loads == 0, "construction must not load the schema"
    generator.serialize()
    generator.serialize()
    generator.scala_schema.rdfs()
    assert generator.loads == 1


def test_schema_is_not_parsed_at_construction_time():
    """Nothing reads the schema until something asks for output."""
    assert _CountingGenerator(str(SCHEMA))._scala_schema is None


def test_nothing_here_parses_the_schema_with_linkml_python():
    """LinkML-Scala is the only thing that reads the schema, so there is no SchemaView at all."""
    generator = _CountingGenerator(str(SCHEMA))
    generator.serialize()
    assert not hasattr(generator, "schemaview")
    assert not hasattr(generator, "_imports")


@pytest.mark.parametrize("option", UNSUPPORTED_OPTIONS)
def test_unsupported_options_are_refused(option, tmp_path):
    """importmap, base_dir and include have no LinkML-Scala equivalent, so they are refused."""
    value = str(tmp_path) if option == "base_dir" else str(SCHEMA)
    with pytest.raises(NotImplementedError, match=option):
        _CountingGenerator(str(SCHEMA), **{option: value})


def test_the_refusal_names_every_option_that_was_set(tmp_path):
    """Setting two at once must not hide one of them."""
    with pytest.raises(NotImplementedError) as raised:
        _CountingGenerator(str(SCHEMA), importmap=str(SCHEMA), base_dir=str(tmp_path))
    assert "importmap" in str(raised.value)
    assert "base_dir" in str(raised.value)


@pytest.mark.parametrize("option", UNSUPPORTED_OPTIONS)
def test_unset_options_are_fine(option):
    """The refusal triggers on a value, not on the option existing."""
    assert _CountingGenerator(str(SCHEMA), **{option: None}).serialize()


def test_an_already_parsed_schema_is_refused():
    """A parsed schema is refused, and the refusal explains why."""
    with pytest.raises(TypeError, match="needs a path to a schema file"):
        _CountingGenerator(SchemaView(str(SCHEMA)).schema)


def test_yaml_text_is_accepted():
    generator = _CountingGenerator(INLINE_SCHEMA)
    assert generator.schema_is_yaml_text
    assert "rdfs:Class" in generator.serialize()


def test_a_path_is_not_mistaken_for_yaml_text():
    assert not _CountingGenerator(str(SCHEMA)).schema_is_yaml_text


def test_a_missing_path_says_so():
    """A typo'd path must not be mistaken for YAML and reported as a parse failure."""
    with pytest.raises(FileNotFoundError, match="no such schema file: nope.yaml"):
        _CountingGenerator("nope.yaml")


def test_close_releases_the_schema_and_is_repeatable():
    generator = _CountingGenerator(str(SCHEMA))
    generator.serialize()
    generator.close()
    assert generator._scala_schema is None
    generator.close()


def test_close_then_use_reloads():
    """Using the generator after closing it is allowed, it just loads again."""
    generator = _CountingGenerator(str(SCHEMA))
    generator.serialize()
    generator.close()
    generator.serialize()
    assert generator.loads == 2


def test_context_manager_releases_the_schema():
    with _CountingGenerator(str(SCHEMA)) as generator:
        generator.serialize()
        assert generator._scala_schema is not None
    assert generator._scala_schema is None


def test_generatorversion_comes_from_the_bindings():
    """The version on record is the LinkML-Scala version, not a constant in this repository."""
    assert _CountingGenerator(str(SCHEMA)).generatorversion == build_info()["linkml_scala_version"]


def test_build_info_reports_the_library_it_loaded():
    info = build_info()
    assert info["linkml_scala_version"]
    assert info["metamodel_version"]


def test_bindings_returns_the_module():
    assert bindings() is linkml_scala


def test_absent_bindings_blame_the_platform(monkeypatch):
    real_import = builtins.__import__

    def without_linkml_scala(name, *args, **kwargs):
        if name == "linkml_scala":
            raise ImportError("No module named 'linkml_scala'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", without_linkml_scala)
    with pytest.raises(ImportError) as raised:
        _CountingGenerator(str(SCHEMA)).serialize()
    message = str(raised.value)
    assert "not available on" in message
    assert platform.machine() in message
    assert SUPPORTED_PLATFORMS in message
    assert "pip install" not in message, "there is nothing for the user to install"
