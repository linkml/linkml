"""Tests for the shared utilities behind ohi LinkML backed generators.

These cover schema loading, reuse and release.
"""

import builtins
import json
import logging
from dataclasses import dataclass
from io import TextIOBase
from pathlib import Path
from typing import ClassVar

import pytest
import yaml

from linkml.generators.common.ohi import (
    IN_MEMORY_IMPORTS_DIR,
    OhiBackedGenerator,
    bindings,
    build_info,
)
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.yamlgen import YAMLGenerator
from linkml.utils.generator_base import GeneratorBase
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import load_schema_wrap

ohi_linkml = pytest.importorskip("ohi_linkml", reason="the ohi LinkML bindings are not installed")

pytestmark = pytest.mark.ossiegen

SCHEMA = Path(__file__).parent / "input" / "ossie_ontology.yaml"

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
class _CountingGenerator(OhiBackedGenerator):
    """Counts how often the schema is handed to ohi LinkML."""

    valid_formats: ClassVar[list[str]] = ["yaml"]

    def __post_init__(self) -> None:
        super().__post_init__()
        self.loads = 0

    def _load(self, ohi_linkml_module):
        self.loads += 1
        return super()._load(ohi_linkml_module)

    def serialize(self, **kwargs) -> str:
        return self.ohi_schema.ossie()


def test_it_implements_the_base_contract():
    """The ohi LinkML base is a ``GeneratorBase`` but not a LinkML-Python ``Generator``."""
    from linkml.utils.generator import Generator

    assert issubclass(OhiBackedGenerator, GeneratorBase)
    assert not issubclass(OhiBackedGenerator, Generator)


def test_it_is_abstract():
    """``serialize`` is still owed by subclasses."""
    with pytest.raises(TypeError, match="abstract"):
        OhiBackedGenerator(str(SCHEMA))


def test_schema_is_loaded_once_and_reused():
    """Repeated generator calls must reuse the loaded schema."""
    generator = _CountingGenerator(str(SCHEMA))
    assert generator.loads == 0, "construction must not load the schema"
    generator.serialize()
    generator.serialize()
    generator.ohi_schema.ossie()
    assert generator.loads == 1


def test_schema_is_not_parsed_at_construction_time():
    """Nothing reads the schema until something asks for output."""
    assert _CountingGenerator(str(SCHEMA))._ohi_schema is None


def test_nothing_here_parses_the_schema_with_linkml_python():
    """ohi LinkML is the only thing that reads the schema, so there is no SchemaView at all."""
    generator = _CountingGenerator(str(SCHEMA))
    generator.serialize()
    assert not hasattr(generator, "schemaview")
    assert not hasattr(generator, "_imports")


@pytest.mark.parametrize("option", ["include", "importmap", "base_dir"])
def test_unset_import_options_are_fine(option):
    assert _CountingGenerator(str(SCHEMA), **{option: None}).serialize()


UNITS_SCHEMA = """
id: https://example.org/units/core
name: units_core
prefixes:
  linkml: https://w3id.org/linkml/
  units: https://example.org/units/
default_prefix: units
default_range: string
imports:
  - linkml:types
classes:
  Unit:
    description: A unit of measure
"""
"""A schema that the importing schemas find only through an import map."""


def _importing_schema(import_: str) -> str:
    """A schema that imports ``import_``, as YAML text.

    :param import_: the import, such as ``units:core``.
    :return: the schema.
    """
    return f"""
id: https://example.org/measures
name: measures
prefixes:
  linkml: https://w3id.org/linkml/
  units: https://example.org/units/
  measures: https://example.org/measures/
default_prefix: measures
default_range: string
imports:
  - linkml:types
  - {import_}
classes:
  Measure:
    attributes:
      unit:
        range: Unit
"""


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A schema in ``model/``, whose import of ``units:core`` is in ``deps/units/core.yaml``.

    :param tmp_path: pytest's temporary directory.
    :return: the project directory.
    """
    (tmp_path / "model").mkdir()
    (tmp_path / "model" / "measures.yaml").write_text(_importing_schema("units:core"))
    (tmp_path / "deps" / "units").mkdir(parents=True)
    (tmp_path / "deps" / "units" / "core.yaml").write_text(UNITS_SCHEMA)
    return tmp_path


def _concepts(generator: OhiBackedGenerator) -> str:
    """The Ossie output, which names every class it got, including imported ones.

    :param generator: the generator to run.
    :return: the output.
    """
    with generator:
        return generator.serialize()


def test_an_unmapped_import_is_not_downloaded(project):
    """Without a map, ``units:core`` is a URL, and ohi LinkML never downloads schemas."""
    with pytest.raises(ohi_linkml.SchemaLoadError):
        _concepts(_CountingGenerator(str(project / "model" / "measures.yaml")))


@pytest.mark.parametrize(
    "key",
    ["units:core", "https://example.org/units/core", "units:", "https://example.org/units/"],
)
def test_importmap_as_a_mapping_is_relative_to_the_schema(project, key):
    """Exact and prefix entries, as CURIEs or URIs, with a location relative to the schema."""
    location = "../deps/units/core" if key.endswith("core") else "../deps/units/"
    generator = _CountingGenerator(str(project / "model" / "measures.yaml"), importmap={key: location})
    assert "concept: Unit" in _concepts(generator)


def test_importmap_as_a_mapping_is_relative_to_base_dir(project):
    generator = _CountingGenerator(
        str(project / "model" / "measures.yaml"),
        importmap={"units:core": "deps/units/core"},
        base_dir=str(project),
    )
    assert "concept: Unit" in _concepts(generator)


def test_importmap_file_is_relative_to_its_own_directory(project):
    """Locations in a map file are joined to the file's directory, as in LinkML-Python."""
    (project / "importmap.json").write_text(json.dumps({"units:": "deps/units/"}))
    for importmap in (str(project / "importmap.json"), project / "importmap.json"):
        generator = _CountingGenerator(str(project / "model" / "measures.yaml"), importmap=importmap)
        assert "concept: Unit" in _concepts(generator)


