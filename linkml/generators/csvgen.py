"""
Generate CSVs
"""
import os
import sys
from csv import DictWriter
from typing import List, Union, TextIO, Set, Optional

import click

from linkml_runtime.linkml_model.meta import ClassDefinition, ClassDefinitionName, SchemaDefinition
from linkml_runtime.utils.formatutils import underscore, be
from linkml.utils.generator import Generator, shared_arguments


class CsvGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ['csv', 'tsv']

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], **kwargs) -> None:
        super().__init__(schema, **kwargs)
        self.sep: Optional[str] = None
        self.closure: Optional[Set[ClassDefinitionName]] = None       # List of classes to include in output
        self.writer: Optional[DictWriter] = None
        self.generate_header()

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

        dialect: str = "excel" if self.format == 'csv' else "excel-tab"
        self.writer = DictWriter(sys.stdout, ['id', 'mappings', 'description'], dialect=dialect)
        self.writer.writeheader()

    def visit_class(self, cls: ClassDefinition) -> bool:
        # TODO: find out what to do with mappings
        if not self.closure or cls.name in self.closure:
            self.writer.writerow({'id': underscore(cls.name),
                                  # 'mappings': "|".join(cls.mappings),
                                  'mappings': '',
                                  'description': be(cls.description)})
            return True
        return False


@shared_arguments(CsvGenerator)
@click.command()
@click.option("--root", "-r", multiple=True, help="Class(es) to transform")
def cli(yamlfile, root=None, **args):
    """ Generate CSV/TSV file from LinkML model """
    print(CsvGenerator(yamlfile, **args).serialize(classes=root, **args))


if __name__ == '__main__':
    cli()
