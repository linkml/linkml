"""Shared utilities for generators implemented as wrappers around ohi LinkML.

`ohi LinkML <https://linkml.ohi.dev/>`_ is an independent LinkML
implementation with its own generators. It's packaged as a natively-compiled library with
Python bindings (the ``neverblink-linkml`` package on PyPI). A generator built on this base
is a wrapper: report bugs in the output to ohi LinkML.
"""

import functools
import logging
from abc import ABCMeta
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass, field
from io import TextIOBase
from pathlib import Path
from typing import Any, TextIO

import click
import yaml

from linkml._version import __version__
from linkml.cli.logging import DEFAULT_LOG_LEVEL_INT
from linkml.utils.generator import Generator
from linkml.utils.generator_base import GeneratorBase
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.utils.context_utils import parse_import_map
from linkml_runtime.utils.schemaview import SCHEMA_ELEMENTS, load_schema_wrap

logger = logging.getLogger(__name__)

SchemaInput = str | Path | TextIO | Mapping[str, Any] | SchemaDefinition | SchemaView | GeneratorBase
"""Everything a generator takes as its schema. See :attr:`OhiBackedGenerator.schema`."""

IN_MEMORY_IMPORTS_DIR = ".linkml-importmap"
"""Directory, under the current one, of the made-up locations of the schemas that an import map
holds in memory, as dicts. Nothing is read from or written to it. It's only there so that the
relative imports of these schemas are read from the current directory, as in LinkML-Python."""


def bindings():
    """Import the ohi LinkML Python bindings.

    Imported lazily so that ``linkml`` stays importable when the bindings are missing
    (e.g., when linkml was installed from conda-forge).

    :return: the ``ohi_linkml`` module.
    :raises ImportError: if the bindings are not installed.
    """
    try:
        import ohi_linkml
    except ImportError as exc:  # pragma: no cover - depends on how linkml was installed
        raise ImportError(
            "This generator is implemented by ohi LinkML, whose Python bindings are not "
            "installed. This usually only happens if you did not install linkml from PyPI, "
            "but from a different source, such as conda-forge. "
            "Install the bindings with: pip install neverblink-linkml"
        ) from exc
    return ohi_linkml


def ohi_import_options(
    importmap: str | Path | Mapping[str, Any] | TextIO | None, base: str | Path
) -> tuple[dict[str, str], dict[str, str]]:
    """Turn a LinkML-Python import map into ohi LinkML's import options.

    The map is read with LinkML-Python's own ``parse_import_map``, so it takes the same forms, and
    relative locations are resolved the same way: against the directory of the map file when the
    map is a path, otherwise against ``base``. Then each schema the map holds in memory, as a dict,
    gets a made-up location in :data:`IN_MEMORY_IMPORTS_DIR`, and is handed over under it.

    >>> import_map, imports = ohi_import_options(
    ...     {"units:": "deps/units", "https://example.org/core": "/shared/core"}, "/models"
    ... )
    >>> import_map == {"units:": "/models/deps/units", "https://example.org/core": "/shared/core"}
    True
    >>> imports
    {}
    >>> import_map, imports = ohi_import_options({"units:core": {"id": "https://example.org/units/core"}}, "/models")
    >>> import_map["units:core"] in imports
    True

    :param importmap: the import map, in any form that LinkML-Python's ``--importmap`` takes.
    :param base: the directory to resolve relative locations against when the map is not a file.
    :return: the import map, and the text of each schema to load from memory, by location.
    """
    if importmap is None:
        return {}, {}
    entries = parse_import_map(str(importmap) if isinstance(importmap, Path) else importmap, str(base))
    import_map: dict[str, str] = {}
    imports: dict[str, str] = {}
    for index, (key, location) in enumerate(entries.items()):
        if isinstance(location, Mapping):
            in_memory = str(Path(IN_MEMORY_IMPORTS_DIR, f"{index}.yaml").absolute())
            imports[in_memory] = yaml.safe_dump(dict(location), sort_keys=False)
            location = in_memory
        import_map[key] = location
    return import_map, imports


def is_url(text: str) -> bool:
    """Check if a schema or location is a URL, which ohi LinkML never downloads.

    >>> is_url("https://example.org/schema.yaml"), is_url("model/schema.yaml"), is_url("C:\\\\schema.yaml")
    (True, False, False)

    :param text: a path, URL or YAML text.
    :return: whether it's a URL.
    """
    return "\n" not in text and "://" in text


