"""Generate an `RDFS <https://www.w3.org/TR/rdf-schema/>`_ vocabulary from a LinkML schema.

The translation itself is not implemented here. This module is a thin wrapper around the RDFS
generator in `LinkML-Scala <https://github.com/NeverBlink-OSS/linkml-scala>`_, using
its Python bindings. See :mod:`linkml.generators.common.scala` for the shared machinery. Report
bugs in the output in the LinkML-Scala repository.

Classes and enums become ``rdfs:Class``, slots become ``rdf:Property`` with an ``rdfs:range``,
and ``is_a`` becomes ``rdfs:subClassOf`` on classes and ``rdfs:subPropertyOf`` on slots. See
:mod:`linkml.generators.owlgen` if you need the full expressiveness of OWL: cardinality,
disjoint classes or class expressions.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import click
from rdflib import Graph

from linkml.generators.common.scala import ScalaBackedGenerator, print_versions
from linkml.utils.generator import shared_arguments


@dataclass
class RdfsGenerator(ScalaBackedGenerator):
    """Generates an RDFS vocabulary describing the schema's classes, slots and enums.

    >>> from linkml.generators.rdfsgen import RdfsGenerator
    >>> schema = '''
    ... id: https://example.org/personinfo
    ... name: personinfo
    ... prefixes:
    ...   linkml: https://w3id.org/linkml/
    ...   personinfo: https://example.org/personinfo/
    ... default_prefix: personinfo
    ... default_range: string
    ... imports:
    ...   - linkml:types
    ... classes:
    ...   Person:
    ...     description: A human being
    ...     attributes:
    ...       age:
    ...         range: integer
    ... '''
    >>> print(RdfsGenerator(schema).serialize())
    PREFIX personinfo: <https://example.org/personinfo/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    <BLANKLINE>
    personinfo:Person a rdfs:Class ;
      rdfs:comment "A human being" .
    <BLANKLINE>
    personinfo:age a rdf:Property ;
      rdfs:range xsd:integer .
    <BLANKLINE>
    """

    generatorname: ClassVar[str] = os.path.basename(__file__)
    valid_formats: ClassVar[list[str]] = ["ttl", "nt"]
    file_extension: ClassVar[str] = "rdfs.ttl"

    # TODO: document supported vs unsupported features
    # TODO: link to this generator from owlgen and shaclgen as an alternative

    exclude_imports: bool = False
    """Leave imported classes and enums out, spelled as in ``gen-shacl``.

    Becomes LinkML-Scala's ``only_classes_from_root_schema``.
    """

    def _generate(self, fmt: str) -> str:
        """Ask LinkML-Scala for the vocabulary in one of the serializations it writes itself.

        :param fmt: ``ttl`` or ``nt``.
        :return: the serialized vocabulary, byte for byte as LinkML-Scala produced it.
        """
        return self.scala_schema.rdfs(only_classes_from_root_schema=self.exclude_imports, format=fmt)

    def as_turtle(self) -> str:
        """Generate the RDFS vocabulary as Turtle, prefixed and pretty-printed upstream.

        Which prefixes get declared is up to the schema's ``emit_prefixes``.

        :return: the vocabulary in Turtle.
        """
        return self._generate("ttl")

    def as_ntriples(self) -> str:
        """Generate the RDFS vocabulary as N-Triples.

        :return: the vocabulary in N-Triples.
        """
        return self._generate("nt")

    def as_graph(self) -> Graph:
        """Generate the RDFS vocabulary as an rdflib graph.

        Parsed from the Turtle, so the prefixes are preserved.

        :return: the parsed vocabulary.
        """
        return Graph(bind_namespaces="none").parse(data=self.as_turtle(), format="turtle")

    def serialize(self, **kwargs) -> str:
        """Generate the RDFS vocabulary in :attr:`format`.

        :param kwargs: ignored, so the shared CLI options can be passed straight through.
        :return: the serialized vocabulary.
        """
        return self._generate(self.format)


@shared_arguments(RdfsGenerator)
@click.option(
    "--exclude-imports/--include-imports",
    default=False,
    show_default=True,
    help="Use --exclude-imports to exclude imported classes and enums from the generated "
    "vocabulary. Imported slots are still emitted. This is useful if you generate a vocabulary "
    "per schema file and combine them afterwards.",
)
@click.option("-o", "--output", help="Output file name. Writes to stdout if not given.")
@click.option(
    "-V",
    "--version",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=print_versions,
    help="Show the linkml and LinkML-Scala versions and exit.",
)
@click.command(name="rdfs")
def cli(yamlfile, **args):
    """Generate an RDFS vocabulary from a LinkML model.

    Classes and enums become rdfs:Class, slots become rdf:Property with an rdfs:range, and is_a
    becomes rdfs:subClassOf on classes and rdfs:subPropertyOf on slots. Use --exclude-imports to
    describe only the classes and enums the root schema declares.

    RDFS cannot express cardinality, disjoint classes or class expressions. Use gen-owl for
    those, or gen-shacl to validate data.

    The generator is implemented in LinkML-Scala, which is maintained separately. Please submit
    bug reports and feature requests to https://github.com/NeverBlink-OSS/linkml-scala
    """
    with RdfsGenerator(yamlfile, **args) as generator:
        vocabulary = generator.serialize()
        if generator.output:
            Path(generator.output).write_text(vocabulary)
        else:
            print(vocabulary)


if __name__ == "__main__":
    cli()
