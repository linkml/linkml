"""The contract every LinkML generator satisfies, including generators written in Python
and those wrapping other implementations (e.g., in Scala).

:class:`~linkml.utils.generator.Generator` implements this contract using the Python classes
``SchemaLoader`` and ``SchemaView``.
"""

import abc
import logging
from collections.abc import Mapping
from pathlib import Path
from typing import Any, ClassVar


class GeneratorBase(metaclass=abc.ABCMeta):
    """Base class for every generator, independent of the used LinkML implementation.

    Deliberately **not** a dataclass. Subclasses declare the attributes below as their own
    dataclass fields, which keeps each generator's constructor signature and field order under
    its own control.

    Subclasses must:

    - declare a dataclass field for :attr:`schema` and for every option they honor,
    - call :meth:`_init_common` from ``__post_init__``,
    - implement :meth:`serialize`.
    """

    # ClassVars

    generatorname: ClassVar[str] = None
    """Name of the generator. Override with ``os.path.basename(__file__)``."""

    generatorversion: ClassVar[str] = None
    """Version of the generator."""

    valid_formats: ClassVar[list[str]] = []
    """Allowed formats. The first one is the default."""

    file_extension: ClassVar[str] = None
    """Extension for output files, without the leading dot."""

    # Attributes every generator is expected to have. Annotations only, so that the dataclass
    # machinery in subclasses does not pick them up as fields.

    schema: Any
    """The schema to generate from. What is accepted is up to the subclass."""

    format: str | None
    """Expected output format. One of :attr:`valid_formats`."""

    metadata: bool
    """True means include date, generator, etc. information in the output if appropriate."""

    useuris: bool | None
    """True means declared class slot uri's are used. False means use model uris."""

    log_level: int | None
    """Logging level, 0 is minimum."""

    logger: logging.Logger | None
    """Logger to use for logging messages."""

    verbose: bool | None
    """Verbosity."""

    mergeimports: bool | None
    """True means merge imported sources into the importing package. False means keep separate."""

    source_file_date: str | None
    """Modification date of the input source file."""

    source_file_size: int | None
    """Size of the source file in bytes."""

    output: str | None
    """Path to output file. Note all generators may not implement this uniformly, see
    https://github.com/linkml/linkml/issues/923"""

    directory_output: bool
    """True means output is to a directory, False is to stdout."""

    base_dir: str | None
    """Working directory or base URL of sources. Setting this is necessary for correct retrieval
    of relative imports."""

    importmap: str | Mapping[str, str] | None
    """File name of import mapping file -- maps import name/uri to target."""

    include: str | Path | Any | None
    """If set, include extra schema outside of the imports mechanism."""

    stacktrace: bool
    """True means print stack trace, false just error message."""

    def _init_common(self) -> None:
        """Apply the common options that do not depend on a specific LinkML implementation.

        :raises ValueError: if :attr:`format` is not one of :attr:`valid_formats`.
        """
        if self.log_level is not None:
            self.logger.setLevel(self.log_level)
        if self.format is None:
            self.format = self.valid_formats[0]
        if self.format not in self.valid_formats:
            raise ValueError(f"Unrecognized format: {self.format}; known={self.valid_formats}")
        if not self.metadata:
            self.source_file_date = None
            self.source_file_size = None

    @abc.abstractmethod
    def serialize(self, **kwargs) -> str:
        """Generate output in :attr:`format`.

        :param kwargs: generator specific parameters.
        :return: the generated output.
        """
        raise NotImplementedError
