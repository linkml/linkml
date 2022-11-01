"""
YAML Schema to RDF Generator

Generate a JSON LD representation of the model

"""
import os
import urllib.parse as urlparse
from dataclasses import dataclass, field
from typing import Optional, TextIO, Union, List

import click
from linkml_runtime.linkml_model.meta import SchemaDefinition
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
    # TODO: we leave ttl as default for backwards compatibility but nt is recommended, see https://github.com/linkml/linkml/issues/163
    valid_formats = ["ttl"] + sorted(
        [x.name for x in rdflib_plugins(None, rdflib_Parser) if "/" not in str(x.name)]
    )
    visit_all_class_slots = False
    uses_schemaloader = True

    # ObjectVars
    emit_metadata: bool = field(default_factory=lambda: False)
    context: List[str] = None


    def _data(self, g: Graph) -> str:
        return g.serialize(
            format="turtle" if self.format == "ttl" else self.format
        ).decode()

    def end_schema(
        self, output: Optional[str] = None, context: str = None, **_
    ) -> None:
        gen = JSONLDGenerator(
            self,
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
        if output:
            with open(output, "w", encoding="UTF-8") as outf:
                outf.write(self._data(graph))
        else:
            print(self._data(graph))


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
