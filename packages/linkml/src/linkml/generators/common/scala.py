"""Shared utilities for generators implemented as wrappers around LinkML-Scala.

`LinkML-Scala <https://github.com/NeverBlink-OSS/linkml-scala>`_ is an independent LinkML
implementation with its own generators. It's packaged as a natively-compiled library with
Python bindings (the ``neverblink-linkml`` package on PyPI). A generator built on this base
is a wrapper: report bugs in the output to LinkML-Scala.
"""

import functools
import logging
import platform
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

LinkML-Scala resolves imports itself, from disk, relative to the schema being read, and currently
does not support these options.

Upstream issue: https://github.com/NeverBlink-OSS/linkml-scala/issues/210
"""

SUPPORTED_PLATFORMS = "Linux and macOS on x86-64 and ARM64, and Windows on x86-64"
"""Help text for platforms for which LinkML-Scala has binary builds.

This reflects the wheels available at https://pypi.org/project/neverblink-linkml/#files
Keep this in sync with the rules in ``packages/linkml/pyproject.toml``.
"""


def bindings():
    """Import the LinkML-Scala Python bindings.

    Imported lazily so that ``linkml`` stays importable on platforms LinkML-Scala is not built for.

    :return: the ``linkml_scala`` module.
    :raises ImportError: if the bindings are not installed, which normally means this platform
        is not supported.
    """
    try:
        import linkml_scala
    except ImportError as exc:  # pragma: no cover - depends on the platform
        raise ImportError(
            f"This generator is not available on {platform.system()} {platform.machine()}. "
            "It is implemented by LinkML-Scala, which ships as a natively-compiled library, and "
            f"there is no build of it for this platform. Supported: {SUPPORTED_PLATFORMS}. "
            "Request support for your platform here: "
            "https://github.com/NeverBlink-OSS/linkml-scala/issues/new"
        ) from exc
    return linkml_scala


@functools.cache
def build_info() -> dict[str, Any]:
    """Version and build metadata for the LinkML-Scala library the bindings loaded.

    :return: the metadata, with keys including ``linkml_scala_version`` and
        ``metamodel_version``.
    """
    return bindings().build_info()


def print_versions(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    """Print the linkml and LinkML-Scala versions and exit, as an eager ``--version`` callback.

    Wire it into a generator's CLI with::

        @click.option("-V", "--version", is_flag=True, is_eager=True, expose_value=False,
                      callback=print_versions,
                      help="Show the linkml and LinkML-Scala versions and exit.")

    :param ctx: the click context, exited once the versions are printed.
    :param param: the click parameter. Unused, but click passes it.
    :param value: whether the flag was given.
    """
    if not value or ctx.resilient_parsing:
        return
    info = build_info()
    click.echo(f"linkml {__version__}")
    click.echo(f"LinkML-Scala {info['linkml_scala_version']} (metamodel {info['metamodel_version']})")
    ctx.exit()


@dataclass
class ScalaBackedGenerator(GeneratorBase, metaclass=ABCMeta):
    """Base class for generators that use LinkML-Scala.

    Subclasses set :attr:`valid_formats` and implement
    :meth:`~linkml.utils.generator_base.GeneratorBase.serialize` by calling one method on
    :attr:`scala_schema`.

    Loading a schema is the expensive part and every generator call on a loaded schema is cheap,
    so :attr:`scala_schema` is built on first use and then reused. Release it with
    :meth:`close`, or use the generator as a context manager::

        with SomeGenerator("schema.yaml") as generator:
            print(generator.serialize())

    Dropping the last reference will release it too, but only when the garbage collector gets to it.

    Unlike :class:`~linkml.utils.generator.Generator` this takes a path and nothing else, and
    nothing here parses the schema: LinkML-Scala reads it, resolves its imports, and is the only
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

    _scala_schema: Any = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.logger:
            self.logger = logger
        self._init_common()
        if not isinstance(self.schema, str | Path):
            raise TypeError(
                f"{type(self).__name__} needs a path to a schema file, or the schema as YAML "
                f"text, not a {type(self.schema).__name__}. LinkML-Scala reads and resolves the "
                "schema itself, so can't work with a parsed Python object. "
                "See https://github.com/NeverBlink-OSS/linkml-scala"
            )
        if not self.schema_is_yaml_text and not Path(self.schema).is_file():
            raise FileNotFoundError(f"no such schema file: {self.schema}")
        refused = [name for name in UNSUPPORTED_OPTIONS if getattr(self, name)]
        if refused:
            raise NotImplementedError(
                f"{type(self).__name__} does not support {', '.join(refused)}. LinkML-Scala "
                "resolves imports itself and has no equivalent option yet. "
                "Upstream issue: https://github.com/NeverBlink-OSS/linkml-scala/issues/210"
            )

    @property
    def schema_is_yaml_text(self) -> bool:
        """Heuristic to test if :attr:`schema` is the schema itself rather than a path to it."""
        return isinstance(self.schema, str) and "\n" in self.schema

    @property
    def generatorversion(self) -> str:
        """The LinkML-Scala version doing the translation, read from the ABI."""
        return build_info()["linkml_scala_version"]

    @property
    def scala_schema(self):
        """The schema as LinkML-Scala sees it, loaded on first use and then reused.

        :return: a ``linkml_scala.Schema``, owned by this generator. Do not close it; call
            :meth:`close` instead.
        :raises ImportError: if this platform has no LinkML-Scala build.
        :raises linkml_scala.SchemaLoadError: if LinkML-Scala cannot load the schema.
        """
        if self._scala_schema is None:
            linkml_scala = bindings()
            self._scala_schema = self._load(linkml_scala)
            for issue in self._scala_schema.issues(linkml_scala.ERROR) + self._scala_schema.issues(linkml_scala.FATAL):
                self.logger.warning(f"LinkML-Scala reported: {issue.get('message', issue)}")
        return self._scala_schema

    def _load(self, linkml_scala):
        """Load the schema into LinkML-Scala.

        :param linkml_scala: the bindings module.
        :return: a ``linkml_scala.Schema``.
        """
        if self.schema_is_yaml_text:
            return linkml_scala.load_string(self.schema)
        return linkml_scala.load_file(self.schema)

    def close(self) -> None:
        """Release the loaded schema. Calling it more than once is fine."""
        schema, self._scala_schema = self._scala_schema, None
        if schema is not None:
            schema.close()

    def __enter__(self) -> "ScalaBackedGenerator":
        return self

    def __exit__(self, *exception: object) -> None:
        self.close()
