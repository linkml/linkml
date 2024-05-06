"""
YAML Schema to RDF Generator

Generate a JSON LD representation of the model

"""

import os
import urllib.parse as urlparse
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Optional

import click
from linkml_runtime.linkml_model import SchemaDefinition
from rdflib import Graph
from rdflib.plugin import Parser as rdflib_Parser
from rdflib.plugin import plugins as rdflib_plugins

from linkml import METAMODEL_CONTEXT_URI
from linkml._version import __version__
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.utils.generator import Generator, shared_arguments


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
    context: List[str] = None
    original_schema: SchemaDefinition = None
    """See https://github.com/linkml/linkml/issues/871"""

    def __post_init__(self):
        self.original_schema = deepcopy(self.schema)
        super().__post_init__()

    def _data(self, g: Graph) -> str:
        return g.serialize(format="turtle" if self.format == "ttl" else self.format)

    def end_schema(self, output: Optional[str] = None, context: str = None, **_) -> str:
        gen = JSONLDGenerator(
            self.original_schema,
            format=JSONLDGenerator.valid_formats[0],
            metadata=self.emit_metadata,
            importmap=self.importmap,
        )
        # Iterate over permissible text strings making them URI compatible
        for e in gen.schema.enums.values():
            for pv in e.permissible_values.values():
                pv.text = urlparse.quote(pv.text)
        jsonld_str = gen.serialize(context=context)

        graph = Graph()
        graph.parse(
            data=jsonld_str,
            format="json-ld",
            base=str(self.namespaces._base),
            prefix=True,
        )
        out = self._data(graph)
        if output:
            with open(output, "w", encoding="UTF-8") as outf:
                outf.write(out)

        return out


@shared_arguments(RDFGenerator)
@click.command()
@click.option("-o", "--output", help="Output file name")
@click.option(
    "--context",
    default=[METAMODEL_CONTEXT_URI],
    show_default=True,
    multiple=True,
    help=f"JSONLD context file (default: {METAMODEL_CONTEXT_URI})",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **kwargs):
    """Generate an RDF representation of a LinkML model"""
    print(RDFGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
