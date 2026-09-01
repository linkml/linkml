"""Tests for the generator base contract.

:class:`~linkml.utils.generator_base.GeneratorBase` was pulled out of
:class:`~linkml.utils.generator.Generator` so that generators which are not implemented in
Python can share the option handling code.
"""

import abc
import dataclasses
import inspect
import logging
from dataclasses import dataclass
from typing import ClassVar

import pytest

from linkml.utils.generator import Generator
from linkml.utils.generator_base import GeneratorBase

# Generator's constructor signature, as it was before GeneratorBase existed. Positional order
# matters: callers pass these positionally, and reordering them would break compatibility.
GENERATOR_FIELDS = [
    "schema",
    "schemaview",
    "format",
    "metadata",
    "useuris",
    "log_level",
    "mergeimports",
    "source_file_date",
    "source_file_size",
    "logger",
    "verbose",
    "output",
    "namespaces",
    "directory_output",
    "base_dir",
    "metamodel_name_map",
    "importmap",
    "emit_prefixes",
    "metamodel",
    "stacktrace",
    "include",
]


def test_generator_fields_are_unchanged():
    """``Generator``'s fields and their order must be exactly what they were."""
    assert [f.name for f in dataclasses.fields(Generator)] == GENERATOR_FIELDS


def test_generator_takes_no_fields_from_the_base():
    """The base contributes no dataclass fields, which is what keeps the order above stable."""
    assert not dataclasses.is_dataclass(GeneratorBase)
    assert "schema" in Generator.__dataclass_fields__
    assert not hasattr(GeneratorBase, "__dataclass_fields__")


def test_generator_only_requires_a_schema():
    """Everything except ``schema`` still has a default."""
    parameters = list(inspect.signature(Generator).parameters.values())
    assert parameters[0].name == "schema"
    assert parameters[0].default is inspect.Parameter.empty
    assert all(p.default is not inspect.Parameter.empty for p in parameters[1:])


def test_generator_is_a_generator_base():
    """``Generator`` implements the contract, so ``shared_arguments`` accepts either."""
    assert issubclass(Generator, GeneratorBase)


@pytest.mark.parametrize("name", ["generatorname", "generatorversion", "valid_formats", "file_extension"])
def test_shared_classvars_reach_generator(name):
    """The ClassVars moved to the base must still be readable off ``Generator``."""
    assert getattr(Generator, name) == getattr(GeneratorBase, name)


def test_base_is_abstract():
    """``GeneratorBase`` cannot be instantiated, and ``serialize`` is what subclasses owe it."""
    assert isinstance(GeneratorBase, abc.ABCMeta)
    assert GeneratorBase.__abstractmethods__ == frozenset({"serialize"})
    with pytest.raises(TypeError, match="abstract"):
        GeneratorBase()


@dataclass
class _MinimalGenerator(GeneratorBase):
    """A generator that does not use LinkML-Python, to test the base on its own."""

    schema: str
    format: str | None = None
    metadata: bool = True
    log_level: int | None = None
    logger: logging.Logger | None = None
    source_file_date: str | None = None
    source_file_size: int | None = None

    valid_formats: ClassVar[list[str]] = ["json", "yaml"]

    def __post_init__(self) -> None:
        if not self.logger:
            self.logger = logging.getLogger(__name__)
        self._init_common()

    def serialize(self, **kwargs) -> str:
        return self.schema


def test_subclass_needs_no_linkml_python_machinery():
    """A subclass can satisfy the contract without SchemaView, SchemaLoader or the metamodel."""
    assert _MinimalGenerator("hello").serialize() == "hello"


def test_format_defaults_to_the_first_valid_format():
    assert _MinimalGenerator("x").format == "json"


def test_explicit_format_is_kept():
    assert _MinimalGenerator("x", format="yaml").format == "yaml"


def test_unknown_format_is_rejected_and_names_the_format():
    """The error says which format was asked for, and which ones exist."""
    with pytest.raises(ValueError, match=r"Unrecognized format: toml; known=\['json', 'yaml'\]"):
        _MinimalGenerator("x", format="toml")


def test_log_level_is_applied():
    logger = logging.getLogger("test_generator_base.level")
    _MinimalGenerator("x", log_level=logging.DEBUG, logger=logger)
    assert logger.level == logging.DEBUG


def test_no_metadata_drops_the_source_file_details():
    """``--no-metadata`` clears the source file date and size, whatever the generator does next."""
    generator = _MinimalGenerator("x", metadata=False, source_file_date="2026-09-01", source_file_size=12)
    assert generator.source_file_date is None
    assert generator.source_file_size is None


def test_metadata_keeps_the_source_file_details():
    generator = _MinimalGenerator("x", metadata=True, source_file_date="2026-09-01", source_file_size=12)
    assert generator.source_file_date == "2026-09-01"
    assert generator.source_file_size == 12
