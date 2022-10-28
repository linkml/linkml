"""
Generate CSVs
"""
import os
import sys
from csv import DictWriter
from dataclasses import dataclass
from typing import List, Optional, Set, TextIO, Union

import click
from linkml_runtime.linkml_model.meta import (ClassDefinition,
                                              ClassDefinitionName,
                                              SchemaDefinition)
from linkml_runtime.utils.formatutils import be, underscore

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments


@dataclass
class CsvGenerator(Generator):
    """
    Generates CSV summaries

    Note: this generator is not widely used,
    and has largely been supplanted by schemasheets
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["csv", "tsv"]
    uses_schemaloader = True
    requires_metamodel = False

    # ObjectVars
    sep: Optional[str] = None
    """Separator for columns"""

    closure: Optional[
        Set[ClassDefinitionName]
    ] = None
    """List of classes to include in output"""

    writer: Optional[DictWriter] = None
    """Python dictwriter"""

    def __post_init__(self):
        super().__post_init__()
        self.generate_header()  # TODO: don't do this in initialization

    def generate_header(self):
        print(f"# metamodel_version: {self.schema.metamodel_version}")
        if self.schema.version:
            print(f"# version: {self.schema.version}")

    def visit_schema(self, classes: List[ClassDefinitionName] = None, **_) -> None:
        # Note: classes comes from the "root" argument
        self.closure = set()

        if classes is None:
            classes = []

        # Validate the supplied list of classes
        for clsname in classes:
            if clsname not in self.schema.classes:
                raise ValueError(f"Unrecognized class: {clsname}")
            else:
                self.closure.update(self.ancestors(self.schema.classes[clsname]))

        dialect: str = "excel" if self.format == "csv" else "excel-tab"
        self.writer = DictWriter(
            sys.stdout, ["id", "mappings", "description"], dialect=dialect
        )
        self.writer.writeheader()

    def visit_class(self, cls: ClassDefinition) -> bool:
        # TODO: find out what to do with mappings
        if not self.closure or cls.name in self.closure:
            self.writer.writerow(
                {
                    "id": underscore(cls.name),
                    # 'mappings': "|".join(cls.mappings),
                    "mappings": "",
                    "description": be(cls.description),
                }
            )
            return True
        return False


@shared_arguments(CsvGenerator)
@click.command()
@click.version_option(__version__, "-V", "--version")
@click.option("--root", "-r", multiple=True, help="Class(es) to transform")
def cli(yamlfile, root=None, **args):
    """Generate CSV/TSV file from LinkML model"""
    print(CsvGenerator(yamlfile, **args).serialize(classes=root, **args))


if __name__ == "__main__":
    cli()