def test_importmap_as_an_open_file_like_the_cli_passes_it(project):
    """``--importmap`` is a ``click.File``, so the generator gets an open file."""
    (project / "importmap.json").write_text(json.dumps({"units:core": "../deps/units/core"}))
    with (project / "importmap.json").open() as stream:
        generator = _CountingGenerator(str(project / "model" / "measures.yaml"), importmap=stream)
        assert "concept: Unit" in _concepts(generator)


def test_importmap_with_a_schema_in_memory(project):
    """A map value can be the schema itself, as in LinkML-Python. It's never written to disk."""
    in_memory = yaml.safe_load(UNITS_SCHEMA.replace("A unit of measure", "From memory"))
    generator = _CountingGenerator(str(project / "model" / "measures.yaml"), importmap={"units:core": in_memory})
    assert "From memory" in _concepts(generator)
    assert not Path(IN_MEMORY_IMPORTS_DIR).exists()


def test_importmap_to_a_url_is_not_downloaded(project):
    generator = _CountingGenerator(
        str(project / "model" / "measures.yaml"), importmap={"units:": "https://example.com/units/"}
    )
    with pytest.raises(ohi_linkml.SchemaLoadError):
        _concepts(generator)


def test_yaml_text_reads_relative_imports_from_base_dir(project):
    generator = _CountingGenerator(_importing_schema("deps/units/core"), base_dir=str(project))
    assert "concept: Unit" in _concepts(generator)


def test_yaml_text_reads_relative_imports_from_the_current_directory(project, monkeypatch):
    """Without ``base_dir``, as in LinkML-Python, which resolves them against the current directory."""
    monkeypatch.chdir(project)
    assert "concept: Unit" in _concepts(_CountingGenerator(_importing_schema("deps/units/core")))


def test_yaml_text_with_an_importmap_relative_to_base_dir(project):
    generator = _CountingGenerator(
        _importing_schema("units:core"), importmap={"units:": "deps/units/"}, base_dir=str(project)
    )
    assert "concept: Unit" in _concepts(generator)


@pytest.fixture
def relative_project(tmp_path: Path) -> Path:
    """A schema in ``model/``, which imports ``../deps/units/core`` by a relative path.

    :param tmp_path: pytest's temporary directory.
    :return: the schema file.
    """
    (tmp_path / "model").mkdir()
    (tmp_path / "deps" / "units").mkdir(parents=True)
    (tmp_path / "deps" / "units" / "core.yaml").write_text(UNITS_SCHEMA)
    schema = tmp_path / "model" / "measures.yaml"
    schema.write_text(_importing_schema("../deps/units/core"))
    return schema


SCHEMA_FORMS = {
    "path as text": str,
    "Path": lambda path: path,
    "open file": lambda path: path.open(),
    "SchemaDefinition": lambda path: load_schema_wrap(str(path)),
    "SchemaView": lambda path: SchemaView(str(path)),
    "SchemaView with merged imports": lambda path: _merged(SchemaView(str(path))),
    "Generator using SchemaView": lambda path: JsonSchemaGenerator(str(path)),
    "Generator using SchemaLoader": lambda path: YAMLGenerator(str(path)),
    "Generator using SchemaLoader, without mergeimports": lambda path: YAMLGenerator(str(path), mergeimports=False),
    "ohi LinkML backed generator": lambda path: _CountingGenerator(str(path)),
    "YAML text with base_dir": lambda path: {"schema": path.read_text(), "base_dir": str(path.parent)},
    "dict with base_dir": lambda path: {"schema": yaml.safe_load(path.read_text()), "base_dir": str(path.parent)},
    "Generator using SchemaLoader, from YAML text": lambda path: YAMLGenerator(
        path.read_text(), base_dir=str(path.parent)
    ),
}
"""Every form of schema that LinkML-Python generators take, made from the schema's file."""


def _merged(view: SchemaView) -> SchemaView:
    """Merge the imports of a schema view into its schema, as some callers do.

    :param view: the schema view.
    :return: the same view.
    """
    view.merge_imports()
    return view