@dataclass(frozen=True)
class SchemaSource:
    """Where ohi LinkML reads the root schema from."""

    location: Path | None
    """The schema's file, as an absolute path, or None for a schema that has no file."""

    text: str | None
    """The schema as YAML text, read instead of :attr:`location`. None to read the file."""

    directory: Path
    """The directory that the schema's relative imports are read from, as an absolute path."""


def schema_source(schema: SchemaInput, base_dir: str | Path | None) -> SchemaSource:
    """Find out where to read a schema from, for everything LinkML-Python generators take.

    A path is read by ohi LinkML. A schema that is already in memory is handed over as YAML
    text. When it came from a file, it keeps that file's location, so that its relative imports,
    and imports that lead back to it, are resolved as if it were read from there.

    >>> source = schema_source("id: https://example.org/s\\nname: s\\n", "/models")
    >>> source.location, source.directory.as_posix()
    (None, '/models')

    :param schema: the schema, in any form :attr:`OhiBackedGenerator.schema` takes.
    :param base_dir: the directory for the relative imports of a schema that has no file.
    :return: where to read the schema from.
    :raises ValueError: if the schema is a URL.
    :raises FileNotFoundError: if the schema is a path to a file that does not exist.
    :raises TypeError: if the schema is something else entirely.
    """
    without_file = Path(base_dir or ".").absolute()
    if isinstance(schema, Generator) and schema.uses_schemaloader:
        # SchemaLoader copies every imported element into the schema, even without mergeimports,
        # but keeps its imports, so ohi LinkML would see each of them twice. Read the file the
        # schema came from instead, or else leave out what was imported.
        location = schema.schema_location
        if location and not is_url(str(location)) and Path(location).is_file():
            return schema_source(Path(location), base_dir)
        return schema_source(without_imported_elements(schema.schema), base_dir)
    if isinstance(schema, GeneratorBase):
        return schema_source(schema.schema, base_dir)
    if isinstance(schema, SchemaView):
        return schema_source(schema.schema, base_dir)
    if isinstance(schema, SchemaDefinition):
        source_file = str(schema.source_file or "")
        text = yaml_dumper.dumps(schema)
        if source_file and not is_url(source_file) and Path(source_file).is_file():
            location = Path(source_file).absolute()
            return SchemaSource(location, text, location.parent)
        return SchemaSource(None, text, without_file)
    if isinstance(schema, Mapping):
        return SchemaSource(None, yaml.safe_dump(dict(schema), sort_keys=False), without_file)
    if isinstance(schema, TextIOBase):
        text, name = schema.read(), getattr(schema, "name", None)
        if isinstance(name, str) and Path(name).is_file():
            location = Path(name).absolute()
            return SchemaSource(location, text, location.parent)
        return SchemaSource(None, text, without_file)
    if isinstance(schema, str) and "\n" in schema:
        return SchemaSource(None, schema, without_file)
    if isinstance(schema, str | Path):
        if is_url(str(schema)):
            raise ValueError(
                f"{schema} is a URL. ohi LinkML never downloads schemas, as that is unsafe. "
                "Download it first, and pass the path."
            )
        location = Path(schema).absolute()
        if not location.is_file():
            raise FileNotFoundError(f"no such schema file: {schema}")
        return SchemaSource(location, None, location.parent)
    raise TypeError(f"can't read a schema from a {type(schema).__name__}")


def without_imported_elements(schema: SchemaDefinition) -> SchemaDefinition:
    """A copy of a schema without the elements that came from its imports.

    For a schema loaded by LinkML-Python's ``SchemaLoader``, which copies the elements of the
    imports into it, sets ``from_schema`` on every element, and keeps the ``imports``.

    :param schema: the merged schema.
    :return: a copy, with only the elements whose ``from_schema`` is the schema itself.
    """
    schema = deepcopy(schema)
    for kind in SCHEMA_ELEMENTS:
        elements = getattr(schema, kind)
        for name in [name for name, element in elements.items() if element.from_schema not in (None, schema.id)]:
            del elements[name]
    return schema


def merge_include(source: SchemaSource, include: str | Path | SchemaDefinition) -> SchemaSource:
    """Merge ``include`` into the schema, as LinkML-Python's generators do.

    The elements of ``include`` are copied into the schema, unless it already has one with the
    same name. Its imports are not, as in LinkML-Python. The merge is done by LinkML-Python's
    ``SchemaView.merge_schema``, on a fresh copy of the schema, so no schema object is changed.

    :param source: the schema to merge into.
    :param include: the schema to merge, as a path, YAML text or a parsed schema.
    :return: the merged schema, from the same location.
    """
    if isinstance(include, str | Path):
        included = schema_source(include, source.directory)
        include = load_schema_wrap(included.text if included.text is not None else str(included.location))
    view = SchemaView(load_schema_wrap(source.text if source.text is not None else str(source.location)))
    view.merge_schema(include)
    return SchemaSource(source.location, yaml_dumper.dumps(view.schema), source.directory)


