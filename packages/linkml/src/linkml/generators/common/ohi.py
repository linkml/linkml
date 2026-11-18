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
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import click

from linkml._version import __version__
from linkml.cli.logging import DEFAULT_LOG_LEVEL_INT
from linkml.utils.generator_base import GeneratorBase

logger = logging.getLogger(__name__)

UNSUPPORTED_OPTIONS = ("importmap", "base_dir", "include")
"""Unsupported options that change how imports should be resolved.

ohi LinkML resolves imports itself, from disk, relative to the schema being read, and currently
does not support these options.

Upstream issue: https://github.com/NeverBlink-OSS/ohi/issues/210
"""


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

    Unlike :class:`~linkml.utils.generator.Generator` this takes a path and nothing else, and
    nothing here parses the schema: ohi LinkML reads it, resolves its imports, and is the only
    thing that has an opinion about it. That is also why the options in
    :data:`UNSUPPORTED_OPTIONS` are refused rather than emulated.
    """

    schema: str | Path
    """Path to the schema file, or the schema itself as YAML text.

    URLs or parsed schemas are not supported.
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
    """Refused. See :data:`UNSUPPORTED_OPTIONS`."""

    importmap: str | Mapping[str, str] | None = None
    """Refused. See :data:`UNSUPPORTED_OPTIONS`."""

    stacktrace: bool = False
    """True means print stack trace, false just error message."""

    include: str | Path | None = None
    """Refused. See :data:`UNSUPPORTED_OPTIONS`."""

    _ohi_schema: Any = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.logger:
            self.logger = logger
        self._init_common()
        if not isinstance(self.schema, str | Path):
            raise TypeError(
                f"{type(self).__name__} needs a path to a schema file, or the schema as YAML "
                f"text, not a {type(self.schema).__name__}. ohi LinkML reads and resolves the "
                "schema itself, so can't work with a parsed Python object. "
                "See https://linkml.ohi.dev/docs/python-bindings/"
            )
        if not self.schema_is_yaml_text and not Path(self.schema).is_file():
            raise FileNotFoundError(f"no such schema file: {self.schema}")
        refused = [name for name in UNSUPPORTED_OPTIONS if getattr(self, name)]
        if refused:
            raise NotImplementedError(
                f"{type(self).__name__} does not support {', '.join(refused)}. ohi LinkML "
                "resolves imports itself and has no equivalent option yet. "
                "Upstream issue: https://github.com/NeverBlink-OSS/ohi/issues/210"
            )

    @property
    def schema_is_yaml_text(self) -> bool:
        """Heuristic to test if :attr:`schema` is the schema itself rather than a path to it."""
        return isinstance(self.schema, str) and "\n" in self.schema

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

        :param ohi_linkml: the bindings module.
        :return: a ``ohi_linkml.Schema``.
        """
        if self.schema_is_yaml_text:
            return ohi_linkml.load_string(self.schema)
        return ohi_linkml.load_file(self.schema)

    def close(self) -> None:
        """Release the loaded schema. Calling it more than once is fine."""
        schema, self._ohi_schema = self._ohi_schema, None
        if schema is not None:
            schema.close()

    def __enter__(self) -> "OhiBackedGenerator":
        return self

    def __exit__(self, *exception: object) -> None:
        self.close()
