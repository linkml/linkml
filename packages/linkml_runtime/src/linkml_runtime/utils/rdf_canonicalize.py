"""Deterministic RDF serialization, provided by the ``diffable-rdf`` library.

The graph is canonicalized with RDFC-1.0, sorted, and serialized. Graphs that
pyoxigraph cannot hold -- literal predicates from SHACL annotation mode, or
relative IRIs such as the metamodel's ``bibo:status <testing>`` -- fall back to
rdflib with content-derived blank-node labels, which is still reproducible
across processes. The library's ``docs/api.md`` documents the full contract
and its limitations.

This module adapts the library's reporting: the library logs degraded output
through :mod:`logging`, which is silent without a configured handler, while
linkml emits :class:`RDFCanonicalizationWarning` so that a user running a
generator sees it by default.
"""

import logging
import warnings

import rdflib
from diffable_rdf import canonicalize_rdf_graph as _canonicalize_rdf_graph


class RDFCanonicalizationWarning(UserWarning):
    """Issued when ``canonicalize_rdf_graph`` produces output via a degraded path.

    Surfaced via ``warnings.warn`` (not the ``logging`` module) so that it is
    visible by default to both CLI users and library API consumers regardless
    of logging configuration. Filterable with
    ``warnings.filterwarnings("ignore", category=RDFCanonicalizationWarning)``.
    """


_LIBRARY_LOGGER = "diffable_rdf"


class _DegradedPathWarnings(logging.Handler):
    """Collect the library's warning logs and re-emit them as Python warnings.

    Records are collected during the call and re-emitted in :meth:`__exit__`
    rather than from :meth:`emit`. Warning at the moment the record arrives
    would put eight ``logging`` frames plus an unknown number of library frames
    between :func:`warnings.warn` and the caller, and the library's depth
    differs per message, so no single ``stacklevel`` could point at the caller.
    Re-emitting from ``__exit__`` makes the distance a constant.

    The handler is attached to the library's package logger rather than the
    root logger. The library logs under module-level children such as
    ``diffable_rdf.canonicalize``, which propagate to the package logger, so
    attaching there catches every module without naming any of them.

    ``propagate`` is left alone: a caller who *did* configure logging still
    gets the record through their own handlers, and seeing the message once
    per mechanism is a better trade than suppressing a handler they asked for.
    """

    def __init__(self) -> None:
        super().__init__(level=logging.WARNING)
        self._messages: list[str] = []
        self._logger = logging.getLogger(_LIBRARY_LOGGER)
        self._previous_level = logging.NOTSET

    def emit(self, record: logging.LogRecord) -> None:
        """Record one formatted message for re-emission on exit."""
        self._messages.append(record.getMessage())

    def __enter__(self) -> "_DegradedPathWarnings":
        """Attach to the library's logger, raising its level if it is silent."""
        self._previous_level = self._logger.level
        if not self._logger.isEnabledFor(logging.WARNING):
            self._logger.setLevel(logging.WARNING)
        self._logger.addHandler(self)
        return self

    def __exit__(self, *exc_info: object) -> None:
        """Detach, restore the logger, and re-emit what was collected.

        Runs on the exception path too, so a caller who gets an exception still
        learns about the degradation that preceded it.
        """
        self._logger.removeHandler(self)
        self._logger.setLevel(self._previous_level)
        for message in self._messages:
            # 3 frames: warnings.warn, this method, and the ``with`` statement
            # in canonicalize_rdf_graph -- so the warning lands on its caller.
            warnings.warn(message, RDFCanonicalizationWarning, stacklevel=3)


def canonicalize_rdf_graph(
    graph: rdflib.Graph,
    output_format: str = "turtle",
    diff_stable: bool = False,
) -> str:
    """Serialize an rdflib Graph deterministically using RDFC-1.0 canonicalization.

    The graph is transferred to pyoxigraph via N-Triples, canonicalized with
    RDFC-1.0, sorted, and serialized back to the requested format. Prefix
    bindings from the rdflib Graph are preserved in the output for formats that
    support them (Turtle, TriG, N3, RDF/XML).

    Falls back to plain rdflib serialization for unsupported formats or graphs
    containing non-standard RDF (e.g. literal predicates), warning with
    :class:`RDFCanonicalizationWarning` so that the caller knows the output is
    less strongly guaranteed than usual.

    :param graph: The rdflib Graph to serialize.
    :param output_format: Target serialization format (e.g. ``"turtle"``, ``"nt"``).
    :param diff_stable: Use diffable-rdf labels to reduce blank-node churn across
        edits. Disabled by default. The non-standard RDF fallback warns when it
        cannot apply these labels.
        See https://linkml.io/linkml/howtos/collaborative-development.html#rdf-in-version-control
    :return: Deterministic string serialization of the graph.
    :raises ValueError: If the graph cannot be serialized to ``output_format``
        in a form that parses back -- notably a line-oriented format asked to
        write a relative IRI, which N-Triples forbids.
    """
    # Frames between warnings.warn and this function's caller are counted in
    # _DegradedPathWarnings.__exit__, which is where the re-emission happens.
    with _DegradedPathWarnings():
        return _canonicalize_rdf_graph(graph, output_format=output_format, diff_stable=diff_stable)
