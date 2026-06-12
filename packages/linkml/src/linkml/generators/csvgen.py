"""
Generate CSVs
"""

import os
from csv import DictWriter
from dataclasses import dataclass
from io import StringIO

import click

from linkml._version import __version__
from linkml.utils.deprecation import deprecated_fields
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, ClassDefinitionName
from linkml_runtime.utils.formatutils import be, underscore


@deprecated_fields({"head": "metadata", "emit_metadata": "metadata"})
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
    uses_schemaloader = False

    # ObjectVars
    sep: str | None = None
    """Separator for columns"""

    closure: set[ClassDefinitionName] | None = None
    """List of classes to include in output"""

    writer: DictWriter | None = None
    """Python dictwriter"""

    _str_io: StringIO | None = None
    """String that the writer outputs to"""

    def serialize(self, classes: list[ClassDefinitionName] | None = None, **kwargs) -> str:
        """Generate a CSV/TSV summary of the schema's classes.

        :param classes: only include these classes and their is_a ancestors
        """
        sv = self.schemaview
        self.closure = set()
        for clsname in classes or []:
            if clsname not in sv.all_classes():
                msg = f"Unrecognized class: {clsname}"
                raise ValueError(msg)
            self.closure.update(sv.class_ancestors(clsname, mixins=False))

        self._str_io = StringIO()
        dialect: str = "excel" if self.format == "csv" else "excel-tab"
        self.writer = DictWriter(self._str_io, ["id", "mappings", "description"], dialect=dialect)
        self.writer.writeheader()
        # TODO: find out what to do with mappings
        for cls in sorted(sv.all_classes().values(), key=lambda c: c.name.casefold()):
            if not self.closure or cls.name in self.closure:
                self.writer.writerow(
                    {
                        "id": underscore(cls.name),
                        "mappings": "",
                        "description": be(cls.description),
                    }
                )
        return self._str_io.getvalue().rstrip() + "\n"


@shared_arguments(CsvGenerator)
@click.command(name="csv")
@click.version_option(__version__, "-V", "--version")
@click.option("--root", "-r", multiple=True, help="Class(es) to transform")
def cli(yamlfile, root=None, **args):
    """Generate CSV/TSV file from LinkML model"""
    print(CsvGenerator(yamlfile, **args).serialize(classes=root, **args))


if __name__ == "__main__":
    cli()
