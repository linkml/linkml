"""Generate an `Apache Ossie <https://github.com/apache/ossie>`_ ontology from a LinkML schema.

The translation itself is not implemented here. This module is a thin wrapper around the Ossie
generator in `LinkML-Scala <https://github.com/NeverBlink-OSS/linkml-scala>`_, using
its Python bindings. See :mod:`linkml.generators.common.scala` for the shared machinery. Report
bugs in the output in the LinkML-Scala repository.

Classes become ``EntityType`` concepts, enums and types become ``ValueType`` concepts, slots
become relationships, and ``is_a`` and ``mixins`` become ``extends``.
"""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

import click

from linkml.generators.common.scala import ScalaBackedGenerator, print_versions
from linkml.utils.generator import shared_arguments

PRUNING_MODES = ("skip", "schema", "treeRoot")
"""Pruning modes LinkML-Scala accepts, spelled as in its own CLI."""


@dataclass
class OssieGenerator(ScalaBackedGenerator):
    """Generates an Ossie ontology describing the schema's classes, slots, enums and types.

    >>> from linkml.generators.ossiegen import OssieGenerator
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
    >>> print(OssieGenerator(schema).serialize())
    version: 0.2.0.dev0
    name: personinfo
    ontology:
      - concept: Person
        type: EntityType
        description: A human being
        relationships:
          - name: age
            roles:
              - concept: Integer
            multiplicity: ManyToOne
            verbalizes:
              - "{Person} age {Integer}"
    <BLANKLINE>
    """

    generatorname: ClassVar[str] = os.path.basename(__file__)
    valid_formats: ClassVar[list[str]] = ["yaml", "json"]
    file_extension: ClassVar[str] = "ossie.yaml"

    pruning_mode: str = "skip"
    """Which classes, enums and types become concepts. One of :data:`PRUNING_MODES`."""

    tree_root: str | None = None
    """Class to prune from instead of the schema's own ``tree_root``. Only valid with
    ``pruning_mode="treeRoot"``."""

    def _generate(self, fmt: str) -> str:
        """Ask LinkML-Scala for the ontology in one of the supported serialization formats.

        :param fmt: ``yaml`` or ``json``.
        :return: the serialized ontology.
        """
        return self.scala_schema.ossie(pruning_mode=self.pruning_mode, tree_root=self.tree_root, output_format=fmt)

    def as_yaml(self) -> str:
        """Generate the Ossie ontology as YAML.

        :return: the ontology in YAML.
        """
        return self._generate("yaml")

    def as_json(self) -> str:
        """Generate the Ossie ontology as JSON.

        :return: the ontology in JSON.
        """
        return self._generate("json")

    def as_dict(self) -> dict[str, Any]:
        """Generate the Ossie ontology as a Python dictionary.

        Parsed from the JSON.

        :return: the parsed ontology.
        """
        return json.loads(self.as_json())

    def serialize(self, **kwargs) -> str:
        """Generate the Ossie ontology in :attr:`format`.

        :param kwargs: ignored, so the shared CLI options can be passed straight through.
        :return: the serialized ontology.
        """
        return self._generate(self.format)


@shared_arguments(OssieGenerator)
@click.option(
    "--pruning-mode",
    type=click.Choice(PRUNING_MODES),
    default="skip",
    show_default=True,
    help="Which unused elements (classes, types, enums) to remove. "
    "treeRoot - remove all elements unreachable from the tree_root class. "
    "schema - remove all elements unreachable from any of the classes defined in the root schema. "
    "skip - do not remove unused elements.",
)
@click.option("--tree-root", help="Tree root class name to use instead of the schema-defined tree_root.")
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
@click.command(name="ossie")
def cli(yamlfile, **args):
    """Generate an Apache Ossie ontology from a LinkML model.

    Classes become EntityType concepts, enums and types become ValueType concepts, slots become
    relationships, and is_a and mixins become extends. Use --pruning-mode to leave out elements
    that are not reachable from the root schema or from the tree root class.

    The generator is implemented in LinkML-Scala, which is maintained separately. Please submit
    bug reports and feature requests to https://github.com/NeverBlink-OSS/linkml-scala
    """
    with OssieGenerator(yamlfile, **args) as generator:
        ontology = generator.serialize()
        if generator.output:
            Path(generator.output).write_text(ontology)
        else:
            print(ontology)


if __name__ == "__main__":
    cli()
