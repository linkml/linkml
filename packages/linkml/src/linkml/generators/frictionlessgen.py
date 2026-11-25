"""Generate a `Frictionless Data Package <https://datapackage.org/>`_ from a LinkML schema.

The translation itself is not implemented here. This module is a thin wrapper around the
Frictionless generator in `ohi LinkML <https://linkml.ohi.dev/>`_, using its Python bindings. See
:mod:`linkml.generators.common.ohi` for the shared machinery. Report bugs in the output in the ohi
LinkML repository.

Every concrete class becomes a CSV table, described by its own Table Schema. Slots whose
range is a type or an enum become columns. A slot whose range is another class becomes either a
JSON column (when the range is inlined) or a column holding the other row's identifier, with a
foreign key to the other table.
"""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

import click

from linkml.generators.common.ohi import PRUNING_MODES, OhiBackedGenerator, print_versions
from linkml.utils.generator import shared_arguments

DATA_PACKAGE = "datapackage.json"
"""Name of the top-level descriptor, which refers to the table schemas in the other files."""


@dataclass
class FrictionlessGenerator(OhiBackedGenerator):
    """Generates a Frictionless Data Package with a table for each class of the schema.

    >>> from linkml.generators.frictionlessgen import FrictionlessGenerator
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
    ...       id:
    ...         identifier: true
    ...       age:
    ...         range: integer
    ... '''
    >>> generator = FrictionlessGenerator(schema)
    >>> list(generator.as_files())
    ['datapackage.json', 'schemas/person.json']
    >>> print(generator.serialize())
    {
      "profile": "tabular-data-package",
      "name": "personinfo",
      "id": "https://example.org/personinfo",
      "resources": [
        {
          "name": "person",
          "profile": "tabular-data-resource",
          "path": "data/person.csv",
          "format": "csv",
          "mediatype": "text/csv",
          "encoding": "utf-8",
          "description": "A human being",
          "schema": {
            "fields": [
              {
                "name": "age",
                "type": "integer",
                "constraints": {
                  "required": false
                },
                "rdfType": "http://www.w3.org/2001/XMLSchema#integer",
                "format": "default"
              },
              {
                "name": "id",
                "type": "string",
                "constraints": {
                  "required": true
                },
                "rdfType": "http://www.w3.org/2001/XMLSchema#string",
                "format": "default"
              }
            ],
            "primaryKey": "id"
          }
        }
      ]
    }
    """

    generatorname: ClassVar[str] = os.path.basename(__file__)
    valid_formats: ClassVar[list[str]] = ["json"]
    file_extension: ClassVar[str] = "json"

    pruning_mode: str = "skip"
    """Which classes become tables. One of :data:`~linkml.generators.common.ohi.PRUNING_MODES`."""

    tree_root: str | None = None
    """Class to prune from instead of the schema's own ``tree_root``. Only valid with
    ``pruning_mode="tree_root"``."""

    skip_classes_without_identifier: bool = False
    """Leave out the tables of classes with no identifier. Such a table has no primary key, so no
    other table can refer to it. The tree root always gets a table."""

    def as_files(self) -> dict[str, str]:
        """Generate the data package as separate files.

        :return: the JSON of each file, by its path relative to the package directory, sorted by
            path: :data:`DATA_PACKAGE`, then one ``schemas/<table>.json`` per table.
        """
        files = self.ohi_schema.frictionless(
            pruning_mode=self.pruning_mode,
            tree_root=self.tree_root,
            skip_classes_without_identifier=self.skip_classes_without_identifier,
        )
        return dict(sorted(files.items()))

    def as_dict(self) -> dict[str, Any]:
        """Generate the data package as one descriptor, with the table schemas in it.

        The bindings only give the separate files, so each table schema is put back into its
        resource here.

        :return: the parsed descriptor.
        """
        files = self.as_files()
        package = json.loads(files[DATA_PACKAGE])
        for resource in package["resources"]:
            resource["schema"] = json.loads(files[resource["schema"]])
        return package

    def serialize(self, **kwargs) -> str:
        """Generate the data package as one JSON document, with the table schemas in it.

        It's the same as what ohi LinkML's own CLI prints.

        :param kwargs: ignored, so the shared CLI options can be passed straight through.
        :return: the descriptor as JSON.
        """
        return json.dumps(self.as_dict(), indent=2, ensure_ascii=False)

    def write(self, directory: str | Path) -> list[Path]:
        """Write the data package to a directory, as :data:`DATA_PACKAGE` and one
        ``schemas/<table>.json`` per table.

        Files with the same name are replaced. The CSV files that the package refers to are not
        written.

        :param directory: where to write the files. Created if it does not exist.
        :return: the written files.
        """
        directory = Path(directory)
        written = []
        for name, content in self.as_files().items():
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            # Written as is, so that lines end with \n on Windows too.
            path.write_text(content, encoding="utf-8", newline="\n")
            written.append(path)
        return written


@shared_arguments(FrictionlessGenerator)
@click.option(
    "--pruning-mode",
    type=click.Choice(PRUNING_MODES),
    default="skip",
    show_default=True,
    help="Which classes become tables. "
    "tree_root - only the classes reachable from the tree_root class. "
    "schema - only the classes reachable from the classes defined in the root schema. "
    "skip - all classes.",
)
@click.option("--tree-root", help="Tree root class name to use instead of the schema-defined tree_root.")
@click.option(
    "--skip-classes-without-identifier",
    is_flag=True,
    help="Leave out the tables of classes with no identifier. Such a table has no primary key, so "
    "no other table can refer to it.",
)
@click.option(
    "-o", "--output", help="File to write the data package to, as one JSON document. Writes to stdout if not given."
)
@click.option(
    "-d",
    "--output-directory",
    type=click.Path(file_okay=False, path_type=Path),
    help="Directory to write the data package to, as datapackage.json plus one schemas/<table>.json per table.",
)
@click.option(
    "-V",
    "--version",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=print_versions,
    help="Show the linkml and ohi LinkML versions and exit.",
)
@click.command(name="frictionless")
def cli(yamlfile, output_directory, **args):
    """Generate a Frictionless Data Package from a LinkML model.

    Every concrete class becomes a CSV table with its own Table Schema, and references
    between classes become foreign keys. By default, the package is printed as one JSON document
    with the table schemas in it. Use --output to write it to a file instead, or
    --output-directory to write datapackage.json and one schemas/<table>.json per table.

    The generator is implemented in ohi LinkML, which is maintained separately. Please submit
    bug reports and feature requests to https://github.com/NeverBlink-OSS/ohi/issues
    """
    if output_directory is not None and args["output"]:
        raise click.UsageError("Give either --output or --output-directory, not both.")
    with FrictionlessGenerator(yamlfile, **args) as generator:
        if output_directory is not None:
            generator.write(output_directory)
        elif generator.output:
            Path(generator.output).write_text(generator.serialize(), encoding="utf-8", newline="\n")
        else:
            print(generator.serialize())


if __name__ == "__main__":
    cli()