@functools.cache
def build_info() -> dict[str, Any]:
    """Version and build metadata for the ohi LinkML library the bindings loaded.

    :return: the metadata, with keys including ``linkml_scala_version`` and
        ``metamodel_version``.
    """
    return bindings().build_info()


def print_versions(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    """Print the linkml and ohi LinkML versions and exit, as an eager ``--version`` callback.

    Wire it into a generator's CLI with::

        @click.option("-V", "--version", is_flag=True, is_eager=True, expose_value=False,
                      callback=print_versions,
                      help="Show the linkml and ohi LinkML versions and exit.")

    :param ctx: the click context, exited once the versions are printed.
    :param param: the click parameter. Unused, but click passes it.
    :param value: whether the flag was given.
    """
    if not value or ctx.resilient_parsing:
        return
    info = build_info()
    click.echo(f"linkml {__version__}")
    click.echo(f"ohi LinkML {info['linkml_scala_version']} (metamodel {info['metamodel_version']})")
    ctx.exit()


@dataclass
class OhiBackedGenerator(GeneratorBase, metaclass=ABCMeta):
    """Base class for generators that use ohi LinkML.

    Subclasses set :attr:`valid_formats` and implement
    :meth:`~linkml.utils.generator_base.GeneratorBase.serialize` by calling one method on
    :attr:`ohi_schema`.

    Loading a schema is the expensive part and every generator call on a loaded schema is cheap,
    so :attr:`ohi_schema` is built on first use and then reused. Release it with
    :meth:`close`, or use the generator as a context manager::

        with SomeGenerator("schema.yaml") as generator:
            print(generator.serialize())

    Dropping the last reference will release it too, but only when the garbage collector gets to it.

    It takes the same schemas and import options as :class:`~linkml.utils.generator.Generator`,
    but ohi LinkML reads the schema and resolves its imports, so it's the only thing that has an
    opinion about it. A schema given as a path is not parsed in Python at all. :attr:`importmap`
    and :attr:`base_dir` are turned into ohi LinkML's own import options, so that imports are
    found where LinkML-Python finds them.

    ohi LinkML never downloads a schema, so a URL as the schema is refused, and an import that only
    resolves to a URL fails to load.
    """

    schema: SchemaInput
    """The schema, in any form :class:`~linkml.utils.generator.Generator` takes:

    - a path to the schema file, as text or a :class:`~pathlib.Path`,
    - the schema as YAML text,
    - an open file,
    - a dict with the schema,
    - a parsed :class:`~linkml_runtime.linkml_model.SchemaDefinition`, or a
      :class:`~linkml_runtime.SchemaView`,
    - another generator, whose schema, :attr:`base_dir` and :attr:`importmap` are used.

    The relative imports of a schema that has a file, including a ``SchemaDefinition`` with a
    ``source_file``, are read from the file's directory. Changes to it in memory are kept. The
    relative imports of a schema without a file are read from :attr:`base_dir`, or else from the
    current directory, as in LinkML-Python.

    URLs are refused: ohi LinkML never downloads schemas.
    """

    # Options. Same names, types and defaults as Generator, minus the ones apply only to
    # generators written in Python (e.g., schemaview, or the visitor ClassVars).
    format: str | None = None
    """Expected output format. One of :attr:`valid_formats`."""

    metadata: bool = True
    """Kept for parity with the shared CLI options. Currently not used."""

    useuris: bool | None = None
    """Kept for parity with the shared CLI options. Currently not used."""

    include_generation_date: bool = False
    """Kept for parity with the shared CLI options. ohi LinkML output never carries a
    timestamp, so it is reproducible either way."""

    log_level: int | None = DEFAULT_LOG_LEVEL_INT
    """Logging level, 0 is minimum."""

    mergeimports: bool | None = True
    """Legacy option, always assumed to be True."""

    source_file_date: str | None = None
    """Modification date of the input source file."""

    source_file_size: int | None = None
    """Size of the source file in bytes."""

    logger: logging.Logger | None = None
    """Logger to use for logging messages."""

    verbose: bool | None = None
    """Verbosity."""

    output: str | None = None
    """Path to output file. Writing it is up to the CLI, as it is for other generators."""

    directory_output: bool = False
    """True means output is to a directory, False is to stdout."""

    base_dir: str | None = None
    """Directory that the relative locations in :attr:`importmap` are relative to.

    When :attr:`schema` has no file, such as YAML text, its relative imports are read from this
    directory too. Without it, they are read from the current directory.
    """

    importmap: str | Mapping[str, Any] | TextIO | None = None
    """Where to load imports from, as in LinkML-Python.

    A mapping from an import, a CURIE prefix such as ``units:``, or a URI, to the location to load
    it from. It can also be the path of a JSON or YAML file with such a mapping, an open file, or
    the JSON or YAML text. A value can also be a schema, as a dict, to load from memory.

    Relative locations are relative to the directory of the map file when the map is given as a
    path. Otherwise, including the open file that ``--importmap`` passes, they are relative to
    :attr:`base_dir`, or else to the directory of :attr:`schema`. LinkML-Python uses the directory
    of the importing schema instead of the last one. The two differ only when a schema in another
    directory uses the same import map entry.
    """

    stacktrace: bool = False
    """True means print stack trace, false just error message."""

    include: str | Path | SchemaDefinition | None = None
    """An extra schema to merge in, outside of the imports mechanism, as in LinkML-Python.

    Its elements are added to the schema, unless the schema already has one with the same name.
    Its imports are not. A path, YAML text, or a parsed schema.
    """

    _ohi_schema: Any = field(default=None, init=False, repr=False)

    _source: SchemaSource | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.logger:
            self.logger = logger
        self._init_common()
        if isinstance(self.schema, GeneratorBase):
            # As in LinkML-Python, the other generator's import options apply, unless these are set.
            self.base_dir = self.base_dir or self.schema.base_dir
            self.importmap = self.importmap if self.importmap is not None else self.schema.importmap
        if isinstance(self.schema, TextIOBase):
            # An open file can be read only once, and may be closed before the schema is loaded.
            self._source = schema_source(self.schema, self.base_dir)
        elif not isinstance(self.schema, SchemaDefinition | SchemaView | GeneratorBase):
            # Fail fast on a missing file or a URL. A parsed schema can still change, so it's
            # read when it's loaded, as LinkML-Python does.
            schema_source(self.schema, self.base_dir)

    @property
    def source(self) -> SchemaSource:
        """Where ohi LinkML reads the schema from, with :attr:`include` merged in.

        Worked out when the schema is loaded, so that changes to a parsed schema up to then are
        kept, as in LinkML-Python.
        """
        source = self._source or schema_source(self.schema, self.base_dir)
        if self.include is not None:
            source = merge_include(source, self.include)
        return source

    @property
    def generatorversion(self) -> str:
        """The ohi LinkML version doing the translation, read from the ABI."""
        return build_info()["linkml_scala_version"]

    @property
    def ohi_schema(self):
        """The schema as ohi LinkML sees it, loaded on first use and then reused.

        :return: a ``ohi_linkml.Schema``, owned by this generator. Do not close it; call
            :meth:`close` instead.
        :raises ImportError: if the ohi LinkML bindings are not installed.
        :raises ohi_linkml.SchemaLoadError: if ohi LinkML cannot load the schema.
        """
        if self._ohi_schema is None:
            ohi_linkml = bindings()
            self._ohi_schema = self._load(ohi_linkml)
            for issue in self._ohi_schema.issues(ohi_linkml.ERROR) + self._ohi_schema.issues(ohi_linkml.FATAL):
                self.logger.warning(f"ohi LinkML reported: {issue.get('message', issue)}")
        return self._ohi_schema

    def _load(self, ohi_linkml):
        """Load the schema into ohi LinkML.

        A schema with a file is loaded from it, with its text from memory if there is one, so
        that ohi LinkML resolves imports relative to it, and imports that lead back to it reach
        the same schema.

        :param ohi_linkml: the bindings module.
        :return: a ``ohi_linkml.Schema``.
        """
        source = self.source
        import_map, imports = ohi_import_options(self.importmap, self.base_dir or source.directory)
        if source.location is None:
            return ohi_linkml.load_string(source.text, imports, base_dir=source.directory, import_map=import_map)
        if source.text is not None:
            imports[str(source.location)] = source.text
        return ohi_linkml.load_file(source.location, imports=imports, import_map=import_map)

    def close(self) -> None:
        """Release the loaded schema. Calling it more than once is fine."""
        schema, self._ohi_schema = self._ohi_schema, None
        if schema is not None:
            schema.close()

    def __enter__(self) -> "OhiBackedGenerator":
        return self

    def __exit__(self, *exception: object) -> None:
        self.close()
