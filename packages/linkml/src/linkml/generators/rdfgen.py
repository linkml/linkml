"""
YAML Schema to RDF Generator

Generate a JSON LD representation of the model

"""

import json
import os
import urllib.parse as urlparse
from copy import deepcopy
from dataclasses import dataclass

import click
from rdflib import Graph
from rdflib.plugin import Parser as rdflib_Parser
from rdflib.plugin import plugins as rdflib_plugins

from linkml import LOCAL_METAMODEL_LDCONTEXT_FILE
from linkml._version import __version__
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph

#: ``@context`` string entries whose URI scheme is in this set are kept when
#: ``RDFGenerator`` strips relative per-module refs before handing the JSON-LD
#: to rdflib. ``http``/``https`` cover published context documents (e.g.
#: ``https://w3id.org/linkml/types.context.jsonld``); ``file`` covers the
#: vendored metamodel context absolutized by ``JSONLDGenerator.end_schema``.
_RESOLVABLE_CONTEXT_URI_SCHEMES = frozenset({"http", "https", "file"})


def _strip_relative_context_refs(jsonld_str: str) -> str:
    """Drop relative-path string entries from the JSON-LD ``@context`` array.

    ``JSONLDGenerator.end_schema`` appends one ``<import>.context.jsonld``
    string per loaded import. For sibling-relative imports these refs have no
    URI scheme (e.g. ``./base.context.jsonld``) and rdflib resolves them
    against ``@base`` — typically an ``https://`` schema URI — producing
    HTTP 404s because no such context file is published.

    ``gen-rdf`` always merges imports into the working schema before
    serialization, so the prefix bindings and class definitions those
    per-module refs would otherwise contribute are already inlined. Filtering
    the unresolvable refs is safe and converts the failure into a no-op.

    Absolute URIs (``http``/``https``/``file``) and inline ``@context``
    dicts (including the ``@base`` directive emitted by ``JSONLDGenerator``)
    are preserved unchanged.
    """
    doc = json.loads(jsonld_str)
    context = doc.get("@context")
    if not isinstance(context, list):
        return jsonld_str

    def _is_resolvable(entry):
        if not isinstance(entry, str):
            return True
        return urlparse.urlparse(entry).scheme in _RESOLVABLE_CONTEXT_URI_SCHEMES

    filtered = [entry for entry in context if _is_resolvable(entry)]
    if len(filtered) == len(context):
        return jsonld_str
    doc["@context"] = filtered
    return json.dumps(doc)


@dataclass
class RDFGenerator(Generator):
    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    # TODO: we leave ttl as default for backwards compatibility but nt is
    # recommended, see https://github.com/linkml/linkml/issues/163
    valid_formats = ["ttl"] + sorted([x.name for x in rdflib_plugins(None, rdflib_Parser) if "/" not in str(x.name)])
    visit_all_class_slots = False
    uses_schemaloader = True

    # ObjectVars
    emit_metadata: bool = False
    context: list[str] = None
    original_schema: SchemaDefinition = None
    """See https://github.com/linkml/linkml/issues/871"""

    def __post_init__(self):
        self.original_schema = deepcopy(self.schema)
        super().__post_init__()

    def _data(self, g: Graph) -> str:
        fmt = "turtle" if self.format == "ttl" else self.format
        return canonicalize_rdf_graph(g, output_format=fmt)

    def end_schema(self, output: str | None = None, context: str = None, **_) -> str:
        gen = JSONLDGenerator(
            self.original_schema,
            format=JSONLDGenerator.valid_formats[0],
            metadata=self.emit_metadata,
            importmap=self.importmap,
            metamodel_context=LOCAL_METAMODEL_LDCONTEXT_FILE,
        )
        # Iterate over permissible text strings making them URI compatible
        for e in gen.schema.enums.values():
            for pv in e.permissible_values.values():
                pv.text = urlparse.quote(pv.text)
        jsonld_str = gen.serialize(context=context)

        # Drop unresolvable per-module ``@context`` refs that
        # ``JSONLDGenerator`` adds for each loaded import (e.g.
        # ``./base.context.jsonld``); see ``_strip_relative_context_refs``.
        jsonld_str = _strip_relative_context_refs(jsonld_str)

        graph = Graph()
        graph.parse(
            data=jsonld_str,
            format="json-ld",
            base=str(self.namespaces._base),
            prefix=True,
        )
        if output:
            out = self._data(graph)
            with open(output, "w", encoding="UTF-8") as outf:
                outf.write(out)
            return out

        return self._data(graph)


@shared_arguments(RDFGenerator)
@click.command(name="rdf")
@click.option("-o", "--output", help="Output file name")
@click.option(
    "--context",
    default=[LOCAL_METAMODEL_LDCONTEXT_FILE],
    show_default=True,
    multiple=True,
    help="JSONLD context file (default: vendored meta.context.jsonld)",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **kwargs):
    """Generate an RDF representation of a LinkML model"""
    print(RDFGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