@pytest.mark.parametrize("form", SCHEMA_FORMS)
def test_every_form_of_schema_is_accepted(relative_project, form, caplog):
    """Each loads with its relative import, and without its imported elements seen twice."""
    made = SCHEMA_FORMS[form](relative_project)
    kwargs = made if isinstance(made, dict) else {"schema": made}
    with caplog.at_level(logging.WARNING):
        output = _concepts(_CountingGenerator(**kwargs))
    if isinstance(made, TextIOBase):
        made.close()
    assert "concept: Measure" in output
    assert "concept: Unit" in output
    assert not [record for record in caplog.records if "Non-unique" in record.getMessage()]


def test_yaml_text_without_imports():
    assert "concept: Thing" in _concepts(_CountingGenerator(INLINE_SCHEMA))


def test_changes_to_a_parsed_schema_are_kept(relative_project):
    """A parsed schema from a file is still read in place of the file, with its relative imports."""
    schema = load_schema_wrap(str(relative_project))
    generator = _CountingGenerator(schema)
    schema.classes["Extra"] = ClassDefinition("Extra")
    output = _concepts(generator)
    assert "concept: Extra" in output
    assert "concept: Unit" in output


def test_an_open_file_can_be_closed_before_generating(relative_project):
    with relative_project.open() as stream:
        generator = _CountingGenerator(stream)
    assert "concept: Unit" in _concepts(generator)


def test_another_generators_import_options_are_used(project):
    other = _CountingGenerator(str(project / "model" / "measures.yaml"), importmap={"units:": "../deps/units/"})
    assert "concept: Unit" in _concepts(_CountingGenerator(other))


def test_a_url_is_refused():
    with pytest.raises(ValueError, match="never downloads"):
        _CountingGenerator("https://example.org/schema.yaml")


def test_something_that_is_not_a_schema_is_refused():
    with pytest.raises(TypeError, match="int"):
        _CountingGenerator(42)


EXTRA_SCHEMA = """
id: https://example.org/extra
name: extra
classes:
  Extra:
    description: Merged in
  Measure:
    description: Not merged, as the schema already has a Measure
"""


@pytest.mark.parametrize("form", ["path", "YAML text", "SchemaDefinition"])
def test_include_merges_a_schema_in(relative_project, form):
    """As in LinkML-Python, the included elements are added unless the schema has them already."""
    path = relative_project.parent / "extra.yaml"
    path.write_text(EXTRA_SCHEMA)
    include = {"path": str(path), "YAML text": EXTRA_SCHEMA, "SchemaDefinition": load_schema_wrap(str(path))}[form]
    output = _concepts(_CountingGenerator(str(relative_project), include=include))
    assert "concept: Extra" in output
    assert "Not merged" not in output
    assert "concept: Unit" in output


def test_include_does_not_change_the_given_schemas(relative_project):
    schema = load_schema_wrap(str(relative_project))
    included = yaml_loader.load(EXTRA_SCHEMA, target_class=SchemaDefinition)
    _concepts(_CountingGenerator(schema, include=included))
    assert "Extra" not in schema.classes
    assert included.classes["Measure"].description.startswith("Not merged")


def test_include_from_a_url_is_refused(relative_project):
    with pytest.raises(ValueError, match="never downloads"):
        _concepts(_CountingGenerator(str(relative_project), include="https://example.org/extra.yaml"))


def test_a_missing_path_says_so():
    """A typo'd path must not be mistaken for YAML and reported as a parse failure."""
    with pytest.raises(FileNotFoundError, match="no such schema file: nope.yaml"):
        _CountingGenerator("nope.yaml")


def test_close_releases_the_schema_and_is_repeatable():
    generator = _CountingGenerator(str(SCHEMA))
    generator.serialize()
    generator.close()
    assert generator._ohi_schema is None
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
        assert generator._ohi_schema is not None
    assert generator._ohi_schema is None


def test_generatorversion_comes_from_the_bindings():
    """The version on record is the ohi LinkML version, not a constant in this repository."""
    assert _CountingGenerator(str(SCHEMA)).generatorversion == build_info()["linkml_scala_version"]


def test_build_info_reports_the_library_it_loaded():
    info = build_info()
    assert info["linkml_scala_version"]
    assert info["metamodel_version"]


def test_bindings_returns_the_module():
    assert bindings() is ohi_linkml


def test_absent_bindings_say_how_to_install_them(monkeypatch):
    """The bindings are a dependency, so a missing one is something the user can fix."""
    real_import = builtins.__import__

    def without_ohi_linkml(name, *args, **kwargs):
        if name == "ohi_linkml":
            raise ImportError("No module named 'ohi_linkml'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", without_ohi_linkml)
    with pytest.raises(ImportError) as raised:
        _CountingGenerator(str(SCHEMA)).serialize()
    message = str(raised.value)
    assert "not installed" in message
    assert "pip install neverblink-linkml" in message
